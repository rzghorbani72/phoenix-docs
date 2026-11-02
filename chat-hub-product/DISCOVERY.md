# Product Discovery — LLM Hub سازمانی
_Last updated: 2026-10-27_

> ورودی‌ها: وایت‌برد «LLM Hub Features»، [founder/product-brief.md](../founder/product-brief.md)، کد فعلی این ریپو، تحقیق رقبا (منابع پایین صفحه).
> **هشدار شواهد:** تا امروز **۰ مصاحبه‌ی کاربر** انجام شده. هر چیزی در این سند که با «فرض» علامت خورده، نظر ذی‌نفعان است نه شواهد. بخش ۶ برنامه‌ی جمع‌کردن شواهد است.

---

## ۱. Outcome (نه راه‌حل)

| Outcome | شاخص | Baseline | هدف ۹۰ روزه بعد از GA |
|---|---|---|---|
| کارمندان از ابزار داخلی استفاده کنند، نه اکانت شخصی | WAU / کل کارمندان هدف | نامعلوم — اندازه بگیرید | ۴۰٪ |
| ترافیک Shadow AI کم شود | ترافیک پروکسی به chatgpt.com, claude.ai, gemini | نامعلوم — قبل از لانچ بگیرید | −۵۰٪ |
| هزینه‌ی AI قابل‌پیش‌بینی و قابل‌تخصیص باشد | ٪ هزینه که به یک کاربر/واحد نسبت داده شده | ۰٪ | ۱۰۰٪ |
| دید امنیتی روی داده‌ی خروجی | ٪ درخواست‌ها با trace + برچسب guardrail | ۰٪ | ۱۰۰٪ |
| توسعه‌دهنده‌ها از کلید سازمانی در IDE استفاده کنند | dev فعال هفتگی با API key | ۰ | ۶۰٪ dev‌ها |

## ۲. سگمنت‌ها و Job-to-be-Done

| سگمنت | JTBD (فرض) | درد فعلی (فرض) |
|---|---|---|
| **کارمند عمومی** (حقوقی، مالی، فروش، HR) | «وقتی متن/سند دارم، می‌خواهم سریع خلاصه/بازنویسی/تحلیل کنم» | VPN + اکانت شخصی، محدودیت رایگان، نگرانی امنیتی |
| **توسعه‌دهنده** | «وقتی در VS Code کد می‌زنم، می‌خواهم بهترین مدل کد در ابزار خودم کار کند» | پرداخت شخصی Cursor/Copilot، کلید شخصی، تحریم پرداخت |
| **مدیر واحد / صاحب بودجه** | «می‌خواهم بدانم تیمم چقدر خرج می‌کند و سقف بگذارم» | هیچ دیدی ندارد |
| **امنیت / CISO** | «می‌خواهم بدانم چه داده‌ای بیرون می‌رود و جلوی موارد حساس را بگیرم» | Shadow AI کاملاً کور است |
| **ادمین پلتفرم / IT** | «می‌خواهم کاربر، مدل، سهمیه و policy را بدون کد مدیریت کنم» | — |

## ۳. Opportunity Solution Tree

```
OUTCOME: ۴۰٪ WAU و −۵۰٪ Shadow AI
│
├─ O1: کیفیت باید هم‌سطح ChatGPT/Claude شخصی باشد
│    ├─ دسترسی به مدل‌های تاپ (چند ارائه‌دهنده)       ← وایت‌برد: Provider
│    ├─ انتخاب مدل مثل Cursor + حالت Auto              ← وایت‌برد: Model Selection
│    └─ فایل/تصویر/صوت در چت                          ← وایت‌برد: File process / storage
│
├─ O2: کاربر باید بداند چقدر سهمیه دارد (اعتماد)
│    ├─ صفحه‌ی Usage در پروفایل (مثل Cursor/OpenRouter) ← وایت‌برد: Usage, Home stats
│    └─ هشدار ۸۰٪ / ۱۰۰٪ سهمیه
│
├─ O3: توسعه‌دهنده باید در ابزار خودش کار کند
│    ├─ API key سلف‌سرویس OpenAI-compatible            ← وایت‌برد: OpenAI API (incl. Files)
│    └─ راهنمای Continue / Cline / Roo Code
│
├─ O4: مدیر باید کنترل هزینه داشته باشد
│    ├─ بودجه per-user / per-واحد / per-دوره          ← وایت‌برد: Accounting
│    └─ RBAC + داشبورد
│
└─ O5: امنیت باید دید و کنترل داشته باشد
     ├─ Trace با search/filter و TTFT                   ← وایت‌برد: Trace
     ├─ Guardrail محلی، چندرسانه‌ای، prompt قابل‌ویرایش  ← وایت‌برد: GuardRail
     └─ مدیریت سشن‌ها
```

