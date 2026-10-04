# Course–Project Alignment | مواءمة الدورة والمشروع

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Why this matrix exists

This matrix shows how the five-day Tamweel Lite project implements the learning outcomes of **SDA-DSC-211 — Advanced Machine Learning Methods**. Every assessed concept is linked to a lab, a learner artifact and a rubric criterion.

</td>
<td width="50%" valign="top" dir="rtl">

## لماذا توجد هذه المصفوفة؟

توضح هذه المصفوفة كيف يحقق مشروع **Tamweel Lite** المتدرج خلال خمسة أيام مخرجات تعلم برنامج **SDA-DSC-211 — أساليب تعلم الآلة المتقدمة**. يرتبط كل مفهوم مقيم بلاب ومخرج للمتدرب ومعيار في سلم التقييم.

</td>
</tr>
</table>

## Alignment matrix | مصفوفة المواءمة

| Outcome | Learning outcome — English | مخرج التعلم — العربية | Day / Lab | Learner evidence | Rubric |
|---|---|---|---|---|---|
| LO1 | Build high-performance tabular classifiers with XGBoost and LightGBM and compare them against a defensible baseline. | بناء مصنفات عالية الأداء للبيانات الجدولية باستخدام XGBoost وLightGBM ومقارنتها بخط أساس قابل للدفاع. | Day 1 — `01_baseline_boosting.ipynb` | model comparison, learning curves, candidate decision | J3 |
| LO2 | Design validation that respects time, repeated customers and leakage boundaries. | تصميم تحقق يراعي الزمن والعملاء المتكررين وحدود تسرب البيانات. | Day 2 — `02_validation_tuning.ipynb` | leakage audit, fold audit, OOF coverage | J4 |
| LO3 | Apply bounded hyperparameter optimisation without turning the lab into an uncontrolled search. | تطبيق ضبط محدود للمعاملات دون تحويل اللاب إلى بحث غير منضبط. | Day 2 — bounded Optuna search | search results, selected parameters, provenance | J4 |
| LO4 | Handle class imbalance and asymmetric error costs using honest predictions and a documented policy. | معالجة عدم توازن الفئات وتفاوت تكلفة الأخطاء باستخدام تنبؤات صادقة وسياسة موثقة. | Day 3 — `03_cost_sensitive_decision.ipynb` | strategy comparison, threshold sweep, Decision Card | J5 |
| LO5 | Explain global and local model behaviour with permutation importance and SHAP while respecting interpretability limits. | تفسير سلوك النموذج العام والمحلي باستخدام أهمية التبديل وSHAP مع الالتزام بحدود التفسير. | Day 4 — `04_explain_calibrate.ipynb` | importance tables, beeswarm, waterfall, reason codes | J6 |
| LO6 | Evaluate calibration, stability, uncertainty and operational impact rather than relying on discrimination alone. | تقييم المعايرة والاستقرار وعدم اليقين والأثر التشغيلي بدل الاعتماد على قدرة الترتيب وحدها. | Day 4 | reliability curve, Brier, ECE, bootstrap/stability evidence | J6, J8 |
| LO7 | Build and assess averaging or stacking with honest out-of-fold predictions and a Worth-It Gate. | بناء المتوسط أو التكديس وتقييمه باستخدام تنبؤات OOF صادقة وبوابة جدوى. | Day 5 — `05_final_model.ipynb` | ensemble comparison, Worth-It decision, final pipeline | J7 |
| LO8 | Deliver a reproducible end-to-end project with governance, interpretation and a professional defence. | تسليم مشروع متكامل قابل لإعادة الإنتاج ويتضمن الحوكمة والتفسير والدفاع المهني. | Days 1–5 + Notebook 99 | README, reports, Model Card, manifest, final bundle, presentation | J1, J2, J8, J9, P1–P5 |

## Five-day build journey | رحلة البناء خلال خمسة أيام

| Day | English focus | التركيز بالعربية | Main artifact |
|---:|---|---|---|
| 1 | Baseline, gradient boosting and fair comparison | خط الأساس والتعزيز والمقارنة العادلة | model comparison and candidate decision |
| 2 | Honest validation, leakage control and bounded search | التحقق الصادق ومنع التسرب والبحث المحدود | validation report and best parameters |
| 3 | Imbalance, threshold, simulated decision cost and capacity | عدم التوازن والعتبة وتكلفة القرار التعليمية والسعة | Decision Card |
| 4 | Explainability, calibration and stability | التفسير والمعايرة والاستقرار | Interpretability Report |
| 5 | Ensemble decision, final model and reproducible delivery | قرار التجميع والنموذج النهائي والتسليم القابل لإعادة الإنتاج | final model, submission and Model Card |

<table>
<tr>
<td width="50%" valign="top" dir="ltr">

## Design principles

1. One progressive project replaces disconnected examples.
2. Every day produces an artifact used by the final submission.
3. Code runs on free Colab CPU with pinned dependencies.
4. The core path remains accessible to beginner-to-intermediate learners.
5. Advanced extensions do not block the required path.
6. Assessment rewards evidence and reasoning, not only model score.
7. Challenge data and hidden evaluation remain isolated.
8. The learner must be able to explain every central decision.

</td>
<td width="50%" valign="top" dir="rtl">

## مبادئ التصميم

1. يحل مشروع متدرج واحد محل الأمثلة المنفصلة.
2. ينتج كل يوم مخرجًا يدخل في التسليم النهائي.
3. يعمل الكود على CPU المجاني في Colab بإصدارات مثبتة.
4. يبقى المسار الأساسي مناسبًا للمبتدئ إلى المتوسط.
5. لا تعطل الامتدادات المتقدمة المسار الإلزامي.
6. يكافئ التقييم الأدلة والتفسير، وليس درجة النموذج فقط.
7. تبقى بيانات التحدي والتقييم المخفي معزولة.
8. يجب أن يستطيع المتدرب شرح كل قرار محوري.

</td>
</tr>
</table>

## Evidence traceability | تتبع الأدلة

The final repository should allow a reviewer to move from each learning outcome to the exact notebook section, generated artifact, report paragraph and rubric criterion that proves completion.

يجب أن يمكّن المستودع النهائي المراجع من الانتقال من كل مخرج تعلم إلى قسم الدفتر والملف الناتج وفقرة التقرير ومعيار التقييم التي تثبت تحقيقه.
