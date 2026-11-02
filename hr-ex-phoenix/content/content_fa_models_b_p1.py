"""Persian model pages, part 1 (qwen-moe .. legacy-encoders). Mirrors content_en_models.py."""

PAGES1 = {
    "qwen-moe": {
        "title": "خانوادهٔ Qwen MoE: Qwen3.5-35B-A3B، Qwen3.6-35B-A3B، Qwen3-30B-A3B",
        "title_plain": "Qwen 35B-A3B / 30B-A3B",
        "status": "off",
        "chip": "0 replica، در حال ارزیابی",
        "summary": "در یک پاراگراف برای TPM: سه مدل mixture-of-experts از Qwen بسته‌بندی و آماده‌اند، اما خاموش هستند. هر سه Deployment در Kubernetes روی صفر replica است و هیچ سرویسی در git آن‌ها را صدا نمی‌زند. چون فقط حدود 3B پارامتر فعال دارند، سریع‌ترین مدل‌های بزرگ این پلتفرم‌اند و برای مراحل حساس به تأخیر گزینهٔ طبیعی‌اند. load balancerهای آن‌ها هنوز به چند پردازهٔ bare-metal اشاره می‌کنند، پس شاید کسی دستی آن‌ها را آزمایش می‌کند.",
        "facts": [
            ("مدل‌ها (واقعیت)", "Alibaba Qwen، مجوز Apache-2.0؛ نسخه‌های 3.5 و 3.6 ذاتاً بینایی-زبانی‌اند و 3-30B-2507 فقط متنی است"),
            ("اندازه‌ها (واقعیت)", "35B کل / حدود 3B فعال (3.5 و 3.6)؛ 30.5B / حدود 3.3B (3-30B)"),
            ("زمینهٔ بومی (واقعیت)", "حدود 256K"),
            ("سقف در اینجا", "15,000 برای هر سه"),
            ("موتورها", "vLLM 0.17.0 / 0.19.1 / 0.15.1"),
            ("Replicaها", "0 / 0 / 0 (هر کدام 3 LB)"),
        ],
        "sections": [
            ("نحوهٔ سرو در این‌جا", {"table": [
                ["Deployment", "نام سرو‌شده", "پرچم‌ها", "upstreamهای LB", "مرجع"],
                ["qwen3.5-35b-a3b", "`Qwen/Qwen3.5-35B-A3B`", "`--enable-auto-tool-choice`, `--tool-call-parser qwen3_coder`, `--language-model-only`؛ ثابت‌شده روی میزبان‌های kp1-ga1/kp1-ga8", "headless + `172.23.0.4:8330`", "`prod/qwen3.5-35b-a3b/values.yaml:2,5,64-73,85-97,344-350`"],
                ["qwen3.6-35b-a3b", "`Qwen/Qwen3.6-35B-A3B`", "مانند بالا", "headless + `172.23.0.17:8123`", "`prod/qwen3.6-35b-a3b/values.yaml:5,87,93,344-350`"],
                ["qwen3-30b-a3b", "`Qwen/Qwen3-30B-A3B-Instruct-2507`", "`--tool-call-parser hermes`", "فقط headless", "`prod/qwen3-30b-a3b/values.yaml:5,93-96,151`"],
            ]}),
            ("چه کسی استفاده می‌کند", "هیچ‌کس در git. `qwen3-5-35b-a3b-lb` فقط در یک خط کامنت‌شده در `chatbot-mobinnet` دیده می‌شود. مدل `Qwen/Qwen3.8-27B` در AQA مدل دیگری است که از طریق AxonHub صدا زده می‌شود؛ ببینید [AxonHub aliases](axonhub-aliases.html)."),
            ("چرا وجود دارند (استنباطی)", "کاندیداهای مقایسه با Gemma-4 26B-A4B برای مراحل حساس به سرعت. گزینهٔ `--language-model-only` بخش بینایی را حذف می‌کند تا حافظهٔ GPU صرفه‌جویی شود."),
            ("مبادلات (Trade-offs)", [
                "حدود 3B پارامتر فعال، سریع‌ترین decode را در بین مدل‌های بزرگ این‌جا می‌دهد؛ کیفیت فارسی در مقایسه با Gemma-4 در git اثبات نشده است.",
            ]),
            ("ریسک‌ها و پرسش‌های باز", [
                "Exporter برای Qwen3.5 آدرس `172.16.21.4:8335` را scrape می‌کند، اما LB از `172.23.0.4:8330` استفاده می‌کند.",
                "تصمیم لازم است: حذف، یا اجرای یک ارزیابی مستند.",
            ]),
            ("چگونه مشاهده کنیم", [
                "`vllm-qwen3-5-gpu-exporter`؛ آمار Envoy روی سه LB مربوط به Qwen.",
            ]),
        ],
    },
    "llama-3-trtllm": {
        "title": "Llama-3 روی TensorRT-LLM (openai-trtllm، قدیمی)",
        "title_plain": "Llama-3 TRT-LLM",
        "status": "live",
        "chip": "یک مصرف‌کنندهٔ قدیمی",
        "summary": "در یک پاراگراف برای TPM: یک راه‌اندازی اولیهٔ LLM درون‌سازمانی. یک مدل از خانوادهٔ Llama-3 روی NVIDIA Triton با TensorRT-LLM در یک میزبان bare-metal اجرا می‌شود و یک سرویس واسط کوچک درخواست‌های به سبک OpenAI را به فراخوانی Triton تبدیل می‌کند. فقط یک بات، یعنی `chatbot-tejarat-local`، هنوز آن را صدا می‌زند. اندازهٔ دقیق مدل در git نیست.",
        "facts": [
            ("مدل (استنباطی)", "خانوادهٔ Llama-3: قالب history در wrapper همان قالب چت Llama-3 است"),
            ("اندازه", "نامشخص (Llama-3 در دو نسخهٔ 8B و 70B عرضه می‌شود)"),
            ("زمینهٔ بومی (واقعیت)", "8K (Llama-3) یا 128K (Llama-3.1 به بعد)"),
            ("موتور", "Triton TensorRT-LLM در `http://172.22.1.6:8001`"),
            ("Wrapper", "`mci/sre/openai_trtllm:1.0`، 3 replica، `openai-trtllm-api:3000` (`prod/openai-trtllm/values.yaml:2-6,27-41`)"),
        ],
        "sections": [
            ("چه کسی استفاده می‌کند", "`chatbot-tejarat-local` (`prod/chatbot-tejarat-local/values.yaml:100`). در EX استفاده نمی‌شود."),
            ("چرا آن‌جا استفاده می‌شود (استنباطی)", "نسخهٔ «محلی» بات بانک تجارت؛ احتمالاً برای نگه داشتن داده‌ها درون سازمان، پیش از آنکه poolهای vLLM وجود داشته باشند."),
            ("مبادلات (Trade-offs)", [
                "TensorRT-LLM توان عملیاتی بالایی دارد، اما هر مدل به یک engine کامپایل‌شده نیاز دارد؛ تعویض مدل در مقایسه با vLLM کند است.",
            ]),
            ("ریسک‌ها و پرسش‌های باز", [
                "آیا tejarat-local هنوز فعال است؟ اگر نه، نقش LLM میزبان 172.22.1.6 باید بازنشسته شود.",
                "برای توکن‌های TRT-LLM exporter وجود ندارد (فقط `prod/embedding-exporter/22.1.6.yaml` یک پورت embedding را روی آن میزبان scrape می‌کند).",
            ]),
            ("چگونه مشاهده کنیم", [
                "لاگ‌های pod مربوط به wrapper؛ هیچ سری Prometheus در git نیست.",
            ]),
        ],
    },
    "hakim-embedding": {
        "title": "Hakim embedding روی Triton (CPU + GPU)",
        "title_plain": "Hakim (Triton)",
        "status": "live",
        "chip": "پرمصرف‌ترین endpoint: 26 سرویس",
        "summary": "در یک پاراگراف برای TPM: Hakim مدل embedding متن فارسی ساختهٔ خود MCINext است؛ یک جمله را به بردار تبدیل می‌کند تا پرسش‌های مشابه در پایگاه برداری پیدا شوند. این استقرار Triton پرارجاع‌ترین endpoint مدل در پلتفرم است (26 سرویس). در EX بازیابی چت‌بات متنی را سرو می‌کند؛ مسیر صوتی EX از مدل هم‌خانواده‌ای به نام [hakim-unsup](hakim-unsup.html) استفاده می‌کند. هم روی podهای CPU و هم GPU اجرا می‌شود و مصرف‌کننده‌ها از طریق یک پروکسی Envoy که جلوی podهای GPU است می‌آیند.",
        "facts": [
            ("مدل (استنباطی)", "Hakim، یک encoder فارسی از نوع BERT از MCINext؛ حدود 0.1 تا 0.2B پارامتر، ورودی 512 توکنی (تأییدنشده)"),
            ("موتور", "Triton `mci/tritonserver/torch:25.08-v1.0`، مدل Python (`prod/hakim-embedding-serve/values.yaml:1-11`)"),
            ("وزن‌ها", "`chatbot-data-prod/new_embeddings/embedding`"),
            ("Podها", "CPU 1 (`MODEL_DEVICE=cpu`، 12 CPU / 25Gi، `:47-57,76-84`)؛ GPU 2 (`:93-108,180-200`)"),
            ("پروکسی", "`hakim-embedding-serve-proxy:1080` → GPU headless (`:236-241,505-514`)"),
        ],
        "sections": [
            ("چه کسی استفاده می‌کند", (
                {"table": [
                    ["سرویس", "مؤلفه", "متغیر محیطی", "مرجع"],
                    ["chatbot-ex (EX)", "chatbot (متنی)", "`EMBEDDING_BASE_URL`", "`prod/chatbot-ex/values.yaml:135-136`"],
                    ["chatbot-ex (EX)", "kb / kb_worker (0 replica)", "`EMBEDDING_BASE_URL`", "`:762-763`, `:859-860`"],
                    ["حدود 24 سرویس دیگر", "خانوادهٔ aiva، باتات MCI، باتات IVA", "`EMBEDDING_BASE_URL` / `HAKIM_EMBEDDING_BASE_URL`", "اسکن پلتفرم"],
                ]},
            )),
            ("چرا آن‌جا استفاده می‌شود (استنباطی)", "embedderهای چندزبانهٔ متن‌باز در فارسی ضعیف‌ترند؛ مدل داخلی که روی داده‌های فارسی آموزش دیده، بازیابی بهتری می‌دهد و حتی روی CPU هزینهٔ اجرای کمی دارد."),
            ("مبادلات (Trade-offs)", [
                "مدل کوچک است: ارزان و سریع، اما پنجرهٔ ورودی کوتاهی دارد (معمولاً 512 توکن)، پس ورودی‌های KB باید chunk شوند.",
                "دو خانوادهٔ embedding (Hakim-Triton برای متن EX و hakim-unsup برای صوت EX) بردارهای ناسازگار تولید می‌کنند: دو collection مربوط به EX را نمی‌توان با پرسش‌های یکدیگر جست‌وجو کرد.",
            ]),
            ("ریسک‌ها و پرسش‌های باز", [
                "پایپ‌لاین متنی EX که `chatbot-ex-contexts` را پر می‌کرد (kb و kb_worker) روی 0 replica است: چت‌بات متنی ممکن است در یک collection منجمد جست‌وجو کند.",
                "Exporter: فایل `triton-hakim-embedding.yaml` آدرس bare-metal با نشانی `172.16.21.4:9014` را scrape می‌کند که upstream پروکسی نیست.",
            ]),
            ("چگونه مشاهده کنیم", [
                "متریک‌های Triton روی پورت 8002 podهای GPU (`nv_inference_request_success`، `nv_inference_compute_infer_duration_us`).",
                "آمار پروکسی Envoy.",
            ]),
        ],
    },
    "hakim-unsup": {
        "title": "hakim-unsup (Hakim بدون نظارت، vLLM pooling)",
        "title_plain": "hakim-unsup",
        "status": "live",
        "chip": "بازیابی صوتی EX",
        "summary": "در یک پاراگراف برای TPM: hakim-unsup گونه‌ای از مدل embedding فارسی Hakim است که vLLM آن را در حالت «pooling» سرو می‌کند؛ یعنی به‌جای متن، بردار برمی‌گرداند. مغز صوتی EX برای هر آیتم دانش دو بار از آن استفاده می‌کند: یک بار هنگام همگام‌سازی پایگاه دانش با vector store و یک بار برای هر گفتهٔ تماس‌گیرنده در زمان پاسخ. چون هر دو طرف باید از یک مدل استفاده کنند، تغییر آن یعنی embedding دوبارهٔ تمام آیتم‌های دانش EX.",
        "facts": [
            ("مدل (استنباطی)", "encoder از خانوادهٔ Hakim، گونهٔ آموزش‌دیدهٔ بدون نظارت؛ اندازه تأییدنشده (حدود 0.1 تا 0.2B)"),
            ("نام سرو‌شده", "`hakim-unsup`"),
            ("موتور", "vLLM `v0.25.1` با `--runner pooling` (ایمیج CPU به نام `vllm-openai-cpu`) (`prod/hakim-unsupervised/values.yaml:1-6,72-83`)"),
            ("max-model-len", "512؛ پردازش chunk‌شدهٔ pooler تا 32,768 توکن (`:72-83`)"),
            ("Podها", "CPU 2 (gpu-mem 0.5)، GPU 1 (gpu-mem 0.9، `:105-110,197-207`)"),
            ("پروکسی", "`hakim-unsupervised-vllm-proxy:1080/v1` → GPU headless + `172.23.0.17:5113` (`:228-233,505-511,534-556`)"),
        ],
        "sections": [
            ("چه کسی استفاده می‌کند", (
                {"table": [
                    ["سرویس", "مؤلفه", "نقش", "مرجع"],
                    ["chatbot-ex (EX)", "iva-chatbot", "embed کردن هر گفته برای جست‌وجو", "`prod/chatbot-ex/values.yaml:1316-1317`, `:2472-2473`"],
                    ["chatbot-ex (EX)", "iva_kb", "embed کردن آیتم‌های KB هنگام sync", "`:973-976`"],
                    ["aiva, aiva-neda, aiva-poll", "api, kb, kb_worker, synapse", "مشابه بالا", "`prod/aiva/values.yaml:85,2920,3132`"],
                ]},
                "مراحل EX: [embed](../steps/k-embed.html)، [sync](../steps/k-sync.html)، [search](../steps/k-search.html). افزوده‌شده در 2026-09-02 (`9fc1042f5`)؛ iva_kb در EX از 2026-10-31 روی آن است (`8ef60ae49`).",
            )),
            ("چرا آن‌جا استفاده می‌شود (استنباطی)", "vLLM یک API سازگار با OpenAI به نام `/v1/embeddings`، batching و یک ایمیج واحد برای CPU و GPU می‌دهد. پیش‌فرض کد، مدل `text-embedding-3-large` از OpenAI است (`phoenix:python/aiva/aiva/chat/config.py:49`)، پس این انتخاب متن کارکنان را درون سازمان نگه می‌دارد."),
            ("مبادلات (Trade-offs)", [
                "پنجرهٔ 512 توکنی: پاسخ‌های بلند KB توسط pooler chunk می‌شوند و بردار نهایی میانگین chunkها است (استنباطی).",
                "آستانهٔ جست‌وجوی `CONTEXT_RETRIEVE_THRESHOLD=0.25` (`:2488-2489`) برای همین مدل تنظیم شده است؛ با تعویض مدل باید دوباره تنظیم شود.",
            ]),
            ("ریسک‌ها و پرسش‌های باز", [
                "یک گونهٔ `coa-proxy` وجود دارد (`:811-817`) که در git مصرف‌کننده ندارد.",
                "Upstream از نوع bare-metal یعنی `172.23.0.17:5113` روی همان میزبان پرترافیکی است که 31B اختصاصی EX را دارد.",
            ]),
            ("چگونه مشاهده کنیم", [
                "متریک‌های pooling در vLLM روی podها (`vllm:e2e_request_latency_seconds`).",
                "آمار پروکسی Envoy.",
            ]),
        ],
    },
    "hakim-search": {
        "title": "hakim-search",
        "title_plain": "hakim-search",
        "status": "unknown",
        "chip": "در حال اجرا، بدون مصرف‌کننده در git",
        "summary": "در یک پاراگراف برای TPM: گونهٔ سوم Hakim که ظاهراً برای جست‌وجو تنظیم شده، روی دو pod با GPU و یک پردازهٔ bare-metal پشت یک load balancer عمومی مخصوص خودش اجرا می‌شود. هیچ سرویسی در git آن را صدا نمی‌زند. شاید یک محصول جست‌وجو بیرون از این مخزن‌ها از آن استفاده می‌کند یا یک آزمایش است.",
        "facts": [
            ("موتور", "vLLM `v0.15.0`، gpu-mem 0.90 (`prod/hakim-search/values.yaml:1-6,90-95`)"),
            ("وزن‌ها", "`chatbot-data-prod/hakim_search` → سرو‌شده با نام `hakim-search` (`:116-119`)"),
            ("Replicaها", "2 + Envoy LB ×3 (`:122-151`)"),
            ("LB", "`chatbot-hakim-search-lb.pr.mci.dev` → headless + `172.23.0.17:8120` (`:343-349`)"),
        ],
        "sections": [
            ("چه کسی استفاده می‌کند", "ارجاعی در chatbot-ops یا phoenix نیست. از تیم پلتفرم بپرسید؛ نام میزبان عمومی نشان می‌دهد یک فراخواننده از بیرون وجود دارد (استنباطی)."),
            ("چرا وجود دارد (استنباطی)", "یک embedding (یا reranker) تخصصی برای بازیابی، برای آزمایش در برابر hakim-unsup."),
            ("ریسک‌ها و پرسش‌های باز", [
                "هزینهٔ GPU بدون مالک مشخص.",
                "vLLM 0.15.0 قدیمی است.",
            ]),
            ("چگونه مشاهده کنیم", [
                "`vllm-hakim-search-exporter` آدرس `172.23.0.17:8120` را scrape می‌کند؛ ServiceMonitor مربوط به pod.",
            ]),
        ],
    },
    "gemma-embedding": {
        "title": "Gemma embedding (gemma-embedding-lb)",
        "title_plain": "Gemma embedding",
        "status": "unknown",
        "chip": "فقط LB، بدون مصرف‌کننده",
        "summary": "در یک پاراگراف برای TPM: یک load balancer با نام «gemma embedding» جلوی دو پردازهٔ bare-metal قرار دارد. نام آن به EmbeddingGemma از Google اشاره می‌کند، یک مدل embedding چندزبانهٔ کوچک که احتمالاً برای مقایسه با Hakim آزمایش می‌شود. هیچ چیزی در git آن را صدا نمی‌زند.",
        "facts": [
            ("مدل (استنباطی)", "EmbeddingGemma: حدود 308M پارامتر، بردار 768 بعدی، ورودی حدود 2K توکن (مشخصات مدل، اگر حدس درست باشد)"),
            ("LB", "`gemma-embedding-vllm-proxy.pr.mci.dev` (`prod/gemma-embedding-lb/values.yaml:1-6,20-24`)"),
            ("Upstreamها", "`172.23.0.17:4001`, `172.23.0.17:4002` (`:278-284`)"),
        ],
        "sections": [
            ("تاریخچه", "افزوده‌شده در 2026-09-05 (`b9bbf6d88` “Add gemma embedding lb”)."),
            ("ریسک‌ها و پرسش‌های باز", [
                "کدام مدل و با کدام پرچم‌ها؟ در git نیست.",
                "هدف exporter وجود ندارد.",
            ]),
        ],
    },
    "legacy-encoders": {
        "title": "Encoderهای قدیمی: embedding سفارشی MCI و zibert_v2",
        "title_plain": "Embedding سفارشی MCI / zibert_v2",
        "status": "live",
        "chip": "باتات نسل اول",
        "summary": "در یک پاراگراف برای TPM: پیش از Hakim، باتات MCI از یک مدل embedding فاین‌تیون‌شده روی Triton (`custom-embedding`) و یک مدل برداری محلی کوچک به نام `zibert_v2` استفاده می‌کردند که درون کانتینر خود بات بارگذاری می‌شود. هر دو هنوز برای باتات قدیمی‌تر (قوهٔ قضائیه، انقلاب، بازخورد، خدمت) اجرا می‌شوند. EX از آن‌ها استفاده نمی‌کند.",
        "facts": [
            ("embedding سفارشی MCI", "Triton `nvidia/tritonserver:24.12-trtllm-python-py3`، backend پایتون، max_batch_size 4، 2 replica، میزبان `chatbot-embedding.pr.mci.dev`؛ وزن‌ها `chatbot-datachunk-prod/models/fine_tuned_mci_data` (`prod/chatbot-custom-embedding/values.yaml:1-12,56-60,83`)"),
            ("zibert_v2", "`VECTOR_MODEL_PATH=/app/resources/zibert_v2` در judiciary و revolution (`prod/chatbot-judiciary/values.yaml:106`)؛ `/app/zibert_v2` در feedback (`prod/chatbot-feedback-service/values.yaml:56`)؛ یک اپ Ray Serve به نام `/zibert` (`prod/chatbot-ray/serve-cluster.yaml:29-32`)"),
            ("اندازه", "نامشخص؛ zibert احتمالاً هم‌اندازهٔ BERT-base است (حدود 0.1B) (استنباطی)"),
        ],
        "sections": [
            ("چرا باقی مانده‌اند (استنباطی)", "embedding دوبارهٔ collectionهای باتات قدیمی‌تر زحمت دارد و سود محصولی کمی دارد."),
            ("ریسک‌ها و پرسش‌های باز", [
                "ایمیج Triton قدیمی است؛ `prod/embedding-exporter/22.1.6.yaml` یک نسخهٔ bare-metal در `172.22.1.6:8014` را scrape می‌کند که با برچسب custom-mci-embedding مشخص شده است.",
                "مدل‌های درون‌پردازه با replicaهای بات مقیاس می‌گیرند و از CPU بات مصرف می‌کنند.",
            ]),
        ],
    },
}
