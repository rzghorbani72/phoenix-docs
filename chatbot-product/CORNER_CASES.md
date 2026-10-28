# Corner Cases
_Last updated: 2026-10-27_

## Accounting / بودجه

### C1 — Overspend همزمان
**Scenario:** کاربر با $0.10 بودجه‌ی باقی‌مانده، ۵ درخواست streaming همزمان (مثلاً ایجنت IDE) می‌فرستد. هر کدام موقع شروع بودجه را چک می‌کند و همه رد می‌شوند.
**Effect:** هزینه‌ی واقعی چند برابر بودجه می‌شود، چون هزینه بعد از پایان stream محاسبه می‌شود.
**Source:** الگوی شناخته‌شده‌ی metering بعد از مصرف.
**Status:** Open — رزرو بودجه قبل از درخواست (بر اساس max_tokens تخمینی) + تسویه بعد از پایان + سقف concurrency per-key.

### C2 — Stream قطع‌شده
**Scenario:** کاربر وسط پاسخ تب را می‌بندد یا Stop می‌زند.
**Effect:** ارائه‌دهنده توکن تولیدشده را حساب می‌کند ولی usage chunk آخر هرگز نمی‌رسد. اختلاف بین حساب ما و صورتحساب ارائه‌دهنده.
**Source:** رفتار SSE. فرانت فعلی [src/lib/api.ts](../src/lib/api.ts) abort دارد.
**Status:** Open — `stream_options.include_usage`. در abort، توکن‌ها را از متن دریافت‌شده تخمین بزنید. reconcile ماهانه با صورتحساب.

### C3 — جابه‌جایی کاربر بین واحدها وسط دوره
**Scenario:** کاربر روز ۱۵ ماه از واحد A به B می‌رود (sync از AD).
**Effect:** هزینه‌ی نیمه‌ی اول ماه به حساب B می‌رود یا بودجه‌اش reset می‌شود.
**Source:** مدل داده‌ی سلسله‌مراتبی.
**Status:** Open — هزینه را در لحظه‌ی تراکنش با `org_unit_id` ثبت کنید، نه با join روی وضعیت فعلی کاربر.

### C4 — «توکن باقی‌مانده» گمراه‌کننده است
**Scenario:** کاربر «۱M توکن باقی‌مانده» می‌بیند. با Opus، این مقدار ۲۰ برابر سریع‌تر از Haiku تمام می‌شود.
**Effect:** کاربر غافلگیر و عصبانی می‌شود و اعتماد از بین می‌رود (O2).
**Source:** دلیل اینکه Cursor و OpenRouter اعتبار پولی نشان می‌دهند، نه توکن.
**Status:** Open — واحد نمایش را «اعتبار» بگذارید. توکن فقط در جزئیات نمایش داده شود.

## API Key / Developer

### C5 — نشت کلید در git
**Scenario:** dev کلید را در `settings.json` یا `.env` کامیت می‌کند.
**Effect:** هر کسی که به ریپو دسترسی دارد با سهمیه‌ی آن dev مصرف می‌کند.
**Source:** الگوی رایج. GitHub/GitLab secret scanning بر اساس پیشوند کار می‌کند.
**Status:** Open — پیشوند یکتا `hub-sk-` + قانون در GitLab secret detection داخلی + expiry پیش‌فرض ۹۰ روز + IP allowlist اختیاری.

### C6 — ایجنت IDE در حلقه
**Scenario:** Cline یا Roo در یک loop خطا ۲۰۰ درخواست ۱۰۰k توکنی می‌فرستد.
**Effect:** بودجه‌ی ماه در ۱ ساعت تمام می‌شود.
**Source:** رفتار شناخته‌شده‌ی ایجنت‌های کدنویسی.
**Status:** Open — rate limit (RPM و TPM) per-key + سقف روزانه علاوه بر ماهانه.

### C7 — ناسازگاری tool calling
**Scenario:** dev مدل Claude را از مسیر OpenAI-compatible با tool calling موازی صدا می‌زند.
**Effect:** فرمت tool call‌ها یا stream بعد از ترجمه کمی متفاوت است و برخی افزونه‌های IDE می‌شکنند.
**Source:** لایه‌ی ترجمه‌ی LiteLLM و OpenRouter.
**Status:** Open — یک suite تست با Continue و Cline روی هر مدل مجاز، قبل از اضافه کردن آن به لیست dev.

