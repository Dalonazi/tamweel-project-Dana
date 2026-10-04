"""Validate the bilingual learner repository as a release candidate.

This check is intentionally conservative. It verifies documentation consistency,
forbidden wording, obvious secret patterns, required release files and the absence
of unfinished placeholders. It does not replace hosted-Colab acceptance, the
private evaluator or instructor review.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

REQUIRED_FILES = [
    "README.md",
    "START_HERE.md",
    "READINESS_GUIDE.md",
    "COLAB_GUIDE.md",
    "GITHUB_GUIDE.md",
    "FAQ.md",
    "TROUBLESHOOTING.md",
    "LEARNING_RESOURCES.md",
    "GLOSSARY.md",
    "DAY1_GUIDE.md",
    "DAY2_GUIDE.md",
    "DAY3_GUIDE.md",
    "DAY4_GUIDE.md",
    "DAY5_GUIDE.md",
    "FINAL_CHECK_GUIDE.md",
    "TECHNICAL_REQUIREMENTS.md",
    "ADMINISTRATIVE_REQUIREMENTS.md",
    "RUBRIC.md",
    "SUBMISSION_GUIDE.md",
    "COURSE_ALIGNMENT.md",
    "RELEASE_NOTES.md",
    "content/bilingual_manifest.yml",
    "release/release_scope.json",
]

LEARNER_TEXT_FILES = [
    path
    for path in REQUIRED_FILES
    if path.endswith(".md") and not path.startswith("docs/")
]

FORBIDDEN_PHRASES = {
    "verbally announced": "submission schedule must be issued in writing",
    "تحددها المدربة شفهيًا": "يجب توثيق موعد وقناة التسليم كتابيًا",
    "الخسارة الافتراضية": "use تكلفة القرار التعليمية",
    "guaranteed error-free": "do not promise zero execution errors",
    "مضمون بلا أخطاء": "لا تعد بضمان مطلق لعدم وجود أخطاء",
}

PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bFIXME\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"<INSERT[^>]*>", re.IGNORECASE),
]

SECRET_PATTERNS = {
    "GitHub classic token": re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    "GitHub fine-grained token": re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
    "OpenAI-style key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "Google API key": re.compile(r"AIza[0-9A-Za-z_-]{25,}"),
    "Private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("check-output/release-candidate.json"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    issues: list[dict[str, str]] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            issues.append({"file": relative, "issue": "required file is missing"})

    for relative in LEARNER_TEXT_FILES:
        path = root / relative
        if not path.is_file():
            continue
        text = read_text(path)
        if "<!-- BILINGUAL:EN -->" not in text or "<!-- BILINGUAL:AR -->" not in text:
            issues.append({"file": relative, "issue": "bilingual markers are missing"})
        for phrase, reason in FORBIDDEN_PHRASES.items():
            if phrase.casefold() in text.casefold():
                issues.append({"file": relative, "issue": f"forbidden phrase: {phrase} ({reason})"})
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(text):
                issues.append({"file": relative, "issue": f"unfinished placeholder: {pattern.pattern}"})
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                issues.append({"file": relative, "issue": f"possible secret detected: {label}"})

    release_notes = root / "RELEASE_NOTES.md"
    if release_notes.is_file():
        notes = read_text(release_notes)
        for signal in ("v1.1.0", "90", "10", "Notebook 99", "دفتر 99"):
            if signal not in notes:
                issues.append({"file": "RELEASE_NOTES.md", "issue": f"missing release signal: {signal}"})

    readme = root / "README.md"
    if readme.is_file():
        text = read_text(readme)
        required_links = [
            "notebooks/00_readiness_check.ipynb",
            "notebooks/01_baseline_boosting.ipynb",
            "notebooks/02_validation_tuning.ipynb",
            "notebooks/03_cost_sensitive_decision.ipynb",
            "notebooks/04_explain_calibrate.ipynb",
            "notebooks/05_final_model.ipynb",
            "notebooks/99_final_submission_check.ipynb",
        ]
        for link in required_links:
            if link not in text:
                issues.append({"file": "README.md", "issue": f"missing canonical notebook link: {link}"})

    status = "PASS" if not issues else "FAIL"
    report: dict[str, Any] = {
        "status": status,
        "issues": issues,
        "required_file_count": len(REQUIRED_FILES),
        "learner_text_file_count": len(LEARNER_TEXT_FILES),
        "scope": (
            "Static pre-release documentation, privacy and consistency check. "
            "Hosted Colab, visual QA, private evaluation and submission receipt controls remain separate."
        ),
    }
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
