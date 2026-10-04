"""Generate the bilingual final-check guide from controlled Notebook 99 sections."""
from __future__ import annotations

from pathlib import Path

from build_bilingual_final_check import SECTIONS

OUTPUT = Path("FINAL_CHECK_GUIDE.md")

CHECK_MEANINGS = """## What each gate proves | معنى كل بوابة

| Gate | What it proves | ما تثبته |
|---|---|---|
| Environment Check | Template files, unit tests and local links are technically sound; it does not prove learner completion | سلامة ملفات القالب والاختبارات والروابط المحلية؛ ولا يثبت اكتمال عمل المتدرب |
| Notebook Smoke Test | Applications execute in isolated workspaces without requiring completed learner prose | إمكانية تشغيل التطبيقات في مساحات معزولة دون اشتراط اكتمال النصوص |
| Final Project Check | Required project files, fresh execution, predictions, policy and manifest satisfy the declared technical contract | توافق الملفات والتشغيل الجديد والتنبؤات والسياسة والـmanifest مع العقد التقني المعلن |
| Instructor review | Interpretation, authenticity, presentation and final score | التفسير وأصالة العمل والعرض والدرجة النهائية |
"""

LOCAL = """## Local execution | التشغيل المحلي

```bash
python -m pip install -r requirements-colab.txt -r requirements-check.txt -c constraints.txt
python scripts/final_check.py --root . --output .check-output --prepare
python -m tamweel.inference --input data/tamweel_challenge.csv --output .check-output/probabilities.csv
```

The inference interface returns only `application_id,probability`. Apply the decision policy once after collecting the full batch. Do not compute a challenge performance score from the public unlabelled data.

تعيد واجهة التنبؤ `application_id,probability` فقط. طبّق سياسة القرار مرة واحدة بعد جمع الدفعة كاملة. لا تحسب درجة أداء للتحدي من البيانات العامة غير المعلّمة.
"""


def table(section: dict[str, str]) -> str:
    return f"""<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## {section["en_title"]}

{section["en_body"].strip()}

</td>
<td width="50%" valign="top" dir="rtl">

## {section["ar_title"]}

{section["ar_body"].strip()}

</td>
</tr>
</table>
"""


def main() -> int:
    ordered = list(SECTIONS.values())
    content = [
        "# Final Project Check Guide | دليل الفحص النهائي للمشروع",
        "",
        "<!-- BILINGUAL:EN -->",
        "<!-- BILINGUAL:AR -->",
        "",
        '<div align="center">',
        "",
        "**SDA-DSC-211 · Tamweel Lite · Technical preflight, not a grade or receipt | فحص تقني تمهيدي، وليس درجة أو إيصالًا**",
        "",
        "[Open Notebook 99 in Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/99_final_submission_check.ipynb) · [Submission guide](SUBMISSION_GUIDE.md) · [Day 5 guide](DAY5_GUIDE.md)",
        "",
        "</div>",
        "",
    ]
    content.extend(table(section) for section in ordered)
    content.extend(
        [
            CHECK_MEANINGS,
            "## Public and private repositories | المستودعات العامة والخاصة",
            "",
            "GitHub-hosted validation uses the standard `ubuntu-latest` runner for public repositories. In a private repository, use Notebook 99 on free Colab to avoid consuming a private Actions quota. No GPU, payment card or paid service is required.",
            "",
            "يستخدم التحقق المستضاف في GitHub مشغل `ubuntu-latest` القياسي للمستودعات العامة. في المستودع الخاص استخدم دفتر 99 على Colab المجاني لتجنب استهلاك حصة Actions الخاصة. لا تحتاج إلى GPU أو بطاقة دفع أو خدمة مدفوعة.",
            "",
            LOCAL,
            "[Return to the learner guide](STUDENT_GUIDE.md) · [Open Notebook 99](notebooks/99_final_submission_check.ipynb)",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(content), encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(ordered)} bilingual sections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
