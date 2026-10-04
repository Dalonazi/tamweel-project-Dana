"""Generate the Day 5 bilingual learner guide from controlled notebook sections."""
from __future__ import annotations

from pathlib import Path

from build_bilingual_day5 import SECTIONS

OUTPUT = Path("DAY5_GUIDE.md")

JOURNEY = """## Lab journey | رحلة اللاب

| Minutes | English task | المهمة بالعربية |
|---:|---|---|
| 0–10 | Inspect roles and OOF diversity | افحص الأدوار وتنوع OOF |
| 10–25 | Compare averages and nested stacking | قارن المتوسطات وStacking المتداخل |
| 25–35 | Apply the worth-it gate and decision policy | طبّق بوابة الجدوى وسياسة القرار |
| 35–45 | Freeze calibration and score the challenge | ثبّت المعايرة وقيّم التحدي |
| 45–55 | Write the model card and assemble evidence | اكتب بطاقة النموذج واجمع الأدلة |
| 55–60 | Verify the bundle and save the notebook | تحقق من الحزمة واحفظ الدفتر |
"""

EVIDENCE = """## Required evidence | الأدلة المطلوبة

| Evidence | Purpose | الغرض |
|---|---|---|
| `day5_roles.csv` | Fit/calibration/exclusion roles | أدوار التدريب والمعايرة والاستبعاد |
| `day5_oof_predictions.csv` | Common outer-OOF predictions | تنبؤات OOF الخارجية المشتركة |
| `day5_fold_scores.csv` | Fold metrics for six candidates | مقاييس الطيات للخيارات الستة |
| `ensemble_comparison.csv` | Worth-it gate inputs and result | مدخلات ونتيجة بوابة الجدوى |
| `day5_probability_correlation.csv` | Probability diversity | تنوع الاحتمالات |
| `day5_residual_correlation.csv` | Residual diversity | تنوع البواقي |
| `day5_threshold_sweep.csv` | Cost/capacity threshold search | بحث العتبة وفق التكلفة والسعة |
| `day5_region_audit.csv` | Descriptive regional OOF audit | تدقيق OOF وصفي للمناطق |
| `day5_period_capacity.csv` | Capacity by validation period | السعة حسب فترة التحقق |
| `day5_cost_sensitivity.csv` | Fixed-decision cost scenarios | سيناريوهات التكلفة مع قرار ثابت |
| `day5_calibration_predictions.csv` | Raw and calibrated fit diagnostics | تشخيصات المعايرة الخام والمعايرة |
| `day5_calibration_fit_bins.csv` | Reliability-bin counts | حاويات الموثوقية ومقاماتها |
| `final_model/` | Portable model and hash manifest | النموذج القابل للنقل وبيان بصماته |
| `final_policy.json` | Frozen threshold, mapping and batch policy | العتبة والتحويل وسياسة الدفعة |
| `final_metrics.json` | Selection and diagnostic scope | نطاق الاختيار والتشخيص |
| `submission/submission.csv` | One row for every challenge ID | صف واحد لكل معرف تحدٍّ |
| `reports/MODEL_CARD.md` | Model scope, limits and monitoring | نطاق النموذج وقيوده ومتابعته |
| `reports/ENSEMBLE_DECISION.md` | Evidence-based complexity decision | قرار التعقيد المدعوم بالأدلة |
| `PROJECT_README.md` | Arabic/English executive summary | الملخص التنفيذي العربي والإنجليزي |
| `submission/project_bundle.zip` | Verifiable project bundle | حزمة المشروع القابلة للتحقق |
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
        "# Day 5 Guide | دليل اليوم الخامس",
        "",
        "<!-- BILINGUAL:EN -->",
        "<!-- BILINGUAL:AR -->",
        "",
        '<div align="center">',
        "",
        "**SDA-DSC-211 · Tamweel Lite · Final Model, Delivery and Evidence | النموذج النهائي والتسليم والأدلة**",
        "",
        "[Open Day 5 in Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/05_final_model.ipynb) · [View notebook](notebooks/05_final_model.ipynb) · [Submission guide](SUBMISSION_GUIDE.md) · [Final check guide](FINAL_CHECK_GUIDE.md)",
        "",
        "</div>",
        "",
        table(ordered[0]),
        JOURNEY,
    ]
    content.extend(table(section) for section in ordered[1:-1])
    content.extend(
        [
            EVIDENCE,
            table(ordered[-1]),
            "[Return to the learner guide](STUDENT_GUIDE.md) · [Open Notebook 99](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/99_final_submission_check.ipynb) · [StackingClassifier](https://scikit-learn.org/1.6/modules/generated/sklearn.ensemble.StackingClassifier.html) · [Frozen-estimator calibration](https://scikit-learn.org/1.6/modules/generated/sklearn.calibration.CalibratedClassifierCV.html)",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(content), encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(ordered)} bilingual sections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
