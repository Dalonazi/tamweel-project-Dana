# Day 2 Guide | دليل اليوم الثاني

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<div align="center">

**SDA-DSC-211 · Tamweel Lite · Honest Validation and Bounded Search | التحقق الصادق والبحث المحدود**

[Open Day 2 in Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/02_validation_tuning.ipynb) · [View notebook](notebooks/02_validation_tuning.ipynb) · [Feature dictionary](data/feature_dictionary.csv)

</div>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## What you will build

In 60 minutes, replace the Day 1 random teaching split with a controlled validation design that addresses five risks:

1. Post-outcome feature leakage.
2. Preprocessing leakage.
3. Time leakage.
4. Customer overlap.
5. Duplicate-event leakage.

You will reserve a separate historical customer cohort for bounded Optuna search, freeze the selected parameters, then evaluate later mature-label periods with zero shared customers inside each training–validation fold.

**Required outcome:** a technically complete run plus your own interpretation of leakage, split design, observed metric gaps, preprocessing discipline and limitations.

All data is synthetic. The lab supports learning and portfolio evidence only; it must not drive real financing decisions.

</td>
<td width="50%" valign="top" dir="rtl">

## ماذا ستبني؟

خلال 60 دقيقة، استبدل التقسيم العشوائي التعليمي في اليوم الأول بتصميم تحقق محكوم يعالج خمسة مخاطر:

1. تسرب خصائص ما بعد النتيجة.
2. تسرب المعالجة المسبقة.
3. تسرب الزمن.
4. تداخل العملاء.
5. تسرب الأحداث المكررة.

ستحجز مجموعة تاريخية منفصلة من العملاء لبحث Optuna محدود، ثم تجمّد الإعدادات المختارة وتقيّم فترات لاحقة ناضجة الأهداف مع عدم وجود عملاء مشتركين داخل كل طية تدريب وتحقق.

**المخرج المطلوب:** تشغيل مكتمل تقنيًا، وتفسيرك الخاص للتسرب وتصميم التقسيم والفجوات المرصودة وانضباط المعالجة والقيود.

جميع البيانات اصطناعية. يخدم اللاب التعلم وأدلة الملف المهني فقط، ولا يجوز أن يقود قرارات تمويل فعلية.

</td>
</tr>
</table>

## Lab journey | رحلة اللاب

| Minutes | English task | المهمة بالعربية |
|---:|---|---|
| 0–8 | Prepare a fresh free-CPU environment and inspect the data contract | جهّز بيئة CPU مجانية جديدة وافحص عقد البيانات |
| 8–18 | Audit feature availability and duplicate events | دقّق إتاحة الخصائص والأحداث المكررة |
| 18–30 | Inspect time, customer and 90-day maturity boundaries | افحص حدود الزمن والعملاء ونضج الهدف لمدة 90 يومًا |
| 30–45 | Run the bounded search on the reserved historical cohort | نفّذ البحث المحدود على المجموعة التاريخية المحجوزة |
| 45–53 | Compare fold means, sample variation and OOF coverage | قارن متوسطات الطيات والتشتت العيّني وتغطية OOF |
| 53–60 | Write your interpretation and export evidence | اكتب تفسيرك وصدّر الأدلة |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Start from a controlled session

1. Open the notebook and select the free **CPU** runtime.
2. Choose **Runtime → Run all**. No previous notebook is required.
3. Do not mount Drive and do not add API keys.
4. Use `FAST_MODE=True` first: two CPU threads and a ceiling of 200 trees.
5. `FULL_MODE=True` is optional and raises the ceiling to 600 trees.
6. Both modes retain at most eight sequential Optuna trials, three internal search folds and a 120-second cooperative search budget.
7. If setup requests a restart, choose **Restart session** and run from the beginning.

The setup verifies pinned versions, the data manifest and SHA-256 hashes. A checksum or imported-version failure must not be bypassed.

</td>
<td width="50%" valign="top" dir="rtl">

## ابدأ من جلسة محكومة

