# بيانات Tamweel Lite

ابدأ بـ[دليل البيانات](DATA_GUIDE.md) و[قاموس الخصائص](feature_dictionary.csv). البيانات اصطناعية بالكامل: 10,000 طلب تدريب و2,500 طلب تحدٍّ دون إجابات.

يفحص دفتر الاستعداد أسماء الأعمدة والأنواع والنطاقات وبصمات الملفات قبل تحميلها. استخدم `data_contract.json` مرجعًا للقواعد و`data_manifest.json` مرجعًا للبصمات.

لا تستخدم عمودي نسخة التسرب في النموذج النهائي، ولا ترفع بيانات عملاء حقيقيين أو معلومات شخصية. لا تضع الهدف أو أعمدة ما بعد النتيجة في بيانات التحدي.

The notebook downloads and verifies the released CSV files. All records are synthetic; identifiers and dates are for tracing and splitting, not prediction.
