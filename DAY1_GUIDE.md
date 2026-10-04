# Day 1 Guide | دليل اليوم الأول

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<div align="center">

**SDA-DSC-211 · Tamweel Lite · Baseline and Boosting | خط الأساس ونماذج التعزيز**

[Open Day 1 in Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/01_baseline_boosting.ipynb) · [View notebook](notebooks/01_baseline_boosting.ipynb) · [Data guide](data/DATA_GUIDE.md)

</div>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## What you will build

In 60 minutes, produce a reproducible comparison of **Logistic Regression, XGBoost and LightGBM** on the same synthetic financing-risk data. Select one initial candidate and justify the choice with evidence from your own run.

This lab is a **teaching baseline**, not a deployment estimate. The stratified random split does not separate repeated customers and does not reproduce time or target-maturity boundaries. Day 2 replaces it with honest validation.

**Required outcome:** a technically complete run plus your own problem statement, candidate choice, evidence, limitation, next test and two exit answers.

</td>
<td width="50%" valign="top" dir="rtl">

## ماذا ستبني؟

خلال 60 دقيقة، أنشئ مقارنة قابلة لإعادة الإنتاج بين **Logistic Regression وXGBoost وLightGBM** على بيانات مخاطر تمويل اصطناعية موحدة. اختر مرشحًا أوليًا واحدًا وبرر قرارك بأدلة من تشغيلك أنت.

هذا اللاب **خط أساس تعليمي** وليس تقديرًا للنشر. التقسيم العشوائي الطبقي لا يفصل العملاء المتكررين ولا يحاكي حدود الزمن أو نضج الهدف. سيستبدله اليوم الثاني بتحقق صادق.

**المخرج المطلوب:** تشغيل مكتمل تقنيًا، وصياغة مشكلة من كتابتك، واختيار مرشح، ودليل، وقيد، واختبار تالٍ، وإجابتان عن سؤالي الخروج.

</td>
</tr>
</table>

## Lab journey | رحلة اللاب

| Minutes | English task | المهمة بالعربية |
|---:|---|---|
| 0–5 | Start a fresh free-CPU session | ابدأ جلسة جديدة على CPU المجاني |
| 5–12 | Inspect data, target and split roles | افحص البيانات والهدف وأدوار التقسيم |
| 12–22 | Fit the Logistic Regression baseline | درّب خط الأساس Logistic Regression |
| 22–38 | Select boosting rounds and refit XGBoost and LightGBM | اختر جولات التعزيز وأعد تدريب XGBoost وLightGBM |
| 38–48 | Compare metrics, timing and curves | قارن المقاييس والزمن والمنحنيات |
| 48–55 | Select a candidate and write your argument | اختر مرشحًا واكتب حجتك |
| 55–60 | Export evidence and verify completion | صدّر الأدلة وتحقق من الإكمال |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Start from a fresh session

1. Open the notebook and select the free **CPU** runtime.
2. Choose **Runtime → Run all**. Notebook 00 is not required beforehand.
3. Do not mount Drive and do not add API keys.
4. Use the default `FAST_MODE=True` first: 10,000 rows, 22 features, up to 300 trees and two CPU threads.
5. Use `FULL_MODE=True` only after preserving the baseline run; it raises the ceiling to 900 trees but is not required.
6. If setup requests a restart, choose **Restart session** and run all cells from the beginning.

The actual duration varies with the free Colab service. Resource limits are not a reason to purchase a subscription.

</td>
<td width="50%" valign="top" dir="rtl">

## ابدأ من جلسة جديدة

1. افتح الدفتر واختر بيئة **CPU** المجانية.
2. اختر **Runtime → Run all**. لا يلزم تشغيل دفتر 00 قبله.
3. لا تربط Drive ولا تضف مفاتيح API.
4. استخدم أولًا الإعداد الافتراضي `FAST_MODE=True`: عدد 10,000 سجل و22 خاصية وحتى 300 شجرة وخيطَي CPU.
5. استخدم `FULL_MODE=True` فقط بعد حفظ تجربة الأساس؛ يرفع السقف إلى 900 شجرة لكنه غير إلزامي.
6. إذا طلب الإعداد إعادة التشغيل، اختر **Restart session** ثم شغّل جميع الخلايا من البداية.

يختلف الزمن الفعلي حسب خدمة Colab المجانية. حدود الموارد ليست سببًا لشراء اشتراك.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Understand the four data roles

| Role | Rows | Purpose |
|---|---:|---|
| Inner fit | 6,000 | Learn preprocessing and boosting trees while selecting their count |
| Inner stop | 2,000 | Select the tree count using log loss |
| Development | 8,000 | Refit all three models after internal decisions are fixed |
| Comparison | 2,000 | Score the models once after fitting |

The 6,000 and 2,000 inner sets are contained inside the 8,000 development rows; they are not extra data. Seed 211 controls the outer split and models, while seed 212 controls the inner split.

