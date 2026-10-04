# Phase 6 — Day 4 Bilingual Implementation Report

## Status

**COMPLETE — controlled candidate on `develop/bilingual-v1.1.0`; not merged to `main`.**

This phase converted Day 4 into a paired bilingual learner experience while preserving the released `v1.0.0` executable logic and scientific outputs.

## Scope

Production materials completed in this phase:

- `notebooks/04_explain_calibrate.ipynb`
- `DAY4_GUIDE.md`
- `content/day4_notebook_code_contract.json`
- `scripts/build_bilingual_day4.py`
- `scripts/build_day4_guide.py`
- `scripts/check_day4_reference_parity.py`
- `.github/workflows/build_bilingual_day4.yml`
- `.github/workflows/day4_reference_parity.yml`
- Day 4 extensions to the bilingual manifest, bilingual content check and notebook smoke test

## Learner-facing design

The production notebook contains 12 paired learner sections. Every learner section uses:

- English LTR on the left
- Arabic RTL on the right
- one shared executable path
- `bilingual_pair_id`
- `bilingual_order: en-left-ar-right`
- `content_version: 1.1.0`

The converted content covers:

1. controlled free-CPU setup;
2. fit, calibration, policy and evaluation role separation;
3. held-out permutation importance;
4. global SHAP interpretation and log-odds units;
5. local waterfall explanation and narrow perturbation stability;
6. sigmoid calibration, Brier score, log-loss and ECE;
7. customer-cluster bootstrap scope and limitations;
8. transported policy threshold and diagnostic review-zone capacity;
9. six evidence-based learner responses;
10. report and artifact export;
11. limitations, governance boundaries and non-causal interpretation;
12. readiness checkpoint before Day 5.

The guide and notebook state that the data are fictional, model explanations do not establish causes, calibration improvement must be measured rather than assumed, the ±0.02 review zone is operational rather than an individual confidence interval, and `CAPACITY_REVIEW_REQUIRED` is a valid finding.

## Executable-cell preservation

The Day 4 code contract was captured from the released `v1.0.0` notebook and protects all 10 executable cells by stable cell ID and SHA-256 hash.

Validation result:

| Contract check | Result |
|---|---:|
| Expected executable cells | 10 |
| Candidate executable cells | 10 |
| Missing cells | 0 |
| Unexpected cells | 0 |
| Changed cells | 0 |
| Final status | PASS |

## Deterministic generation

The controlled Day 4 build workflow:

1. captures the released executable-cell contract;
2. verifies code before conversion;
3. replaces only the 12 learner markdown sections;
4. rejects missing, duplicate or unexpected sections;
5. verifies code after conversion;
6. generates the bilingual notebook and guide;
7. records build evidence;
8. commits generated materials only when content changes.

Generated-material commit:

`7f68b8e11068ca4b72dee3648326ac1b918549a7` — `Generate bilingual Day 4 materials`

## Released-reference parity

The candidate and released `main` notebook were executed in separate clean workspaces using the pinned CPU environment and assessment mode. The comparison passed with no scientific-output differences.

### Stable tabular outputs

| Output | Reference rows | Candidate rows | Result |
|---|---:|---:|---|
| `day4_roles.csv` | 10,000 | 10,000 | MATCH |
| `day4_predictions.csv` | 2,906 | 2,906 | MATCH |
| `permutation_importance.csv` | 20 | 20 | MATCH |
| `day4_shap_global.csv` | 22 | 22 | MATCH |
| `day4_reason_codes.csv` | 3 | 3 | MATCH |
| `day4_local_stability.csv` | 3 | 3 | MATCH |
| `day4_reliability_bins.csv` | 20 | 20 | MATCH |
| `day4_period_metrics.csv` | 4 | 4 | MATCH |
| `day4_bootstrap.csv` | 200 | 200 | MATCH |
| `day4_policy_sweep.csv` | 592 | 592 | MATCH |
| `day4_review_flags.csv` | 1,733 | 1,733 | MATCH |
| `day4_capacity.csv` | 2 | 2 | MATCH |

### Additional stable evidence

The following also match:

- `calibration_metrics.json`
- `day4_shap_metadata.json`
- `day4_stability_summary.json`
- `day4_provenance.json`
- `day4_reflection.json`
- `day4_run.json`
- complete arrays in `shap_values_sample.npz`
- exact `day4_model.txt`
- normalized `reports/INTERPRETABILITY_REPORT.md`

The SHAP evidence contains 300 explained rows across 22 features. The saved model text contains 140,874 characters in both runs, and the normalized interpretability report contains 2,602 characters in both runs.

### Run status parity

| Field | Released reference | Bilingual candidate |
|---|---|---|
| Technical status | `TECHNICAL_READY` | `TECHNICAL_READY` |
| Explanation source | `LIVE` | `LIVE` |
| Capacity status | `CAPACITY_REVIEW_REQUIRED` | `CAPACITY_REVIEW_REQUIRED` |

Runtime timing keys and PNG byte equality are intentionally excluded. Numerical tables, probabilities, SHAP arrays, model text, policy outputs, capacity outputs, provenance, reflection and report text are included.

## Quality gates

Validated candidate head:

`2b6899466f6d41319a9289e7039f844e861dbd00`

| Quality gate | Run ID | Result |
|---|---:|---|
| Bilingual Content Check | `37103282372` | PASS |
| Environment Check | `37103282388` | PASS |
| Day 1 Reference Parity regression guard | `37103282368` | PASS |
| Day 2 Reference Parity regression guard | `37103282383` | PASS |
| Day 3 Reference Parity regression guard | `37103282376` | PASS |
| Day 4 Reference Parity | `37103282377` | PASS |
| Notebook Smoke Test | `37103282397` | PASS |

The notebook smoke test verifies executable contracts through Day 4 and executes the notebook suite in fresh kernels.

## Manifest state after Phase 6

Completed:

- README and glossary
- Day 1 guide and Notebook 01
- Day 2 guide and Notebook 02
- Day 3 guide and Notebook 03
- Day 4 guide and Notebook 04
- Notebook 00 readiness materials

Still planned:

- `notebooks/05_final_model.ipynb`
- `notebooks/99_final_submission_check.ipynb`
- Day 5 guide and remaining learner-facing submission documents
- final release-hash rebuild
- hosted-Colab visual and responsive acceptance from a clean Google account
- private evaluator and private submission registry
- merge to `main`
- publication of `v1.1.0`

## Release decision

**Do not merge yet.** Phase 6 is technically complete, but the controlled release remains open until Day 5, Notebook 99, final release hashes and hosted-Colab acceptance are complete.
