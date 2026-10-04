"""Convert Day 4 learner markdown to paired bilingual cells without changing code."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CONTENT_VERSION = "1.1.0"
REQUIRED_ORDER = "en-left-ar-right"
DEFAULT_NOTEBOOK = Path("notebooks/04_explain_calibrate.ipynb")
DEFAULT_CONTRACT = Path("content/day4_notebook_code_contract.json")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {path}")
    return value


def source_text(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    if isinstance(source, str):
        return source
    raise ValueError("Notebook cell source must be a string or list of strings.")


def code_hashes(notebook: dict[str, Any]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        cell_id = cell.get("id")
        if not isinstance(cell_id, str) or not cell_id:
            raise ValueError("Every executable cell must have a stable id.")
        hashes[cell_id] = hashlib.sha256(source_text(cell).encode("utf-8")).hexdigest()
    return hashes


def contract_hashes(contract: dict[str, Any]) -> dict[str, str]:
    return {item["id"]: item["sha256"] for item in contract.get("code_cells", [])}


def verify_code(actual: dict[str, str], expected: dict[str, str], stage: str) -> None:
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    changed = sorted(
        cell_id
        for cell_id in set(expected) & set(actual)
        if expected[cell_id] != actual[cell_id]
    )
    if missing or unexpected or changed:
        raise RuntimeError(
            f"Executable-cell contract failed during {stage}: "
            f"missing={missing}, unexpected={unexpected}, changed={changed}"
        )


def as_lines(text: str) -> list[str]:
    stripped = text.strip()
    if not stripped:
        return []
    values = stripped.splitlines()
    return [value + "\n" for value in values[:-1]] + [values[-1]]


def paired_cell(
    pair_id: str,
    en_title: str,
    en_body: str,
    ar_title: str,
    ar_body: str,
) -> dict[str, Any]:
    html = f"""
<table style="width:100%; border-collapse:collapse;">
<tr>
<td width="50%" valign="top" dir="ltr" style="padding:14px; border:1px solid #d0d7de;">
<h2>{en_title}</h2>
{en_body.strip()}
</td>
<td width="50%" valign="top" dir="rtl" style="padding:14px; border:1px solid #d0d7de;">
<h2>{ar_title}</h2>
{ar_body.strip()}
</td>
</tr>
</table>
"""
    return {
        "cell_type": "markdown",
        "id": pair_id.replace("_", "-"),
        "metadata": {
            "bilingual_pair_id": pair_id,
            "bilingual_order": REQUIRED_ORDER,
            "learner_facing": True,
            "content_version": CONTENT_VERSION,
        },
        "source": as_lines(html),
    }


SECTIONS: dict[str, dict[str, str]] = {
    "b3503b13": {
        "pair_id": "day4_header",
        "en_title": "Day 4 · Explain the model and test its probabilities",
        "ar_title": "اليوم الرابع · فسّر النموذج واختبر احتمالاته",
        "en_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · 60-minute lab · Free CPU</strong></p>
<p>Ask two different questions: what information does the fitted model use, and do its probability scores agree with observed event frequency on a separate period? Compare permutation importance, global and local SHAP explanations, calibration, stability and the operational effect of a diagnostic review zone.</p>
<p><strong>Deliverable:</strong> <code>reports/INTERPRETABILITY_REPORT.md</code>, six figures and the complete evidence bundle.</p>
<p><strong>Boundary:</strong> the data are fictional. Explanations describe a fitted model, not causes, protected-trait effects or real financing decisions. Calibration improvement is measured, never assumed.</p>
<table><tr><th>Minutes</th><th>Your task</th></tr><tr><td>0–10</td><td>Separate data roles and inspect permutation importance</td></tr><tr><td>10–25</td><td>Read the beeswarm and SHAP output unit</td></tr><tr><td>25–35</td><td>Explain one synthetic request and test local stability</td></tr><tr><td>35–48</td><td>Compare calibration, Brier score and ECE</td></tr><tr><td>48–54</td><td>Read stability limits and review capacity</td></tr><tr><td>54–60</td><td>Complete the report and export evidence</td></tr></table>
""",
        "ar_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · لاب 60 دقيقة · CPU مجاني</strong></p>
