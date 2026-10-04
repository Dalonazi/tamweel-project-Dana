"""Generate the Day 4 bilingual learner guide from the controlled notebook sections."""
from __future__ import annotations

from pathlib import Path

from build_bilingual_day4 import SECTIONS

OUTPUT = Path("DAY4_GUIDE.md")

JOURNEY = """## Lab journey | رحلة اللاب

| Minutes | English task | المهمة بالعربية |
|---:|---|---|
| 0–10 | Separate data roles and inspect permutation importance | افصل أدوار البيانات وافحص أهمية التبديل |
| 10–25 | Read the beeswarm and SHAP output unit | اقرأ beeswarm ووحدة مخرجات SHAP |
| 25–35 | Explain one synthetic request and test local stability | فسّر طلبًا اصطناعيًا واختبر الاستقرار المحلي |
| 35–48 | Compare calibration, Brier score and ECE | قارن المعايرة وBrier وECE |
| 48–54 | Read stability limits and review capacity | اقرأ حدود الاستقرار وسعة المراجعة |
| 54–60 | Complete the report and export evidence | أكمل التقرير وصدّر الأدلة |
"""

EVIDENCE = """## Required evidence | الأدلة المطلوبة

| Evidence | Purpose | الغرض |
|---|---|---|
| `day4_roles.csv` | Role assignment and exclusions | توزيع الأدوار والاستبعادات |
| `day4_predictions.csv` | Policy and evaluation probabilities | احتمالات السياسة والتقييم |
| `permutation_importance.csv` | Held-out feature dependence | اعتماد النموذج على الخصائص |
| `day4_shap_global.csv` | Global SHAP magnitude | أهمية SHAP العامة |
| `day4_reason_codes.csv` | Local positive contributions | الإسهامات المحلية الموجبة |
| `day4_local_stability.csv` | Narrow perturbation evidence | دليل التغير المحلي المحدود |
| `day4_reliability_bins.csv` | Bin counts and observed rates | أعداد الحاويات والتكرار المرصود |
| `day4_period_metrics.csv` | Quarter-level descriptive metrics | المقاييس الوصفية حسب الربع |
| `day4_bootstrap.csv` | Customer-cluster replicates | سحبات bootstrap للعملاء |
| `day4_policy_sweep.csv` | Policy threshold candidates | مرشحو عتبة السياسة |
| `day4_review_flags.csv` | Risk and near-threshold flags | إشارات المخاطر والحالات القريبة |
| `day4_capacity.csv` | Period capacity audit | تدقيق سعة كل فترة |
| Six JSON analysis files | Metrics, provenance, reflection and run status | المقاييس والمصدر والتفسير وحالة التشغيل |
| `shap_values_sample.npz` | Complete SHAP arrays without pickle | مصفوفات SHAP الكاملة دون pickle |
| `day4_model.txt` | Saved LightGBM model | نموذج LightGBM المحفوظ |
| Six PNG figures | Visual evidence | الأدلة البصرية |
| `reports/INTERPRETABILITY_REPORT.md` | Learner interpretation | تفسير المتدرب |
| `artifacts/day4_artifacts.zip` | Submission bundle | حزمة التسليم |
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
        "# Day 4 Guide | دليل اليوم الرابع",
        "",
        "<!-- BILINGUAL:EN -->",
        "<!-- BILINGUAL:AR -->",
        "",
        '<div align="center">',
        "",
        "**SDA-DSC-211 · Tamweel Lite · Explainability, Calibration and Stability | التفسير والمعايرة والاستقرار**",
        "",
        "[Open Day 4 in Colab](https://colab.research.google.com/github/almiyead-rgb/sda-dsc-211-student-template/blob/main/notebooks/04_explain_calibrate.ipynb) · [View notebook](notebooks/04_explain_calibrate.ipynb) · [Interpretability-report template](reports/INTERPRETABILITY_REPORT_TEMPLATE.md)",
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
            "[Return to the learner guide](STUDENT_GUIDE.md) · [TreeExplainer](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html) · [Frozen-estimator calibration](https://scikit-learn.org/1.6/modules/generated/sklearn.calibration.CalibratedClassifierCV.html) · [Permutation importance](https://scikit-learn.org/1.6/modules/permutation_importance.html)",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(content), encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(ordered)} bilingual sections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
