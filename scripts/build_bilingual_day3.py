"""Convert Day 3 learner markdown to a paired bilingual layout without changing code."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CONTENT_VERSION = "1.1.0"
REQUIRED_ORDER = "en-left-ar-right"


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


def lines(text: str) -> list[str]:
    values = text.strip().splitlines()
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
        "source": lines(html),
    }


SECTIONS: dict[str, dict[str, str]] = {
    "36af768d": {
        "pair_id": "day3_header",
        "en_title": "Day 3 · Choose a decision threshold you can defend",
        "ar_title": "اليوم الثالث · اختر عتبة قرار تستطيع تبريرها",
        "en_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · 60-minute lab · Free CPU</strong></p>
<p>Compare unweighted training, class weighting and training-only oversampling on the same honest out-of-fold rows. Convert model scores into simulated review flags using an explicit error-loss policy and a capacity ceiling for every validation period.</p>
<p><strong>Deliverables:</strong> model and threshold comparisons, a cost curve, exact threshold JSON, period-capacity and regional audits, sensitivity scenarios, provenance, your written reasoning and <code>reports/DECISION_CARD.md</code>.</p>
<p><strong>Decision boundary:</strong> a flag means simulated review, not automatic approval or refusal. Loss values are educational decision units, not Saudi riyals, fees, expected credit loss or grade deductions. Threshold selection uses development OOF labels and is not a final independent test.</p>
<table><tr><th>Minutes</th><th>Your task</th></tr><tr><td>0–10</td><td>Freeze the loss and capacity policy</td></tr><tr><td>10–20</td><td>Generate OOF evidence for three strategies</td></tr><tr><td>20–35</td><td>Compare ranking and sweep thresholds</td></tr><tr><td>35–45</td><td>Audit capacity in every period</td></tr><tr><td>45–50</td><td>Inspect cost sensitivity</td></tr><tr><td>50–55</td><td>Review descriptive regional differences</td></tr><tr><td>55–60</td><td>Write and export the decision card</td></tr></table>
""",
        "ar_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · لاب 60 دقيقة · CPU مجاني</strong></p>
<p>قارن التدريب غير الموزون ووزن الفئة وإعادة أخذ العينات داخل التدريب فقط على صفوف OOF الصادقة نفسها. ثم حوّل درجات النموذج إلى إشارات مراجعة محاكاة باستخدام سياسة معلنة لخسارة الأخطاء وسقف سعة لكل فترة تحقق.</p>
<p><strong>المخرجات:</strong> مقارنات النماذج والعتبات، ومنحنى التكلفة، وملف JSON للعتبة الدقيقة، وتدقيق السعة والمناطق، وسيناريوهات الحساسية، ومصدر التنفيذ، وتفسيرك المكتوب، وملف <code>reports/DECISION_CARD.md</code>.</p>
<p><strong>حد القرار:</strong> الإشارة تعني مراجعة محاكاة، ولا تعني قبولًا أو رفضًا آليًا. قيم الخسارة وحدات قرار تعليمية، وليست ريالات سعودية أو رسومًا أو خسارة ائتمانية متوقعة أو خصمًا من الدرجة. اختيار العتبة يستخدم أهداف OOF التطويرية، وليس اختبارًا نهائيًا مستقلًا.</p>
<table><tr><th>الدقائق</th><th>مهمتك</th></tr><tr><td>0–10</td><td>ثبّت سياسة الخسارة والسعة</td></tr><tr><td>10–20</td><td>أنشئ أدلة OOF للاستراتيجيات الثلاث</td></tr><tr><td>20–35</td><td>قارن الترتيب وامسح العتبات</td></tr><tr><td>35–45</td><td>دقّق السعة في كل فترة</td></tr><tr><td>45–50</td><td>افحص حساسية التكلفة</td></tr><tr><td>50–55</td><td>راجع الفروق الوصفية بين المناطق</td></tr><tr><td>55–60</td><td>اكتب بطاقة القرار وصدّرها</td></tr></table>
""",
    },
    "b1dfdacf": {
        "pair_id": "day3_setup",
        "en_title": "1. Prepare a controlled environment",
        "ar_title": "1. جهّز بيئة تشغيل محكومة",
        "en_body": """
