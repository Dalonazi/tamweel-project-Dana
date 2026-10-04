# Troubleshooting Playbook | دليل استكشاف الأخطاء

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<div align="center">

**Diagnose first · Correct the source · Rerun from a clean state**  
**شخّص أولًا · صحح المصدر · أعد التشغيل من حالة نظيفة**

[Colab guide](COLAB_GUIDE.md) · [GitHub guide](GITHUB_GUIDE.md) · [Readiness guide](READINESS_GUIDE.md)

</div>

## First-response sequence | تسلسل المعالجة الأول

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

When an error appears:

1. Read the last red traceback line and the cell title.
2. Do not continue running later cells.
3. Confirm the approved notebook and repository URL.
4. Confirm the free CPU runtime.
5. Check whether setup completed successfully.
6. Save any learner text you wrote.
7. Apply the matching correction below.
8. Restart the session if instructed.
9. Run from the first cell.
10. Verify the regenerated evidence files.

Do not “fix” a failure by disabling checks, changing expected hashes or inserting fabricated outputs.

</td>
<td width="50%" valign="top" dir="rtl">

عند ظهور خطأ:

1. اقرأ آخر سطر أحمر في Traceback وعنوان الخلية.
2. لا تتابع تشغيل الخلايا اللاحقة.
3. تأكد من الدفتر المعتمد ورابط المستودع.
4. تأكد من اختيار CPU المجاني.
5. تحقق من اكتمال خلية الإعداد.
6. احفظ أي نص كتبته في إجابات المتدرب.
7. طبّق التصحيح المناسب أدناه.
8. أعد تشغيل الجلسة إذا طُلب ذلك.
9. شغّل من أول خلية.
10. تحقق من إعادة إنشاء ملفات الأدلة.

لا تعالج الفشل بتعطيل الفحوص أو تغيير البصمات المتوقعة أو إدخال مخرجات مصطنعة.

</td>
</tr>
</table>

## Colab and environment problems | مشكلات Colab والبيئة

| Symptom | Likely cause | English correction | التصحيح بالعربية |
|---|---|---|---|
| Runtime disconnected | Temporary hosted session ended | Reopen the saved notebook, select CPU and run from the first cell | افتح الدفتر المحفوظ، واختر CPU، وشغّل من أول خلية |
| Variables are undefined after reconnecting | Runtime memory was reset | Restart and use **Run all**; do not resume from a middle cell | أعد التشغيل واستخدم **Run all** ولا تبدأ من خلية وسطية |
| Package version conflict | A different version was imported before setup | Restart session, then run setup before importing any package | أعد تشغيل الجلسة ثم شغّل الإعداد قبل استيراد أي حزمة |
| Installation appears frozen | Large wheel download or temporary network delay | Wait several minutes; if no progress, save work and retry in a fresh session | انتظر عدة دقائق؛ وإذا لم يظهر تقدم فاحفظ عملك وأعد المحاولة في جلسة جديدة |
| Free runtime unavailable | Temporary Colab quota or capacity limit | Save work and retry later; do not purchase compute | احفظ عملك وأعد المحاولة لاحقًا؛ لا تشترِ موارد |
| Browser tab crashed | Local browser memory or extension conflict | Reopen in a fresh tab, close heavy tabs and rerun from the beginning | افتح الدفتر في تبويب جديد وأغلق التبويبات الثقيلة وأعد التشغيل من البداية |

## Source verification problems | مشكلات التحقق من المصدر

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

### `Checksum mismatch`

The downloaded or local file does not match the approved source.

**Action:**

1. Stop execution.
2. Reopen the released notebook.
3. Restore the original file from the approved repository.
4. Delete the mismatched local copy.
5. Run setup again.

Never update the expected checksum to match an unknown file.

### Missing verified support file

Use the setup cell to download the approved file. If repeated network failure prevents this, use the documented repository-ZIP fallback while preserving paths and filenames.

</td>
<td width="50%" valign="top" dir="rtl">

### `Checksum mismatch`

الملف المنزّل أو المحلي لا يطابق المصدر المعتمد.

**الإجراء:**

1. أوقف التنفيذ.
2. أعد فتح الدفتر المنشور.
3. استرجع الملف الأصلي من المستودع المعتمد.
4. احذف النسخة المحلية غير المطابقة.
5. أعد خلية الإعداد.

لا تغيّر البصمة المتوقعة لتطابق ملفًا مجهولًا.

### ملف دعم موثق مفقود

استخدم خلية الإعداد لتنزيل الملف المعتمد. وإذا منع فشل الشبكة المتكرر ذلك، فاستخدم مسار ZIP الموثق مع الحفاظ على المسارات وأسماء الملفات.

