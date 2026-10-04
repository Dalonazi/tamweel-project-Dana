# Phase 5 — Day 3 Bilingual Implementation Report | تقرير المرحلة الخامسة — تنفيذ اليوم الثالث ثنائي اللغة

**Target release:** `v1.1.0`  
**Development branch:** `develop/bilingual-v1.1.0`  
**Published learner release:** `v1.0.0` and `main` remain unchanged  
**Validated implementation head:** `642809ac887f809e77f9f0ba256ea54fb1478323`

## Release decision | قرار الإصدار

Day 3 is technically accepted inside the controlled Draft branch. It is not published to learners. The pull request remains Draft until Notebooks 04–05 and 99, remaining learner documents, final release hashes and manual hosted-Colab acceptance are complete.

تم قبول اليوم الثالث تقنيًا داخل فرع التطوير المحكوم. لم يُنشر للمتدربين، ويظل Pull Request بصيغة Draft حتى اكتمال دفاتر 04 و05 و99 وبقية وثائق المتدرب وبصمات الإصدار النهائية والقبول اليدوي داخل Colab المستضاف.

## 1. Production notebook converted | تحويل الدفتر الفعلي

`notebooks/03_cost_sensitive_decision.ipynb` now contains **11 paired learner-facing sections**:

1. Day purpose, boundaries and 60-minute journey | هدف اليوم وحدوده ورحلة 60 دقيقة
2. Controlled free-CPU setup | تجهيز CPU مجاني محكوم
3. Educational loss and capacity policy | سياسة الخسارة والسعة التعليمية
4. Unweighted, weighted and oversampled training | التدريب غير الموزون والموزون وإعادة العينات
5. Ranking and the limits of accuracy | الترتيب وحدود Accuracy
6. Exact threshold sweep and tie handling | مسح العتبات الدقيق ومعالجة التعادل
7. Per-period capacity and policy sensitivity | سعة كل فترة وحساسية السياسة
8. Descriptive regional audit | التدقيق الوصفي للمناطق
9. Learner-owned decision argument | حجة القرار التي يكتبها المتدرب
10. Decision-card and evidence export | تصدير بطاقة القرار والأدلة
11. Completion gate and Day 4 bridge | بوابة الإكمال والربط باليوم الرابع

Every section uses English LTR on the left and Arabic RTL on the right. The notebook retains one shared executable path; no code is duplicated by language.

## 2. Scientific and decision boundaries | الحدود العلمية وحدود القرار

The bilingual content preserves the released exercise while making the following boundaries explicit:

- All data are synthetic.
- A flag means simulated review, not automatic approval or refusal.
- The loss policy `10 × FN + 1 × FP` uses educational decision units; it is not SAR, a fee, expected credit loss or a grade deduction.
- The capacity ceiling is 12% in each validation period, rounded down.
- Threshold selection uses development OOF labels and is not final independent-test performance.
- Weighted and oversampled scores are not treated as calibrated probabilities.
- Regional FPR results are descriptive; they are not a significance test, causal conclusion or legal fairness certification.
- Challenge data remain closed throughout training, selection and threshold choice.

## 3. Day 3 guide rebuilt | إعادة بناء دليل اليوم الثالث

`DAY3_GUIDE.md` was rebuilt as a complete side-by-side bilingual guide covering:

- the 60-minute workflow;
- fresh-session and free-CPU instructions;
- the educational loss matrix and capacity policy;
- fair comparison of three imbalance strategies;
- OOF coverage and warm-up rows;
- ROC-AUC, Average Precision, recall, precision and accuracy limitations;
- exact threshold sweep, ties and constrained selection;
- sensitivity scenarios for FN costs 8, 10 and 12;
- descriptive regional FPR audit;
- learner-owned reasoning requirements;
- the complete Day 3 evidence inventory;
- readiness states, recovery rules and the completion gate.

## 4. Executable-code protection | حماية الكود التنفيذي

The released executable-cell contract is stored in:

```text
content/day3_notebook_code_contract.json
```

It records stable IDs and SHA-256 hashes for all **9 executable cells** from the released `v1.0.0` notebook.

Result:

```text
Expected executable cells: 9
Actual executable cells:   9
Missing cells:              0
Unexpected cells:           0
Changed cells:              0
Status:                     PASS
```

