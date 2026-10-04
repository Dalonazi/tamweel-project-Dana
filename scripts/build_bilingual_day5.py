"""Convert Day 5 learner markdown to paired bilingual cells without changing code."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CONTENT_VERSION = "1.1.0"
REQUIRED_ORDER = "en-left-ar-right"
DEFAULT_NOTEBOOK = Path("notebooks/05_final_model.ipynb")
DEFAULT_CONTRACT = Path("content/day5_notebook_code_contract.json")


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
    "ba3659f2": {
        "pair_id": "day5_header",
        "en_title": "Day 5 · Choose what is worth shipping and deliver your project",
        "ar_title": "اليوم الخامس · اختر ما يستحق وسلّم مشروعك",
        "en_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · 60-minute lab · Free CPU</strong></p>
<p>Complete the same project. Compare three single models with equal averaging, weighted averaging and stacking, then decide whether complexity earns its place. Export a reproducible final model, <code>submission.csv</code>, a model card and a documented project bundle.</p>
<p><strong>Deliverables:</strong> nested-forward OOF evidence, ensemble decision, frozen policy, calibrated final model, challenge predictions, model card, project README and verified bundle.</p>
<p><strong>Boundary:</strong> <code>KEEP SINGLE</code> is a valid result when supported by evidence. The data are synthetic and cannot support real financing decisions. Technical completion is not a grade or a submission receipt.</p>
<table><tr><th>Minutes</th><th>Your task</th></tr><tr><td>0–10</td><td>Inspect data roles and OOF diversity</td></tr><tr><td>10–25</td><td>Compare averaging and nested stacking</td></tr><tr><td>25–35</td><td>Apply the worth-it gate and freeze the threshold</td></tr><tr><td>35–45</td><td>Freeze calibration and verify challenge predictions</td></tr><tr><td>45–55</td><td>Write the model card and merge earlier evidence</td></tr><tr><td>55–60</td><td>Download the bundle and save the executed notebook</td></tr></table>
""",
        "ar_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · لاب 60 دقيقة · CPU مجاني</strong></p>
<p>أكمل المشروع نفسه. قارن ثلاثة نماذج مفردة بمتوسط بسيط ومتوسط موزون وStacking، ثم قرر هل يستحق التعقيد مكانه. صدّر نموذجًا نهائيًا قابلًا لإعادة التشغيل وملف <code>submission.csv</code> وبطاقة نموذج وحزمة مشروع موثقة.</p>
<p><strong>التسليم:</strong> أدلة OOF أمامية متداخلة، وقرار التجميع، وسياسة مجمدة، ونموذج نهائي معاير، وتنبؤات التحدي، وبطاقة النموذج، وREADME المشروع، وحزمة متحقق منها.</p>
<p><strong>الحدود:</strong> نتيجة <code>KEEP SINGLE</code> صحيحة عندما تدعمها الأدلة. البيانات اصطناعية ولا تصلح لقرارات تمويل فعلية. الإكمال التقني ليس درجة أو إيصال تسليم.</p>
<table><tr><th>الدقائق</th><th>مهمتك</th></tr><tr><td>0–10</td><td>افحص أدوار البيانات وتنوع OOF</td></tr><tr><td>10–25</td><td>قارن المتوسط والتجميع المتداخل</td></tr><tr><td>25–35</td><td>طبّق بوابة الجدوى وثبّت العتبة</td></tr><tr><td>35–45</td><td>ثبّت المعايرة وتحقق من تنبؤات التحدي</td></tr><tr><td>45–55</td><td>اكتب بطاقة النموذج وادمج الأدلة السابقة</td></tr><tr><td>55–60</td><td>نزّل الحزمة واحفظ الدفتر المنفذ</td></tr></table>
""",
    },
    "786f76c4": {
        "pair_id": "day5_setup",
        "en_title": "1. Prepare a controlled environment",
        "ar_title": "1. جهّز بيئة تشغيل محكومة",
        "en_body": """
