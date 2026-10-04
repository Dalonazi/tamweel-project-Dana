# Private submission registry specification | مواصفات سجل التسليم الخاص

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

## Purpose | الغرض

The registry is the authoritative private record of what was submitted, when it was received and which exact repository version was evaluated. Public issues, chat messages and mutable branch links are not sufficient submission records.

السجل هو المرجع الخاص المعتمد لما تم تسليمه ووقت استلامه والنسخة الدقيقة التي تم تقييمها. لا تكفي Issues العامة أو رسائل المحادثة أو روابط الفروع القابلة للتغيير بوصفها سجلًا نهائيًا.

## Required fields | الحقول الإلزامية

| Field | Rule | القاعدة |
|---|---|---|
| `cohort_code` | Instructor-issued cohort identifier | رمز الدفعة الصادر من المدربة |
| `student_code` | Public-safe identifier | معرف لا يكشف بيانات شخصية |
| `full_name` | Private record only | يظهر في السجل الخاص فقط |
| `github_username` | Exact account owner | اسم حساب GitHub الدقيق |
| `repository_url` | Repository evaluated | رابط المستودع الذي سيُقيّم |
| `final_tag` | Immutable final tag | Tag نهائي غير قابل لإعادة الاستخدام |
| `exact_commit_sha` | Full 40-character SHA | SHA كامل من 40 محرفًا |
| `final_check_url` | Workflow or approved alternate check | رابط الفحص أو المسار البديل المعتمد |
| `presentation_file` | Final five-slide PDF | العرض النهائي من خمس شرائح |
| `declaration` | Student confirms final version and authorship | إقرار بالنسخة النهائية وملكية العمل |
| `submitted_at` | Server-side timestamp | وقت استلام يولده النظام |
| `receipt_id` | Unique immutable receipt | رقم إيصال فريد وغير قابل للتعديل |

## Recommended implementation | التنفيذ المقترح

Use a private repository or an approved learning-management form. For a private GitHub repository, use a structured Issue Form with no public visibility and an automated receipt workflow.

يُستخدم مستودع خاص أو نموذج معتمد في نظام إدارة التعلم. وعند استخدام GitHub، يكون المستودع خاصًا ويستخدم Issue Form منظمًا مع Workflow لإصدار الإيصال.

Suggested private structure:

```text
.github/ISSUE_TEMPLATE/final_submission.yml
submissions/<cohort>/<student_code>/<receipt_id>.json
receipts/<cohort>/<student_code>/<receipt_id>.md
evaluation/<cohort>/<student_code>/<receipt_id>.json
policies/retention.md
policies/resubmission.md
```

## Receipt workflow | مسار الإيصال

1. Validate required fields and URL formats.
2. Resolve the repository, tag and exact SHA.
3. Confirm that the tag points to the submitted SHA.
4. Record the server timestamp.
5. Generate a unique receipt ID.
6. Write an immutable JSON record.
7. Return a private receipt to the learner.
8. Queue the private evaluator using the exact SHA.

1. التحقق من الحقول وصيغ الروابط.
2. التحقق من المستودع وTag وSHA.
3. التأكد من أن Tag يشير إلى SHA المرسل.
4. تسجيل وقت الخادم.
5. توليد رقم إيصال فريد.
6. حفظ سجل JSON غير قابل للتعديل.
7. إرسال إيصال خاص للمتدرب.
8. إدراج النسخة الدقيقة في قائمة المقيم الخاص.

## Resubmission | إعادة التسليم

- A resubmission creates a new receipt; it never overwrites the earlier record.
- The new version requires a new commit SHA and normally a new tag.
- The written cohort policy defines whether the latest valid receipt or the first receipt is graded.
- Previous receipts remain available for audit until the review period closes.

- تنشئ إعادة التسليم إيصالًا جديدًا ولا تستبدل السجل السابق.
- تتطلب النسخة الجديدة SHA جديدًا وعادةً Tag جديدًا.
- تحدد سياسة الدفعة المكتوبة أي نسخة تعتمد في التقييم.
- تبقى الإيصالات السابقة متاحة للمراجعة حتى انتهاء فترة الاعتراض.

## Privacy and retention | الخصوصية والاحتفاظ

- The registry is private and access is limited to authorised course staff.
- Do not publish names, grades, receipts or evaluator reports.
- Retain records for the approved review period, then archive or delete them according to the applicable policy.
- Do not store passwords, access tokens or copies of unrelated personal documents.

## Status values | حالات السجل

```text
RECEIVED
IDENTITY_VERIFIED
EVALUATION_QUEUED
EVALUATION_COMPLETE
MANUAL_REVIEW_REQUIRED
RESUBMITTED
CLOSED
```

A receipt confirms receipt only. It does not confirm technical correctness, authenticity, a grade or successful completion.

يثبت الإيصال الاستلام فقط، ولا يثبت صحة المشروع أو أصالته أو درجته أو اجتيازه.

This specification remains a blueprint until a private registry is created, access-controlled and tested end to end.

تبقى هذه المواصفات مخططًا إلى أن يُنشأ السجل الخاص وتُضبط صلاحياته ويُختبر من البداية إلى النهاية.
