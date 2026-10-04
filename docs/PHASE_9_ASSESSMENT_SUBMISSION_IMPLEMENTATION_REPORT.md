# Phase 9 — Assessment and Submission Governance
# المرحلة التاسعة — حوكمة التقييم والتسليم

## Scope | النطاق

This phase strengthens the learner-facing governance layer without changing any notebook code, model logic, data contract or scientific output.

تعزز هذه المرحلة طبقة الحوكمة الموجهة للمتدرب دون تغيير أي كود داخل الدفاتر أو منطق للنماذج أو عقد للبيانات أو مخرج علمي.

## Files implemented | الملفات المنفذة

- `TECHNICAL_REQUIREMENTS.md`
- `ADMINISTRATIVE_REQUIREMENTS.md`
- `RUBRIC.md`
- `SUBMISSION_GUIDE.md`
- `COURSE_ALIGNMENT.md`
- `content/bilingual_manifest.yml`

## Design decisions | القرارات التصميمية

1. English is independently readable and Arabic is independently readable.
2. Side-by-side content uses English LTR on the left and Arabic RTL on the right where practical.
3. The project remains 90 points and the presentation/defence remains 10 points.
4. Performance descriptors were added without changing the criterion weights.
5. Integrity gates are separate from score thresholds.
6. The simulated decision loss is explicitly an educational analytical unit, not Saudi riyals and not a grade deduction.
7. The final submission is one complete repository after five progressive build stages.
8. Public GitHub issues are not accepted as a private submission record.
9. Cohort deadlines and resubmission rules must have a written private record; a verbal announcement is not the only evidence.
10. A green automated check is evidence of technical execution, not a grade, authenticity decision or receipt.

1. يمكن قراءة الإنجليزية باستقلال، ويمكن قراءة العربية باستقلال.
2. يظهر المحتوى المتوازي بالإنجليزية يسارًا LTR والعربية يمينًا RTL حيث يكون ذلك عمليًا.
3. بقي المشروع 90 نقطة والعرض والمناقشة 10 نقاط.
4. أضيفت مستويات الأداء دون تغيير أوزان المعايير.
5. فُصلت بوابات النزاهة عن حدود الدرجات.
6. وُضّح أن تكلفة القرار التعليمية وحدة تحليلية تعليمية، وليست ريالات سعودية ولا خصمًا من الدرجة.
7. التسليم النهائي مستودع واحد كامل بعد خمس مراحل بناء متدرجة.
8. لا تُقبل Issues العامة في GitHub بوصفها سجل تسليم خاصًا.
9. يجب أن يكون لمواعيد الدفعة وقواعد إعادة التسليم سجل خاص مكتوب؛ ولا يكون الإعلان الشفهي الدليل الوحيد.
10. الفحص الآلي الأخضر دليل تنفيذ تقني، وليس درجة أو حكمًا بالأصالة أو إيصال استلام.

## Assessment model preserved | نموذج التقييم المحفوظ

| Component | Points | المكوّن | النقاط |
|---|---:|---|---:|
| Technical and administrative project | 90 | المشروع التقني والإداري | 90 |
| Presentation and defence | 10 | العرض والمناقشة | 10 |
| Total | 100 | الإجمالي | 100 |

Pass remains `≥ 70`; distinction remains `≥ 95`; comparison occurs before display rounding.

بقي النجاح `≥ 70` والتميز `≥ 95`، وتتم المقارنة قبل تقريب الرقم المعروض.

## New governance controls | ضوابط الحوكمة الجديدة

- Technical acceptance matrix `T1–T12`.
- Administrative acceptance matrix `A1–A12`.
- Four performance levels for every rubric criterion.
- Nine integrity gates covering leakage, hidden data, threshold selection, reproducibility, hard-coding, version identity, recovery disclosure, privacy and oral ownership.
- Required private submission fields and timestamped receipt.
- Immutable tag and exact 40-character commit SHA.
- Clear resubmission version-replacement rule.
- Course-outcome traceability from objective to lab, artifact and rubric.

- مصفوفة قبول تقني `T1–T12`.
- مصفوفة قبول إداري `A1–A12`.
- أربعة مستويات أداء لكل معيار.
- تسع بوابات نزاهة تشمل التسرب والبيانات المخفية واختيار العتبة وقابلية إعادة الإنتاج والتثبيت اليدوي وهوية النسخة والإفصاح عن الاستعادة والخصوصية والملكية الشفهية.
- حقول تسليم خاص إلزامية وإيصال مؤرخ.
- Tag غير قابل للتغيير وCommit SHA كامل من 40 محرفًا.
- قاعدة واضحة لاستبدال النسخة عند إعادة التسليم.
- تتبع مخرجات الدورة من الهدف إلى اللاب والمخرج ومعيار التقييم.

## Verification boundaries | حدود التحقق

- No executable notebook cell was edited in this phase.
- Existing released-reference parity checks remain regression guards.
- The bilingual manifest now enforces the new learner-facing governance files.
- Final hosted-Colab acceptance and the private evaluator remain release blockers.

- لم تُعدّل أي خلية تنفيذية في هذه المرحلة.
- تبقى اختبارات التطابق مع الإصدار المنشور حواجز لمنع الانحدار.
- يفرض manifest الثنائي الآن التحقق من ملفات الحوكمة الجديدة الموجهة للمتدرب.
- يبقى اختبار Colab المستضاف والمقيّم الخاص من متطلبات ما قبل الإصدار.

## Release status | حالة الإصدار

This phase is part of the controlled `v1.1.0` candidate on `develop/bilingual-v1.1.0`. It must not be merged until the complete release checklist is satisfied.

هذه المرحلة جزء من مرشح الإصدار المحكوم `v1.1.0` على فرع `develop/bilingual-v1.1.0`. ولا تُدمج قبل استيفاء قائمة اعتماد الإصدار كاملة.
