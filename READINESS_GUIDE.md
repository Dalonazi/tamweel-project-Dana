# Readiness Guide | دليل الاستعداد

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<div align="center">

**Complete this 30–40 minute path before Day 1 | أكمل هذا المسار خلال 30–40 دقيقة قبل اليوم الأول**

[Open Notebook 00 in Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/00_readiness_check.ipynb) · [View Notebook 00](notebooks/00_readiness_check.ipynb)

</div>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Readiness outcome

You are ready when you can:

- Open a notebook from GitHub in Colab.
- Select the free CPU runtime.
- Run all cells in order.
- Read a successful environment check.
- Save an executed notebook in your own repository.
- Download and upload project evidence files.
- Explain the basic difference between a class prediction and a probability.

The readiness questions are ungraded. Their purpose is to identify gaps before the assessed project begins.

</td>
<td width="50%" valign="top" dir="rtl">

## نتيجة الاستعداد

تكون جاهزًا عندما تستطيع:

- فتح دفتر من GitHub داخل Colab.
- اختيار بيئة CPU المجانية.
- تشغيل جميع الخلايا بالترتيب.
- قراءة نتيجة فحص البيئة الناجح.
- حفظ دفتر منفذ داخل مستودعك.
- تنزيل ملفات أدلة المشروع ورفعها.
- شرح الفرق الأساسي بين التصنيف والاحتمال.

أسئلة الاستعداد غير محسوبة في الدرجة. هدفها اكتشاف الفجوات قبل بدء المشروع المقيم.

</td>
</tr>
</table>

## Step 1 — Create your project copy | الخطوة 1 — أنشئ نسخة مشروعك

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Sign in to Google and GitHub.
2. Open the course template.
3. Select **Use this template → Create a new repository**.
4. Choose your own account as the owner.
5. Use a neutral name such as `tamweel-project-01`.
6. Confirm that the repository contains the `notebooks`, `scripts`, `data`, `reports`, `artifacts` and `submission` folders.

Do not place your national ID, phone number, private email, password or access token in the repository.

</td>
<td width="50%" valign="top" dir="rtl">

1. سجّل الدخول إلى Google وGitHub.
2. افتح قالب الدورة.
3. اختر **Use this template → Create a new repository**.
4. اختر حسابك بوصفه المالك.
5. استخدم اسمًا محايدًا مثل `tamweel-project-01`.
6. تأكد من وجود المجلدات `notebooks` و`scripts` و`data` و`reports` و`artifacts` و`submission`.

لا تضع رقم الهوية أو رقم الهاتف أو البريد الخاص أو كلمة المرور أو رمز الوصول داخل المستودع.

</td>
</tr>
</table>

## Step 2 — Run Notebook 00 | الخطوة 2 — شغّل دفتر 00

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Open the Colab link above.
2. Confirm that the notebook URL points to the official course template.
3. Select **Runtime → Change runtime type → CPU**. If Colab shows `None`, use that option.
4. Choose **Runtime → Run all**.
5. Allow the setup cell to install only the pinned free packages it needs.
6. Wait for `Environment ready` and `READY`.

If setup asks for a restart because a conflicting package was already imported, select **Runtime → Restart session**, then run from the beginning.

Never bypass a checksum failure or replace a verified file with an unknown download.

</td>
<td width="50%" valign="top" dir="rtl">

1. افتح رابط Colab أعلاه.
2. تأكد أن رابط الدفتر يشير إلى قالب الدورة الرسمي.
3. اختر **Runtime → Change runtime type → CPU**. وإذا ظهر الخيار باسم `None` فاستخدمه.
4. نفّذ **Runtime → Run all**.
5. اسمح لخلية الإعداد بتثبيت الحزم المجانية المثبتة الإصدارات فقط.
6. انتظر ظهور `Environment ready` و`READY`.

إذا طلب الإعداد إعادة التشغيل بسبب حزمة سبق استيرادها بإصدار متعارض، فاختر **Runtime → Restart session** ثم شغّل من البداية.

لا تتجاوز خطأ البصمة ولا تستبدل ملفًا موثقًا بتنزيل مجهول.

</td>
</tr>
</table>

## Step 3 — Review the six concepts | الخطوة 3 — راجع المفاهيم الستة

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

Review these concepts inside the notebook:

1. Binary classification.
2. Predicted probability.
3. Train, validation and test roles.
4. Confusion matrix.
5. Precision and recall.
6. Why evaluation data must remain separate from training.

Enter your answers in the provided learner response area, rerun the review cell and read the feedback. Empty or copied answers do not demonstrate understanding even though this readiness activity is ungraded.

</td>
<td width="50%" valign="top" dir="rtl">

راجع داخل الدفتر المفاهيم الآتية:

1. التصنيف الثنائي.
2. الاحتمال المتوقع.
3. أدوار التدريب والتحقق والاختبار.
4. مصفوفة الالتباس.
5. Precision وRecall.
6. سبب فصل بيانات التقييم عن التدريب.

اكتب إجاباتك في مساحة استجابة المتدرب، ثم أعد تشغيل خلية المراجعة واقرأ التغذية الراجعة. الإجابة الفارغة أو المنسوخة لا تثبت الفهم حتى لو كان نشاط الاستعداد غير محسوب في الدرجة.

</td>
</tr>
</table>

## Step 4 — Save the executed notebook | الخطوة 4 — احفظ الدفتر المنفذ

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

Preferred paths:

**Path A — Download and upload**

