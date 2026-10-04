# Final Project Check Guide | دليل الفحص النهائي للمشروع

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<div align="center">

**SDA-DSC-211 · Tamweel Lite · Technical preflight, not a grade or receipt | فحص تقني تمهيدي، وليس درجة أو إيصالًا**

[Open Notebook 99 in Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/99_final_submission_check.ipynb) · [Submission guide](SUBMISSION_GUIDE.md) · [Day 5 guide](DAY5_GUIDE.md)

</div>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Notebook 99 · Final project self-check

<p><strong>SDA-DSC-211 · Tamweel Lite · Prepared and delivered by Meaad Al-Marri | ميعاد المري</strong></p>
<p>Use a fresh free-CPU session to inspect <strong>your own project snapshot</strong>. Run the cells in order. The checker reports the status of each required file and executes the applications in isolated workspaces; it does not award an automatic grade.</p>
<p>The assessment framework is 90 technical/administrative points plus 10 presentation points. Passing starts at 70 and distinction at 95 before rounding, but the instructor reviews interpretation, authenticity and presentation.</p>
<p><strong>Security boundary:</strong> upload only files you know. Do not connect Drive, accounts, secrets or private data. The notebook executes project code. A successful technical check is not a submission receipt.</p>
<p><a href="https://github.com/almiyead-rgb/sda-dsc-211-student-template/blob/main/FINAL_CHECK_GUIDE.md">Final-check guide</a></p>

</td>
<td width="50%" valign="top" dir="rtl">

## دفتر 99 · الفحص الذاتي النهائي للمشروع

<p><strong>SDA-DSC-211 · Tamweel Lite · إعداد وتقديم ميعاد المري | Meaad Al-Marri</strong></p>
<p>استخدم جلسة CPU مجانية جديدة لفحص <strong>لقطة مشروعك أنت</strong>. شغّل الخلايا بالترتيب. يعرض الفاحص حالة كل ملف مطلوب ويشغّل التطبيقات في مساحات عمل معزولة، لكنه لا يمنح درجة تلقائية.</p>
<p>إطار التقييم 90 نقطة تقنية وإدارية و10 نقاط للعرض. يبدأ النجاح من 70 والتميز من 95 قبل التقريب، بينما تراجع المدربة التفسير وأصالة العمل والعرض.</p>
<p><strong>حد الأمان:</strong> ارفع الملفات التي تعرفها فقط. لا تربط Drive أو الحسابات أو الأسرار أو البيانات الخاصة. يشغّل الدفتر شيفرة المشروع. نجاح الفحص التقني ليس إيصال تسليم.</p>
<p><a href="https://github.com/almiyead-rgb/sda-dsc-211-student-template/blob/main/FINAL_CHECK_GUIDE.md">دليل الفحص النهائي</a></p>

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## 1. Identify the exact project snapshot

<p>For a public repository, enter <code>owner/repository</code> and the full 40-character commit SHA. Never use a moving branch name such as <code>main</code>. For a local project, leave both fields blank and provide one complete project ZIP in the upload step.</p>
<p>Do not upload the Day 5 ZIP by itself. The snapshot must also contain executed notebooks, imported evidence from Days 1–4, the presentation and the template files required by the submission contract.</p>
<p>The checker works on a fixed snapshot and builds a manifest in a temporary copy; it does not change GitHub. After a successful check, upload the extracted final files to your repository, rerun Final Project Check, and record the final SHA and tag through the private submission channel. Any schedule is the one announced by the instructor for your cohort.</p>

</td>
<td width="50%" valign="top" dir="rtl">

## 1. حدّد لقطة المشروع بدقة

<p>للمستودع العام اكتب <code>owner/repository</code> وSHA كاملًا من 40 خانة. لا تستخدم اسم فرع متحرك مثل <code>main</code>. للمشروع المحلي اترك الحقلين فارغين وقدّم ZIP كاملًا واحدًا في خطوة الرفع.</p>
<p>لا ترفع ZIP اليوم الخامس وحده. يجب أن تضم اللقطة أيضًا الدفاتر المنفذة، والأدلة المستوردة من الأيام 1–4، والعرض، وملفات القالب المطلوبة في عقد التسليم.</p>
<p>يعمل الفاحص على لقطة ثابتة ويبني manifest في نسخة مؤقتة؛ ولا يغير GitHub. بعد نجاح الفحص ارفع الملفات النهائية المستخرجة إلى مستودعك، ثم أعد Final Project Check وسجّل SHA وtag النهائيين عبر قناة التسليم الخاصة. يعتمد الموعد على ما تعلنه المدربة لدفعتك.</p>

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## 2. Prepare verified checking tools