The comparison rows must not be used for early stopping or repeated tuning. Reusing them to chase the highest score converts them into a tuning set.

</td>
<td width="50%" valign="top" dir="rtl">

## افهم أدوار البيانات الأربعة

| الدور | الصفوف | الغرض |
|---|---:|---|
| Inner fit | 6,000 | تعلم المعالجة وأشجار التعزيز أثناء اختيار عددها |
| Inner stop | 2,000 | اختيار عدد الأشجار باستخدام log loss |
| Development | 8,000 | إعادة تدريب النماذج الثلاثة بعد تثبيت القرارات الداخلية |
| Comparison | 2,000 | تقييم النماذج مرة واحدة بعد التدريب |

مجموعتا 6,000 و2,000 الداخليتان جزء من صفوف التطوير البالغ عددها 8,000، وليستا بيانات إضافية. تتحكم البذرة 211 في التقسيم الخارجي والنماذج، بينما تتحكم البذرة 212 في التقسيم الداخلي.

يجب ألا تستخدم صفوف المقارنة للإيقاف المبكر أو الضبط المتكرر. إعادة استخدامها للبحث عن أعلى نتيجة تحولها إلى مجموعة ضبط.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Read the metrics correctly

- **ROC-AUC:** ranking quality across thresholds.
- **Average Precision (AP):** non-interpolated summary of the precision–recall curve; this is the course definition of PR-AUC.
- **train_seconds:** boosting tree selection plus refit, or baseline fitting for Logistic Regression. Download and plotting time are excluded.
- **selected_trees:** one-based selected tree count. It is blank for Logistic Regression.

Inspect ROC-AUC and AP together, especially because the positive class is uncommon. Report sample size and positive prevalence with the metrics.

A small difference on one split does not prove general superiority. This lab does not establish calibration, operational value or stability.

</td>
<td width="50%" valign="top" dir="rtl">

## اقرأ المقاييس بصورة صحيحة

- **ROC-AUC:** جودة ترتيب الحالات عبر العتبات.
- **Average Precision (AP):** ملخص غير مستوفى خطيًا لمنحنى precision–recall؛ وهو تعريف PR-AUC المعتمد في الدورة.
- **train_seconds:** اختيار عدد أشجار التعزيز وإعادة التدريب، أو تدريب خط الأساس في Logistic Regression. لا يشمل التنزيل والرسم.
- **selected_trees:** عدد الأشجار المختار ويبدأ من 1. تبقى الخانة فارغة لـLogistic Regression.

اقرأ ROC-AUC وAP معًا، خصوصًا مع ندرة الفئة الموجبة. اذكر حجم العينة ونسبة الموجب مع المقاييس.

الفارق الصغير في تقسيم واحد لا يثبت تفوقًا عامًا. لا يثبت هذا اللاب المعايرة أو القيمة التشغيلية أو الاستقرار.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Own the decision

In the **Your decision** cell, complete:

1. A problem statement covering the outcome, decision time and teaching use.
2. One candidate: Logistic Regression, XGBoost or LightGBM.
3. One numerical or comparative evidence statement from your run.
4. One limitation the experiment cannot resolve.
5. One next test that could change your decision.
6. Two exit answers:
   - Why inspect AP beside ROC-AUC under class imbalance?
   - Why must the comparison sample remain separate from early stopping?

The checkpoint only detects missing fields. It does not assess correctness, award a grade or prove authorship. Do not copy a peer's table or explanation.

</td>
<td width="50%" valign="top" dir="rtl">

## امتلك قرارك

في خلية **Your decision** أكمل:

1. صياغة مشكلة توضح النتيجة ولحظة القرار والاستخدام التعليمي.
2. مرشحًا واحدًا: Logistic Regression أو XGBoost أو LightGBM.
3. دليلًا رقميًا أو مقارنة من تشغيلك.
4. قيدًا لا تستطيع التجربة معالجته.
5. اختبارًا تاليًا قد يغير قرارك.
6. إجابتين عن سؤالي الخروج:
   - لماذا تفحص AP بجانب ROC-AUC عند عدم توازن الفئات؟
   - لماذا يجب فصل عينة المقارنة عن الإيقاف المبكر؟

يكتشف الفحص الخانات الفارغة فقط. لا يقيم صحة الإجابة ولا يمنح درجة ولا يثبت الملكية. لا تنسخ جدول زميل أو تفسيره.

</td>
</tr>
</table>

## Required evidence | الأدلة المطلوبة

Save the executed notebook as `notebooks/01_baseline_boosting.ipynb`. Extract `day1_artifacts.zip` and upload these eight files to `artifacts/`:

