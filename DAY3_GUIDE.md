# Day 3 Guide | دليل اليوم الثالث

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<div align="center">

**SDA-DSC-211 · Tamweel Lite · Cost-Sensitive Decisions | القرارات الحساسة للتكلفة**

[Open Day 3 in Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/03_cost_sensitive_decision.ipynb) · [View notebook](notebooks/03_cost_sensitive_decision.ipynb) · [Decision-card template](reports/DECISION_CARD_TEMPLATE.md)

</div>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## What you will build

In 60 minutes, compare three class-imbalance treatments on the same honest OOF rows, then choose a score threshold under an explicit educational loss policy and a capacity ceiling for every validation period.

You will produce:

- a model-strategy comparison;
- a complete threshold sweep;
- a constrained and unconstrained operating point;
- period-capacity, regional and sensitivity audits;
- `threshold_metrics.json`, figures and provenance;
- `reports/DECISION_CARD.md` with your own interpretation.

A flag represents a **simulated review**, not automatic approval or refusal. The loss values are educational decision units, not Saudi riyals, fees, expected credit loss or grade deductions.

</td>
<td width="50%" valign="top" dir="rtl">

## ماذا ستبني؟

خلال 60 دقيقة، قارن ثلاث طرق لمعالجة عدم توازن الفئات على صفوف OOF الصادقة نفسها، ثم اختر عتبة درجات ضمن سياسة معلنة للخسارة التعليمية وسقف سعة لكل فترة تحقق.

ستنتج:

- مقارنة بين استراتيجيات التدريب؛
- مسحًا كاملًا للعتبات؛
- نقطة تشغيل مقيدة وأخرى غير مقيدة؛
- تدقيق السعة والمناطق والحساسية؛
- ملف `threshold_metrics.json` ورسومًا ومصدرًا للتنفيذ؛
- ملف `reports/DECISION_CARD.md` بتفسيرك أنت.

تعني الإشارة **مراجعة محاكاة**، ولا تعني قبولًا أو رفضًا آليًا. قيم الخسارة وحدات قرار تعليمية، وليست ريالات سعودية أو رسومًا أو خسارة ائتمانية متوقعة أو خصمًا من الدرجة.

</td>
</tr>
</table>

## Lab journey | رحلة اللاب

| Minutes | English task | المهمة بالعربية |
|---:|---|---|
| 0–10 | Freeze the loss and capacity policy | ثبّت سياسة الخسارة والسعة |
| 10–20 | Generate OOF evidence for three strategies | أنشئ أدلة OOF للاستراتيجيات الثلاث |
| 20–35 | Compare ranking and sweep thresholds | قارن الترتيب وامسح العتبات |
| 35–45 | Audit capacity in every period | دقّق السعة في كل فترة |
| 45–50 | Inspect cost sensitivity | افحص حساسية التكلفة |
| 50–55 | Review descriptive regional differences | راجع الفروق الوصفية بين المناطق |
| 55–60 | Write and export the decision card | اكتب بطاقة القرار وصدّرها |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Start from a fresh free-CPU session

1. Select the free **CPU** runtime and choose **Runtime → Run all**.
2. Notebook 02 is not required beforehand; the honest time/customer split is rebuilt from source.
3. Do not mount Drive and do not add API keys.
4. Start with `FAST_MODE=True`: 80 trees per model and two CPU threads.
5. `FULL_MODE=True` raises the optional tree cap to 160; it is not required.
6. If setup reports an imported-version mismatch, restart the session and run from the beginning.

No paid service, GPU or additional oversampling package is required.

</td>
<td width="50%" valign="top" dir="rtl">

## ابدأ من جلسة CPU مجانية جديدة

1. اختر بيئة **CPU** المجانية ثم نفّذ **Runtime → Run all**.
2. لا يلزم تشغيل دفتر 02 مسبقًا؛ يعاد بناء تقسيم الزمن والعملاء الصادق من المصدر.
3. لا تربط Drive ولا تضف مفاتيح API.
4. ابدأ بـ`FAST_MODE=True`: عدد 80 شجرة لكل نموذج وخيطا CPU.
5. يرفع `FULL_MODE=True` سقف الأشجار الاختياري إلى 160، وهو غير إلزامي.
6. إذا ظهر اختلاف في إصدار مكتبة مستوردة، أعد تشغيل الجلسة ثم شغّل من البداية.

