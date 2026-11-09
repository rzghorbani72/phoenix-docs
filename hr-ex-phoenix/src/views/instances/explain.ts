import type { ComponentRole } from "../../lib/instanceTypes";
import type { PipelineStageId } from "../../lib/instances";
import type { Lang } from "./i18n";

/**
 * What each thing does and why it matters. Ops records values, not the reasons behind them, so
 * nothing here claims why a value was chosen. Sources: README and the pipeline map content.
 */
type Text = { en: string; fa: string };

export const STEP_WHY: Record<PipelineStageId, { what: Text; why: Text }> = {
  call: {
    what: {
      en: "Takes the caller's audio, decides when they have finished speaking, turns speech into text and reads the answer back.",
      fa: "صدای تماس‌گیرنده را می‌گیرد، تشخیص می‌دهد حرفش تمام شده، گفتار را به نوشتار تبدیل می‌کند و پاسخ را می‌خواند.",
    },
    why: {
      en: "This is what callers feel directly. The timing values decide whether the assistant answers quickly or cuts people off, and the speech service decides how well it understands them and where the audio goes.",
      fa: "تماس‌گیرنده همین بخش را مستقیم حس می‌کند. مقادیر زمانی تعیین می‌کنند دستیار سریع پاسخ دهد یا حرف را قطع کند، و سرویس گفتار تعیین می‌کند چقدر درست می‌فهمد و صدا به کجا می‌رود.",
    },
  },
  brain: {
    what: {
      en: "Reads each caller turn, applies the guardrails, chooses what to do and writes the answer.",
      fa: "هر نوبت تماس‌گیرنده را می‌خواند، گاردریل‌ها را اعمال می‌کند، تصمیم می‌گیرد چه کند و پاسخ را می‌نویسد.",
    },
    why: {
      en: "Answer quality and safety are decided here. The brain version sets which features exist, the model sets quality, speed and cost, and the tools set what the assistant is allowed to do.",
      fa: "کیفیت و ایمنی پاسخ اینجا تعیین می‌شود. نسخهٔ مغز قابلیت‌ها را، مدل کیفیت و سرعت و هزینه را، و ابزارها کارهای مجاز دستیار را تعیین می‌کنند.",
    },
  },
  kb: {
    what: {
      en: "Stores the approved content and finds the passages that match each question.",
      fa: "محتوای تأییدشده را نگه می‌دارد و بخش‌های مرتبط با هر پرسش را پیدا می‌کند.",
    },
    why: {
      en: "The assistant should answer from approved content, not from what a model happens to recall. Own collections keep one instance's answers from appearing in another.",
      fa: "دستیار باید از محتوای تأییدشده پاسخ دهد، نه از حافظهٔ مدل. مجموعه‌های مستقل نمی‌گذارند پاسخ یک نمونه در نمونهٔ دیگر ظاهر شود.",
    },
  },
  analytics: {
    what: {
      en: "After a call ends, collects the record, transcribes and analyses it, and serves the results to the analytics panel.",
      fa: "پس از پایان تماس، سابقه را جمع می‌کند، متن و تحلیل می‌سازد و نتیجه را به پنل تحلیل می‌دهد.",
    },
    why: {
      en: "This is where calls become reports, and where people's data rests. Topics, databases and buckets show whether this instance's calls are kept apart from other instances.",
      fa: "تماس‌ها اینجا به گزارش تبدیل می‌شوند و دادهٔ افراد اینجا می‌ماند. تاپیک‌ها، پایگاه‌های داده و باکت‌ها نشان می‌دهند تماس‌های این نمونه از نمونه‌های دیگر جدا هستند یا نه.",
    },
  },
  ops: {
    what: {
      en: "The gateways, screens, sign-in, caches and monitoring around the pipeline, and the shared models it depends on.",
      fa: "درگاه‌ها، صفحه‌ها، ورود، کش‌ها و پایش پیرامون پایپ‌لاین، و مدل‌های مشترکی که به آن‌ها وابسته است.",
    },
    why: {
      en: "A problem here reaches every step, and a shared service can affect several instances at once. Metrics decide whether anyone would notice.",
      fa: "مشکل این بخش به همهٔ مرحله‌ها می‌رسد و یک سرویس مشترک می‌تواند چند نمونه را با هم تحت تأثیر بگذارد. سنجه‌ها تعیین می‌کنند کسی متوجه مشکل بشود یا نه.",
    },
  },
};