<p>Open a fresh session, select the free CPU runtime and choose <strong>Runtime → Run all</strong>. Setup verifies pinned versions, data hashes and support files before training.</p>
<ul><li><code>FAST_MODE=True</code>: 80 trees per model and two CPU threads; use this first.</li><li><code>FULL_MODE=True</code>: optional 160-tree cap.</li><li>The Day 2 time/customer split is rebuilt from source; no previous notebook output is required.</li><li>No GPU, API key, Drive mount, paid package or external service is required.</li></ul>
<p>Tree count is frozen before comparing imbalance treatments. Do not tune again after reading today’s OOF results. If setup requests a restart, restart the session and run from the beginning.</p>
""",
        "ar_body": """
<p>افتح جلسة جديدة، واختر CPU المجاني، ثم نفّذ <strong>Runtime → Run all</strong>. يتحقق الإعداد من الإصدارات المثبتة وبصمات البيانات وملفات الدعم قبل التدريب.</p>
<ul><li><code>FAST_MODE=True</code>: عدد 80 شجرة لكل نموذج وخيطا CPU؛ ابدأ به.</li><li><code>FULL_MODE=True</code>: سقف اختياري قدره 160 شجرة.</li><li>يعاد بناء تقسيم الزمن والعملاء من اليوم الثاني من المصدر؛ لا تحتاج إلى مخرجات دفتر سابق.</li><li>لا تحتاج إلى GPU أو مفتاح API أو ربط Drive أو حزمة مدفوعة أو خدمة خارجية.</li></ul>
<p>يُثبّت عدد الأشجار قبل مقارنة طرق عدم التوازن. لا تعِد الضبط بعد قراءة نتائج OOF اليوم. إذا طلب الإعداد إعادة التشغيل، أعد الجلسة ثم شغّل الدفتر من البداية.</p>
""",
    },
    "6215b30a": {
        "pair_id": "day3_policy",
        "en_title": "2. Freeze the teaching loss and capacity policy",
        "ar_title": "2. ثبّت سياسة الخسارة والسعة التعليمية",
        "en_body": """
<p>The target is a default event within 90 days after application. All records are synthetic, and challenge data remain closed.</p>
<table><tr><th>Outcome</th><th>Teaching meaning</th><th>Loss units</th></tr><tr><td>TP</td><td>Flag before a later default event</td><td>0</td></tr><tr><td>FN</td><td>Later default without a flag</td><td>10</td></tr><tr><td>FP</td><td>Flag on a non-default case</td><td>1</td></tr><tr><td>TN</td><td>Non-default case without a flag</td><td>0</td></tr></table>
<p><strong>Observed educational loss = 10 × FN + 1 × FP.</strong> Review cost and review effectiveness are omitted from this simplified policy.</p>
<p><strong>Capacity rule:</strong> flags must not exceed 12% of requests in <em>each</em> validation period, rounded down to a whole request. A pooled rate alone can hide overload in one period. Keep this policy fixed for the core exercise.</p>
""",
        "ar_body": """
