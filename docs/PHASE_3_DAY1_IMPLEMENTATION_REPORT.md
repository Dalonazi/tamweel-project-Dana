# Phase 3 — Day 1 Bilingual Implementation Report | تقرير المرحلة الثالثة — تنفيذ اليوم الأول ثنائي اللغة

**Target release:** `v1.1.0`  
**Development branch:** `develop/bilingual-v1.1.0`  
**Published learner release:** `v1.0.0` remains unchanged  
**Scope:** Notebook 01, Day 1 guide, executable-code protection, scientific-output parity and fresh-kernel validation

## Release decision | قرار الإصدار

Day 1 is technically accepted inside the controlled draft branch. It is not yet published to learners and the pull request must remain in Draft state until Notebooks 02–05 and 99, all learner guides, the final release hashes and the manual hosted-Colab acceptance are complete.

تم قبول اليوم الأول تقنيًا داخل فرع التطوير المحكوم. لم يُنشر للمتدربين بعد، ويجب أن يبقى Pull Request بصيغة Draft حتى اكتمال دفاتر 02–05 و99 وجميع أدلة المتدرب وبصمات الإصدار النهائية واختبار القبول اليدوي داخل Colab المستضاف.

## 1. Production notebook converted | تحويل الدفتر الفعلي

The production file `notebooks/01_baseline_boosting.ipynb` now contains **12 paired learner-facing sections** with:

- English on the left using explicit `dir="ltr"`.
- Arabic on the right using explicit `dir="rtl"`.
- One shared executable path; code is not duplicated by language.
- Equivalent objectives, warnings, evidence requirements and completion criteria.
- Beginner-focused explanations without removing the specialist concepts.
- Consistent use of **Simulated Decision Cost | تكلفة القرار التعليمية**.

أصبح الملف الفعلي `notebooks/01_baseline_boosting.ipynb` يحتوي على **12 قسمًا تعليميًا ثنائيًا**؛ الإنجليزية يسارًا والعربية يمينًا، مع مسار تنفيذ مشترك واحد وتكافؤ الأهداف والتحذيرات والأدلة ومعايير الإكمال.

### Paired sections | الأقسام الثنائية

1. Day purpose, limits and 60-minute journey | هدف اليوم وحدوده ورحلة 60 دقيقة
2. Environment setup | تجهيز البيئة
3. Task and data understanding | فهم المهمة والبيانات
4. Data-role separation | فصل أدوار البيانات
5. Logistic Regression baseline | خط الأساس
6. Boosting and early stopping | التعزيز والإيقاف المبكر
7. Learning-curve interpretation | تفسير منحنيات التعلم
8. Fair model comparison | المقارنة العادلة
9. ROC and precision–recall interpretation | تفسير ROC وprecision–recall
10. Learner-owned decision | قرار المتدرب
11. Evidence export | تصدير الأدلة
12. Completion gate and next step | بوابة الإكمال والخطوة التالية

## 2. Day 1 guide rebuilt | إعادة بناء دليل اليوم الأول

`DAY1_GUIDE.md` was converted into a complete side-by-side bilingual guide. It now includes:

- A precise 60-minute run plan.
- Fresh-session and free-CPU instructions.
- The four data roles and their exact row counts.
- Correct interpretation of ROC-AUC, Average Precision and selected tree counts.
- Learner-owned reasoning requirements.
- The eight required artifact files.
- Readiness-state meanings.
- Troubleshooting and completion gates.
- Privacy and credential restrictions.

جرى تحويل `DAY1_GUIDE.md` إلى دليل ثنائي كامل يتضمن خطة الزمن وأدوار البيانات وتفسير المقاييس ومتطلبات القرار والأدلة الثمانية وحالات الجاهزية وحل المشكلات وبوابة الإكمال.

## 3. Executable-code protection | حماية الكود التنفيذي

A released-code contract was captured in:

```text
content/day1_notebook_code_contract.json
```

It records the stable IDs and SHA-256 hashes of all **10 executable cells** from the released `v1.0.0` notebook.

The reusable checker rejects:

- A missing executable cell.
- An unexpected executable cell.
- Any byte-level change in a protected code cell.

Result:

```text
Expected executable cells: 10
Actual executable cells:   10
Missing cells:              0
Unexpected cells:           0
Changed cells:              0
Status:                     PASS
```

يسجل العقد معرفات وبصمات الخلايا التنفيذية العشر من الإصدار المنشور، ويفشل عند فقد خلية أو إضافة خلية غير متوقعة أو تغير أي بايت في الكود المحمي.

## 4. Deterministic generation | التوليد الحتمي

Added:

```text
scripts/capture_notebook_code_contract.py
scripts/build_bilingual_day1.py
.github/workflows/build_bilingual_day1.yml
```