<p>The setup cell downloads the course checking tools from one pinned revision, verifies the SHA-256 of every source, installs the free pinned environment and enables assessment mode with two CPU threads.</p>
<p>Wait until <code>CHECK_TOOLS_READY</code> appears. Never bypass a source checksum mismatch. Each application is later executed in a separate process and workspace; the checker redirects only the documented project directory and does not rewrite learner answers or training logic.</p>

</td>
<td width="50%" valign="top" dir="rtl">

## 2. جهّز أدوات فحص موثقة

<p>تنزّل خلية الإعداد أدوات فحص الدورة من مراجعة مثبتة واحدة، وتتحقق من SHA-256 لكل مصدر، وتثبت البيئة المجانية المقيدة، وتفعل وضع التقييم بخيطي CPU.</p>
<p>انتظر ظهور <code>CHECK_TOOLS_READY</code>. لا تتجاوز عدم تطابق بصمة المصدر. يُشغّل كل تطبيق لاحقًا في عملية ومجلد مستقلين؛ ويعيد الفاحص توجيه مجلد المشروع الموثق فقط دون إعادة كتابة إجابات المتدرب أو منطق التدريب.</p>

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## 3. Read the project snapshot safely

<p>If repository fields are blank, choose exactly one project ZIP. Do not enter a password or token. For a public repository, the notebook downloads the archive for the exact SHA.</p>
<p>The reader limits the archive to 100 MiB, validates path names and safe extraction rules, and prints the archive SHA-256. Confirm that the displayed project root is your intended snapshot before continuing.</p>

</td>
<td width="50%" valign="top" dir="rtl">

## 3. اقرأ لقطة المشروع بأمان

<p>إذا كانت حقول المستودع فارغة فاختر ZIP مشروع واحدًا فقط. لا تدخل كلمة مرور أو token. للمستودع العام ينزّل الدفتر الأرشيف الخاص بالـSHA المحدد.</p>
<p>يحد القارئ حجم الأرشيف بـ100 MiB، ويتحقق من أسماء المسارات وقواعد الفك الآمن، ثم يعرض SHA-256 للأرشيف. تأكد أن جذر المشروع المعروض هو اللقطة المقصودة قبل المتابعة.</p>

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## 4. Run the check and read every finding

<p>The final checker validates required files, hashes, prediction structure, the 12% batch policy and the final manifest. It then executes readiness and Days 1–5 in clean processes and workspaces.</p>
<p>Read the <strong>File / How to fix</strong> table. File presence does not prove that an interpretation is correct; the instructor reviews meaning and authenticity. Empty responses, recovery examples and labelled educational examples do not satisfy final readiness.</p>
<p><code>READY FOR FINAL SUBMISSION | جاهز للتسليم النهائي</code> means only that the declared technical checks passed. <code>NEEDS_WORK</code> is actionable: correct the original project files and rerun the complete check.</p>

</td>
<td width="50%" valign="top" dir="rtl">

## 4. شغّل الفحص واقرأ كل ملاحظة

<p>يتحقق الفاحص النهائي من الملفات المطلوبة والبصمات وبنية التنبؤات وسياسة الدفعة 12% والـmanifest النهائي. ثم يشغّل الاستعداد والأيام 1–5 في عمليات ومساحات عمل نظيفة.</p>
<p>اقرأ جدول <strong>File / How to fix</strong>. وجود الملف لا يثبت صحة التفسير؛ تراجع المدربة المعنى وأصالة العمل. لا تحقق الإجابات الفارغة أو مخرجات التعافي أو الأمثلة التعليمية الموسومة الجاهزية النهائية.</p>
<p>تعني <code>READY FOR FINAL SUBMISSION | جاهز للتسليم النهائي</code> نجاح الفحوص التقنية المعلنة فقط. أما <code>NEEDS_WORK</code> فهي نتيجة قابلة للتنفيذ: صحح ملفات المشروع الأصلية ثم أعد الفحص الكامل.</p>

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## 5. Save the report and final bundle

