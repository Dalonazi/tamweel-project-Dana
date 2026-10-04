# Private evaluator specification | مواصفات المقيم الخاص

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

## Purpose | الغرض

The private evaluator independently verifies that a submitted repository can reproduce predictions and required evidence from the exact submitted commit. It must live in a private repository controlled by the instructor and must never expose hidden labels, student grades or security credentials.

يتحقق المقيم الخاص بصورة مستقلة من قدرة مستودع الطالب على إعادة إنتاج التنبؤات والأدلة المطلوبة من Commit التسليم نفسه. يجب أن يوجد في مستودع خاص تديره المدربة، وألا يكشف التسميات المخفية أو الدرجات أو بيانات الدخول.

## Required input | المدخلات المطلوبة

```text
cohort_code
student_code
repository_url
exact_commit_sha
final_tag
submission_receipt_id
```

The evaluator checks out the exact SHA, not the current `main` branch.

يسحب المقيم Commit SHA الدقيق، ولا يعتمد على آخر نسخة من `main`.

## Inference contract | عقد الاستدلال

Every final project must support:

```bash
python -m tamweel.inference \
  --input hidden_features.csv \
  --output predictions.csv
```

Required output columns:

```text
application_id, probability
```

The evaluator applies the frozen batch decision policy separately and compares the regenerated output with the submitted artifacts.

## Evaluation stages | مراحل التقييم

1. **Repository identity** — verify URL, SHA, tag and manifest consistency.
2. **Clean environment** — install pinned CPU dependencies in an isolated workspace.
3. **Forbidden-content scan** — reject hidden labels, secrets, evaluator files and prohibited personal data.
4. **Rebuild** — run the documented build and inference path with `ASSESSMENT_MODE=1`.
5. **Hidden features** — predict on private feature rows never included in the learner template.
6. **Row-order test** — shuffle input order and verify predictions remain attached to `application_id`.
7. **Perturbation test** — change selected input values and verify the model responds rather than returning fixed predictions.
8. **Reproduction test** — compare regenerated artifacts with submitted files within declared numeric tolerances.
9. **Integrity gates** — evaluate leakage, challenge isolation, threshold source, hard-coding, version identity and recovery disclosure.
10. **Private score report** — write machine evidence and instructor observations without publishing grades.

1. **هوية المستودع** — التحقق من الرابط وSHA وTag وManifest.
2. **بيئة نظيفة** — تثبيت بيئة CPU معزولة بالإصدارات المحددة.
3. **فحص المحتوى المحظور** — رفض التسميات المخفية والأسرار وملفات المقيم والبيانات الشخصية المحظورة.
4. **إعادة البناء** — تشغيل مسار البناء والاستدلال مع `ASSESSMENT_MODE=1`.
5. **خصائص مخفية** — التنبؤ على صفوف لم تُنشر في قالب المتدرب.
6. **اختبار ترتيب الصفوف** — تغيير الترتيب والتحقق من ارتباط التنبؤ بالمعرف.
7. **اختبار التغيير** — تعديل قيم مختارة والتأكد من أن النموذج يستجيب بدل إخراج قيم ثابتة.
8. **اختبار إعادة الإنتاج** — مقارنة المخرجات المعاد توليدها بملفات التسليم ضمن حدود رقمية معلنة.
9. **بوابات النزاهة** — فحص التسرب وعزل التحدي ومصدر العتبة والتثبيت اليدوي وهوية النسخة والإفصاح عن التعافي.
10. **تقرير درجات خاص** — حفظ الأدلة الآلية وملاحظات المدربة دون نشر الدرجات.

## Hidden assets | الأصول المخفية

The private repository contains:

```text
hidden/hidden_features.csv
hidden/hidden_labels.csv
hidden/student_profiles.csv
checks/test_inference_contract.py
checks/test_row_order.py
checks/test_prediction_variation.py
checks/test_forbidden_files.py
checks/test_reproducibility.py
rubric/private_scoring.yml
```

None of these files may be copied into the public learner template.

## Student profiles | ملفات المتدربين

Use a small set of controlled policy profiles to reduce answer copying while preserving a common learning path:

| Profile | FN weight | FP weight | Capacity |
|---|---:|---:|---:|
| A | 10 | 1 | 12% |
| B | 12 | 1 | 10% |
| C | 8 | 2 | 15% |
| D | 15 | 2 | 8% |

The profile changes policy analysis, not the hidden model labels.

## Security and privacy | الأمن والخصوصية

- No student credentials are stored.
- Use read-only access to public repositories or instructor-approved temporary access to private submissions.
- Logs redact URLs containing credentials and never print secrets.
- Grades and receipts remain private.
- Hidden labels are never uploaded as workflow artifacts.
- Retain evidence according to the cohort policy, then delete temporary clones.

## Output | المخرج

Each evaluation creates a private JSON report and a human-readable Markdown report containing:

```text
identity_status
clean_run_status
inference_status
hidden_metric_summary
integrity_gate_results
reproducibility_result
manual_review_required
private_score_breakdown
```

This specification is a blueprint only until the private repository and hidden assets are created and tested.

هذه المواصفات مخطط تنفيذي فقط إلى أن يُنشأ المستودع الخاص وتُضاف الأصول المخفية وتُختبر فعليًا.