<p>اطرح سؤالين مختلفين: ما المعلومات التي يستخدمها النموذج المدرّب، وهل تتفق درجات احتماله مع تكرار الحدث المرصود في فترة منفصلة؟ قارن أهمية التبديل، وتفسيرات SHAP العامة والمحلية، والمعايرة، والاستقرار، والأثر التشغيلي لمنطقة مراجعة تشخيصية.</p>
<p><strong>التسليم:</strong> ملف <code>reports/INTERPRETABILITY_REPORT.md</code> وستة رسوم وحزمة الأدلة الكاملة.</p>
<p><strong>الحدود:</strong> البيانات اصطناعية. تصف التفسيرات نموذجًا مدرّبًا، ولا تثبت الأسباب أو أثر السمات المحمية أو قرارات تمويل حقيقية. يُقاس تحسن المعايرة ولا يُفترض مسبقًا.</p>
<table><tr><th>الدقائق</th><th>مهمتك</th></tr><tr><td>0–10</td><td>افصل أدوار البيانات وافحص أهمية التبديل</td></tr><tr><td>10–25</td><td>اقرأ beeswarm ووحدة مخرجات SHAP</td></tr><tr><td>25–35</td><td>فسّر طلبًا اصطناعيًا واختبر الاستقرار المحلي</td></tr><tr><td>35–48</td><td>قارن المعايرة وBrier وECE</td></tr><tr><td>48–54</td><td>اقرأ حدود الاستقرار وسعة المراجعة</td></tr><tr><td>54–60</td><td>أكمل التقرير وصدّر الأدلة</td></tr></table>
""",
    },
    "1fb03eec": {
        "pair_id": "day4_setup",
        "en_title": "1. Prepare a controlled environment",
        "ar_title": "1. جهّز بيئة تشغيل محكومة",
        "en_body": """
<p>Open a fresh free-CPU session and choose <strong>Runtime → Run all</strong>. Setup verifies pinned packages, file hashes and support assets before any model work.</p>
<ul><li>Keep <code>FAST_MODE=True</code> and <code>USE_SHAP_EXAMPLE=False</code> for the primary run.</li><li>Use at most two CPU threads; no GPU, Drive mount, API key or paid service is required.</li><li>The fitted estimator is frozen before calibration. <code>FrozenEstimator</code> allows sigmoid calibration without retraining on calibration rows.</li><li>Do not replace the time/customer role split with a random split.</li></ul>
<p>If setup requests a restart, restart the session and run from the beginning. Never bypass a checksum failure.</p>
""",
        "ar_body": """
<p>افتح جلسة CPU مجانية جديدة ثم نفّذ <strong>Runtime → Run all</strong>. يتحقق الإعداد من الحزم المثبتة وبصمات الملفات وأصول الدعم قبل أي عمل على النموذج.</p>
<ul><li>اترك <code>FAST_MODE=True</code> و<code>USE_SHAP_EXAMPLE=False</code> في التشغيل الأساسي.</li><li>استخدم خيطي CPU كحد أقصى؛ لا تحتاج إلى GPU أو ربط Drive أو مفتاح API أو خدمة مدفوعة.</li><li>يُجمّد النموذج قبل المعايرة. يتيح <code>FrozenEstimator</code> تعلم تحويل sigmoid دون إعادة التدريب على صفوف المعايرة.</li><li>لا تستبدل تقسيم الزمن والعملاء بتقسيم عشوائي.</li></ul>
<p>إذا طلب الإعداد إعادة التشغيل، أعد الجلسة ثم شغّل من البداية. لا تتجاوز فشل البصمة.</p>
""",
    },
    "e91161e0": {
        "pair_id": "day4_roles",
        "en_title": "2. Separate fit, calibration, policy and evaluation",
        "ar_title": "2. افصل fit وcalibration وpolicy وevaluation",
        "en_body": """
<p>The synthetic target is a default event within 90 days after application. Newer-role customers are reserved first and removed from earlier roles; identifiers and dates are not model features.</p>
<table><tr><th>Role</th><th>Period or condition</th><th>Only permitted use</th></tr><tr><td><code>fit</code></td><td>Outcome matures before 2023-07-01</td><td>Learn imputation and the weighted model</td></tr><tr><td><code>calibration</code></td><td>Jul–Sep 2023</td><td>Learn sigmoid only</td></tr><tr><td><code>policy</code></td><td>Jan–Mar 2024</td><td>Select the 10×FN+FP threshold under 12% capacity</td></tr><tr><td><code>evaluation</code></td><td>Jul–Dec 2024</td><td>Measure and explain after freezing</td></tr></table>
<p>Gaps and conflicting-customer rows remain excluded. Evaluation is separate inside this lab but has appeared earlier in the course; it is not a final untouched test. Challenge data remain closed.</p>
<p>FAST uses 80 trees, 300 SHAP rows, three permutations and 200 customer-cluster bootstrap replicates. FULL is optional: 160 trees, 600 rows, five permutations and 500 replicates. The ±0.02 review zone is an operational scenario, not a confidence interval.</p>
""",
        "ar_body": """
