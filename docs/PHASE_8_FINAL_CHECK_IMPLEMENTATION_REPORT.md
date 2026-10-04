# Phase 8 — Notebook 99 and Final-Check Bilingual Implementation Report

## Status

**COMPLETE — controlled candidate on `develop/bilingual-v1.1.0`; not merged to `main`.**

Notebook 99 and the final-check guide are now bilingual and protected by the released executable-cell contract. The published `v1.0.0` release and the `main` branch remain unchanged.

## Scope completed

- `notebooks/99_final_submission_check.ipynb`
- `FINAL_CHECK_GUIDE.md`
- `content/notebook99_code_contract.json`
- `scripts/build_bilingual_final_check.py`
- `scripts/build_final_check_guide.py`
- `scripts/check_final_check_notebook.py`
- `.github/workflows/build_bilingual_final_check.yml`
- `.github/workflows/final_check_notebook.yml`
- Notebook 99 extensions to the bilingual manifest, bilingual content gate and notebook smoke gate

## Learner-facing design

Notebook 99 now contains six paired learner sections:

1. final-project self-check purpose, assessment boundary and security notice;
2. exact project snapshot using a full commit SHA or one complete project ZIP;
3. pinned, hash-verified checking tools and assessment mode;
4. safe project snapshot reading and 100 MiB archive limit;
5. technical check execution, findings and correction path;
6. report, final-bundle download and repository submission sequence.

Every learner section uses:

- English LTR on the left;
- Arabic RTL on the right;
- one shared executable path;
- `bilingual_pair_id`;
- `bilingual_order: en-left-ar-right`;
- `learner_facing: true`;
- `content_version: 1.1.0`.

The final-check materials state explicitly that:

- the notebook inspects the learner's own fixed project snapshot;
- a full 40-character commit SHA is required for a public repository;
- a moving branch name such as `main` is not accepted as a reproducible snapshot;
- no password, token, Drive connection, account connection or private data is required;
- uploaded archives are size-limited and extracted with safe-path validation;
- source files are downloaded from a pinned revision and verified by SHA-256;
- readiness, Days 1–5 and the final contract are checked in isolated workspaces;
- `READY FOR FINAL SUBMISSION` means the declared technical gates passed only;
- technical readiness is not a grade, authenticity determination or submission receipt;
- the instructor remains responsible for interpretation, authenticity, presentation and score;
- the learner must rerun the check after any project change because the manifest and hashes are snapshot-specific.

## Executable-cell preservation

The released `v1.0.0` Notebook 99 contains five executable cells. The controlled contract protects all five by stable cell ID and SHA-256.

| Contract check | Result |
|---|---:|
| Expected executable cells | 5 |
| Candidate executable cells | 5 |
| Missing cells | 0 |
| Unexpected cells | 0 |
| Changed cells | 0 |
| Final status | PASS |

Protected cell IDs:

- `ea0d9afa`
- `24d8a679`
- `0c05021e`
- `a9a8bf0d`
- `2a1a4a61`

## Deterministic generation

The controlled build workflow:

1. captures the released Notebook 99 executable-cell contract;
2. verifies code before conversion;
3. replaces only the six learner markdown cells;
4. rejects missing, duplicate or unexpected sections;
5. verifies executable bytes after conversion;
6. generates the bilingual notebook and final-check guide;
7. validates static structure and required safety signals;
8. commits generated files only when content changes;
9. uploads contract and structural evidence.

Generated-material commit:

`c6100e86372861dca892a50316be3ff29211e6a2` — `Generate bilingual final-check materials`

## Controlled structural validation

Notebook 99 cannot be given a meaningful released-reference output-parity claim without an actual learner project snapshot, network access and the interactive Colab upload/download flow. The correct gate for this phase is therefore exact executable-cell preservation plus static structural and security validation.

The structural checker passed with:

| Check | Result |
|---|---:|
| Executable cells | 5 |
| Contract cells | 5 |
| Bilingual sections | 6 |
| Missing cells | 0 |
| Unexpected cells | 0 |
| Changed cells | 0 |
| Syntax failures | 0 |
| Forbidden account/secret signals | 0 |
| Final status | PASS |

Required behavior and safety signals verified in the unchanged executable code:

- `PROJECT_REPOSITORY`
- `PROJECT_SHA`
- `PROJECT_ZIP`
- `CHECK_REVISION`
- `CHECK_HASHES`
- `ASSESSMENT_MODE`
- `extract_project`
- `100*1024*1024`
- `scripts/final_check.py`
- `self_check_report.json`
- `final_project_bundle.zip`
- `files.download`

The static checker also rejects account/secret integration signals such as `drive.mount`, `getpass.getpass` and `GITHUB_TOKEN`.

## Quality gates

Validated candidate head:

`92297c2262804289fc5a9c43c298e06f9a897eea`

| Quality gate | Run ID | Result |
|---|---:|---|
| Bilingual Content Check | `37104277830` | PASS |
| Environment Check | `37104277834` | PASS |
| Day 1 Reference Parity regression guard | `37104277858` | PASS |
| Day 2 Reference Parity regression guard | `37104277865` | PASS |
| Day 3 Reference Parity regression guard | `37104277859` | PASS |
| Day 4 Reference Parity regression guard | `37104277838` | PASS |
| Day 5 Reference Parity regression guard | `37104277817` | PASS |
| Notebook Smoke Test | `37104277819` | PASS |
| Notebook 99 Contract and Structure | `37104277852` | PASS |

The notebook smoke gate now verifies executable-cell contracts for Notebook 00, Days 1–5 and Notebook 99, validates Notebook 99's bilingual structure, and executes Notebooks 00–05 in fresh kernels. Notebook 99 itself is deliberately not executed by the generic smoke runner because its live behavior requires a supplied project snapshot and interactive Colab file operations.

## Manifest state after Phase 8

Complete:

- bilingual `README.md` and `GLOSSARY.md`;
- Notebook 00 readiness materials;
- production Notebooks 01–05;
- production Notebook 99;
- Days 1–5 bilingual learner guides;
- bilingual final-check guide;
- executable-cell contracts for Notebook 00, Days 1–5 and Notebook 99;
- released-reference parity gates for Days 1–5;
- controlled structural and safety gate for Notebook 99.

All currently declared learner-facing notebooks and guides in the bilingual manifest are marked complete.

## Remaining release blockers

- rebuild the final release hashes after every learner-facing file is frozen;
- run Notebook 99 with a real complete learner project snapshot in a fresh hosted Colab session;
- complete visual and responsive acceptance in the actual Colab interface;
- verify English-left and Arabic-right rendering on practical screen widths;
- complete the private evaluator and private submission registry;
- review the final release manifest and release notes;
- merge to `main` only after the release gates pass;
- publish `v1.1.0` only after the controlled merge.

## Release decision

**Do not merge yet.** The bilingual conversion and automated repository gates are complete. Final release hashes, hosted-Colab acceptance and the private evaluation/submission controls remain release-blocking requirements.