لا تحتاج إلى خدمة مدفوعة أو GPU أو مكتبة إضافية لإعادة العينات.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Freeze the educational decision policy

The target is a default event within 90 days after application. Challenge data remain closed.

| Outcome | Teaching meaning | Loss units |
|---|---|---:|
| TP | Flag before a later default event | 0 |
| FN | Later default without a flag | 10 |
| FP | Flag on a non-default case | 1 |
| TN | Non-default case without a flag | 0 |

**Observed educational loss = 10 × FN + 1 × FP.** Review cost and review effectiveness are omitted.

Flags must not exceed **12% of requests in each validation period**, rounded down to a whole request. A pooled percentage is not enough because it can hide overload in one period.

</td>
<td width="50%" valign="top" dir="rtl">

## ثبّت سياسة القرار التعليمية

الهدف هو وقوع حدث تعثر خلال 90 يومًا بعد الطلب. تبقى بيانات التحدي مغلقة.

| النتيجة | معناها التعليمي | وحدات الخسارة |
|---|---|---:|
| TP | إشارة قبل حدث تعثر لاحق | 0 |
| FN | تعثر لاحق بلا إشارة | 10 |
| FP | إشارة لحالة لم تتعثر | 1 |
| TN | حالة سليمة بلا إشارة | 0 |

**الخسارة التعليمية المرصودة = 10 × FN + 1 × FP.** لا تتضمن السياسة تكلفة المراجعة أو فعاليتها.

يجب ألا تتجاوز الإشارات **12% من طلبات كل فترة تحقق**، مع التقريب إلى العدد الصحيح الأدنى. لا تكفي النسبة المجمعة لأنها قد تخفي ازدحام فترة بعينها.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Compare the three training strategies fairly

| Strategy | Change inside the training fold |
|---|---|
| `unweighted` | No row duplication or class weight |
| `weighted` | `scale_pos_weight = negatives / positives` from that fold’s training rows only |
| `oversampled` | Randomly duplicate the minority class inside training until balanced |

All three LightGBM models use the same features, folds, tree budget and seed. Missing-value imputation is learned from original training rows before oversampling. Validation rows are never reweighted or resampled.

Class weighting changes model fitting. The FN/FP policy changes the downstream decision. They are not the same quantity.

Weighting and oversampling can distort calibration. Do not read a raw score of 0.70 as a reliable 70% probability before Day 4.

</td>
<td width="50%" valign="top" dir="rtl">

## قارن استراتيجيات التدريب الثلاث بعدالة

| الاستراتيجية | التغيير داخل طية التدريب |
|---|---|
| `unweighted` | لا نسخ للصفوف ولا وزن للفئة |
| `weighted` | `scale_pos_weight = negatives / positives` من صفوف تدريب الطية فقط |
| `oversampled` | نسخ عشوائي للفئة الأقل داخل التدريب حتى التوازن |

تستخدم نماذج LightGBM الثلاث الخصائص والطيات وميزانية الأشجار والبذرة نفسها. يتعلم تعويض القيم المفقودة من صفوف التدريب الأصلية قبل إعادة العينات. لا يُعاد وزن صفوف التحقق أو أخذ عينات منها.

يغيّر وزن الفئة تدريب النموذج، بينما تغيّر سياسة FN وFP القرار اللاحق؛ وهما ليستا الكمية نفسها.

قد يشوّه الوزن وإعادة العينات المعايرة. لا تفسّر الدرجة الخام 0.70 بوصفها احتمالًا موثوقًا قدره 70% قبل اليوم الرابع.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Understand the evidence source and coverage

Each strategy produces **5,039 honest OOF predictions**, covering 50.39% of the 10,000 training rows and 100% of rows eligible for the forward validation windows. Another 4,961 warm-up rows have no OOF prediction.

Do not fill missing OOF rows with training predictions.

`MODEL_FOR_DECISION="weighted"` is declared before comparison. It is not a claim that weighting must win. Preserve the baseline before trying another strategy; repeated strategy selection on the same OOF labels increases optimism.

