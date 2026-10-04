# GitHub Guide | دليل GitHub

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<div align="center">

**Browser-first workflow · No terminal required for the learner path**  
**مسار يعتمد على المتصفح · لا يحتاج المتدرب إلى Terminal**

[Course template](https://github.com/almiyead-rgb/sda-dsc-211-student-template) · [Final submission guide](SUBMISSION_GUIDE.md)

</div>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## What GitHub stores

GitHub is the permanent record of your project. It stores:

- Notebooks and source code.
- Reports and evidence files.
- Commit history.
- Automated check results.
- The final tag and exact commit SHA.

A Colab runtime is temporary. GitHub is where the instructor must be able to inspect the final version you submitted.

</td>
<td width="50%" valign="top" dir="rtl">

## ماذا يحفظ GitHub؟

GitHub هو السجل الدائم لمشروعك. يحفظ:

- الدفاتر والكود المصدري.
- التقارير وملفات الأدلة.
- سجل الـCommits.
- نتائج الفحوص الآلية.
- Tag النهائي وCommit SHA الدقيق.

Runtime في Colab مؤقت. أما GitHub فهو المكان الذي يجب أن تستطيع المدربة مراجعة النسخة النهائية المسلّمة من خلاله.

</td>
</tr>
</table>

## Create your repository from the template | أنشئ مستودعك من القالب

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Open the course template.
2. Select **Use this template → Create a new repository**.
3. Choose your own account as **Owner**.
4. Enter a neutral repository name, such as `tamweel-project-01`.
5. Follow the cohort visibility policy.
6. Select **Create repository**.
7. Confirm that the new URL contains your username and repository name.

Do not use **Fork** for the normal learner path unless the instructor explicitly requests it.

</td>
<td width="50%" valign="top" dir="rtl">

1. افتح قالب الدورة.
2. اختر **Use this template → Create a new repository**.
3. اختر حسابك في خانة **Owner**.
4. اكتب اسمًا محايدًا مثل `tamweel-project-01`.
5. اتبع سياسة إتاحة المستودع الخاصة بالدفعة.
6. اختر **Create repository**.
7. تأكد أن الرابط الجديد يحتوي اسم حسابك واسم المستودع.

لا تستخدم **Fork** في مسار المتدرب المعتاد إلا إذا طلبت المدربة ذلك صراحة.

</td>
</tr>
</table>

## Understand the repository folders | افهم مجلدات المستودع

| Folder | English purpose | الغرض بالعربية |
|---|---|---|
| `notebooks/` | Executed notebooks 00, 01–05 and 99 | الدفاتر المنفذة 00 و01–05 و99 |
| `artifacts/` | CSV, JSON and figures produced by the labs | ملفات CSV وJSON والرسوم الناتجة من اللابات |
| `reports/` | Decision Card, interpretation report, ensemble decision and Model Card | بطاقة القرار وتقرير التفسير وقرار التجميع وبطاقة النموذج |
| `submission/` | Final prediction file, manifest and delivery evidence | ملف التنبؤ النهائي والـManifest وأدلة التسليم |
| `presentation/` | Five-slide presentation source and PDF | مصدر العرض المكون من خمس شرائح وملف PDF |
| `tamweel/` | Reproducible inference code | كود الاستدلال القابل لإعادة التشغيل |
| `scripts/` | Setup, checks and rebuild utilities | أدوات الإعداد والفحص وإعادة البناء |
| `data/` | Synthetic course data and data contract | بيانات الدورة الاصطناعية وعقد البيانات |

## Upload files through the browser | ارفع الملفات من المتصفح

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Open the correct folder in your repository.
2. Select **Add file → Upload files**.
3. Drag the files or choose them from your device.
4. Review the destination path shown above the upload area.
5. Enter a clear commit message, such as `Complete Day 3 decision evidence`.
6. Commit the change.
7. Open the uploaded files and verify that they are readable.

Do not upload a ZIP as the only evidence. Keep the actual notebooks, reports and output files in their required folders.

</td>
<td width="50%" valign="top" dir="rtl">

1. افتح المجلد الصحيح داخل مستودعك.
2. اختر **Add file → Upload files**.
3. اسحب الملفات أو اخترها من جهازك.
4. راجع مسار الوجهة الظاهر أعلى منطقة الرفع.
5. اكتب رسالة Commit واضحة مثل `Complete Day 3 decision evidence`.
6. احفظ التغيير.
7. افتح الملفات المرفوعة وتأكد من أنها مقروءة.

لا ترفع ZIP بوصفه الدليل الوحيد. احتفظ بالدفاتر والتقارير وملفات المخرجات الفعلية داخل مجلداتها المطلوبة.

</td>
</tr>
</table>

## Save a notebook from Colab | احفظ دفترًا من Colab

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

### Recommended route

Download the executed `.ipynb` file, then upload it to `notebooks/` through the GitHub browser interface.

### Optional route

If **File → Save a copy in GitHub** is available:

- Confirm Owner.
- Confirm Repository.
- Confirm Branch.
- Confirm File path.
- Use a clear commit message.

Do not edit the same notebook in Colab and GitHub at the same time. Keep a local copy before resolving a conflict.

</td>
<td width="50%" valign="top" dir="rtl">

### المسار الموصى به

نزّل ملف `.ipynb` المنفذ، ثم ارفعه إلى `notebooks/` من واجهة GitHub في المتصفح.

### المسار الاختياري

إذا كان **File → Save a copy in GitHub** متاحًا:

- تأكد من Owner.
- تأكد من Repository.
- تأكد من Branch.
- تأكد من File path.
- استخدم رسالة Commit واضحة.

لا تعدل الدفتر نفسه في Colab وGitHub في الوقت نفسه. احتفظ بنسخة محلية قبل معالجة أي تعارض.

</td>
</tr>
</table>

## Read commits and the commit SHA | افهم الـCommit وSHA

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

A **commit** is a recorded project state. Each commit has a unique hexadecimal identifier called a **commit SHA**.

For final submission:

1. Finish all changes.
2. Run the final checks.
3. Create one final commit.
4. Open the commit page.
5. Copy the full 40-character SHA.
6. Record it in the private submission form.

A branch name such as `main` is not an immutable version identifier. The exact SHA is required.

</td>
<td width="50%" valign="top" dir="rtl">

الـ**Commit** هو حالة مسجلة من المشروع. ويحصل كل Commit على معرّف سداسي عشري فريد يسمى **Commit SHA**.

عند التسليم النهائي:

1. أكمل جميع التعديلات.
2. شغّل الفحوص النهائية.
3. أنشئ Commit نهائيًا واحدًا.
4. افتح صفحة الـCommit.
5. انسخ SHA الكامل المكون من 40 محرفًا.
6. سجله في نموذج التسليم الخاص.

اسم الفرع مثل `main` ليس معرّف نسخة ثابتًا. المطلوب هو SHA الدقيق.

</td>
</tr>
</table>

## Create the final tag | أنشئ Tag النهائي

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

Create the tag only after the final checked commit exists. Use the naming policy published for your cohort, for example:

```text
v1.0-final
```

Confirm that the tag points to the same commit SHA recorded in your submission. Do not move or recreate the tag after submission. If an approved resubmission is allowed, create a new commit and a new tag rather than rewriting the evaluated version.

</td>
<td width="50%" valign="top" dir="rtl">

أنشئ Tag بعد وجود الـCommit النهائي الذي اجتاز الفحص. استخدم سياسة التسمية المنشورة لدفعتك، مثل:

```text
v1.0-final
```

تأكد أن Tag يشير إلى Commit SHA نفسه المسجل في التسليم. لا تنقل Tag ولا تعِد إنشاءه بعد التسليم. وإذا سُمح بإعادة التسليم، فأنشئ Commit جديدًا وTag جديدًا بدل إعادة كتابة النسخة المقيمة.

</td>
</tr>
</table>

## Run GitHub Actions | شغّل GitHub Actions

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

1. Open the **Actions** tab.
2. Select **Final Project Check**.
3. Choose **Run workflow**.
4. Select the final branch.
5. Start the run.
6. Wait for the result.
7. Open the run and keep its URL.

A green check means the automated conditions passed. It does not award a grade, prove authorship or serve as a submission receipt.

If the free Actions quota is temporarily unavailable, follow the documented alternative announced by the instructor for the same exact commit SHA.

</td>
<td width="50%" valign="top" dir="rtl">

1. افتح تبويب **Actions**.
2. اختر **Final Project Check**.
3. اختر **Run workflow**.
4. اختر الفرع النهائي.
5. ابدأ التشغيل.
6. انتظر النتيجة.
7. افتح التشغيل واحتفظ برابطه.

تعني العلامة الخضراء أن الشروط الآلية نجحت. لكنها لا تمنح درجة ولا تثبت الملكية ولا تُعد إيصال استلام.

إذا تعذرت حصة Actions المجانية مؤقتًا، فاتبع المسار البديل الموثق الذي تعلنه المدربة على Commit SHA نفسه.

</td>
</tr>
</table>

## Public repository safety | أمان المستودع العام

Never publish:

- Passwords or tokens. | كلمات المرور أو الرموز.
- National IDs, phone numbers or private email addresses. | أرقام الهوية أو الهاتف أو البريد الخاص.
- Private grades or submission receipts. | الدرجات أو إيصالات التسليم الخاصة.
- Hidden labels or evaluator files. | التسميات المخفية أو ملفات المقيم.
- Employer or third-party confidential data. | بيانات جهة العمل أو بيانات سرية لطرف ثالث.
- Personal information inside notebook outputs or commit messages. | معلومات شخصية داخل مخرجات الدفاتر أو رسائل الـCommit.

## Final repository checklist | قائمة تحقق المستودع النهائي

- [ ] All required files are in the correct folders. | جميع الملفات المطلوبة في المجلدات الصحيحة.
- [ ] Executed notebooks include outputs. | الدفاتر المنفذة تتضمن المخرجات.
- [ ] Reports are complete and readable. | التقارير مكتملة ومقروءة.
- [ ] The repository contains no secrets or private data. | لا يحتوي المستودع أسرارًا أو بيانات خاصة.
- [ ] Notebook 99 completed. | اكتمل دفتر 99.
- [ ] Final Project Check passed or the approved alternative was recorded. | نجح الفحص النهائي أو سُجل البديل المعتمد.
- [ ] Final tag and SHA match. | Tag النهائي وSHA متطابقان.
- [ ] Submission was sent through the private channel. | أُرسل التسليم عبر القناة الخاصة.
- [ ] A receipt was retained. | تم الاحتفاظ بإيصال الاستلام.

[Colab guide | دليل Colab](COLAB_GUIDE.md) · [Final check guide | دليل الفحص النهائي](FINAL_CHECK_GUIDE.md) · [Submission guide | دليل التسليم](SUBMISSION_GUIDE.md)