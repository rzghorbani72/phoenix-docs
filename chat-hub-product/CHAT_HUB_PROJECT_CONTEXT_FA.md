# زمینهٔ سراسری پروژه LLM Hub

این فایل مرجع کوتاه زمینه برای هر گفت‌وگو یا کار فنی دربارهٔ پروژهٔ **LLM Hub سازمانی** است. «چت هاب» و `Chat Hub` نام‌های مستعار همین پروژه‌اند. خلاصهٔ اسناد است، نه جایگزین آن‌ها؛ برای جزئیات به منابع پایین رجوع کنید.

> **تمایز نام:** نام اصلی این پروژه **LLM Hub** است (درگاه AI داخلی برای کارمندان). با «چت‌بات مرکز تماس» (محصول مکالمه‌ای رو به مشتری/کارمند در خانوادهٔ IVA/AIVA) یکی نیست؛ این دو را قاطی نکنید.

## پروژه چیست؟
یک Hub داخلی AI برای کارمندان: چت وب با لاگین سازمانی (SSO)، دسترسی به مدل‌های جهانی از چند ارائه‌دهنده، و API سازمانی سازگار با OpenAI برای توسعه‌دهندگان (VS Code/Continue/Cline). هدف: جایگزین اکانت‌های شخصی و Shadow AI، با شفافیت هزینه، بودجه و کنترل امنیتی.

- **فرضیهٔ MVP:** با لاگین سازمانی و کیفیت برابر مدل‌ها و سهمیهٔ شفاف، ≥۷۰٪ از ۱۰۰ کاربر پایلوت بعد از ۴ هفته هفتگی فعال بمانند و ترافیک به سرویس‌های AI خارجی ≥۳۰٪ کم شود.
- **منطق اولویت:** اول پذیرش (کیفیت، تاریخچه، آپلود، Usage)، بعد کنترل (RBAC، guardrail enforce، واحد سازمانی).
- **پشتهٔ هدف (پیشنهادی در ADR، نه الزاماً پیاده‌شده):** Hub API (FastAPI) + LiteLLM + Keycloak + Postgres + MinIO + Langfuse.

## سگمنت‌ها
کارمند عمومی، توسعه‌دهنده، مدیر واحد/صاحب بودجه، و (در Next) Security Auditor و Platform Admin.

## وضعیت و مراحل (از ROADMAP.md)
M0 Discovery+Foundation (۲۰۲۶-۱۱-۱۷) ← M1 Internal Alpha ۵۰ نفر (۲۰۲۶-۱۲-۱۵) ← M2 Pilot+Dev Beta ۱۰۰+۱۰ نفر (۲۰۲۷-۰۱-۱۲) ← M3 Admin & Governance ← M4 Guardrail Enforce ← M5 GA (۲۰۲۷-۰۴-۲۰). تاریخ‌ها به فرض‌های تیم و دسترسی A1 (ارائه‌دهنده‌ها)، Keycloak/AD وابسته‌اند.

## هشدارهای مهم برای هر کمک‌کننده
1. **هنوز ۰ مصاحبهٔ کاربر انجام نشده.** هر چه «فرض» علامت خورده، نظر ذی‌نفعان است نه شواهد.
2. قابلیت‌ها در سه تیر Now / Next / Later هستند؛ Next و Later را «موجود» یا «تعهدشده» معرفی نکنید.
3. Explicitly cut در MVP: سلسله‌مراتب واحد، داشبورد کامل ادمین، guardrail enforce/چندرسانه‌ای، Files API، Auth API، Agents/Memory/Auto routing.
4. حریم خصوصی trace (دسترسی مدیر به پرامپت کارمند) و نشت از trace از corner caseهای اصلی‌اند (C9/C10)؛ پیش از طراحی، سیاست حریم خصوصی (A5) را ببینید.
5. وضعیت واقعی کد را از خود کد بخوانید؛ این اسناد برنامه‌اند، نه توصیف پیاده‌سازی.

## منابع (نسبت به ریشهٔ مخزن)
- `chat-hub-product/FEATURES.md` — فهرست قابلیت‌ها در Now/Next/Later.
- `chat-hub-product/MVP.md` — فرضیه، In scope، Explicitly cut، معیار Go/Pivot.
- `chat-hub-product/ROADMAP.md` — مراحل M0–M5 و تاریخ‌ها.
- `chat-hub-product/DISCOVERY.md` — outcomeها، سگمنت‌ها، JTBD، برنامهٔ مصاحبه (§۶).
- `chat-hub-product/FEASIBILITY.md` — امکان‌سنجی فنی هر قابلیت.
- `chat-hub-product/CORNER_CASES.md` — حالت‌های لبه C1–C14+ (بودجه، API key، trace، guardrail، auth).
- `chat-hub-product/llm-hub-product.html` — ارائهٔ محصول.

## متن آماده برای آغاز کار
> زمینه: روی پروژهٔ LLM Hub سازمانی کار می‌کنیم (نام مستعار: چت هاب/Chat Hub). `chat-hub-product/CHAT_HUB_PROJECT_CONTEXT_FA.md` را بخوان و برای جزئیات به FEATURES/MVP/ROADMAP/FEASIBILITY/CORNER_CASES رجوع کن. فرض‌ها را از شواهد و آیتم‌های Next/Later را از MVP جدا نگه دار.
