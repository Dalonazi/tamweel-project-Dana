"""Execute Day 5 from the bilingual candidate and released reference, then compare stable outputs."""
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

NOTEBOOK = Path("notebooks/05_final_model.ipynb")
CSV_PATHS = [
    "artifacts/day5_roles.csv",
    "artifacts/day5_oof_predictions.csv",
    "artifacts/day5_fold_scores.csv",
    "artifacts/ensemble_comparison.csv",
    "artifacts/day5_threshold_sweep.csv",
    "artifacts/day5_region_audit.csv",
    "artifacts/day5_period_capacity.csv",
    "artifacts/day5_cost_sensitivity.csv",
    "artifacts/day5_probability_correlation.csv",
    "artifacts/day5_residual_correlation.csv",
    "artifacts/day5_calibration_predictions.csv",
    "artifacts/day5_calibration_fit_bins.csv",
    "submission/submission.csv",
]
JSON_PATHS = [
    "artifacts/day5_run.json",
    "artifacts/day5_reflection.json",
    "artifacts/day5_oof_provenance.json",
    "artifacts/day5_ensemble_gate.json",
    "artifacts/final_policy.json",
    "artifacts/final_metrics.json",
    "artifacts/day5_final_provenance.json",
    "artifacts/day5_project_check.json",
]
TEXT_PATHS = [
    "PROJECT_README.md",
    "reports/MODEL_CARD.md",
    "reports/ENSEMBLE_DECISION.md",
]
FIGURES = [
    "artifacts/day5_diversity.png",
    "artifacts/day5_ensemble_comparison.png",
    "artifacts/day5_policy_regions.png",
    "artifacts/day5_calibration_fit.png",
    "artifacts/day5_challenge_capacity.png",
]
REQUIRED_ONLY = [
    "artifacts/environment.json",
    "submission/submission_manifest.json",
    "submission/project_bundle.zip",
]
VOLATILE_KEYS = {
    "elapsed_seconds",
    "runtime_seconds",
    "run_seconds",
    "total_seconds",
    "train_seconds",
    "training_seconds",
    "fit_seconds",
    "seconds",
}


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
        raise ValueError(f"Expected one workspace adapter; found {adapted}")

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
            timeout=600,
            kernel_name="python3",
            resources={"metadata": {"path": str(workspace)}},
        ).execute()
    finally:
        os.environ.clear()
        os.environ.update(previous)
    return workspace, round(time.perf_counter() - started, 3)


def compare_frame(reference: pd.DataFrame, candidate: pd.DataFrame) -> list[str]:
    if list(reference.columns) != list(candidate.columns):
        return [f"column mismatch: {list(reference.columns)} != {list(candidate.columns)}"]
    if len(reference) != len(candidate):
        return [f"row-count mismatch: {len(reference)} != {len(candidate)}"]
    issues: list[str] = []
    for column in reference.columns:
        left, right = reference[column], candidate[column]
        if pd.api.types.is_numeric_dtype(left) and pd.api.types.is_numeric_dtype(right):
            if not np.allclose(
                pd.to_numeric(left, errors="coerce").to_numpy(float),
                pd.to_numeric(right, errors="coerce").to_numpy(float),
                rtol=1e-10,
                atol=1e-12,
                equal_nan=True,
            ):
                issues.append(f"numeric mismatch in {column}")
        elif not left.fillna("<NA>").astype(str).equals(right.fillna("<NA>").astype(str)):
            issues.append(f"value mismatch in {column}")
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


def normalized_text(path: Path) -> str:
    return "\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()).strip()


def model_files(root: Path) -> list[Path]:
    folder = root / "artifacts/final_model"
    if not folder.is_dir():
        return []
    return sorted(path.relative_to(root) for path in folder.rglob("*") if path.is_file())


