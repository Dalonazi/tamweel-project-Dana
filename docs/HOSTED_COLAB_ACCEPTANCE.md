# Hosted Colab acceptance protocol | بروتوكول اعتماد Colab المستضاف

<!-- BILINGUAL:EN -->
<!-- BILINGUAL:AR -->

This protocol is the final manual gate for the free hosted-Colab path. GitHub Actions smoke tests do not replace it.

هذا البروتوكول هو بوابة الاعتماد اليدوية النهائية لمسار Colab المجاني المستضاف. لا تستبدله اختبارات GitHub Actions.

## Test identity | هوية الاختبار

| Field | Value |
|---|---|
| Candidate version | `v1.1.0` |
| Repository | `almiyead-rgb/sda-dsc-211-student-template` |
| Candidate branch or exact SHA | Record before starting |
| Google account | Clean account without prior course files |
| Browser | Chrome and Edge on Windows |
| Runtime | Free CPU only |
| Drive mount | Not used |
| API keys / paid services | Not used |

## Acceptance sequence | تسلسل الاعتماد

| Step | English acceptance action | إجراء الاعتماد بالعربية | Evidence |
|---:|---|---|---|
| 1 | Open Notebook 00 from the canonical Colab link in a private/incognito window. | افتح دفتر 00 من رابط Colab المعتمد داخل نافذة خاصة. | Screenshot of source URL and runtime |
| 2 | Select free CPU and run all cells from a new session. | اختر CPU المجاني وشغّل جميع الخلايا من جلسة جديدة. | Executed notebook and readiness JSON files |
| 3 | Create a temporary learner repository from the template. | أنشئ مستودع متدرب تجريبيًا من القالب. | Repository URL and initial SHA |
| 4 | Execute Notebooks 01–05, each from a fresh runtime, without hidden local files. | شغّل دفاتر 01–05، وكل دفتر في جلسة جديدة، دون ملفات محلية مخفية. | Executed notebooks, exported artifacts and elapsed times |
| 5 | Save each executed notebook and all required outputs in the temporary repository. | احفظ كل دفتر منفذ وجميع المخرجات المطلوبة في المستودع التجريبي. | Commit SHAs for each day |
| 6 | Run Notebook 99 against the complete repository snapshot. | شغّل دفتر 99 على نسخة المشروع المكتملة. | Self-check report and final bundle |
| 7 | Run GitHub Actions → Final Project Check on the same exact commit. | شغّل Final Project Check على Commit نفسه. | Workflow URL and result |
| 8 | Create a final tag on the checked commit and verify that tag and SHA resolve to the same version. | أنشئ Tag نهائيًا على Commit الذي تم فحصه وتحقق من تطابقهما. | Tag URL and exact 40-character SHA |
| 9 | Repeat the rendering review at 1366 px, 1024 px and a narrow mobile width. | كرر مراجعة العرض عند 1366 و1024 وعرض جوال ضيق. | Screenshots of bilingual cells |
| 10 | Repeat the critical path in Edge after completing Chrome. | كرر المسار الحرج في Edge بعد إتمام Chrome. | Browser-specific result |

## Pass criteria | معايير الاجتياز

- No paid upgrade, GPU, Drive mount, token or API key is required.
- Every primary notebook completes with `Run all` in the documented order.
- English remains on the left and Arabic on the right at desktop widths.
- Narrow screens remain readable without mandatory horizontal scrolling.
- Exported files exist on the learner device and inside the learner repository.
- Notebook 99 and the final workflow inspect the same exact project version.
- Recovery output is never accepted as personal execution evidence in assessment mode.
- No private labels, hidden evaluator assets or secrets appear in the public repository.

- لا يلزم شراء ترقية أو GPU أو ربط Drive أو Token أو مفتاح API.
- يكتمل كل دفتر أساسي عبر `Run all` بالترتيب الموثق.
- تبقى الإنجليزية يسارًا والعربية يمينًا على الشاشات المكتبية.
- تبقى الشاشات الضيقة مقروءة دون تمرير أفقي إلزامي.
- توجد الملفات المصدرة على جهاز المتدرب وداخل مستودعه.
- يفحص دفتر 99 والـWorkflow النهائي النسخة الدقيقة نفسها.
- لا تُقبل مخرجات التعافي بوصفها دليل تنفيذ شخصي داخل وضع التقييم.
- لا تظهر تسميات خاصة أو أصول المقيم المخفية أو الأسرار في المستودع العام.

## Evidence record | سجل الأدلة

Create `docs/acceptance/HOSTED_COLAB_RESULT.md` only after the manual run. Record:

- tester name or controlled identifier;
- date and time zone;
- browser and version;
- candidate SHA;
- result for each notebook;
- installation time and execution time;
- screenshots or private evidence references;
- defects found and corrective commit;
- final decision: `PASS`, `PASS WITH LIMITATIONS`, or `FAIL`.

لا يُنشأ سجل النتيجة إلا بعد التشغيل اليدوي الفعلي، ولا يجوز وضع حالة `PASS` اعتمادًا على GitHub Actions وحدها.
