"""Execute Day 3 from the candidate and released reference, then compare stable outputs."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any

import nbformat
import numpy as np
import pandas as pd
from nbclient import NotebookClient

NOTEBOOK = Path("notebooks/03_cost_sensitive_decision.ipynb")
FRAME_SPECS: dict[str, list[str]] = {
    "day3_model_report.csv": ["train_seconds"],
    "day3_model_comparison.csv": [],
    "day3_oof_predictions.csv": [],
    "day3_oof_coverage.csv": [],
    "threshold_sweep.csv": [],
    "day3_review_flags.csv": [],
    "day3_period_capacity.csv": [],
    "day3_region_audit.csv": [],
    "day3_cost_sensitivity.csv": [],
}
JSON_FILES = {
    "threshold_metrics.json",
    "day3_provenance.json",
    "day3_reflection.json",
    "day3_run.json",
}
VOLATILE_JSON_KEYS = {
    "elapsed_seconds",
    "train_seconds",
    "training_seconds",
    "run_seconds",
    "runtime_seconds",
    "total_seconds",
}
ARTIFACT_FILES = {
    "environment.json",
    "day3_model_report.csv",
    "day3_model_comparison.csv",
    "day3_oof_predictions.csv",
    "day3_oof_coverage.csv",
    "threshold_sweep.csv",
    "day3_review_flags.csv",
    "day3_period_capacity.csv",
    "day3_region_audit.csv",
    "day3_cost_sensitivity.csv",
    "threshold_metrics.json",
    "day3_provenance.json",
    "day3_reflection.json",
    "day3_run.json",
    "cost_curve.png",
    "day3_roc_pr.png",
    "day3_capacity_regions.png",
    "day3_artifacts.zip",
}
REPORT_FILE = Path("reports/DECISION_CARD.md")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def execute(repo_root: Path, workspace: Path) -> tuple[Path, float]:
    workspace.mkdir(parents=True, exist_ok=True)
    notebook = nbformat.read(repo_root / NOTEBOOK, as_version=4)
    adapted = 0
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        lines = cell.source.splitlines()
        for index, line in enumerate(lines):
            if line.startswith("ROOT = ") and "TAMWEEL_PROJECT_DIR" in line:
                lines[index] = 'ROOT = Path(os.environ["TAMWEEL_PROJECT_DIR"]).resolve()'
                adapted += 1
        cell.source = "\n".join(lines)
    if adapted != 1:
        raise ValueError(
            f"Expected one workspace adapter in {repo_root / NOTEBOOK}; found {adapted}"
        )

    previous = os.environ.copy()
    os.environ.update(
        ASSESSMENT_MODE="1",
        TAMWEEL_PROJECT_DIR=str(workspace),
        OMP_NUM_THREADS="2",
        OPENBLAS_NUM_THREADS="2",
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONIOENCODING="utf-8",
    )
    started = time.perf_counter()
    try:
        NotebookClient(
            notebook,
            timeout=300,
            kernel_name="python3",
            resources={"metadata": {"path": str(workspace)}},
        ).execute()
    finally:
        os.environ.clear()
        os.environ.update(previous)
    return workspace, round(time.perf_counter() - started, 3)


def compare_frame(
    reference: pd.DataFrame,
    candidate: pd.DataFrame,
    *,
    exclude: list[str],
    numeric_tolerance: float = 1e-10,
) -> list[str]:
    issues: list[str] = []
    reference = reference.drop(columns=exclude, errors="ignore").reset_index(drop=True)
    candidate = candidate.drop(columns=exclude, errors="ignore").reset_index(drop=True)
    if list(reference.columns) != list(candidate.columns):
        return [
            "Column mismatch: "
            f"reference={list(reference.columns)}, candidate={list(candidate.columns)}"
        ]
    if len(reference) != len(candidate):
        return [f"Row-count mismatch: {len(reference)} != {len(candidate)}"]

    for column in reference.columns:
        left = reference[column]
        right = candidate[column]
        if pd.api.types.is_numeric_dtype(left) and pd.api.types.is_numeric_dtype(right):
            if not np.allclose(
                pd.to_numeric(left, errors="coerce").to_numpy(dtype=float),
                pd.to_numeric(right, errors="coerce").to_numpy(dtype=float),
                rtol=numeric_tolerance,
                atol=1e-12,
                equal_nan=True,
            ):
                issues.append(f"Numeric mismatch in {column}")
        elif not left.fillna("<NA>").astype(str).equals(
            right.fillna("<NA>").astype(str)
        ):
            issues.append(f"Value mismatch in {column}")
    return issues


def sanitized(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: sanitized(item)
            for key, item in sorted(value.items())
            if key not in VOLATILE_JSON_KEYS
        }
    if isinstance(value, list):
        return [sanitized(item) for item in value]
    if isinstance(value, float) and np.isnan(value):
        return "<NaN>"
    return value


def normalized_text(path: Path) -> str:
    return "\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()).strip()


def compare_workspace(reference_root: Path, candidate_root: Path) -> dict[str, Any]:
    issues: list[str] = []
    comparisons: dict[str, Any] = {}
    reference_artifacts = reference_root / "artifacts"
    candidate_artifacts = candidate_root / "artifacts"

    for label, folder in (("reference", reference_artifacts), ("candidate", candidate_artifacts)):
        missing = sorted(name for name in ARTIFACT_FILES if not (folder / name).is_file())
        if missing:
            issues.append(f"{label} missing required artifacts: {missing}")
        if not (reference_root if label == "reference" else candidate_root).joinpath(REPORT_FILE).is_file():
            issues.append(f"{label} missing required report: {REPORT_FILE.as_posix()}")

    if issues:
        return {"status": "FAIL", "issues": issues, "comparisons": comparisons}

    for filename, exclude in FRAME_SPECS.items():
        reference_frame = pd.read_csv(reference_artifacts / filename)
        candidate_frame = pd.read_csv(candidate_artifacts / filename)
        frame_issues = compare_frame(reference_frame, candidate_frame, exclude=exclude)
        issues.extend(f"{filename}: {issue}" for issue in frame_issues)
        comparisons[filename] = {
            "reference_rows": len(reference_frame),
            "candidate_rows": len(candidate_frame),
            "excluded_volatile_columns": exclude,
        }

    for filename in sorted(JSON_FILES):
        reference_json = sanitized(read_json(reference_artifacts / filename))
        candidate_json = sanitized(read_json(candidate_artifacts / filename))
        if reference_json != candidate_json:
            issues.append(f"{filename}: stable JSON content differs")
        comparisons[filename] = {
            "excluded_volatile_keys": sorted(VOLATILE_JSON_KEYS),
        }

    reference_card = normalized_text(reference_root / REPORT_FILE)
    candidate_card = normalized_text(candidate_root / REPORT_FILE)
    if reference_card != candidate_card:
        issues.append(f"{REPORT_FILE.as_posix()}: generated decision card differs")
    comparisons[REPORT_FILE.as_posix()] = {
        "reference_characters": len(reference_card),
        "candidate_characters": len(candidate_card),
    }

    reference_run = read_json(reference_artifacts / "day3_run.json")
    candidate_run = read_json(candidate_artifacts / "day3_run.json")
    comparisons["run_status"] = {
        "reference_technical_status": reference_run.get("technical_status"),
        "candidate_technical_status": candidate_run.get("technical_status"),
        "reference_oof_coverage": reference_run.get("oof_whole_data_coverage"),
        "candidate_oof_coverage": candidate_run.get("oof_whole_data_coverage"),
        "reference_example_only": reference_run.get("example_only"),
        "candidate_example_only": candidate_run.get("example_only"),
    }

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "comparisons": comparisons,
        "required_artifacts": sorted(ARTIFACT_FILES),
        "required_report": REPORT_FILE.as_posix(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-root", type=Path, default=Path.cwd())
    parser.add_argument("--reference-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    candidate_repo = args.candidate_root.resolve()
    reference_repo = args.reference_root.resolve()
    with tempfile.TemporaryDirectory(prefix="day3-parity-") as temp:
        temp_root = Path(temp)
        reference_workspace, reference_seconds = execute(
            reference_repo, temp_root / "reference-workspace"
        )
        candidate_workspace, candidate_seconds = execute(
            candidate_repo, temp_root / "candidate-workspace"
        )
        report = compare_workspace(reference_workspace, candidate_workspace)
        report.update(
            {
                "reference": "main / released v1.0.0 learner notebook",
                "candidate": "develop/bilingual-v1.1.0",
                "reference_seconds": reference_seconds,
                "candidate_seconds": candidate_seconds,
                "scope": (
                    "Compares stable Day 3 model, OOF, threshold, capacity, sensitivity, "
                    "regional-audit, provenance and decision-card outputs. Training/runtime "
                    "timing fields and image bytes are intentionally excluded."
                ),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
