# Course Glossary | قاموس الدورة

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

The English definition appears on the left; the professional Arabic equivalent and explanation appear on the right.  
يظهر التعريف الإنجليزي في اليسار، ويظهر المقابل العربي المهني وشرحه في اليمين.

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Baseline

A simple reference model or policy used to judge whether later complexity adds measurable value.

</td>
<td width="50%" valign="top" dir="rtl">

## خط الأساس — Baseline

نموذج أو سياسة مرجعية بسيطة يُقاس عليها ما إذا كان التعقيد اللاحق يضيف قيمة قابلة للقياس.

</td>
</tr>
<tr><td valign="top" dir="ltr">

## Boosting

Sequentially adding learners so that later learners focus on errors left by earlier ones.

</td><td valign="top" dir="rtl">

## التعزيز — Boosting

إضافة متعلمين بالتتابع بحيث يركز اللاحق منها على الأخطاء التي تركها السابق.

</td></tr>
<tr><td valign="top" dir="ltr">

## Early stopping

Stopping iterative training when validation performance no longer improves, then retaining the best observed iteration.

</td><td valign="top" dir="rtl">

## الإيقاف المبكر — Early stopping

إيقاف التدريب التكراري عندما يتوقف أداء التحقق عن التحسن، مع الاحتفاظ بأفضل تكرار تم رصده.

</td></tr>
<tr><td valign="top" dir="ltr">

## Data leakage

Using information during model development that would not be available at the real decision time.

</td><td valign="top" dir="rtl">

## تسرب البيانات — Data leakage

استخدام معلومات أثناء تطوير النموذج لم تكن ستكون متاحة عند لحظة القرار الفعلية.

</td></tr>
<tr><td valign="top" dir="ltr">

## Temporal leakage

Allowing information from the future, or from an outcome that has not yet matured, to influence training or validation.

</td><td valign="top" dir="rtl">

## التسرب الزمني — Temporal leakage

السماح لمعلومات مستقبلية أو لنتيجة لم يكتمل رصدها بعد بالتأثير في التدريب أو التحقق.

</td></tr>
<tr><td valign="top" dir="ltr">

## Group leakage

Placing related records, such as repeated applications from the same customer, on both sides of a validation boundary.

</td><td valign="top" dir="rtl">

## تسرب المجموعات — Group leakage

وضع سجلات مترابطة، مثل طلبات العميل المتكررة، في جانبي حد التحقق نفسه.

</td></tr>
<tr><td valign="top" dir="ltr">

## Out-of-fold prediction (OOF)

A prediction for a row produced by a model that was not trained on that row.

</td><td valign="top" dir="rtl">

## تنبؤ خارج الطية — OOF

تنبؤ لسجل ينتجه نموذج لم يتدرب على ذلك السجل.

</td></tr>
<tr><td valign="top" dir="ltr">

## Class imbalance

A classification setting in which one class appears much less frequently than the other.

</td><td valign="top" dir="rtl">

## عدم توازن الفئات — Class imbalance

حالة تصنيف تظهر فيها إحدى الفئات بنسبة أقل بكثير من الفئة الأخرى.

</td></tr>
<tr><td valign="top" dir="ltr">

## ROC-AUC

A threshold-independent measure of how well the model ranks positive cases above negative cases.

</td><td valign="top" dir="rtl">

## المساحة تحت منحنى ROC — ROC-AUC

مقياس مستقل عن عتبة محددة يوضح قدرة النموذج على ترتيب الحالات الإيجابية أعلى من الحالات السلبية.

</td></tr>
<tr><td valign="top" dir="ltr">

## Average Precision (AP)

A summary of precision–recall performance that is especially useful for imbalanced classification.

</td><td valign="top" dir="rtl">

## متوسط الدقة — Average Precision

مقياس يلخص أداء الدقة والاستدعاء ويكون مفيدًا بصورة خاصة في مسائل التصنيف غير المتوازن.

</td></tr>
<tr><td valign="top" dir="ltr">

## False negative (FN)

A positive case that the model fails to flag.

</td><td valign="top" dir="rtl">

## سلبية كاذبة — False negative

حالة إيجابية لا يرفع النموذج لها إشارة.

</td></tr>
<tr><td valign="top" dir="ltr">

## False positive (FP)

A negative case that the model incorrectly flags.

</td><td valign="top" dir="rtl">

## إيجابية كاذبة — False positive

حالة سلبية يرفع النموذج لها إشارة بصورة غير صحيحة.

</td></tr>
<tr><td valign="top" dir="ltr">

## Decision threshold

The cutoff that converts a probability or score into a decision flag.

</td><td valign="top" dir="rtl">

## عتبة القرار — Decision threshold

الحد الذي يحول الاحتمال أو الدرجة إلى إشارة قرار.

</td></tr>
<tr><td valign="top" dir="ltr">

## Simulated decision cost

A learning metric that assigns explicit units to different error types. It is not a real financial loss or a grade deduction.

</td><td valign="top" dir="rtl">

## تكلفة القرار التعليمية — Simulated decision cost

مقياس تعليمي يمنح أنواع الأخطاء أوزانًا صريحة، ولا يمثل خسارة مالية فعلية أو خصمًا من الدرجة.

</td></tr>
<tr><td valign="top" dir="ltr">

## Review capacity

The maximum number or proportion of cases that an operational team can examine.

</td><td valign="top" dir="rtl">

## سعة المراجعة — Review capacity

العدد أو النسبة القصوى من الحالات التي يستطيع فريق التشغيل مراجعتها.

</td></tr>
<tr><td valign="top" dir="ltr">

## Optuna