1. افتح الدفتر واختر بيئة **CPU** المجانية.
2. اختر **Runtime → Run all**. لا يلزم تشغيل أي دفتر سابق.
3. لا تربط Drive ولا تضف مفاتيح API.
4. استخدم أولًا `FAST_MODE=True`: خيطا CPU وسقف 200 شجرة.
5. الإعداد `FULL_MODE=True` اختياري ويرفع السقف إلى 600 شجرة.
6. يحتفظ الوضعان بحد أقصى قدره ثماني تجارب Optuna متتابعة وثلاث طيات داخلية وميزانية بحث تعاونية قدرها 120 ثانية.
7. إذا طلب الإعداد إعادة التشغيل، اختر **Restart session** ثم شغّل من البداية.

يتحقق الإعداد من الإصدارات المثبتة وبيان البيانات وبصمات SHA-256. لا تتجاوز فشل البصمة أو اختلاف إصدار مستورد.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Audit information availability

The target `default_within_90d` means a default event occurs within 90 days after the application. It does not mean an account reaches exactly 90 days past due.

Read the feature dictionary's `available_at` field. A predictor is eligible only when its value exists at application time. Correlation strength by itself is not a leakage test.

| Risk | Required guard |
|---|---|
| Target leakage | Remove fields that describe the later outcome |
| Preprocessing leakage | Fit imputation on training rows only |
| Time leakage | Train only on applications whose labels matured before validation starts |
| Customer leakage | Remove validation customers from the corresponding training fold |
| Duplicate leakage | Deduplicate identical events and reject conflicting copies |

The notebook reads the dirty training copy to demonstrate the audit. Challenge data may be downloaded for package-integrity checks, but it is not used in today's model selection, fitting or comparison.

</td>
<td width="50%" valign="top" dir="rtl">

## دقّق إتاحة المعلومات

يعني الهدف `default_within_90d` وقوع حدث تعثر خلال 90 يومًا بعد تقديم الطلب. ولا يعني وصول الحساب إلى 90 يوم تأخر بالضبط.

اقرأ حقل `available_at` في قاموس الخصائص. لا تُقبل الخاصية إلا إذا كانت قيمتها موجودة وقت تقديم الطلب. قوة الارتباط وحدها ليست اختبارًا للتسرب.

| الخطر | الحارس المطلوب |
|---|---|
| تسرب الهدف | حذف الحقول التي تصف النتيجة اللاحقة |
| تسرب المعالجة | تعلم التعويض من صفوف التدريب فقط |
| تسرب الزمن | التدريب على الطلبات التي نضجت أهدافها قبل بدء التحقق |
| تسرب العميل | حذف عملاء التحقق من تدريب الطية المقابلة |
| تسرب التكرار | حذف الأحداث المتطابقة ورفض النسخ المتعارضة |

يقرأ الدفتر نسخة التدريب المتسربة لشرح التدقيق. قد تُنزّل بيانات التحدي للتحقق من سلامة الحزمة، لكنها لا تدخل اختيار نموذج اليوم أو تدريبه أو مقارنته.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Understand the forward folds

For every outer fold, a training application is eligible only when:

**application date + 90 days < validation start**

The strict inequality intentionally excludes a label that matures exactly on the validation boundary. Every customer appearing in a validation window is removed from that fold's training rows.

| Validation window | Mature, customer-purged training rows | Validation rows | Shared customers inside fold |
|---|---:|---:|---:|
| Jul–Dec 2023 | 3,223 | 1,632 | 0 |
| Jan–Jun 2024 | 4,460 | 1,674 | 0 |
| Jul–Dec 2024 | 5,731 | 1,733 | 0 |

These are the released-data counts under the pinned seed and contract. A customer may appear in more than one validation period; the guarantee is zero overlap between training and validation within the same fold.

Earlier records form a warm-up period. They must not receive fitted-training predictions and be relabeled as OOF evidence.

</td>
<td width="50%" valign="top" dir="rtl">

## افهم الطيات الزمنية

لا يُقبل طلب في تدريب أي طية إلا عندما يحقق الشرط الآتي:

**تاريخ الطلب + 90 يومًا < بداية التحقق**

تستبعد المتباينة الصارمة عمدًا الهدف الذي ينضج في يوم حد التحقق نفسه. ويُحذف من تدريب كل طية كل عميل يظهر في فترة تحققها.

| فترة التحقق | صفوف تدريب ناضجة ومستبعدة العملاء | صفوف التحقق | العملاء المشتركون داخل الطية |
|---|---:|---:|---:|
| يوليو–ديسمبر 2023 | 3,223 | 1,632 | 0 |
| يناير–يونيو 2024 | 4,460 | 1,674 | 0 |
| يوليو–ديسمبر 2024 | 5,731 | 1,733 | 0 |

