"""Convert Day 2 learner markdown to a paired bilingual layout without changing code."""
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
    "4806f764": {
        "pair_id": "day2_header",
        "en_title": "Day 2 · Validate honestly before tuning",
        "ar_title": "اليوم الثاني · تحقّق بصدق قبل ضبط النموذج",
        "en_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · 60-minute lab · Free CPU</strong></p>
<p>Audit feature availability, remove post-outcome leakage and exact duplicate events, then evaluate later requests with mature labels while excluding each validation fold's customers from its training fold. Freeze a bounded search on a separate historical customer cohort before reading outer-validation results.</p>
<p><strong>Deliverables:</strong> leakage and fold audits, bounded-search history, frozen parameters, validation report and summary, out-of-fold predictions and coverage, provenance, figures, run metadata and your written interpretation.</p>
<p><strong>Scientific boundary:</strong> all records are synthetic. The random protocols are negative controls, not deployment evidence. The forward folds estimate a particular later-period, unseen-customer scenario; they are not a final independent test and do not prove fairness, calibration or operational value.</p>
<table><tr><th>Minutes</th><th>Your task</th></tr><tr><td>0–8</td><td>Prepare the environment and read the data contract</td></tr><tr><td>8–18</td><td>Audit leakage and duplicate events</td></tr><tr><td>18–30</td><td>Inspect time, customer and label-maturity boundaries</td></tr><tr><td>30–45</td><td>Run the bounded search on the reserved cohort</td></tr><tr><td>45–53</td><td>Compare means, variation and coverage</td></tr><tr><td>53–60</td><td>Write your reasoning and export evidence</td></tr></table>
""",
        "ar_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · لاب 60 دقيقة · CPU مجاني</strong></p>
<p>دقّق زمن إتاحة الخصائص، واحذف تسرب ما بعد النتيجة والنسخ المتطابقة من الحدث، ثم قيّم الطلبات اللاحقة بعد نضج أهدافها مع استبعاد عملاء كل طية تحقق من تدريب الطية نفسها. جمّد بحثًا محدودًا على مجموعة تاريخية منفصلة قبل قراءة نتائج التحقق الخارجي.</p>
<p><strong>المخرجات:</strong> تدقيق التسرب والطيات، وسجل البحث المحدود، والإعدادات المجمدة، وتقرير التحقق وملخصه، وتنبؤات OOF وتغطيتها، ومصدر التدريب، والرسوم، وبيانات التشغيل، وتفسيرك المكتوب.</p>
<p><strong>حد علمي:</strong> جميع السجلات اصطناعية. البروتوكولات العشوائية ضوابط سلبية وليست دليل نشر. تقيس الطيات الزمنية سيناريو محددًا لطلبات لاحقة من عملاء غير موجودين في تدريب الطية؛ وليست اختبارًا نهائيًا مستقلًا، ولا تثبت العدالة أو المعايرة أو القيمة التشغيلية.</p>
<table><tr><th>الدقائق</th><th>مهمتك</th></tr><tr><td>0–8</td><td>جهّز البيئة واقرأ عقد البيانات</td></tr><tr><td>8–18</td><td>دقّق التسرب والطلبات المكررة</td></tr><tr><td>18–30</td><td>افحص حدود الزمن والعملاء ونضج الهدف</td></tr><tr><td>30–45</td><td>نفّذ البحث المحدود على المجموعة المحجوزة</td></tr><tr><td>45–53</td><td>قارن المتوسط والتشتت والتغطية</td></tr><tr><td>53–60</td><td>اكتب تفسيرك وصدّر الأدلة</td></tr></table>
""",
    },
    "b32f917b": {
        "pair_id": "day2_setup",
        "en_title": "1. Prepare a controlled environment",
        "ar_title": "1. جهّز بيئة تشغيل محكومة",
        "en_body": """
<p>Open a fresh notebook session, select the free CPU runtime and choose <strong>Runtime → Run all</strong>. Setup verifies pinned library versions, the data manifest and SHA-256 hashes before modeling.</p>
<ul><li><code>FAST_MODE=True</code>: two CPU threads and a ceiling of 200 trees; use this first.</li><li><code>FULL_MODE=True</code>: optional ceiling of 600 trees.</li><li>Both modes retain at most eight sequential trials, three search folds and a 120-second cooperative search budget.</li><li>No GPU, API key, Drive mount or paid service is required.</li></ul>
<p><strong>Pass condition:</strong> the cell prints <code>Day 2 setup verified</code>. Do not bypass checksum or imported-version failures; restart the session and run from the beginning.</p>
""",
        "ar_body": """
<p>افتح جلسة دفتر جديدة، واختر بيئة CPU المجانية، ثم نفّذ <strong>Runtime → Run all</strong>. يتحقق الإعداد من إصدارات المكتبات المثبتة وبيان البيانات وبصمات SHA-256 قبل بدء النمذجة.</p>
<ul><li><code>FAST_MODE=True</code>: خيطا CPU وسقف 200 شجرة؛ ابدأ به.</li><li><code>FULL_MODE=True</code>: سقف اختياري يبلغ 600 شجرة.</li><li>يحتفظ الوضعان بحد أقصى قدره ثماني تجارب متتابعة وثلاث طيات للبحث وميزانية بحث تعاونية قدرها 120 ثانية.</li><li>لا تحتاج إلى GPU أو مفتاح API أو ربط Drive أو خدمة مدفوعة.</li></ul>
<p><strong>شرط الاجتياز:</strong> ظهور <code>Day 2 setup verified</code>. لا تتجاوز فشل البصمة أو اختلاف إصدار مستورد؛ أعد تشغيل الجلسة ثم شغّل الدفتر من البداية.</p>
""",
    },
    "035ce1ff": {
        "pair_id": "day2_leakage",
        "en_title": "2. Audit information availability and duplicates",
        "ar_title": "2. دقّق إتاحة المعلومات والتكرار",
        "en_body": """
<p>The target <code>default_within_90d</code> records whether a default event occurs within 90 days after the application. It does not mean an account reaches exactly 90 days past due.</p>
<p>Use the feature dictionary's <code>available_at</code> field. A predictor is eligible only when its information exists at application time. A strong correlation alone does not prove leakage.</p>
<table><tr><th>Risk</th><th>Guard</th></tr><tr><td>Target leakage</td><td>Remove fields describing the later outcome</td></tr><tr><td>Preprocessing leakage</td><td>Learn imputation from training rows only</td></tr><tr><td>Time leakage</td><td>Train only on applications whose labels are mature before validation starts</td></tr><tr><td>Customer leakage</td><td>Exclude validation customers from the same fold's training rows</td></tr><tr><td>Duplicate leakage</td><td>Deduplicate identical events and reject conflicting copies</td></tr></table>
<p>The dirty training copy is read to demonstrate the audit. Challenge data is not used for model selection or comparison in this lab.</p>
""",
        "ar_body": """
<p>يسجل الهدف <code>default_within_90d</code> ما إذا وقع حدث تعثر خلال 90 يومًا بعد الطلب. ولا يعني وصول الحساب إلى 90 يوم تأخر بالضبط.</p>
<p>استخدم حقل <code>available_at</code> في قاموس الخصائص. لا تُقبل الخاصية إلا إذا كانت معلومتها موجودة وقت تقديم الطلب. الارتباط القوي وحده لا يثبت التسرب.</p>
<table><tr><th>الخطر</th><th>الحارس</th></tr><tr><td>تسرب الهدف</td><td>حذف الحقول التي تصف النتيجة اللاحقة</td></tr><tr><td>تسرب المعالجة</td><td>تعلم التعويض من صفوف التدريب فقط</td></tr><tr><td>تسرب الزمن</td><td>التدريب على الطلبات التي نضجت أهدافها قبل بدء التحقق</td></tr><tr><td>تسرب العميل</td><td>استبعاد عملاء التحقق من تدريب الطية نفسها</td></tr><tr><td>تسرب التكرار</td><td>حذف الأحداث المتطابقة ورفض النسخ المتعارضة</td></tr></table>
<p>تُقرأ نسخة التدريب المتسربة لشرح التدقيق. لا تُستخدم بيانات التحدي في اختيار النموذج أو مقارنته في هذا اللاب.</p>
""",
    },
    "26438cc9": {
        "pair_id": "day2_folds",
        "en_title": "3. Freeze time, customer and label-maturity roles",
        "ar_title": "3. جمّد أدوار الزمن والعملاء ونضج الهدف",
        "en_body": """
<p>The notebook creates three consecutive forward-validation windows. For each fold, training rows must satisfy:</p>
<p><strong>application date + 90 days &lt; validation start</strong></p>
<p>The strict inequality intentionally excludes labels that mature exactly on the boundary. Every customer appearing in a fold's validation period is removed from that fold's training rows.</p>
<ul><li>The design evaluates later requests from customers unseen in the corresponding training fold.</li><li>A customer may appear in more than one validation period; the guarantee is zero train–validation overlap within each fold.</li><li>Earlier rows remain a warm-up period. They must not receive fitted-training predictions disguised as OOF evidence.</li><li>Exact duplicate events are removed before splitting. Conflicting copies stop execution.</li></ul>
<p>Inspect the fold-audit table and figure before interpreting any performance metric.</p>
""",
        "ar_body": """
<p>ينشئ الدفتر ثلاث فترات تحقق زمنية متتابعة. يجب أن تحقق صفوف تدريب كل طية الشرط الآتي:</p>
<p><strong>تاريخ الطلب + 90 يومًا &lt; بداية التحقق</strong></p>
<p>تستبعد المتباينة الصارمة عمدًا الأهداف التي تنضج في يوم الحد نفسه. ويُحذف من تدريب كل طية كل عميل يظهر في فترة تحقق تلك الطية.</p>
<ul><li>يقيس التصميم طلبات لاحقة من عملاء لم يظهروا في تدريب الطية المقابلة.</li><li>قد يظهر العميل في أكثر من فترة تحقق؛ والضمان هو عدم وجود تداخل بين التدريب والتحقق داخل الطية نفسها.</li><li>تبقى الصفوف المبكرة فترة تمهيد. لا تمنحها تنبؤات تدريب ثم تعرضها بوصفها OOF.</li><li>تُحذف الأحداث المتطابقة قبل التقسيم، بينما توقف النسخ المتعارضة التنفيذ.</li></ul>
<p>افحص جدول تدقيق الطيات والرسم قبل تفسير أي مقياس أداء.</p>
""",
    },
    "01b5d8e8": {
        "pair_id": "day2_search_cohort",
        "en_title": "4. Reserve search before reading outer validation",
        "ar_title": "4. احجز البحث قبل قراءة التحقق الخارجي",
        "en_body": """
<p>Hyperparameters are selected once from a historical cohort that is mature before the first outer-validation window. All customers used in any of the three outer-validation periods are excluded from this search cohort.</p>
<p>Inside the reserved cohort, three forward folds also separate customers. Each fold contains an inner stopping split: preprocessing and trees are learned on inner-fit rows, the tree count is selected on inner-stop log loss, and the model is then refit on the full fold-training rows.</p>
<ul><li>Outer-validation rows never select imputation, tree count or hyperparameters.</li><li>Future target values are not used to define search parameters.</li><li>The released data produces a relatively small search cohort, with few positive examples in some inner partitions. Record this limitation.</li></ul>
<p>The best search AP is a model-selection statistic. It is not an estimate of future outer performance.</p>
""",
        "ar_body": """
<p>تُختار المعاملات مرة واحدة من مجموعة تاريخية نضجت أهدافها قبل أول فترة تحقق خارجي. ويُستبعد من مجموعة البحث جميع العملاء المستخدمين في فترات التحقق الخارجي الثلاث.</p>
<p>داخل المجموعة المحجوزة توجد ثلاث طيات زمنية تفصل العملاء أيضًا. تتضمن كل طية جزءًا داخليًا للإيقاف: تتعلم المعالجة والأشجار من صفوف inner fit، ويُختار عدد الأشجار من inner stop باستخدام log loss، ثم يُعاد التدريب على صفوف تدريب الطية كاملة.</p>
<ul><li>لا تختار صفوف التحقق الخارجي التعويض أو عدد الأشجار أو معاملات البحث.</li><li>لا تُستخدم أهداف المستقبل في تحديد إعدادات البحث.</li><li>تنتج البيانات المنشورة مجموعة بحث صغيرة نسبيًا، مع أمثلة موجبة قليلة في بعض الأجزاء الداخلية. وثّق هذا القيد.</li></ul>
<p>أفضل AP داخل البحث إحصائية لاختيار النموذج، وليست تقديرًا للأداء الخارجي المستقبلي.</p>
""",
    },
    "cd23c217": {
        "pair_id": "day2_optuna",
        "en_title": "5. Run a bounded Optuna search",
        "ar_title": "5. نفّذ بحث Optuna محدودًا",
        "en_body": """
<p>The objective is mean <strong>Average Precision (AP)</strong> across three internal forward folds. Search changes only <code>learning_rate</code>, <code>num_leaves</code> and <code>min_child_samples</code>.</p>
<ul><li>Seed: 211.</li><li>At most eight sequential trials.</li><li>At most 120 seconds for search, with cooperative stopping that can finish slightly after the boundary.</li><li><code>COMPLETE</code>: all three fold scores were calculated.</li><li><code>PRUNED</code>: the trial stopped early.</li><li><code>FAIL</code>: the attempt did not produce a complete objective; partial values are not a completed mean.</li></ul>
<p>If no trial completes, the notebook shows a stored <code>EDUCATIONAL_EXAMPLE</code> for discussion only and reports <code>TUNING_REQUIRED</code>. The example is never copied into your live results or submission. Retry later in a fresh free-CPU session rather than purchasing compute.</p>
""",
        "ar_body": """
<p>الهدف هو متوسط <strong>Average Precision (AP)</strong> عبر ثلاث طيات زمنية داخلية. يغيّر البحث فقط <code>learning_rate</code> و<code>num_leaves</code> و<code>min_child_samples</code>.</p>
<ul><li>البذرة: 211.</li><li>حد أقصى قدره ثماني تجارب متتابعة.</li><li>حد أقصى قدره 120 ثانية للبحث، مع إيقاف تعاوني قد ينتهي بعد الحد بقليل.</li><li><code>COMPLETE</code>: اكتملت درجات الطيات الثلاث.</li><li><code>PRUNED</code>: أوقفت التجربة مبكرًا.</li><li><code>FAIL</code>: لم تنتج المحاولة هدفًا مكتملًا؛ ولا تُعامل القيم الجزئية بوصفها متوسطًا مكتملًا.</li></ul>
<p>إذا لم تكتمل أي تجربة، يعرض الدفتر <code>EDUCATIONAL_EXAMPLE</code> محفوظًا للنقاش فقط ويظهر <code>TUNING_REQUIRED</code>. لا يُنسخ المثال إلى نتائجك الفعلية أو تسليمك. أعد المحاولة لاحقًا في جلسة CPU مجانية جديدة بدل شراء موارد حوسبة.</p>
""",
    },
    "7431ec58": {
        "pair_id": "day2_comparison",
        "en_title": "6. Compare only after search is frozen",
        "ar_title": "6. قارن بعد تجميد البحث",
        "en_body": """
<p>Every protocol uses LightGBM, but the data protocol changes:</p>
<table><tr><th>Protocol</th><th>Purpose</th></tr><tr><td>Leaky random control</td><td>Deliberately uses two post-outcome fields and all-row imputation; unsafe negative control</td></tr><tr><td>Clean random control</td><td>Uses eligible fields and training-only imputation but still mixes time and customers; unsafe for decisions</td></tr><tr><td>Honest fixed</td><td>Uses forward mature-label, customer-purged folds with the fixed base parameters and 80 trees</td></tr><tr><td>Honest reserved search</td><td>Uses the same honest outer folds with parameters frozen on the separate search cohort and internal tree selection</td></tr></table>
<p>The random protocols cover 10,000 requests; the time-based protocols cover 5,039 later eligible requests and use different training sizes. Gaps are descriptive and combine period, population and data-availability differences. They are not isolated causal estimates of leakage.</p>
""",
        "ar_body": """
<p>تستخدم جميع البروتوكولات LightGBM، لكن بروتوكول البيانات يتغير:</p>
<table><tr><th>البروتوكول</th><th>الغرض</th></tr><tr><td>Leaky random control</td><td>يستخدم عمدًا خاصيتين بعد النتيجة وتعويضًا من كامل البيانات؛ ضابط سلبي غير آمن</td></tr><tr><td>Clean random control</td><td>يستخدم الخصائص المؤهلة وتعويض التدريب فقط، لكنه يخلط الزمن والعملاء؛ غير صالح للقرار</td></tr><tr><td>Honest fixed</td><td>يستخدم طيات زمنية ناضجة الأهداف ومستبعدة العملاء مع الإعداد الأساسي الثابت و80 شجرة</td></tr><tr><td>Honest reserved search</td><td>يستخدم الطيات الخارجية الصادقة نفسها مع معاملات مجمدة من مجموعة البحث واختيار داخلي لعدد الأشجار</td></tr></table>
<p>تغطي البروتوكولات العشوائية 10,000 طلب، بينما تغطي البروتوكولات الزمنية 5,039 طلبًا لاحقًا مؤهلًا وبأحجام تدريب مختلفة. الفروق وصفية وتجمع اختلافات الفترة والسكان والبيانات المتاحة، وليست تقديرًا سببيًا مستقلًا للتسرب.</p>
""",
    },
    "bf425604": {
        "pair_id": "day2_variation",
        "en_title": "Read mean and variation together",
        "ar_title": "اقرأ المتوسط والتشتت معًا",
        "en_body": """
<p>The reported score is the unweighted mean across three folds. Error bars show the sample standard deviation with <code>ddof=1</code>.</p>
<ul><li>The folds are related time periods, not three independent experiments.</li><li>The error bar is not a confidence interval and not a significance test.</li><li>AP means <strong>Average Precision</strong>, not trapezoidal area under the precision–recall curve.</li><li>Read fold size, positive rate and coverage beside the headline metrics.</li></ul>
<p>Selected tree counts or the last decimal places can differ across systems even with pinned versions. Do not repeat search because an outer-validation number is disappointing; repeated selection on outer folds converts them into development data.</p>
""",
        "ar_body": """
<p>الدرجة المعروضة هي المتوسط غير الموزون للطيات الثلاث. وتمثل أشرطة الخطأ الانحراف المعياري العيّني باستخدام <code>ddof=1</code>.</p>
<ul><li>الطيات فترات زمنية مترابطة وليست ثلاث تجارب مستقلة.</li><li>شريط الخطأ ليس فترة ثقة ولا اختبار دلالة.</li><li>يشير AP إلى <strong>Average Precision</strong> وليس المساحة شبه المنحرفة تحت منحنى precision–recall.</li><li>اقرأ حجم الطية ونسبة الفئة الموجبة والتغطية بجانب المقاييس الرئيسية.</li></ul>
<p>قد يختلف عدد الأشجار المختار أو آخر المنازل العشرية بين الأنظمة رغم تثبيت الإصدارات. لا تُعد البحث لأن رقم التحقق الخارجي لم يعجبك؛ فالاختيار المتكرر على الطيات الخارجية يحولها إلى بيانات تطوير.</p>
""",
    },
    "f864dd58": {
        "pair_id": "day2_oof",
        "en_title": "7. Verify out-of-fold coverage",
        "ar_title": "7. تحقّق من تغطية OOF",
        "en_body": """
<p>Every saved probability is generated for an application outside the corresponding fold's training rows after its internal choices are fixed.</p>
<ul><li>Each successful honest scheme produces 5,039 OOF probabilities.</li><li>The remaining 4,961 applications are warm-up rows without OOF predictions.</li><li>Coverage is 50.39% of all clean training rows and 100% of requests eligible from 2023-07-01 onward.</li><li>Do not fill warm-up rows with training predictions or artificial probabilities.</li><li>Do not export the leaky-control predictions for later decision work.</li></ul>
<p>This OOF set is not an independent final test and does not guarantee fairness or calibration. Preserve each row's role so later decisions use declared coverage.</p>
""",
        "ar_body": """
<p>يُنتج كل احتمال محفوظ لطلب خارج صفوف تدريب الطية المقابلة بعد تثبيت خياراتها الداخلية.</p>
<ul><li>ينتج كل إعداد صادق ناجح 5,039 احتمال OOF.</li><li>تبقى الطلبات البالغ عددها 4,961 صفوف تمهيد بلا تنبؤات OOF.</li><li>تبلغ التغطية 50.39% من جميع صفوف التدريب النظيفة و100% من الطلبات المؤهلة بدءًا من 2023-07-01.</li><li>لا تملأ صفوف التمهيد بتنبؤات التدريب أو احتمالات مصطنعة.</li><li>لا تصدّر تنبؤات الضابط المتسرب لأعمال القرار اللاحقة.</li></ul>
<p>لا تمثل مجموعة OOF اختبارًا نهائيًا مستقلًا، ولا تضمن العدالة أو المعايرة. احتفظ بدور كل صف حتى تُبنى القرارات اللاحقة على تغطية معلنة.</p>
""",
    },
    "28602abc": {
        "pair_id": "day2_reasoning",
        "en_title": "8. Write your own validation argument",
        "ar_title": "8. اكتب حجتك الخاصة للتحقق",
        "en_body": """
<p>Complete the shared response dictionary in your own words, then rerun the response and export cells:</p>
<ol><li>Name one leaked field and explain why its information was unavailable at application time.</li><li>Justify time ordering, customer separation and the strict 90-day maturity rule.</li><li>Cite two numerical gaps from your validation table and explain why they do not prove universal superiority.</li><li>Explain why imputation is learned inside training and what the inner stopping set controls.</li><li>State one search-budget limitation and one OOF-coverage or fold-dependence limitation.</li></ol>
<p>The checkpoint detects missing fields only. It does not write your answer, judge correctness, award a grade or prove authorship.</p>
""",
        "ar_body": """
<p>أكمل قاموس الإجابات المشترك بصياغتك أنت، ثم أعد تشغيل خلية الإجابات وخلية التصدير:</p>
<ol><li>اذكر خاصية متسربة، واشرح لماذا لم تكن معلومتها متاحة وقت تقديم الطلب.</li><li>برر ترتيب الزمن وفصل العملاء وقاعدة نضج الهدف الصارمة لمدة 90 يومًا.</li><li>استشهد بفجوتين رقميتين من جدول التحقق، واشرح لماذا لا تثبتان تفوقًا عامًا.</li><li>اشرح لماذا يُتعلم التعويض داخل التدريب وما الذي يتحكم فيه جزء الإيقاف الداخلي.</li><li>اذكر قيدًا في ميزانية البحث وقيدًا في تغطية OOF أو اعتماد الطيات.</li></ol>
<p>يفحص الحارس اكتمال الخانات فقط؛ لا يكتب إجابتك، ولا يحكم على صحتها، ولا يمنح درجة، ولا يثبت الملكية.</p>
""",
    },
    "b2ad2797": {
        "pair_id": "day2_export",
        "en_title": "9. Export evidence and preserve provenance",
        "ar_title": "9. صدّر الأدلة واحتفظ بمصدرها",
        "en_body": """
<p>The export cell writes the validation tables, search record, audits, OOF predictions and coverage, provenance, reflection, run metadata, three figures and <code>environment.json</code>, then creates <code>day2_artifacts.zip</code>.</p>
<p>Download the ZIP from <strong>Files → tamweel → artifacts</strong>, extract it and upload the actual files to your repository's <code>artifacts/</code> directory. Save the executed notebook as <code>notebooks/02_validation_tuning.ipynb</code>.</p>
<ul><li><code>TECHNICAL_READY</code>: execution and at least one live tuning trial completed.</li><li><code>TUNING_REQUIRED</code>: no live trial completed; rerun is required.</li><li><code>LEARNER_WORK_REQUIRED</code>: technical work exists, but your written fields are incomplete.</li><li><code>READY_FOR_REVIEW</code>: required fields are present; this is not a grade or correctness guarantee.</li></ul>
<p>Saving again replaces this day's artifact names. Preserve a copy before rerunning. Never upload credentials, access tokens or personal data.</p>
""",
        "ar_body": """
<p>تكتب خلية التصدير جداول التحقق وسجل البحث والتدقيقات وتنبؤات OOF وتغطيتها ومصدر التدريب والتفسير وبيانات التشغيل وثلاثة رسوم و<code>environment.json</code>، ثم تنشئ <code>day2_artifacts.zip</code>.</p>
<p>نزّل الحزمة من <strong>Files → tamweel → artifacts</strong>، وافكها، وارفع الملفات الفعلية إلى مجلد <code>artifacts/</code> في مستودعك. واحفظ الدفتر المنفذ باسم <code>notebooks/02_validation_tuning.ipynb</code>.</p>
<ul><li><code>TECHNICAL_READY</code>: نجح التنفيذ واكتملت تجربة ضبط فعلية واحدة على الأقل.</li><li><code>TUNING_REQUIRED</code>: لم تكتمل تجربة فعلية؛ يلزم إعادة التشغيل.</li><li><code>LEARNER_WORK_REQUIRED</code>: توجد الأدلة التقنية، لكن حقولك الكتابية غير مكتملة.</li><li><code>READY_FOR_REVIEW</code>: الحقول المطلوبة موجودة؛ ولا تمثل درجة أو ضمانًا لصحة التفسير.</li></ul>
<p>يستبدل الحفظ المتكرر أسماء ملفات هذا اليوم. احتفظ بنسخة قبل إعادة التشغيل. لا ترفع بيانات اعتماد أو رموز وصول أو بيانات شخصية.</p>
""",
    },
    "4fa5ff55": {
        "pair_id": "day2_completion",
        "en_title": "Completion checkpoint and next step",
        "ar_title": "نقطة الإكمال والخطوة التالية",
        "en_body": """
<ul><li>You can identify the removed post-outcome fields and explain their availability time.</li><li>Each fold shows zero shared customers and mature training labels before validation starts.</li><li>You can distinguish attempted, completed, pruned and failed search trials.</li><li>You read fold means, sample standard deviations, population differences and OOF coverage together.</li><li>You completed the five learner-owned responses and saved the executed notebook plus the artifact bundle outside the temporary session.</li></ul>
<p><strong>Before presenting results:</strong> show one leakage example, point to evidence of customer separation and label maturity, distinguish mean fold AP from pooled AP, and state the result's limits beside the score.</p>
<p><strong>References:</strong> scikit-learn cross-validation and preprocessing-leakage guidance, LightGBM early stopping and Optuna bounded-study documentation linked in the course guide.</p>
<p><strong>Day 3:</strong> use the honest validation foundation to examine simulated decision costs, thresholds and the consequences of false approvals and false declines.</p>
""",
        "ar_body": """
<ul><li>تستطيع تحديد خصائص ما بعد النتيجة المحذوفة وشرح زمن إتاحة معلوماتها.</li><li>تُظهر كل طية صفر عملاء مشتركين ونضج أهداف التدريب قبل بدء التحقق.</li><li>تستطيع التمييز بين محاولات البحث والمكتمل منها والموقوفة والفاشلة.</li><li>تقرأ متوسطات الطيات والانحرافات المعيارية العيّنية واختلاف السكان وتغطية OOF معًا.</li><li>أكملت الإجابات الخمس التي يملكها المتدرب، وحفظت الدفتر المنفذ وحزمة الأدلة خارج الجلسة المؤقتة.</li></ul>
<p><strong>قبل عرض النتائج:</strong> اعرض مثالًا للتسرب، وأشر إلى دليل فصل العملاء ونضج الهدف، وميّز بين متوسط AP عبر الطيات وAP بعد جمع الاحتمالات، وضع حدود النتيجة بجانب الدرجة.</p>
<p><strong>المراجع:</strong> إرشادات scikit-learn للتحقق ومنع تسرب المعالجة، وتوثيق LightGBM للإيقاف المبكر، وتوثيق Optuna للبحث المحدود، وكلها مرتبطة في دليل الدورة.</p>
<p><strong>اليوم الثالث:</strong> استخدم أساس التحقق الصادق لفحص تكاليف القرار التعليمية والعتبات وآثار الموافقات الخاطئة والرفض الخاطئ.</p>
""",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--notebook",
        type=Path,
        default=Path("notebooks/02_validation_tuning.ipynb"),
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("content/day2_notebook_code_contract.json"),
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
        raise RuntimeError(f"Missing expected Day 2 markdown cells: {missing_sections}")

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