export const SETTING_WHY: Record<string, Text> = {
  AGENT_GREETING_MESSAGE: { en: "The first thing every caller hears. It sets expectations for the whole call.", fa: "نخستین جمله‌ای که هر تماس‌گیرنده می‌شنود و انتظار او را از تماس شکل می‌دهد." },
  AGENT_GREETING_ALLOW_INTERRUPTION: { en: "If on, a caller can start talking without waiting for the greeting to finish.", fa: "اگر روشن باشد، تماس‌گیرنده لازم نیست برای پایان خوشامد صبر کند." },
  AGENT_STT_CLIENT: { en: "Which service hears the caller. It decides accuracy, and whether audio stays on our own servers.", fa: "کدام سرویس صدای تماس‌گیرنده را می‌شنود. دقت را تعیین می‌کند و اینکه صدا روی سرورهای خودمان می‌ماند یا نه." },
  AGENT_STT_MODEL: { en: "The speech model or profile in use. Mistakes here carry into every later step.", fa: "مدل یا پروفایل گفتار. خطای این بخش به همهٔ مرحله‌های بعدی منتقل می‌شود." },
  AGENT_TTS_MODEL: { en: "The voice callers hear for this instance.", fa: "صدایی که تماس‌گیرنده در این نمونه می‌شنود." },
  AGENT_TTS_SPEED: { en: "Faster saves time but is harder to follow on a phone line.", fa: "سرعت بیشتر زمان را کم می‌کند، اما شنیدن پشت تلفن را سخت‌تر می‌کند." },
  AGENT_TURN_MODEL: { en: "How the assistant decides a caller has finished. deactive means silence timing alone decides.", fa: "دستیار چگونه می‌فهمد حرف تماس‌گیرنده تمام شده. deactive یعنی فقط زمان سکوت تصمیم می‌گیرد." },
  AGENT_MIN_ENDPOINTING_DELAY: { en: "Lower replies sooner but risks cutting off someone who only paused.", fa: "مقدار کمتر پاسخ را سریع‌تر می‌کند، اما ممکن است حرف کسی را که فقط مکث کرده قطع کند." },
  AGENT_MAX_ENDPOINTING_DELAY: { en: "The most the assistant waits. Higher is more patient but can feel slow.", fa: "بیشترین زمان انتظار دستیار. مقدار بیشتر صبورتر است، اما می‌تواند کند به نظر برسد." },
  AGENT_MIN_INTERRUPTION_DURATION: { en: "Lower lets callers interrupt easily, but background noise can stop the assistant too.", fa: "مقدار کمتر قطع کردن دستیار را آسان می‌کند، اما صدای محیط هم ممکن است آن را متوقف کند." },
  AGENT_VAD_MIN_SILENCE_DURATION: { en: "How much silence counts as the end of a phrase. Too low splits sentences.", fa: "چه مقدار سکوت پایان عبارت حساب می‌شود. مقدار خیلی کم جمله‌ها را تکه‌تکه می‌کند." },
  AGENT_VAD_PREFIX_PADDING_DURATION: { en: "Audio kept from just before speech starts, so first words are not lost.", fa: "صدای کمی پیش از شروع گفتار نگه داشته می‌شود تا کلمه‌های اول از بین نروند." },
  AGENT_NUM_IDLE_PROCESSES: { en: "Workers already warm for the next call. More answers bursts faster but holds memory.", fa: "پردازش‌های آماده برای تماس بعدی. تعداد بیشتر هجوم تماس را سریع‌تر پاسخ می‌دهد، اما حافظه می‌گیرد." },
  AGENT_SIP_RTP_STABILIZATION_DELAY: { en: "A short wait for audio to settle. It is the first thing to raise if greetings sound clipped.", fa: "مکث کوتاه برای پایدار شدن صدا. اگر ابتدای خوشامد بریده شنیده می‌شود، اول این را زیاد کنید." },
  AGENT_APM_TRANSACTION_SAMPLE_RATE: { en: "How many calls are traced. Higher shows more problems but stores more data.", fa: "چه سهمی از تماس‌ها ردگیری می‌شود. مقدار بیشتر مشکلات بیشتری را نشان می‌دهد، اما دادهٔ بیشتری ذخیره می‌کند." },
  AGENT_KAFKA_TOPIC: { en: "Where the call summary is published after the call, for memory and analytics to read.", fa: "جایی که خلاصهٔ تماس پس از پایان منتشر می‌شود تا حافظه و تحلیل آن را بخوانند." },
  AGENT_LLM_MODEL: { en: "The main answer model. It sets answer quality, speed and cost.", fa: "مدل اصلی پاسخ. کیفیت، سرعت و هزینهٔ پاسخ را تعیین می‌کند." },
  AGENT_ENABLED_TOOLS: { en: "Actions the assistant can take, such as sending an SMS. Each one is something it can do without a person.", fa: "کارهایی که دستیار می‌تواند انجام دهد، مثل ارسال پیامک. هرکدام کاری است که بدون انسان انجام می‌شود." },
  VOICE_BRIDGE_ENABLED: { en: "Says a short filler line while the real answer is prepared, so the caller does not sit in silence.", fa: "تا آماده شدن پاسخ اصلی یک جملهٔ کوتاه می‌گوید تا تماس‌گیرنده در سکوت نماند." },
  CONTEXTS_COLLECTION_NAME: { en: "Where the approved answers are searched. An own collection keeps this content separate.", fa: "جایی که پاسخ‌های تأییدشده جست‌وجو می‌شوند. مجموعهٔ مستقل این محتوا را جدا نگه می‌دارد." },
  IVA_CONTEXTS_COLLECTION_NAME: { en: "The content searched for phone calls specifically.", fa: "محتوایی که مخصوص تماس تلفنی جست‌وجو می‌شود." },
  GUARDRAIL_COLLECTION_NAME: { en: "Examples used to spot questions the assistant must refuse.", fa: "نمونه‌هایی که برای شناختن پرسش‌های ممنوع به کار می‌روند." },
  INSTRUCTIONS_COLLECTION_NAME: { en: "Instructions pulled in for the assistant depending on the question.", fa: "دستورالعمل‌هایی که بسته به پرسش به دستیار داده می‌شوند." },
  CONTEXTS_FILTER_LLM_ENABLED: { en: "A model re-checks search results. Answers get more relevant, each turn gets slower.", fa: "یک مدل نتایج جست‌وجو را دوباره بررسی می‌کند. پاسخ مرتبط‌تر و هر نوبت کندتر می‌شود." },
  PHOENIX_PROJECT_NAME: { en: "Where this instance's traces are kept. An own project lets you judge its quality and cost alone.", fa: "جایی که ردگیری این نمونه نگه داشته می‌شود. پروژهٔ مستقل امکان سنجش جداگانهٔ کیفیت و هزینه را می‌دهد." },
  POSTGRES_DATABASE: { en: "Holds the calls and tags the panel shows. An own database keeps this instance's people separate.", fa: "تماس‌ها و برچسب‌هایی را که پنل نشان می‌دهد نگه می‌دارد. پایگاه مستقل دادهٔ افراد این نمونه را جدا نگه می‌دارد." },
  CLICKHOUSE_DATABASE: { en: "Holds analysis results before they sync to the panel. When shared, separation depends on how data is filtered.", fa: "نتایج تحلیل را پیش از رسیدن به پنل نگه می‌دارد. اگر مشترک باشد، جدایی داده به فیلتر کردن درست وابسته است." },
  KAFKA_CALL_TOPIC: { en: "The stream of finished calls waiting for analysis.", fa: "جریان تماس‌های پایان‌یافته که منتظر تحلیل‌اند." },
  KAFKA_TELC_CALL_TOPIC: { en: "The stream of telecom call records read by this instance's analytics.", fa: "جریان سوابق تماس مخابراتی که تحلیل این نمونه آن را می‌خواند." },
  KAFKA_CALL_ASR_TOPIC: { en: "The stream of calls after transcription.", fa: "جریان تماس‌ها پس از تبدیل به متن." },
  KAFKA_IVA_TOPIC: { en: "The stream of phone assistant sessions read by analytics.", fa: "جریان جلسه‌های دستیار تلفنی که تحلیل آن را می‌خواند." },
  KAFKA_TICKET_TOPIC: { en: "The stream of tickets read by analytics.", fa: "جریان تیکت‌ها که تحلیل آن را می‌خواند." },
  MINIO_BUCKET_NAME: { en: "Where analysis files are stored.", fa: "جایی که فایل‌های تحلیل ذخیره می‌شوند." },
  MINIO_IVA_BUCKET_NAME: { en: "Where phone assistant recordings are read from. These recordings hold people's voices.", fa: "جایی که ضبط‌های دستیار تلفنی از آن خوانده می‌شوند. این ضبط‌ها صدای افراد را در خود دارند." },
  AI_AGENT: { en: "Which agent's calls this analytics stack treats as its own.", fa: "این تحلیل، تماس‌های کدام عامل را مال خود می‌داند." },
  CAMPAIGN_CODE: { en: "The identifier scores and rewards are recorded under.", fa: "شناسه‌ای که امتیازها و جایزه‌ها با آن ثبت می‌شوند." },
  CAMPAIGN_NAME: { en: "The name people see for the campaign.", fa: "نام کمپین که افراد می‌بینند." },
  CAMPAIGN_END_AT: { en: "After this date the campaign should stop, along with anything still running for it.", fa: "پس از این تاریخ کمپین و هر چیزی که برایش اجرا می‌شود باید متوقف شود." },
  SCORING_AGENT_ID: { en: "Which agent's calls earn campaign points.", fa: "تماس‌های کدام عامل امتیاز کمپین می‌گیرند." },
};