<p>The report is always copied to <code>Files → final_check_downloads/self_check_report.json</code>. The final project bundle is copied and downloaded only when the checker reports readiness.</p>
<p>If the browser download does not start, refresh the Files pane and download one file at a time. Confirm that the files exist on your device before closing the session. After any project change, rerun the check because the manifest and file hashes are snapshot-specific.</p>
<p>The course-tool revision is not your submission SHA. Extract the final bundle, upload the actual files to your repository, run the repository Final Project Check, create <code>final-submission</code> on the same commit, and record the SHA/tag privately. Do not publish personal data or submission details in public Issues.</p>

</td>
<td width="50%" valign="top" dir="rtl">

## 5. احفظ التقرير والحزمة النهائية

<p>يُنسخ التقرير دائمًا إلى <code>Files → final_check_downloads/self_check_report.json</code>. ولا تُنسخ الحزمة النهائية وتُنزّل إلا عندما يعلن الفاحص الجاهزية.</p>
<p>إذا لم يبدأ تنزيل المتصفح فحدّث لوحة Files ونزّل ملفًا واحدًا في كل مرة. تأكد من وجود الملفات على جهازك قبل إغلاق الجلسة. بعد أي تعديل في المشروع أعد الفحص لأن manifest وبصمات الملفات تخص لقطة محددة.</p>
<p>مراجعة أدوات الدورة ليست SHA تسليمك. فك الحزمة النهائية وارفع الملفات الفعلية إلى مستودعك، وشغّل Final Project Check، وأنشئ <code>final-submission</code> على commit نفسه، ثم سجّل SHA/tag بصورة خاصة. لا تنشر البيانات الشخصية أو تفاصيل التسليم في Issues عامة.</p>

</td>
</tr>
</table>

## What each gate proves | معنى كل بوابة

| Gate | What it proves | ما تثبته |
|---|---|---|
| Environment Check | Template files, unit tests and local links are technically sound; it does not prove learner completion | سلامة ملفات القالب والاختبارات والروابط المحلية؛ ولا يثبت اكتمال عمل المتدرب |
| Notebook Smoke Test | Applications execute in isolated workspaces without requiring completed learner prose | إمكانية تشغيل التطبيقات في مساحات معزولة دون اشتراط اكتمال النصوص |
| Final Project Check | Required project files, fresh execution, predictions, policy and manifest satisfy the declared technical contract | توافق الملفات والتشغيل الجديد والتنبؤات والسياسة والـmanifest مع العقد التقني المعلن |
| Instructor review | Interpretation, authenticity, presentation and final score | التفسير وأصالة العمل والعرض والدرجة النهائية |

## Public and private repositories | المستودعات العامة والخاصة

GitHub-hosted validation uses the standard `ubuntu-latest` runner for public repositories. In a private repository, use Notebook 99 on free Colab to avoid consuming a private Actions quota. No GPU, payment card or paid service is required.

يستخدم التحقق المستضاف في GitHub مشغل `ubuntu-latest` القياسي للمستودعات العامة. في المستودع الخاص استخدم دفتر 99 على Colab المجاني لتجنب استهلاك حصة Actions الخاصة. لا تحتاج إلى GPU أو بطاقة دفع أو خدمة مدفوعة.

## Local execution | التشغيل المحلي

```bash
python -m pip install -r requirements-colab.txt -r requirements-check.txt -c constraints.txt
python scripts/final_check.py --root . --output .check-output --prepare
python -m tamweel.inference --input data/tamweel_challenge.csv --output .check-output/probabilities.csv
```

The inference interface returns only `application_id,probability`. Apply the decision policy once after collecting the full batch. Do not compute a challenge performance score from the public unlabelled data.

تعيد واجهة التنبؤ `application_id,probability` فقط. طبّق سياسة القرار مرة واحدة بعد جمع الدفعة كاملة. لا تحسب درجة أداء للتحدي من البيانات العامة غير المعلّمة.

[Return to the learner guide](STUDENT_GUIDE.md) · [Open Notebook 99](notebooks/99_final_submission_check.ipynb)