<p>Open a fresh free-CPU session and choose <strong>Runtime → Run all</strong>. Setup verifies package versions, source hashes and required assets. If a restart is requested, restart and run from the beginning.</p>
<ul><li>No GPU, Drive mount, payment or terminal command is required.</li><li>Use the primary live path. The labelled OOF example is discussion-only and cannot export a final model or submission.</li><li>Do not bypass a checksum failure or substitute another learner's evidence.</li></ul>
""",
        "ar_body": """
<p>افتح جلسة CPU مجانية جديدة ثم نفّذ <strong>Runtime → Run all</strong>. يتحقق الإعداد من إصدارات الحزم وبصمات المصادر والأصول المطلوبة. إذا طلب إعادة التشغيل، أعد الجلسة وشغّل من البداية.</p>
<ul><li>لا تحتاج إلى GPU أو ربط Drive أو دفع أو أوامر طرفية.</li><li>استخدم المسار الحي الأساسي. مثال OOF الموسوم للمناقشة فقط ولا يصدّر نموذجًا نهائيًا أو ملف تسليم.</li><li>لا تتجاوز فشل البصمة ولا تستبدل أدلتك بأدلة متدرب آخر.</li></ul>
""",
    },
    "67a54f85": {
        "pair_id": "day5_roles",
        "en_title": "2. Reserve calibration and respect label availability",
        "ar_title": "2. احجز المعايرة واحترم وقت إتاحة النتائج",
        "en_body": """
<p>The synthetic target is a default event within 90 days after application. July–September 2024 is calibration-only, and its customers are removed from the full fit-and-selection pool. The pool includes only applications whose outcomes matured before 1 July 2024.</p>
<p>Comparison folds are 2023Q1, 2023Q3 and 2024Q1. In every outer fold, training is earlier than validation by enough time for the 90-day outcome to mature, and validation customers are excluded from training. A second forward split inside outer training learns averaging weights and the logistic stacker.</p>
<p>The meta-model never learns from in-sample base predictions and is never evaluated on rows used to fit it. This OOF evidence supports development and selection; earlier course work has already used the training data, so it is not a final untouched test. Challenge labels are unavailable.</p>
""",
        "ar_body": """
<p>الهدف الاصطناعي هو وقوع حدث تعثر خلال 90 يومًا بعد الطلب. تُحجز يوليو–سبتمبر 2024 للمعايرة فقط، ويُستبعد عملاؤها من كامل حوض التدريب والاختيار. يضم الحوض الطلبات التي نضجت نتائجها قبل 1 يوليو 2024 فقط.</p>
<p>طيات المقارنة هي 2023Q1 و2023Q3 و2024Q1. في كل طية خارجية يكون التدريب أقدم من التحقق بما يكفي لنضج الهدف خلال 90 يومًا، ويُستبعد عملاء التحقق من التدريب. ويُستخدم تقسيم أمامي ثانٍ داخل التدريب الخارجي لتعلم الأوزان ونموذج Logistic الأعلى.</p>
<p>لا يتعلم النموذج الأعلى من تنبؤات داخل التدريب ولا يُقاس على الصفوف التي تعلم منها. تدعم أدلة OOF التطوير والاختيار؛ وقد استُخدمت بيانات التدريب سابقًا في الدورة، لذلك ليست اختبارًا نهائيًا لم يُمسّ. لا تتوفر تسميات التحدي.</p>
""",
    },
    "3c838b4d": {
        "pair_id": "day5_nested_stacking",
        "en_title": "3. Build nested forward OOF without leakage",
        "ar_title": "3. ابنِ OOF أماميًا متداخلًا دون تسرب",
        "en_body": """
<p>Compare unweighted LightGBM, XGBoost and Logistic Regression. Handle error cost later through the decision threshold. Imputation and scaling are learned inside training only.</p>
<p>Weighted averaging searches a small non-negative weight grid summing to one on <strong>inner OOF only</strong>. The logistic stacker learns from the same three inner-OOF columns. Base learners are then refit on the outer training data and all candidates are measured on the outer validation period.</p>
<p>Weights and coefficients may differ by fold; the object being compared is the learning procedure. If the CPU budget expires, a labelled educational matrix may appear. That mode exports no final model or submission, and assessment mode blocks it.</p>
""",
        "ar_body": """