const ROLE_WHY: Record<ComponentRole, Text> = {
  voice: { en: "Handles the live call.", fa: "تماس زنده را اداره می‌کند." },
  brain: { en: "Decides and writes each answer.", fa: "هر پاسخ را تصمیم‌گیری می‌کند و می‌نویسد." },
  knowledge: { en: "Serves the approved content.", fa: "محتوای تأییدشده را ارائه می‌کند." },
  analytics: { en: "Turns calls into analytics.", fa: "تماس‌ها را به داده‌های تحلیلی تبدیل می‌کند." },
  media: { en: "Carries call audio or call events.", fa: "صدا یا رویدادهای تماس را منتقل می‌کند." },
  auth: { en: "Signs people in and issues their access tokens.", fa: "کاربران را وارد می‌کند و توکن دسترسی می‌دهد." },
  gateway: { en: "Receives and routes incoming traffic.", fa: "ترافیک ورودی را می‌گیرد و هدایت می‌کند." },
  cache: { en: "Keeps short-lived data for fast reads.", fa: "دادهٔ کوتاه‌مدت را برای خواندن سریع نگه می‌دارد." },
  ui: { en: "The screen people use.", fa: "صفحه‌ای که افراد با آن کار می‌کنند." },
  other: { en: "A supporting service of this instance.", fa: "سرویس پشتیبان این نمونه." },
};

