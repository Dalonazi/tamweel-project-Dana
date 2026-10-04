# Technical Requirements | المتطلبات التقنية

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Purpose

These requirements define the minimum technical contract for the Tamweel Lite project. They are not optional styling preferences. The final repository must be reproducible, auditable and runnable on free Google Colab CPU without paid services, API keys, GPUs or a local installation.

</td>
<td width="50%" valign="top" dir="rtl">

## الغرض

تحدد هذه المتطلبات الحد الأدنى للعقد التقني لمشروع **Tamweel Lite**. وهي ليست تفضيلات شكلية اختيارية. يجب أن يكون المستودع النهائي قابلًا لإعادة الإنتاج والمراجعة والتشغيل على CPU المجاني في Google Colab، من دون خدمات مدفوعة أو مفاتيح API أو GPU أو تثبيت محلي إلزامي.

</td>
</tr>
</table>

## Technical acceptance matrix | مصفوفة القبول التقني

| Code | English requirement | المتطلب بالعربية | Required evidence |
|---|---|---|---|
| T1 | Use the pinned free-CPU environment. No paid subscription, API key, token, GPU or Drive mount is required for the assessed path. | استخدم بيئة CPU المجانية ذات الإصدارات المثبتة. لا يحتاج مسار التقييم إلى اشتراك مدفوع أو مفتاح API أو رمز وصول أو GPU أو ربط Drive. | `environment.json`, executed notebooks, clean `Run all` |
| T2 | Use only the synthetic course data and preserve the published role separation. Challenge labels must remain unavailable to the learner workflow. | استخدم بيانات الدورة الاصطناعية فقط، وحافظ على فصل الأدوار المنشور. يجب ألا تكون تسميات التحدي متاحة لمسار عمل المتدرب. | data hashes, role audit, provenance files |
| T3 | Learn preprocessing, imputation, weighting and resampling from training rows only. Do not fit them on validation, policy, calibration, evaluation or challenge rows. | تعلّم المعالجة والتعويض والأوزان وإعادة أخذ العينات من صفوف التدريب فقط. لا تُلائمها على صفوف التحقق أو السياسة أو المعايرة أو التقييم أو التحدي. | notebook logic, fold/role audits |
| T4 | Use honest out-of-fold predictions for model comparison and threshold selection where specified. Do not choose the threshold from the final evaluation or challenge data. | استخدم تنبؤات OOF الصادقة لمقارنة النماذج واختيار العتبة حيث يطلب ذلك. لا تختَر العتبة من بيانات التقييم النهائي أو التحدي. | OOF coverage, threshold report, decision card |
| T5 | Apply the teaching policy exactly as documented: simulated decision loss `10 × FN + 1 × FP` and review capacity not exceeding 12% in each validation period, unless the instructor assigns a documented profile. | طبّق السياسة التعليمية كما هي موثقة: تكلفة القرار التعليمية `10 × FN + 1 × FP` وسعة مراجعة لا تتجاوز 12% في كل فترة تحقق، ما لم تخصص المدربة ملف سياسة موثقًا. | threshold metrics, period-capacity audit |
| T6 | Interpret model dependence with the correct units and limits. SHAP explains the fitted model; it does not prove causality, fairness or legal compliance. | فسّر اعتماد النموذج بالوحدات والحدود الصحيحة. يشرح SHAP النموذج المدرّب، ولا يثبت السببية أو العدالة أو الامتثال النظامي. | interpretability report, SHAP provenance |
| T7 | Learn calibration on calibration rows only, freeze it before policy/evaluation use, and report Brier score, ECE and reliability evidence rather than assuming improvement. | تعلّم المعايرة من صفوف المعايرة فقط، وثبّتها قبل استخدامها في السياسة أو التقييم، واعرض Brier وECE وأدلة الموثوقية بدل افتراض التحسن. | calibration comparison, reliability curve |
| T8 | Ship an ensemble only when the documented Worth-It Gate supports it. `KEEP_SINGLE_MODEL` is a valid engineering decision when the ensemble does not add stable value. | لا تعتمد التجميع إلا عندما تدعمه بوابة الجدوى الموثقة. ويُعد `KEEP_SINGLE_MODEL` قرارًا هندسيًا صحيحًا عندما لا يضيف التجميع قيمة مستقرة. | ensemble decision, stability evidence |
| T9 | The final inference interface must accept new feature rows and return `application_id` and a probability. The frozen batch policy is applied after probability generation. | يجب أن تستقبل واجهة الاستدلال النهائية صفوف خصائص جديدة وتعيد `application_id` واحتمالًا. تُطبّق سياسة الدفعة المجمدة بعد توليد الاحتمالات. | runnable inference command, `submission.csv` |
| T10 | Outputs must be reproducible from source. Record seeds, package versions, hashes, parameters, provenance and the exact repository commit. | يجب أن تكون المخرجات قابلة لإعادة البناء من المصدر. سجّل البذور والإصدارات والبصمات والمعاملات ومصدر التنفيذ وCommit المستودع الدقيق. | manifest, provenance, exact SHA, final tag |
| T11 | Recovery and example outputs are learning aids only. They must be disclosed and cannot be submitted as personal execution evidence in assessment mode. | مخرجات الاستعادة والأمثلة وسائل تعلم فقط. يجب الإفصاح عنها، ولا يجوز تسليمها بوصفها دليل تنفيذ شخصي في وضع التقييم. | recovery disclosure, assessment-mode checks |
| T12 | Do not fabricate metrics, screenshots, outputs, commits or timestamps. Do not hard-code challenge predictions or copy another learner’s evidence. | لا تنشئ مقاييس أو صورًا أو مخرجات أو Commits أو أوقاتًا مصطنعة. لا تثبّت تنبؤات التحدي يدويًا ولا تنسخ أدلة متدرب آخر. | clean rerun, hidden evaluator, oral defence |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Minimum technical acceptance

A project is technically ready only when all of the following are true:

1. Notebooks `00` and `01–05` run from a clean environment.
2. Notebook `99` reports the required files and hashes without a blocking error.
3. The executable inference interface reproduces the submitted probabilities from the recorded commit.
4. Required artifacts, reports and provenance files exist and are internally consistent.
5. No known leakage feature, challenge label, secret or personal data is present.
6. The exact tag and commit SHA identify the assessed version.

A green automated check supports review; it is not a grade, authenticity decision or submission receipt.

</td>
<td width="50%" valign="top" dir="rtl">

## الحد الأدنى للقبول التقني

يُعد المشروع جاهزًا تقنيًا فقط عند تحقق جميع ما يأتي:

1. تعمل دفاتر `00` و`01–05` من بيئة نظيفة.
2. يعرض دفتر `99` الملفات والبصمات المطلوبة من دون خطأ مانع.
3. تعيد واجهة الاستدلال التنفيذية إنتاج الاحتمالات المسلّمة من Commit المسجل.
4. توجد الأدلة والتقارير وملفات مصدر التنفيذ المطلوبة وتتسق داخليًا.
5. لا توجد خاصية تسرب معروفة أو تسميات تحدٍ أو أسرار أو بيانات شخصية.
6. يحدد Tag وCommit SHA الدقيقان النسخة التي ستُقيّم.

يدعم الفحص الآلي الأخضر عملية المراجعة، لكنه ليس درجة أو حكمًا بالأصالة أو إيصال استلام.

</td>
</tr>
</table>
