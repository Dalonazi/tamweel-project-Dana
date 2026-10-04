"""Convert Day 1 learner markdown to a paired bilingual layout without changing code."""
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


def paired_cell(pair_id: str, en_title: str, en_body: str, ar_title: str, ar_body: str) -> dict[str, Any]:
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
    "bcfdd218": {
        "pair_id": "day1_header",
        "en_title": "Day 1 · Build a baseline and compare boosting",
        "ar_title": "اليوم الأول · ابنِ خط أساس وقارن نماذج التعزيز",
        "en_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · 60-minute lab · Free CPU</strong></p>
<p>Train Logistic Regression, XGBoost and LightGBM on the same development and comparison rows. Compare ranking quality and training time, then select an initial candidate using evidence from your own run.</p>
<p><strong>Deliverables:</strong> model-comparison CSV, prediction evidence, split membership, learning curves, ROC/precision–recall figure, run metadata and your written decision.</p>
<p><strong>Important boundary:</strong> the stratified random split is a temporary teaching baseline. It does not separate repeated customers or reproduce time and target-maturity boundaries. Do not present these scores as a deployment estimate. Day 2 replaces this design with honest validation.</p>
<table><tr><th>Minutes</th><th>Your task</th></tr><tr><td>0–12</td><td>Prepare the CPU environment and inspect data</td></tr><tr><td>12–38</td><td>Fit the baseline and select boosting rounds</td></tr><tr><td>38–48</td><td>Compare metrics and curves</td></tr><tr><td>48–60</td><td>Write your decision and export evidence</td></tr></table>
""",
        "ar_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · لاب 60 دقيقة · CPU مجاني</strong></p>
<p>درّب Logistic Regression وXGBoost وLightGBM على صفوف التطوير والمقارنة نفسها. قارن جودة ترتيب المخاطر وزمن التدريب، ثم اختر مرشحًا أوليًا اعتمادًا على أدلة تشغيلك أنت.</p>
<p><strong>المخرجات:</strong> ملف مقارنة النماذج، وأدلة التنبؤ، وعضوية التقسيم، ومنحنيات التعلم، ورسم ROC وprecision–recall، وبيانات التشغيل، وقرارك المكتوب.</p>
<p><strong>حد مهم:</strong> التقسيم العشوائي الطبقي خط أساس تعليمي مؤقت؛ لا يفصل العملاء المتكررين ولا يحاكي حدود الزمن ونضج الهدف. لا تعرض هذه الدرجات بوصفها تقديرًا للنشر. سيستبدل اليوم الثاني هذا التصميم بتحقق صادق.</p>
<table><tr><th>الدقائق</th><th>مهمتك</th></tr><tr><td>0–12</td><td>جهّز بيئة CPU وافحص البيانات</td></tr><tr><td>12–38</td><td>درّب خط الأساس واختر جولات التعزيز</td></tr><tr><td>38–48</td><td>قارن المقاييس والمنحنيات</td></tr><tr><td>48–60</td><td>اكتب قرارك وصدّر الأدلة</td></tr></table>
""",
    },
    "53ce6e4f": {
        "pair_id": "day1_setup",
        "en_title": "1. Prepare the environment",
        "ar_title": "1. جهّز بيئة التشغيل",
        "en_body": """
<p>Select <strong>Runtime → Run all</strong> using the free CPU runtime. The setup downloads pinned course files, verifies SHA-256 hashes and retries temporary network failures.</p>
<ul><li><code>FAST_MODE=True</code>: up to 300 trees and two CPU threads; use this first.</li><li><code>FULL_MODE=True</code>: optional cap of 900 trees after saving the baseline run.</li><li>No GPU, API key, Drive mount or paid subscription is required.</li></ul>
<p><strong>Pass condition:</strong> the setup prints <code>Day 1 setup verified</code>. A checksum or imported-version failure must not be bypassed; restart the session and run from the beginning.</p>
""",
        "ar_body": """
<p>اختر <strong>Runtime → Run all</strong> باستخدام CPU المجاني. ينزّل الإعداد ملفات الدورة ذات الإصدارات المثبتة، ويتحقق من بصمات SHA-256، ويعيد محاولة أخطاء الشبكة المؤقتة.</p>
<ul><li><code>FAST_MODE=True</code>: حتى 300 شجرة وخيطَي CPU؛ ابدأ به.</li><li><code>FULL_MODE=True</code>: سقف اختياري يبلغ 900 شجرة بعد حفظ تجربة الأساس.</li><li>لا تحتاج إلى GPU أو مفتاح API أو ربط Drive أو اشتراك مدفوع.</li></ul>
<p><strong>شرط الاجتياز:</strong> ظهور <code>Day 1 setup verified</code>. لا تتجاوز فشل البصمة أو اختلاف إصدار مستورد؛ أعد تشغيل الجلسة ثم شغّل الدفتر من البداية.</p>
""",
    },
    "9ebfdcfc": {
        "pair_id": "day1_data",
        "en_title": "2. Understand the task and data",
        "ar_title": "2. افهم المهمة والبيانات",
        "en_body": """
<p>All records are synthetic. The target <code>default_within_90d</code> records whether a default event occurs within 90 days after the application; it does not mean a delay of exactly 90 days.</p>
<ul><li>Use 22 features available at application time.</li><li>Exclude identifiers, dates, split-control columns and the target from model inputs.</li><li>Learn missing-value imputation from training rows only.</li><li>Do not use challenge data in this lab.</li></ul>
<p><strong>Learner checkpoint:</strong> write the outcome being estimated, the decision time and the intended teaching use. This simulation must not drive real financing decisions.</p>
""",
        "ar_body": """
<p>جميع السجلات اصطناعية. يسجل الهدف <code>default_within_90d</code> ما إذا وقع حدث تعثر خلال 90 يومًا بعد الطلب؛ ولا يعني تأخرًا مدته 90 يومًا بالضبط.</p>
<ul><li>استخدم 22 خاصية متاحة وقت تقديم الطلب.</li><li>استبعد المعرّفات والتواريخ وأعمدة التحكم في التقسيم والهدف من مدخلات النموذج.</li><li>تعلّم تعويض القيم المفقودة من صفوف التدريب فقط.</li><li>لا تستخدم بيانات التحدي في هذا اللاب.</li></ul>
<p><strong>نقطة تعلم:</strong> اكتب النتيجة التي تقدرها، ولحظة اتخاذ القرار، والاستخدام التعليمي المقصود. لا تُستخدم هذه المحاكاة لاتخاذ قرارات تمويل فعلية.</p>
""",
    },
    "08b5235a": {
        "pair_id": "day1_roles",
        "en_title": "3. Separate data roles before fitting",
        "ar_title": "3. افصل أدوار البيانات قبل التدريب",
        "en_body": """
<p>The 10,000 applications have distinct roles:</p>
<table><tr><th>Role</th><th>Rows</th><th>Purpose</th></tr><tr><td>Inner fit</td><td>6,000</td><td>Fit preprocessing and trees while selecting their count</td></tr><tr><td>Inner stop</td><td>2,000</td><td>Select the number of trees using log loss</td></tr><tr><td>Development</td><td>8,000</td><td>Refit each model after internal decisions are fixed</td></tr><tr><td>Comparison</td><td>2,000</td><td>Score all models once after fitting</td></tr></table>
<p>The inner sets are contained inside development; they are not extra data. The comparison set must not be used for early stopping or repeated tuning. This separation improves the teaching comparison, but customer and time leakage remain intentionally unresolved until Day 2.</p>
""",
        "ar_body": """
<p>للطلبات البالغ عددها 10,000 أدوار منفصلة:</p>
<table><tr><th>الدور</th><th>الصفوف</th><th>الغرض</th></tr><tr><td>Inner fit</td><td>6,000</td><td>تعلم المعالجة والأشجار أثناء اختيار عددها</td></tr><tr><td>Inner stop</td><td>2,000</td><td>اختيار عدد الأشجار باستخدام log loss</td></tr><tr><td>Development</td><td>8,000</td><td>إعادة تدريب كل نموذج بعد تثبيت القرارات الداخلية</td></tr><tr><td>Comparison</td><td>2,000</td><td>تقييم جميع النماذج مرة واحدة بعد التدريب</td></tr></table>
<p>المجموعتان الداخليتان جزء من التطوير وليستا بيانات إضافية. لا تستخدم مجموعة المقارنة للإيقاف المبكر أو الضبط المتكرر. يحسن هذا الفصل المقارنة التعليمية، لكن تسرب العميل والزمن يبقيان دون معالجة عمدًا حتى اليوم الثاني.</p>
""",
    },
    "4500d7ee": {
        "pair_id": "day1_baseline",
        "en_title": "4. Start with a simple baseline",
        "ar_title": "4. ابدأ بخط أساس بسيط",
        "en_body": """
<p>The baseline is a single Pipeline: median imputation, feature scaling and Logistic Regression. Every learned preprocessing value comes from development rows only.</p>
<p><strong>Why it matters:</strong> a more complex model must demonstrate value over a credible simple reference. Complexity is not evidence of improvement.</p>
<p><strong>Observe:</strong> training time, ROC-AUC and Average Precision. Do not reject the baseline merely because it does not use trees.</p>
""",
        "ar_body": """
<p>خط الأساس Pipeline واحدة تجمع التعويض بالوسيط وتوحيد المقاييس وLogistic Regression. تُتعلم جميع قيم المعالجة من صفوف التطوير فقط.</p>
<p><strong>لماذا يهم؟</strong> يجب أن يثبت النموذج الأكثر تعقيدًا قيمة تتجاوز مرجعًا بسيطًا وموثوقًا. التعقيد وحده ليس دليلًا على التحسن.</p>
<p><strong>راقب:</strong> زمن التدريب وROC-AUC وAverage Precision. لا تستبعد خط الأساس لمجرد أنه لا يستخدم الأشجار.</p>
""",
    },
    "f1f9043b": {
        "pair_id": "day1_boosting",
        "en_title": "5. Compare boosting with early stopping",
        "ar_title": "5. قارن التعزيز باستخدام الإيقاف المبكر",
        "en_body": """
<p>Boosting adds trees sequentially to reduce the objective. Under logistic classification, tree contributions accumulate in log-odds space before conversion to probability; the model is not directly summing tree probabilities.</p>
<table><tr><th>Control</th><th>What to observe</th></tr><tr><td><code>learning_rate</code></td><td>Contribution of each tree; a smaller value may require more trees</td></tr><tr><td><code>max_trees</code></td><td>Search ceiling, not a mandatory tree count</td></tr><tr><td><code>xgb_depth</code> / <code>lgb_leaves</code></td><td>Tree complexity</td></tr><tr><td><code>min_child_samples</code></td><td>Prevents very small LightGBM leaves</td></tr><tr><td><code>patience</code></td><td>Rounds without improvement in inner-stop log loss</td></tr></table>
<p><code>selected_trees</code> is one-based. Logistic Regression has no tree count. Class weights are intentionally deferred to a later lab.</p>
""",
        "ar_body": """
<p>يضيف التعزيز أشجارًا بالتتابع لتقليل دالة الهدف. في التصنيف اللوجستي تتراكم إسهامات الأشجار في فضاء log-odds قبل تحويلها إلى احتمال؛ ولا يجمع النموذج احتمالات الأشجار مباشرة.</p>
<table><tr><th>الإعداد</th><th>ما الذي تراقبه؟</th></tr><tr><td><code>learning_rate</code></td><td>مساهمة كل شجرة؛ قد تتطلب القيمة الأصغر أشجارًا أكثر</td></tr><tr><td><code>max_trees</code></td><td>سقف البحث وليس عددًا إلزاميًا</td></tr><tr><td><code>xgb_depth</code> / <code>lgb_leaves</code></td><td>تعقيد الأشجار</td></tr><tr><td><code>min_child_samples</code></td><td>يمنع أوراق LightGBM الصغيرة جدًا</td></tr><tr><td><code>patience</code></td><td>عدد الجولات دون تحسن في inner-stop log loss</td></tr></table>
<p>يبدأ <code>selected_trees</code> من 1. لا يوجد عدد أشجار لـLogistic Regression. تؤجل أوزان الفئات عمدًا إلى لاب لاحق.</p>
""",
    },
    "62c41b86": {
        "pair_id": "day1_learning_curves",
        "en_title": "Read the learning curves",
        "ar_title": "اقرأ منحنيات التعلم",
        "en_body": """
<p>The dashed line shows inner-stop loss. The vertical marker shows the selected tree count. Falling training loss alone is not enough.</p>
<ul><li>Identify where inner-stop loss stops improving.</li><li>Record whether the search reached the tree budget.</li><li>Do not infer general superiority from one curve.</li></ul>
<p>Plot labels remain concise English technical labels so exported figures render consistently across environments.</p>
""",
        "ar_body": """
<p>يمثل الخط المتقطع خسارة inner stop، وتحدد العلامة الرأسية عدد الأشجار المختار. انخفاض خسارة التدريب وحدها لا يكفي.</p>
<ul><li>حدد أين توقفت خسارة inner stop عن التحسن.</li><li>سجل ما إذا وصل البحث إلى سقف الأشجار.</li><li>لا تستنتج تفوقًا عامًا من منحنى واحد.</li></ul>
<p>تبقى عناوين الرسوم التقنية بالإنجليزية وبصياغة قصيرة لضمان ثبات عرض الملفات المصدّرة عبر البيئات المختلفة.</p>
""",
    },
    "ae6bf438": {
        "pair_id": "day1_comparison",
        "en_title": "6. Compare the three models fairly",
        "ar_title": "6. قارن النماذج الثلاثة بعدالة",
        "en_body": """
<p><strong>ROC-AUC</strong> summarizes ranking of positive versus negative cases across thresholds. <strong>Average Precision (AP)</strong> summarizes precision–recall performance and is especially useful when the positive class is uncommon. In this course, PR-AUC refers to scikit-learn Average Precision, not trapezoidal area.</p>
<p><code>train_seconds</code> includes tree-count selection and refitting for boosting models, and fitting for Logistic Regression. Download and plotting time are excluded. Timing is an observation from this run, not a hardware guarantee.</p>
<p>This single split has no confidence interval and does not establish calibration, operational value or general superiority. Simulated decision cost <code>10 × FN + FP</code> and 12% review capacity are introduced in a later decision lab.</p>
""",
        "ar_body": """
<p>يلخص <strong>ROC-AUC</strong> ترتيب الحالات الموجبة مقابل السالبة عبر العتبات. ويلخص <strong>Average Precision (AP)</strong> أداء precision–recall، ويكون مهمًا عند ندرة الفئة الموجبة. في هذه الدورة يشير PR-AUC إلى Average Precision في scikit-learn، وليس المساحة شبه المنحرفة.</p>
<p>يشمل <code>train_seconds</code> اختيار عدد الأشجار وإعادة التدريب لنماذج التعزيز، وتدريب Logistic Regression. لا يشمل زمن التنزيل والرسم. الزمن رصد لهذا التشغيل وليس ضمانًا على جهاز آخر.</p>
<p>لا تتضمن هذه التجربة الواحدة فترات ثقة، ولا تثبت المعايرة أو القيمة التشغيلية أو التفوق العام. ستُستخدم تكلفة القرار التعليمية <code>10 × FN + FP</code> وسعة مراجعة 12% في لاب قرار لاحق.</p>
""",
    },
    "3a1ed7c7": {
        "pair_id": "day1_curves",
        "en_title": "Read ROC and precision–recall together",
        "ar_title": "اقرأ ROC وprecision–recall معًا",
        "en_body": """
<p>The ROC reference line represents random ranking. The precision reference line equals the positive prevalence in the comparison sample.</p>
<ul><li>Compare curve separation, not only one headline number.</li><li>Inspect precision when recall is high.</li><li>Return to the table for exact values and sample context.</li></ul>
<p>A visually higher curve on one random split is evidence for this run only.</p>
""",
        "ar_body": """
<p>يمثل الخط المرجعي في ROC ترتيبًا عشوائيًا، بينما يساوي خط precision المرجعي نسبة الفئة الموجبة في عينة المقارنة.</p>
<ul><li>قارن تباعد المنحنيات، ولا تعتمد على رقم رئيس واحد فقط.</li><li>افحص precision عندما يكون recall مرتفعًا.</li><li>ارجع إلى الجدول للقيم الدقيقة وسياق حجم العينة.</li></ul>
<p>ارتفاع منحنى بصريًا على تقسيم عشوائي واحد دليل يخص هذا التشغيل فقط.</p>
""",
    },
    "d5aa2e63": {
        "pair_id": "day1_decision",
        "en_title": "7. Own the model-selection decision",
        "ar_title": "7. امتلك قرار اختيار النموذج",
        "en_body": """
<p>Complete the next shared code cell in your own words. There is no automatic winner and no model is required to win.</p>
<ol><li><strong>Problem statement:</strong> outcome, decision time and intended teaching use.</li><li><strong>Candidate:</strong> choose one of the three models.</li><li><strong>Evidence:</strong> cite a number or comparison from your run.</li><li><strong>Limitation:</strong> state what this experiment cannot prove.</li><li><strong>Next test:</strong> identify evidence that could change your choice.</li></ol>
<p><strong>Exit questions:</strong> Why inspect AP beside ROC-AUC under class imbalance? Why must the comparison set remain separate from early stopping?</p>
<p>The automated checkpoint detects empty fields only. It does not judge correctness, award a grade or prove authorship.</p>
""",
        "ar_body": """
<p>أكمل خلية الكود المشتركة التالية بصياغتك أنت. لا يوجد فائز تلقائي، ولا يُشترط أن يفوز نموذج محدد.</p>
<ol><li><strong>صياغة المشكلة:</strong> النتيجة ولحظة القرار والاستخدام التعليمي.</li><li><strong>المرشح:</strong> اختر أحد النماذج الثلاثة.</li><li><strong>الدليل:</strong> استشهد برقم أو مقارنة من تشغيلك.</li><li><strong>القيد:</strong> وضح ما لا تستطيع التجربة إثباته.</li><li><strong>الاختبار التالي:</strong> حدد دليلًا قد يغير اختيارك.</li></ol>
<p><strong>سؤالا الخروج:</strong> لماذا تفحص AP بجانب ROC-AUC عند عدم توازن الفئات؟ ولماذا يجب فصل مجموعة المقارنة عن الإيقاف المبكر؟</p>
<p>يكتشف الفحص الآلي الخانات الفارغة فقط؛ لا يحكم على صحة الإجابة ولا يمنح درجة ولا يثبت الملكية الفكرية.</p>
""",
    },
    "f238a809": {
        "pair_id": "day1_export",
        "en_title": "8. Export evidence, not screenshots",
        "ar_title": "8. صدّر الأدلة وليس لقطات الشاشة فقط",
        "en_body": """
<p>The export cell writes eight required files and creates <code>day1_artifacts.zip</code>. Download the ZIP, extract it and upload the actual files to <code>artifacts/</code>. Save the executed notebook in <code>notebooks/</code>.</p>
<ul><li><code>TECHNICAL_READY</code>: the models and evidence were produced.</li><li><code>LEARNER_WORK_REQUIRED</code>: technical execution passed, but your written fields remain incomplete.</li><li><code>READY_FOR_REVIEW</code>: required fields are present; this is not a grade or correctness guarantee.</li></ul>
<p>Copy your problem statement into your project README. Never upload access tokens, passwords or personal data.</p>
""",
        "ar_body": """
<p>تكتب خلية التصدير ثمانية ملفات إلزامية وتنشئ <code>day1_artifacts.zip</code>. نزّل الحزمة وافكها وارفع الملفات الفعلية إلى <code>artifacts/</code>. واحفظ الدفتر المنفذ داخل <code>notebooks/</code>.</p>
<ul><li><code>TECHNICAL_READY</code>: تم إنتاج النماذج والأدلة.</li><li><code>LEARNER_WORK_REQUIRED</code>: نجح التنفيذ التقني، لكن حقولك الكتابية غير مكتملة.</li><li><code>READY_FOR_REVIEW</code>: الحقول المطلوبة موجودة؛ ولا تمثل درجة أو ضمانًا لصحة التفسير.</li></ul>
<p>انسخ صياغة المشكلة إلى README الخاص بمشروعك. لا ترفع رموز الدخول أو كلمات المرور أو البيانات الشخصية.</p>
""",
    },
    "822b40ad": {
        "pair_id": "day1_completion",
        "en_title": "Completion checkpoint and next step",
        "ar_title": "نقطة الإكمال والخطوة التالية",
        "en_body": """
<ul><li>Three valid model rows appear in <code>day1_model_comparison.csv</code>.</li><li>You can explain development, inner stopping and comparison roles.</li><li>You selected one candidate and documented evidence, a limitation and a next test.</li><li>You saved the executed notebook and all eight artifacts outside the temporary Colab session.</li></ul>
<p><strong>Optional extension:</strong> after preserving the baseline, change <code>learning_rate</code> once with the same split. Document the impact on tree count and time. Repeatedly searching for the highest comparison score would convert the comparison set into a tuning set.</p>
<p><strong>Troubleshooting:</strong> retry setup after a download interruption; restart the session after an imported-version mismatch; restore original files after a checksum failure; never replace your outputs with another learner's table.</p>
<p><strong>Day 2:</strong> test customer separation, time ordering and target maturity, then reassess whether the first candidate remains credible.</p>
""",
        "ar_body": """
<ul><li>تظهر ثلاثة صفوف صالحة في <code>day1_model_comparison.csv</code>.</li><li>تستطيع شرح أدوار التطوير والإيقاف الداخلي والمقارنة.</li><li>اخترت مرشحًا ووثقت دليلًا وقيدًا واختبارًا تاليًا.</li><li>حفظت الدفتر المنفذ والملفات الثمانية خارج جلسة Colab المؤقتة.</li></ul>
<p><strong>توسع اختياري:</strong> بعد حفظ تجربة الأساس، غيّر <code>learning_rate</code> مرة واحدة مع التقسيم نفسه، ووثق أثره على عدد الأشجار والزمن. البحث المتكرر عن أعلى نتيجة يحول مجموعة المقارنة إلى مجموعة ضبط.</p>
<p><strong>حل التعثر:</strong> أعد خلية الإعداد عند انقطاع التنزيل؛ أعد تشغيل الجلسة عند اختلاف إصدار مستورد؛ استرجع الملفات الأصلية عند فشل البصمة؛ ولا تستبدل مخرجاتك بجدول متدرب آخر.</p>
<p><strong>اليوم الثاني:</strong> اختبر فصل العملاء وترتيب الزمن ونضج الهدف، ثم أعد تقييم مدى موثوقية المرشح الأول.</p>
""",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=Path, default=Path("notebooks/01_baseline_boosting.ipynb"))
    parser.add_argument("--contract", type=Path, default=Path("content/day1_notebook_code_contract.json"))
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
        raise RuntimeError(f"Missing expected Day 1 markdown cells: {missing_sections}")

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