const PART_WHY: Record<string, Text> = {
  "chatbot-iva-agent": { en: "Joins each call and runs listening, turn-taking, speech-to-text and text-to-speech.", fa: "به هر تماس می‌پیوندد و شنیدن، نوبت‌گیری، گفتار به نوشتار و نوشتار به گفتار را اجرا می‌کند." },
  egress: { en: "Records the caller and the assistant to storage.", fa: "صدای تماس‌گیرنده و دستیار را در فضای ذخیره ضبط می‌کند." },
  websocall: { en: "Connects calls over the web instead of a phone line.", fa: "تماس را به‌جای خط تلفن از طریق وب برقرار می‌کند." },
  "websocall-ui": { en: "The web page for placing those calls.", fa: "صفحهٔ وب برای برقراری این تماس‌ها." },
  vector: { en: "Moves call events into the analytics database.", fa: "رویدادهای تماس را به پایگاه دادهٔ تحلیلی می‌برد." },
  synapse: { en: "Provides extra context to the agents.", fa: "زمینهٔ بیشتری به عامل‌ها می‌دهد." },
  aiva: { en: "The AIVA brain: guardrails, intent and the main answer agent run side by side on each turn.", fa: "مغز AIVA: گاردریل، تشخیص نیت و عامل اصلی پاسخ در هر نوبت هم‌زمان اجرا می‌شوند." },
  "aiva-poll": { en: "The AIVA build that runs spoken surveys.", fa: "نسخهٔ AIVA برای اجرای نظرسنجی گفتاری." },
  "adcs-chatbot": { en: "The ADCS chat brain, an older path than AIVA.", fa: "مغز چت ADCS، مسیری قدیمی‌تر از AIVA." },
  "aiva-knowledgebase": { en: "Manages the content AIVA searches.", fa: "محتوایی را که AIVA جست‌وجو می‌کند مدیریت می‌کند." },
  "adcs-kb": { en: "Manages knowledge base content for ADCS.", fa: "محتوای پایگاه دانش ADCS را مدیریت می‌کند." },
  grogu: { en: "Reads call records, fetches audio, transcribes it and stores the result.", fa: "سوابق تماس را می‌خواند، صدا را می‌گیرد، متن می‌سازد و نتیجه را ذخیره می‌کند." },
  "coa-api": { en: "Serves the analytics panel and syncs analysis results into it.", fa: "پنل تحلیل را ارائه می‌کند و نتایج تحلیل را به آن همگام می‌کند." },
  "coa-ai": { en: "The engine that analyses calls.", fa: "موتوری که تماس‌ها را تحلیل می‌کند." },
  "coa-api-archive-old-calls": { en: "Archives old calls, then removes them from the live tables.", fa: "تماس‌های قدیمی را بایگانی و از جدول‌های اصلی حذف می‌کند." },
  "coa-scoring": { en: "Scores calls and runs rewards for the campaign.", fa: "تماس‌ها را امتیاز می‌دهد و جایزه‌های کمپین را اجرا می‌کند." },
  envoy: { en: "The gateway in front of this instance's services.", fa: "درگاه جلوی سرویس‌های این نمونه." },
  ratelimit: { en: "Limits how many requests get through.", fa: "تعداد درخواست‌های مجاز را محدود می‌کند." },
};

