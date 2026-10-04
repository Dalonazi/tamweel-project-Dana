# Assessment Rubric | سلم التقييم

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Scoring model

The assessment has two components:

- **Project:** 90 points.
- **Presentation and defence:** 10 points.
- **Total:** 100 points.

Pass is **70 or more**. Distinction is **95 or more**. Scores are compared before display rounding.

The rubric rewards method, evidence, reproducibility and reasoning. A high AUC, a low simulated decision cost or a green automated check does not by itself prove project quality.

</td>
<td width="50%" valign="top" dir="rtl">

## نموذج احتساب الدرجة

يتكون التقييم من جزأين:

- **المشروع:** 90 نقطة.
- **العرض والمناقشة:** 10 نقاط.
- **الإجمالي:** 100 نقطة.

النجاح من **70 فأعلى**، والتميز من **95 فأعلى**. تُقارن الدرجات قبل تقريب العرض.

يكافئ السلم المنهج والأدلة وقابلية إعادة الإنتاج والتفسير. لا تكفي قيمة AUC مرتفعة أو تكلفة قرار تعليمية منخفضة أو فحوص آلية خضراء وحدها لإثبات جودة المشروع.

</td>
</tr>
</table>

## Project criteria — 90 points | معايير المشروع — 90 نقطة

| Code | Points | English criterion | المعيار بالعربية | Primary evidence |
|---|---:|---|---|---|
| J1 | 8 | Repository structure, bilingual navigation and clear learner journey | تنظيم المستودع والتنقل الثنائي ووضوح رحلة المتدرب | README, links, folders, rendered pages |
| J2 | 12 | Reproducibility, Colab readiness and clean `Run all` execution | قابلية إعادة الإنتاج وجاهزية Colab وتشغيل `Run all` نظيف | versions, seeds, hashes, logs, manifest |
| J3 | 10 | Day 1 baseline and boosting comparison | اليوم الأول: خط الأساس ومقارنة التعزيز | fair model comparison, learning curves, candidate decision |
| J4 | 15 | Day 2 honest validation, leakage control and bounded Optuna search | اليوم الثاني: التحقق الصادق ومنع التسرب وبحث Optuna المحدود | role/fold audits, OOF evidence, search results |
| J5 | 15 | Day 3 imbalance treatment, simulated decision cost, threshold and capacity | اليوم الثالث: معالجة عدم التوازن وتكلفة القرار التعليمية والعتبة والسعة | OOF predictions, threshold sweep, Decision Card |
| J6 | 15 | Day 4 permutation importance, SHAP, calibration and stability | اليوم الرابع: أهمية التبديل وSHAP والمعايرة والاستقرار | figures, metrics, Interpretability Report |
| J7 | 7 | Day 5 ensemble decision, integrated pipeline and portable inference | اليوم الخامس: قرار التجميع والخط المتكامل والاستدلال القابل للنقل | Worth-It Gate, final model, inference test |
| J8 | 5 | Model Card, responsible-use limits, regional audit and unresolved gaps | بطاقة النموذج وحدود الاستخدام المسؤول وتدقيق المناطق والفجوات | Model Card, limitations, monitoring notes |
| J9 | 3 | Final tag, exact SHA, manifest and submission bundle | Tag النهائي وSHA الدقيق وmanifest وحزمة التسليم | immutable reference, hashes, receipt record |
|  | **90** | **Project subtotal** | **مجموع المشروع** |  |

## Presentation criteria — 10 points | معايير العرض — 10 نقاط

| Code | Points | English criterion | المعيار بالعربية | Primary evidence |
|---|---:|---|---|---|
| P1 | 2 | Problem, target and practical value are defined accurately | تعريف المشكلة والهدف والقيمة العملية بدقة | Slide 1 |
| P2 | 2 | Architecture, data roles and validation method are clear | وضوح المعمارية وأدوار البيانات ومنهج التحقق | Slide 2 |
| P3 | 3 | Evidence, metrics, threshold and simulated decision cost are interpreted correctly | تفسير الأدلة والمقاييس والعتبة وتكلفة القرار التعليمية بصورة صحيحة | Slide 3 |
| P4 | 2 | Explainability, calibration, limits and responsible-use boundaries are communicated | شرح التفسير والمعايرة والقيود وحدود الاستخدام المسؤول | Slides 4–5 |
| P5 | 1 | Oral answers are consistent with the learner’s repository evidence | اتساق إجابات المناقشة مع أدلة مستودع المتدرب | Defence questions |
|  | **10** | **Presentation subtotal** | **مجموع العرض** |  |

## Performance levels | مستويات الأداء

Use the following level descriptors when allocating points within each criterion.

تُستخدم الأوصاف الآتية عند توزيع نقاط كل معيار.

