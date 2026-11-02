PAGES4 = {
"gemma-3": {
    "title": "Gemma-3 12B و 27B (استخرهای قدیمی)",
    "title_plain": "Gemma-3 12B / 27B",
    "status": "live",
    "chip": "بات‌های قدیمی MCI، نه EX",
    "summary": "خلاصهٔ یک‌بندی برای TPM: نسل قبلی Gemma هنوز چند چت‌بات قدیمی MCI را سرو می‌کند. مدل 12B یک استقرار کوچک Kubernetes به‌علاوهٔ دو پردازهٔ bare-metal دارد. مدل 27B فقط روی bare-metal است و load balancer آن روی صفر replica است، پس بات‌ها با IP خام به آن می‌رسند. هیچ بخشی از EX از Gemma-3 استفاده نمی‌کند. پرسش اصلی TPM این است که این بات‌ها چه زمانی مهاجرت می‌کنند تا GPUها آزاد شوند.",
    "facts": [
        ("مدل (واقعیت)", "Gemma-3 12B-it و 27B-it، متراکم، چندوجهی (متن + تصویر)، منتشرشده در 2025"),
        ("context بومی (واقعیت)", "128K"),
        ("پاد 12B", "vLLM **v0.11.0**، سقف 15K، بدون پرچم ویژه، 1 replica (`prod/gemma3-12b/values.yaml:2,5,86-92`)"),
        ("LB مربوط به 12B", "`gemma3-12-llm-lb`: پاد + `172.16.21.4:7000/7001` (`prod/gemma3-12-llm-lb/values.yaml:222-233`)"),
        ("LB مربوط به 27B", "`gemma3-27-llm-lb`، **0 replica**، upstreamها `172.16.21.4:8001/8005` (`prod/gemma3-27-llm-lb/values.yml:2,198-204`)"),
    ],
    "sections": [
        ("چه کسی از آن استفاده می‌کند", ({"table": [
            ["مدل", "سرویس", "چگونه", "مرجع"],
            ["27B", "chatbot-mci، chatbot-mci-agent-chat، chatbot-mcymci-redirector", "از طریق `gemma3-27-llm-lb` (که 0 replica دارد!)", "`prod/chatbot-mci/values.yaml:1008`، `prod/chatbot-mci-agent-chat/values.yaml:881`، `prod/chatbot-mcymci-redirector/values.yaml:1397`"],
            ["27B (استنباطی)", "chatbot-arbaeen، chatbot-bale، chatbot-mci-clone، chatbot-mymci-arbaeen، chatbot-rubika", "`http://172.16.21.4:8001/v1` خام", "`prod/chatbot-arbaeen/values.yaml:929`، `prod/chatbot-bale/values.yaml:1048`"],
            ["12B (استنباطی)", "chatbot-mci-clone", "`http://172.16.21.4:8000/v1` خام", "`prod/chatbot-mci-clone/values.yaml:422`"],
            ["12B", "چند بات", "در 2026-10-07 به AxonHub منتقل شدند (`5ef9c30f6`)", "git"],
        ]},)),
        ("چرا آنجا استفاده می‌شود (استنباطی)", "بات‌هایی که پیش از Gemma-4 ساخته شده‌اند روی پرامپت‌های Gemma-3 تنظیم شده‌اند؛ مهاجرت به آزمون دوبارهٔ پرامپت نیاز دارد."),
        ("مصالحه‌ها", [
            "vLLM 0.11.0 چندین نسخه عقب است (0.25.1 جاهای دیگر): parserهای Gemma-4 را ندارد و زمان‌بندی قدیمی‌تری دارد.",
            "فراخواننده‌های با IP خام از هر health check مربوط به LB دور می‌زنند.",
        ]),
        ("ریسک‌ها و پرسش‌های باز", [
            "اگر LB واقعاً 0 پاد داشته باشد، فراخواننده‌های `gemma3-27-llm-lb` خطای اتصال می‌گیرند (مگر fallback داشته باشند) — بررسی کنید این بات‌ها واقعاً زنده‌اند.",
            "Exporter برای 12B فقط `172.16.21.4:7001` را scrape می‌کند.",
        ]),
        ("چگونه مشاهده‌اش کنیم", [
            "`vllm-gemma3-12-gpu-exporter` (bare-metal پورت 7001) و ServiceMonitor پاد 12B.",
        ]),
    ],
},
"gpt-oss-120b": {
    "title": "gpt-oss-120b (MoE با وزن باز از OpenAI)",
    "title_plain": "gpt-oss-120b",
    "status": "live",
    "chip": "عمدتاً بازنشسته",
    "summary": "خلاصهٔ یک‌بندی برای TPM: gpt-oss-120b مدل بزرگ با وزن باز از OpenAI است: حدود 117B پارامتر اما فقط حدود 5B فعال در هر توکن، با استدلال و استفادهٔ قوی از ابزار. قبلاً یکی از مدل‌های اصلی بات‌های MCI و AQA بود. در اواسط اکتبر 2026 بیشتر فراخواننده‌ها به Gemma-4 26B-A4B منتقل شدند. پاد Kubernetes آن روی صفر است، اما هنوز دو load balancer به دوازده پورت bare-metal پخش می‌کنند و یک سرویس نمایشی هنوز آن را صدا می‌زند. همچنین به‌عنوان پیش‌فرض کد برای چند گام aiva باقی مانده است؛ اگر روزی یک متغیر env حذف شود، این مهم می‌شود.",
    "facts": [
        ("مدل (واقعیت)", "OpenAI gpt-oss-120b، وزن‌های باز با مجوز Apache-2.0، فقط متن، MoE"),
        ("اندازه (واقعیت)", "حدود 117B کل، حدود 5.1B فعال؛ وزن‌های MXFP4 روی یک GPU با 80 GB جا می‌شوند"),
        ("context بومی (واقعیت)", "128K"),
        ("پاد k8s", "vLLM v0.11.0، سقف 15K، **0 replica**، بدون پرچم parser برای استدلال/ابزار (`prod/gpt-oss-120b/values.yaml:2,5,84-93`)"),
        ("LBها", "`gpt-oss-120-llm-lb` (10 bare-metal)، `gpt-oss-120-iva-llm-lb` (2 bare-metal)"),
    ],
    "sections": [
        ("چگونه اینجا سرو می‌شود", {"table": [
            ["LB", "upstreamها", "مرجع"],
            ["gpt-oss-120-llm-lb", "پاد (0 replica) + `172.16.21.4:8122/8124/8125/8126` + `172.23.0.3:8010-8015`", "`prod/gpt-oss-120-llm-lb/values.yaml:222-288`"],
            ["gpt-oss-120-iva-llm-lb", "`172.16.21.4:8120/8121`", "`prod/gpt-oss-120-iva-llm-lb/values.yaml:222-228`"],
        ]}),
        ("چه کسی از آن استفاده می‌کند", [
            "زنده: `demo-iva-sales` از طریق استخر IVA (`prod/demo-iva-sales/values.yaml:75`).",
            "ارجاع‌های کامنت‌شده در chatbot-mci، rubika، bale، ewano، mci-iva، mobinnet.",
            "پیش‌فرض‌های کد: `openai/gpt-oss-120b` برای فیلتر context، فیلتر دستورالعمل‌ها، intent، voice bridge، دسته‌بندی و روشن‌سازی در aiva (`phoenix:python/aiva/aiva/chat/config.py:111,124,160,206,220,232`).",
        ]),
        ("چرا کم‌رنگ شد", "commitها: “feat: changed the old gpt oss model urls to new gemma4 26b” (`62c1f34ab`، 2026-10-14) و “changing oss to gemma” (`220cf41ea`، 2026-10-17). دلایل محتمل (استنباطی): اداره کردن یک خانوادهٔ مدل آسان‌تر است؛ Gemma-4 فارسی را بهتر مدیریت می‌کند؛ vLLM قدیمی parser ابزار برای gpt-oss نداشت."),
        ("مصالحه‌ها", [
            "حدود 5B فعال آن را در هر توکن به سرعت 26B-A4B می‌رساند، با دانش کل بیشتر؛ اما خروجی استدلال (قالب harmony) توکن اضافه می‌کند و به تجزیهٔ درست نیاز دارد.",
        ]),
        ("ریسک‌ها و پرسش‌های باز", [
            "12 پورت bare-metal هنوز اختصاص دارند؛ چه کسی از آن‌ها استفاده می‌کند؟ شاید کانال‌های AxonHub.",
            "Exporter مقدار `172.23.0.3:8017` را scrape می‌کند که هیچ LB از آن استفاده نمی‌کند.",
        ]),
        ("چگونه مشاهده‌اش کنیم", [
            "exporter با نام `vllm-gpt-oss-120` (`172.16.21.4:8120-8126`، `172.23.0.3:8011-8017`).",
        ]),
    ],
},
}
