# Phase 10 — Bilingual Onboarding and Learner Support

## Scope

Phase 10 converts the remaining learner onboarding and support documents to the same controlled bilingual standard used by the production notebooks and daily guides.

English appears on the left with explicit LTR direction. Arabic appears on the right with explicit RTL direction. Long operational sections remain readable on GitHub and practical screen widths. No executable notebook cell, model logic, data contract or scientific output is changed in this phase.

## Files rebuilt

- `START_HERE.md`
- `READINESS_GUIDE.md`
- `COLAB_GUIDE.md`
- `GITHUB_GUIDE.md`
- `FAQ.md`
- `TROUBLESHOOTING.md`
- `LEARNING_RESOURCES.md`
- `content/bilingual_manifest.yml`

## Design decisions

### Beginner-first navigation

The onboarding path now follows one explicit sequence:

1. Create a repository from the template.
2. Complete Notebook 00 readiness.
3. Use free Colab CPU.
4. Save the executed notebook and evidence.
5. Build one connected project over five days.
6. Run Notebook 99 and the final GitHub Action.
7. Record the exact tag and commit SHA.
8. Submit through the private cohort channel.

### One shared technical path

The documents do not create separate Arabic and English technical procedures. Both language columns point to the same notebook, files, workflows, policies and submission contract.

### Free and low-friction operation

The support material states consistently that the learner path requires:

- free Colab CPU;
- a free GitHub account;
- no GPU or TPU;
- no API key;
- no paid subscription;
- no local Python installation;
- no Drive mount;
- no terminal for the standard learner workflow.

### Error prevention

The Colab and troubleshooting guides now explicitly cover:

- clean `Run all` execution;
- restart requirements after package conflicts;
- checksum failures;
- temporary runtime loss;
- missing variables caused by out-of-order cells;
- incorrect repository destinations;
- file-download verification;
- GitHub Actions states;
- hard-coded or recovery-output rejection;
- manifest, tag and SHA mismatches;
- private support-request evidence.

### Academic integrity and privacy

All onboarding documents reinforce that learners must not publish:

- passwords or access tokens;
- national IDs, private email addresses or phone numbers;
- private grades or submission receipts;
- hidden labels or evaluator files;
- confidential employer or third-party data;
- fabricated or hard-coded outputs.

Notebook 99 technical readiness remains separate from grade, authorship and submission receipt.

### Learning resource governance

The resource library keeps the previously recorded verified videos and official documentation. It is reorganised by beginner path and course day. It does not add paid requirements, does not present external examples as project evidence and preserves the existing link-status interpretation.

## Bilingual-manifest enforcement

The following files are now marked `complete` and require both bilingual markers:

- `START_HERE.md`
- `READINESS_GUIDE.md`
- `COLAB_GUIDE.md`
- `GITHUB_GUIDE.md`
- `FAQ.md`
- `TROUBLESHOOTING.md`
- `LEARNING_RESOURCES.md`

The manifest continues to enforce all notebooks, daily guides, governance documents, rubric, submission guide and course-alignment matrix.

## Acceptance gates

Phase 10 is accepted when:

1. `Bilingual Content Check` passes with the expanded manifest.
2. Local Markdown-link validation passes.
3. External resource link checking reports no unresolved broken required resource.
4. Environment and notebook smoke checks remain green.
5. Released-reference parity remains green for Days 1–5.
6. Notebook 99 contract and structural validation remain green.

## Release boundary

The branch remains a controlled `v1.1.0` candidate. This phase does not merge to `main`, publish a release or claim hosted-Colab acceptance. Remaining release work includes public-portal synchronisation, final release-hash rebuild, hosted-Colab acceptance, visual/responsive review, private evaluator and private submission registry.