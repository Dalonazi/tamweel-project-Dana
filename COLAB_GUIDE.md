# Google Colab Guide | دليل Google Colab

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<div align="center">

**Free CPU · No API key · No paid subscription · No Drive mount required**  
**CPU مجاني · دون مفتاح API · دون اشتراك مدفوع · دون حاجة إلى ربط Drive**

[Open Notebook 00](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/00_readiness_check.ipynb) · [Readiness guide](READINESS_GUIDE.md)

</div>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## What Colab is

Google Colab runs Python notebooks in a browser. The runtime is temporary: variables, installed packages and generated files can disappear when the session ends or disconnects. Your GitHub repository—not the Colab runtime—is the permanent project record.

Use Colab to execute code. Use GitHub to preserve notebooks, reports and evidence.

</td>
<td width="50%" valign="top" dir="rtl">

## ما هو Colab؟

يشغّل Google Colab دفاتر Python داخل المتصفح. بيئة التشغيل مؤقتة؛ فقد تختفي المتغيرات والحزم المثبتة والملفات الناتجة عند انتهاء الجلسة أو انقطاعها. مستودع GitHub هو السجل الدائم للمشروع، وليس Runtime في Colab.

استخدم Colab لتنفيذ الكود، واستخدم GitHub لحفظ الدفاتر والتقارير والأدلة.

</td>
</tr>
</table>

## Open the approved notebook | افتح الدفتر المعتمد

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Use the Colab link in the course README or the daily guide.
2. Confirm that the URL contains:

```text
almiyead-rgb/sda-dsc-211-student-template
```

3. Review the notebook title before running it.
4. Save a copy for your own project before making learner changes.

Do not run a notebook copied from an unknown source or shared through an unverified shortened link.

</td>
<td width="50%" valign="top" dir="rtl">

1. استخدم رابط Colab الموجود في README أو دليل اليوم.
2. تأكد أن الرابط يحتوي:

```text
almiyead-rgb/sda-dsc-211-student-template
```

3. راجع عنوان الدفتر قبل تشغيله.
4. احفظ نسخة خاصة بمشروعك قبل إدخال تعديلات المتدرب.

لا تشغّل دفترًا من مصدر مجهول أو من رابط مختصر غير موثق.

</td>
</tr>
</table>

## Select the runtime | اختر بيئة التشغيل

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Select **Runtime → Change runtime type**.
2. Choose **CPU**. Some interfaces display this as `None` under hardware accelerator.
3. Keep the standard hosted runtime.
4. Do not enable GPU or TPU for this course.

The project is designed for the free CPU runtime and two CPU threads. Buying compute units is not required.

</td>
<td width="50%" valign="top" dir="rtl">

1. اختر **Runtime → Change runtime type**.
2. اختر **CPU**. وقد يظهر الخيار باسم `None` ضمن Hardware accelerator.
3. استخدم البيئة المستضافة القياسية.
4. لا تفعّل GPU أو TPU لهذه الدورة.

صُمم المشروع للعمل على CPU المجاني وباستخدام خيطي CPU. لا يلزم شراء وحدات حوسبة.

</td>
</tr>
</table>

## Run the notebook correctly | شغّل الدفتر بالطريقة الصحيحة

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

For the primary run:

1. Read the objective and boundary section.
2. Select **Runtime → Run all**.
3. Allow the setup cell to verify packages, revisions and checksums.
4. Wait for each cell to finish before editing learner response fields.
5. Read warnings and interpretation prompts.
6. Complete learner-owned answers.
7. Rerun the relevant response/export cells.

Do not run cells in a random order on the first attempt. Do not skip the setup cell. Do not change pinned revisions, file hashes or assessment flags.

</td>
<td width="50%" valign="top" dir="rtl">

في التشغيل الأساسي:

1. اقرأ قسم الهدف والحدود.
2. اختر **Runtime → Run all**.
3. اسمح لخلية الإعداد بالتحقق من الحزم والإصدارات والبصمات.
4. انتظر اكتمال كل خلية قبل تعديل حقول استجابة المتدرب.
5. اقرأ التحذيرات وأسئلة تفسير النتائج.
6. أكمل الإجابات التي يكتبها المتدرب.
7. أعد تشغيل خلايا الإجابات والتصدير المرتبطة بها.

لا تشغّل الخلايا بترتيب عشوائي في المحاولة الأولى. لا تتجاوز خلية الإعداد. لا تغير الإصدارات المثبتة أو بصمات الملفات أو أعلام التقييم.

</td>
</tr>
</table>

## Understand cell states | افهم حالات الخلايا

| Colab state | English meaning | المعنى بالعربية |
|---|---|---|
| Empty execution indicator | Cell has not run in this session | لم تُشغّل الخلية في الجلسة الحالية |
| Spinning indicator | Cell is running | الخلية قيد التنفيذ |
| Numbered indicator | Cell completed in the current execution order | اكتملت الخلية وفق ترتيب التنفيذ الحالي |
| Red error output | Execution stopped or produced an exception | توقف التنفيذ أو ظهر استثناء |
| Warning text | Read before continuing; it may describe a limitation rather than a failure | اقرأ التحذير قبل المتابعة؛ فقد يصف قيدًا وليس فشلًا |

## Save the notebook | احفظ الدفتر

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

### Recommended path: download and upload

1. After `Run all`, select **File → Download → Download .ipynb**.
2. Confirm the file exists on your device.
3. Upload it to `notebooks/` in your own GitHub repository.
4. Open it from GitHub and confirm that outputs are present.