<p>الهدف الاصطناعي هو وقوع حدث تعثر خلال 90 يومًا بعد الطلب. تُحجز بيانات عملاء الأدوار الأحدث أولًا وتُستبعد من الأدوار الأسبق، ولا تدخل المعرّفات والتواريخ ضمن خصائص النموذج.</p>
<table><tr><th>الدور</th><th>الفترة أو الشرط</th><th>الاستخدام الوحيد</th></tr><tr><td><code>fit</code></td><td>تنضج النتيجة قبل 2023-07-01</td><td>تعلم التعويض والنموذج الموزون</td></tr><tr><td><code>calibration</code></td><td>يوليو–سبتمبر 2023</td><td>تعلم sigmoid فقط</td></tr><tr><td><code>policy</code></td><td>يناير–مارس 2024</td><td>اختيار عتبة 10×FN+FP ضمن سعة 12%</td></tr><tr><td><code>evaluation</code></td><td>يوليو–ديسمبر 2024</td><td>القياس والتفسير بعد التثبيت</td></tr></table>
<p>تبقى الفجوات وصفوف العملاء المتعارضين مستبعدة. التقييم منفصل داخل هذا اللاب لكنه ظهر سابقًا في الدورة؛ لذلك ليس اختبارًا نهائيًا لم يُمسّ. تبقى بيانات التحدي مغلقة.</p>
<p>يستخدم FAST عدد 80 شجرة و300 صف SHAP وثلاثة تبديلات و200 سحب bootstrap للعملاء. المسار FULL اختياري: 160 شجرة و600 صف وخمسة تبديلات و500 سحب. منطقة المراجعة ±0.02 سيناريو تشغيلي وليست فترة ثقة.</p>
""",
    },
    "7aed298c": {
        "pair_id": "day4_permutation",
        "en_title": "3. Measure held-out dependence with permutation importance",
        "ar_title": "3. قِس اعتماد النموذج بأهمية التبديل",
        "en_body": """
<p>Permutation importance measures the decrease in <strong>Average Precision</strong> when a feature group is shuffled on evaluation rows without retraining. The three region indicators are shuffled together so the audit does not create impossible region combinations.</p>
<p>Training gain and held-out permutation answer different questions. A negative decrease is retained. Repeat standard deviation is variability across permutations, not a confidence interval. Correlated features can share signal and make individual importance appear smaller.</p>
<p>Do not use this evaluation result to redesign features and then call the same evaluation period independent.</p>
""",
        "ar_body": """
<p>تقيس أهمية التبديل انخفاض <strong>Average Precision</strong> عند تبديل مجموعة خصائص داخل صفوف التقييم دون إعادة التدريب. تُبدّل مؤشرات المنطقة الثلاث معًا حتى لا ينشئ التدقيق تركيبات إقليمية مستحيلة.</p>
<p>يجيب مكسب التدريب وأهمية التبديل على سؤالين مختلفين. يُحتفظ بالانخفاض السالب. انحراف التكرارات يصف التباين بين التبديلات وليس فترة ثقة. قد تتشارك الخصائص المترابطة الإشارة فتبدو أهمية كل خاصية منفردة أقل.</p>
<p>لا تستخدم نتيجة التقييم لإعادة تصميم الخصائص ثم تصف الفترة نفسها بأنها مستقلة.</p>
""",
    },
    "51ca20b6": {
        "pair_id": "day4_shap_global",
        "en_title": "4. Read the global SHAP explanation and its unit",
        "ar_title": "4. اقرأ تفسير SHAP العام ووحدته",
        "en_body": """
