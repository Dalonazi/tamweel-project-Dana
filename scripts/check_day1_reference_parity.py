"""Execute Day 1 from the candidate and released reference, then compare stable outputs."""
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


NOTEBOOK = Path("notebooks/01_baseline_boosting.ipynb")
STABLE_MODEL_COLUMNS = [
    "model",
    "roc_auc",
    "average_precision",
    "selected_trees",
    "comparison_rows",
    "positive_rate",
]
STABLE_RUN_KEYS = [
    "technical_status",
    "data_revision",
    "lab_revision",
    "lab_sha256",
    "data_manifest_sha256",
    "training_file_sha256",
    "config",
    "mode",
    "split",
    "split_method",
    "shared_customers",
    "ap_definition",
]


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {path}")
    return value


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
        raise ValueError(f"Expected one workspace adapter in {repo_root / NOTEBOOK}; found {adapted}")

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
            timeout=180,
            kernel_name="python3",
            resources={"metadata": {"path": str(workspace)}},
        ).execute()
    finally:
        os.environ.clear()
        os.environ.update(previous)
    return workspace / "artifacts", round(time.perf_counter() - started, 3)


def compare_frame(
    reference: pd.DataFrame,
    candidate: pd.DataFrame,
    *,
    key: str,
    numeric_tolerance: float = 1e-10,
) -> list[str]:
    issues: list[str] = []
    reference = reference.sort_values(key).reset_index(drop=True)
    candidate = candidate.sort_values(key).reset_index(drop=True)
    if list(reference.columns) != list(candidate.columns):
        issues.append(
            f"Column mismatch for {key}: reference={list(reference.columns)}, candidate={list(candidate.columns)}"
        )
        return issues
    if len(reference) != len(candidate):
        issues.append(f"Row-count mismatch for {key}: {len(reference)} != {len(candidate)}")
        return issues
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
                issues.append(f"Numeric mismatch in {key}.{column}")
        elif not left.fillna("<NA>").astype(str).equals(
            right.fillna("<NA>").astype(str)
        ):
            issues.append(f"Value mismatch in {key}.{column}")
    return issues


def compare_artifacts(reference: Path, candidate: Path) -> dict[str, Any]:
    issues: list[str] = []

    reference_models = pd.read_csv(reference / "day1_model_comparison.csv")
    candidate_models = pd.read_csv(candidate / "day1_model_comparison.csv")
    missing_columns = sorted(set(STABLE_MODEL_COLUMNS) - set(reference_models.columns))
    if missing_columns:
        issues.append(f"Reference model table lacks stable columns: {missing_columns}")
    else:
        issues.extend(
            compare_frame(
                reference_models[STABLE_MODEL_COLUMNS],
                candidate_models[STABLE_MODEL_COLUMNS],
                key="model",
            )
        )

    reference_predictions = pd.read_csv(reference / "day1_comparison_predictions.csv")
    candidate_predictions = pd.read_csv(candidate / "day1_comparison_predictions.csv")
    issues.extend(
        compare_frame(
            reference_predictions,
            candidate_predictions,
            key="application_id",
        )
    )

    reference_membership = pd.read_csv(reference / "day1_split_membership.csv")
    candidate_membership = pd.read_csv(candidate / "day1_split_membership.csv")
    issues.extend(
        compare_frame(
            reference_membership,
            candidate_membership,
            key="application_id",
        )
    )

    reference_run = read_json(reference / "day1_run.json")
    candidate_run = read_json(candidate / "day1_run.json")
    for key in STABLE_RUN_KEYS:
        if reference_run.get(key) != candidate_run.get(key):
            issues.append(f"Stable run metadata mismatch: {key}")

    required = {
        "environment.json",
        "day1_model_comparison.csv",
        "day1_comparison_predictions.csv",
        "day1_split_membership.csv",
        "day1_learning_curves.png",
        "day1_roc_pr.png",
        "day1_reflection.json",
        "day1_run.json",
        "day1_artifacts.zip",
    }
    for label, folder in (("reference", reference), ("candidate", candidate)):
        missing = sorted(name for name in required if not (folder / name).is_file())
        if missing:
            issues.append(f"{label} missing required artifacts: {missing}")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "comparisons": {
            "model_metrics": "stable scientific columns",
            "prediction_rows": len(reference_predictions),
            "split_rows": len(reference_membership),
            "stable_run_keys": STABLE_RUN_KEYS,
            "required_artifacts": sorted(required),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-root", type=Path, default=Path.cwd())
    parser.add_argument("--reference-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    candidate_root = args.candidate_root.resolve()
    reference_root = args.reference_root.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    try:
        with tempfile.TemporaryDirectory(prefix="day1-parity-") as temp:
            temp_root = Path(temp)
            reference_artifacts, reference_seconds = execute(
                reference_root, temp_root / "reference-workspace"
            )
            candidate_artifacts, candidate_seconds = execute(
                candidate_root, temp_root / "candidate-workspace"
            )
            report = compare_artifacts(reference_artifacts, candidate_artifacts)
            report.update(
                {
                    "reference": "main / released v1.0.0 learner notebook",
                    "candidate": "develop/bilingual-v1.1.0",
                    "reference_seconds": reference_seconds,
                    "candidate_seconds": candidate_seconds,
                    "scope": (
                        "Compares stable scientific outputs and required artifact inventory. "
                        "Timing fields and image bytes are intentionally excluded."
                    ),
                }
            )
    except Exception as exc:
        report = {
            "status": "ERROR",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "reference": "main / released v1.0.0 learner notebook",
            "candidate": "develop/bilingual-v1.1.0",
        }

    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