**نکته‌ی coaching:** همه‌ی آیتم‌های وایت‌برد به یک Opportunity وصل شدند، ولی O1 و O2 مستقیماً Outcome اصلی (پذیرش) را حرکت می‌دهند و O4/O5 فقط **بعد از پذیرش** ارزش دارند. ترتیب roadmap از همین می‌آید.

## ۴. تحلیل رقبا و Build vs Buy

| محصول | نوع | از آن چه یاد بگیریم | محدودیت برای ما |
|---|---|---|---|
| **Cursor** (Team dashboard) | مرجع UX | usage per member، spend limit، لیست مدل + Auto | SaaS، پرداخت از ایران |
| **OpenRouter** | مرجع UX + upstream | صفحه‌ی Activity، کلید با limit، کاتالوگ مدل | شخص ثالث داده را می‌بیند |
| **LiteLLM Proxy** | موتور gateway (OSS) | virtual key، بودجه user/team با duration، spend log، OpenAI API، hook برای guardrail | SSO ادمین‌UI بالای ۵ کاربر و audit log نیاز به لایسنس دارند |
| **Langfuse** | Trace (OSS) | trace/span، latency، فیلتر؛ هسته MIT | RBAC پروژه‌ای، audit log، masking سمت سرور = Enterprise |
| **Open WebUI** | چت (OSS) | RBAC گروهی، دسترسی مدل per-group | از v0.6.6 تغییر برند بالای ۵۰ کاربر لایسنس می‌خواهد؛ بودجه ندارد |
| **LibreChat** | چت (OSS) | balance توکن و auto-refill | balance سراسری است، per-user فقط با اسکریپت |
| **Portkey / TrueFoundry / Kong AI GW** | Gateway تجاری | governance آماده | هزینه، وابستگی، دسترسی |
| **ChatGPT Enterprise / Claude Enterprise** | خرید کامل | معیار کیفیت | احتمالاً به‌دلیل تحریم/قرارداد در دسترس نیست |

### تصمیم پیشنهادی: «Compose, don't vibe-code the core»
وایت‌برد عنوان «vibe coded» دارد. برای **چت UI و داشبورد** این خوب است. برای **حسابداری توکن، مدیریت کلید و احراز هویت** خطرناک است: باگ در این‌ها یعنی پول سوخته یا کلید لو رفته.

```
                ┌──────────── Keycloak (OIDC روی AD) ────────────┐
                │   ← «Auth API used by product too» همین است     │
Browser (React) ─► Hub API (Python/FastAPI — کد ما)               │
VS Code ────────►   • SSO، RBAC، سشن‌ها                            │
                    • Accounting: سلسله‌مراتب واحد، بودجه، دوره    │
                    • صدور API key (wrapper روی virtual key)        │
                    • Guardrail (local model، prompt از DB)         │
                    • Files: MinIO + parsing                        │
                    └─► LiteLLM Proxy (موتور) ─► OpenRouter / مستقیم / vLLM
                              └─► OTel → Langfuse (trace, TTFT)
                    Postgres (state) + ClickHouse (usage/trace)
```

- **چرا Hub API خودمان جلوی LiteLLM؟** SSO، RBAC، audit و سلسله‌مراتب واحد را خودمان می‌سازیم ← لایسنس Enterprise LiteLLM لازم نیست و اگر روزی LiteLLM را عوض کردیم، فقط موتور عوض می‌شود.
- **چرا Keycloak به‌جای «Auth API» خودساخته؟** محصولات دیگر سازمان هم با OIDC استاندارد وصل می‌شوند؛ نوشتن IdP از صفر یکی از پرریسک‌ترین کارهای ممکن است.
- **چرا Open WebUI نه؟** فرانت React خودتان را دارید؛ fork از Open WebUI هم با مشکل لایسنس برند و هم با بودجه‌ی ناموجود روبه‌رو است.