<p>قارن LightGBM وXGBoost وLogistic Regression دون أوزان فئات، ثم عالج تكلفة الخطأ لاحقًا عبر عتبة القرار. يتعلم التعويض والتقييس داخل التدريب فقط.</p>
<p>يفحص المتوسط الموزون شبكة صغيرة من أوزان غير سالبة مجموعها واحد على <strong>OOF الداخلي فقط</strong>. ويتعلم نموذج Logistic الأعلى من الأعمدة الثلاثة الداخلية نفسها. ثم تُعاد ملاءمة النماذج الأساسية على التدريب الخارجي وتُقاس جميع الخيارات على فترة التحقق الخارجية.</p>
<p>قد تختلف الأوزان والمعاملات بين الطيات؛ ما نقارنه هو إجراء التعلم. إذا انتهت ميزانية CPU فقد يظهر مثال تعليمي موسوم. لا يصدّر هذا الوضع نموذجًا نهائيًا أو ملف تسليم، ويمنعه وضع التقييم.</p>
""",
    },
    "a60ff030": {
        "pair_id": "day5_diversity",
        "en_title": "4. Inspect prediction and residual diversity",
        "ar_title": "4. افحص تنوع الاحتمالات والبواقي",
        "en_body": """
<p>The first heatmap shows correlation among base-model OOF probabilities. The second shows correlation among residuals <code>p − y</code> on the same requests.</p>
<p>Residuals share the target and may remain highly correlated. Correlation is descriptive and does not establish causality. Low correlation alone does not prove ensemble gain and does not justify adding a weak model without measured improvement.</p>
""",
        "ar_body": """
<p>تعرض الخريطة الأولى ترابط احتمالات OOF للنماذج الأساسية، وتعرض الثانية ترابط البواقي <code>p − y</code> على الطلبات نفسها.</p>
<p>تشترك البواقي في الهدف وقد يبقى ترابطها مرتفعًا. الارتباط وصفي ولا يثبت السببية. كما أن الارتباط المنخفض وحده لا يثبت تحسن التجميع ولا يبرر إضافة نموذج ضعيف دون قياس.</p>
""",
    },
    "af6811cb": {
        "pair_id": "day5_worth_it",
        "en_title": "5. Apply the worth-it gate",
        "ar_title": "5. طبّق بوابة: هل يستحق التجميع؟",
        "en_body": """
<p>Select the best single model by mean <strong>Average Precision</strong> across the three forward folds. Accept an ensemble only when its AP gain exceeds that single model's fold standard deviation and Brier worsens by no more than 0.005 and ECE by no more than 0.01.</p>
<p>These thresholds are fixed educational rules, not grades, success rates or a significance test. The standard deviation describes only three periods, whose training histories overlap. It is not a confidence interval.</p>
<p>If several ensembles pass, prefer the simplest: equal average, then weighted average, then stack. Do not force an ensemble to win. Report Average Precision; do not replace it with trapezoidal PR area.</p>
""",
        "ar_body": """
<p>اختر أفضل نموذج مفرد وفق متوسط <strong>Average Precision</strong> عبر الطيات الأمامية الثلاث. اقبل التجميع فقط إذا تجاوز تحسن AP انحراف ذلك النموذج بين الطيات، ولم يسوء Brier بأكثر من 0.005 ولا ECE بأكثر من 0.01.</p>
<p>هذه حدود تعليمية ثابتة وليست درجات أو نسب نجاح أو اختبار دلالة. يصف الانحراف ثلاث فترات فقط تتشارك تاريخًا تدريبيًا؛ وليس فترة ثقة.</p>
<p>إذا اجتاز أكثر من تجميع فاختر الأبسط: المتوسط البسيط ثم الموزون ثم Stack. لا تجبر التجميع على الفوز. أبلغ Average Precision ولا تستبدله بمساحة PR شبه المنحرفة.</p>
""",
    },
    "c8fae7f7": {
        "pair_id": "day5_policy",
        "en_title": "6. Freeze the OOF decision policy",
        "ar_title": "6. جمّد سياسة القرار على OOF",
        "en_body": """
