# Dependency and Release Map | خريطة الاعتمادات والإصدار

Target release: `v1.1.0`  
Protected published baseline: `v1.0.0` at commit `81a6a2603ccdeb395b94b7d09c966fb98d863e7b`

## Why this map exists | سبب إنشاء الخريطة

The notebooks download verified course files by commit revision and SHA-256. Editing a script, manifest, data file, or package constraint without regenerating dependent hashes can break Colab setup even when the edited file itself is correct.

تقوم الدفاتر بتنزيل ملفات الدورة والتحقق منها باستخدام Commit Revision وبصمات SHA-256. قد يؤدي تعديل سكربت أو Manifest أو ملف بيانات أو قيد إصدار دون إعادة توليد البصمات التابعة إلى تعطيل إعداد Colab رغم صحة الملف المعدل.

## Public dependency layers | طبقات الاعتماد العامة

```text
GitHub release commit
├── requirements-colab.txt
├── constraints.txt
├── data/data_manifest.json
├── data/data_contract.json
├── scripts/setup_colab.py
├── scripts/data_checks.py
├── scripts/day1_lab.py
├── scripts/day2_validation.py
├── scripts/day3_decision.py
├── scripts/day4_trust.py
├── scripts/day5_final.py
├── scripts/day5_delivery.py
├── scripts/submission_contract.py
├── notebooks/00–05
└── notebooks/99_final_submission_check.ipynb
```

## Notebook dependency contract | عقد اعتماد الدفاتر

| Notebook | Primary script dependencies | Major evidence |
|---|---|---|
| `00_readiness_check.ipynb` | setup, readiness checks, data checks | environment readiness |
| `01_baseline_boosting.ipynb` | setup, data checks, day1 lab | model comparison |
| `02_validation_tuning.ipynb` | setup, data checks, day2 validation | leakage and validation reports |
| `03_cost_sensitive_decision.ipynb` | setup, data checks, day3 decision | OOF threshold and Decision Card |
| `04_explain_calibrate.ipynb` | setup, data checks, day4 trust | SHAP, calibration, stability |
| `05_final_model.ipynb` | setup, days 1–5 scripts, delivery helpers | final model, policy, Model Card |
| `99_final_submission_check.ipynb` | final check, run notebooks, submission contract | readiness report and final manifest |

## Hash-sensitive changes | تغييرات حساسة للبصمات

The following changes require a release-hash rebuild:

- Any file downloaded by a notebook using an expected SHA-256.
- `data/data_manifest.json` or a data file named inside it.
- `scripts/setup_colab.py`.
- Any day-specific script fetched by a notebook.
- Package version files used by the setup path.
- Notebook source when its own hash is stored in a manifest or submission contract.

## Safe editorial changes | تغييرات تحريرية منخفضة المخاطر

These changes normally do not alter scientific output, but they still require notebook JSON validation:

- Learner-facing Markdown translation.
- Spacing and typography.
- Explanatory tables.
- Link labels.
- Accessibility metadata.
- Bilingual checkpoint wording, provided required identifiers remain unchanged.

## Required release sequence | تسلسل الإصدار الإلزامي

1. Freeze feature work.
2. Run unit tests.
3. Execute notebooks `00–05` in fresh kernels.
4. Execute notebook `99` against a completed fixture project.
5. Regenerate data and source hashes.
6. Update notebook revision constants.
7. Re-run all notebooks after hash changes.
8. Run final project validation.
9. Confirm no private evaluator assets exist in the public tree.
10. Tag the exact approved commit.
11. Publish release notes and update the portal version.

## Rollback | الرجوع

The published `v1.0.0` tag remains the rollback point. The bilingual branch must not rewrite or move that tag. A failed migration is corrected on the development branch or abandoned without changing the learner release.

## Planned automation | الأتمتة المخطط لها

`v1.1.0` will add a release builder that calculates source hashes, updates controlled notebook constants, validates the data manifest, and produces a machine-readable release report. Manual hash editing will not be accepted as the final release process.