<p>الهدف هو وقوع حدث تعثر خلال 90 يومًا بعد الطلب. جميع السجلات اصطناعية، وتبقى بيانات التحدي مغلقة.</p>
<table><tr><th>النتيجة</th><th>معناها التعليمي</th><th>وحدات الخسارة</th></tr><tr><td>TP</td><td>إشارة قبل حدث تعثر لاحق</td><td>0</td></tr><tr><td>FN</td><td>تعثر لاحق لم ترفع له إشارة</td><td>10</td></tr><tr><td>FP</td><td>إشارة لحالة لم تتعثر</td><td>1</td></tr><tr><td>TN</td><td>حالة سليمة بلا إشارة</td><td>0</td></tr></table>
<p><strong>الخسارة التعليمية المرصودة = 10 × FN + 1 × FP.</strong> لا تتضمن السياسة المبسطة تكلفة المراجعة أو فعاليتها.</p>
<p><strong>قاعدة السعة:</strong> يجب ألا تتجاوز الإشارات 12% من طلبات <em>كل</em> فترة تحقق، مع التقريب إلى العدد الصحيح الأدنى. قد تخفي النسبة المجمعة وحدها ازدحام فترة معينة. أبقِ السياسة ثابتة في التطبيق الأساسي.</p>
""",
    },
    "ed930e9b": {
        "pair_id": "day3_strategies",
        "en_title": "3. Change training only, never validation",
        "ar_title": "3. غيّر التدريب فقط ولا تمس التحقق",
        "en_body": """
<p>All three LightGBM strategies use the same approved features, folds, tree budget and random seed:</p>
<table><tr><th>Strategy</th><th>Training change</th></tr><tr><td><code>unweighted</code></td><td>No row duplication or class weight</td></tr><tr><td><code>weighted</code></td><td><code>scale_pos_weight = negatives / positives</code> from that fold’s training rows only</td></tr><tr><td><code>oversampled</code></td><td>Randomly duplicate the minority class inside training until classes are balanced</td></tr></table>
<p>Missing-value imputation is learned from the original training rows before oversampling. Validation prevalence remains untouched. Class weighting changes model fitting; the FN/FP policy changes the downstream decision. They are not the same quantity.</p>
<p>Weighting and oversampling can distort probability calibration. Do not interpret a raw score of 0.70 as a reliable 70% probability before Day 4 calibration checks.</p>
<p>If the cooperative CPU budget expires, a labelled educational example may support discussion, but it is not a learner run and cannot be submitted. Assessment mode disables this fallback.</p>
""",
        "ar_body": """
<p>تستخدم استراتيجيات LightGBM الثلاث الخصائص والطيات وميزانية الأشجار والبذرة نفسها:</p>
<table><tr><th>الاستراتيجية</th><th>التغيير داخل التدريب</th></tr><tr><td><code>unweighted</code></td><td>لا نسخ للصفوف ولا وزن للفئة</td></tr><tr><td><code>weighted</code></td><td><code>scale_pos_weight = negatives / positives</code> من صفوف تدريب الطية فقط</td></tr><tr><td><code>oversampled</code></td><td>نسخ عشوائي للفئة الأقل داخل التدريب حتى تتوازن الفئتان</td></tr></table>
<p>يتعلم تعويض القيم المفقودة من صفوف التدريب الأصلية قبل إعادة العينات. تبقى نسبة الفئة في التحقق دون تغيير. يغيّر وزن الفئة تدريب النموذج، بينما تغيّر سياسة FN وFP القرار اللاحق؛ وهما كميتان مختلفتان.</p>
<p>قد يشوّه الوزن وإعادة العينات معايرة الاحتمالات. لا تفسّر الدرجة الخام 0.70 بوصفها احتمالًا موثوقًا قدره 70% قبل فحوص المعايرة في اليوم الرابع.</p>
<p>إذا انتهت ميزانية CPU التعاونية، فقد يظهر مثال تعليمي موسوم للنقاش، لكنه ليس تشغيل المتدرب ولا يصلح للتسليم. يعطّل وضع التقييم هذا البديل.</p>
""",
    },
    "88402ae4": {
        "pair_id": "day3_ranking",
        "en_title": "4. Accuracy can hide complete failure",
        "ar_title": "4. قد تخفي Accuracy فشلًا كاملًا",
        "en_body": """
<p>Each strategy covers the same 5,039 later eligible applications. Another 4,961 warm-up rows have no OOF prediction and must not be filled with training predictions.</p>
<ul><li><strong>ROC-AUC:</strong> pooled OOF ranking quality across thresholds.</li><li><strong>Average Precision:</strong> the course PR-AUC definition for the pooled OOF rows.</li><li><strong>Accuracy at 0.5:</strong> a decision result at one arbitrary threshold, not a complete model-quality measure.</li></ul>
<p>The “flag nobody” reference can show high accuracy while recall is zero. Inspect prevalence, AP, recall, precision, flags and loss together. Pooled AP here is not the mean of Day 2 fold AP values.</p>
""",
        "ar_body": """