1. Select **File → Download → Download .ipynb**.
2. Confirm that the file exists in your device Downloads folder.
3. Open `notebooks/` in your repository.
4. Select **Add file → Upload files**.
5. Upload the executed notebook and commit it with a clear message.

**Path B — Save a copy in GitHub**

Use this only if the feature is already available in your account. Confirm Owner, Repository and File path before saving. Do not paste a personal access token into a notebook.

</td>
<td width="50%" valign="top" dir="rtl">

المسارات الموصى بها:

**المسار A — التنزيل ثم الرفع**

1. اختر **File → Download → Download .ipynb**.
2. تأكد من وجود الملف في مجلد التنزيلات على جهازك.
3. افتح مجلد `notebooks/` في مستودعك.
4. اختر **Add file → Upload files**.
5. ارفع الدفتر المنفذ واحفظه برسالة Commit واضحة.

**المسار B — Save a copy in GitHub**

استخدمه فقط إذا كان متاحًا مسبقًا في حسابك. راجع Owner وRepository وFile path قبل الحفظ. لا تلصق Personal Access Token داخل الدفتر.

</td>
</tr>
</table>

## Step 5 — Save the readiness evidence | الخطوة 5 — احفظ أدلة الاستعداد

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

In the Colab file panel, open:

```text
tamweel/artifacts/
```

Download `readiness_artifacts.zip`, extract it on your device and upload these files to `artifacts/` in your repository:

- `environment.json`
- `data_check.json`
- `runtime_checks.json`
- `readiness_report.json`

Open each uploaded file in GitHub to confirm that it is readable and stored in the correct repository.

</td>
<td width="50%" valign="top" dir="rtl">

من لوحة الملفات في Colab افتح:

```text
tamweel/artifacts/
```

نزّل `readiness_artifacts.zip`، وفك ضغطه على جهازك، ثم ارفع الملفات الآتية إلى مجلد `artifacts/` في مستودعك:

- `environment.json`
- `data_check.json`
- `runtime_checks.json`
- `readiness_report.json`

افتح كل ملف بعد رفعه في GitHub للتأكد من أنه مقروء ومحفوظ داخل المستودع الصحيح.

</td>
</tr>
</table>

## Readiness checklist | قائمة التحقق من الاستعداد

- [ ] I created my own repository from the template. | أنشأت مستودعي من القالب.
- [ ] I used the free CPU runtime. | استخدمت CPU المجاني.
- [ ] Notebook 00 completed with `READY`. | اكتمل دفتر 00 بحالة `READY`.
- [ ] I reviewed the six ungraded questions. | راجعت الأسئلة الستة غير المحسوبة.
- [ ] I saved the executed notebook. | حفظت الدفتر المنفذ.
- [ ] I uploaded the four JSON evidence files. | رفعت ملفات JSON الأربعة.
- [ ] I opened the uploaded files in GitHub. | فتحت الملفات المرفوعة في GitHub للتأكد منها.

## Common readiness problems | مشكلات الاستعداد الشائعة

| Symptom | English action | الإجراء بالعربية |
|---|---|---|
| Temporary download failure | Rerun the setup cell. Keep verified local files if their hashes match. | أعد خلية الإعداد، واحتفظ بالملفات المحلية فقط إذا تطابقت بصماتها. |
| Checksum mismatch | Reopen the approved notebook and restore the original file. | أعد فتح الدفتر المعتمد واسترجع الملف الأصلي. |
| Imported package version conflict | Restart the session, then run setup before importing packages. | أعد تشغيل الجلسة ثم شغّل الإعداد قبل استيراد الحزم. |
| Colab runtime disconnected | Reopen the saved notebook and run from the beginning. | افتح الدفتر المحفوظ وأعد التشغيل من البداية. |
| File exists in Colab but not on the device | Refresh the Files panel and download the file explicitly. | حدّث لوحة Files ونزّل الملف صراحة. |
| Free usage limit reached | Save your work and retry later; do not purchase compute. | احفظ عملك وأعد المحاولة لاحقًا؛ لا تشترِ موارد حوسبة. |

## Supported fallback | المسار البديل المدعوم

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

If network access repeatedly fails and no verified local files are available, download the repository ZIP from GitHub, extract it on your device and upload the unchanged `scripts/`, `data/`, requirements and constraints files to `/content/tamweel/` while preserving folder names. The same checksums still apply. Internet access may still be required to install a missing package.

This fallback restores source files only. It does not provide model outputs or replace your assessed execution.

</td>
<td width="50%" valign="top" dir="rtl">

إذا تكرر فشل الشبكة ولم تتوفر ملفات محلية موثقة، فنزّل ZIP المستودع من GitHub، وفك ضغطه على جهازك، ثم ارفع مجلدي `scripts/` و`data/` وملفات المتطلبات والقيود دون تعديل إلى `/content/tamweel/` مع الحفاظ على أسماء المجلدات. تبقى فحوص البصمات نفسها مطبقة، وقد تحتاج إلى الإنترنت لتثبيت حزمة مفقودة.

هذا المسار يعيد ملفات المصدر فقط، ولا يوفر مخرجات نموذج ولا يستبدل تنفيذك المقيم.

</td>
</tr>
</table>

[Colab availability policy](https://research.google.com/colaboratory/faq.html) · [Colab guide | دليل Colab](COLAB_GUIDE.md) · [Troubleshooting | حل المشكلات](TROUBLESHOOTING.md)