export const partWhy = (lang: Lang, family: string, role: ComponentRole): string => (PART_WHY[family] ?? ROLE_WHY[role])[lang];
export const settingWhy = (lang: Lang, key: string): string | undefined => SETTING_WHY[key]?.[lang];

/** What each part of the Raya scoring service does, from its README. Keyed by the part's own name. */
const SCORING_PART: [string, Text][] = [
  ["campaign-events", { en: "One-shot job for end-of-campaign surveys and inactivity follow-ups.", fa: "کار یک‌باره برای نظرسنجی پایان کمپین و پیگیری عدم فعالیت." }],
  ["maintenance", { en: "One-shot cleanup of old finished sync logs.", fa: "پاک‌سازی یک‌باره گزارش‌های همگام‌سازی قدیمی." }],
  ["sms-worker", { en: "Sends the queued Persian SMS messages.", fa: "پیامک‌های فارسی صف‌شده را می‌فرستد." }],
  ["syncer", { en: "Keeps importing analysed calls from ClickHouse and scoring them.", fa: "تماس‌های تحلیل‌شده را از ClickHouse می‌گیرد و امتیاز می‌دهد." }],
  ["api", { en: "Serves rankings, records survey callbacks and finalizes winners.", fa: "رتبه‌ها را ارائه می‌کند، بازخورد نظرسنجی را ثبت می‌کند و برندگان را نهایی می‌کند." }],
];

export const scoringPartWhy = (lang: Lang, name: string): string | undefined =>
  SCORING_PART.find(([suffix]) => name.endsWith(suffix))?.[1][lang];