<p>تغطي كل استراتيجية الطلبات اللاحقة المؤهلة نفسها وعددها 5,039. وتبقى 4,961 عينة تمهيدية بلا تنبؤ OOF، ولا يجوز ملؤها بتنبؤات التدريب.</p>
<ul><li><strong>ROC-AUC:</strong> جودة ترتيب OOF المجمعة عبر العتبات.</li><li><strong>Average Precision:</strong> تعريف PR-AUC المعتمد في الدورة لصفوف OOF المجمعة.</li><li><strong>Accuracy عند 0.5:</strong> نتيجة قرار عند عتبة اعتباطية واحدة، وليست مقياسًا كاملًا لجودة النموذج.</li></ul>
<p>قد يحقق مرجع «لا ترفع إشارة لأحد» Accuracy مرتفعة بينما يساوي Recall صفرًا. اقرأ نسبة الموجب وAP وRecall وPrecision وعدد الإشارات والخسارة معًا. AP المجمعة هنا ليست متوسط AP لطيات اليوم الثاني.</p>
""",
    },
    "f40e7d34": {
        "pair_id": "day3_threshold",
        "en_title": "5. Sweep every distinct decision rule",
        "ar_title": "5. افحص كل قاعدة عتبة مميزة",
        "en_body": """
<p>A request is flagged when <strong>score ≥ threshold</strong>. The sweep evaluates every distinct score, adds 0.5 explicitly and includes a no-flag rule, avoiding a coarse grid that can miss the best observed rule.</p>
<ul><li>Tied scores remain together; do not break ties by identifier to fill capacity.</li><li>If loss ties, prefer fewer flags and then the higher threshold.</li><li>Select one minimum-loss rule without a capacity limit and another minimum-loss rule feasible in every period.</li></ul>
<p>The unconstrained rule cannot have higher observed OOF loss than 0.5 because 0.5 is included. The capacity-constrained rule may have higher loss when 0.5 is infeasible.</p>
<p>Selection on OOF is safer than selection on training predictions, but it still uses the same development labels to choose the threshold. The selected loss is optimistic development evidence, not final-test performance.</p>
""",
        "ar_body": """
<p>ترفع الإشارة عندما تكون <strong>الدرجة ≥ العتبة</strong>. يفحص المسح كل درجة مميزة، ويضيف 0.5 صراحة، ويضم قاعدة بلا إشارات، بدل شبكة خشنة قد تفوّت أفضل قاعدة مرصودة.</p>
<ul><li>تبقى الدرجات المتعادلة معًا؛ لا تكسر التعادل بالمعرّف لملء السعة.</li><li>عند تساوي الخسارة، فضّل إشارات أقل ثم العتبة الأعلى.</li><li>اختر قاعدة بأقل خسارة دون قيد، وقاعدة أخرى بأقل خسارة قابلة للتنفيذ في كل فترة.</li></ul>
<p>لا يمكن أن تتجاوز خسارة القاعدة غير المقيدة خسارة 0.5 المرصودة لأن 0.5 ضمن المرشحين. وقد تزيد خسارة القاعدة المقيدة إذا كانت 0.5 غير قابلة للتنفيذ.</p>
<p>الاختيار على OOF أكثر أمانًا من الاختيار على تنبؤات التدريب، لكنه ما زال يستخدم أهداف التطوير نفسها لاختيار العتبة. الخسارة المختارة دليل تطوير متفائل، وليست أداء اختبار نهائي.</p>
""",
    },
    "9251be3e": {
        "pair_id": "day3_capacity",
        "en_title": "6. Audit every period and test policy sensitivity",
        "ar_title": "6. دقّق كل فترة واختبر حساسية السياسة",
        "en_body": """