def compare_outputs(reference: Path, candidate: Path) -> dict[str, Any]:
    issues: list[str] = []
    comparisons: dict[str, Any] = {}
    required = CSV_PATHS + JSON_PATHS + TEXT_PATHS + FIGURES + REQUIRED_ONLY
    for label, root in (("reference", reference), ("candidate", candidate)):
        missing = [relative for relative in required if not (root / relative).is_file()]
        if missing:
            issues.append(f"{label} missing required files: {missing}")
        if not (root / "artifacts/final_model").is_dir():
            issues.append(f"{label} missing artifacts/final_model")
    if issues:
        return {"status": "FAIL", "issues": issues, "comparisons": comparisons}

    for relative in CSV_PATHS:
        ref = pd.read_csv(reference / relative, float_precision="round_trip")
        cand = pd.read_csv(candidate / relative, float_precision="round_trip")
        file_issues = compare_frame(ref, cand)
        issues.extend(f"{relative}: {issue}" for issue in file_issues)
        comparisons[relative] = {"reference_rows": len(ref), "candidate_rows": len(cand)}

    for relative in JSON_PATHS:
        ref = sanitized(read_json(reference / relative))
        cand = sanitized(read_json(candidate / relative))
        if ref != cand:
            issues.append(f"{relative}: stable JSON differs")
        comparisons[relative] = {"excluded_volatile_keys": sorted(VOLATILE_KEYS)}

    for relative in TEXT_PATHS:
        ref = normalized_text(reference / relative)
        cand = normalized_text(candidate / relative)
        if ref != cand:
            issues.append(f"{relative}: normalized text differs")
        comparisons[relative] = {
            "reference_characters": len(ref),
            "candidate_characters": len(cand),
        }

    ref_models = model_files(reference)
    cand_models = model_files(candidate)
    if ref_models != cand_models:
        issues.append(f"final model file list differs: {ref_models} != {cand_models}")
    for relative in sorted(set(ref_models) & set(cand_models)):
        left = reference / relative
        right = candidate / relative
        if left.suffix == ".json":
            if sanitized(read_json(left)) != sanitized(read_json(right)):
                issues.append(f"{relative}: model JSON differs")
        elif left.read_bytes() != right.read_bytes():
            issues.append(f"{relative}: model bytes differ")
    comparisons["artifacts/final_model"] = {"files": [str(path) for path in ref_models]}

    ref_run = read_json(reference / "artifacts/day5_run.json")
    cand_run = read_json(candidate / "artifacts/day5_run.json")
    comparisons["run_status"] = {
        "reference_technical_status": ref_run.get("technical_status"),
        "candidate_technical_status": cand_run.get("technical_status"),
        "reference_source": ref_run.get("source"),
        "candidate_source": cand_run.get("source"),
        "reference_chosen": ref_run.get("chosen"),
        "candidate_chosen": cand_run.get("chosen"),
        "reference_decision": ref_run.get("decision"),
        "candidate_decision": cand_run.get("decision"),
    }

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "comparisons": comparisons,
        "required_files": required,
        "excluded_from_byte_equality": FIGURES + REQUIRED_ONLY,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-root", type=Path, default=Path.cwd())
    parser.add_argument("--reference-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="day5-parity-") as temp:
        temp_root = Path(temp)
        reference, reference_seconds = execute(args.reference_root.resolve(), temp_root / "reference")
        candidate, candidate_seconds = execute(args.candidate_root.resolve(), temp_root / "candidate")
        report = compare_outputs(reference, candidate)
        report.update(
            reference="main / released v1.0.0 learner notebook",
            candidate="develop/bilingual-v1.1.0",
            reference_seconds=reference_seconds,
            candidate_seconds=candidate_seconds,
            scope=(
                "Compares stable Day 5 roles, nested OOF, candidate metrics, ensemble gate, "
                "policy, calibration, portable model, challenge submission and report outputs. "
                "Runtime timing fields, PNG bytes, bundle ZIP bytes and manifest hashes that "
                "depend on volatile files are intentionally excluded."
            ),
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
