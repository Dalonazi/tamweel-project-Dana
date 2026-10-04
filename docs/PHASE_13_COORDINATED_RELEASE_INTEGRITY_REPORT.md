# Phase 13 — Coordinated Release Integrity | المرحلة 13 — سلامة الإصدار المنسق

## Decision | القرار

The learner template remains a controlled `v1.1.0` candidate. This phase corrected the release inventory mechanism and linked the learner candidate to an independently checked portal candidate identity. It did not authorise merge, tagging or publication.

يبقى قالب المتدرب مرشحًا محكومًا للإصدار `v1.1.0`. صححت هذه المرحلة آلية جرد ملفات الإصدار وربطت مرشح المتدرب بهوية بوابة يجري التحقق منها بصورة مستقلة. لم تمنح المرحلة تصريح الدمج أو إنشاء Tag أو النشر.

## Defect found | الخلل المكتشف

The original release manifest used `Path.glob()` on patterns such as:

```text
content/**
data/**
scripts/**
.github/workflows/**
```

Some patterns resolved to directories. The collector skipped directories and therefore silently omitted their nested files. The first candidate identity contained 35 files and was incomplete.

كانت أداة Manifest تستخدم `Path.glob()` مع أنماط مجلدات، وقد تعيد هذه الأنماط المجلد نفسه. كانت الأداة تتجاوز المجلدات، ولذلك أسقطت ملفاتها المتداخلة بصمت. احتوت الهوية الأولى على 35 ملفًا وكانت غير مكتملة.

## Correction | التصحيح

`scripts/build_release_manifest.py` now:

1. Expands every include pattern.
2. Adds directly matched files.
3. Recurses through every matched directory using `rglob('*')`.
4. Applies exclusions to every resolved file.
5. Deduplicates by repository-relative path.
6. Sorts paths before calculating the aggregate digest.

## Corrected learner identity | هوية المتدرب المصححة

```text
manifest: release/release_manifest.candidate.json
file_count: 127
aggregate_sha256: 5e45aaf207fc67c605519e0fbdf8c67a9f67f5da42cc0954c0780544c3fc55c8
```

The previous 35-file identity is superseded and must not be used in approval records.

## Cross-repository evidence | أدلة المستودعين

The portal repository now stores:

```text
release/coordinated_candidate.json
```

It pins the learner identity above and the portal candidate identity. The automated `Coordinated v1.1.0 Candidate Check` fetches both committed manifests and compares:

- release version,
- repository identity,
- file count,
- aggregate SHA-256,
- internal file-list count consistency.

The coordinated check passed after the corrected manifests were committed.

## Automated state | الحالة الآلية

- Release Candidate Integrity after correction: PASS.
- Notebook 99 contract and structure: PASS.
- Bilingual, environment, Days 1–5 reference parity and notebook smoke gates remain active.
- Portal cross-repository candidate identity check: PASS.

## Remaining manual/private gates | البوابات اليدوية والخاصة المتبقية

- Hosted Colab acceptance and signed record.
- Hosted Colab bilingual visual review.
- Private evaluator repository and hidden synthetic assets.
- Exact-SHA inference and anti-hard-coding tests.
- Private submission registry and immutable receipt test.
- Final content freeze.
- Final manifest generation from the frozen tree.
- Coordinated merge and `v1.1.0` publication.

## Release status | حالة الإصدار

```text
AUTOMATED_CANDIDATE_INTEGRITY: PASS
HOSTED_COLAB_ACCEPTANCE: PENDING
PRIVATE_EVALUATOR: PENDING
PRIVATE_SUBMISSION_REGISTRY: PENDING
MERGE_AUTHORISED: NO
PUBLICATION_AUTHORISED: NO
```
