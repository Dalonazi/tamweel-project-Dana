# Start Your Project | ابدأ مشروعك

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<div align="center">

**SDA-DSC-211 · Advanced Machine Learning Methods | أساليب تعلم الآلة المتقدمة**  
**Tamweel Lite · Five-day progressive project | مشروع تراكمي لمدة خمسة أيام**

[Learning portal](https://almiyead-rgb.github.io/advanced-machine-learning-methods-sda-dsc-211/) · [Readiness guide](READINESS_GUIDE.md) · [Assessment](RUBRIC.md)

</div>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## What you will build

You will build one connected machine-learning project across five days. Each day adds a verified layer: baseline models, honest validation, cost-sensitive decision policy, interpretation and calibration, then ensemble selection and final delivery.

Your final repository must contain executed notebooks, evidence files, reports, a reproducible inference package, final predictions, a Model Card and a five-slide presentation.

</td>
<td width="50%" valign="top" dir="rtl">

## ماذا ستبني؟

ستبني مشروع تعلم آلي واحدًا مترابطًا خلال خمسة أيام. يضيف كل يوم طبقة قابلة للتحقق: نماذج خط الأساس، والتحقق الصادق، وسياسة القرار الحساسة للتكلفة، والتفسير والمعايرة، ثم اختيار التجميع والتسليم النهائي.

يجب أن يحتوي مستودعك النهائي على الدفاتر المنفذة، وملفات الأدلة، والتقارير، وحزمة استدلال قابلة لإعادة التشغيل، والتنبؤات النهائية، وبطاقة النموذج، وعرض من خمس شرائح.

</td>
</tr>
</table>

## Before you begin | قبل أن تبدأ

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

You need:

- A free Google account for Colab.
- A free GitHub account for storing your project.
- A modern desktop or laptop browser.
- Basic familiarity with Python, pandas and binary classification.

You do **not** need a GPU, credit card, API key, paid subscription, local Python installation or Google Drive mount.

If GitHub or Colab is new to you, complete the beginner path in the readiness guide before Day 1.

</td>
<td width="50%" valign="top" dir="rtl">

تحتاج إلى:

- حساب Google مجاني لتشغيل Colab.
- حساب GitHub مجاني لحفظ المشروع.
- متصفح حديث على حاسب مكتبي أو محمول.
- معرفة أساسية بـPython وpandas والتصنيف الثنائي.

لا تحتاج إلى GPU أو بطاقة دفع أو مفتاح API أو اشتراك مدفوع أو تثبيت Python محليًا أو ربط Google Drive.

إذا كانت هذه أول تجربة لك مع GitHub أو Colab، فأكمل مسار المبتدئين في دليل الاستعداد قبل اليوم الأول.

</td>
</tr>
</table>

## Create your repository | أنشئ مستودعك

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Open the course template repository.
2. Select **Use this template → Create a new repository**.
3. Choose your own GitHub account as the owner.
4. Use a project name such as `tamweel-project-01`.
5. Do not include your national ID, phone number, private email or grade in the repository name or files.
6. Keep the repository available to the instructor according to the cohort policy.

After creation, confirm that your browser URL contains your GitHub username and your new repository name.

</td>
<td width="50%" valign="top" dir="rtl">

1. افتح مستودع قالب الدورة.
2. اختر **Use this template → Create a new repository**.
3. اختر حسابك في GitHub بوصفه المالك.
4. استخدم اسمًا مثل `tamweel-project-01`.
5. لا تضع رقم الهوية أو رقم الهاتف أو البريد الخاص أو الدرجة في اسم المستودع أو ملفاته.
6. أبقِ المستودع متاحًا للمدربة وفق سياسة الدفعة.

بعد الإنشاء، تأكد أن رابط المتصفح يحتوي اسم حسابك واسم مستودعك الجديد.

</td>
</tr>
</table>

## Complete the readiness check | أكمل فحص الاستعداد

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Read [READINESS_GUIDE.md](READINESS_GUIDE.md).
2. Open [Notebook 00 in Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/00_readiness_check.ipynb).
3. Select the free CPU runtime.
4. Choose **Runtime → Run all**.
5. Confirm that you see `Environment ready` and `READY`.
6. Review the six ungraded questions.
7. Save the executed notebook and the four readiness JSON files in your own repository.

Do not continue by ignoring a checksum, missing-file or package-version failure.

</td>
<td width="50%" valign="top" dir="rtl">

1. اقرأ [READINESS_GUIDE.md](READINESS_GUIDE.md).
2. افتح [دفتر 00 في Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/00_readiness_check.ipynb).
3. اختر بيئة CPU المجانية.
4. نفّذ **Runtime → Run all**.
5. تأكد من ظهور `Environment ready` و`READY`.
6. راجع الأسئلة الستة غير المحسوبة في الدرجة.
7. احفظ الدفتر المنفذ وملفات JSON الأربعة الخاصة بالاستعداد داخل مستودعك.

لا تتابع العمل مع تجاهل خطأ في البصمة أو ملف مفقود أو إصدار مكتبة غير مطابق.

</td>
</tr>
</table>

## Five-day journey | رحلة الأيام الخمسة

| Day | English outcome | المخرج بالعربية | Guide |
|---:|---|---|---|
| 1 | Compare Logistic Regression, XGBoost and LightGBM; choose a justified candidate | مقارنة Logistic Regression وXGBoost وLightGBM واختيار نموذج مرشح مبرر | [Day 1](DAY1_GUIDE.md) |
| 2 | Build honest time/customer validation, leakage audits and bounded Optuna search | بناء تحقق صادق يراعي الزمن والعملاء وتدقيق التسرب وبحث Optuna محدود | [Day 2](DAY2_GUIDE.md) |
| 3 | Compare imbalance treatments and select a threshold under cost and capacity constraints | مقارنة معالجة عدم التوازن واختيار عتبة ضمن قيود التكلفة والسعة | [Day 3](DAY3_GUIDE.md) |
| 4 | Explain the fitted model, calibrate probabilities and document stability limits | تفسير النموذج ومعايرة الاحتمالات وتوثيق حدود الاستقرار | [Day 4](DAY4_GUIDE.md) |
| 5 | Evaluate averaging and stacking, freeze the final pipeline and prepare delivery | تقييم المتوسطات والتكديس وتجميد المسار النهائي وتجهيز التسليم | [Day 5](DAY5_GUIDE.md) |

## Save your work correctly | احفظ عملك بطريقة صحيحة

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

For every day:

1. Work from your own notebook copy.
2. Run the notebook from the first cell to the last cell.
3. Read the result interpretation prompts.
4. Complete the learner-owned response fields.
5. Download or save the executed notebook.
6. Upload the actual CSV, JSON, figures and reports—not screenshots only.
7. Use a clear commit message.
8. Open the uploaded file in GitHub to confirm the destination.

Colab sessions are temporary. A file created in the runtime is not safely stored until you download or commit it.

</td>
<td width="50%" valign="top" dir="rtl">

في كل يوم:

1. اعمل على نسخة الدفتر الخاصة بك.
2. شغّل الدفتر من أول خلية إلى آخر خلية.
3. اقرأ أسئلة تفسير النتائج.
4. أكمل الحقول التي يكتبها المتدرب بنفسه.
5. نزّل الدفتر المنفذ أو احفظه.
6. ارفع ملفات CSV وJSON والرسوم والتقارير الفعلية، لا لقطات الشاشة وحدها.
7. استخدم رسالة Commit واضحة.
8. افتح الملف بعد رفعه في GitHub للتأكد من الوجهة.

جلسات Colab مؤقتة. وجود الملف داخل Runtime لا يعني أنه حُفظ بأمان ما لم تنزله أو ترفعه إلى المستودع.

</td>
</tr>
</table>

## Final submission | التسليم النهائي

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

The five daily stages are submitted once as one complete project.

Before submission:

1. Complete all reports and the five-slide presentation.
2. Run [Notebook 99](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/99_final_submission_check.ipynb).
3. Correct issues in the original files and rerun the check.
4. Run **Actions → Final Project Check** in your repository.
5. Record the exact full commit SHA.
6. Create the final tag on that same commit.
7. Submit through the private cohort channel and keep the receipt.

Read [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md). Technical readiness is not a grade, authenticity determination or submission receipt.

</td>
<td width="50%" valign="top" dir="rtl">

تُسلّم مراحل الأيام الخمسة مرة واحدة كمشروع كامل.

قبل التسليم:

1. أكمل جميع التقارير والعرض المكون من خمس شرائح.
2. شغّل [دفتر 99](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/99_final_submission_check.ipynb).
3. صحح المشكلات في الملفات الأصلية ثم أعد الفحص.
4. شغّل **Actions → Final Project Check** في مستودعك.
5. سجل Commit SHA الكامل والدقيق.
6. أنشئ Tag النهائي على Commit نفسه.
7. سلّم عبر القناة الخاصة للدفعة واحتفظ بإيصال الاستلام.

اقرأ [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md). الجاهزية التقنية ليست درجة ولا إثبات أصالة ولا إيصال استلام.

</td>
</tr>
</table>

## Essential references | المراجع الأساسية

- [Colab guide | دليل Colab](COLAB_GUIDE.md)
- [GitHub guide | دليل GitHub](GITHUB_GUIDE.md)
- [Technical requirements | المتطلبات التقنية](TECHNICAL_REQUIREMENTS.md)
- [Administrative requirements | المتطلبات الإدارية](ADMINISTRATIVE_REQUIREMENTS.md)
- [Assessment rubric | سلم التقييم](RUBRIC.md)
- [Troubleshooting | حل المشكلات](TROUBLESHOOTING.md)
- [Learning resources | الموارد التعليمية](LEARNING_RESOURCES.md)

> Never publish passwords, tokens, personal identifiers, private grades, hidden labels or submission receipts.  
> لا تنشر كلمات المرور أو رموز الوصول أو المعرّفات الشخصية أو الدرجات الخاصة أو التسميات المخفية أو إيصالات التسليم.