<p>A fixed random evaluation sample is explained with TreeSHAP for the raw weighted model. The background is the training tree-path distribution; displayed feature values are the model inputs after fit-only imputation.</p>
<p><strong>raw margin = base value + Σ SHAP</strong>, followed by <strong>raw probability = sigmoid(raw margin)</strong>. SHAP values here are in <strong>log-odds</strong>, not probability points. Do not transform each contribution separately and add the transformed values. <code>sigmoid(base_value)</code> is not necessarily the mean predicted probability.</p>
<p>Read the beeswarm in four steps: mean absolute magnitude for rank, sign for score direction, colour for feature value and spread for heterogeneous effects. This explains model behaviour; it does not establish causality or fairness.</p>
<p>If the labelled educational example appears, it is for discussion only and cannot be submitted as the learner's own run.</p>
""",
        "ar_body": """
<p>تُفسّر عينة عشوائية ثابتة من التقييم باستخدام TreeSHAP للنموذج الخام الموزون. تمثل الخلفية توزيع مسارات أشجار التدريب، وقيم الخصائص المعروضة هي مدخلات النموذج بعد التعويض المتعلم من fit فقط.</p>
<p><strong>raw margin = base value + مجموع SHAP</strong> ثم <strong>raw probability = sigmoid(raw margin)</strong>. قيم SHAP هنا بوحدة <strong>log-odds</strong> وليست نقاط احتمال. لا تحوّل كل مساهمة منفردة ثم تجمع القيم المحولة. كما أن <code>sigmoid(base_value)</code> ليس بالضرورة متوسط الاحتمالات المتوقعة.</p>
<p>اقرأ beeswarm بأربع خطوات: متوسط القيمة المطلقة للترتيب، والإشارة لاتجاه الدرجة، واللون لقيمة الخاصية، والانتشار لاختلاف الأثر. هذا تفسير لسلوك النموذج ولا يثبت السببية أو العدالة.</p>
<p>إذا ظهر المثال التعليمي الموسوم فهو للمناقشة فقط ولا يصلح للتسليم كتجربة المتدرب.</p>
""",
    },
    "fbe3d1b0": {
        "pair_id": "day4_shap_local",
        "en_title": "5. Explain one high-score synthetic request",
        "ar_title": "5. فسّر طلبًا اصطناعيًا مرتفع الدرجة",
        "en_body": """
<p>The lab selects the highest raw score inside the SHAP sample without using the observed outcome. The waterfall displays the largest contributions and groups the remainder; the complete contribution vector is preserved in the evidence file.</p>
<p>At most three reason statements are derived from actual positive contributions. Check whether the displayed input was imputed before interpreting it. A positive contribution does not mean the feature is always high, and changing the feature does not guarantee a changed outcome.</p>
<p>The <code>bureau_score ±1</code> perturbation is a narrow local stability check. It is not a guarantee for every request, feature or future period.</p>
""",
        "ar_body": """
<p>يختار اللاب أعلى درجة خام داخل عينة SHAP دون استخدام النتيجة المرصودة. تعرض waterfall أكبر الإسهامات وتجمع البقية، مع حفظ متجه الإسهامات الكامل في ملف الأدلة.</p>
<p>تُشتق ثلاث عبارات سبب كحد أقصى من الإسهامات الموجبة الفعلية. تحقّق أولًا هل القيمة المعروضة عُوّضت قبل تفسيرها. لا تعني المساهمة الموجبة أن الخاصية مرتفعة دائمًا، ولا يضمن تغيير الخاصية تغير النتيجة.</p>
<p>اختبار <code>bureau_score ±1</code> فحص محلي ضيق للاستقرار، وليس ضمانًا لكل طلب أو خاصية أو فترة مستقبلية.</p>
""",
    },
    "b314b571": {
        "pair_id": "day4_calibration",
        "en_title": "6. Test calibration on a separate period",
        "ar_title": "6. اختبر المعايرة على فترة منفصلة",
        "en_body": """
<p>Sigmoid is learned on calibration rows only, without new class weights. The fitted model and calibrator are then frozen and measured on evaluation.</p>
<p>Compare ROC-AUC and Average Precision for ranking, and Brier score, log-loss and ECE for probability quality. A lower Brier score alone does not prove perfect calibration.</p>
<p>ECE uses ten equal-width bins: Σ(bin count ÷ all rows × |mean probability − observed rate|). Empty bins remain visible and every bin count is reported. ECE depends on bin boundaries and sample size; sparse bins are weak evidence.</p>
<p>A single monotone sigmoid mapping preserves the ordering of this model, but calibration is not guaranteed to improve. Isotonic calibration is optional and requires caution with the small number of calibration positives.</p>
""",
        "ar_body": """