The bilingual conversion changes learner-facing Markdown and notebook metadata only.

## 5. Deterministic generation | التوليد الحتمي

Added:

```text
scripts/build_bilingual_day3.py
.github/workflows/build_bilingual_day3.yml
```

The build workflow captures the released contract, replaces only the 11 expected Markdown cells, verifies executable-cell identity before and after conversion, writes the production notebook and commits generated outputs only when they differ.

Generated bilingual notebook commit:

```text
ecfd52b66e412957607a0f3004ef5a67f5d038b6
```

## 6. Released-reference parity | التطابق مع المرجع المنشور

Added:

```text
scripts/check_day3_reference_parity.py
.github/workflows/day3_reference_parity.yml
```

**Workflow:** `Day 3 Reference Parity`  
**Run:** `37102403872`  
**Result:** `PASS`

The workflow executed the released `main` notebook and the bilingual candidate in separate fresh workspaces. Stable outputs matched after excluding only documented volatile timing fields and image bytes.

| Artifact | Reference rows | Candidate rows | Result |
|---|---:|---:|---|
| `day3_model_report.csv` | 9 | 9 | Match |
| `day3_model_comparison.csv` | 3 | 3 | Match |
| `day3_oof_predictions.csv` | 15,117 | 15,117 | Match |
| `day3_oof_coverage.csv` | 10,000 | 10,000 | Match |
| `threshold_sweep.csv` | 5,042 | 5,042 | Match |
| `day3_review_flags.csv` | 5,039 | 5,039 | Match |
| `day3_period_capacity.csv` | 3 | 3 | Match |
| `day3_region_audit.csv` | 4 | 4 | Match |
| `day3_cost_sensitivity.csv` | 3 | 3 | Match |

Stable JSON content also matched for:

```text
threshold_metrics.json
day3_provenance.json
day3_reflection.json
day3_run.json
```

The generated `reports/DECISION_CARD.md` matched exactly at 2,116 normalized characters. Both runs produced `TECHNICAL_READY`, and all 18 expected artifact files plus the decision card existed.

## 7. Automated quality evidence | أدلة الجودة الآلية

Validation against implementation head `642809ac887f809e77f9f0ba256ea54fb1478323`:

| Quality gate | Run | Result |
|---|---:|---|
| Bilingual Content Check | `37102403892` | PASS |
| Environment Check | `37102403891` | PASS |
| Day 1 Reference Parity regression guard | `37102403886` | PASS |
| Day 2 Reference Parity regression guard | `37102403915` | PASS |
| Day 3 Reference Parity | `37102403872` | PASS |
| Notebook Smoke Test | `37102403910` | PASS |

The smoke test verified the exact executable-cell contracts for Notebooks 00, 01, 02 and 03, executed Notebooks 00–05 in fresh kernels and uploaded the evidence artifact.

## 8. Migration status | حالة التحويل

The bilingual manifest now marks these production learner files complete:

```text
README.md
GLOSSARY.md
DAY1_GUIDE.md
DAY2_GUIDE.md
DAY3_GUIDE.md
notebooks/00_readiness_check.ipynb
notebooks/01_baseline_boosting.ipynb
notebooks/02_validation_tuning.ipynb
notebooks/03_cost_sensitive_decision.ipynb
```

Notebooks 04, 05 and 99 remain `planned`, preventing the partial migration from being presented as a completed bilingual release.

## 9. Remaining release-level acceptance | القبول المتبقي على مستوى الإصدار

- Manual execution from a fresh hosted Google Colab account.
- Visual and responsive review in the actual Colab interface.
- Conversion and verification of Notebooks 04, 05 and 99.
- Conversion of Days 4–5 guides, requirements, reports, rubric and submission documents.
- Final release-hash rebuild after learner-facing files are frozen.
- Private evaluator and private submission registry.
- Merge to `main` and publication of `v1.1.0`.

## Phase 6 entry | دخول المرحلة السادسة

Day 4 may be converted next using the same controlled pattern, with special attention to SHAP interpretation, calibration, uncertainty, causal-language restrictions and the non-submittable recovery path.

يمكن بدء اليوم الرابع بالنمط المحكوم نفسه، مع عناية خاصة بتفسير SHAP والمعايرة وعدم اليقين ومنع اللغة السببية ومسار التعافي غير الصالح للتسليم.