</td>
</tr>
</table>

## Notebook execution problems | مشكلات تنفيذ الدفتر

| Symptom | Likely cause | English correction | التصحيح بالعربية |
|---|---|---|---|
| A later cell says a variable is missing | Cells ran out of order or runtime restarted | Run from the first cell using **Run all** | شغّل من أول خلية باستخدام **Run all** |
| Notebook completes but learner response is blank | Response field was not edited or its export cell was not rerun | Write your response, rerun the response and export cells | اكتب إجابتك ثم أعد خلايا الإجابة والتصدير |
| `ASSESSMENT_MODE` rejects recovery data | Example output is not acceptable for submission | Return to live execution and regenerate real project evidence | ارجع إلى التشغيل الفعلي وأعد إنشاء أدلة مشروعك |
| Full mode takes too long | Optional settings exceed the free-runtime target | Return to `FAST_MODE=True` | أعد الإعداد إلى `FAST_MODE=True` |
| Figure does not appear | Plot cell did not complete or output was cleared | Rerun the relevant cell after its prerequisites | أعد الخلية بعد تشغيل الخلايا السابقة المطلوبة |
| Unexpected result after manual edits | Core code or fixed policy was changed | Restore the approved notebook and modify learner fields only | استرجع الدفتر المعتمد وعدّل حقول المتدرب فقط |

## Data and validation problems | مشكلات البيانات والتحقق

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

### Missing or extra columns

Compare the input with the published data contract. Do not rename or manufacture columns to force execution. Restore the approved synthetic dataset.

### Duplicate or missing `application_id`

Stop submission generation. Rebuild predictions from the approved challenge features and verify one row per identifier.

### Leakage audit fails

Remove the prohibited feature from the model path and rerun validation. Do not hide the audit result.

### Customer overlap or time-order failure

Restore the approved split logic. A random split is not an acceptable substitute for the required time/customer validation.

</td>
<td width="50%" valign="top" dir="rtl">

### أعمدة مفقودة أو إضافية

قارن المدخل بعقد البيانات المنشور. لا تغيّر أسماء الأعمدة ولا تنشئ أعمدة مصطنعة لإجبار التنفيذ. استرجع مجموعة البيانات الاصطناعية المعتمدة.

### تكرار أو فقدان `application_id`

أوقف إنشاء التسليم. أعد بناء التنبؤات من خصائص التحدي المعتمدة وتحقق من وجود صف واحد لكل معرّف.

### فشل تدقيق التسرب

أزل الخاصية المحظورة من مسار النموذج وأعد التحقق. لا تخفِ نتيجة التدقيق.

### تداخل العملاء أو فشل ترتيب الزمن

استرجع منطق التقسيم المعتمد. لا يُقبل التقسيم العشوائي بديلًا عن التحقق المطلوب الذي يراعي الزمن والعملاء.

</td>
</tr>
</table>

## SHAP and calibration problems | مشكلات SHAP والمعايرة

| Symptom | Likely cause | English correction | التصحيح بالعربية |
|---|---|---|---|
| SHAP import or runtime failure | Package/runtime mismatch or temporary resource issue | Restart, rerun setup and use the pinned versions | أعد التشغيل ونفّذ الإعداد واستخدم الإصدارات المثبتة |
| `USE_SHAP_EXAMPLE=True` appears | Recovery example mode was selected | Use it only for learning; disable it and create live evidence before submission | استخدمه للتعلم فقط ثم عطّله وأنشئ أدلة تشغيل فعلية قبل التسليم |
| SHAP contributions do not sum as expected | Probability and raw-margin units were mixed | Read the day-four unit explanation and compare in log-odds | راجع شرح الوحدات في اليوم الرابع وقارن بوحدة log-odds |
| Calibration result worsens | Calibration is not guaranteed to improve every metric | Report the measured result honestly; do not force a positive conclusion | وثق النتيجة المقاسة بصدق ولا تفرض استنتاجًا إيجابيًا |
| ECE changes with bin count | ECE depends on binning | Use the course configuration and document the limitation | استخدم إعداد الدورة ووثق هذا القيد |

## File download and upload problems | مشكلات تنزيل الملفات ورفعها

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

### The notebook says the file was created, but I cannot find it

1. Open the Colab **Files** panel.
2. Select refresh.
3. Open the exact folder printed by the notebook.
4. Use the file menu and select **Download**.
5. Confirm the file exists on your device.

A success message in a cell does not prove that the browser download completed.

### I uploaded to the wrong repository

Download a local copy immediately, open the correct repository and upload it to the correct folder. Verify Owner, Repository and path before committing.