<p>The per-period table is the binding capacity evidence. A pooled rate alone is insufficient. Preserve the full exported threshold precision; rounding can change which tied or boundary scores are flagged.</p>
<p>Test FN costs of 8, 10 and 12 while holding FP cost at 1 and capacity at 12%. These are ±20% policy scenarios, not confidence intervals. They show whether the operating point is fragile to a plausible assumption change.</p>
<p>The theoretical unconstrained threshold 1/11 requires calibrated probabilities, the stated loss matrix and no capacity limit. Do not impose it on today’s weighted raw scores.</p>
<p>Historical feasibility does not guarantee future capacity. A production process would monitor queue volume, score distribution, prevalence and threshold stability.</p>
""",
        "ar_body": """
<p>جدول كل فترة هو دليل السعة الملزم؛ لا تكفي النسبة المجمعة وحدها. احتفظ بالدقة الكاملة للعتبة المصدرة، لأن التقريب قد يغيّر الحالات المتعادلة أو الواقعة عند الحد.</p>
<p>اختبر خسارة FN بالقيم 8 و10 و12 مع إبقاء خسارة FP عند 1 والسعة عند 12%. هذه سيناريوهات سياسة ±20% وليست فترات ثقة، وتوضح مدى هشاشة نقطة التشغيل أمام تغير افتراض معقول.</p>
<p>تتطلب العتبة النظرية غير المقيدة 1/11 احتمالات معايرة ومصفوفة الخسارة المحددة وغياب قيد السعة. لا تفرضها على درجات اليوم الخام الموزونة.</p>
<p>لا تضمن القابلية التاريخية سعة المستقبل. تحتاج العملية الفعلية إلى مراقبة حجم الطابور وتوزيع الدرجات ونسبة الحدث واستقرار العتبة.</p>
""",
    },
    "1dd37e9d": {
        "pair_id": "day3_groups",
        "en_title": "7. Report descriptive group differences carefully",
        "ar_title": "7. أبلغ عن الفروق الوصفية بين المجموعات بحذر",
        "en_body": """
<p>After freezing one shared threshold, compute each synthetic region’s false-positive rate as <strong>FP ÷ non-default cases</strong>. Report the denominator, flag count and recall alongside the rate.</p>
<ul><li>The gap is the largest FPR minus the smallest, in percentage points.</li><li>A missing denominator produces a missing rate, not zero.</li><li>Groups with fewer than 30 non-default cases receive a low-support warning.</li></ul>
<p>This is a descriptive audit, not a statistical significance test, legal fairness certification or causal conclusion about geography. A visible gap requires review; a small gap does not prove fairness. Do not hide differences by assigning separate thresholds to groups without a governed policy.</p>
""",
        "ar_body": """
<p>بعد تثبيت عتبة مشتركة واحدة، احسب معدل الإنذار الخاطئ لكل منطقة اصطناعية وفق <strong>FP ÷ الحالات غير المتعثرة</strong>. اعرض المقام وعدد الإشارات وRecall بجانب المعدل.</p>
<ul><li>الفجوة هي أكبر FPR ناقص أصغره بوحدة نقطة مئوية.</li><li>غياب المقام ينتج معدلًا غير متاح، لا صفرًا.</li><li>تُوسم المجموعة عندما يقل دعم الحالات السليمة عن 30.</li></ul>
<p>هذا تدقيق وصفي، وليس اختبار دلالة أو شهادة عدالة قانونية أو استنتاجًا سببيًا عن الجغرافيا. الفجوة الظاهرة تحتاج إلى مراجعة، والفجوة الصغيرة لا تثبت العدالة. لا تخفِ الفروق بعتبات منفصلة للمجموعات دون سياسة محكومة.</p>
""",
    },
    "7db1c236": {
        "pair_id": "day3_reasoning",
        "en_title": "8. Write the decision argument yourself",
        "ar_title": "8. اكتب حجة القرار بنفسك",
        "en_body": """