### Optional path: Save a copy in GitHub

Use this only if it is already available in your account. Verify:

- Owner
- Repository
- Branch
- File path

Do not enter a GitHub password or personal access token into a notebook.

</td>
<td width="50%" valign="top" dir="rtl">

### المسار الموصى به: التنزيل ثم الرفع

1. بعد `Run all` اختر **File → Download → Download .ipynb**.
2. تأكد من وجود الملف على جهازك.
3. ارفعه إلى مجلد `notebooks/` داخل مستودعك.
4. افتحه من GitHub وتأكد من وجود المخرجات.

### المسار الاختياري: Save a copy in GitHub

استخدمه فقط إذا كان متاحًا مسبقًا في حسابك. راجع:

- Owner
- Repository
- Branch
- File path

لا تدخل كلمة مرور GitHub أو Personal Access Token داخل دفتر.

</td>
</tr>
</table>

## Download evidence files | نزّل ملفات الأدلة

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Open the **Files** panel on the left side of Colab.
2. Select the refresh icon if a generated file is not visible.
3. Open the output folder named in the notebook.
4. Use the file menu and select **Download**.
5. Download one file or the provided evidence ZIP.
6. Confirm that the download reached your device.
7. Upload the extracted evidence to the correct GitHub folder.

Typical locations:

- Daily outputs: `/content/tamweel/artifacts/`
- Reports: `/content/tamweel/reports/`
- Final submission: `/content/tamweel/submission/`
- Notebook 99 downloads: `/content/final_check_downloads/`

</td>
<td width="50%" valign="top" dir="rtl">

1. افتح لوحة **Files** في الجانب الأيسر من Colab.
2. اضغط زر التحديث إذا لم يظهر الملف الناتج.
3. افتح مجلد المخرجات المذكور في الدفتر.
4. افتح قائمة الملف واختر **Download**.
5. نزّل الملف منفردًا أو حزمة الأدلة ZIP.
6. تأكد أن التنزيل وصل إلى جهازك.
7. ارفع الأدلة بعد فكها إلى المجلد الصحيح في GitHub.

المسارات المعتادة:

- مخرجات الأيام: `/content/tamweel/artifacts/`
- التقارير: `/content/tamweel/reports/`
- التسليم النهائي: `/content/tamweel/submission/`
- تنزيلات دفتر 99: `/content/final_check_downloads/`

</td>
</tr>
</table>

## Restart, reconnect and rerun | إعادة التشغيل والاتصال

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

Use **Restart session** when:

- Setup reports that a conflicting package version was already imported.
- The notebook explicitly asks for a restart after installation.
- The runtime state is inconsistent after a failed experiment.

After restarting, run from the first cell. Variables and generated files from the previous runtime may be gone.

If the browser reconnects to the same runtime, inspect the cell state before continuing. When uncertain, save your work and start a fresh session.

</td>
<td width="50%" valign="top" dir="rtl">

استخدم **Restart session** عندما:

- يذكر الإعداد أن إصدار حزمة متعارضًا سبق استيراده.
- يطلب الدفتر إعادة التشغيل بعد التثبيت.
- تصبح حالة Runtime غير متسقة بعد تجربة فاشلة.

بعد إعادة التشغيل، شغّل من أول خلية. قد تختفي المتغيرات والملفات الناتجة من الجلسة السابقة.

إذا أعاد المتصفح الاتصال بالجلسة نفسها، فتحقق من حالة الخلايا قبل المتابعة. وعند الشك احفظ عملك وابدأ جلسة جديدة.

</td>
</tr>
</table>

## Safe operating rules | قواعد التشغيل الآمن

- Never mount Drive unless the instructor publishes a specific approved need. | لا تربط Drive ما لم تصدر المدربة حاجة معتمدة ومحددة.
- Never paste passwords, API keys or access tokens. | لا تلصق كلمات مرور أو مفاتيح API أو رموز وصول.
- Never disable checksum or data-contract checks. | لا تعطّل فحوص البصمة أو عقد البيانات.
- Never submit recovery examples as your own run. | لا تسلّم أمثلة الاستعادة بوصفها تشغيلك الشخصي.
- Keep `FAST_MODE=True` unless the daily guide explicitly allows an optional full run. | اترك `FAST_MODE=True` ما لم يسمح دليل اليوم بمسار كامل اختياري.
- Save actual files, not screenshots only. | احفظ الملفات الفعلية، لا لقطات الشاشة فقط.

## Quick troubleshooting | معالجة سريعة

| Problem | English action | الإجراء بالعربية |
|---|---|---|
| Runtime disconnected | Reopen the saved notebook and run from the first cell | افتح الدفتر المحفوظ وشغّل من أول خلية |
| Package conflict | Restart session and run setup first | أعد تشغيل الجلسة وشغّل الإعداد أولًا |
| Checksum mismatch | Restore the approved file; do not bypass the check | استرجع الملف المعتمد ولا تتجاوز الفحص |
| File not visible | Refresh the Files panel | حدّث لوحة Files |
| Download did not start | Use the file menu and download one file at a time | استخدم قائمة الملف ونزّل ملفًا واحدًا في كل مرة |
| Free quota unavailable | Save your work and retry later; do not purchase compute | احفظ عملك وأعد المحاولة لاحقًا؛ لا تشترِ موارد |

[GitHub guide | دليل GitHub](GITHUB_GUIDE.md) · [Troubleshooting | حل المشكلات](TROUBLESHOOTING.md) · [Colab FAQ](https://research.google.com/colaboratory/faq.html)