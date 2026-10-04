# Phase 4 — Day 2 Bilingual Implementation Report | تقرير المرحلة الرابعة — تنفيذ اليوم الثاني ثنائي اللغة

**Target release:** `v1.1.0`  
**Development branch:** `develop/bilingual-v1.1.0`  
**Published learner release:** `v1.0.0` and `main` remain unchanged  
**Scope:** Notebook 02, Day 2 guide, executable-code protection, honest-validation parity and automated quality gates

## Release decision | قرار الإصدار

Day 2 is technically accepted inside the controlled draft branch. It is not published to learners and the pull request must remain in Draft state until Notebooks 03–05 and 99, the remaining learner documentation, final release hashes and manual hosted-Colab acceptance are complete.

تم قبول اليوم الثاني تقنيًا داخل فرع التطوير المحكوم. لم يُنشر للمتدربين، ويجب أن يبقى Pull Request بصيغة Draft حتى اكتمال دفاتر 03–05 و99 وبقية وثائق المتدرب وبصمات الإصدار النهائية واختبار القبول اليدوي داخل Colab المستضاف.

## 1. Production notebook converted | تحويل الدفتر الفعلي

The production file `notebooks/02_validation_tuning.ipynb` now contains **12 paired learner-facing sections** with:

- English on the left using explicit `dir="ltr"`.
- Arabic on the right using explicit `dir="rtl"`.
- One shared executable path; code is not duplicated by language.
- Equivalent scientific boundaries, warnings, evidence requirements and completion criteria.
- Beginner-accessible explanations without removing time-aware validation, leakage control, nested tree selection or bounded-search concepts.
- Synthetic-data and non-deployment limitations placed beside the workflow rather than hidden in a final note.

أصبح الملف الفعلي `notebooks/02_validation_tuning.ipynb` يحتوي على **12 قسمًا تعليميًا ثنائيًا**؛ الإنجليزية يسارًا والعربية يمينًا، مع مسار تنفيذ مشترك واحد وتكافؤ الحدود العلمية والتحذيرات والأدلة ومعايير الإكمال.

### Paired sections | الأقسام الثنائية

1. Day purpose, deliverables and 60-minute journey | هدف اليوم ومخرجاته ورحلة 60 دقيقة
2. Controlled environment setup | تجهيز بيئة محكومة
3. Information-availability and duplicate audit | تدقيق إتاحة المعلومات والتكرار
4. Time, customer and label-maturity roles | أدوار الزمن والعملاء ونضج الهدف
5. Reserved historical search cohort | مجموعة البحث التاريخية المحجوزة
6. Bounded Optuna search | بحث Optuna المحدود
7. Honest and negative-control comparison | مقارنة التحقق الصادق والضوابط السلبية
8. Mean and sample variation interpretation | تفسير المتوسط والتشتت العيّني
9. Out-of-fold coverage | تغطية OOF
10. Learner-owned validation argument | حجة التحقق التي يكتبها المتدرب
11. Evidence export and provenance | تصدير الأدلة ومصدرها
12. Completion checkpoint and Day 3 bridge | بوابة الإكمال والربط باليوم الثالث

## 2. Day 2 guide rebuilt | إعادة بناء دليل اليوم الثاني

`DAY2_GUIDE.md` was rebuilt as a complete side-by-side bilingual guide. It now includes:

- A precise 60-minute execution plan.
- Fresh free-CPU instructions and pinned-environment safeguards.
- The five leakage risks and their required guards.
- The strict target-maturity condition: `application date + 90 days < validation start`.
- Released fold counts and the zero-shared-customer condition.
- The 1,935-row reserved historical search cohort.
- Search budget, trial states and educational-example restrictions.
- Definitions and limitations of all four comparison protocols.
- Correct interpretation of fold means, sample standard deviation and OOF coverage.
- Five learner-owned reasoning requirements.
- A table of the 15 files inside the Day 2 evidence bundle.
- Readiness states, troubleshooting and technical references.

أعيد بناء `DAY2_GUIDE.md` كدليل ثنائي كامل يشرح مخاطر التسرب وحدود الطيات ومجموعة البحث المحجوزة وميزانية Optuna والبروتوكولات الأربعة وتغطية OOF ومتطلبات التفسير وملفات الأدلة وحالات الجاهزية.

## 3. Executable-code protection | حماية الكود التنفيذي

A released-code contract was generated in:

```text
content/day2_notebook_code_contract.json
```

It records stable IDs and SHA-256 hashes for all **10 executable cells** from the released `v1.0.0` notebook.

Result:

```text
Expected executable cells: 10
Actual executable cells:   10
Missing cells:              0
Unexpected cells:           0
Changed cells:              0
Status:                     PASS
```

يفشل العقد عند فقد خلية أو إضافة خلية غير متوقعة أو تغير أي بايت في الكود المحمي. اقتصر التحويل على Markdown وMetadata التعليميين.

## 4. Deterministic generation | التوليد الحتمي

Added:

```text
scripts/build_bilingual_day2.py
.github/workflows/build_bilingual_day2.yml
```

The controlled build workflow:

1. Captures the released executable-cell contract.
2. Replaces only the 12 expected learner-facing Markdown cells.
3. Rejects a missing or unexpected section.
4. Verifies executable-cell identity before and after conversion.
5. Writes the production notebook and contract.
6. Commits generated outputs only when they differ.
7. Uploads build evidence for review.