<p>يتعلم sigmoid من صفوف calibration فقط دون أوزان فئات جديدة. ثم يُثبّت النموذج والمعاير وتُقاس النتائج على evaluation.</p>
<p>قارن ROC-AUC وAverage Precision للترتيب، وBrier وlog-loss وECE لجودة الاحتمال. لا يثبت انخفاض Brier وحده المعايرة المثالية.</p>
<p>يستخدم ECE عشر حاويات متساوية العرض: مجموع (عدد الحاوية ÷ جميع الصفوف × |متوسط الاحتمال − التكرار المرصود|). تبقى الحاويات الفارغة ظاهرة ويُعرض عدد كل حاوية. يتأثر ECE بحدود الحاويات وحجم العينة؛ الحاويات القليلة دليل ضعيف.</p>
<p>يحافظ تحويل sigmoid المتزايد الواحد على ترتيب هذا النموذج، لكن التحسن غير مضمون. المعايرة isotonic توسع اختياري يحتاج حذرًا مع قلة الموجبات في عينة المعايرة.</p>
""",
    },
    "a5e6de14": {
        "pair_id": "day4_stability",
        "en_title": "7. Quantify what the stability interval does and does not cover",
        "ar_title": "7. حدّد ما تغطيه فترة الاستقرار وما لا تغطيه",
        "en_body": """
<p>The paired bootstrap samples <strong>customers</strong>, keeping each customer's requests together, and compares raw versus calibrated results on the same replicates. It reports 95% percentile intervals for AP and Brier change.</p>
<p>The model and calibrator remain fixed. The interval therefore excludes uncertainty from model training, calibration fitting and future temporal drift. It is not a confidence interval for one applicant's probability.</p>
<p>Quarter-level evaluation metrics describe temporal variation. They are not three independent folds or a confidence interval. Any change designed after viewing evaluation needs new evidence.</p>
""",
        "ar_body": """
<p>يسحب bootstrap المزدوج <strong>العملاء</strong> مع إبقاء طلبات العميل معًا، ويقارن النتائج الخام والمعايرة على السحبات نفسها. يعرض فترات مئينية 95% لـAP وتغير Brier.</p>
<p>يبقى النموذج والمعاير ثابتين؛ لذلك لا تشمل الفترة عدم يقين تدريب النموذج أو تعلم المعايرة أو الانجراف الزمني المستقبلي. كما أنها ليست فترة ثقة لاحتمال طلب واحد.</p>
<p>تصف مقاييس أرباع التقييم التغير الزمني، وليست طيات مستقلة أو فترة ثقة. أي تعديل يُصمم بعد رؤية التقييم يحتاج إلى دليل جديد.</p>
""",
    },
    "243d7cd1": {
        "pair_id": "day4_review_zone",
        "en_title": "8. Test whether the review zone fits capacity",
        "ar_title": "8. اختبر ملاءمة منطقة المراجعة للسعة",
        "en_body": """
<p>The raw threshold was selected on the policy role only under the 10×FN+FP loss and a 12% capacity ceiling. It is transported through the monotone sigmoid mapping; it is not reselected on evaluation and is not copied from a different Day 3 model.</p>
<p>The ±0.02 probability zone is a diagnostic band for near-threshold cases, not individual uncertainty. When combining it with risk flags, count the union once. Capacity can fail in a later period even before adding the zone.</p>
<p><code>CAPACITY_REVIEW_REQUIRED</code> is a valid finding. Do not raise the ceiling, hide rows or retune the threshold after seeing evaluation. A revised policy must be developed and evaluated with new evidence.</p>
""",
        "ar_body": """