<p>Complete the shared response cell in your own words and cite numbers from your run:</p>
<ol><li>Why the selected threshold is defensible.</li><li>The observed loss–capacity trade-off.</li><li>The regional FPR gap and what needs review.</li><li>Limitations: OOF development selection, coverage, calibration and simplified policy.</li><li>Why accuracy can mislead under class imbalance.</li><li>Why threshold selection uses OOF rather than training predictions or challenge data.</li></ol>
<p>Copying the threshold alone is insufficient. The automated checkpoint detects missing fields only; it does not judge correctness, assign a grade or establish authorship.</p>
""",
        "ar_body": """
<p>أكمل خلية الإجابات المشتركة بصياغتك أنت، واستشهد بأرقام من تشغيلك:</p>
<ol><li>لماذا يمكن الدفاع عن العتبة المختارة.</li><li>المقايضة المرصودة بين الخسارة والسعة.</li><li>فجوة FPR بين المناطق وما يحتاج إلى مراجعة.</li><li>القيود: اختيار تطويري على OOF، والتغطية، والمعايرة، وتبسيط السياسة.</li><li>لماذا قد تكون Accuracy مضللة مع عدم توازن الفئات.</li><li>لماذا نختار العتبة على OOF بدل تنبؤات التدريب أو بيانات التحدي.</li></ol>
<p>لا يكفي نسخ رقم العتبة. يكتشف الفحص الآلي الحقول الفارغة فقط؛ ولا يحكم على صحة الإجابة أو يمنح درجة أو يثبت الملكية.</p>
""",
    },
    "817dbb08": {
        "pair_id": "day3_export",
        "en_title": "9. Export the decision card and evidence",
        "ar_title": "9. صدّر بطاقة القرار والأدلة",
        "en_body": """
<p>The export cell creates <code>reports/DECISION_CARD.md</code> from actual run values and your text, then saves CSV, JSON and figure evidence.</p>
<ul><li><code>TECHNICAL_READY</code>: the live run and technical guards completed.</li><li><code>LEARNER_WORK_REQUIRED</code>: technical work passed, but your interpretation remains incomplete.</li><li><code>READY_FOR_REVIEW</code>: required text fields exist; this is not an automated grade.</li><li><code>EXAMPLE_ONLY_NOT_SUBMITTABLE</code>: the recovery example was used and cannot represent your work.</li></ul>
<p>Download <code>day3_artifacts.zip</code>, extract it at the repository root and retain the generated <code>artifacts/</code> and <code>reports/</code> folders. Save the executed notebook as <code>notebooks/03_cost_sensitive_decision.ipynb</code>. Uploading only the ZIP does not satisfy the visible-file requirements.</p>
""",
        "ar_body": """
<p>تنشئ خلية التصدير ملف <code>reports/DECISION_CARD.md</code> من قيم التشغيل الفعلية ونصك، ثم تحفظ أدلة CSV وJSON والرسوم.</p>
<ul><li><code>TECHNICAL_READY</code>: اكتمل التشغيل الفعلي والحراس التقنية.</li><li><code>LEARNER_WORK_REQUIRED</code>: نجح الجانب التقني، لكن تفسيرك ما زال ناقصًا.</li><li><code>READY_FOR_REVIEW</code>: الحقول النصية موجودة؛ وهذه ليست درجة آلية.</li><li><code>EXAMPLE_ONLY_NOT_SUBMITTABLE</code>: استُخدم مثال التعافي ولا يمكن اعتباره عملك.</li></ul>
<p>نزّل <code>day3_artifacts.zip</code> وافكّه في جذر المستودع مع الاحتفاظ بمجلدي <code>artifacts/</code> و<code>reports/</code>. احفظ الدفتر المنفذ باسم <code>notebooks/03_cost_sensitive_decision.ipynb</code>. رفع ملف ZIP وحده لا يحقق متطلبات الملفات الظاهرة.</p>
""",
    },
    "782e8d6f": {
        "pair_id": "day3_completion",
        "en_title": "Completion checkpoint and Day 4 bridge",
        "ar_title": "بوابة الإكمال والربط باليوم الرابع",
        "en_body": """
