# Phase 11 — Pre-release integrity controls | المرحلة 11 — ضوابط النزاهة قبل الإصدار

## Scope | النطاق

This phase adds deterministic release-manifest generation, static release-candidate validation, hosted-Colab acceptance instructions and controlled specifications for the private evaluator and private submission registry.

تضيف هذه المرحلة توليد Manifest حتمي للإصدار، وفحصًا ثابتًا لمرشح الإصدار، وتعليمات اعتماد Colab المستضاف، ومواصفات محكومة للمقيم الخاص وسجل التسليم الخاص.

## Implemented files | الملفات المنفذة

```text
release/release_scope.json
scripts/build_release_manifest.py
scripts/check_release_candidate.py
.github/workflows/release_candidate.yml
docs/HOSTED_COLAB_ACCEPTANCE.md
docs/PRIVATE_EVALUATOR_SPEC.md
docs/PRIVATE_SUBMISSION_REGISTRY_SPEC.md
RELEASE_NOTES.md
docs/PHASE_11_PRERELEASE_CONTROLS_IMPLEMENTATION_REPORT.md
```

## Design decisions | القرارات التصميمية

1. The integrity manifest excludes itself and does not embed a commit SHA, preventing circular hashing.
2. The immutable release tag and exact commit SHA remain separate release-record fields.
3. Candidate checks scan required bilingual files, unfinished placeholders, prohibited legacy wording and obvious secret patterns.
4. Hosted-Colab acceptance remains a manual gate and cannot be inferred from GitHub Actions alone.
5. Hidden labels and evaluator tests are specified but not placed in the public learner repository.
6. Submission receipts remain private and distinct from technical readiness or grades.

1. يستبعد Manifest النزاهة نفسه ولا يضمّن SHA للـCommit حتى لا ينشأ اعتماد دائري.
2. يبقى Tag غير القابل للتغيير وSHA الدقيق حقولًا مستقلة في سجل الإصدار.
3. يفحص مرشح الإصدار الملفات الثنائية المطلوبة والعبارات القديمة والعناصر غير المكتملة وأنماط الأسرار الظاهرة.
4. يبقى اعتماد Colab اختبارًا يدويًا ولا يُستنتج من GitHub Actions وحده.
5. تم توثيق الأصول المخفية واختبارات المقيم دون وضعها في المستودع العام.
6. يبقى إيصال التسليم خاصًا ومنفصلًا عن الجاهزية التقنية والدرجة.

## Claims and limitations | الادعاءات والحدود

This phase can prove that the candidate repository has a deterministic integrity inventory and passes static consistency checks. It does not claim that hosted Colab has been manually accepted, that the private evaluator exists, or that the private submission registry has been deployed.

تثبت هذه المرحلة وجود جرد نزاهة حتمي واجتياز فحوص الاتساق الثابتة. ولا تدعي اكتمال اختبار Colab اليدوي أو إنشاء المقيم الخاص أو تشغيل سجل التسليم الخاص.

## Next gate | البوابة التالية

- Run the new `Release Candidate Integrity` workflow.
- Complete hosted-Colab acceptance using a full learner snapshot.
- Create and test the private evaluator repository.
- Create and test the private submission registry.
- Freeze learner-facing files and commit the final `release/release_manifest.json`.
- Coordinate the portal and learner-template release.
