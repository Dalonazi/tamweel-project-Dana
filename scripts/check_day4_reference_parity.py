"""Execute Day 4 from the bilingual candidate and released reference, then compare stable outputs."""
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

NOTEBOOK = Path("notebooks/04_explain_calibrate.ipynb")

CSV_FILES = [
    "day4_roles.csv",
    "day4_predictions.csv",
    "permutation_importance.csv",
    "day4_shap_global.csv",
    "day4_reason_codes.csv",
    "day4_local_stability.csv",
    "day4_reliability_bins.csv",
    "day4_period_metrics.csv",
    "day4_bootstrap.csv",
    "day4_policy_sweep.csv",
    "day4_review_flags.csv",
    "day4_capacity.csv",
]

JSON_FILES = [
    "calibration_metrics.json",
    "day4_shap_metadata.json",
    "day4_stability_summary.json",
    "day4_provenance.json",
    "day4_reflection.json",
    "day4_run.json",
]

FIGURES = [
    "permutation_importance.png",
    "shap_beeswarm.png",
    "shap_waterfall.png",
    "reliability_curve.png",
    "stability_summary.png",
    "review_zone.png",
]

REQUIRED_ARTIFACTS = set(
    CSV_FILES
    + JSON_FILES
    + FIGURES
    + [
        "environment.json",
        "shap_values_sample.npz",
        "day4_model.txt",
        "day4_artifacts.zip",
    ]
)
REQUIRED_REPORT = Path("reports/INTERPRETABILITY_REPORT.md")
VOLATILE_KEYS = {
    "elapsed_seconds",
    "run_seconds",
    "runtime_seconds",
    "total_seconds",
    "train_seconds",
    "training_seconds",
    "fit_seconds",
    "calibration_seconds",
    "shap_seconds",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def execute(repo_root: Path, workspace: Path) -> tuple[Path, Path, float]:
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
            timeout=360,
            kernel_name="python3",
            resources={"metadata": {"path": str(workspace)}},
        ).execute()
    finally:
        os.environ.clear()
        os.environ.update(previous)

    return (
        workspace / "artifacts",
        workspace / REQUIRED_REPORT,
        round(time.perf_counter() - started, 3),
    )


def compare_frame(reference: pd.DataFrame, candidate: pd.DataFrame) -> list[str]:
    issues: list[str] = []
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
            left_values = pd.to_numeric(left, errors="coerce").to_numpy(dtype=float)
            right_values = pd.to_numeric(right, errors="coerce").to_numpy(dtype=float)
            if not np.allclose(
                left_values,
                right_values,
                rtol=1e-10,
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
            if key not in VOLATILE_KEYS
        }
    if isinstance(value, list):
        return [sanitized(item) for item in value]
    if isinstance(value, float) and np.isnan(value):
        return "<NaN>"
    return value


def normalize_text(path: Path) -> str:
    return "\n".join(
        line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
    ).strip()


def compare_npz(reference_path: Path, candidate_path: Path) -> list[str]:
    issues: list[str] = []
    with np.load(reference_path, allow_pickle=False) as reference, np.load(
        candidate_path, allow_pickle=False
    ) as candidate:
        if set(reference.files) != set(candidate.files):
            return [
                f"NPZ keys differ: reference={sorted(reference.files)}, "
                f"candidate={sorted(candidate.files)}"
            ]
        for key in sorted(reference.files):
            left = reference[key]
            right = candidate[key]
            if left.shape != right.shape:
                issues.append(f"{key}: shape mismatch {left.shape} != {right.shape}")
                continue
            if np.issubdtype(left.dtype, np.number) and np.issubdtype(
                right.dtype, np.number
            ):
                if not np.allclose(
                    left.astype(float),
                    right.astype(float),
                    rtol=1e-10,
                    atol=1e-12,
                    equal_nan=True,
                ):
                    issues.append(f"{key}: numeric values differ")
            elif not np.array_equal(left, right):
                issues.append(f"{key}: values differ")
    return issues


