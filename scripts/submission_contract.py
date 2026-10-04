"""File contract for a final project; hashes establish bytes, never a grade."""
from hashlib import sha256
from pathlib import Path, PurePosixPath
import json
import re
import zipfile

NOTEBOOKS = ['00_readiness_check', '01_baseline_boosting', '02_validation_tuning',
             '03_cost_sensitive_decision', '04_explain_calibrate', '05_final_model']
MANIFEST = 'submission/final_project_manifest.json'
BUNDLE = 'submission/final_project_bundle.zip'
EXCLUDED = {MANIFEST, BUNDLE, 'submission/project_bundle.zip',
            'submission/self_check_report.json', 'submission/self_check_report.md'}
SKIP_DIRS = {'.git', '__pycache__', '.ipynb_checkpoints', '.venv', '.cache', 'rebuild_check', '.check-output'}
EXTENSIONS = {'.py', '.md', '.ipynb', '.json', '.csv', '.png', '.npz', '.txt', '.ubj', '.pdf', '.yml', '.yaml', '.cff', '.html', '.css', '.js'}
FORBIDDEN = re.compile(r'(?i)(challenge_labels|challenge_seeds|hidden_data|instructor|master_prompt|blueprint|\.env$|id_rsa|credentials)')
PLACEHOLDER = re.compile(r'(?i)\[اكتب|أضف دليلك وتفسيرك هنا|Add your evidence and explanation here|\bTODO\b|\bYOUR_[A-Z_]+\b')
REQUIRED = ['README.md', 'PROJECT_README.md', 'requirements-colab.txt', 'constraints.txt',
            'data/data_contract.json', 'data/data_manifest.json', 'data/tamweel_train.csv', 'data/tamweel_challenge.csv',
            'tamweel/__init__.py', 'tamweel/inference.py', 'scripts/inference.py', 'scripts/rebuild_final.py',
            'submission/submission.csv', 'artifacts/final_model/model.json', 'artifacts/final_model/model_manifest.json',
            'artifacts/day5_run.json', 'artifacts/environment.json', 'artifacts/day5_reflection.json',
            'artifacts/day5_oof_predictions.csv', 'artifacts/day5_fold_scores.csv', 'artifacts/ensemble_comparison.csv',
            'artifacts/final_metrics.json', 'artifacts/final_policy.json', 'artifacts/day5_oof_provenance.json',
            'artifacts/day5_final_provenance.json', 'artifacts/day5_ensemble_gate.json',
            'artifacts/day5_diversity.png', 'artifacts/day5_ensemble_comparison.png', 'artifacts/day5_policy_regions.png',
            'artifacts/day5_calibration_fit.png', 'artifacts/day5_challenge_capacity.png',
            'reports/MODEL_CARD.md', 'reports/ENSEMBLE_DECISION.md', 'presentation/final_presentation.pdf']
REQUIRED += [f'notebooks/{name}.ipynb' for name in NOTEBOOKS[1:]]
DAILY_REQUIRED = {
    1: ['day1_model_comparison.csv', 'day1_comparison_predictions.csv', 'day1_split_membership.csv', 'day1_learning_curves.png', 'day1_roc_pr.png'],
    2: ['validation_summary.csv', 'leakage_audit.csv', 'fold_audit.csv', 'optuna_results.csv', 'best_params.json', 'day2_validation_comparison.png'],
    3: ['threshold_metrics.json', 'threshold_sweep.csv', 'day3_oof_predictions.csv', 'day3_region_audit.csv', 'cost_curve.png', 'DECISION_CARD.md'],
    4: ['calibration_metrics.json', 'permutation_importance.csv', 'day4_shap_metadata.json', 'day4_stability_summary.json', 'shap_beeswarm.png', 'shap_waterfall.png', 'reliability_curve.png', 'INTERPRETABILITY_REPORT.md'],
}


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def json_read(path):
    def reject(value):
        raise ValueError('JSON must not contain NaN or infinity.')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON keys are not allowed.')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), parse_constant=reject, object_pairs_hook=unique)


