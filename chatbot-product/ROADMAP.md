# Roadmap
_Last updated: 2026-10-27_

**فرض‌های پایه برای همه‌ی تاریخ‌ها:** تیم ۳ تا ۴ مهندس (۱ فرانت، ۲ بک‌اند/پلتفرم، ۰.۵ DevOps) + ۱ PM یا PO پاره‌وقت. Keycloak یا AD در دسترس است. A1 (دسترسی به ارائه‌دهنده‌ها) تا پایان M0 تأیید می‌شود. **اگر هر کدام از این‌ها غلط باشد، همه‌ی تاریخ‌ها جابه‌جا می‌شوند.**

---

## M0 — Discovery + Foundation — target: 2026-11-17 (۳ هفته)
**Depends on:** دسترسی به ۲۷ نفر برای مصاحبه، لاگ پروکسی سازمان، استعلام حقوقی.
**Scope:**
- ۲۷ مصاحبه طبق [DISCOVERY.md](DISCOVERY.md) §۶ + baseline ترافیک Shadow AI.
- تصمیم معماری (ADR): Hub API (FastAPI) + LiteLLM + Keycloak + Postgres + MinIO + Langfuse.
- Hub API اسکلت + Keycloak + LiteLLM در docker-compose. حذف `VITE_API_KEY` از فرانت.
- CI، محیط staging، secret management.

**What breaks the date:** جواب منفی یا معلق برای A1. Keycloak به AD وصل نشود.

## M1 — Internal Alpha (۵۰ نفر، واحد فنی) — target: 2026-12-15 (۴ هفته)
**Depends on:** M0. نتیجه‌ی مصاحبه‌ها لیست مدل‌ها و سقف بودجه را تأیید کند.
**Scope:** SSO اجباری · چت چندمدلی با انتخاب مدل · تاریخچه‌ی سرور · آپلود فایل/تصویر · بودجه‌ی flat per-user · صفحه‌ی Usage · trace metadata + TTFT · 👍/👎 · guardrail shadow متنی.
**What breaks the date:** streaming از مسیر Hub API و LiteLLM latency قابل‌قبولی ندهد (p95 TTFT > ۲s). مهاجرت تاریخچه از `localStorage`.

## M2 — Pilot + Dev Beta (۱۰۰ نفر از ۳ واحد + ۱۰ dev) — target: 2027-01-12 (۴ هفته)
**Depends on:** M1 پایدار (بدون P0 در ۲ هفته‌ی آخر).
**Scope:** API key سلف‌سرویس (پیشوند، expiry، budget و rate limit per-key) · راهنمای VS Code (Continue/Cline) · هشدار ۸۰٪ و ۱۰۰٪ · اجرای تست‌های A2، A3، A4 و A7.
**What breaks the date:** ایجنت‌های IDE بودجه را در روزهای اول تمام کنند ← باید rate limit و سقف per-key از روز اول باشد.

**🚦 Go/No-Go (2027-01-12):** بر اساس معیارهای [MVP.md](MVP.md).

## M3 — Admin & Governance — target: 2027-02-23 (۶ هفته)
**Depends on:** Go از M2. ۵+ مصاحبه با مدیران و امنیت. **سیاست حریم خصوصی trace تصویب شده.**
**Scope:** داشبورد ادمین · RBAC پنج‌نقشی · سلسله‌مراتب واحد + sync از AD · بودجه per-واحد/per-دوره · مدیریت سشن‌ها · trace search/filter با دسترسی محتوای break-glass و لاگ‌شده · Home stats.
**What breaks the date:** ساختار واحدها در AD تمیز نباشد (معمولاً نیست). تصویب سیاست حریم خصوصی طول بکشد.

## M4 — Guardrail Enforce — target: 2027-03-23 (۴ هفته)
**Depends on:** ۸+ هفته داده‌ی shadow. A6 پاس شده باشد.
**Scope:** guardrail متنی در حالت enforce (مسدود، ماسک یا هشدار) · ویرایش prompt توسط ادمین با نسخه‌بندی، تست روی دیتاست ثابت و rollback · گزارش امنیتی هفتگی.
**What breaks the date:** false positive > ۵٪. مدل guard محلی latency بیش از ۳۰۰ms داشته باشد.

## M5 — GA سازمانی — target: 2027-04-20 (۴ هفته، شامل نوروز)
**Depends on:** M3 و M4. ظرفیت سرور برای کل سازمان (load test).
**Scope:** rollout تدریجی واحد به واحد · ورک‌شاپ‌ها · Auto routing (اگر دیتاست آماده باشد) · OpenAI Files API.
**What breaks the date:** نوروز (۲۹ اسفند تا ۱۳ فروردین ≈ 2027-03-20 تا 2027-04-02) دو هفته‌ی کاری را می‌گیرد. این در تاریخ لحاظ شده ولی buffer دیگری نیست.

## Later (بعد از GA، بر اساس شواهد)
Guardrail تصویر و صوت · مسیر self-hosted برای داده‌ی حساس · Agents / Memory / RAG · Auth برای محصولات دیگر.

---

```
Nov '26     Dec        Jan '27     Feb        Mar        Apr
|M0 ███|
       |M1 ████|
                |M2 ████|🚦
                         |M3 ██████|
                                    |M4 ████|
                                            |M5 ████| GA
```