The pooled AP reported today is Average Precision over all eligible OOF rows. It is not the mean of Day 2 fold AP values and not trapezoidal PR-AUC.

</td>
<td width="50%" valign="top" dir="rtl">

## افهم مصدر الأدلة وتغطيتها

تنتج كل استراتيجية **5,039 تنبؤ OOF صادقًا**، تغطي 50.39% من صفوف التدريب البالغ عددها 10,000، و100% من الصفوف المؤهلة لفترات التحقق الأمامية. وتبقى 4,961 عينة تمهيدية بلا تنبؤ OOF.

لا تملأ صفوف OOF المفقودة بتنبؤات التدريب.

يُعلن `MODEL_FOR_DECISION="weighted"` قبل المقارنة، وليس ادعاءً بأن الوزن يجب أن يفوز. احفظ خط الأساس قبل تجربة استراتيجية أخرى؛ يزيد الاختيار المتكرر على أهداف OOF نفسها من تفاؤل التقدير.

يمثل AP المجمّع اليوم Average Precision لجميع صفوف OOF المؤهلة. وليس متوسط AP لطيات اليوم الثاني، ولا مساحة شبه المنحرف لمنحنى PR.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Read ranking and operating-point metrics together

The “flag nobody” reference may show high accuracy while recall is zero. Inspect:

- prevalence;
- ROC-AUC and pooled AP;
- recall and precision at 0.5;
- number and fraction flagged;
- observed educational loss;
- capacity feasibility.

Accuracy is not a sufficient measure under class imbalance. A model can classify the majority class almost everywhere and still miss the cases that matter most to the stated policy.

</td>
<td width="50%" valign="top" dir="rtl">

## اقرأ مقاييس الترتيب ونقطة التشغيل معًا

قد يعرض مرجع «لا ترفع إشارة لأحد» Accuracy مرتفعة بينما يساوي Recall صفرًا. افحص:

- نسبة الفئة الموجبة؛
- ROC-AUC وAP المجمّع؛
- Recall وPrecision عند 0.5؛
- عدد الإشارات ونسبتها؛
- الخسارة التعليمية المرصودة؛
- قابلية التنفيذ ضمن السعة.

لا تكفي Accuracy مع عدم توازن الفئات. قد يصنف النموذج فئة الأغلبية في معظم الحالات، ومع ذلك يفوّت الحالات الأهم للسياسة المعلنة.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Sweep thresholds without breaking ties

A request is flagged when **score ≥ threshold**. The sweep evaluates:

- every distinct score;
- threshold 0.5 explicitly;
- a no-flag rule.

Tied scores remain together. Do not break ties by identifier to fill capacity. If two rules have the same loss, prefer fewer flags and then the higher threshold.

Select:

1. the minimum observed-loss rule without a capacity limit;
2. the minimum observed-loss rule feasible in every period.

The unconstrained rule cannot have higher observed loss than 0.5 because 0.5 is a candidate. The constrained rule may have higher loss if 0.5 is infeasible.

Selection uses OOF labels and is therefore development evidence, not final-test performance.

</td>
<td width="50%" valign="top" dir="rtl">

## امسح العتبات دون كسر التعادل

ترفع الإشارة عندما تكون **الدرجة ≥ العتبة**. يفحص المسح:

- كل درجة مميزة؛
- العتبة 0.5 صراحة؛
- قاعدة بلا إشارات.

تبقى الدرجات المتعادلة معًا. لا تكسر التعادل بالمعرّف لملء السعة. وعند تساوي الخسارة، فضّل إشارات أقل ثم العتبة الأعلى.

اختر:

1. قاعدة بأقل خسارة مرصودة دون قيد سعة؛
2. قاعدة بأقل خسارة مرصودة وقابلة للتنفيذ في كل فترة.

لا يمكن أن تتجاوز خسارة القاعدة غير المقيدة خسارة 0.5 لأن 0.5 مرشحة. وقد تزيد خسارة القاعدة المقيدة إذا كانت 0.5 غير قابلة للتنفيذ.

يستخدم الاختيار أهداف OOF، ولذلك فهو دليل تطوير وليس أداء اختبار نهائي.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Audit capacity and policy sensitivity