def safe_name(name):
    if not isinstance(name, str):
        raise ValueError('Expected a relative file name.')
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '\\' in name or ':' in name or '..' in p.parts or str(p) != name or p == PurePosixPath('.'):
        raise ValueError('Unsafe archive/manifest path.')
    return p


def inventory(root):
    root = Path(root).resolve()
    result = {}
    total = 0
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            raise ValueError(f'Symbolic links are not allowed: {rel}')
        if not path.is_file() or rel in EXCLUDED:
            continue
        if FORBIDDEN.search(rel):
            raise ValueError(f'Private or credential file must not be submitted: {rel}')
        if path.suffix == '.zip' and re.fullmatch(r'day[1-4]_artifacts\.zip', path.name):
            continue
        if path.suffix not in EXTENSIONS and path.name not in {'.gitignore', '.nojekyll'}:
            raise ValueError(f'Unsupported file: {rel}')
        total += path.stat().st_size
        if path.stat().st_size > 32*1024*1024 or total > 100*1024*1024 or len(result) >= 500:
            raise ValueError('Project exceeds the 500-file/100 MiB teaching limit.')
        result[rel] = {'bytes': path.stat().st_size, 'sha256': digest(path)}
    return result


def inventory_digest(files):
    return sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def build_manifest(root, bundle=False):
    root = Path(root).resolve()
    files = inventory(root)
    run = json_read(root/'artifacts/day5_run.json')
    environment = json_read(root/'artifacts/environment.json')
    result = {'format_version': 1, 'scope': 'Final learner project files', 'files': files,
              'content_sha256': inventory_digest(files), 'seed': run['config']['seed'],
              'environment': environment, 'course_support_revision': run['lab_revision'],
              'receipt_note': 'Record the final repository SHA/tag outside this manifest after committing; no self-reference.',
              'meaning': 'File integrity only. Not a grade, authorship proof or submission receipt.'}
    target = root/MANIFEST
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    if bundle:
        with zipfile.ZipFile(root/BUNDLE, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name in [*files, MANIFEST]:
                archive.write(root/name, name)
    return result


def check_manifest(root):
    root = Path(root)
    manifest = json_read(root/MANIFEST)
    files = inventory(root)
    if manifest.get('format_version') != 1 or manifest.get('files') != files or manifest.get('content_sha256') != inventory_digest(files):
        raise ValueError('Final manifest is incomplete or stale; rebuild it after your last edit.')
    run = json_read(root/'artifacts/day5_run.json')
    if manifest.get('seed') != run['config']['seed'] or manifest.get('environment') != json_read(root/'artifacts/environment.json'):
        raise ValueError('Manifest seed/environment does not match the run.')
    return manifest


def extract_project(archive, destination):
    destination = Path(destination).resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Extract into a new, empty directory.')
    with zipfile.ZipFile(archive) as z:
        entries = z.infolist()
        if len(entries) > 700 or sum(e.file_size for e in entries) > 100*1024*1024:
            raise ValueError('Archive exceeds the project limit.')
        seen = set()
        for entry in entries:
            name = entry.filename.rstrip('/')
            path = safe_name(name)
            if name.casefold() in seen or ((entry.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError('Duplicate paths or symbolic links in archive.')
            seen.add(name.casefold())
            if any(p in SKIP_DIRS for p in path.parts) or FORBIDDEN.search(name):
                raise ValueError('Archive contains a private or excluded path.')
            if entry.file_size > 32*1024*1024:
                raise ValueError('An archive entry exceeds the file limit.')
        destination.mkdir(parents=True, exist_ok=True)
        for entry in entries:
            if not entry.is_dir():
                target = destination.joinpath(*PurePosixPath(entry.filename).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(entry))
    # GitHub source ZIPs have one enclosing directory; learner bundles do not.
    children = list(destination.iterdir())
    return children[0] if len(children) == 1 and children[0].is_dir() else destination
