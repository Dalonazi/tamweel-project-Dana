"""Convert Notebook 00 markdown to the approved bilingual layout.

Executable cells are preserved byte-for-byte. The script is deterministic and
safe to run repeatedly on the development branch.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

NOTEBOOK = Path("notebooks/00_readiness_check.ipynb")
CONTENT_VERSION = "1.1.0"
ORDER = "en-left-ar-right"


def paired(en_title: str, en_body: str, ar_title: str, ar_body: str, heading: str = "h2") -> str:
    return f'''<table>
<tr>
<td width="50%" valign="top" dir="ltr">
<{heading}>{en_title}</{heading}>
{en_body}
</td>
<td width="50%" valign="top" dir="rtl">
<{heading}>{ar_title}</{heading}>
{ar_body}
</td>
</tr>
</table>'''


SECTIONS: dict[str, dict[str, str]] = {
    "30e8de0d": {
        "new_id": "readiness-header",
        "pair_id": "readiness_header",
        "source": paired(
            "Readiness Check",
            '''<p><strong>SDA-DSC-211 · Tamweel Lite · Notebook 00</strong></p>
<p>Spend <strong>30–40 minutes</strong> preparing your environment, inspecting the project data and completing six ungraded self-check questions.</p>
<p><strong>Outputs:</strong> <code>environment.json</code>, <code>data_check.json</code>, <code>runtime_checks.json</code> and <code>readiness_report.json</code>.</p>
<p>Use a free CPU runtime. No payment card, GPU, API key or Drive mount is required. Choose <strong>Runtime → Run all</strong>, then save the notebook and outputs before the session ends.</p>
<p>Prepared and delivered by <strong>Meaad Al-Marri</strong>.</p>''',
            "فحص الاستعداد",
            '''<p><strong>SDA-DSC-211 · Tamweel Lite · دفتر 00</strong></p>
<p>خصص <strong>30–40 دقيقة</strong> لتجهيز البيئة وفحص بيانات المشروع والإجابة عن ستة أسئلة للمراجعة الذاتية غير المحسوبة في الدرجة.</p>
<p><strong>المخرجات:</strong> <code>environment.json</code> و<code>data_check.json</code> و<code>runtime_checks.json</code> و<code>readiness_report.json</code>.</p>
<p>استخدم CPU المجاني. لا تحتاج إلى بطاقة دفع أو GPU أو مفتاح API أو ربط Drive. اختر <strong>Runtime → Run all</strong>، ثم احفظ الدفتر والمخرجات قبل انتهاء الجلسة.</p>
<p>إعداد وتقديم <strong>ميعاد المري</strong>.</p>''',
            "h1",
        ),
    },
    "154d386d": {
        "new_id": "readiness-setup",
        "pair_id": "readiness_setup",
        "source": paired(
            "1. Prepare the workspace",
            '''<p>Select <strong>CPU</strong> from <strong>Runtime → Change runtime type</strong>. Run the shared setup cell before importing course libraries.</p>
<p>The setup downloads a fixed course revision, verifies SHA-256 checksums, retries temporary network failures three times, limits CPU threads and installs only missing pinned versions.</p>
<p><strong>Do not bypass a checksum failure.</strong> If an imported version changed, restart the session and run all cells from the beginning.</p>''',
            "1. جهّز مساحة العمل",
            '''<p>اختر <strong>CPU</strong> من <strong>Runtime → Change runtime type</strong>. شغّل خلية الإعداد المشتركة قبل استيراد مكتبات الدورة.</p>
<p>ينزّل الإعداد نسخة دورة ثابتة، ويتحقق من بصمات SHA-256، ويعيد محاولة أخطاء الشبكة المؤقتة ثلاث مرات، ويحد خيوط CPU، ويثبت الإصدارات المفقودة فقط.</p>
<p><strong>لا تتجاوز فشل البصمة.</strong> عند اختلاف إصدار مستورد، أعد تشغيل الجلسة ثم شغّل جميع الخلايا من البداية.</p>''',
        ),
    },
    "20e10bd1": {
        "new_id": "readiness-data",
        "pair_id": "readiness_data",
        "source": paired(
            "2. Inspect the project data",
            '''<p>The training file contains <strong>10,000 rows and 22 model features</strong>. The challenge file contains <strong>2,500 rows without the target</strong>. All records are synthetic.</p>
<p><code>default_within_90d</code> means a default event within 90 days after the application. Identifiers, dates and split-control columns are not model features.</p>
<p><strong>Expected result:</strong> file sizes, missing-value counts and a successful contract/hash check. Execution stops if columns, hashes or challenge-label boundaries change.</p>''',
            "2. افحص بيانات المشروع",
            '''<p>يحتوي ملف التدريب على <strong>10,000 سجل و22 خاصية للنموذج</strong>. ويحتوي ملف التحدي على <strong>2,500 سجل دون الهدف</strong>. جميع السجلات اصطناعية.</p>
<p>يعني <code>default_within_90d</code> وقوع حدث تعثر خلال 90 يومًا بعد الطلب. لا تدخل المعرّفات والتواريخ وأعمدة التحكم في التقسيم ضمن خصائص النموذج.</p>
<p><strong>الناتج المتوقع:</strong> أحجام الملفات وعدد القيم الناقصة ونجاح فحص العقد والبصمات. يتوقف التنفيذ عند تغير الأعمدة أو البصمات أو حدود فصل إجابات التحدي.</p>''',
        ),
    },
    "baf762fe": {
        "new_id": "readiness-essentials",
        "pair_id": "readiness_essentials",
        "source": paired(
            "3. Four essentials you will use every day",
            '''<ul>
<li><strong>Classification:</strong> predicting class 0 or 1 is not the same as estimating probability.</li>
<li><strong><code>predict_proba</code>:</strong> returns an estimated probability between 0 and 1, not a guarantee.</li>
<li><strong>Train / validation / test:</strong> learn from training, choose decisions with validation, and preserve final evaluation independence.</li>
<li><strong>Confusion matrix:</strong> counts TP, TN, FP and FN after a threshold converts scores into flags.</li>
</ul>
<p><strong>Learning example:</strong> 3 missed defaults and 20 false alarms under <code>10 × FN + FP</code> produce 50 simulated decision-cost units. This is not a real monetary loss or a 50-point grade deduction.</p>''',
            "3. أربع أفكار ستستخدمها يوميًا",
            '''<ul>
<li><strong>التصنيف:</strong> تقدير الفئة 0 أو 1 يختلف عن تقدير الاحتمال.</li>
<li><strong><code>predict_proba</code>:</strong> يعيد احتمالًا مقدرًا بين 0 و1، وليس ضمانًا.</li>
<li><strong>التدريب والتحقق والاختبار:</strong> تعلّم من التدريب، واختر القرارات بالتحقق، وحافظ على استقلال التقييم النهائي.</li>
<li><strong>مصفوفة الالتباس:</strong> تعد TP وTN وFP وFN بعد تحويل الدرجات إلى إشارات باستخدام عتبة.</li>
</ul>
<p><strong>مثال تعليمي:</strong> تؤدي 3 حالات تعثر لم تُرصد و20 إنذارًا خاطئًا وفق <code>10 × FN + FP</code> إلى 50 وحدة تكلفة قرار تعليمية. لا تمثل خسارة مالية فعلية ولا خصم 50 درجة.</p>''',
        ),
    },
    "ea03b394": {
        "new_id": "readiness-compatibility",
        "pair_id": "readiness_compatibility",
        "source": paired(
            "4. Test tool compatibility",
            '''<p>The shared cell uses a small independent sample of <strong>300 synthetic rows</strong> to check Logistic Regression, XGBoost, LightGBM, SHAP, calibration and Optuna.</p>
<p>This is a software compatibility check. It does not select a project model and is not an assessed modelling result.</p>
<p><strong>Expected result:</strong> all six checks report <code>PASS</code>.</p>''',
            "4. اختبر توافق الأدوات",
            '''<p>تستخدم الخلية المشتركة عينة مستقلة صغيرة من <strong>300 سجل اصطناعي</strong> لفحص Logistic Regression وXGBoost وLightGBM وSHAP والمعايرة وOptuna.</p>
<p>هذا فحص لتوافق البرامج. لا يختار نموذج المشروع ولا يمثل نتيجة نمذجة محسوبة في التقييم.</p>
<p><strong>الناتج المتوقع:</strong> ظهور <code>PASS</code> في الفحوص الستة.</p>''',
        ),
    },
    "d1290d75": {
        "new_id": "readiness-quiz",
        "pair_id": "readiness_quiz",
        "source": paired(
            "5. Check your understanding — six ungraded questions",
            '''<p>Replace each <code>None</code> in <code>answers</code> with A, B or C. You may run the notebook first and return to the answers later. The result is not part of the course grade.</p>
<ol>
<li><code>predict_proba</code> returns 0.20. A: 20 guaranteed cases. B: an estimated 20% probability. C: a learner grade of 20.</li>
<li>Where should missing-value imputation be fitted? A: all data. B: challenge data. C: training rows inside each fold.</li>
<li>Which field suggests temporal leakage? A: collections contact after application. B: income known at application. C: requested term.</li>
<li>A customer has repeated applications. A: separate customers across validation boundaries. B: shuffle rows only. C: use customer ID as the target.</li>
<li>With 3 FN, 20 FP and weights 10 and 1, what is the simulated cost? A: 23. B: 50. C: 230.</li>
<li>Where should progress be saved before Colab closes? A: temporary session only. B: screenshot only. C: notebook and outputs in the repository or on the device.</li>
</ol>''',
            "5. اختبر فهمك — ستة أسئلة غير محسوبة",
            '''<p>استبدل كل <code>None</code> في قائمة <code>answers</code> بالحرف A أو B أو C. يمكنك تشغيل الدفتر أولًا ثم العودة للإجابات. لا تدخل النتيجة ضمن درجة الدورة.</p>
<ol>
<li>أعاد <code>predict_proba</code> القيمة 0.20. A: 20 حالة مؤكدة. B: احتمال مقدر بنسبة 20%. C: درجة المتدرب 20.</li>
<li>أين يجب تعلم تعويض القيم المفقودة؟ A: جميع البيانات. B: بيانات التحدي. C: صفوف التدريب داخل كل طية.</li>
<li>أي حقل يشير إلى تسرب زمني؟ A: اتصال التحصيل بعد الطلب. B: الدخل المعروف وقت الطلب. C: المدة المطلوبة.</li>
<li>للعميل طلبات متكررة. A: افصل العملاء بين حدود التحقق. B: اكتف بخلط الصفوف. C: استخدم معرف العميل هدفًا.</li>
<li>عند 3 FN و20 FP ووزنين 10 و1، ما تكلفة القرار التعليمية؟ A: 23. B: 50. C: 230.</li>
<li>أين تحفظ تقدمك قبل إغلاق Colab؟ A: الجلسة المؤقتة فقط. B: لقطة شاشة فقط. C: الدفتر والمخرجات في المستودع أو على الجهاز.</li>
</ol>''',
        ),
    },
    "a3ebeab8": {
        "new_id": "readiness-export",
        "pair_id": "readiness_export",
        "source": paired(
            "6. Export readiness evidence",
            '''<p>The export cell writes environment, data and compatibility summaries to <code>artifacts/</code> and creates <code>readiness_artifacts.zip</code>.</p>
<p>Download the files and the executed notebook before the runtime ends. Extract the ZIP and upload its contents to <code>artifacts/</code>; do not rely on the ZIP alone.</p>
<p>The package contains no personal data and no challenge labels.</p>''',
            "6. صدّر أدلة الاستعداد",
            '''<p>تحفظ خلية التصدير ملخصات البيئة والبيانات والتوافق داخل <code>artifacts/</code>، وتنشئ ملف <code>readiness_artifacts.zip</code>.</p>
<p>نزّل الملفات والدفتر المنفذ قبل انتهاء الجلسة. فك ZIP وارفع محتوياته إلى <code>artifacts/</code>؛ لا تعتمد على ملف ZIP وحده.</p>
<p>لا تحتوي الحزمة على بيانات شخصية أو إجابات التحدي.</p>''',
        ),
    },
    "8d0bff8e": {
        "new_id": "readiness-finish",
        "pair_id": "readiness_finish",
        "source": paired(
            "Before you close the notebook",
            '''<ul>
<li>Confirm that <code>Environment ready</code> appeared without an error.</li>
<li>Understand the difference between model features, the target and split-control identifiers.</li>
<li>Review all six questions; they are not graded.</li>
<li>Save the notebook and actual outputs outside the temporary runtime.</li>
</ul>
<p><strong>Reflection:</strong> Why is chronological order alone insufficient when the training outcome has not finished maturing?</p>
<p><strong>Troubleshooting:</strong> retry setup after a temporary download failure; restart the session after an imported-version mismatch; restore the original file after a checksum mismatch; never purchase resources to finish this lab.</p>''',
            "قبل إغلاق الدفتر",
            '''<ul>
<li>تأكد من ظهور <code>Environment ready</code> دون خطأ.</li>
<li>افهم الفرق بين خصائص النموذج والهدف ومعرّفات التحكم في التقسيم.</li>
<li>راجع الأسئلة الستة؛ فهي غير محسوبة في الدرجة.</li>
<li>احفظ الدفتر والمخرجات الفعلية خارج جلسة التشغيل المؤقتة.</li>
</ul>
<p><strong>تأمل:</strong> لماذا لا يكفي ترتيب التواريخ إذا لم يكتمل رصد نتيجة طلب التدريب؟</p>
<p><strong>حل التعثر:</strong> أعد الإعداد بعد فشل تنزيل مؤقت، وأعد تشغيل الجلسة عند اختلاف إصدار مستورد، واسترجع الملف الأصلي عند اختلاف البصمة، ولا تشتر موارد لإكمال هذا اللاب.</p>''',
        ),
    },
}


def lines(text: str) -> list[str]:
    values = text.splitlines(keepends=True)
    if values and not values[-1].endswith("\n"):
        return values
    return values


def main() -> None:
    notebook: dict[str, Any] = json.loads(NOTEBOOK.read_text(encoding="utf-8-sig"))
    original_code = {
        cell.get("id"): cell.get("source")
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    }

    replaced: set[str] = set()
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        section = SECTIONS.get(cell.get("id"))
        if not section:
            continue
        original_id = cell["id"]
        cell["id"] = section["new_id"]
        cell["metadata"] = {
            "bilingual_pair_id": section["pair_id"],
            "bilingual_order": ORDER,
            "learner_facing": True,
            "content_version": CONTENT_VERSION,
        }
        cell["source"] = lines(section["source"])
        replaced.add(original_id)

    missing = sorted(set(SECTIONS) - replaced)
    if missing:
        raise ValueError(f"Expected markdown cells were not found: {missing}")

    current_code = {
        cell.get("id"): cell.get("source")
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    }
    if original_code != current_code:
        raise ValueError("Executable cells changed during bilingual conversion.")

    notebook.setdefault("metadata", {}).setdefault("colab", {})["name"] = NOTEBOOK.name
    NOTEBOOK.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {NOTEBOOK} with {len(replaced)} bilingual sections.")


if __name__ == "__main__":
    main()