<ul><li>You can identify FN and FP and explain the teaching loss matrix.</li><li>You can show capacity compliance for every period, not only in aggregate.</li><li>You compared weighting and oversampling without declaring a required winner.</li><li>You preserved the exact threshold and documented sensitivity and group-audit limits.</li><li>You saved the executed notebook, 17 artifact files and the decision card outside the temporary Colab session.</li></ul>
<p><strong>Troubleshooting:</strong> restart after an imported-version mismatch; rerun setup after a network interruption; never bypass a checksum; rerun live CPU training if the educational example appears; never submit another learner’s outputs.</p>
<p><strong>Day 4:</strong> inspect global and local explanations, test calibration and decide whether the score can be interpreted as a probability.</p>
""",
        "ar_body": """
<ul><li>تستطيع تحديد FN وFP وشرح مصفوفة الخسارة التعليمية.</li><li>تستطيع إثبات الالتزام بالسعة في كل فترة، وليس في المجموع فقط.</li><li>قارنت الوزن وإعادة العينات دون افتراض فائز مطلوب.</li><li>حفظت العتبة بكامل دقتها ووثقت الحساسية وحدود تدقيق المجموعات.</li><li>حفظت الدفتر المنفذ و17 ملف دليل وبطاقة القرار خارج جلسة Colab المؤقتة.</li></ul>
<p><strong>حل التعثر:</strong> أعد تشغيل الجلسة عند اختلاف إصدار مستورد؛ أعد الإعداد بعد انقطاع الشبكة؛ لا تتجاوز فحص البصمة؛ أعد التدريب الفعلي على CPU عند ظهور المثال التعليمي؛ ولا تسلّم مخرجات متدرب آخر.</p>
<p><strong>اليوم الرابع:</strong> افحص التفسير العالمي والمحلي، واختبر المعايرة، وقرر هل يمكن تفسير الدرجة بوصفها احتمالًا.</p>
""",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--notebook", type=Path, default=Path("notebooks/03_cost_sensitive_decision.ipynb")
    )
    parser.add_argument(
        "--contract", type=Path, default=Path("content/day3_notebook_code_contract.json")
    )
    parser.add_argument("--output-report", type=Path)
    args = parser.parse_args()

    notebook = load_json(args.notebook)
    contract = load_json(args.contract)
    expected = contract_hashes(contract)
    before = code_hashes(notebook)
    verify_code(before, expected, "pre-conversion")

    found: set[str] = set()
    converted: list[dict[str, Any]] = []
    for cell in notebook.get("cells", []):
        cell_id = cell.get("id")
        if cell.get("cell_type") == "markdown" and cell_id in SECTIONS:
            section = SECTIONS[cell_id]
            converted.append(
                paired_cell(
                    section["pair_id"],
                    section["en_title"],
                    section["en_body"],
                    section["ar_title"],
                    section["ar_body"],
                )
            )
            found.add(cell_id)
        else:
            converted.append(cell)

    missing_sections = sorted(set(SECTIONS) - found)
    if missing_sections:
        raise RuntimeError(f"Missing expected Day 3 markdown cells: {missing_sections}")

    notebook["cells"] = converted
    metadata = notebook.setdefault("metadata", {})
    metadata["course_content_version"] = CONTENT_VERSION
    metadata["bilingual_layout"] = REQUIRED_ORDER

    after = code_hashes(notebook)
    verify_code(after, expected, "post-conversion")
    args.notebook.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )

    report = {
        "status": "PASS",
        "notebook": args.notebook.as_posix(),
        "paired_markdown_cells": len(found),
        "executable_cells_preserved": len(expected),
        "content_version": CONTENT_VERSION,
        "layout": REQUIRED_ORDER,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output_report:
        args.output_report.parent.mkdir(parents=True, exist_ok=True)
        args.output_report.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
