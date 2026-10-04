"""Validate phased Arabic-English learner content for SDA-DSC-211.

The manifest allows gradual conversion. Only entries marked ``complete`` are
blocking. Planned entries are reported so the migration remains visible.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
ENGLISH_RE = re.compile(r"[A-Za-z]")
# Editorial defects that should not enter the bilingual release.
JOINED_TOKEN_RE = re.compile(
    r"(?:اليوم|دفتر|من|على|إصدار|تجارب|مدة|حتى|سعة)(?:\d|CPU|GPU|Optuna|v\d)",
    re.IGNORECASE,
)


@dataclass
class Finding:
    level: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"level": self.level, "path": self.path, "message": self.message}


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def validate_markdown(root: Path, item: dict[str, Any]) -> list[Finding]:
    rel = item["path"]
    path = root / rel
    findings: list[Finding] = []
    if not path.is_file():
        return [Finding("error", rel, "File does not exist.")]
    text = path.read_text(encoding="utf-8-sig")
    for marker in item.get("required_markers", []):
        if marker not in text:
            findings.append(Finding("error", rel, f"Missing required marker: {marker}"))
    if not ARABIC_RE.search(text):
        findings.append(Finding("error", rel, "No Arabic learner content detected."))
    if not ENGLISH_RE.search(text):
        findings.append(Finding("error", rel, "No English learner content detected."))
    if JOINED_TOKEN_RE.search(text):
        findings.append(Finding("error", rel, "Joined Arabic/Latin token detected; add a space."))
    if '<td' in text and 'dir="ltr"' not in text:
        findings.append(Finding("error", rel, "Paired table lacks an explicit LTR block."))
    if '<td' in text and 'dir="rtl"' not in text:
        findings.append(Finding("error", rel, "Paired table lacks an explicit RTL block."))
    return findings


def validate_notebook(root: Path, item: dict[str, Any], rules: dict[str, Any]) -> list[Finding]:
    rel = item["path"]
    path = root / rel
    findings: list[Finding] = []
    if not path.is_file():
        return [Finding("error", rel, "Notebook does not exist.")]
    try:
        notebook = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return [Finding("error", rel, f"Invalid notebook JSON: {exc}")]

    pair_key = rules.get("notebook_pair_metadata_key", "bilingual_pair_id")
    order_key = rules.get("notebook_order_metadata_key", "bilingual_order")
    required_order = rules.get("required_notebook_order", "en-left-ar-right")
    pair_ids: list[str] = []
    paired_count = 0

    for index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "markdown":
            continue
        metadata = cell.get("metadata") or {}
        if pair_key not in metadata:
            continue
        paired_count += 1
        pair_id = metadata[pair_key]
        if not isinstance(pair_id, str) or not pair_id.strip():
            findings.append(Finding("error", rel, f"Cell {index}: invalid {pair_key}."))
        else:
            pair_ids.append(pair_id)
        if metadata.get(order_key) != required_order:
            findings.append(
                Finding("error", rel, f"Cell {index}: {order_key} must be {required_order}.")
            )
        source = "".join(cell.get("source", []))
        if 'dir="ltr"' not in source or 'dir="rtl"' not in source:
            findings.append(Finding("error", rel, f"Cell {index}: missing explicit LTR/RTL blocks."))
        if not ARABIC_RE.search(source) or not ENGLISH_RE.search(source):
            findings.append(Finding("error", rel, f"Cell {index}: both languages are required."))
        if JOINED_TOKEN_RE.search(source):
            findings.append(Finding("error", rel, f"Cell {index}: joined Arabic/Latin token detected."))

    minimum = int(item.get("minimum_paired_cells", 1))
    if paired_count < minimum:
        findings.append(
            Finding("error", rel, f"Expected at least {minimum} paired cells; found {paired_count}.")
        )
    duplicates = sorted({value for value in pair_ids if pair_ids.count(value) > 1})
    if duplicates:
        findings.append(Finding("error", rel, f"Duplicate bilingual pair IDs: {duplicates}"))
    return findings


def validate(root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = read_yaml(manifest_path)
    rules = manifest.get("rules") or {}
    enforce_complete_only = bool(rules.get("enforce_only_complete_items", True))
    findings: list[Finding] = []
    summary = {"complete": 0, "planned": 0, "other": 0}

    for kind in ("markdown_files", "notebooks"):
        for item in manifest.get(kind, []):
            status = str(item.get("status", "planned"))
            summary[status if status in summary else "other"] += 1
            if enforce_complete_only and status != "complete":
                findings.append(Finding("info", item["path"], f"Migration status: {status}."))
                continue
            if kind == "markdown_files":
                findings.extend(validate_markdown(root, item))
            else:
                findings.extend(validate_notebook(root, item, rules))

    errors = [finding for finding in findings if finding.level == "error"]
    return {
        "status": "PASS" if not errors else "FAIL",
        "release_target": manifest.get("release_target"),
        "summary": summary,
        "errors": len(errors),
        "findings": [finding.as_dict() for finding in findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--manifest", type=Path, default=Path("content/bilingual_manifest.yml")
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    report = validate(root, manifest_path)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
