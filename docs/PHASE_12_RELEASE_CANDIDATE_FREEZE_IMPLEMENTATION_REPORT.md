# Phase 12 · Release Candidate Freeze Controls
# المرحلة 12 · ضوابط تجميد مرشح الإصدار

## Scope | النطاق

This phase converted the pre-release design into persistent release-candidate evidence while keeping `v1.1.0` unpublished.

حوّلت هذه المرحلة تصميم ما قبل الإصدار إلى أدلة ثابتة لمرشح الإصدار مع إبقاء `v1.1.0` غير منشور.

## Implemented | ما تم تنفيذه

- Updated `Release Candidate Integrity` to generate and persist `release/release_manifest.candidate.json` on the controlled development branch.
- Preserved a copy of the manifest in the workflow artifact.
- Added `docs/HOSTED_COLAB_ACCEPTANCE_RECORD.md` for signed manual execution evidence.
- Added `release/RELEASE_FREEZE_STATUS.md` with automated, manual and private release gates.
- Opened public tracking issue `#2` without exposing hidden labels, identities, grades or receipt data.
- Kept the final immutable tag and exact commit SHA outside the manifest to avoid circular identity.

## Candidate integrity identity | هوية سلامة المرشح

```text
release_version: v1.1.0
file_count: 35
aggregate_sha256: b4a6c05eca0b1b7716a97c89d2c80b5a63052ace9892ea8b625e696d18a5a53b
```

This is a candidate inventory, not the final release manifest. It remains refreshable until manual Colab acceptance and private controls pass.

هذا جرد مرشح وليس Manifest الإصدار النهائي. يبقى قابلًا للتحديث حتى نجاح اعتماد Colab والضوابط الخاصة.

## Automated evidence | الأدلة الآلية

The release-candidate workflow completed successfully after generating the persistent candidate manifest. Existing bilingual, environment, reference-parity, notebook-smoke and Notebook 99 gates remained enabled.

## Deliberate limitations | الحدود المقصودة

- Hosted Colab acceptance is not claimed as complete.
- Visual bilingual rendering inside hosted Colab is not claimed as complete.
- The private evaluator repository has not been created through the current connector.
- The private submission registry has not been created through the current connector.
- No final `release_manifest.json`, tag, merge or public release is authorised.

## Release decision | قرار الإصدار

```text
CANDIDATE_READY_FOR_MANUAL_ACCEPTANCE
NOT_AUTHORISED_FOR_MERGE_OR_PUBLICATION
```