<p>اختيرت العتبة الخام على دور policy فقط ضمن خسارة 10×FN+FP وسقف سعة 12%. تُنقل عبر تحويل sigmoid المتزايد، ولا يُعاد اختيارها على evaluation ولا تُنسخ من نموذج مختلف في اليوم الثالث.</p>
<p>منطقة الاحتمال ±0.02 نطاق تشخيصي للحالات القريبة من العتبة وليست عدم يقين فرديًا. عند جمعها مع إشارات المخاطر احسب اتحاد المجموعتين مرة واحدة. قد تفشل السعة في فترة لاحقة حتى قبل إضافة المنطقة.</p>
<p>ظهور <code>CAPACITY_REVIEW_REQUIRED</code> نتيجة صحيحة. لا ترفع السقف ولا تُخفِ صفوفًا ولا تعِد ضبط العتبة بعد رؤية التقييم. يجب تطوير السياسة المعدلة وتقييمها بدليل جديد.</p>
""",
    },
    "b32204ee": {
        "pair_id": "day4_interpretation",
        "en_title": "9. Write the interpretation supported by your evidence",
        "ar_title": "9. اكتب تفسيرًا تدعمه أدلتك",
        "en_body": """
<p>Complete all six fields in <code>responses</code> and cite your measured values and denominators:</p>
<ol><li>global versus local explanation;</li><li>SHAP output unit and background;</li><li>limits of reason statements and correlated features;</li><li>calibration evidence on the separate period;</li><li>what the stability interval includes and excludes;</li><li>the review zone's effect on period capacity.</li></ol>
<p>Completeness changes the learner checkpoint to ready for review. It does not verify correctness and does not award an automatic grade.</p>
""",
        "ar_body": """
<p>أكمل الحقول الستة داخل <code>responses</code> واستشهد بالقيم المقاسة ومقاماتها:</p>
<ol><li>الفرق بين التفسير العام والمحلي؛</li><li>وحدة SHAP وخلفيته؛</li><li>حدود عبارات السبب والخصائص المترابطة؛</li><li>دليل المعايرة على الفترة المنفصلة؛</li><li>ما تشمله فترة الاستقرار وما تستبعده؛</li><li>أثر منطقة المراجعة في سعة كل فترة.</li></ol>
<p>يحوّل اكتمال النصوص بوابة المتدرب إلى جاهز للمراجعة، لكنه لا يتحقق من صحة الإجابات ولا يمنح درجة آلية.</p>
""",
    },
    "332c6d91": {
        "pair_id": "day4_export",
        "en_title": "10. Export the report and evidence bundle",
        "ar_title": "10. صدّر التقرير وحزمة الأدلة",
        "en_body": """
<p>Re-run the export cell after completing <code>responses</code>. Download <code>artifacts/day4_artifacts.zip</code> and keep its <code>artifacts/</code> and <code>reports/</code> structure. Save the executed notebook as <code>notebooks/04_explain_calibrate.ipynb</code>.</p>
<p>The bundle contains 12 CSV tables, six analysis JSON files plus the environment record, a compressed NPZ of complete SHAP values, the LightGBM model text, six PNG figures and <code>reports/INTERPRETABILITY_REPORT.md</code>.</p>
<p>Read probability CSV files with <code>float_precision="round_trip"</code> when exact round trips matter. A technically successful run can still require learner work or capacity review. Educational-example mode is not submittable and is blocked in assessment mode.</p>
""",
        "ar_body": """
<p>أعد تشغيل خلية التصدير بعد إكمال <code>responses</code>. نزّل <code>artifacts/day4_artifacts.zip</code> واحتفظ بهيكل <code>artifacts/</code> و<code>reports/</code>. احفظ الدفتر المنفذ باسم <code>notebooks/04_explain_calibrate.ipynb</code>.</p>
<p>تضم الحزمة 12 جدول CSV وستة ملفات JSON تحليلية إضافة إلى سجل البيئة، وملف NPZ مضغوط لقيم SHAP الكاملة، ونص نموذج LightGBM، وستة رسوم PNG، وملف <code>reports/INTERPRETABILITY_REPORT.md</code>.</p>
<p>استخدم <code>float_precision="round_trip"</code> عند إعادة قراءة ملفات الاحتمالات إذا كانت الاستعادة الدقيقة مهمة. قد ينجح التشغيل تقنيًا مع بقاء عمل على المتدرب أو مراجعة للسعة. وضع المثال التعليمي غير صالح للتسليم ويُحظر في وضع التقييم.</p>
""",
    },
    "c8296a62": {
        "pair_id": "day4_checkpoint",
        "en_title": "Before moving to Day 5",
        "ar_title": "قبل الانتقال إلى اليوم الخامس",
        "en_body": """
