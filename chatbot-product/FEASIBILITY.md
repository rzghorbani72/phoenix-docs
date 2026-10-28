# Feasibility Assessment
_Last updated: 2026-10-27_

**وضعیت کد امروز:** ریپو فقط یک فرانت React 19 + Vite است ([src/lib/api.ts](../src/lib/api.ts)، [src/hooks/useConversations.ts](../src/hooks/useConversations.ts)). بک‌اند نداریم، تاریخچه در `localStorage` است و کلید API در bundle مرورگر (`VITE_API_KEY`) قرار دارد. پس هر effort پایین «بک‌اند از صفر» را فرض می‌کند، با یک تیم ۳ تا ۴ نفره (فرض).

مقیاس: S ≤ ۱ هفته · M = ۲–۳ هفته · L = ۱–۲ ماه · XL > ۲ ماه (یک نفر تمام‌وقت)

---

## Auth + SSO + سشن‌ها
**Effort:** M — با Keycloak روی AD موجود. اگر Auth API از صفر نوشته شود: XL.
**Impact:** پیش‌نیاز همه‌چیز. بدون هویت، نه usage داریم نه بودجه و نه trace.
**Risk:** مدیریت refresh token و revoke سشن. یک IdP خودساخته = ریسک امنیتی بالا.
**Confidence:** High

مدیریت سشن (لیست و revoke) در Keycloak آماده است. فقط باید در داشبورد نمایش داده شود.

## Gateway چندمدلی + لیست مدل (مثل Cursor)
**Effort:** S تا M — LiteLLM به‌عنوان موتور. لیست مدل per-role در Hub API.
**Impact:** مستقیماً O1 (کیفیت = پذیرش).
**Risk:** وابستگی به A1 (دسترسی به ارائه‌دهنده). ترجمه‌ی tool-calling بین فرمت‌ها برای مدل‌های غیر OpenAI ناقص است.
**Confidence:** High

## Accounting: CRUD کاربر + بودجه per-user / per-واحد / per-دوره
**Effort:** L — CRUD ساده است، ولی **سلسله‌مراتب واحد سازمانی** (سازمان ← معاونت ← واحد ← کاربر) و دوره‌ها (روزانه/ماهانه) در نسخه‌ی رایگان LiteLLM نیست. budget روی user/team/key با `budget_duration` هست، ولی org hierarchy و admin سازمانی Enterprise است. پس سلسله‌مراتب را در Hub API می‌سازیم و در LiteLLM به team/user نگاشت می‌کنیم.
**Impact:** O4. بدون آن، روشن کردن مدل‌های گران برای ۱۰ هزار نفر از نظر مالی ریسک است.
**Risk:** Race condition در کسر بودجه در درخواست‌های همزمان streaming (CORNER_CASES). کاربری که واحدش عوض می‌شود.
**Confidence:** Medium — رفتار دقیق LiteLLM در overspend همزمان باید تست شود.

## صفحه‌ی Usage در پروفایل + Home Stats
**Effort:** M — LiteLLM spend log دارد. aggregation در ClickHouse/Postgres و UI در React.
**Impact:** O2. فرض A3: دیدن سهمیه اعتماد می‌سازد.
**Risk:** کم. نکته: عدد «توکن باقی‌مانده» برای مدل‌های مختلف بی‌معنی است. **به‌جای آن «اعتبار» (credit یا ریال) نشان دهید**، مثل Cursor و OpenRouter.
**Confidence:** High

## API key سلف‌سرویس OpenAI-compatible برای VS Code
**Effort:** S تا M — virtual key در LiteLLM. Hub API فقط صدور، نمایش یک‌باره، revoke، expiry و budget per-key را مدیریت می‌کند.
**Impact:** O3. dev‌ها پرمصرف‌ترین و پرریسک‌ترین کاربرها از نظر نشت کد هستند.
**Risk:** نشت کلید در git. ایجنت‌های IDE (Cline/Roo) ۱۰ تا ۱۰۰ برابر چت توکن مصرف می‌کنند و بودجه را می‌ترکانند.
**Confidence:** High

## OpenAI Files API
**Effort:** L — LiteLLM پاس‌ترو دارد، ولی `file_id` مخصوص هر ارائه‌دهنده است. فایلی که برای OpenAI آپلود شده با Claude کار نمی‌کند. برای جدا شدن از ارائه‌دهنده باید فایل در MinIO خودمان ذخیره و هنگام فراخوانی به فرمت هر ارائه‌دهنده تبدیل شود.
**Impact:** متوسط. dev‌ها کمتر از Files API مستقیم استفاده می‌کنند. چت با فایل (O1) مهم‌تر است.
**Risk:** پیچیدگی سازگاری. هزینه‌ی ذخیره‌سازی.
**Confidence:** Medium

## File process + File storage (چت)
**Effort:** M — MinIO، استخراج متن PDF/DOCX (pdfjs در فرانت فعلی هست؛ سمت سرور Docling یا Unstructured)، تصویر به مدل vision.
**Impact:** O1. حجم زیادی از کار کارمندان عمومی سند است.
**Risk:** فایل‌های بزرگ از context window بیشتر می‌شوند. اسکن بدافزار.
**Confidence:** High

## Trace (search + filter، custom span با TTFT)
**Effort:** M — OTel GenAI conventions به Langfuse (هسته MIT). TTFT را در Hub API اندازه بگیرید، از لحظه‌ی دریافت تا اولین chunk SSE، و به‌عنوان span attribute بفرستید.
**Impact:** O5 و عملیات (دیباگ latency).
**Risk:** **حریم خصوصی.** اگر مدیران بتوانند متن پرامپت کارمندان را بخوانند، فرض A5 می‌شکند. RBAC پروژه‌ای و masking در Langfuse لایسنس می‌خواهند، پس کنترل دسترسی به محتوا را در Hub API انجام دهید و در Langfuse فقط metadata یا محتوای ماسک‌شده بفرستید.
**Confidence:** Medium

## Guardrail (local، multimodal، prompt قابل‌تغییر توسط ادمین)
**Effort:** L
- متن: مدل guard محلی روی vLLM (Gemma فعلی یا یک guard model) + regex. policy prompt در DB، قابل ویرایش و نسخه‌دار.
- تصویر: OCR + vision guard.
- صوت: Whisper محلی برای transcribe، بعد guard متنی.

**Impact:** O5. ولی اگر زود و سخت‌گیرانه فعال شود، با false positive، O1 را می‌کشد.
**Risk:** latency اضافه، false positive، fail-open/fail-closed. **ادمینی که prompt guard را عوض کند می‌تواند ناخواسته همه‌چیز را باز یا بسته کند.** پس نسخه‌بندی، تست روی دیتاست ثابت قبل از publish و rollback لازم است.
**Confidence:** Medium — بسته به A6.

## Auto routing (Jev / Gemma)
**Effort:** M — طراحی‌اش در گفت‌وگوی قبلی انجام شد (guided choice + logprobs).
**Impact:** هزینه −۳۰ تا −۵۰٪ (تخمین). کیفیت باید ثابت بماند.
**Risk:** routing اشتباه = افت کیفیت حس‌شده.
**Confidence:** Low — داده‌ی برچسب‌خورده نداریم.

## Agent library / Memory (سمت راست وایت‌برد، ناخوانا)
**Effort:** XL
**Impact:** نامعلوم. شواهدی از کاربران نداریم.
**Confidence:** Low — Later تا بعد از Discovery.