هذه أعداد البيانات المنشورة وفق البذرة والعقد المثبتين. قد يظهر العميل في أكثر من فترة تحقق؛ والضمان هو عدم التداخل بين التدريب والتحقق داخل الطية نفسها.

تشكّل السجلات المبكرة فترة تمهيد. لا تمنحها تنبؤات تدريب ثم تعيد تسميتها بوصفها أدلة OOF.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Separate search from evaluation

The notebook reserves 1,935 mature historical applications before the first outer-validation period, excluding every customer used in any of the three outer-validation windows.

Search uses three internal forward folds. Inside each fold:

1. Inner-fit rows learn imputation and trees.
2. Inner-stop rows select the tree count using log loss.
3. The model is refit on the complete fold-training rows after the tree count is fixed.

Outer-validation rows never select imputation, tree count or hyperparameters. The reserved cohort is small, and some internal partitions contain few positive examples; record this as an instability risk.

The best search AP is a model-selection result. It is not an estimate of future outer performance.

</td>
<td width="50%" valign="top" dir="rtl">

## افصل البحث عن التقييم

يحجز الدفتر 1,935 طلبًا تاريخيًا ناضجًا قبل أول فترة تحقق خارجي، مع استبعاد كل عميل مستخدم في أي فترة من فترات التحقق الخارجي الثلاث.

يستخدم البحث ثلاث طيات زمنية داخلية. داخل كل طية:

1. تتعلم صفوف inner fit التعويض والأشجار.
2. تختار صفوف inner stop عدد الأشجار باستخدام log loss.
3. يُعاد تدريب النموذج على صفوف تدريب الطية كاملة بعد تثبيت عدد الأشجار.

لا تختار صفوف التحقق الخارجي التعويض أو عدد الأشجار أو معاملات البحث. المجموعة المحجوزة صغيرة، وبعض أجزائها الداخلية يحتوي أمثلة موجبة قليلة؛ سجّل ذلك بوصفه خطرًا على استقرار الاختيار.

أفضل AP داخل البحث نتيجة لاختيار النموذج، وليس تقديرًا للأداء الخارجي المستقبلي.

</td>
</tr>
</table>

## Bounded-search contract | عقد البحث المحدود

| Limit | Value | الحد | القيمة |
|---|---:|---|---:|
| Seed | 211 | البذرة | 211 |
| Optuna attempts | At most 8 sequential trials | محاولات Optuna | حتى 8 تجارب متتابعة |
| Internal validation | 3 forward customer-separated folds | التحقق الداخلي | 3 طيات زمنية تفصل العملاء |
| Search budget | 120 seconds; cooperative stop can finish slightly later | ميزانية البحث | 120 ثانية؛ قد ينتهي الإيقاف التعاوني بعد الحد بقليل |
| CPU threads | 2 | خيوط CPU | 2 |
| Tree ceiling | 200 in FAST; 600 in optional FULL | سقف الأشجار | 200 في FAST و600 في FULL الاختياري |
| Early stopping | 20 rounds without inner log-loss improvement | الإيقاف المبكر | 20 جولة دون تحسن في log loss الداخلي |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Read search states correctly

- `COMPLETE`: all three internal fold scores were calculated.
- `PRUNED`: the trial stopped early.
- `FAIL`: the attempt did not produce a complete objective; partial fold values are not a completed mean.
- `TUNING_REQUIRED`: no live trial completed and the lab must be rerun.

If no trial completes, a stored `EDUCATIONAL_EXAMPLE` appears for discussion only. It is not copied into live results, does not select parameters for you and must never replace your own completed search.

The time budget covers the search itself, not setup, plotting or later comparisons. Resource limits are not a reason to purchase a subscription.

</td>
<td width="50%" valign="top" dir="rtl">

## اقرأ حالات البحث بصورة صحيحة

- `COMPLETE`: اكتملت درجات الطيات الداخلية الثلاث.
- `PRUNED`: أوقفت التجربة مبكرًا.
- `FAIL`: لم تنتج المحاولة هدفًا مكتملًا؛ ولا تصبح القيم الجزئية متوسطًا مكتملًا.
- `TUNING_REQUIRED`: لم تكتمل تجربة فعلية ويلزم إعادة تشغيل اللاب.

