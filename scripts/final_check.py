"""Run the learner's final checks on one fixed project directory."""
import argparse
from pathlib import Path
import json
from submission_contract import build_manifest
from run_notebooks import run
from validate_submission import validate, write_report


def check_project(root, output, prepare=False):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.is_relative_to(root) and '.check-output' not in output.relative_to(root).parts:
        raise ValueError('Store check results outside the project, or in .check-output/.')
    output.mkdir(parents=True, exist_ok=True)
    preparation_error = None
    if prepare:
        try:
            build_manifest(root)
        except (OSError, ValueError, KeyError, TypeError) as error:
            preparation_error = str(error)
    smoke = run(root, output/'notebooks', strict=True)
    result = validate(root, output/'notebooks/notebook_run.json')
    if preparation_error:
        result['manifest_preparation_error'] = preparation_error
    write_report(result, output)
    if result['ready_for_submission'] and prepare:
        build_manifest(root, bundle=True)
    print(result['status'])
    for row in result['checks']:
        if row['status'] == 'FAIL':
            print(f"{row['file']} | {row['how_to_fix']} | {row['detail']}")
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, default=Path('.check-output'))
    parser.add_argument('--prepare', action='store_true', help='Rebuild the manifest; export a ZIP only if all checks pass.')
    args = parser.parse_args()
    result = check_project(args.root, args.output, args.prepare)
    raise SystemExit(0 if result['ready_for_submission'] else 1)