<p>Search every distinct selected-model OOF score for the minimum educational loss <strong>10 × FN + FP</strong>, subject to a 12% capacity ceiling in every fold and overall. Equal scores remain one block.</p>
<p>Loss units are fictional teaching units, not Saudi riyals, fees or grade deductions. Regional FPR tables are descriptive OOF diagnostics with denominators and positive counts; they are not a fairness certificate. Challenge FPR cannot be computed without labels.</p>
<p>The sensitivity table changes FN cost only while holding the model, threshold and decisions fixed.</p>
""",
        "ar_body": """
<p>افحص كل درجة OOF مميزة للنموذج المختار بحثًا عن أقل خسارة تعليمية <strong>10 × FN + FP</strong> ضمن سقف سعة 12% في كل طية وفي المجموع. تبقى الدرجات المتساوية كتلة واحدة.</p>
<p>وحدات الخسارة تعليمية افتراضية وليست ريالات سعودية أو رسومًا أو خصمًا من الدرجة. جداول FPR الإقليمية تدقيقات وصفية على OOF مع المقامات وعدد الموجبات؛ وليست شهادة عدالة. لا يمكن حساب FPR للتحدي دون تسميات.</p>
<p>يغيّر جدول الحساسية تكلفة FN فقط مع تثبيت النموذج والعتبة والقرارات.</p>
""",
    },
    "da2afff9": {
        "pair_id": "day5_final_fit",
        "en_title": "7. Refit the chosen procedure and freeze calibration",
        "ar_title": "7. أعد ملاءمة الإجراء المختار وثبّت المعايرة",
        "en_body": """
<p>Refit the chosen learning procedure on the eligible pool and learn one sigmoid mapping on the reserved calibration period only. Do not retrain the estimator afterward; an old calibrator and threshold would no longer match it.</p>
<p>Transport the raw OOF threshold to the calibrated scale when the mapping is monotone. The reliability figure is a <strong>calibration-fit diagnostic on the same rows used to learn the calibrator</strong>, not an independent evaluation.</p>
<p>Transporting a threshold from OOF models to a refitted model can change flag volume, so a full-batch capacity policy must be declared before looking at challenge outcomes. Day 4 SHAP explanations belong to the Day 4 model and must not be attributed automatically to a different final model or ensemble.</p>
""",
        "ar_body": """
<p>أعد ملاءمة إجراء التعلم المختار على الحوض المؤهل، وتعلم تحويل sigmoid واحدًا من فترة المعايرة المحجوزة فقط. لا تعِد تدريب النموذج بعدها؛ وإلا لم يعد المعاير والعتبة القديمان مطابقين له.</p>
<p>انقل عتبة OOF الخام إلى المقياس المعاير عندما يكون التحويل متزايدًا. رسم الموثوقية <strong>تشخيص ملاءمة على الصفوف نفسها التي تعلم منها المعاير</strong> وليس تقييمًا مستقلًا.</p>
<p>قد يغير نقل العتبة من نماذج OOF إلى نموذج معاد التدريب حجم الإشارات، لذلك يجب إعلان سياسة سعة للدفعة الكاملة قبل رؤية نتائج التحدي. تفسيرات SHAP في اليوم الرابع تخص نموذج اليوم الرابع ولا تُنسب تلقائيًا إلى نموذج نهائي أو تجميع مختلف.</p>
""",
    },
    "27c3b0cb": {
        "pair_id": "day5_challenge",
        "en_title": "8. Score every challenge request and apply capacity once",
        "ar_title": "8. صدّر كل طلب وطبّق السعة مرة واحدة",
        "en_body": """
<p><code>inference.predict</code> returns application ID and calibrated probability while preserving request order. Probabilities may be computed in chunks, but concatenate all chunks before applying the full-batch policy once.</p>
<p>Candidates exceed the transported threshold. If they exceed 12% of the 2,500-request batch, keep the highest probabilities up to the 300-request ceiling. Never split an equal-score block with the identifier; if the whole boundary block does not fit, exclude it and leave capacity unused.</p>
<p><code>decision=1</code> is a simulated review flag. <code>decision=0</code> is not a safety guarantee or financing approval. Challenge AP, loss and FPR are not computed because labels are unavailable. Models are exported in JSON/native formats rather than untrusted pickle files.</p>
""",
        "ar_body": """