### C8 — `file_id` بین ارائه‌دهنده‌ها
**Scenario:** dev فایل را از Files API آپلود می‌کند و بعد با مدل دیگری به آن ارجاع می‌دهد.
**Effect:** خطای 404 یا رفتار متفاوت.
**Source:** Files API مخصوص هر ارائه‌دهنده است.
**Status:** Open — ذخیره‌سازی مستقل در MinIO و `file_id` خودمان (FEASIBILITY).

## Trace / Privacy

### C9 — مدیر پرامپت کارمند را می‌خواند
**Scenario:** مدیر واحد در trace متن پرامپت‌های یک کارمند را باز می‌کند، مثلاً سؤال پزشکی یا شخصی.
**Effect:** شایعه پخش می‌شود، استفاده سقوط می‌کند و کارمندان به ابزار شخصی برمی‌گردند. Outcome اصلی می‌شکند. ریسک حقوقی هم دارد.
**Source:** فرض A5. ویژگی‌های RBAC و masking در Langfuse self-hosted پولی است.
**Status:** Open — پیش‌فرض: مدیران فقط metadata می‌بینند. محتوا فقط برای نقش Security Auditor با دلیل ثبت‌شده و لاگ دسترسی. سیاست را قبل از لانچ به کارمندان اعلام کنید.

### C10 — Trace خودش نشت داده است
**Scenario:** Langfuse یا ClickHouse همه‌ی پرامپت‌ها را خام نگه می‌دارد، از جمله داده‌ی حساس.
**Effect:** بزرگ‌ترین مخزن داده‌ی حساس سازمان بدون retention.
**Source:** طراحی.
**Status:** Open — retention (مثلاً ۹۰ روز برای محتوا، ۲ سال برای metadata) + رمزنگاری at-rest + ماسک قبل از ذخیره.

## Guardrail

### C11 — Guardrail down است
**Scenario:** سرور vLLM مدل guard ری‌استارت می‌شود.
**Effect:** fail-closed یعنی کل سازمان بدون چت. fail-open یعنی بدون محافظت.
**Source:** طراحی.
**Status:** Open — در shadow حالت fail-open. در enforce، regex همیشه اجرا شود و مدل guard با timeout ۳۰۰ms fail-open + alert.

### C12 — ادمین prompt guard را خراب می‌کند
**Scenario:** ادمین policy prompt را ویرایش می‌کند و ناخواسته همه‌ی پرامپت‌ها «حساس» می‌شوند.
**Effect:** کل سازمان مسدود یا ماسک‌شده.
**Source:** وایت‌برد («prompt change by Admin»).
**Status:** Open — نسخه‌بندی + اجرای خودکار روی دیتاست ثابت قبل از publish (اگر FP > ۵٪ باشد، بلاک شود) + rollback یک‌کلیکی + canary روی ۵٪ ترافیک.

### C13 — دور زدن guardrail با تصویر یا فایل
**Scenario:** کاربر متن محرمانه را اسکرین‌شات می‌گیرد یا داخل PDF آپلود می‌کند.
**Effect:** guard متنی آن را نمی‌بیند.
**Source:** وایت‌برد (multimodal).
**Status:** Accepted risk تا M4 — در Later با OCR بسته می‌شود. فعلاً در trace علامت `has_attachment` بخورد.

## Auth / Session

### C14 — کارمند جداشده
**Scenario:** کارمند از سازمان می‌رود. حساب AD غیرفعال می‌شود ولی API key‌اش فعال است.
**Effect:** دسترسی ادامه‌دار از بیرون سازمان.
**Source:** الگوی رایج. کلیدها به سشن SSO وابسته نیستند.
**Status:** Open — sync روزانه از AD: کاربر غیرفعال ← revoke همه‌ی کلیدها و سشن‌ها.

### C15 — اعتبار تاریخچه‌ی قدیمی
**Scenario:** کاربران فعلی تاریخچه‌ی چت را در `localStorage` دارند ([src/hooks/useConversations.ts](../src/hooks/useConversations.ts)).
**Effect:** بعد از لاگین، تاریخچه گم‌شده به نظر می‌رسد.
**Source:** کد فعلی.
**Status:** Open — یک بار import خودکار به سرور بعد از اولین لاگین.
