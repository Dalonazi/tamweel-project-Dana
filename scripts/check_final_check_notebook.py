"""Validate Notebook 99 structure, bilingual metadata and released executable-cell contract."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_ORDER = "en-left-ar-right"
REQUIRED_PAIRS = {
    "final_check_header",
    "final_check_source",
    "final_check_tools",
    "final_check_snapshot",
    "final_check_run",
    "final_check_save",
}
REQUIRED_CODE_SIGNALS = {
    "PROJECT_REPOSITORY",
    "PROJECT_SHA",
    "PROJECT_ZIP",
    "CHECK_REVISION",
    "CHECK_HASHES",
    "ASSESSMENT_MODE",
    "extract_project",
    "100*1024*1024",
    "scripts/final_check.py",
    "self_check_report.json",
    "final_project_bundle.zip",
    "files.download",
}
FORBIDDEN_SIGNALS = {
    "drive.mount",
    "getpass.getpass",
    "GITHUB_TOKEN",
}


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
    parser.add_argument("--notebook", type=Path, default=Path("notebooks/99_final_submission_check.ipynb"))
    parser.add_argument("--contract", type=Path, default=Path("content/notebook99_code_contract.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    notebook = load_json(args.notebook)
    contract = load_json(args.contract)
    issues: list[str] = []
    code_cells = [cell for cell in notebook.get("cells", []) if cell.get("cell_type") == "code"]
    markdown_cells = [cell for cell in notebook.get("cells", []) if cell.get("cell_type") == "markdown"]

    expected = {item["id"]: item["sha256"] for item in contract.get("code_cells", [])}
    actual: dict[str, str] = {}
    all_code: list[str] = []
    for cell in code_cells:
        cell_id = cell.get("id")
        source = source_text(cell)
        all_code.append(source)
        if not isinstance(cell_id, str) or not cell_id:
            issues.append("Executable cell without stable id")
            continue
        actual[cell_id] = hashlib.sha256(source.encode("utf-8")).hexdigest()
        try:
            ast.parse(source)
        except SyntaxError as exc:
            issues.append(f"{cell_id}: syntax error at line {exc.lineno}: {exc.msg}")
        if cell.get("execution_count") is not None:
            issues.append(f"{cell_id}: execution_count must be null in source notebook")
        if cell.get("outputs"):
            issues.append(f"{cell_id}: source notebook must not contain outputs")

    missing_code = sorted(set(expected) - set(actual))
    unexpected_code = sorted(set(actual) - set(expected))
    changed_code = sorted(
        cell_id for cell_id in set(expected) & set(actual) if expected[cell_id] != actual[cell_id]
    )
    if missing_code:
        issues.append(f"Missing executable cells: {missing_code}")
    if unexpected_code:
        issues.append(f"Unexpected executable cells: {unexpected_code}")
    if changed_code:
        issues.append(f"Changed executable cells: {changed_code}")

    pairs: list[str] = []
    for cell in markdown_cells:
        metadata = cell.get("metadata", {})
        pair_id = metadata.get("bilingual_pair_id") if isinstance(metadata, dict) else None
        order = metadata.get("bilingual_order") if isinstance(metadata, dict) else None
        text = source_text(cell)
        if not isinstance(pair_id, str) or not pair_id:
            issues.append(f"Markdown cell {cell.get('id')} lacks bilingual_pair_id")
            continue
        pairs.append(pair_id)
        if order != REQUIRED_ORDER:
            issues.append(f"{pair_id}: bilingual_order must be {REQUIRED_ORDER}")
        if 'dir="ltr"' not in text or 'dir="rtl"' not in text:
            issues.append(f"{pair_id}: missing explicit LTR/RTL columns")
        if not metadata.get("learner_facing"):
            issues.append(f"{pair_id}: learner_facing must be true")
        if metadata.get("content_version") != "1.1.0":
            issues.append(f"{pair_id}: content_version must be 1.1.0")

    if set(pairs) != REQUIRED_PAIRS:
        issues.append(
            f"Bilingual pair mismatch: missing={sorted(REQUIRED_PAIRS - set(pairs))}, "
            f"unexpected={sorted(set(pairs) - REQUIRED_PAIRS)}"
        )
    if len(pairs) != len(set(pairs)):
        issues.append("Duplicate bilingual pair ids")

    code_blob = "\n".join(all_code)
    missing_signals = sorted(signal for signal in REQUIRED_CODE_SIGNALS if signal not in code_blob)
    forbidden_signals = sorted(signal for signal in FORBIDDEN_SIGNALS if signal in code_blob)
    if missing_signals:
        issues.append(f"Missing final-check safety/behavior signals: {missing_signals}")
    if forbidden_signals:
        issues.append(f"Forbidden secret/account integration signals: {forbidden_signals}")

    metadata = notebook.get("metadata", {})
    if metadata.get("bilingual_order") != REQUIRED_ORDER:
        issues.append("Notebook metadata bilingual_order is missing or incorrect")
    if metadata.get("bilingual_content_version") != "1.1.0":
        issues.append("Notebook metadata bilingual_content_version is missing or incorrect")

    report = {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "notebook": str(args.notebook),
        "code_cells": len(code_cells),
        "contract_cells": len(expected),
        "paired_sections": len(pairs),
        "pair_ids": pairs,
        "missing_code_cells": missing_code,
        "unexpected_code_cells": unexpected_code,
        "changed_code_cells": changed_code,
        "required_code_signals": sorted(REQUIRED_CODE_SIGNALS),
        "execution_scope": (
            "Static and contract validation only. Full live behavior depends on a learner project "
            "snapshot, network access and Colab upload/download interactions."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