<p>تعيد <code>inference.predict</code> معرف الطلب والاحتمال المعاير مع الحفاظ على ترتيب الطلبات. يمكن حساب الاحتمالات على أجزاء، لكن اجمع الأجزاء كلها قبل تطبيق سياسة الدفعة الكاملة مرة واحدة.</p>
<p>المرشحون هم من يتجاوزون العتبة المنقولة. إذا تجاوزوا 12% من دفعة تضم 2,500 طلب، احتفظ بالأعلى احتمالًا حتى سقف 300 طلب. لا تقسّم كتلة درجات متساوية باستخدام المعرّف؛ إذا لم تتسع كتلة الحد كاملة فاستبعدها واترك جزءًا من السعة دون استخدام.</p>
<p><code>decision=1</code> إشارة مراجعة محاكاة، و<code>decision=0</code> ليس ضمان سلامة أو قبول تمويل. لا تُحسب AP أو الخسارة أو FPR للتحدي لغياب التسميات. تُصدّر النماذج بصيغ JSON/native بدل ملفات pickle غير الموثوقة.</p>
""",
    },
    "9e751e4c": {
        "pair_id": "day5_project",
        "en_title": "9. Write your decision and assemble your evidence",
        "ar_title": "9. اكتب قرارك واجمع أدلتك",
        "en_body": """
<p>Complete every response field using your measured values. Tables alone are not an interpretation, and response completeness permits review but does not award a grade.</p>
<p>If the final model differs from Day 4, state that Day 4 explanations belong to that earlier model and identify what must be rechecked for the final version.</p>
<p>You may upload your actual <code>day1_artifacts.zip</code> through <code>day4_artifacts.zip</code> to the displayed Colab working folder. The exporter imports them under <code>evidence/day1/</code> through <code>evidence/day4/</code> without overwriting model code. Do not use a peer's bundle or the educational example as your personal run evidence.</p>
<p>Add executed notebooks and a five-slide PDF presentation when available. Do not publish your full name, grade or private data in a public repository.</p>
""",
        "ar_body": """
<p>أكمل جميع حقول الإجابات باستخدام القيم التي قستها. الجداول وحدها ليست تفسيرًا، واكتمال الإجابات يسمح بالمراجعة لكنه لا يمنح درجة.</p>
<p>إذا اختلف النموذج النهائي عن اليوم الرابع، فاذكر أن تفسيرات اليوم الرابع تخص النموذج السابق وحدد ما يلزم إعادة فحصه للنسخة النهائية.</p>
<p>يمكنك رفع حزمك الفعلية <code>day1_artifacts.zip</code> إلى <code>day4_artifacts.zip</code> في مجلد عمل Colab المعروض. يستوردها المصدّر تحت <code>evidence/day1/</code> حتى <code>evidence/day4/</code> دون الكتابة فوق شيفرة النموذج. لا تستخدم حزمة زميل أو المثال التعليمي كدليل تشغيل شخصي.</p>
<p>أضف الدفاتر المنفذة وعرض PDF من خمس شرائح عند توفرها. لا تنشر اسمك الكامل أو درجتك أو بيانات خاصة في مستودع عام.</p>
""",
    },
    "c51da0a3": {
        "pair_id": "day5_export",
        "en_title": "10. Export and verify the project bundle",
        "ar_title": "10. صدّر حزمة المشروع وتحقق منها",
        "en_body": """