### GitHub rejects a large file

Do not remove required evidence. Confirm whether the file belongs in the project and use the provided compact export. Contact the instructor through the private support channel if a required generated file exceeds GitHub limits.

</td>
<td width="50%" valign="top" dir="rtl">

### يذكر الدفتر أن الملف أُنشئ لكنني لا أجده

1. افتح لوحة **Files** في Colab.
2. اضغط زر التحديث.
3. افتح المسار الدقيق الذي طبعه الدفتر.
4. افتح قائمة الملف واختر **Download**.
5. تأكد من وجود الملف على جهازك.

رسالة النجاح داخل الخلية لا تثبت أن تنزيل المتصفح اكتمل.

### رفعت الملف إلى مستودع خاطئ

نزّل نسخة محلية فورًا، وافتح المستودع الصحيح، وارفعها إلى المجلد الصحيح. راجع Owner وRepository والمسار قبل الحفظ.

### رفض GitHub ملفًا كبيرًا

لا تحذف الأدلة المطلوبة. تحقق أن الملف جزء مطلوب من المشروع واستخدم التصدير المضغوط المرفق. تواصل عبر قناة الدعم الخاصة إذا تجاوز ملف مطلوب ناتج حدود GitHub.

</td>
</tr>
</table>

## GitHub Actions problems | مشكلات GitHub Actions

| Status | English meaning and action | المعنى والإجراء بالعربية |
|---|---|---|
| Yellow / queued | The run is waiting for a runner; wait before retrying | التشغيل ينتظر Runner؛ انتظر قبل إعادة المحاولة |
| Red / failed | Open the failed job and first failed step; correct the source file | افتح المهمة الفاشلة وأول خطوة فاشلة وصحح الملف الأصلي |
| Cancelled | A newer run or concurrency rule replaced it | أُلغي بسبب تشغيل أحدث أو قاعدة تزامن |
| No workflow button | Workflow may not exist on the selected branch | تأكد من الفرع ووجود ملف Workflow |
| Quota unavailable | Use the documented private alternative on the same exact SHA | استخدم البديل الخاص الموثق على SHA نفسه |

Do not repeatedly rerun an unchanged failing workflow. Correct the root cause first.  
لا تكرر تشغيل Workflow فاشل دون تغيير؛ صحح السبب الجذري أولًا.

## Final-check and submission problems | مشكلات الفحص والتسليم

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

### Notebook 99 reports missing files

Correct the original repository folders. Do not create empty placeholder files merely to satisfy the filename check.

### Manifest hash mismatch

Regenerate the manifest after the final files are frozen. Do not edit a hashed file after generating the manifest without rebuilding it.

### Tag and SHA do not match

Create or correct the final tag so it points to the exact submitted commit. Do not move an evaluated tag after submission.

### I submitted the wrong version

Follow the written resubmission policy. Use a new commit, new tag and new private receipt. Keep the earlier evaluated version intact.

</td>
<td width="50%" valign="top" dir="rtl">

### يذكر دفتر 99 وجود ملفات مفقودة

صحح المجلدات الأصلية في المستودع. لا تنشئ ملفات فارغة لمجرد اجتياز فحص الاسم.

### عدم تطابق بصمات Manifest

أعد توليد Manifest بعد تثبيت الملفات النهائية. لا تعدّل ملفًا مشمولًا بالبصمة بعد إنشاء Manifest دون إعادة بنائه.

### Tag وSHA غير متطابقين

أنشئ Tag النهائي أو صححه ليشير إلى Commit المسلّم نفسه. لا تنقل Tag المقيم بعد التسليم.

### سلّمت نسخة خاطئة

اتبع سياسة إعادة التسليم المكتوبة. استخدم Commit جديدًا وTag جديدًا وإيصالًا خاصًا جديدًا، وأبقِ النسخة المقيمة السابقة كما هي.

</td>
</tr>
</table>

## What to include in a private support request | ماذا ترسل في طلب الدعم الخاص؟

Include:

- Cohort Code and Student Code. | رمز الدفعة ورمز المتدرب.
- Notebook name and section title. | اسم الدفتر وعنوان القسم.
- Exact error text or screenshot with private data removed. | نص الخطأ أو لقطة بعد إزالة البيانات الخاصة.
- Whether you used CPU and `FAST_MODE=True`. | هل استخدمت CPU و`FAST_MODE=True`.
- The last step that completed successfully. | آخر خطوة اكتملت بنجاح.
- Repository URL and commit SHA when relevant. | رابط المستودع وSHA عند الحاجة.

Do not send passwords, tokens or hidden data.  
لا ترسل كلمات مرور أو رموز وصول أو بيانات مخفية.