The per-period capacity table is the binding evidence. Save the exact exported threshold; rounding may change which tied or boundary scores are flagged.

Test FN costs of 8, 10 and 12 while holding FP cost at 1 and capacity at 12%. These are **±20% policy scenarios**, not confidence intervals.

The theoretical threshold 1/11 requires calibrated probabilities, the stated loss matrix and no capacity limit. Do not impose it on today’s weighted raw scores.

Historical feasibility does not guarantee future feasibility. A real process would monitor queue volume, score distribution, prevalence and threshold stability.

</td>
<td width="50%" valign="top" dir="rtl">

## دقّق السعة وحساسية السياسة

جدول السعة لكل فترة هو الدليل الملزم. احفظ العتبة المصدرة بكامل دقتها، لأن التقريب قد يغيّر الحالات المتعادلة أو الواقعة عند الحد.

اختبر خسارة FN بالقيم 8 و10 و12 مع إبقاء خسارة FP عند 1 والسعة عند 12%. هذه **سيناريوهات سياسة ±20%** وليست فترات ثقة.

تتطلب العتبة النظرية 1/11 احتمالات معايرة ومصفوفة الخسارة المعلنة وغياب قيد السعة. لا تفرضها على درجات اليوم الخام الموزونة.

لا تضمن القابلية التاريخية قابلية المستقبل. تحتاج العملية الفعلية إلى مراقبة حجم الطابور وتوزيع الدرجات ونسبة الحدث واستقرار العتبة.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Treat the regional audit as descriptive evidence

For each synthetic region, the false-positive rate is **FP ÷ non-default cases**. Report the denominator, flags and recall beside the rate.

- The gap is the largest FPR minus the smallest, in percentage points.
- A missing denominator produces a missing value, not zero.
- Fewer than 30 non-default cases triggers a low-support warning.

This is not a significance test, legal fairness certification or causal conclusion about geography. A visible gap requires review; a small gap does not prove fairness. Do not create group-specific thresholds merely to hide a difference.

</td>
<td width="50%" valign="top" dir="rtl">

## تعامل مع تدقيق المناطق بوصفه دليلًا وصفيًا

معدل الإنذار الخاطئ لكل منطقة اصطناعية هو **FP ÷ الحالات غير المتعثرة**. اعرض المقام وعدد الإشارات وRecall بجانب المعدل.

- الفجوة هي أكبر FPR ناقص أصغره بوحدة نقطة مئوية.
- غياب المقام ينتج قيمة غير متاحة، لا صفرًا.
- يؤدي دعم أقل من 30 حالة سليمة إلى تحذير قلة الدعم.

هذا ليس اختبار دلالة أو شهادة عدالة قانونية أو استنتاجًا سببيًا عن الجغرافيا. الفجوة الظاهرة تحتاج إلى مراجعة، والفجوة الصغيرة لا تثبت العدالة. لا تنشئ عتبات خاصة بالمجموعات لمجرد إخفاء الفرق.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Own the decision argument

In the learner-response cell, use numbers from your run to explain:

1. why the selected threshold is defensible;
2. the observed loss–capacity trade-off;
3. the regional FPR gap and what needs review;
4. limits related to OOF selection, coverage, calibration and simplified costs;
5. why accuracy can mislead under imbalance;
6. why threshold selection uses OOF rather than training predictions or challenge data.

The automated checkpoint detects missing text only. It does not assess correctness, assign a grade or establish authorship.

</td>
<td width="50%" valign="top" dir="rtl">

## امتلك حجة القرار

في خلية إجابات المتدرب، استخدم أرقام تشغيلك لتشرح:

1. لماذا يمكن الدفاع عن العتبة المختارة؛
2. المقايضة المرصودة بين الخسارة والسعة؛
3. فجوة FPR بين المناطق وما يحتاج إلى مراجعة؛
4. القيود المرتبطة باختيار OOF والتغطية والمعايرة وتبسيط التكاليف؛
5. لماذا قد تكون Accuracy مضللة مع عدم التوازن؛
6. لماذا نختار العتبة على OOF بدل تنبؤات التدريب أو بيانات التحدي.

