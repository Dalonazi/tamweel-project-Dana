# Administrative Requirements | المتطلبات الإدارية

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Purpose

These requirements define how the learner repository is organised, identified, documented, submitted and discussed. They protect the learner, the instructor and the integrity of the assessment record, while ensuring that every project is professionally publishable on GitHub.

</td>
<td width="50%" valign="top" dir="rtl">

## الغرض

تحدد هذه المتطلبات كيفية تنظيم مستودع المتدرب وتعريفه وتوثيقه وتسليمه ومناقشته. وهي تحمي المتدرب والمدربة وسلامة سجل التقييم، وتضمن أن يكون كل مشروع قابلًا للنشر المهني على GitHub.

</td>
</tr>
</table>

## Administrative acceptance matrix | مصفوفة القبول الإداري

| Code | English requirement | المتطلب بالعربية | Required evidence |
|---|---|---|---|
| A1 | Create one learner repository from the official template and keep the published folder structure unless a documented technical reason requires a change. | أنشئ مستودع متدرب واحدًا من القالب الرسمي، وحافظ على بنية المجلدات المنشورة ما لم توجد حاجة تقنية موثقة للتغيير. | repository URL, readable structure |
| A2 | Create and activate a GitHub account before the course begins if you do not already have one. Confirm that you can sign in, create repositories and push or upload files. | أنشئ حسابًا في GitHub وفعّله قبل بدء الدورة إذا لم يكن لديك حساب مسبقًا، وتأكد من قدرتك على تسجيل الدخول وإنشاء المستودعات ورفع الملفات أو دفعها. | active GitHub account, repository creation test |
| A3 | Use a cohort/student code in the public repository. Do not publish national ID, private email, phone number, grade, receipt or other unnecessary personal data. | استخدم رمز الدفعة أو المتدرب في المستودع العام. لا تنشر رقم الهوية أو البريد الخاص أو الهاتف أو الدرجة أو إيصال التسليم أو أي بيانات شخصية غير لازمة. | public-repository review |
| A4 | Add a clear, complete and professional repository description that states the project purpose, scope and expected output. | أضف وصفًا واضحًا وشاملًا ومهنيًا للمستودع يبيّن هدف المشروع ونطاقه والمخرج المتوقع منه. | repository description |
| A5 | Maintain a professional `README.md` that explains the project idea, problem, architecture, data, environment setup, execution steps, outputs, limitations and usage instructions. | حافظ على ملف `README.md` احترافي يشرح فكرة المشروع والمشكلة والمعمارية والبيانات وتجهيز البيئة وخطوات التشغيل والمخرجات والقيود وطريقة الاستخدام. | README review |
| A6 | Keep `README.md`, executed notebooks, reports, artifacts, model files, `submission.csv`, `metrics.json` and the final presentation accessible from clear links. | اجعل `README.md` والدفاتر المنفذة والتقارير والأدلة وملفات النموذج و`submission.csv` و`metrics.json` والعرض النهائي قابلة للوصول من روابط واضحة. | navigation check |
| A7 | Provide technical documentation appropriate to the project, including data roles, modelling decisions, validation design, package versions, seeds, limitations and reproducibility instructions. | قدم توثيقًا تقنيًا مناسبًا للمشروع، يشمل أدوار البيانات وقرارات النمذجة وتصميم التحقق وإصدارات الحزم والبذور والقيود وتعليمات إعادة الإنتاج. | technical documentation, provenance files |
| A8 | Apply Git version-control good practices: use meaningful commits, avoid replacing the entire project without explanation, preserve important milestones and do not rewrite the assessed history. | طبّق أفضل الممارسات في إدارة الإصدارات باستخدام Git: استخدم رسائل Commit واضحة، ولا تستبدل المشروع كاملًا دون توضيح، واحتفظ بالمراحل المهمة، ولا تعِد كتابة السجل الذي جرى تقييمه. | commit history, final tag |
| A9 | Document sources, material changes and any approved recovery output used during learning. Clearly disclose reused code, external references and assistance that materially affected the project. | وثّق المصادر والتغييرات الجوهرية وأي مخرجات استعادة معتمدة استُخدمت أثناء التعلم، وأفصح بوضوح عن الأكواد المعاد استخدامها والمراجع الخارجية وأي مساعدة أثرت جوهريًا في المشروع. | README, references, disclosures |
| A10 | State the training programme and course code in the repository, including `SDA-DSC-211 — Advanced Machine Learning Methods | أساليب تعلم الآلة المتقدمة`. | أشر داخل المستودع إلى البرنامج التدريبي ورمز الدورة، بما في ذلك `SDA-DSC-211 — Advanced Machine Learning Methods | أساليب تعلم الآلة المتقدمة`. | README or project metadata |
| A11 | Add the SDAIA Academy GitHub link when contextually appropriate, without presenting the learner repository as an official SDAIA repository or using protected branding without approval. | أضف رابط حساب أكاديمية سدايا على GitHub عند ملاءمة السياق، من دون الإيحاء بأن مستودع المتدرب مستودع رسمي لسدايا أو استخدام هوية محمية دون موافقة. | README reference and disclaimer |
| A12 | Complete the required Decision Card, Interpretability Report, Ensemble Decision and Model Card using evidence from your own executed project. | أكمل بطاقة القرار وتقرير التفسير وقرار التجميع وبطاقة النموذج باستخدام أدلة مشروعك الذي نفذته بنفسك. | four completed reports |
| A13 | Prepare a five-slide presentation and export it to PDF using any free tool. The presentation must match the exact final repository version. | أعد عرضًا من خمس شرائح وصدّره إلى PDF باستخدام أي أداة مجانية. يجب أن يطابق العرض النسخة النهائية الدقيقة من المستودع. | presentation PDF, matching metrics |
| A14 | Run the final check, commit all final files, create the final tag, record the full commit SHA and preserve the generated manifest and bundle. | شغّل الفحص النهائي، ثم نفّذ Commit لجميع الملفات، وأنشئ Tag نهائيًا، وسجّل Commit SHA كاملًا، واحتفظ بالـmanifest والحزمة الناتجة. | successful check, tag, SHA, manifest |
| A15 | Submit through the private channel approved for the cohort and retain the timestamped receipt or confirmation. Public issues are not a submission channel. | سلّم عبر القناة الخاصة المعتمدة للدفعة، واحتفظ بإيصال أو تأكيد مؤرخ. لا تُعد Issues العامة قناة تسليم. | private receipt ID or confirmation |
| A16 | Follow the written cohort deadline and resubmission policy issued by the instructor in the approved private channel. A verbal announcement may explain the process but must not be the only record. | التزم بموعد الدفعة وسياسة إعادة التسليم المكتوبين في القناة الخاصة المعتمدة. يمكن للشرح الشفهي توضيح الإجراء، لكنه لا يكون السجل الوحيد. | cohort notice, submission timestamp |
| A17 | Keep the final repository available for review until grades and appeals are closed. Do not rewrite the submitted tag or force-push the assessed commit. | أبقِ المستودع النهائي متاحًا للمراجعة حتى إغلاق الدرجات والاعتراضات. لا تعد كتابة Tag المسلّم ولا تستخدم Force Push على Commit المقيم. | immutable tag, accessible commit |
| A18 | Use only content you are permitted to publish. Do not upload confidential employer data, third-party personal data, credentials or copyrighted material without permission. | استخدم فقط محتوى مسموحًا بنشره. لا ترفع بيانات جهة عمل سرية أو بيانات شخصية للغير أو بيانات اعتماد أو مواد محمية دون إذن. | repository privacy review |
| A19 | Attend the project defence and answer questions using your own repository evidence. Inability to explain a key decision may reduce the relevant criterion score. | احضر مناقشة المشروع وأجب باستخدام أدلة مستودعك. قد يؤدي عدم القدرة على شرح قرار أساسي إلى خفض درجة المعيار المرتبط. | presentation and oral defence |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Course evaluation at the start of the final day

