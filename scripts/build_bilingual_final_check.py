"""Convert Notebook 99 learner markdown to paired bilingual cells without changing code."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CONTENT_VERSION = "1.1.0"
REQUIRED_ORDER = "en-left-ar-right"
DEFAULT_NOTEBOOK = Path("notebooks/99_final_submission_check.ipynb")
DEFAULT_CONTRACT = Path("content/notebook99_code_contract.json")


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
    "ac2e555b": {
        "pair_id": "final_check_header",
        "en_title": "Notebook 99 · Final project self-check",
        "ar_title": "دفتر 99 · الفحص الذاتي النهائي للمشروع",
        "en_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · Prepared and delivered by Meaad Al-Marri | ميعاد المري</strong></p>
<p>Use a fresh free-CPU session to inspect <strong>your own project snapshot</strong>. Run the cells in order. The checker reports the status of each required file and executes the applications in isolated workspaces; it does not award an automatic grade.</p>
<p>The assessment framework is 90 technical/administrative points plus 10 presentation points. Passing starts at 70 and distinction at 95 before rounding, but the instructor reviews interpretation, authenticity and presentation.</p>
<p><strong>Security boundary:</strong> upload only files you know. Do not connect Drive, accounts, secrets or private data. The notebook executes project code. A successful technical check is not a submission receipt.</p>
<p><a href="https://github.com/almiyead-rgb/sda-dsc-211-student-template/blob/main/FINAL_CHECK_GUIDE.md">Final-check guide</a></p>
""",
        "ar_body": """
<p><strong>SDA-DSC-211 · Tamweel Lite · إعداد وتقديم ميعاد المري | Meaad Al-Marri</strong></p>
<p>استخدم جلسة CPU مجانية جديدة لفحص <strong>لقطة مشروعك أنت</strong>. شغّل الخلايا بالترتيب. يعرض الفاحص حالة كل ملف مطلوب ويشغّل التطبيقات في مساحات عمل معزولة، لكنه لا يمنح درجة تلقائية.</p>
<p>إطار التقييم 90 نقطة تقنية وإدارية و10 نقاط للعرض. يبدأ النجاح من 70 والتميز من 95 قبل التقريب، بينما تراجع المدربة التفسير وأصالة العمل والعرض.</p>
<p><strong>حد الأمان:</strong> ارفع الملفات التي تعرفها فقط. لا تربط Drive أو الحسابات أو الأسرار أو البيانات الخاصة. يشغّل الدفتر شيفرة المشروع. نجاح الفحص التقني ليس إيصال تسليم.</p>
<p><a href="https://github.com/almiyead-rgb/sda-dsc-211-student-template/blob/main/FINAL_CHECK_GUIDE.md">دليل الفحص النهائي</a></p>
""",
    },
    "044737da": {
        "pair_id": "final_check_source",
        "en_title": "1. Identify the exact project snapshot",
        "ar_title": "1. حدّد لقطة المشروع بدقة",
        "en_body": """
<p>For a public repository, enter <code>owner/repository</code> and the full 40-character commit SHA. Never use a moving branch name such as <code>main</code>. For a local project, leave both fields blank and provide one complete project ZIP in the upload step.</p>
<p>Do not upload the Day 5 ZIP by itself. The snapshot must also contain executed notebooks, imported evidence from Days 1–4, the presentation and the template files required by the submission contract.</p>
<p>The checker works on a fixed snapshot and builds a manifest in a temporary copy; it does not change GitHub. After a successful check, upload the extracted final files to your repository, rerun Final Project Check, and record the final SHA and tag through the private submission channel. Any schedule is the one announced by the instructor for your cohort.</p>
""",
        "ar_body": """
<p>للمستودع العام اكتب <code>owner/repository</code> وSHA كاملًا من 40 خانة. لا تستخدم اسم فرع متحرك مثل <code>main</code>. للمشروع المحلي اترك الحقلين فارغين وقدّم ZIP كاملًا واحدًا في خطوة الرفع.</p>
<p>لا ترفع ZIP اليوم الخامس وحده. يجب أن تضم اللقطة أيضًا الدفاتر المنفذة، والأدلة المستوردة من الأيام 1–4، والعرض، وملفات القالب المطلوبة في عقد التسليم.</p>
<p>يعمل الفاحص على لقطة ثابتة ويبني manifest في نسخة مؤقتة؛ ولا يغير GitHub. بعد نجاح الفحص ارفع الملفات النهائية المستخرجة إلى مستودعك، ثم أعد Final Project Check وسجّل SHA وtag النهائيين عبر قناة التسليم الخاصة. يعتمد الموعد على ما تعلنه المدربة لدفعتك.</p>
""",
    },
    "79717564": {
        "pair_id": "final_check_tools",
        "en_title": "2. Prepare verified checking tools",
        "ar_title": "2. جهّز أدوات فحص موثقة",
        "en_body": """
<p>The setup cell downloads the course checking tools from one pinned revision, verifies the SHA-256 of every source, installs the free pinned environment and enables assessment mode with two CPU threads.</p>
<p>Wait until <code>CHECK_TOOLS_READY</code> appears. Never bypass a source checksum mismatch. Each application is later executed in a separate process and workspace; the checker redirects only the documented project directory and does not rewrite learner answers or training logic.</p>
""",
        "ar_body": """
<p>تنزّل خلية الإعداد أدوات فحص الدورة من مراجعة مثبتة واحدة، وتتحقق من SHA-256 لكل مصدر، وتثبت البيئة المجانية المقيدة، وتفعل وضع التقييم بخيطي CPU.</p>
<p>انتظر ظهور <code>CHECK_TOOLS_READY</code>. لا تتجاوز عدم تطابق بصمة المصدر. يُشغّل كل تطبيق لاحقًا في عملية ومجلد مستقلين؛ ويعيد الفاحص توجيه مجلد المشروع الموثق فقط دون إعادة كتابة إجابات المتدرب أو منطق التدريب.</p>
""",
    },
    "08b7386b": {
        "pair_id": "final_check_snapshot",
        "en_title": "3. Read the project snapshot safely",
        "ar_title": "3. اقرأ لقطة المشروع بأمان",
        "en_body": """
<p>If repository fields are blank, choose exactly one project ZIP. Do not enter a password or token. For a public repository, the notebook downloads the archive for the exact SHA.</p>
<p>The reader limits the archive to 100 MiB, validates path names and safe extraction rules, and prints the archive SHA-256. Confirm that the displayed project root is your intended snapshot before continuing.</p>
""",
        "ar_body": """
<p>إذا كانت حقول المستودع فارغة فاختر ZIP مشروع واحدًا فقط. لا تدخل كلمة مرور أو token. للمستودع العام ينزّل الدفتر الأرشيف الخاص بالـSHA المحدد.</p>
<p>يحد القارئ حجم الأرشيف بـ100 MiB، ويتحقق من أسماء المسارات وقواعد الفك الآمن، ثم يعرض SHA-256 للأرشيف. تأكد أن جذر المشروع المعروض هو اللقطة المقصودة قبل المتابعة.</p>
""",
    },
    "012bbcfa": {
        "pair_id": "final_check_run",
        "en_title": "4. Run the check and read every finding",
        "ar_title": "4. شغّل الفحص واقرأ كل ملاحظة",
        "en_body": """
<p>The final checker validates required files, hashes, prediction structure, the 12% batch policy and the final manifest. It then executes readiness and Days 1–5 in clean processes and workspaces.</p>
<p>Read the <strong>File / How to fix</strong> table. File presence does not prove that an interpretation is correct; the instructor reviews meaning and authenticity. Empty responses, recovery examples and labelled educational examples do not satisfy final readiness.</p>
<p><code>READY FOR FINAL SUBMISSION | جاهز للتسليم النهائي</code> means only that the declared technical checks passed. <code>NEEDS_WORK</code> is actionable: correct the original project files and rerun the complete check.</p>
""",
        "ar_body": """
<p>يتحقق الفاحص النهائي من الملفات المطلوبة والبصمات وبنية التنبؤات وسياسة الدفعة 12% والـmanifest النهائي. ثم يشغّل الاستعداد والأيام 1–5 في عمليات ومساحات عمل نظيفة.</p>
<p>اقرأ جدول <strong>File / How to fix</strong>. وجود الملف لا يثبت صحة التفسير؛ تراجع المدربة المعنى وأصالة العمل. لا تحقق الإجابات الفارغة أو مخرجات التعافي أو الأمثلة التعليمية الموسومة الجاهزية النهائية.</p>
<p>تعني <code>READY FOR FINAL SUBMISSION | جاهز للتسليم النهائي</code> نجاح الفحوص التقنية المعلنة فقط. أما <code>NEEDS_WORK</code> فهي نتيجة قابلة للتنفيذ: صحح ملفات المشروع الأصلية ثم أعد الفحص الكامل.</p>
""",
    },
    "88fd658c": {
        "pair_id": "final_check_save",
        "en_title": "5. Save the report and final bundle",
        "ar_title": "5. احفظ التقرير والحزمة النهائية",
        "en_body": """
<p>The report is always copied to <code>Files → final_check_downloads/self_check_report.json</code>. The final project bundle is copied and downloaded only when the checker reports readiness.</p>
<p>If the browser download does not start, refresh the Files pane and download one file at a time. Confirm that the files exist on your device before closing the session. After any project change, rerun the check because the manifest and file hashes are snapshot-specific.</p>
<p>The course-tool revision is not your submission SHA. Extract the final bundle, upload the actual files to your repository, run the repository Final Project Check, create <code>final-submission</code> on the same commit, and record the SHA/tag privately. Do not publish personal data or submission details in public Issues.</p>
""",
        "ar_body": """
<p>يُنسخ التقرير دائمًا إلى <code>Files → final_check_downloads/self_check_report.json</code>. ولا تُنسخ الحزمة النهائية وتُنزّل إلا عندما يعلن الفاحص الجاهزية.</p>
<p>إذا لم يبدأ تنزيل المتصفح فحدّث لوحة Files ونزّل ملفًا واحدًا في كل مرة. تأكد من وجود الملفات على جهازك قبل إغلاق الجلسة. بعد أي تعديل في المشروع أعد الفحص لأن manifest وبصمات الملفات تخص لقطة محددة.</p>
<p>مراجعة أدوات الدورة ليست SHA تسليمك. فك الحزمة النهائية وارفع الملفات الفعلية إلى مستودعك، وشغّل Final Project Check، وأنشئ <code>final-submission</code> على commit نفسه، ثم سجّل SHA/tag بصورة خاصة. لا تنشر البيانات الشخصية أو تفاصيل التسليم في Issues عامة.</p>
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
            raise RuntimeError(f"Unexpected Notebook 99 markdown cell: id={cell_id!r}, pair={pair_id!r}")
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
            f"Notebook 99 markdown coverage mismatch: "
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
        default=Path("check-output/notebook99-bilingual-build.json"),
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
        "execution_scope": "Structural conversion only; live final check requires a learner project snapshot and Colab download/upload interactions.",
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