The build workflow captures the released contract, replaces only the 12 learner-facing Markdown cells, verifies executable-cell identity before and after conversion, writes the production notebook and uploads build evidence.

**Build workflow:** `Build Bilingual Day 1 Notebook`  
**Run:** `37100287588`  
**Result:** `success`  
**Generated notebook commit:** `57c40a467983ec71f9f15387a19dc1b1f2a905cc`

يولد المسار الآلي الدفتر الثنائي بصورة حتمية، ويستبدل خلايا الشرح فقط، ويتحقق من ثبات الكود قبل التحويل وبعده.

## 5. Scientific-output parity | تطابق المخرجات العلمية

A dedicated workflow executes the released `main` notebook and the bilingual candidate in separate fresh workspaces, then compares stable scientific outputs.

Added:

```text
scripts/check_day1_reference_parity.py
.github/workflows/day1_reference_parity.yml
```

**Final parity workflow:** `Day 1 Reference Parity`  
**Run:** `37100712997`  
**Result:** `success`

Verified:

- Stable model-comparison columns match.
- All 2,000 comparison prediction rows match.
- All 10,000 split-membership rows match.
- Stable run metadata and hashes match.
- All nine required generated files, including the ZIP bundle, exist in both runs.
- Volatile timing values and image bytes are intentionally excluded from equality claims.

تم التحقق من تطابق أعمدة المقارنة العلمية و2,000 صف تنبؤ و10,000 صف عضوية تقسيم وبيانات التشغيل الثابتة وحصر الملفات الناتجة. لا يشمل ادعاء التطابق قيم الزمن المتغيرة أو بايتات الصور.

## 6. Automated quality evidence | أدلة الجودة الآلية

Validation was run against final implementation commit `86e70fe3dc7a3f66736f393358343880aab1fb00`.

| Quality gate | Run | Result |
|---|---:|---|
| Bilingual Content Check | `37100713039` | PASS |
| Environment Check | `37100713100` | PASS |
| Day 1 Reference Parity | `37100712997` | PASS |
| Notebook Smoke Test | `37100713031` | PASS |

The final Notebook Smoke Test also verified the Notebook 00 and Day 1 executable-cell contracts, executed Notebooks 00–05 in fresh kernels, staged reports outside the project inventory and uploaded the resulting evidence artifact.

تحقق اختبار التشغيل النهائي من عقدي كود دفتر 00 واليوم الأول، وشغّل الدفاتر 00–05 في Kernels جديدة، وحفظ التقارير خارج حصر ملفات مشروع الطالب ثم رفع أدلة التشغيل.

## 7. Phased migration status | حالة التحويل المرحلي

The bilingual manifest now marks the following learner files as complete:

```text
README.md
GLOSSARY.md
DAY1_GUIDE.md
notebooks/00_readiness_check.ipynb
notebooks/01_baseline_boosting.ipynb
```

The manifest keeps Notebooks 02–05 and 99 in `planned` status so incomplete conversion cannot be presented as a finished bilingual release.

يسجل Manifest أن README والقاموس ودليل اليوم الأول ودفترَي 00 و01 مكتملة، بينما تبقى دفاتر 02–05 و99 في حالة `planned` لمنع تقديم التحويل الجزئي بوصفه إصدارًا مكتملًا.

## 8. Acceptance still pending | القبول المتبقي

The following items are deliberately not marked complete:

1. Manual execution in a fresh hosted Google Colab account.
2. Visual review of all 12 paired sections inside the actual Colab interface.
3. Responsive/mobile review of long bilingual tables.
4. Conversion and verification of Notebooks 02–05 and 99.
5. Conversion of Days 2–5 guides, requirements, reports, rubric and submission documents.
6. Final release-hash rebuild after all learner-facing files are frozen.
7. Private evaluator and private submission registry.
8. Merge to `main` and publication of `v1.1.0`.

لم يُعتمد بعد التشغيل اليدوي في حساب Colab نظيف، أو الفحص البصري داخل Colab، أو تحويل بقية الأيام، أو إعادة بناء بصمات الإصدار النهائية، أو المقيم الخاص، أو الدمج والنشر.

## Phase 4 entry | دخول المرحلة الرابعة

Day 2 may be converted next using the same controlled pattern:

1. Capture the released executable-cell contract.
2. Convert learner-facing Markdown only.
3. Rebuild the Day 2 guide side by side.
4. Extend bilingual and smoke quality gates.
5. Compare stable outputs against the released reference.
6. Keep `main` and the published portal unchanged until the full release passes.

يمكن بدء اليوم الثاني بالنمط المحكوم نفسه: عقد للكود المنشور، وتحويل الشرح فقط، ودليل ثنائي، وفحوص جودة، ومقارنة المخرجات مع المرجع المنشور، دون تغيير `main`.