| File | Evidence purpose | فائدة الدليل |
|---|---|---|
| `environment.json` | Environment versions and source files | إصدارات البيئة ومصادر الملفات |
| `day1_model_comparison.csv` | Metrics and timing for all three models | مقاييس النماذج الثلاثة وأزمنتها |
| `day1_comparison_predictions.csv` | Probabilities for the 2,000 comparison rows | احتمالات صفوف المقارنة البالغ عددها 2,000 |
| `day1_split_membership.csv` | Role assigned to each application | دور كل طلب داخل التقسيم |
| `day1_learning_curves.png` | Evidence for selected boosting rounds | دليل اختيار عدد جولات التعزيز |
| `day1_roc_pr.png` | ROC and precision–recall comparison | مقارنة ROC وprecision–recall |
| `day1_reflection.json` | Your problem statement and reasoning | صياغة المشكلة وحجتك وإجاباتك |
| `day1_run.json` | Configuration, hashes and run provenance | الإعدادات والبصمات ومصدر التشغيل |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Readiness states

- `TECHNICAL_READY`: three models and technical evidence were produced.
- `LEARNER_WORK_REQUIRED`: execution passed, but learner-owned fields remain incomplete.
- `READY_FOR_REVIEW`: required fields are present. This is not an automated grade and does not guarantee the quality of the argument.

Copy the problem statement into your project README. Save the notebook and files outside the temporary Colab session before closing it.

</td>
<td width="50%" valign="top" dir="rtl">

## حالات الجاهزية

- `TECHNICAL_READY`: أُنتجت النماذج الثلاثة والأدلة التقنية.
- `LEARNER_WORK_REQUIRED`: نجح التنفيذ، لكن الحقول التي يكتبها المتدرب غير مكتملة.
- `READY_FOR_REVIEW`: الحقول المطلوبة موجودة. لا تمثل هذه الحالة درجة آلية ولا تضمن جودة الحجة.

انسخ صياغة المشكلة إلى README الخاص بمشروعك. احفظ الدفتر والملفات خارج جلسة Colab المؤقتة قبل إغلاقها.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Troubleshooting

| Symptom | Action |
|---|---|
| Download interrupted | Rerun the setup cell; it retries temporary failures and accepts only a matching local copy |
| Imported package version differs | Restart the session, then run all cells from setup |
| SHA-256 mismatch | Restore the original published file; never bypass the check |
| Free session ended | Reopen the saved notebook and rerun on free CPU |
| Learner work still required | Complete the decision cell, then rerun export |

Optional local execution uses Python 3.12 or 3.13 with `requirements-colab.txt` and `constraints.txt`. Colab remains the supported beginner path.

</td>
<td width="50%" valign="top" dir="rtl">

## حل المشكلات

| ما ظهر | الإجراء |
|---|---|
| انقطع التنزيل | أعد خلية الإعداد؛ تعيد المحاولة ولا تقبل إلا نسخة محلية مطابقة |
| اختلف إصدار مكتبة مستوردة | أعد تشغيل الجلسة ثم شغّل جميع الخلايا من الإعداد |
| اختلفت بصمة SHA-256 | استرجع الملف المنشور الأصلي ولا تتجاوز الفحص |
| انتهت الجلسة المجانية | افتح الدفتر المحفوظ وأعد التشغيل على CPU المجاني |
| ما زال عمل المتدرب مطلوبًا | أكمل خلية القرار ثم أعد خلية التصدير |

يدعم التشغيل المحلي الاختياري Python 3.12 أو 3.13 باستخدام `requirements-colab.txt` و`constraints.txt`. يبقى Colab هو المسار المعتمد للمبتدئين.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Completion gate

Before moving to Day 2, confirm that:

- The comparison CSV contains three valid model rows.
- You can explain development, inner fit, inner stop and comparison roles.
- Your decision cites evidence and acknowledges a limitation.
- All eight evidence files and the executed notebook are saved.
- No personal data, password or access token is present in the public repository.

**Optional extension:** preserve the baseline, then change `learning_rate` once using the same split. Document the change in tree count and time without claiming that one attempt identifies the best setting.

</td>
<td width="50%" valign="top" dir="rtl">

## بوابة الإكمال

قبل الانتقال إلى اليوم الثاني، تحقق من الآتي:

- يحتوي ملف المقارنة على ثلاثة صفوف صالحة للنماذج.
- تستطيع شرح أدوار development وinner fit وinner stop وcomparison.
- يستشهد قرارك بدليل ويقر بقيد واضح.
- حفظت ملفات الأدلة الثمانية والدفتر المنفذ.
- لا توجد بيانات شخصية أو كلمة مرور أو رمز دخول في المستودع العام.

**توسع اختياري:** احفظ تجربة الأساس، ثم غيّر `learning_rate` مرة واحدة باستخدام التقسيم نفسه. وثق أثر التغيير على عدد الأشجار والزمن دون الادعاء بأن محاولة واحدة تحدد أفضل إعداد.

</td>
</tr>
</table>

Prepared and delivered by **Meaad Al-Marri | ميعاد المري** · [GitHub guide | دليل GitHub](GITHUB_GUIDE.md) · [Assessment rubric | التقييم](RUBRIC.md)