A course-evaluation form will be shared at the beginning of the final training day by the authorised SDAIA representative or through the approved SDAIA channel.

Learners are expected to complete the evaluation professionally and independently. This course-evaluation form is separate from the project score and does not replace the project submission, final presentation or defence.

</td>
<td width="50%" valign="top" dir="rtl">

## تقييم الدورة في بداية اليوم الأخير

سيتم مشاركة نموذج تقييم الدورة في بداية اليوم التدريبي الأخير من قبل ممثل سدايا المخوّل أو عبر القناة المعتمدة لدى سدايا.

يتوقع من المتدرب تعبئة التقييم بمهنية واستقلالية. ويعد تقييم الدورة منفصلًا عن درجة المشروع، ولا يحل محل تسليم المشروع أو العرض النهائي أو المناقشة.

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Assessment structure

- Project technical and administrative requirements: **90 points**.
- Final presentation and defence: **10 points**.
- Total: **100 points**.
- Pass: **70 or more**.
- Distinction: **95 or more**.

The project is assessed through the learner's GitHub repository and the exact submitted version. The final score is compared before display rounding. A score of `69.99` does not become a pass, and `94.99` does not become a distinction through display rounding.

</td>
<td width="50%" valign="top" dir="rtl">

## هيكل التقييم

- المتطلبات التقنية والإدارية للمشروع: **90 نقطة**.
- العرض والمناقشة النهائية: **10 نقاط**.
- الإجمالي: **100 نقطة**.
- النجاح: **70 فأعلى**.
- التميز: **95 فأعلى**.

