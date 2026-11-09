"""Persian model pages, part 2 (openai-frontier .. silero-vad). Mirrors content_en_models.py."""

PAGES2 = {
    "openai-frontier": {
        "title": "OpenAI gpt-6-luna و gpt-5.6-sol (بیرونی)",
        "title_plain": "gpt-6-luna / gpt-5.6-sol",
        "status": "external",
        "chip": "خوشامدگویی EX",
        "summary": "در یک پاراگراف: این‌ها مدل‌های میزبانی‌شدهٔ OpenAI هستند که از طریق اینترنت و relayهای خروجی (egress) MCI صدا زده می‌شوند. در EX فقط خوشامدگویی ابتدایی از `gpt-6-luna` استفاده می‌کند: این پیام پیش از آنکه تماس‌گیرنده چیزی بگوید تولید می‌شود، پس گفتار کارکنان ارسال نمی‌شود (البته درخواست شامل prompt خوشامدگویی و هر context نشستی است که prompt بیاورد). محصولات خواهر یعنی aiva، aiva-neda و aiva-poll فراتر می‌روند و `gpt-6-luna` را به‌عنوان عامل اصلی پاسخ‌گویی به کار می‌برند، و ابزار پرسش از داده در AQA آن را برای نوشتن SQL استفاده می‌کند. اندازه و context این مدل‌ها عمومی نیست و این نام‌ها از روی مخزن‌ها قابل تأیید نیستند.",
        "facts": [
            ("فروشنده", "OpenAI، اختصاصی، فقط API"),
            ("اندازه / context", "عمومی نیست؛ این‌جا قابل راستی‌آزمایی نیست"),
            ("Endpoint", "`https://api.openai.com/v1` از طریق `envoy-relay-chatbot` (`prod/chatbot-ex/values.yaml:2510-2521`)"),
            ("کلید", "secret با نام `chatbot-mci/OPENAI_API_KEY_MAIN` (`:2515-2519`)"),
            ("Reasoning effort", "برای خوشامدگویی EX مقدار `'none'` (`:2522-2523`)"),
        ],
        "sections": [
            ("چه کسی استفاده می‌کند", {"table": [
                ["سرویس", "مؤلفه", "نقش", "مدل", "مرجع"],
                ["chatbot-ex (EX)", "iva-chatbot", "عامل خوشامدگویی", "gpt-6-luna", "`prod/chatbot-ex/values.yaml:2510-2514`"],
                ["aiva", "api", "**عامل اصلی** + خوشامدگویی", "gpt-6-luna", "`prod/aiva/values.yaml:95,189`"],
                ["aiva-neda", "api, api_sms, api_bale", "عامل اصلی + خوشامدگویی", "gpt-6-luna", "`prod/aiva-neda/values.yaml:93,188,1561,1909`"],
                ["aiva-poll", "api", "عامل اصلی + خوشامدگویی", "gpt-6-luna", "`prod/aiva-poll/values.yaml:117,209`"],
                ["aqa", "api (NL2SQL)", "عامل SQL", "gpt-6-luna", "`prod/aqa/values.yaml:723`"],
                ["aiva-aqa", "chainlit, api", "عامل", "gpt-5.6-sol", "`prod/aiva-aqa/values.yaml:85,719`"],
            ]}),
            ("چرا آن‌جا استفاده می‌شود", (
                "کامیت‌ها: در خوشامدگویی EX کامیت “chroe(chatbot-ex): change iva-chatbot” (`90580f4f9`، 2026-10-31) نشانی مدل 26B را کامنت کرد و luna را گذاشت؛ در aiva ابتدا “change model to sol” و سپس “change model to luna” (2026-08-27)؛ در aqa “update model to luna” (`071b07a1c`، 2026-10-31).",
                "تفسیر (استنباطی): خوشامدگویی لحن کل تماس را تعیین می‌کند و تنها لحظه‌ای است که عبارت‌پردازی طبیعی یک مدل frontier بیشترین اثر را دارد، در حالی که هنوز هیچ داده‌ای از تماس‌گیرنده وجود ندارد. EX luna را برای عامل اصلی هم امتحان کرد و همان روز دوباره به مدل داخلی برگرداند (`5847d0382`)، که با نگرانی اقامت داده‌های HR جور است.",
            )),
            ("مبادلات (Trade-offs)", [
                "بالاترین کیفیت و بدون هزینهٔ GPU، اما صورت‌حساب به‌ازای هر توکن، تأخیر اینترنت و وابستگی به relay خروجی.",
                "داده از MCI خارج می‌شود: برای خوشامدگویی قابل‌قبول است، برای گفتگوهای HR حساس است.",
            ]),
            ("ریسک‌ها و پرسش‌های باز", [
                "اگر OpenAI یا relay از کار بیفتد، تماس EX خوشامدگویی ندارد؛ آیا متن جایگزین (fallback) وجود دارد؟",
                "با بخش حقوقی/امنیت تأیید کنید کدام فیلدهای prompt به OpenAI می‌رسند.",
                "هزینهٔ توکن در Prometheus نیست؛ از داشبوردهای usage در OpenAI یا spanهای Phoenix استفاده کنید.",
            ]),
            ("چگونه مشاهده کنیم", [
                "Phoenix `chatbot-ex-iva`: spanهای خوشامدگویی با `llm.model_name = gpt-6-luna`.",
                "لاگ‌های relay خروجی برای `api.openai.com`.",
            ]),
        ],
    },
    "openai-legacy": {
        "title": "سایر نام‌های مدل OpenAI: پیکربندی زنده و پیش‌فرض‌های کد",
        "title_plain": "سایر نام‌های OpenAI",
        "status": "external",
        "chip": "در EX زنده استفاده نمی‌شود",
        "summary": "در یک پاراگراف: بسیاری از سرویس‌های قدیمی‌تر یا کوچک‌تر مستقیماً مدل‌های OpenAI را صدا می‌زنند و بسیاری از کدبیس‌ها وقتی یک متغیر محیطی تنظیم نشده باشد به یک مدل OpenAI برمی‌گردند. هیچ‌کدام امروز روی مسیر زندهٔ EX نیستند، اما پیش‌فرض‌ها اهمیت دارند: حذف یک متغیر محیطی در EX می‌تواند بی‌صدا ترافیک را به OpenAI بفرستد.",
        "facts": [
            ("فروشنده", "OpenAI، اختصاصی"),
            ("واقعیت‌های شناخته‌شده", "gpt-4o / gpt-4o-mini: context برابر 128K؛ gpt-4.1-mini: حدود 1M context؛ gpt-3.5-turbo: 16K؛ text-embedding-ada-002: بردار 1536 بعدی؛ text-embedding-3-large: بردار 3072 بعدی، ورودی 8K"),
            ("قابل‌راستی‌آزمایی‌نیست", "gpt-5.4-mini: اندازه و context عمومی نیست"),
        ],
        "sections": [
            ("پیکربندی زنده", {"table": [
                ["مدل", "سرویس‌ها", "مرجع"],
                ["gpt-5.4-mini", "se-agent", "`prod/se-agent/values.yaml:70`"],
                ["gpt-4.1-mini", "chatbot-mci-iva-avatar, chatbot-mci-english-iva-avatar, chatbot-mci-iva-load-test", "`prod/chatbot-mci-iva-avatar/values.yaml:113`; `prod/chatbot-mci-english-iva-avatar/values.yaml:117`; `prod/chatbot-mci-iva-load-test/values.yaml:1440`"],
                ["gpt-4o-mini / gpt-4o", "chatbot-mci-ar/en/fa/sms/telecom, tejarat(-temp), telecom, xperix-assistant, bale, rubika, mymci-arbaeen, mcymci-redirector", "برای نمونه `prod/chatbot-mci-fa/values.yaml:100`"],
                ["gpt-3.5-turbo, text-embedding-ada-002", "chatbot-feedback-service", "`prod/chatbot-feedback-service/values.yaml:40,52,54`"],
            ]}),
            ("پیش‌فرض‌های کد (فقط وقتی متغیر محیطی تنظیم نشده باشد)", {"table": [
                ["پیش‌فرض", "کجا", "ارتباط با EX"],
                ["`gpt-4.1-mini` (LLM), `text-embedding-3-large` (embedding)", "`phoenix:python/agentlib/agentlib/llm/openai/llm.py:42`; `agentlib/embedding/openai/embedding.py:36`", "agentlib پایهٔ مغز EX است"],
                ["`text-embedding-3-large`", "`phoenix:python/aiva/aiva/chat/config.py:49`; `python/aiva-knowledgebase/aiva_kb/config.py:19`", "EX آن را با hakim-unsup جایگزین می‌کند"],
                ["`gpt-4o-mini`", "`phoenix:python/coa-api/coa/config.py:225`", "coa-api در EX کلید OpenAI و پروکسی دارد اما `OPENAI_MODEL` ندارد: اگر مسیری از کد آن را صدا بزند، پیش‌فرض اعمال می‌شود"],
                ["`gpt-4o-mini`, `gpt-4o-mini-transcribe`, `gpt-4o-mini-tts`", "`phoenix:golang/websocall/internal/config/config.go:54-56`", "websocall در EX آدرس‌های پایه را به iva-chatbot و neurobox بازنویسی می‌کند"],
                ["`gpt-4.1-mini`", "`phoenix:golang/grogu/internal/config/config.go:114` (ticket)", "grogu-iva در EX آن را تنظیم نمی‌کند"],
                ["`text-embedding-3-small`", "`phoenix:golang/synapse/internal/services/entity.go:51`", "synapse در aiva"],
            ]}),
            ("ریسک‌ها و پرسش‌های باز", [
                "بازگشت بی‌صدا به OpenAI یک ریسک اقامت داده است؛ در نظر بگیرید که با نبودن متغیر محیطی مدل، سرویس سریعاً خطا بدهد (fail fast).",
            ]),
        ],
    },
    "axonhub-aliases": {
        "title": "Aliasهای AxonHub: main-guardrail، gemma-4-26B-it-no-reasoning، Qwen3.8-27B",
        "title_plain": "Aliasهای AxonHub",
        "status": "unknown",
        "chip": "جدول مسیریابی در git نیست",
        "summary": "در یک پاراگراف: AxonHub دروازهٔ LLM پلتفرم است. سرویس‌ها می‌توانند یک نام منطقی مثل `main-guardrail` را از آن بخواهند و AxonHub تصمیم می‌گیرد کدام مدل و سرور واقعی پاسخ دهد. این کار انعطاف می‌دهد، چون ops می‌تواند مدل guardrail دوازده بات را یک‌جا عوض کند، اما نگاشت در پایگاه‌دادهٔ AxonHub ذخیره است و در git نیست؛ پس از روی مخزن‌ها هیچ‌کس نمی‌تواند بگوید این فراخوانی‌ها واقعاً توسط کدام مدل پاسخ داده می‌شوند.",
        "facts": [
            ("دروازه", "AxonHub `looplj/axonhub:v1.0.0-beta11`، 3 replica، پورت 8090، پایگاه‌داده `chatbot_llm_gateway` (`prod/chatbot-llm-gateway/values.yaml:1-5,16-25,47-55`)"),
            ("دروازهٔ دوم", "`chatbot-mcinext-llm-gateway`، پایگاه‌داده `mcinext_llm_gateway` (`prod/chatbot-mcinext-llm-gateway/values.yaml:2-5,17,51-52`)"),
            ("احراز هویت", "`AXONHUB_SERVER_API_AUTH_ALLOW_NO_AUTH=true`"),
        ],
        "sections": [
            ("Aliasهای در حال استفاده", {"table": [
                ["Alias", "کاربران", "مرجع", "مدل پشتیبان محتمل (استنباطی)"],
                ["`main-guardrail`", "arbaeen, bale, ewano, chatbot-mci, mci-agent-chat, english-iva-avatar (با غلط املایی `main-guardlrail`), mci-iva-avatar, mci-iva-load-test, mobinnet, rubika, mci-agentic, mci-navigator", "برای نمونه `prod/mci-agentic/values.yaml:386`؛ غلط املایی در `prod/chatbot-mci-english-iva-avatar/values.yaml:128`", "Gemma-3 12B پیش از آنکه `5ef9c30f6` نشانی‌ها را به AxonHub ببرد، مدل guardrail بود"],
                ["`google/gemma-4-26B-it-no-reasoning`", "فراخوانی ابزار در chatbot-mci-iva", "`prod/chatbot-mci-iva/values.yaml:662`", "Gemma-4 26B-A4B با thinking اجباراً خاموش"],
                ["`Qwen/Qwen3.8-27B`", "aqa chainlit", "`prod/aqa/values.yaml:60`", "یک مدل Qwen 27B که بیرون از این مخزن سرو می‌شود"],
                ["`google/gemma-4-26B-A4B-it`", "پیام بیکاری EX (غیرفعال)", "`prod/chatbot-ex/values.yaml:2496-2499`", "pool مدل 26B"],
            ]}),
            ("چرا استفاده می‌شود (استنباطی)", "یک نقطهٔ تغییر برای انتخاب مدل و کلیدها، به‌علاوهٔ حسابداری مصرف به تفکیک کانال."),
            ("ریسک‌ها و پرسش‌های باز", [
                "جدول کانال‌های AxonHub را export کنید و در git یا یک snapshot مستند نگه دارید.",
                "Alias با غلط املایی فقط وقتی کار می‌کند که AxonHub آن را هم تعریف کرده باشد.",
                "`synapse` در aiva به پورت 8080 اشاره می‌کند، اما AxonHub روی 8090 گوش می‌دهد (`prod/aiva/values.yaml:3136,3144`).",
            ]),
            ("چگونه مشاهده کنیم", [
                "رابط AxonHub در `chatbot-llm-gateway.pr.mci.dev` (مصرف به تفکیک مدل و کانال، استنباط‌شده از قابلیت‌های AxonHub).",
                "برچسب لاگ `chatbot-llm-gateway-prod.chatbot`.",
            ]),
        ],
    },
    "soniox-stt": {
        "title": "Soniox: گفتار به متن بی‌درنگ (بیرونی)",
        "title_plain": "Soniox STT",
        "status": "external",
        "chip": "STT زندهٔ EX از 2026-10-31",
        "summary": "در یک پاراگراف: Soniox یک سرویس تجاری ابری تشخیص گفتار است. در EX، عامل صوتی LiveKit صدای تماس‌گیرنده را به Soniox استریم می‌کند و رونوشت فارسی را به‌صورت بی‌درنگ پس می‌گیرد؛ همین متن است که مغز روی آن استدلال می‌کند. این سرویس در 2026-10-31 جای ASR داخلی neurobox را در EX گرفت؛ پس صدای تماس‌گیرنده از طریق relay خروجی از MCI بیرون می‌رود. نکتهٔ جالب: یکپارچه‌سازی Soniox روی main در phoenix نیست و روی یک feature branch قرار دارد.",
        "facts": [
            ("فروشنده", "Soniox، SaaS اختصاصی؛ اندازه عمومی نیست"),
            ("مدل", "EX: تنظیم نشده (پیش‌فرض plugin)؛ aiva-neda: `stt-rt-v5` (`prod/aiva-neda/values.yaml:2917-2920`)"),
            ("پیکربندی EX", "`AGENT_STT_CLIENT=soniox`، کلید `aiva/soniox_api_key`، پروکسی `envoy-relay-chatbot` (`prod/chatbot-ex/values.yaml:3117-3125`)"),
            ("کد", "پشتیبانی Soniox فقط روی branch با نام `origin/feat-soniox-lang` است (کامیت `08b4ecf18`، نسخهٔ v0.41.0)؛ main در phoenix هیچ کد Soniox در `chatbot-iva-agent` ندارد"),
        ],
        "sections": [
            ("چه کسی استفاده می‌کند", {"table": [
                ["سرویس", "مؤلفه", "مرجع"],
                ["chatbot-ex (EX)", "agent (LiveKit)", "`prod/chatbot-ex/values.yaml:3117-3125`"],
                ["aiva", "agent", "`prod/aiva/values.yaml:2129-2130`"],
                ["aiva-neda", "agent (`stt-rt-v5`)", "`prod/aiva-neda/values.yaml:2917-2920`"],
                ["aiva-realtime (کد)", "مدل پیش‌فرض `stt-rt-v5`", "`phoenix:python/aiva-realtime/aiva_realtime/config/realtime.py:64`"],
            ]}),
            ("چرا آن‌جا استفاده می‌شود", "کامیت `748eb9c57` (jinsakai، 2026-10-31) با عنوان “chore(chatbot-ex)” STT داخلی را با Soniox عوض کرد. پیش‌تر aiva با “change stt to soniox” (2026-09-27) به آن رفته بود، برگشته بود و در 2026-10-04 (“return soniox”) دوباره برگردانده شد. دلیل ذکر نشده است؛ احتمالاً دقت بهتر روی صدای پر‌نویز تلفن و استریم بومی (استنباطی). README آن branch می‌گوید Soniox با language hint به‌صورت `fa,en` تنظیم شده است."),
            ("مبادلات (Trade-offs)", [
                "رونوشت‌های جزئی استریمی تأخیر پایان نوبت را کم می‌کنند؛ رفت‌وبرگشت ابری تأخیر شبکه و یک وابستگی بیرونی سخت اضافه می‌کند.",
                "صورت‌حساب به‌ازای هر دقیقه در برابر هزینهٔ GPU داخلی.",
            ]),
            ("ریسک‌ها و پرسش‌های باز", [
                "**حریم خصوصی:** صدای کارکنان از MCI بیرون می‌رود. تأیید استفاده برای EX را بگیرید.",
                "**منشأ build:** ایمیج مستقرشدهٔ `chatbot-iva-agent:3524df3f` کدی دارد که روی main نیست؛ branch را merge یا مستند کنید.",
                "برای EX مدل ثابت نشده است: ارتقای plugin می‌تواند مدل را بی‌صدا عوض کند.",
            ]),
            ("چگونه مشاهده کنیم", [
                "متریک‌های Prometheus عامل LiveKit (تأخیر STT به تفکیک client) و Elastic APM (`AGENT_APM_*`).",
                "لاگ‌های relay خروجی.",
            ]),
        ],
    },
    "neurobox-asr": {
        "title": "Neurobox ASR (k2) با تشخیص احساس و جنسیت",
        "title_plain": "Neurobox ASR",
        "status": "live",
        "chip": "تحلیل آفلاین تماس EX",
        "summary": "در یک پاراگراف: تشخیص گفتار فارسی داخلی MCI که روی NVIDIA Triton سرو می‌شود و از طریق یک دروازهٔ به سبک OpenAI (`neurobox-gateway`) در دسترس است. پس از پایان تماس EX، سرویس grogu ضبط را به این‌جا می‌فرستد تا رونوشت هر گوینده را همراه با برچسب احساس و جنسیت بگیرد؛ این خروجی به تحلیل تماس می‌رود. سایر باتات IVA هم از آن برای STT زنده استفاده می‌کنند. خود مدل‌های ASR از یک namespace دیگر مستقر می‌شوند، پس اندازهٔ آن‌ها در این مخزن‌ها نیست.",
        "facts": [
            ("مدل (استنباطی)", "ASR از نوع k2 / Zipformer (از نام میزبان `asr-k2-…`)؛ طبقه‌بندهای احساس و جنسیت"),
            ("کد دروازه", "`phoenix:golang/neurobox-gateway`: مسیرهای `/audio/transcriptions`, `/audio/emotion`, `/audio/gender`, `/audio/speech` (`internal/server/upstreams.go:29-34`)"),
            ("Backendها", "`TRITON_ASR_URL`, `TRITON_EMOTION_URL`, `TRITON_GENDER_URL` (`config/config.go:311-317`)"),
            ("نام مسیرهای EX", "`coa_iva_prod_long` (grogu-iva)، `coa_mci_prod_long` (coa-api، syncerها)"),
        ],
        "sections": [
            ("چه کسی استفاده می‌کند", {"table": [
                ["سرویس", "مؤلفه", "نام مدل", "مرجع"],
                ["chatbot-ex (EX)", "grogu-iva", "`coa_iva_prod_long`, `ASR_EMOTION=true`, `ASR_GENDER=true`", "`prod/chatbot-ex/values.yaml:3377-3388`"],
                ["chatbot-ex (EX)", "coa-api + 5 syncer", "`coa_mci_prod_long` از طریق `ARS_OPENAI_BASE_URL` (sic)", "`:2777-2780`, `:3726-3728`"],
                ["chatbot-mci-iva", "agent (STT زنده)", "`iva_prod_vad` از طریق `local-stt-prod`", "`prod/chatbot-mci-iva/values.yaml:1107-1110`"],
                ["aiva-poll, front-iva, rubika-iva, mobinnet-iva, shaad-iva", "agent (STT زنده)", "`*_prod_vad`", "برای نمونه `prod/aiva-poll/values.yaml:1734`"],
                ["mci-agentic", "grogu, grogu-iva, grogu-ticket, coa-api", "`coa_mci_prod_long`, `coa_iva_prod_long`, `coa_prod_long`", "`prod/mci-agentic/values.yaml:3591,3864,4139`"],
            ]}),
            ("چرا آن‌جا استفاده می‌شود (استنباطی)", "رونویسی دسته‌ای ضبط‌های کامل در حجم بالا در داخل ارزان‌تر است، صدا را درون MCI نگه می‌دارد و برچسب‌های احساس/جنسیت را اضافه می‌کند که STT ابری ندارد. پسوند `_long` پیش از voice segmenter حذف می‌شود (`phoenix:golang/neurobox-gateway/internal/services/voicesegmenter.go:119,328-329`)، که صدای استریو را پیش از ASR با Silero VAD تکه‌تکه می‌کند."),
            ("مبادلات (Trade-offs)", [
                "نام مدل‌های `_vad` یعنی بخش‌بندی VAD سمت سرور (استنباطی).",
                "کیفیت تحلیل به دقت ASR وابسته است که در این مخزن‌ها اندازه‌گیری نشده است.",
            ]),
            ("ریسک‌ها و پرسش‌های باز", [
                "نسخه‌ها و اندازهٔ مدل‌ها در اختیار تیم neurobox است؛ WER روی صدای مشابه EX را از آن‌ها بخواهید.",
                "STT زندهٔ EX (Soniox) و ASR آفلاین EX (k2) متفاوت‌اند: رونوشت زنده و رونوشت تحلیل برای یک تماس کلمه‌به‌کلمه یکسان نخواهند بود.",
            ]),
            ("چگونه مشاهده کنیم", [
                "Elastic APM دروازه (نمونه‌برداری 0.1)؛ circuit breaker در grogu با `ASR_CONSECUTIVE_FAILURES_CB=12` (`:3383-3384`).",
            ]),
        ],
    },
    "neurobox-tts": {
        "title": "Neurobox TTS (صدای ex_prod) و tts-service از نوع VITS",
        "title_plain": "Neurobox TTS / VITS",
        "status": "live",
        "chip": "همهٔ پاسخ‌های EX را می‌گوید",
        "summary": "در یک پاراگراف: هر جمله‌ای که تماس‌گیرنده EX می‌شنود، توسط تبدیل متن به گفتار فارسی داخلی MCI روی Triton و از طریق همان دروازهٔ neurobox سنتز می‌شود. هر محصول نام صدای خودش را دارد: EX برای تماس زنده از `ex_prod` و برای اعلان‌ها از `coa-ex-prod` استفاده می‌کند. یک سرویس VITS کوچک روی CPU هم جداگانه در کلاستر هست. مدل‌های TTS بیرون از chatbot-ops مستقر می‌شوند، پس اندازهٔ آن‌ها این‌جا نامعلوم است.",
        "facts": [
            ("صدای زندهٔ EX", "`AGENT_TTS_MODEL=ex_prod`، سرعت 1.1، از طریق `neurobox-gateway-green` (`prod/chatbot-ex/values.yaml:3130-3135`)"),
            ("اعلان‌های EX", "`TTS_MODEL=coa-ex-prod` از طریق `neurobox-gateway.pr.mci.dev` (`:2676-2679`)"),
            ("پیش‌فرض‌های دروازه", "نرخ نمونه‌برداری 22,050 Hz، سرعت 0.77 (`phoenix:golang/neurobox-gateway/config/config.go:33-34`)"),
            ("tts-service از نوع VITS", "`MODEL_PATH=/app/vits`، `NUM_THREADS=2`، روی CPU، 1 replica (`prod/tts-service/values.yaml:2-6,39-42`)"),
            ("اندازه (واقعیت)", "مدل‌های VITS معمولاً حدود 30 تا 40M پارامتر دارند؛ اندازهٔ صداهای neurobox نامعلوم است"),
        ],
        "sections": [
            ("چه کسی استفاده می‌کند", {"table": [
                ["سرویس", "مؤلفه", "صدا", "مرجع"],
                ["chatbot-ex (EX)", "agent", "`ex_prod`", "`prod/chatbot-ex/values.yaml:3134-3135`"],
                ["chatbot-ex (EX)", "coa-api", "`coa-ex-prod`", "`:2678-2679`"],
                ["chatbot-ex (EX)", "chatbot, iva-chatbot", "جایگزین `tts_model`", "`:405-406`, `:2457-2458`"],
                ["aiva / aiva-poll / mci-iva", "agent", "`aiva_prod`, `aiva_poll_prod`, `iva_prod`", "`prod/aiva/values.yaml:2149`, `prod/aiva-poll/values.yaml:1748`, `prod/chatbot-mci-iva/values.yaml:1106`"],
            ]}),
            ("چرا آن‌جا استفاده می‌شود (استنباطی)", "کیفیت صدای فارسی و صدای اختصاصی برای هر برند، بدون صورت‌حساب ابری به‌ازای هر نویسه. EX در 2026-10-28 از `tts_model` به `ex_prod` رفت (`4fb71cce4` “change asr tts model”). وجود دروازهٔ green نشان می‌دهد برای TTS استقرار blue/green انجام می‌شود."),
            ("مبادلات (Trade-offs)", [
                "تأخیر TTS مستقیماً به زمان رسیدن اولین صدا اضافه می‌شود؛ استریم جمله‌به‌جمله بخشی از آن را پنهان می‌کند.",
                "اعداد و مخفف‌های فارسی به قواعد سمت prompt نیاز دارند (در promptهای aiva-poll دیده می‌شود) یا به مرحلهٔ اعرابگذاری در coa-api (Gemma-4 31B).",
            ]),
            ("ریسک‌ها و پرسش‌های باز", [
                "کدام backend صدای `ex_prod` را سرو می‌کند و آیا green با blue یکی است؟",
                "چه کسی `tts-service` از نوع VITS را صدا می‌زند؟ در پیکربندی EX پیدا نشد.",
            ]),
            ("چگونه مشاهده کنیم", [
                "Elastic APM دروازه؛ متریک‌های زمان‌بندی TTS در عامل LiveKit.",
            ]),
        ],
    },
    "silero-vad": {
        "title": "Silero VAD (تشخیص فعالیت صوتی)",
        "title_plain": "Silero VAD",
        "status": "live",
        "chip": "در هر worker تماس",
        "summary": "در یک پاراگراف: Silero VAD یک شبکهٔ عصبی متن‌باز بسیار کوچک است که هر چند میلی‌ثانیه می‌گوید آیا صدا شامل گفتار هست یا نه. در EX درون هر worker تماس LiveKit اجرا می‌شود و تعیین می‌کند عامل کی گوش دادن را شروع کند، کی سکوت یک نوبت را تمام کند و کی تماس‌گیرنده وسط حرف عامل بپرد (barge-in). آنقدر کوچک است که روی CPU و بدون سرویس مستقل اجرا می‌شود. آستانه‌های آن تنظیمات محصولی EX هستند که شناختنشان ارزش دارد.",
        "facts": [
            ("مدل (واقعیت)", "Silero VAD (دورهٔ v5)، متن‌باز (MIT)، حدود 1 تا 2 مگابایت ONNX؛ بسیار کمتر از 0.01B پارامتر"),
            ("کتابخانه", "`livekit-plugins-silero==1.2.8` (`phoenix:python/chatbot-iva-agent/requirements.txt:69`)"),
            ("بارگذاری", "`silero.VAD.load(...)` در prewarm (`phoenix:python/chatbot-iva-agent/src/main.py:89-94`)"),
            ("آستانه‌های EX", "activation برابر 0.3، حداقل سکوت 0.5 ثانیه، حداقل گفتار 0.2 ثانیه، prefix padding برابر 0.5 ثانیه (`prod/chatbot-ex/values.yaml:3099-3112`)"),
        ],
        "sections": [
            ("کجاهای دیگر", [
                "سرویس‌های Silero راه‌دور (HTTP/gRPC) برای `aiva-realtime` (`phoenix:python/aiva-realtime/aiva_realtime/config/realtime.py:157`) و برای voice segmenter که ASR آفلاین استفاده می‌کند (`phoenix:golang/voice-segmenter/config/config.go:31`).",
                "Silero در مرورگر (`silero_vad_v5.onnx`) در رابط کاربری websocall (`phoenix:javascript/websocall-ui/app/scripts/copy-vad-assets.mjs:25`).",
            ]),
            ("چرا آن‌جا استفاده می‌شود", "انتخاب استاندارد در LiveKit؛ برای هر فریم سریع است و در برابر نویز از VAD مبتنی بر انرژی مقاوم‌تر است."),
            ("مبادلات (Trade-offs)", [
                "آستانهٔ activation پایین (0.3) گفتار آهسته را می‌گیرد اما نویز بیشتری هم می‌گیرد؛ حداقل وقفه 0.4 ثانیه (`:3113-3114`) از barge-in محافظت می‌کند.",
                "تأخیرهای endpointing بین 0.1 تا 0.5 ثانیه (`:3101-3104`) پاسخ‌گویی را با خطر قطع‌کردن حرف تماس‌گیرنده معامله می‌کنند.",
            ]),
            ("چگونه مشاهده کنیم", [
                "Spanهای APM عامل برای هر نوبت؛ turn-detection exporter (`prod/turn-detection-exporter/exporter.yaml:26-29`).",
            ]),
        ],
    },
}