<p>Open all six figures and verify units, denominators, labels and explanation source. Be able to explain why one monotone mapping can preserve rank, why SHAP contributions do not establish causality and why near-threshold review needs a separate capacity calculation.</p>
<p>If an educational SHAP example was used, rerun live SHAP on CPU before submission; never present the example as your own experiment.</p>
<p><a href="https://github.com/almiyead-rgb/sda-dsc-211-student-template/blob/main/DAY4_GUIDE.md">Day 4 guide</a> · <a href="https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html">TreeExplainer output units</a> · <a href="https://scikit-learn.org/1.6/modules/generated/sklearn.calibration.CalibratedClassifierCV.html">Frozen-model calibration</a></p>
""",
        "ar_body": """
<p>افتح الرسوم الستة وتحقق من الوحدات والمقامات والعناوين ومصدر التفسير. يجب أن تستطيع شرح سبب محافظة تحويل متزايد واحد على الترتيب، ولماذا لا تثبت مساهمات SHAP السببية، ولماذا تحتاج مراجعة الحالات القريبة إلى حساب مستقل للسعة.</p>
<p>إذا استُخدم مثال SHAP التعليمي فأعد تشغيل SHAP المباشر على CPU قبل التسليم، ولا تعرض المثال بوصفه تجربتك.</p>
<p><a href="https://github.com/almiyead-rgb/sda-dsc-211-student-template/blob/main/DAY4_GUIDE.md">دليل اليوم الرابع</a> · <a href="https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html">وحدات TreeExplainer</a> · <a href="https://scikit-learn.org/1.6/modules/generated/sklearn.calibration.CalibratedClassifierCV.html">معايرة نموذج مجمد</a></p>
""",
    },
}

PAIR_TO_SECTION = {value["pair_id"]: value for value in SECTIONS.values()}


def build_notebook(notebook: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    expected_code = contract_hashes(contract)
    verify_code(code_hashes(notebook), expected_code, "before bilingual conversion")

    seen_pairs: set[str] = set()
    cells: list[dict[str, Any]] = []

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            cells.append(cell)
            continue

        cell_id = cell.get("id")
        metadata = cell.get("metadata", {})
        pair_id = metadata.get("bilingual_pair_id") if isinstance(metadata, dict) else None

        if cell_id in SECTIONS:
            section = SECTIONS[cell_id]
        elif pair_id in PAIR_TO_SECTION:
            section = PAIR_TO_SECTION[str(pair_id)]
        else:
            raise RuntimeError(f"Unexpected Day 4 markdown cell: id={cell_id!r}, pair={pair_id!r}")

        if section["pair_id"] in seen_pairs:
            raise RuntimeError(f"Duplicate bilingual pair {section['pair_id']}")
        seen_pairs.add(section["pair_id"])
        cells.append(
            paired_cell(
                section["pair_id"],
                section["en_title"],
                section["en_body"],
                section["ar_title"],
                section["ar_body"],
            )
        )

    expected_pairs = set(PAIR_TO_SECTION)
    if seen_pairs != expected_pairs:
        raise RuntimeError(
            f"Day 4 markdown coverage mismatch: "
            f"missing={sorted(expected_pairs - seen_pairs)}, "
            f"unexpected={sorted(seen_pairs - expected_pairs)}"
        )

    notebook["cells"] = cells
    notebook.setdefault("metadata", {})["bilingual_content_version"] = CONTENT_VERSION
    notebook["metadata"]["bilingual_order"] = REQUIRED_ORDER
    verify_code(code_hashes(notebook), expected_code, "after bilingual conversion")
    return notebook


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=Path, default=DEFAULT_NOTEBOOK)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument(
        "--output-report",
        type=Path,
        default=Path("check-output/day4-bilingual-build.json"),
    )
    args = parser.parse_args()

    notebook = load_json(args.notebook)
    contract = load_json(args.contract)
    before = code_hashes(notebook)
    converted = build_notebook(notebook, contract)
    after = code_hashes(converted)

    args.notebook.write_text(
        json.dumps(converted, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    report = {
        "status": "PASS",
        "notebook": str(args.notebook),
        "content_version": CONTENT_VERSION,
        "bilingual_order": REQUIRED_ORDER,
        "paired_sections": len(SECTIONS),
        "executable_cells": len(before),
        "code_preserved": before == after == contract_hashes(contract),
        "pair_ids": [value["pair_id"] for value in SECTIONS.values()],
    }
    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    args.output_report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
