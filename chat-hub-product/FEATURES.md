# Feature List
_Last updated: 2026-10-27_

تیرها بر اساس [FEASIBILITY.md](FEASIBILITY.md) و Opportunity Tree در [DISCOVERY.md](DISCOVERY.md) چیده شده‌اند. منطق اصلی این است که **اول پذیرش (O1/O2/O3)، بعد کنترل (O4/O5).**

## Now (MVP — تا Internal Alpha / Dev Beta)
- **SSO با Keycloak + لاگین اجباری** — پیش‌نیاز همه‌چیز. کلید از مرورگر حذف می‌شود.
- **Hub API + LiteLLM + ۳ ارائه‌دهنده با fallback** — کیفیت = پذیرش. (ref: LiteLLM, OpenRouter)
- **انتخاب مدل از لیست مجاز per-role** — مثل Cursor. (ref: Cursor model picker)
- **تاریخچه‌ی چت سمت سرور** — `localStorage` برای سازمان قابل قبول نیست.
- **آپلود فایل/تصویر در چت + MinIO** — بیشتر کار کارمندان عمومی با سند است.
- **بودجه‌ی ماهانه per-user (flat) + per-team** — جلوی سوختن پول در پایلوت را می‌گیرد.
- **صفحه‌ی Usage در پروفایل** — اعتبار مصرف‌شده و باقی‌مانده، به تفکیک مدل و روز. هشدار ۸۰٪. (ref: Cursor dashboard, OpenRouter Activity)
- **API key سلف‌سرویس OpenAI-compatible** — پیشوند قابل اسکن (`hub-sk-`)، expiry، budget per-key، rate limit، راهنمای Continue/Cline. (ref: OpenRouter keys)
- **Trace پایه + TTFT** — هر درخواست با user، model، tokens، cost، TTFT و latency. فقط metadata.
- **Guardrail در حالت Shadow (فقط متن)** — برچسب می‌زند، چیزی را مسدود نمی‌کند. داده برای فاز enforce جمع می‌شود.
- **👍/👎 روی هر پاسخ** — تنها معیار «افت کیفیت».

## Next (بعد از ۵+ مصاحبه در هر سگمنت مرتبط)
- **داشبورد ادمین با RBAC کامل** (نقش‌ها: Employee, Developer, Team Manager, Security Auditor, Platform Admin) — مسدود است تا مصاحبه با مدیران واحد مشخص کند چه چیزی واقعاً لازم است.
- **سلسله‌مراتب واحد سازمانی + بودجه per-واحد/per-دوره + sync از AD** — مسدود روی دسترسی به ساختار سازمانی در AD.
- **Trace search/filter + دسترسی محتوا با break-glass** — اول باید سیاست حریم خصوصی تصویب شود (A5).
- **مدیریت سشن‌ها در داشبورد** (لیست و revoke) — روی Keycloak.
- **Guardrail enforce برای متن + prompt قابل‌ویرایش ادمین با نسخه‌بندی و تست** — مسدود روی نتیجه‌ی A6.
- **Home stats** (WAU، هزینه، top models، top واحدها).
- **Auto routing** (Gemma یا Jev) — مسدود روی دیتاست ۵۰۰ پرامپت برچسب‌خورده.
- **OpenAI Files API مستقل از ارائه‌دهنده**.

## Later
- **Guardrail تصویر و صوت** (OCR + vision guard، Whisper) — حجم تصویر/صوت حساس باید اول از trace دیده شود.
- **Auth API برای محصولات دیگر** — با Keycloak در عمل رایگان است. کار اصلی onboarding محصولات است.
- **Self-hosted routing برای داده‌ی حساس** (سناریو ۲).
- **Agent library، Memory، RAG روی اسناد داخلی** — آیتم‌های سمت راست وایت‌برد. هیچ شواهدی هنوز نداریم.
- **کارت سازمانی / پرداخت** (سمت راست وایت‌برد، ناخوانا) — باید روشن شود منظور چیست.
