"""Verify that bilingual notebook editing did not change released executable cells."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {path}")
    return value


def source_text(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    if isinstance(source, str):
        return source
    raise ValueError("Notebook cell source must be a string or list of strings.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("content/notebook_code_contract.json"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    contract = load_json(args.contract)
    notebook_path = Path(contract["notebook"])
    notebook = load_json(notebook_path)

    actual = {
        cell.get("id"): hashlib.sha256(source_text(cell).encode("utf-8")).hexdigest()
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    }
    expected = {
        item["id"]: item["sha256"]
        for item in contract.get("code_cells", [])
    }

    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    changed = sorted(
        cell_id for cell_id in set(expected) & set(actual)
        if expected[cell_id] != actual[cell_id]
    )

    report = {
        "status": "PASS" if not (missing or unexpected or changed) else "FAIL",
        "notebook": str(notebook_path),
        "source_release": contract.get("source_release"),
        "expected_code_cells": len(expected),
        "actual_code_cells": len(actual),
        "missing_code_cells": missing,
        "unexpected_code_cells": unexpected,
        "changed_code_cells": changed,
        "scope": (
            "Checks exact executable-cell bytes. Markdown and notebook metadata "
            "may change during bilingual conversion."
        ),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