<p>The bundle stores permitted data, code, configuration, final model, predictions, reports and file hashes. <code>replay_final.py</code> reproduces predictions from the saved model; <code>rebuild_final.py</code> retrains, reselects and recalibrates from data.</p>
<p>Save the executed notebook as <code>notebooks/05_final_model.ipynb</code>. Download and extract the project ZIP, then upload the actual files while preserving directories; the ZIP alone is not the repository submission. Complete <code>PROJECT_README.md</code> and move its content into the project README.</p>
<p><code>BUNDLE_BYTES_VERIFIED</code> proves only that bundled files match their hashes. It is not project acceptance, a grade or a submission receipt. After the final commit, record your repository SHA and tag outside the manifest through the private submission channel to avoid a circular reference.</p>
""",
        "ar_body": """
<p>تحفظ الحزمة البيانات المسموح بها والشيفرة والإعدادات والنموذج النهائي والتنبؤات والتقارير وبصمات الملفات. يعيد <code>replay_final.py</code> التنبؤ من النموذج المحفوظ، ويعيد <code>rebuild_final.py</code> التدريب والاختيار والمعايرة من البيانات.</p>
<p>احفظ الدفتر المنفذ باسم <code>notebooks/05_final_model.ipynb</code>. نزّل ZIP المشروع وفكّه ثم ارفع الملفات الفعلية مع الحفاظ على المجلدات؛ ZIP وحده ليس تسليم المستودع. أكمل <code>PROJECT_README.md</code> وانقل محتواه إلى README المشروع.</p>
<p><code>BUNDLE_BYTES_VERIFIED</code> يثبت مطابقة الملفات للبصمات فقط. ليس قبولًا للمشروع أو درجة أو إيصال تسليم. بعد آخر commit سجّل SHA وtag لمستودعك خارج manifest عبر قناة التسليم الخاصة لتجنب المرجع الدائري.</p>
""",
    },
    "a9725592": {
        "pair_id": "day5_checkpoint",
        "en_title": "Final checkpoint before submission review",
        "ar_title": "بوابة الفحص قبل مراجعة التسليم",
        "en_body": """
<ul><li>Can you defend <strong>KEEP SINGLE / SHIP ENSEMBLE</strong> with your numbers without comparing training metrics to validation metrics?</li><li>Were ensemble weights and the meta-model learned from inner OOF only, with customer separation and label maturity?</li><li>Did you describe calibration metrics as fit diagnostics rather than independent challenge performance?</li><li>Does every challenge ID appear exactly once, and was capacity applied once to the full batch?</li><li>Are the model card, responses, earlier evidence and presentation complete?</li></ul>
<p>The assessment is 90 technical/administrative points plus 10 presentation points. Passing begins at 70 and distinction at 95 before rounding. This notebook awards no automatic grade and issues no receipt.</p>
<p>Run the free Notebook 99 final check after the files are complete. A successful check remains a technical preflight, not a grade or proof of receipt.</p>
""",
        "ar_body": """
<ul><li>هل تستطيع تبرير <strong>KEEP SINGLE / SHIP ENSEMBLE</strong> بأرقامك دون مقارنة مقاييس التدريب بمقاييس التحقق؟</li><li>هل تعلمت أوزان التجميع والنموذج الأعلى من OOF الداخلي فقط مع فصل العملاء ونضج التسميات؟</li><li>هل وصفت مقاييس المعايرة بأنها تشخيصات ملاءمة لا أداء مستقلًا للتحدي؟</li><li>هل ظهر كل معرف تحدٍّ مرة واحدة، وهل طُبقت السعة مرة واحدة على الدفعة الكاملة؟</li><li>هل اكتملت بطاقة النموذج والإجابات والأدلة السابقة والعرض؟</li></ul>
<p>التقييم 90 نقطة تقنية وإدارية و10 نقاط للعرض. يبدأ النجاح من 70 والتميز من 95 قبل التقريب. لا يمنح هذا الدفتر درجة آلية ولا يصدر إيصالًا.</p>
<p>شغّل دفتر 99 المجاني للفحص النهائي بعد اكتمال الملفات. نجاحه يظل فحصًا تقنيًا تمهيديًا لا درجة أو إثبات استلام.</p>
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
            raise RuntimeError(f"Unexpected Day 5 markdown cell: id={cell_id!r}, pair={pair_id!r}")

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
            f"Day 5 markdown coverage mismatch: "
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
        default=Path("check-output/day5-bilingual-build.json"),
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