إذا لم تكتمل أي تجربة، يظهر `EDUCATIONAL_EXAMPLE` محفوظ للنقاش فقط. لا يُنسخ إلى النتائج الفعلية، ولا يختار الإعدادات نيابة عنك، ولا يجوز أن يستبدل بحثك المكتمل.

تغطي الميزانية زمن البحث نفسه، ولا تشمل الإعداد أو الرسم أو المقارنات اللاحقة. حدود الموارد ليست سببًا لشراء اشتراك.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Interpret the four protocols

| Protocol | Interpretation |
|---|---|
| Leaky random control | Deliberately uses two post-outcome fields and all-row imputation; unsafe negative control |
| Clean random control | Uses eligible fields and training-only imputation, but still mixes time and customers; unsafe for decisions |
| Honest fixed | Forward mature-label, customer-purged folds with base parameters and 80 trees |
| Honest reserved search | The same honest outer folds with parameters frozen on the separate search cohort and internal tree selection |

The random protocols cover 10,000 applications. The time-based protocols cover 5,039 later eligible applications and have different training sizes. The gaps combine changes in period, population and available information; they are descriptive, not isolated causal estimates of leakage.

No model or tuned protocol is required to win. Cleaning leakage can lower, preserve or occasionally raise a metric, and bounded search does not guarantee improvement.

</td>
<td width="50%" valign="top" dir="rtl">

## فسّر البروتوكولات الأربعة

| البروتوكول | التفسير |
|---|---|
| Leaky random control | يستخدم عمدًا خاصيتين بعد النتيجة وتعويضًا من كامل البيانات؛ ضابط سلبي غير آمن |
| Clean random control | يستخدم الخصائص المؤهلة وتعويض التدريب فقط، لكنه يخلط الزمن والعملاء؛ غير صالح للقرار |
| Honest fixed | طيات زمنية ناضجة الأهداف ومستبعدة العملاء مع الإعداد الأساسي و80 شجرة |
| Honest reserved search | الطيات الخارجية الصادقة نفسها مع معاملات مجمدة من مجموعة البحث واختيار داخلي للأشجار |

تغطي البروتوكولات العشوائية 10,000 طلب. وتغطي البروتوكولات الزمنية 5,039 طلبًا لاحقًا مؤهلًا وبأحجام تدريب مختلفة. تجمع الفروق تغيرات الفترة والسكان والمعلومات المتاحة؛ فهي وصفية وليست تقديرًا سببيًا مستقلًا للتسرب.

لا يُشترط أن يفوز نموذج أو بروتوكول مضبوط. قد يخفض تنظيف التسرب المقياس أو يحافظ عليه أو يرفعه أحيانًا، ولا يضمن البحث المحدود التحسن.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Read mean, variation and coverage together

The headline score is the unweighted mean across three folds. Error bars show sample standard deviation with `ddof=1`.

- The folds are related time periods, not independent experiments.
- The error bar is not a confidence interval or significance test.
- AP means **Average Precision**, not trapezoidal area under the precision–recall curve.
- Read validation size and positive prevalence beside the metric.
- Do not rerun search because an outer score is disappointing. Repeated selection on outer folds converts them into development data.

Each successful honest protocol produces 5,039 OOF probabilities. The remaining 4,961 applications are warm-up rows without OOF predictions. Coverage is 50.39% of all clean training rows and 100% of requests eligible from 2023-07-01 onward.

Do not fill warm-up rows with training predictions or artificial probabilities. OOF evidence is not a final independent test and does not guarantee fairness or calibration.

</td>
<td width="50%" valign="top" dir="rtl">

## اقرأ المتوسط والتشتت والتغطية معًا

الدرجة الرئيسية هي المتوسط غير الموزون للطيات الثلاث. وتمثل أشرطة الخطأ الانحراف المعياري العيّني باستخدام `ddof=1`.

- الطيات فترات زمنية مترابطة وليست تجارب مستقلة.
- شريط الخطأ ليس فترة ثقة ولا اختبار دلالة.
- يعني AP **Average Precision** وليس المساحة شبه المنحرفة تحت منحنى precision–recall.
- اقرأ حجم التحقق ونسبة الفئة الموجبة بجانب المقياس.
- لا تُعد البحث لأن رقمًا خارجيًا لم يعجبك؛ فالاختيار المتكرر على الطيات الخارجية يحولها إلى بيانات تطوير.