| Level | English descriptor | الوصف بالعربية | Typical score range within a criterion |
|---|---|---|---|
| 4 — Mastered | Correct, complete, reproducible, well justified and supported by internally consistent evidence. Limitations are stated without prompting. | صحيح ومكتمل وقابل لإعادة الإنتاج ومبرر جيدًا ومدعوم بأدلة متسقة داخليًا. يوضح القيود دون مطالبة. | 90–100% of criterion points |
| 3 — Achieved | Core requirement is correct and reproducible. Minor gaps in explanation, organisation or evidence do not change the conclusion. | المتطلب الأساسي صحيح وقابل لإعادة الإنتاج، مع نواقص محدودة في الشرح أو التنظيم أو الأدلة لا تغيّر الاستنتاج. | 70–89% |
| 2 — Partially achieved | An output exists, but the method, evidence or interpretation is incomplete, weakly justified or only partly reproducible. | يوجد مخرج، لكن المنهج أو الدليل أو التفسير ناقص أو ضعيف التبرير أو قابل لإعادة الإنتاج جزئيًا فقط. | 40–69% |
| 1 — Not achieved | Required output is missing, materially incorrect, unsupported, fabricated or not reproducible. | المخرج المطلوب مفقود أو خاطئ جوهريًا أو غير مدعوم أو مصطنع أو غير قابل لإعادة الإنتاج. | 0–39% |

## Integrity gates | بوابات النزاهة

A total score is not final until the following gates are cleared. A blocked gate causes the project to be returned for correction or investigated before the affected criteria are graded.

لا تصبح الدرجة الإجمالية نهائية قبل اجتياز البوابات الآتية. يؤدي تعطل البوابة إلى إعادة المشروع للتصحيح أو التحقق قبل تقييم المعايير المتأثرة.

| Gate | Blocking condition | الحالة المانعة |
|---|---|---|
| G1 — Leakage | A known post-outcome, target-derived or prohibited feature is used. | استخدام خاصية معروفة بعد النتيجة أو مشتقة من الهدف أو محظورة. |
| G2 — Challenge isolation | Challenge labels or hidden evaluator data are used for training, tuning, calibration or threshold selection. | استخدام تسميات التحدي أو بيانات المقيم المخفية في التدريب أو الضبط أو المعايرة أو اختيار العتبة. |
| G3 — Honest policy selection | The final threshold is selected from the final evaluation or challenge data. | اختيار العتبة النهائية من بيانات التقييم النهائي أو التحدي. |
| G4 — Reproducibility | The recorded commit cannot reproduce the required outputs or inference interface. | عدم قدرة Commit المسجل على إعادة إنتاج المخرجات المطلوبة أو واجهة الاستدلال. |
| G5 — Hard-coding | Predictions, metrics, screenshots or evidence are hard-coded, fabricated or copied. | تثبيت التنبؤات أو المقاييس أو الصور أو الأدلة يدويًا أو اصطناعها أو نسخها. |
| G6 — Version identity | Final tag, exact SHA, manifest and submitted files do not identify the same version. | عدم تطابق Tag النهائي وSHA الدقيق والـmanifest والملفات المسلّمة على النسخة نفسها. |
| G7 — Recovery disclosure | Recovery/example output is presented as personal execution evidence without disclosure. | تقديم مخرجات الاستعادة أو المثال بوصفها تنفيذًا شخصيًا دون إفصاح. |
| G8 — Privacy/security | Secrets, personal data, private grades, receipts or hidden labels are published. | نشر أسرار أو بيانات شخصية أو درجات أو إيصالات خاصة أو تسميات مخفية. |
| G9 — Oral ownership | The learner cannot explain a central decision or identify the supporting evidence in the submitted repository. | عدم قدرة المتدرب على شرح قرار محوري أو تحديد دليله داخل المستودع المسلّم. |

## Score calculation rules | قواعد احتساب الدرجة

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Project score is the sum of `J1–J9`, capped at 90.
2. Presentation score is the sum of `P1–P5`, capped at 10.
3. Final score = project score + presentation score.
4. Compare the unrounded score with the pass and distinction thresholds.
5. `69.99` is below the pass threshold; `94.99` is below the distinction threshold.
6. The simulated decision loss `10 × FN + FP` is an analytical course metric. Its units are not deducted from the grade.
7. Automated checks provide evidence, not automatic marks or a submission receipt.
8. The instructor evaluates the learner’s explanation, evidence quality and defence in addition to technical execution.

</td>
<td width="50%" valign="top" dir="rtl">

1. درجة المشروع هي مجموع `J1–J9` وبحد أقصى 90.
2. درجة العرض هي مجموع `P1–P5` وبحد أقصى 10.
3. الدرجة النهائية = درجة المشروع + درجة العرض.
4. تُقارن الدرجة غير المقربة بحدي النجاح والتميز.
5. الدرجة `69.99` أقل من النجاح، و`94.99` أقل من التميز.
6. تكلفة القرار التعليمية `10 × FN + FP` مقياس تحليلي للدورة، ولا تُخصم وحداتها من الدرجة.
7. تقدم الفحوص الآلية أدلة، ولا تمنح درجات آلية أو إيصال استلام.
8. تقيّم المدربة شرح المتدرب وجودة الأدلة والمناقشة إلى جانب التنفيذ التقني.

</td>
</tr>
</table>