## ۵. فرض‌های پرریسک (قابل ابطال)

| # | فرض | تست | معیار موفقیت | نتیجه |
|---|---|---|---|---|
| A1 | دسترسی پایدار و مجاز به مدل‌های جهانی داریم | استعلام حقوقی + اسکریپت uptime ۱۴ روزه روی ۲ مسیر | تأیید مکتوب + uptime ≥ ۹۹٪ | TBD |
| A2 | کارمندان با کیفیت برابر، ابزار شخصی را رها می‌کنند | پایلوت ۳۰ نفر ۷ روز + مقایسه ترافیک پروکسی | ≥ ۷۰٪ «دیگر نیاز ندارم» و −۳۰٪ ترافیک خارجی آن‌ها | TBD |
| A3 | دیدن usage/سهمیه در پروفایل اعتماد می‌سازد و مصرف بی‌رویه را کم می‌کند | A/B در پایلوت: با/بدون صفحه‌ی Usage | ≥ ۱۵٪ کمتر سهمیه‌ی تمام‌شده در گروه با صفحه | TBD |
| A4 | dev‌ها کلید سازمانی را در VS Code جایگزین ابزار پولی شخصی می‌کنند | ۱۰ dev، ۲ هفته، Continue/Cline با کلید Hub | ≥ ۷/۱۰ بعد از ۲ هفته هنوز فعال | TBD |
| A5 | اگر کارمند بداند prompt‌هایش trace می‌شود، استفاده کم نمی‌شود | نظرسنجی ناشناس (n ≥ ۱۰۰) با دو متن اطلاع‌رسانی | ≥ ۸۰٪ «همچنان استفاده می‌کنم» با متن «فقط امنیت، با لاگ دسترسی» | TBD |
| A6 | Guardrail محلی ≤ ۳۰۰ms و ≥ ۹۵٪ recall روی داده‌ی حساس | ۵۰۰ پرامپت برچسب‌خورده | p95 ≤ ۳۰۰ms، recall ≥ ۹۵٪، FP ≤ ۵٪ | TBD |
| A7 | بودجه‌ی per-user ماهانه X دلار برای ۹۰٪ کاربران کافی است | دو هفته پایلوت بدون سقف، اندازه‌گیری توزیع مصرف | p90 مصرف ≤ X | TBD |

## ۶. برنامه‌ی Discovery (هفته‌ی ۱–۳، موازی با Foundation)

| سگمنت | تعداد مصاحبه (حداقل) | سؤال کلیدی |
|---|---|---|
| کارمند عمومی (۳ واحد) | ۶ | «آخرین باری که از ChatGPT برای کار استفاده کردی را تعریف کن» |
| توسعه‌دهنده | ۶ | «الان در IDE از چه ابزار AI استفاده می‌کنی و چطور پولش را می‌دهی؟» |
| مدیر واحد | ۵ | «اگر تیمت ماهی X خرج AI کند، چه چیزی را باید ببینی؟» |
| CISO / امنیت | ۵ | «کدام نوع داده اگر بیرون برود فاجعه است؟ کدام قابل قبول؟» |
| ادمین IT | ۵ | «ساخت کاربر و تغییر دسترسی الان چطور انجام می‌شود؟» |

**داده‌ی کمّی موازی:** baseline ترافیک پروکسی به سرویس‌های AI (۲ هفته) + نظرسنجی ۱۰ سؤالی (n ≥ ۲۰۰).
**قانون:** هیچ آیتم Next/Later بدون حداقل ۵ مصاحبه در سگمنت مربوط به Now منتقل نمی‌شود.

---

### منابع
- LiteLLM Enterprise: https://docs.litellm.ai/docs/enterprise
- Open WebUI License: https://docs.openwebui.com/license/
- Langfuse open source / license key: https://langfuse.com/docs/open-source · https://langfuse.com/self-hosting/license-key
- LibreChat balance: https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/balance
- Open WebUI vs LibreChat (Portkey, vendor): https://portkey.ai/blog/openwebui-vs-librechat/
- OpenRouter Jev Router: https://openrouter.ai/docs/guides/routing/routers/jev-router

_جزئیات لایسنس‌ها از docs و خلاصه‌های ثانویه است؛ قبل از تصمیم نهایی، متن لایسنس را با واحد حقوقی چک کنید._
