"""Build a deterministic integrity manifest for the frozen learner release.

The manifest intentionally excludes its own file and does not embed a commit SHA,
which avoids a circular hash dependency. The final Git tag and exact commit SHA are
recorded separately in the release record and private submission registry.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def is_excluded(relative: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(relative, pattern) for pattern in patterns)


def collect_files(root: Path, include: list[str], exclude: list[str]) -> list[Path]:
    """Resolve files from file globs and directory globs deterministically.

    ``Path.glob('directory/**')`` can yield directories rather than their files.
    When an include pattern resolves to a directory, recurse through it explicitly so
    release manifests cannot silently omit nested scripts, data or workflows.
    """
    selected: dict[str, Path] = {}

    def add_file(path: Path) -> None:
        if not path.is_file():
            return
        relative = path.relative_to(root).as_posix()
        if is_excluded(relative, exclude):
            return
        selected[relative] = path

    for pattern in include:
        for path in root.glob(pattern):
            if path.is_dir():
                for child in path.rglob("*"):
                    add_file(child)
            else:
                add_file(path)
    return [selected[key] for key in sorted(selected)]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_manifest(root: Path, scope_path: Path) -> dict[str, Any]:
    scope = read_json(scope_path)
    include = [str(item) for item in scope.get("include", [])]
    exclude = [str(item) for item in scope.get("exclude", [])]
    maximum = int(scope.get("maximum_file_bytes", 104857600))
    files = collect_files(root, include, exclude)
    if not files:
        raise RuntimeError("Release scope selected no files.")

    entries: list[dict[str, Any]] = []
    aggregate = hashlib.sha256()
    for path in files:
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise RuntimeError(f"Symlinks are not allowed in the release scope: {relative}")
        size = path.stat().st_size
        if size > maximum:
            raise RuntimeError(f"File exceeds the release size ceiling: {relative} ({size} bytes)")
        digest = sha256(path)
        entries.append({"path": relative, "bytes": size, "sha256": digest})
        aggregate.update(relative.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(str(size).encode("ascii"))
        aggregate.update(b"\0")
        aggregate.update(digest.encode("ascii"))
        aggregate.update(b"\n")

    return {
        "schema_version": 1,
        "release_version": scope["release_version"],
        "repository": scope["repository"],
        "file_count": len(entries),
        "aggregate_sha256": aggregate.hexdigest(),
        "files": entries,
        "notes": (
            "Integrity inventory only. The final immutable Git tag and exact commit SHA "
            "are recorded outside this file to avoid a circular self-reference."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--scope",
        type=Path,
        default=Path("release/release_scope.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("check-output/release_manifest.json"),
    )
    parser.add_argument(
        "--verify",
        type=Path,
        help="Compare the generated manifest with an existing committed manifest.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    scope_path = args.scope if args.scope.is_absolute() else root / args.scope
    manifest = build_manifest(root, scope_path)
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    output.write_text(payload, encoding="utf-8")

    if args.verify:
        expected_path = args.verify if args.verify.is_absolute() else root / args.verify
        expected = read_json(expected_path)
        if expected != manifest:
            raise SystemExit(
                "RELEASE_MANIFEST_MISMATCH: regenerate after the learner-facing files are frozen."
            )
        print("RELEASE_MANIFEST_VERIFIED")
    else:
        print(
            f"RELEASE_MANIFEST_CREATED: {manifest['file_count']} files; "
            f"aggregate={manifest['aggregate_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