A hyperparameter-optimization framework that proposes trials, evaluates them and can prune unpromising trials.

</td><td valign="top" dir="rtl">

## Optuna لتحسين المعاملات

إطار لتحسين المعاملات الفائقة يقترح التجارب ويقيمها، ويمكنه إيقاف التجارب غير الواعدة مبكرًا.

</td></tr>
<tr><td valign="top" dir="ltr">

## Permutation importance

The performance decrease observed when a feature or feature group is shuffled.

</td><td valign="top" dir="rtl">

## أهمية التبديل — Permutation importance

مقدار انخفاض الأداء عند تبديل قيم خاصية أو مجموعة خصائص.

</td></tr>
<tr><td valign="top" dir="ltr">

## SHAP

Additive feature contributions that explain a model output in a defined output space. They do not prove causality.

</td><td valign="top" dir="rtl">

## قيم SHAP لإسهام الخصائص

إسهامات جمعيّة للخصائص تفسر خرج النموذج ضمن وحدة محددة، ولا تثبت السببية.

</td></tr>
<tr><td valign="top" dir="ltr">

## Global explanation

An explanation of the patterns and features the model relies on across many records.

</td><td valign="top" dir="rtl">

## التفسير العام — Global explanation

تفسير للأنماط والخصائص التي يعتمد عليها النموذج عبر مجموعة كبيرة من السجلات.

</td></tr>
<tr><td valign="top" dir="ltr">

## Local explanation

An explanation of the main feature contributions behind one prediction.

</td><td valign="top" dir="rtl">

## التفسير المحلي — Local explanation

تفسير لأهم إسهامات الخصائص التي تقف خلف تنبؤ واحد.

</td></tr>
<tr><td valign="top" dir="ltr">

## Probability calibration

The agreement between predicted probabilities and observed outcome frequencies.

</td><td valign="top" dir="rtl">

## معايرة الاحتمال — Probability calibration

مدى توافق الاحتمالات المتوقعة مع التكرارات الفعلية للنتائج.

</td></tr>
<tr><td valign="top" dir="ltr">

## Reliability diagram

A plot comparing average predicted probabilities with observed frequencies across probability bins.

</td><td valign="top" dir="rtl">

## مخطط الموثوقية — Reliability diagram

رسم يقارن متوسط الاحتمالات المتوقعة بالتكرارات المرصودة عبر حاويات احتمالية.

</td></tr>
<tr><td valign="top" dir="ltr">

## Brier score

The mean squared difference between predicted probabilities and binary outcomes; lower values are better.

</td><td valign="top" dir="rtl">

## درجة براير — Brier score

متوسط مربع الفرق بين الاحتمالات المتوقعة والنتائج الثنائية؛ تكون القيمة الأقل أفضل.

</td></tr>
<tr><td valign="top" dir="ltr">

## Expected Calibration Error (ECE)

A weighted summary of the gaps between confidence and observed frequency across probability bins.

</td><td valign="top" dir="rtl">

## خطأ المعايرة المتوقع — ECE

ملخص موزون للفجوات بين الثقة المتوقعة والتكرار المرصود عبر الحاويات الاحتمالية.

</td></tr>
<tr><td valign="top" dir="ltr">

## Ensemble

A method that combines predictions from multiple models. Its added value must be demonstrated.

</td><td valign="top" dir="rtl">

## تجميع النماذج — Ensemble

أسلوب يجمع تنبؤات عدة نماذج، ويجب إثبات القيمة الإضافية الناتجة عنه.

</td></tr>
<tr><td valign="top" dir="ltr">

## Stacking

Training a meta-model on out-of-fold predictions from base models.

</td><td valign="top" dir="rtl">

## التكديس — Stacking

تدريب نموذج جامع على تنبؤات خارج الطية ناتجة من النماذج الأساسية.

</td></tr>
<tr><td valign="top" dir="ltr">

## Worth-it gate

A documented rule that accepts extra model complexity only when improvement exceeds validation noise and operational cost.

</td><td valign="top" dir="rtl">

## بوابة الجدوى — Worth-it gate

قاعدة موثقة لا تقبل تعقيدًا إضافيًا إلا عندما يتجاوز التحسن ضوضاء التحقق والتكلفة التشغيلية.

</td></tr>
<tr><td valign="top" dir="ltr">

## Inference

Applying a trained model to new feature rows to produce probabilities or scores.

</td><td valign="top" dir="rtl">

## الاستدلال — Inference

تطبيق نموذج مدرب على سجلات خصائص جديدة لإنتاج احتمالات أو درجات.

</td></tr>
<tr><td valign="top" dir="ltr">

## Reproducibility

The ability to regenerate results from specified data, code, versions, seeds and configuration.

</td><td valign="top" dir="rtl">

## قابلية إعادة الإنتاج — Reproducibility

القدرة على إعادة توليد النتائج من بيانات وكود وإصدارات وبذور وإعدادات محددة.

</td></tr>
<tr><td valign="top" dir="ltr">

## Model Card

Structured documentation of intended use, data, validation, performance, limitations and monitoring needs.

</td><td valign="top" dir="rtl">

## بطاقة النموذج — Model Card

توثيق منظم للاستخدام المقصود والبيانات والتحقق والأداء والقيود واحتياجات المراقبة.

</td></tr>
<tr><td valign="top" dir="ltr">

## Commit SHA

The unique identifier of an exact Git commit used to freeze and retrieve the submitted project version.

</td><td valign="top" dir="rtl">

## بصمة Commit — Commit SHA

المعرف الفريد لنسخة Git دقيقة يُستخدم لتجميد إصدار المشروع المقدم واسترجاعه.

</td></tr>
</table>
