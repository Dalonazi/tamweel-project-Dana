"""Execute each lab in a fresh kernel/workspace; original learner files are read only."""
import argparse
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import time
import nbformat
from nbclient import NotebookClient
from submission_contract import NOTEBOOKS, inventory, inventory_digest, json_read, digest


def worker(source, output, strict):
    source, output = Path(source), Path(output)
    with tempfile.TemporaryDirectory(prefix='tamweel-lab-') as folder:
        work = Path(folder)
        notebook = nbformat.read(source, as_version=4)
        adapted = 0
        # Colab notebooks default to /content/tamweel. This execution-only adapter
        # selects a unique directory; no scientific logic or answer is changed.
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                lines = cell.source.splitlines()
                for i, line in enumerate(lines):
                    if line.startswith('ROOT = ') and 'TAMWEEL_PROJECT_DIR' in line:
                        lines[i] = 'ROOT = Path(os.environ["TAMWEEL_PROJECT_DIR"]).resolve()'
                        adapted += 1
                cell.source = '\n'.join(lines)
        if adapted != 1:
            raise ValueError('Expected exactly one documented workspace setting in the notebook.')
        os.environ.update(ASSESSMENT_MODE='1', TAMWEEL_PROJECT_DIR=str(work), OMP_NUM_THREADS='2',
                          OPENBLAS_NUM_THREADS='2', PYTHONDONTWRITEBYTECODE='1')
        started = time.perf_counter()
        NotebookClient(notebook, timeout=180, kernel_name='python3', resources={'metadata': {'path': str(work)}}).execute()
        complete = True
        if source.name[:2] != '00':
            day = int(source.name[:2])
            run = json_read(work/f'artifacts/day{day}_run.json')
            reflection = json_read(work/f'artifacts/day{day}_reflection.json')
            if run['technical_status'] != 'TECHNICAL_READY':
                raise ValueError('Live computation required; no recovery in assessment mode.')
            complete = reflection['checkpoint']['status'] == 'READY_FOR_REVIEW'
        result = {'status': 'PASS' if complete or not strict else 'FAIL', 'learner_complete': complete,
                  'seconds': round(time.perf_counter()-started, 2), 'source_sha256': digest(source),
                  'workspace_adapter': 'Only ROOT redirected to a fresh temporary workspace.',
                  'code_cells': sum(c.cell_type=='code' for c in notebook.cells)}
        output.write_text(json.dumps(result, indent=2), encoding='utf-8')


def run(root, output, strict=False):
    root, output = Path(root).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    before = inventory_digest(inventory(root))
    results = []
    for name in NOTEBOOKS:
        path = f'notebooks/{name}.ipynb'
        result_path = output/f'{name}.json'
        command = [sys.executable, str(Path(__file__).resolve()), '--worker', str(root/path), '--output', str(result_path)]
        if strict:
            command.append('--strict')
        started = time.perf_counter()
        try:
            completed = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace',
                                       timeout=360, env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
        except subprocess.TimeoutExpired:
            result = {'status': 'FAIL', 'learner_complete': False, 'detail': 'Notebook exceeded six-minute limit.'}
        else:
            (output/f'{name}.log').write_text(completed.stdout+'\n'+completed.stderr, encoding='utf-8')
            result = json_read(result_path) if completed.returncode == 0 and result_path.exists() else {'status': 'FAIL', 'learner_complete': False, 'detail': 'See notebook log.'}
        results.append({'notebook': path, **result})
        print(f"{path}: {result['status']} ({time.perf_counter()-started:.1f}s)", flush=True)
    unchanged = before == inventory_digest(inventory(root))
    report = {'status': 'PASS' if unchanged and all(r['status']=='PASS' for r in results) else 'FAIL',
              'assessment_mode': True, 'strict_learner_mode': strict, 'content_sha256': before,
              'source_files_unchanged': unchanged, 'notebooks': results,
              'scope': 'Fresh kernels and workspaces, one notebook at a time; not a grade or authenticity proof.'}
    (output/'notebook_run.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path.cwd())
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--strict', action='store_true')
    p.add_argument('--worker', type=Path)
    args = p.parse_args()
    if args.worker:
        worker(args.worker, args.output, args.strict)
    else:
        raise SystemExit(0 if run(args.root, args.output, args.strict)['status']=='PASS' else 1)