Generated notebook commit:

```text
4d6cb413c3ff10b04eedffea518148be7b6a5e29
```

## 5. Honest-validation scientific parity | تطابق مخرجات التحقق الصادق

A dedicated workflow executes the released `main` notebook and the bilingual candidate in separate fresh workspaces, then compares stable Day 2 outputs.

Added:

```text
scripts/check_day2_reference_parity.py
.github/workflows/day2_reference_parity.yml
```

**Workflow:** `Day 2 Reference Parity`  
**Run:** `37101440142`  
**Result:** `PASS`

Verified row-for-row and value-for-value, after excluding only documented volatile timing fields:

| Artifact | Reference rows | Candidate rows | Result |
|---|---:|---:|---|
| `validation_report.csv` | 12 | 12 | Match |
| `validation_summary.csv` | 4 | 4 | Match |
| `optuna_results.csv` | 8 | 8 | Match |
| `leakage_audit.csv` | 28 | 28 | Match |
| `fold_audit.csv` | 3 | 3 | Match |
| `day2_oof_predictions.csv` | 10,078 | 10,078 | Match |
| `day2_oof_coverage.csv` | 10,000 | 10,000 | Match |

Stable JSON content also matches for:

```text
best_params.json
day2_provenance.json
day2_reflection.json
day2_run.json
```

The parity run confirmed:

- `TECHNICAL_READY` in both versions.
- OOF whole-data coverage of `0.5039` in both versions.
- 5,039 OOF predictions for each of the two honest schemes.
- The same leakage decisions, fold boundaries, model metrics, live-search results, parameters, predictions and provenance.
- All 16 expected generated files exist in both runs, including `day2_artifacts.zip`.
- Training/search timing values and image bytes are intentionally excluded from equality claims.

تحقق المسار من تطابق قرارات التسرب وحدود الطيات ونتائج البحث والمقاييس و10,078 صف تنبؤ OOF وتغطية 10,000 طلب ومصدر التدريب وحالة التشغيل وحصر الملفات الناتجة.

## 6. Automated quality evidence | أدلة الجودة الآلية

Validation against implementation head `701956af0a48b3bbc9fb66c4b1c153728220cc44`:

| Quality gate | Run | Result |
|---|---:|---|
| Bilingual Content Check | `37101440187` | PASS |
| Environment Check | `37101440161` | PASS |
| Day 1 Reference Parity regression guard | `37101440153` | PASS |
| Day 2 Reference Parity | `37101440142` | PASS |
| Notebook Smoke Test | `37101440179` | Queued at report creation |

The bilingual quality gate now checks the Day 2 guide, all 12 paired notebook sections and the exact 10-cell executable contract. The notebook-smoke workflow was extended to verify Notebook 00, Day 1 and Day 2 code contracts before executing Notebooks 00–05 in fresh kernels; its queued run is not represented as a passed check until GitHub completes it.

تحقق بوابة المحتوى من الدليل الثنائي والأقسام الاثني عشر وعقد الخلايا العشر. وجرى توسيع اختبار التشغيل ليفحص عقود دفاتر 00 و01 و02 قبل تشغيل الدفاتر 00–05 في Kernels جديدة، ولا يُسجل التشغيل المعلّق بوصفه ناجحًا قبل اكتماله.

## 7. Phased migration status | حالة التحويل المرحلي

The bilingual manifest now marks the following production learner files as complete:

```text
README.md
GLOSSARY.md
DAY1_GUIDE.md
DAY2_GUIDE.md
notebooks/00_readiness_check.ipynb
notebooks/01_baseline_boosting.ipynb
notebooks/02_validation_tuning.ipynb
```

Notebooks 03–05 and 99 remain `planned`. This prevents a partial migration from being presented as a finished bilingual release.

يسجل Manifest أن أدلة اليومين الأول والثاني ودفاتر 00 و01 و02 مكتملة، بينما تبقى دفاتر 03–05 و99 في حالة `planned`.

## 8. Acceptance still pending | القبول المتبقي

The following items are deliberately not marked complete:

1. Manual execution in a fresh hosted Google Colab account.
2. Visual review of all paired sections inside the actual Colab interface.
3. Responsive/mobile review of long bilingual tables.
4. Completion of the queued final Notebook Smoke Test for this implementation head.
5. Conversion and verification of Notebooks 03–05 and 99.
6. Conversion of Days 3–5 guides, requirements, reports, rubric and submission documents.
7. Final release-hash rebuild after all learner-facing files are frozen.
8. Private evaluator and private submission registry.
9. Merge to `main` and publication of `v1.1.0`.

## Phase 5 entry | دخول المرحلة الخامسة

Day 3 may be converted next using the same controlled pattern:

1. Capture the released Day 3 executable-cell contract.
2. Convert learner-facing Markdown only.
3. Rebuild `DAY3_GUIDE.md` side by side.
4. Preserve the distinction between simulated decision costs and real financial outcomes.
5. Extend bilingual and smoke quality gates.
6. Compare stable Day 3 outputs against the released reference.
7. Keep `main` and the published portal unchanged until the full release passes.

يمكن بدء اليوم الثالث بالنمط المحكوم نفسه، مع حماية الكود وتحويل الشرح فقط ودليل ثنائي وفحوص جودة ومقارنة للمخرجات، دون تغيير `main` أو الإصدار المنشور.