ينتج كل بروتوكول صادق ناجح 5,039 احتمال OOF. وتبقى الطلبات البالغ عددها 4,961 صفوف تمهيد بلا تنبؤات OOF. تبلغ التغطية 50.39% من جميع صفوف التدريب النظيفة و100% من الطلبات المؤهلة بدءًا من 2023-07-01.

لا تملأ صفوف التمهيد بتنبؤات التدريب أو احتمالات مصطنعة. أدلة OOF ليست اختبارًا نهائيًا مستقلًا ولا تضمن العدالة أو المعايرة.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Write your own interpretation

Complete the five response fields using evidence from your run:

1. Name one leaked field and explain why it was unavailable at application time.
2. Justify time ordering, customer separation and the strict 90-day maturity rule.
3. Cite two numerical gaps from the validation table and explain why they do not prove universal superiority.
4. Explain why imputation is learned inside training and what the inner stopping set controls.
5. State one search-budget limitation and one OOF-coverage or fold-dependence limitation.

The automated checkpoint detects missing fields only. It does not write answers, judge correctness, award a grade or prove authorship. Do not copy another learner's table or interpretation.

</td>
<td width="50%" valign="top" dir="rtl">

## اكتب تفسيرك أنت

أكمل حقول الإجابة الخمسة باستخدام أدلة تشغيلك:

1. اذكر خاصية متسربة واشرح لماذا لم تكن متاحة وقت تقديم الطلب.
2. برر ترتيب الزمن وفصل العملاء وقاعدة نضج الهدف الصارمة لمدة 90 يومًا.
3. استشهد بفجوتين رقميتين من جدول التحقق واشرح لماذا لا تثبتان تفوقًا عامًا.
4. اشرح لماذا يُتعلم التعويض داخل التدريب وما الذي يتحكم فيه جزء الإيقاف الداخلي.
5. اذكر قيدًا في ميزانية البحث وقيدًا في تغطية OOF أو اعتماد الطيات.

يكتشف الفحص الآلي الخانات الفارغة فقط. لا يكتب الإجابات، ولا يحكم على صحتها، ولا يمنح درجة، ولا يثبت الملكية. لا تنسخ جدول متدرب آخر أو تفسيره.

</td>
</tr>
</table>

## Required evidence | الأدلة المطلوبة

Save the executed notebook as `notebooks/02_validation_tuning.ipynb`. Extract `day2_artifacts.zip` and upload these 15 files to `artifacts/`:

| File | Evidence purpose | فائدة الدليل |
|---|---|---|
| `environment.json` | Environment versions and verified sources | إصدارات البيئة والمصادر المتحقق منها |
| `validation_report.csv` | Fold-level metrics, sizes and protocol details | مقاييس كل طية وأحجامها وتفاصيل البروتوكول |
| `validation_summary.csv` | Fold means and sample standard deviations | متوسطات الطيات والانحرافات المعيارية العيّنية |
| `optuna_results.csv` | Trial states, values, parameters and durations | حالات التجارب وقيمها ومعاملاتها وأزمنتها |
| `best_params.json` | Live search result and frozen parameters | نتيجة البحث الفعلي والإعدادات المجمدة |
| `leakage_audit.csv` | Availability-based feature decisions | قرارات الخصائص المبنية على زمن الإتاحة |
| `fold_audit.csv` | Time, maturity and customer-separation evidence | أدلة الزمن ونضج الهدف وفصل العملاء |
| `day2_oof_predictions.csv` | Honest out-of-fold probabilities by protocol | احتمالات OOF الصادقة حسب البروتوكول |
| `day2_oof_coverage.csv` | Role and fold assigned to every clean application | دور وطية كل طلب نظيف |
| `day2_provenance.json` | Training, validation and inner-stop membership | عضوية التدريب والتحقق والإيقاف الداخلي |
| `day2_reflection.json` | Your five responses and completion checkpoint | إجاباتك الخمس وحارس الإكمال |
| `day2_run.json` | Configuration, hashes, status and coverage | الإعدادات والبصمات والحالة والتغطية |
| `day2_fold_sizes.png` | Fold-size and validation-window evidence | دليل أحجام الطيات وفترات التحقق |
| `day2_search.png` | Completed live-search trajectory | مسار البحث الفعلي المكتمل |
| `day2_validation_comparison.png` | ROC-AUC and AP comparison with sample variation | مقارنة ROC-AUC وAP مع التشتت العيّني |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Readiness states and completion gate

