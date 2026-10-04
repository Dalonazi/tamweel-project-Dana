# Phase 7 — Day 5 Bilingual Implementation Report

## Status

**COMPLETE — controlled candidate on `develop/bilingual-v1.1.0`; not merged to `main`.**

Day 5 is now bilingual, deterministic and protected by released-code parity. The published `v1.0.0` notebook and `main` branch remain unchanged.

## Scope completed

- `notebooks/05_final_model.ipynb`
- `DAY5_GUIDE.md`
- `content/day5_notebook_code_contract.json`
- `scripts/build_bilingual_day5.py`
- `scripts/build_day5_guide.py`
- `scripts/check_day5_reference_parity.py`
- `.github/workflows/build_bilingual_day5.yml`
- `.github/workflows/day5_reference_parity.yml`
- Day 5 extensions to the bilingual manifest, bilingual content gate and notebook smoke gate

## Learner-facing design

The production notebook now contains 12 paired learner sections:

1. final-lab purpose, deliverables and boundaries;
2. controlled free-CPU setup;
3. fit/selection and calibration role separation;
4. nested forward OOF stacking without leakage;
5. prediction and residual diversity;
6. the fixed worth-it gate for ensemble complexity;
7. OOF decision policy and 12% capacity;
8. final fitting, frozen sigmoid calibration and explanation scope;
9. full-batch challenge scoring and tie-safe capacity;
10. learner reasoning and prior-evidence assembly;
11. bundle export and reproducibility;
12. final checkpoint before Notebook 99.

Every learner section uses English LTR on the left and Arabic RTL on the right. Code is shared once and is not duplicated by language. The notebook records `bilingual_pair_id`, `bilingual_order: en-left-ar-right`, `learner_facing: true` and `content_version: 1.1.0`.

The content states explicitly that:

- `KEEP SINGLE` is a valid outcome when the ensemble does not earn its complexity;
- ensemble weights and the meta-model must learn from inner OOF only;
- calibration-fit diagnostics are not independent challenge performance;
- the OOF loss is `10 × FN + FP` in fictional educational units;
- the 12% policy is applied once to the complete 2,500-request challenge batch;
- equal-score boundary blocks are not split by identifier;
- challenge AP, loss and FPR cannot be claimed without labels;
- Day 4 explanations cannot automatically be attributed to a different final model;
- technical completion, hashes and file presence are not a grade or submission receipt.

## Executable-cell preservation

The released `v1.0.0` notebook contains 10 executable cells. The controlled code contract protects every cell by stable ID and SHA-256.

| Contract check | Result |
|---|---:|
| Expected executable cells | 10 |
| Candidate executable cells | 10 |
| Missing cells | 0 |
| Unexpected cells | 0 |
| Changed cells | 0 |
| Final status | PASS |

## Deterministic generation

The Day 5 build workflow:

1. captures the released executable-cell contract;
2. verifies code before conversion;
3. replaces only the 12 learner markdown cells;
4. rejects missing, duplicate or unexpected sections;
5. verifies code after conversion;
6. generates the notebook and complete bilingual guide;
7. records build evidence;
8. commits generated files only when content changes.

Generated-material commit:

`74ce68fe427f6876c3fa08f69f77bcf693be289a` — `Generate bilingual Day 5 materials`

## Released-reference parity

The candidate and released `main` notebook were executed in separate clean workspaces with the pinned CPU environment and assessment mode. Stable scientific and delivery outputs matched.

### Tabular outputs

| Output | Reference rows | Candidate rows | Result |
|---|---:|---:|---|
| `day5_roles.csv` | 10,000 | 10,000 | MATCH |
| `day5_oof_predictions.csv` | 2,155 | 2,155 | MATCH |
| `day5_fold_scores.csv` | 18 | 18 | MATCH |
| `ensemble_comparison.csv` | 6 | 6 | MATCH |
| `day5_threshold_sweep.csv` | 2,158 | 2,158 | MATCH |
| `day5_region_audit.csv` | 4 | 4 | MATCH |
| `day5_period_capacity.csv` | 3 | 3 | MATCH |
| `day5_cost_sensitivity.csv` | 3 | 3 | MATCH |
| `day5_probability_correlation.csv` | 3 | 3 | MATCH |
| `day5_residual_correlation.csv` | 3 | 3 | MATCH |
| `day5_calibration_predictions.csv` | 836 | 836 | MATCH |
| `day5_calibration_fit_bins.csv` | 20 | 20 | MATCH |
| `submission/submission.csv` | 2,500 | 2,500 | MATCH |

### Stable structured evidence

The following matched after excluding runtime-only timing keys:

- `day5_run.json`
- `day5_reflection.json`
- `day5_oof_provenance.json`
- `day5_ensemble_gate.json`
- `final_policy.json`
- `final_metrics.json`
- `day5_final_provenance.json`
- `day5_project_check.json`

The following text/model outputs also matched:

| Output | Stable evidence |
|---|---|
| `PROJECT_README.md` | 369 normalized characters in both runs |
| `reports/MODEL_CARD.md` | 2,446 normalized characters in both runs |
| `reports/ENSEMBLE_DECISION.md` | 193 normalized characters in both runs |
| `artifacts/final_model/model.json` | stable JSON match |
| `artifacts/final_model/model_manifest.json` | stable JSON match |

### Final decision parity

| Field | Released reference | Bilingual candidate |
|---|---|---|
| Technical status | `TECHNICAL_READY` | `TECHNICAL_READY` |
| Source | `LIVE` | `LIVE` |
| Chosen candidate | `Logistic` | `Logistic` |
| Complexity decision | `KEEP SINGLE` | `KEEP SINGLE` |

The parity gate requires the five PNG figures, environment record, submission manifest and project bundle to exist, but deliberately excludes their bytes or volatile hashes from equality claims. Stable predictions, policies, model metadata, reports and submission rows are compared.

## Quality gates

Validated candidate head:

`c21d0f1eb96c15fa4ab7638cfb288b2097df6149`

| Quality gate | Run ID | Result |
|---|---:|---|
| Bilingual Content Check | `37103761594` | PASS |
| Environment Check | `37103761610` | PASS |
| Day 1 Reference Parity regression guard | `37103761575` | PASS |
| Day 2 Reference Parity regression guard | `37103761645` | PASS |
| Day 3 Reference Parity regression guard | `37103761641` | PASS |
| Day 4 Reference Parity regression guard | `37103761615` | PASS |
| Day 5 Reference Parity | `37103761593` | PASS |
| Notebook Smoke Test | `37103761620` | PASS |

Notebook Smoke Test verified executable-cell contracts through Day 5 and executed Notebooks 00–05 in fresh kernels and isolated workspaces.

## Manifest state after Phase 7

Complete:

- bilingual README and glossary;
- Notebook 00 readiness materials;
- Days 1–5 production notebooks;
- Days 1–5 bilingual learner guides;
- executable-cell contracts for Notebook 00 and Days 1–5;
- released-reference parity gates for Days 1–5.

Still planned:

- bilingual conversion and controlled structural validation of Notebook 99;
- final-check guide bilingual conversion;
- final release-hash rebuild after all learner-facing files are frozen;
- fresh hosted-Colab acceptance from a clean Google account;
- visual and responsive review in the actual Colab interface;
- private evaluator and private submission registry;
- merge to `main` and publication of `v1.1.0`.

## Release decision

**Do not merge yet.** Day 5 is technically complete. Notebook 99, final release hashes and hosted-Colab acceptance remain release-blocking gates.
