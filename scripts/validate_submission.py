"""Explain final-project omissions without assigning a grade."""
import argparse
from pathlib import Path
import json
import re
import numpy as np
import pandas as pd
from submission_contract import (REQUIRED, DAILY_REQUIRED, NOTEBOOKS, PLACEHOLDER, MANIFEST,
                                 json_read, inventory, inventory_digest, check_manifest, digest)
from day5_delivery import validate_submission, replay_submission
from day3_decision import CostPolicy
from data_checks import validate_frame

EXPECTED_CONTRACT_SHA = '3b2d60c52452cb1cc43ea105992211746e5da44cdb2e5ed73b04bbce52dd5d21'
READY = 'READY FOR FINAL SUBMISSION | جاهز للتسليم النهائي'


def validate(root, smoke_report=None, template=False):
    root = Path(root).resolve()
    rows = []

    def check(name, location, fix, operation):
        try:
            operation()
        except (OSError, ValueError, KeyError, TypeError, AssertionError, json.JSONDecodeError) as error:
            rows.append({'check': name, 'status': 'FAIL', 'file': location,
                         'how_to_fix': fix, 'detail': str(error)[:350]})
        else:
            rows.append({'check': name, 'status': 'PASS', 'file': location, 'how_to_fix': '', 'detail': ''})

    def require(condition, message):
        if not condition:
            raise ValueError(message)

    check('safe_files', '.', 'أزل الملفات الخاصة والروابط الرمزية والملفات غير المدعومة.', lambda: inventory(root))

    def data():
        require(digest(root/'data/data_contract.json') == EXPECTED_CONTRACT_SHA, 'Use the released data contract unchanged.')
        contract = json_read(root/'data/data_contract.json')
        for kind in ['train', 'challenge']:
            validate_frame(pd.read_csv(root/f'data/tamweel_{kind}.csv'), contract, kind)
        manifest = json_read(root/'data/data_manifest.json')
        for name in ['data/tamweel_train.csv', 'data/tamweel_challenge.csv']:
            require(digest(root/name) == manifest['files'][name]['sha256'], f'Data checksum mismatch: {name}')
    check('data_contract', 'data/', 'استعد البيانات العامة وعقدها من قالب الدورة.', data)

    if template:
        for name in NOTEBOOKS:
            def notebook_structure(name=name):
                item = json_read(root/f'notebooks/{name}.ipynb')
                require(item.get('nbformat') == 4 and any(c['cell_type'] == 'code' for c in item['cells']), 'Invalid notebook.')
            check('notebook_structure', f'notebooks/{name}.ipynb', 'استعد دفتر التطبيق.', notebook_structure)
        return {'status': 'STARTER_TEMPLATE_HEALTHY' if all(r['status']=='PASS' for r in rows) else 'CHECKS_FAILED',
                'ready_for_submission': False, 'automatic_grade': None, 'checks': rows,
                'meaning': 'فحص القالب فقط؛ لا يدل على اكتمال مشروع متدرب.'}

    for name in REQUIRED:
        check('required_file', name, 'أضف الملف الفعلي إلى المسار المحدد؛ لا يكفي ZIP وحده.',
              lambda name=name: require((root/name).is_file() and (root/name).stat().st_size > 0, 'Missing or empty file.'))

    def unique_daily(day, name):
        paths = list((root/'evidence'/f'day{day}').rglob(name))
        require(len(paths) == 1, f'Expected exactly one {name}; found {len(paths)}.')
        require(paths[0].stat().st_size > 0, 'Empty evidence file.')
        return paths[0]

    def reflection(path, day):
        obj = json_read(path)
        require(obj['checkpoint']['status'] == 'READY_FOR_REVIEW', 'أكمل إجاباتك وأعد خلية الإجابات والتصدير.')
        answers = (obj.get('responses') if day > 1 else
                   {'problem': obj.get('problem_statement'), 'candidate': obj.get('candidate'),
                    **obj.get('notes', {}), **{f'exit_{i}': a for i, a in enumerate(obj.get('exit_answers', []))}})
        expected_count = {1: 7, 2: 5, 3: 6, 4: 6, 5: 9}[day]
        require(isinstance(answers, dict) and len(answers) >= expected_count, 'Reflection fields are missing.')
        require(all(isinstance(v, str) and v.strip() and not PLACEHOLDER.search(v) for v in answers.values()), 'Blank or placeholder answer.')

    def live_run(path):
        obj = json_read(path)
        require(obj['technical_status'] == 'TECHNICAL_READY', 'Run your own FAST computation; recovery is not final evidence.')
        config = obj.get('effective_config', obj.get('config', {}))
        require(isinstance(config.get('seed'), int) and not isinstance(config.get('seed'), bool), 'Record an integer seed in the effective run configuration.')
        require(not any(word in json.dumps(obj) for word in ['EDUCATIONAL_EXAMPLE', 'EXAMPLE_ONLY', 'PRECOMPUTED']), 'Recovery evidence is not accepted.')

    for day in range(1, 5):
        for name in [*DAILY_REQUIRED[day], f'day{day}_reflection.json', f'day{day}_run.json', 'environment.json']:
            check('daily_evidence', f'evidence/day{day}/{name}', 'استورد حزمة يومك المنفذة إلى مجلد evidence المخصص.',
                  lambda day=day, name=name: unique_daily(day, name))
        check('learner_answers', f'evidence/day{day}/', 'أكمل تفسيرك في الدفتر وأعد تصدير حزمة ذلك اليوم.',
              lambda day=day: reflection(unique_daily(day, f'day{day}_reflection.json'), day))
        check('live_execution', f'evidence/day{day}/', 'نفّذ FAST فعليًا؛ المثال المحفوظ لا يستخدم في التسليم.',
              lambda day=day: live_run(unique_daily(day, f'day{day}_run.json')))
    check('learner_answers', 'artifacts/day5_reflection.json', 'أكمل تفسيرات اليوم الخامس التسعة وأعد التصدير.', lambda: reflection(root/'artifacts/day5_reflection.json', 5))
    check('live_execution', 'artifacts/day5_run.json', 'أعد تشغيل اليوم الخامس دون المثال التعليمي.', lambda: live_run(root/'artifacts/day5_run.json'))

    for name in NOTEBOOKS[1:]:
        def executed(name=name):
            nb = json_read(root/f'notebooks/{name}.ipynb')
            cells = [c for c in nb['cells'] if c['cell_type'] == 'code' and ''.join(c['source']).strip()]
            require(bool(cells), 'Notebook contains no code.')
            require(all(isinstance(c.get('execution_count'), int) and c['execution_count'] > 0 for c in cells), 'Save the executed notebook with outputs.')
            require(not any(o['output_type']=='error' for c in cells for o in c.get('outputs', [])), 'An error output remains.')
            require(not any(re.search(r'(?mi)^\s*#\s*TODO\b', ''.join(c['source'])) for c in cells), 'A mandatory TODO comment remains.')
        check('executed_notebook', f'notebooks/{name}.ipynb', 'Run all ثم احفظ نسخة منفذة بالمخرجات.', executed)

    for name in ['PROJECT_README.md', 'reports/MODEL_CARD.md', 'reports/ENSEMBLE_DECISION.md']:
        def report(name=name):
            text = (root/name).read_text(encoding='utf-8')
            require(len(text.strip()) >= 150 and not PLACEHOLDER.search(text), 'Complete your report with your own evidence.')
            if name.endswith('MODEL_CARD.md'):
                require(len(re.findall(r'^## ', text, re.M)) >= 9, 'Model Card requires purpose, data, models, calibration, policy, explanation, limits, reproducibility and ownership sections.')
        check('written_report', name, 'أكمل تفسيرك وأقسام التقرير؛ صحة المحتوى تراجع بشريًا.', report)

    def presentation():
        require((root/'presentation/final_presentation.pdf').read_bytes().startswith(b'%PDF-'), 'Export the presentation as PDF.')
    check('presentation', 'presentation/final_presentation.pdf', 'صدّر عرضك ذي الشرائح الخمس إلى PDF؛ المحتوى يراجع في العرض.', presentation)

    def final_predictions():
        policy = json_read(root/'artifacts/final_policy.json')
        require(policy['cost_policy'] == {'false_negative_cost': 10.0, 'false_positive_cost': 1.0, 'max_flag_fraction': .12}, 'Use the announced educational policy.')
        contract = json_read(root/'data/data_contract.json')
        model = json_read(root/'artifacts/final_model/model.json')
        require(model['contract'] == contract and model['features'] == [f['name'] for f in contract['features']], 'Model predictors differ from the approved features; exclude IDs, dates, target and leaks.')
        submitted = pd.read_csv(root/'submission/submission.csv', float_precision='round_trip')
        challenge = pd.read_csv(root/'data/tamweel_challenge.csv')
        validate_submission(submitted, challenge, policy['calibrated_threshold'], CostPolicy(**policy['cost_policy']))
        replayed = replay_submission(root).set_index('application_id').loc[submitted.application_id]
        require(np.allclose(replayed.probability, submitted.probability, rtol=0, atol=1e-9) and np.array_equal(replayed.decision, submitted.decision), 'Submission differs from the saved model and full-batch policy.')
        metrics = json_read(root/'artifacts/final_metrics.json')
        require(metrics['challenge_metrics'] is None, 'Do not claim challenge performance without hidden labels.')
        require(all(k in metrics for k in ['gate', 'oof_threshold_selection', 'calibration_fit_diagnostics', 'regional_oof']), 'Required metric sections are missing.')
    check('predictions_and_policy', 'submission/submission.csv', 'أعد التصدير من النموذج والسياسة المجمدين؛ لا تعدّل CSV يدويًا.', final_predictions)
    check('final_manifest', MANIFEST, 'أعد بناء manifest بعد آخر تعديل ثم أعد الفحص.', lambda: check_manifest(root))

    def clean_execution():
        require(smoke_report is not None, 'Fresh execution report required; run notebook99 or Final Project Check.')
        proof = json_read(smoke_report)
        require(proof['status'] == 'PASS' and proof['assessment_mode'] is True and proof['strict_learner_mode'] is True, 'Fresh execution did not pass in assessment mode.')
        require(proof['content_sha256'] == inventory_digest(inventory(root)), 'Fresh execution report belongs to different project bytes.')
        require([r['notebook'] for r in proof['notebooks']] == [f'notebooks/{n}.ipynb' for n in NOTEBOOKS], 'Clean run must cover readiness and all five labs.')
        require(all(r['status']=='PASS' and r['learner_complete'] for r in proof['notebooks']), 'Complete the responses in the executed notebook source, not only exported JSON.')
    check('fresh_execution', 'notebooks/', 'شغّل الفحص الكامل من99 أو Actions على الملفات نفسها.', clean_execution)
    passed = all(row['status'] == 'PASS' for row in rows)
    return {'status': READY if passed else 'NEEDS_WORK | يحتاج استكمالًا', 'ready_for_submission': passed,
            'automatic_grade': None, 'checks': rows,
            'meaning': 'Mechanical readiness only. The instructor reviews reasoning, authorship, exact SHA/tag and the presentation.'}


def write_report(result, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output/'self_check_report.json').write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False), encoding='utf-8')
    lines = [f"# {result['status']}", '', result['meaning'], '', '| Check | Status | File | How to fix |', '|---|---|---|---|']
    lines += [f"| {r['check']} | {r['status']} | {r['file']} | {r['how_to_fix']} |" for r in result['checks']]
    (output/'self_check_report.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path.cwd())
    p.add_argument('--smoke-report', type=Path)
    p.add_argument('--output', type=Path, default=Path('.check-output'))
    p.add_argument('--template', action='store_true')
    args = p.parse_args()
    result = validate(args.root, args.smoke_report, args.template)
    write_report(result, args.output)
    print(result['status'])
    for row in result['checks']:
        if row['status'] == 'FAIL':
            print(f"FAIL | {row['file']} | {row['how_to_fix']} | {row['detail']}")
    raise SystemExit(0 if result['ready_for_submission'] or result['status']=='STARTER_TEMPLATE_HEALTHY' else 1)
