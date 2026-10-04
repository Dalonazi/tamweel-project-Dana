# Hosted Colab Acceptance Record | سجل اعتماد Colab المستضاف

**Release candidate | مرشح الإصدار:** `v1.1.0`  
**Repository | المستودع:** `almiyead-rgb/sda-dsc-211-student-template`  
**Status | الحالة:** `PENDING MANUAL EXECUTION | بانتظار التنفيذ اليدوي`

> This record must be completed from a clean Google account and a fresh hosted Colab session. GitHub Actions success does not replace this acceptance test.  
> يجب إكمال هذا السجل باستخدام حساب Google نظيف وجلسة Colab مستضافة جديدة. لا يحل نجاح GitHub Actions محل اختبار الاعتماد هذا.

## Test identity | بيانات الاختبار

| Field | Value |
|---|---|
| Tester |  |
| Date and time |  |
| Browser and version |  |
| Operating system |  |
| Google account condition | Clean test account / حساب اختبار نظيف |
| Candidate commit SHA |  |
| Candidate manifest aggregate SHA-256 |  |

## Required execution matrix | مصفوفة التشغيل الإلزامية

| Check | Expected evidence | Result | Notes |
|---|---|---|---|
| Notebook 00 in a new CPU runtime | `Environment ready` and `READY`; four JSON artifacts | ☐ PASS ☐ FAIL |  |
| Notebook 01 in a new CPU runtime | Model comparison and complete Day 1 artifacts | ☐ PASS ☐ FAIL |  |
| Notebook 02 in a new CPU runtime | Leakage, validation, Optuna and OOF evidence | ☐ PASS ☐ FAIL |  |
| Notebook 03 in a new CPU runtime | Threshold, capacity, sensitivity and Decision Card | ☐ PASS ☐ FAIL |  |
| Notebook 04 in a new CPU runtime | Permutation, SHAP, calibration and interpretation report | ☐ PASS ☐ FAIL |  |
| Notebook 05 in a new CPU runtime | Ensemble decision, portable model and final package | ☐ PASS ☐ FAIL |  |
| Save executed notebooks | Files appear in the correct learner repository | ☐ PASS ☐ FAIL |  |
| Download generated artifacts | Files exist on the local device and open successfully | ☐ PASS ☐ FAIL |  |
| Notebook 99 on a complete learner snapshot | Final self-check report and bundle are produced | ☐ PASS ☐ FAIL |  |
| GitHub Final Project Check | Green run on the exact submitted commit | ☐ PASS ☐ FAIL |  |
| Final tag and SHA | Tag resolves to the recorded 40-character SHA | ☐ PASS ☐ FAIL |  |

## Bilingual rendering review | مراجعة العرض الثنائي

Review Notebook 00, one concept-heavy daily notebook, and Notebook 99 at practical widths.

| Width or device | English left / Arabic right | No forced horizontal scrolling | Readable tables | Result |
|---|---:|---:|---:|---|
| Desktop 1366 px | ☐ | ☐ | ☐ | ☐ PASS ☐ FAIL |
| Laptop 1024 px | ☐ | ☐ | ☐ | ☐ PASS ☐ FAIL |
| Narrow/mobile approximation | Stacked or readable | ☐ | ☐ | ☐ PASS ☐ FAIL |

## Failure handling | معالجة الفشل

For every failure, record:

```text
Notebook or step:
Exact visible error:
Cell or section:
Runtime type:
Whether restart was attempted:
Screenshot or log reference:
Corrective commit SHA:
Retest result:
```

Do not mark the release accepted while any mandatory row is failed or untested.

## Acceptance decision | قرار الاعتماد

- [ ] **ACCEPTED** — all mandatory checks passed on hosted Colab.
- [ ] **REJECTED** — one or more mandatory checks failed.
- [ ] **DEFERRED** — testing is incomplete; no release decision is made.

**Tester signature/name | اسم المنفذ:**  
**Approval date | تاريخ الاعتماد:**  
**Evidence location | موقع الأدلة:**  