يكتشف الفحص الآلي النصوص الناقصة فقط. ولا يقيم صحة الإجابة أو يمنح درجة أو يثبت الملكية.

</td>
</tr>
</table>

## Required evidence | الأدلة المطلوبة

Extract `day3_artifacts.zip` at the repository root. It contains 17 files under `artifacts/` and one card under `reports/`.

| File or group | Evidence purpose | فائدة الدليل |
|---|---|---|
| `cost_curve.png`, `threshold_metrics.json` | Exact threshold, policy and comparison with 0.5 | العتبة الدقيقة والسياسة والمقارنة مع 0.5 |
| `day3_model_report.csv`, `day3_model_comparison.csv` | Fold-level and pooled strategy evidence | أدلة الطيات والمقارنة المجمعة |
| `day3_oof_predictions.csv`, `day3_oof_coverage.csv` | OOF source and coverage | مصدر OOF وتغطيته |
| `threshold_sweep.csv`, `day3_review_flags.csv` | All candidate rules and selected flags | جميع القواعد وإشارات القاعدة المختارة |
| `day3_period_capacity.csv`, `day3_region_audit.csv`, `day3_cost_sensitivity.csv` | Capacity, denominators and policy scenarios | السعة والمقامات وسيناريوهات السياسة |
| `day3_provenance.json`, `day3_run.json`, `environment.json` | Training provenance, settings, hashes and environment | مصدر التدريب والإعدادات والبصمات والبيئة |
| `day3_reflection.json`, `reports/DECISION_CARD.md` | Your reasoning and decision card | تفسيرك وبطاقة القرار |
| `day3_roc_pr.png`, `day3_capacity_regions.png` | Ranking, capacity and group figures | رسوم الترتيب والسعة والمجموعات |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Readiness states and recovery rules

- `TECHNICAL_READY`: the live run and technical checks completed.
- `LEARNER_WORK_REQUIRED`: the technical run passed, but your interpretation is incomplete.
- `READY_FOR_REVIEW`: required text fields exist; this is not an automated grade.
- `EXAMPLE_ONLY_NOT_SUBMITTABLE`: the recovery example was used and cannot represent your work.

If training exceeds the cooperative budget, preserve what you have and rerun later on free CPU. Assessment mode disables the example fallback. Never submit another learner’s table, notebook or decision card.

</td>
<td width="50%" valign="top" dir="rtl">

## حالات الجاهزية وقواعد التعافي

- `TECHNICAL_READY`: اكتمل التشغيل الفعلي والفحص التقني.
- `LEARNER_WORK_REQUIRED`: نجح التشغيل التقني، لكن تفسيرك ناقص.
- `READY_FOR_REVIEW`: الحقول النصية موجودة؛ وهذه ليست درجة آلية.
- `EXAMPLE_ONLY_NOT_SUBMITTABLE`: استُخدم مثال التعافي ولا يمكن اعتباره عملك.

إذا تجاوز التدريب الميزانية التعاونية، فاحفظ ما لديك وأعد التشغيل لاحقًا على CPU المجاني. يعطّل وضع التقييم المثال البديل. لا تسلّم جدول متدرب آخر أو دفتره أو بطاقة قراره.

</td>
</tr>
</table>

## Completion gate | بوابة الإكمال

- The three strategies were compared on the same OOF rows.
- FN, FP and the educational loss matrix can be explained.
- Capacity compliance is shown for every period.
- The exact threshold and its rule `score ≥ threshold` are preserved.
- Sensitivity and regional-audit limits are documented.
- The executed notebook, 17 artifact files and `DECISION_CARD.md` are saved outside the temporary Colab session.

- جرت مقارنة الاستراتيجيات الثلاث على صفوف OOF نفسها.
- تستطيع شرح FN وFP ومصفوفة الخسارة التعليمية.
- أثبت الالتزام بالسعة في كل فترة.
- حُفظت العتبة الدقيقة وقاعدة `score ≥ threshold`.
- وُثقت حدود الحساسية وتدقيق المناطق.
- حُفظ الدفتر المنفذ و17 ملف دليل و`DECISION_CARD.md` خارج جلسة Colab المؤقتة.
