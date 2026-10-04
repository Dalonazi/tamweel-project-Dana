# Release Freeze Status | حالة تجميد الإصدار

**Target | الهدف:** `v1.1.0`  
**Repository | المستودع:** `almiyead-rgb/sda-dsc-211-student-template`  
**Current state | الحالة الحالية:** `CANDIDATE — NOT RELEASED | مرشح — غير منشور`

## Corrected candidate identity | هوية المرشح المصححة

```text
file_count: 127
aggregate_sha256: 5e45aaf207fc67c605519e0fbdf8c67a9f67f5da42cc0954c0780544c3fc55c8
```

The release-manifest builder was corrected to recurse through directories matched by patterns such as `content/**`, `data/**`, `scripts/**` and `.github/workflows/**`. The earlier 35-file identity omitted nested files and is superseded.

صُححت أداة Manifest لتتوسع داخل المجلدات المطابقة لأنماط مثل `content/**` و`data/**` و`scripts/**` و`.github/workflows/**`. أصبحت هوية 35 ملفًا السابقة ملغاة لأنها أسقطت ملفات متداخلة.

## Automated controls | الضوابط الآلية

- [x] Bilingual content validation
- [x] Environment validation
- [x] Reference parity for Days 1–5
- [x] Fresh-kernel notebook smoke test
- [x] Notebook 99 contract and structural validation
- [x] Release-candidate integrity validation
- [x] Deterministic recursive candidate manifest generation
- [x] Cross-repository candidate identity check with the portal

## Manual and private controls | الضوابط اليدوية والخاصة

- [ ] Hosted Colab acceptance completed and signed
- [ ] Visual bilingual rendering reviewed in hosted Colab
- [ ] Private evaluator repository created and tested
- [ ] Hidden evaluation assets generated and access-restricted
- [ ] Private submission registry created and receipt workflow tested
- [ ] Final release notes reviewed
- [x] Learner and portal candidate manifests cross-checked automatically
- [ ] Final learner-facing content freeze approved
- [ ] Final `release_manifest.json` generated after freeze
- [ ] Coordinated merge and `v1.1.0` publication approved

## Freeze rule | قاعدة التجميد

No merge, tag or public release is authorised while any mandatory item above remains unchecked. The candidate manifest may be refreshed during development; the final manifest is generated only after manual acceptance and private-control testing.

لا يُسمح بالدمج أو إنشاء Tag أو نشر الإصدار ما دام أي بند إلزامي أعلاه غير مكتمل. يجوز تحديث Manifest المرشح أثناء التطوير، أما Manifest النهائي فلا يُنشأ إلا بعد اعتماد Colab واختبار الضوابط الخاصة.