- `TECHNICAL_READY`: execution and at least one live tuning trial completed.
- `TUNING_REQUIRED`: no live trial completed; rerun is required.
- `LEARNER_WORK_REQUIRED`: technical evidence exists, but learner-owned fields remain incomplete.
- `READY_FOR_REVIEW`: required fields are present. This is not a grade or correctness guarantee.

Before moving on, confirm that you can:

- Identify the removed post-outcome fields and their availability time.
- Point to zero shared customers and mature-label evidence in every fold.
- Distinguish attempted, completed, pruned and failed search trials.
- Explain why fold standard deviation is descriptive rather than a confidence interval.
- State OOF coverage and the warm-up limitation.
- Save the executed notebook and the extracted artifact files outside the temporary Colab session.

</td>
<td width="50%" valign="top" dir="rtl">

## حالات الجاهزية وبوابة الإكمال

- `TECHNICAL_READY`: نجح التنفيذ واكتملت تجربة ضبط فعلية واحدة على الأقل.
- `TUNING_REQUIRED`: لم تكتمل تجربة فعلية؛ يلزم إعادة التشغيل.
- `LEARNER_WORK_REQUIRED`: توجد الأدلة التقنية، لكن حقول المتدرب ما زالت غير مكتملة.
- `READY_FOR_REVIEW`: الحقول المطلوبة موجودة؛ ولا تمثل درجة أو ضمانًا لصحة التفسير.

قبل الانتقال، تحقق من قدرتك على:

- تحديد خصائص ما بعد النتيجة المحذوفة وزمن إتاحتها.
- الإشارة إلى دليل عدم اشتراك العملاء ونضج الهدف في كل طية.
- التمييز بين محاولات البحث والمكتمل منها والموقوفة والفاشلة.
- شرح لماذا يمثل انحراف الطيات وصفًا للتشتت وليس فترة ثقة.
- ذكر تغطية OOF وقيد فترة التمهيد.
- حفظ الدفتر المنفذ والملفات المستخرجة خارج جلسة Colab المؤقتة.

</td>
</tr>
</table>

## Troubleshooting | حل التعثر

| Symptom | Action | الحالة | الإجراء |
|---|---|---|---|
| Imported-version mismatch | Restart the session, then run all cells from the beginning | اختلاف إصدار مكتبة مستوردة | أعد تشغيل الجلسة ثم شغّل جميع الخلايا من البداية |
| Temporary download failure | Rerun setup; matching local SHA-256 files are accepted | فشل تنزيل مؤقت | أعد خلية الإعداد؛ تُقبل الملفات المحلية المطابقة للبصمة |
| Search budget expires | Preserve completed attempts, inspect the example for discussion only, then rerun later on free CPU | انتهاء ميزانية البحث | احفظ المحاولات المكتملة وراجع المثال للنقاش فقط ثم أعد التشغيل لاحقًا على CPU المجاني |
| Unknown field or conflicting duplicate | Restore the released data and investigate; do not bypass the guard | عمود مجهول أو نسخة متعارضة | استرجع البيانات المنشورة وافحص السبب؛ لا تتجاوز الحارس |
| Local execution | Use Python 3.12 or 3.13 with `requirements-colab.txt` and `constraints.txt`, from the project root | تشغيل محلي | استخدم Python 3.12 أو 3.13 والإصدارات المثبتة من جذر المشروع |

## Technical references | المراجع التقنية

- [scikit-learn cross-validation](https://scikit-learn.org/1.6/modules/cross_validation.html)
- [scikit-learn preprocessing leakage guidance](https://scikit-learn.org/1.6/common_pitfalls.html)
- [LightGBM early stopping](https://lightgbm.readthedocs.io/en/v4.6.0/pythonapi/lightgbm.early_stopping.html)
- [Optuna bounded study execution](https://optuna.readthedocs.io/en/v4.5.0/reference/generated/optuna.study.Study.html)
- [Course rubric | بنود التقييم](RUBRIC.md)
- [GitHub submission guide | دليل الحفظ](GITHUB_GUIDE.md)