def compare_outputs(
    reference_artifacts: Path,
    candidate_artifacts: Path,
    reference_report: Path,
    candidate_report: Path,
) -> dict[str, Any]:
    issues: list[str] = []
    comparisons: dict[str, Any] = {}

    for label, folder in (
        ("reference", reference_artifacts),
        ("candidate", candidate_artifacts),
    ):
        missing = sorted(name for name in REQUIRED_ARTIFACTS if not (folder / name).is_file())
        if missing:
            issues.append(f"{label} missing required artifacts: {missing}")

    for label, report in (
        ("reference", reference_report),
        ("candidate", candidate_report),
    ):
        if not report.is_file():
            issues.append(f"{label} missing required report: {report}")

    if issues:
        return {"status": "FAIL", "issues": issues, "comparisons": comparisons}

    for filename in CSV_FILES:
        reference_frame = pd.read_csv(reference_artifacts / filename)
        candidate_frame = pd.read_csv(candidate_artifacts / filename)
        frame_issues = compare_frame(reference_frame, candidate_frame)
        issues.extend(f"{filename}: {issue}" for issue in frame_issues)
        comparisons[filename] = {
            "reference_rows": len(reference_frame),
            "candidate_rows": len(candidate_frame),
            "columns": list(reference_frame.columns),
        }

    for filename in JSON_FILES:
        reference_json = sanitized(read_json(reference_artifacts / filename))
        candidate_json = sanitized(read_json(candidate_artifacts / filename))
        if reference_json != candidate_json:
            issues.append(
                f"{filename}: stable JSON content differs after removing volatile timing keys"
            )
        comparisons[filename] = {
            "excluded_volatile_keys": sorted(VOLATILE_KEYS)
        }

    npz_issues = compare_npz(
        reference_artifacts / "shap_values_sample.npz",
        candidate_artifacts / "shap_values_sample.npz",
    )
    issues.extend(f"shap_values_sample.npz: {issue}" for issue in npz_issues)
    with np.load(reference_artifacts / "shap_values_sample.npz", allow_pickle=False) as ref_npz:
        comparisons["shap_values_sample.npz"] = {
            "keys": sorted(ref_npz.files),
            "shapes": {key: list(ref_npz[key].shape) for key in ref_npz.files},
        }

    reference_model = (reference_artifacts / "day4_model.txt").read_text(encoding="utf-8")
    candidate_model = (candidate_artifacts / "day4_model.txt").read_text(encoding="utf-8")
    if reference_model != candidate_model:
        issues.append("day4_model.txt: saved model text differs")
    comparisons["day4_model.txt"] = {
        "reference_characters": len(reference_model),
        "candidate_characters": len(candidate_model),
    }

    reference_report_text = normalize_text(reference_report)
    candidate_report_text = normalize_text(candidate_report)
    if reference_report_text != candidate_report_text:
        issues.append("reports/INTERPRETABILITY_REPORT.md: normalized text differs")
    comparisons["reports/INTERPRETABILITY_REPORT.md"] = {
        "reference_characters": len(reference_report_text),
        "candidate_characters": len(candidate_report_text),
    }

    reference_run = read_json(reference_artifacts / "day4_run.json")
    candidate_run = read_json(candidate_artifacts / "day4_run.json")
    comparisons["run_status"] = {
        "reference_technical_status": reference_run.get("technical_status"),
        "candidate_technical_status": candidate_run.get("technical_status"),
        "reference_explanation_source": reference_run.get("explanation_source"),
        "candidate_explanation_source": candidate_run.get("explanation_source"),
        "reference_capacity_status": reference_run.get("capacity_status"),
        "candidate_capacity_status": candidate_run.get("capacity_status"),
    }

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "comparisons": comparisons,
        "required_artifacts": sorted(REQUIRED_ARTIFACTS),
        "required_report": str(REQUIRED_REPORT),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-root", type=Path, default=Path.cwd())
    parser.add_argument("--reference-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    candidate_root = args.candidate_root.resolve()
    reference_root = args.reference_root.resolve()

    with tempfile.TemporaryDirectory(prefix="day4-parity-") as temp:
        temp_root = Path(temp)
        reference_artifacts, reference_report, reference_seconds = execute(
            reference_root, temp_root / "reference-workspace"
        )
        candidate_artifacts, candidate_report, candidate_seconds = execute(
            candidate_root, temp_root / "candidate-workspace"
        )
        report = compare_outputs(
            reference_artifacts,
            candidate_artifacts,
            reference_report,
            candidate_report,
        )
        report.update(
            {
                "reference": "main / released v1.0.0 learner notebook",
                "candidate": "develop/bilingual-v1.1.0",
                "reference_seconds": reference_seconds,
                "candidate_seconds": candidate_seconds,
                "scope": (
                    "Compares stable Day 4 role, prediction, permutation, SHAP, "
                    "calibration, stability, policy, capacity, provenance and "
                    "interpretability-report outputs. Runtime timing fields and "
                    "PNG bytes are intentionally excluded."
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
