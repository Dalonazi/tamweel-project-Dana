# Bilingual Colab Notebook Standard | معيار دفاتر Colab الثنائية

Version: 1.1.0-draft  
Owner: Meaad Al-Marri | ميعاد المري

## Design objective | الهدف التصميمي

Every learner-facing notebook must provide equivalent Arabic and English guidance while keeping one shared executable code path. The learner should not need to switch files or compare two notebooks.

يجب أن يقدم كل دفتر موجه للمتدرب إرشادات عربية وإنجليزية متكافئة مع الحفاظ على مسار كود تنفيذي واحد. لا ينبغي أن يحتاج المتدرب إلى الانتقال بين ملفين أو مقارنة دفترين.

## Required section pattern | النمط الإلزامي لكل قسم

1. Bilingual concept cell.
2. Shared code cell.
3. Bilingual output title.
4. Bilingual interpretation prompts.
5. Checkpoint and saved evidence.

1. خلية مفهوم ثنائية اللغة.
2. خلية كود مشتركة.
3. عنوان ثنائي للمخرجات.
4. أسئلة تفسير باللغتين.
5. نقطة تحقق ودليل محفوظ.

## Desktop rendering | العرض على الحاسب

Use an HTML table inside Markdown cells:

```html
<table>
<tr>
<td width="50%" valign="top" dir="ltr">
<h3>English heading</h3>
<p>Independent English explanation.</p>
</td>
<td width="50%" valign="top" dir="rtl">
<h3>العنوان العربي</h3>
<p>شرح عربي مستقل.</p>
</td>
</tr>
</table>
```

Colab renders this structure without requiring custom JavaScript or paid extensions.

## Mobile and narrow screens | الشاشات الضيقة

Long paragraphs must be split into short blocks. Do not place wide data tables inside paired columns. Use the paired layout for explanation, then show the data table once below both columns.

تُقسم الفقرات الطويلة إلى كتل قصيرة. لا توضع جداول بيانات عريضة داخل العمودين. يستخدم التخطيط الثنائي للشرح، ثم يظهر جدول البيانات مرة واحدة أسفل العمودين.

## Code rules | قواعد الكود

- Code appears once only.
- Variable names, function names, file paths, library names, and commands remain English.
- Comments may be bilingual when they clarify learner decisions.
- Code cells must not depend on the visual language order.
- Every required notebook must run using free CPU.
- No API key, paid service, GPU, or secret is permitted.
- `FAST_MODE=True` is the default learner path.
- Recovery examples must be visibly marked `EXAMPLE_ONLY_NOT_SUBMITTABLE` in both languages.

## Markdown cell metadata | بيانات خلية Markdown

Every learner-facing paired Markdown cell created for v1.1.0 must include:

```json
{
  "bilingual_pair_id": "day03-threshold-policy",
  "bilingual_order": "en-left-ar-right",
  "learner_facing": true,
  "content_version": "1.1.0"
}
```

The pair ID must be unique inside the notebook.

## Notebook header | رأس الدفتر

Every notebook begins with paired content covering:

| English | العربية |
|---|---|
| Lab title | عنوان اللاب |
| Duration | المدة |
| Learning objectives | أهداف التعلم |
| Prerequisites | المتطلبات السابقة |
| Deliverables | المخرجات المطلوبة |
| Acceptance criteria | معايير القبول |
| Runtime and cost | بيئة التشغيل والتكلفة |
| Safety and scope limits | حدود الاستخدام والنطاق |

## Interpretation ownership | ملكية التفسير

At least one learner-owned task must be completed each day. Running the notebook without completing the task is not `READY_FOR_REVIEW`.

- Day 1: justify the candidate model.
- Day 2: classify features as safe, metadata, or leakage.
- Day 3: explain the selected threshold and trade-off.
- Day 4: interpret one local SHAP explanation and state its limits.
- Day 5: issue a documented `KEEP SINGLE` or `SHIP ENSEMBLE` decision.

يجب أن ينجز المتدرب مهمة تفسيرية أو برمجية صغيرة كل يوم. تشغيل الدفتر دون إكمالها لا يحقق حالة `READY_FOR_REVIEW`.

## Error messages | رسائل الأخطاء

Use the technical phrase in English followed by a concise Arabic explanation:

```text
Missing required artifact | ملف الدليل الإلزامي غير موجود
```

Do not translate package names or Python exception classes.

## Acceptance test | اختبار القبول

A notebook is bilingual-ready only when:

1. All learner-facing Markdown sections have both languages.
2. Requirements, numbers, file names, and warnings match.
3. The notebook executes from a fresh kernel.
4. The notebook does not require a previous day's runtime state.
5. The learner-owned checkpoint blocks final readiness when incomplete.
6. Saved files match the documented deliverables.
7. The notebook remains understandable at 200% browser zoom.
