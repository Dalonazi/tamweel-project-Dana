"""Execute Day 2 from the candidate and released reference, then compare stable outputs."""
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


NOTEBOOK = Path("notebooks/02_validation_tuning.ipynb")
FRAME_SPECS: dict[str, dict[str, Any]] = {
    "validation_report.csv": {
        "keys": ["scheme", "fold"],
        "exclude": ["train_seconds"],
    },
    "validation_summary.csv": {
        "keys": ["scheme"],
        "exclude": [],
    },
    "optuna_results.csv": {
        "keys": ["trial"],
        "exclude": ["seconds"],
    },
    "leakage_audit.csv": {
        "keys": ["feature"],
        "exclude": [],
    },
    "fold_audit.csv": {
        "keys": ["fold"],
        "exclude": [],
    },
    "day2_oof_predictions.csv": {
        "keys": ["scheme", "application_id"],
        "exclude": [],
    },
    "day2_oof_coverage.csv": {
        "keys": ["application_id"],
        "exclude": [],
    },
}
JSON_DROP_KEYS: dict[str, set[str]] = {
    "best_params.json": {"elapsed_seconds"},
    "day2_provenance.json": {"train_seconds"},
    "day2_reflection.json": set(),
    "day2_run.json": set(),
}
REQUIRED_ARTIFACTS = {
    "environment.json",
    "validation_report.csv",
    "validation_summary.csv",
    "optuna_results.csv",
    "leakage_audit.csv",
    "fold_audit.csv",
    "day2_oof_predictions.csv",
    "day2_oof_coverage.csv",
    "best_params.json",
    "day2_provenance.json",
    "day2_reflection.json",
    "day2_run.json",
    "day2_fold_sizes.png",
    "day2_search.png",
    "day2_validation_comparison.png",
    "day2_artifacts.zip",
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
            timeout=240,
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
    keys: list[str],
    exclude: list[str],
    numeric_tolerance: float = 1e-10,
) -> list[str]:
    issues: list[str] = []
    missing_keys = [key for key in keys if key not in reference or key not in candidate]
    if missing_keys:
        return [f"Missing comparison keys {missing_keys}"]

    reference = reference.drop(columns=exclude, errors="ignore")
    candidate = candidate.drop(columns=exclude, errors="ignore")
    reference = reference.sort_values(keys, kind="stable").reset_index(drop=True)
    candidate = candidate.sort_values(keys, kind="stable").reset_index(drop=True)

    if list(reference.columns) != list(candidate.columns):
        issues.append(
            "Column mismatch: "
            f"reference={list(reference.columns)}, candidate={list(candidate.columns)}"
        )
        return issues
    if len(reference) != len(candidate):
        issues.append(f"Row-count mismatch: {len(reference)} != {len(candidate)}")
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
                issues.append(f"Numeric mismatch in {column}")
        elif not left.fillna("<NA>").astype(str).equals(
            right.fillna("<NA>").astype(str)
        ):
            issues.append(f"Value mismatch in {column}")
    return issues


def sanitized(value: Any, drop_keys: set[str]) -> Any:
    if isinstance(value, dict):
        return {
            key: sanitized(item, drop_keys)
            for key, item in sorted(value.items())
            if key not in drop_keys
        }
    if isinstance(value, list):
        return [sanitized(item, drop_keys) for item in value]
    if isinstance(value, float) and np.isnan(value):
        return "<NaN>"
    return value


def compare_artifacts(reference: Path, candidate: Path) -> dict[str, Any]:
    issues: list[str] = []
    comparisons: dict[str, Any] = {}

    for label, folder in (("reference", reference), ("candidate", candidate)):
        missing = sorted(name for name in REQUIRED_ARTIFACTS if not (folder / name).is_file())
        if missing:
            issues.append(f"{label} missing required artifacts: {missing}")

    if issues:
        return {
            "status": "FAIL",
            "issues": issues,
            "comparisons": comparisons,
        }

    for filename, spec in FRAME_SPECS.items():
        reference_frame = pd.read_csv(reference / filename)
        candidate_frame = pd.read_csv(candidate / filename)
        frame_issues = compare_frame(
            reference_frame,
            candidate_frame,
            keys=spec["keys"],
            exclude=spec["exclude"],
        )
        issues.extend(f"{filename}: {issue}" for issue in frame_issues)
        comparisons[filename] = {
            "reference_rows": len(reference_frame),
            "candidate_rows": len(candidate_frame),
            "excluded_volatile_columns": spec["exclude"],
        }

    for filename, drop_keys in JSON_DROP_KEYS.items():
        reference_json = sanitized(read_json(reference / filename), drop_keys)
        candidate_json = sanitized(read_json(candidate / filename), drop_keys)
        if reference_json != candidate_json:
            issues.append(
                f"{filename}: stable JSON content differs after excluding {sorted(drop_keys)}"
            )
        comparisons[filename] = {
            "excluded_volatile_keys": sorted(drop_keys),
        }

    reference_run = read_json(reference / "day2_run.json")
    candidate_run = read_json(candidate / "day2_run.json")
    comparisons["run_status"] = {
        "reference_technical_status": reference_run.get("technical_status"),
        "candidate_technical_status": candidate_run.get("technical_status"),
        "reference_oof_coverage": reference_run.get("oof_whole_data_coverage"),
        "candidate_oof_coverage": candidate_run.get("oof_whole_data_coverage"),
    }

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "comparisons": comparisons,
        "required_artifacts": sorted(REQUIRED_ARTIFACTS),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-root", type=Path, default=Path.cwd())
    parser.add_argument("--reference-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    candidate_root = args.candidate_root.resolve()
    reference_root = args.reference_root.resolve()
    with tempfile.TemporaryDirectory(prefix="day2-parity-") as temp:
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
                    "Compares stable Day 2 scientific tables, live search results, "
                    "OOF probabilities, coverage, provenance and run metadata. "
                    "Training/search timing fields and image bytes are intentionally excluded."
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