يُقيَّم المشروع من خلال مستودع المتدرب على GitHub والنسخة الدقيقة التي جرى تسليمها. وتُقارن الدرجة الفعلية قبل تقريب العرض؛ فلا تتحول `69.99` إلى نجاح، ولا تتحول `94.99` إلى تميز بسبب تقريب الرقم المعروض.

</td>
</tr>
</table>

## GitHub community engagement | التفاعل المهني مع مجتمع GitHub

The following practices are strongly encouraged as professional-development activities. They support the Saudi technical ecosystem, but they are **not used as automatic scoring requirements** unless a written cohort notice explicitly states otherwise.

تشجَّع الممارسات التالية بوصفها أنشطة تطوير مهني تسهم في دعم المجتمع التقني السعودي، لكنها **لا تستخدم متطلبات آلية للدرجات** ما لم يرد نص مكتوب بخلاف ذلك ضمن إعلان الدفعة.

1. Add Stars to high-quality Saudi projects that you genuinely find useful. | أضف Stars للمشاريع السعودية عالية الجودة التي تراها مفيدة فعلًا.
2. Follow relevant Saudi technical accounts and repositories. | تابع الحسابات والمستودعات التقنية السعودية ذات الصلة.
3. Contribute responsibly to suitable open-source projects. | ساهم بمسؤولية في المشاريع مفتوحة المصدر المناسبة.
4. Use Forks, Pull Requests and Issues when there is a legitimate technical need and you can add value. | استخدم Fork وPull Requests وIssues عند وجود حاجة تقنية حقيقية وقدرة على تقديم قيمة.
5. Share strong projects with the technical community while protecting privacy, intellectual property and institutional restrictions. | شارك المشاريع المتميزة مع المجتمع التقني مع حماية الخصوصية والملكية الفكرية والقيود المؤسسية.

## Administrative integrity gates | بوابات النزاهة الإدارية

The submission is returned for correction before grading when any of the following prevents reliable review:

يُعاد التسليم للتصحيح قبل التقييم عندما يمنع أحد الآتي المراجعة الموثوقة:

1. Repository, tag or exact SHA is missing or inaccessible. | المستودع أو Tag أو SHA الدقيق مفقود أو غير متاح.
2. The submitted tag does not point to the recorded SHA. | لا يشير Tag المسلّم إلى SHA المسجل.
3. Required project files, technical documentation or reports are missing. | ملفات المشروع أو التوثيق التقني أو التقارير الإلزامية ناقصة.
4. The README does not explain how to understand and run the project. | لا يوضح README كيفية فهم المشروع وتشغيله.
5. The learner publishes private personal data, grades, receipts, secrets or challenge labels. | ينشر المتدرب بيانات شخصية خاصة أو درجات أو إيصالات أو أسرارًا أو تسميات التحدي.
6. The presentation describes results that do not match the submitted repository. | يعرض التقديم نتائج لا تطابق المستودع المسلّم.
7. The submission uses a public issue or an unapproved channel instead of the private submission record. | يستخدم التسليم Issue عامة أو قناة غير معتمدة بدل سجل التسليم الخاص.
8. The repository presents itself as an official SDAIA repository without written authorisation. | يقدم المستودع نفسه بوصفه مستودعًا رسميًا لسدايا دون تفويض مكتوب.
