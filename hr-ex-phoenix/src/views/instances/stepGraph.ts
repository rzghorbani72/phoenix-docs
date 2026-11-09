import type { Instance, InstanceComponent } from "../../lib/instanceTypes";
import type { PipelineStageId, StageDetail } from "../../lib/instances";

export type Text = { en: string; fa: string };

export interface GraphNode {
  id: string;
  title: Text;
  /** The real value for this instance, shown as an identifier. */
  value?: string;
  /** The deployed part behind this node, when there is one. */
  part?: InstanceComponent;
  /** A setting or a fixed point of the flow, not a deployed part. */
  kind: "part" | "setting" | "actor";
}

export interface GraphLayer {
  /** What moves from the layer above into this one. */
  flow?: Text;
  nodes: GraphNode[];
}

const t = (en: string, fa: string): Text => ({ en, fa });

const PART_TITLE: Record<string, Text> = {
  "chatbot-iva-agent": t("Voice agent", "عامل صوتی"),
  websocall: t("Web call service", "سرویس تماس وب"),
  "websocall-ui": t("Web call page", "صفحهٔ تماس وب"),
  egress: t("Call recording", "ضبط تماس"),
  vector: t("Event forwarder", "ارسال رویدادها"),
  synapse: t("Agent context", "زمینهٔ عامل"),
  aiva: t("AIVA brain", "مغز AIVA"),
  "aiva-poll": t("AIVA survey brain", "مغز نظرسنجی AIVA"),
  "adcs-chatbot": t("ADCS brain", "مغز ADCS"),
  "aiva-knowledgebase": t("Knowledge service", "سرویس دانش"),
  "adcs-kb": t("Knowledge service", "سرویس دانش"),
  grogu: t("Call intake and transcription", "دریافت و متن تماس"),
  "coa-ai": t("Call analysis engine", "موتور تحلیل تماس"),
  "coa-scoring": t("Campaign scoring", "امتیازدهی کمپین"),
  "coa-api-archive-old-calls": t("Old call archive", "بایگانی تماس‌های قدیمی"),
  envoy: t("Gateway", "درگاه"),
  ratelimit: t("Rate limiter", "محدودکنندهٔ نرخ"),
  redis: t("Cache", "کش"),
  "adcs-auth": t("Sign-in", "ورود"),
  nginx: t("Web server", "وب‌سرور"),
};

const isWorker = (c: InstanceComponent) => /worker/.test(c.name);
const isSync = (c: InstanceComponent) => /sync|cache/.test(c.name);

/** Parts sharing a title also say their own name, or several boxes would read the same. */
function partNode(c: InstanceComponent, siblings: InstanceComponent[]): GraphNode {
  const title = PART_TITLE[c.family];
  const shared = siblings.filter((o) => o.family === c.family).length > 1;
  return {
    id: c.name, kind: "part", part: c, value: c.version,
    title: !title ? t(c.name, c.name) : shared ? t(`${title.en} · ${c.name}`, `${title.fa} · ${c.name}`) : title,
  };
}

/** Removes what it takes from the pool, so a part can never land in two places or none. */
function pool(detail: StageDetail) {
  let rest = [...detail.components];
  return {
    take(match: (c: InstanceComponent) => boolean): GraphNode[] {
      const hit = rest.filter(match);
      rest = rest.filter((c) => !match(c));
      return hit.map((c) => partNode(c, detail.components));
    },
    rest: () => rest.map((c) => partNode(c, detail.components)),
  };
}

const setting = (inst: Instance, title: Text, key: string): GraphNode[] => {
  const groups = Object.values(inst.config);
  const value = groups.map((g) => g[key]).find((v) => v !== undefined);
  return value === undefined ? [] : [{ id: key, kind: "setting", title, value }];
};

const actor = (id: string, title: Text): GraphNode => ({ id, kind: "actor", title });

const tools = (raw: string | undefined): string | undefined => {
  if (!raw) return raw;
  try { return (JSON.parse(raw) as string[]).join(", ") || undefined; } catch { return raw; }
};

/** Joins two values into one line, for settings that only mean something together. */
function pair(inst: Instance, title: Text, id: string, first: string, second: string, sep: string): GraphNode[] {
  const v = inst.config.voice;
  const value = [v[first], v[second]].filter(Boolean).join(sep);
  return value ? [{ id, kind: "setting", title, value }] : [];
}

const callLayers = (inst: Instance, p: ReturnType<typeof pool>): GraphLayer[] => {
  const brain = inst.brain ? [actor("brain", PART_TITLE[inst.brain.family] ?? t(inst.brain.family, inst.brain.family))] : [];
  return [
    { nodes: [actor("caller", t("Caller", "تماس‌گیرنده")), ...p.take((c) => c.family === "websocall-ui")] },
    { flow: t("audio", "صدا"), nodes: p.take((c) => c.family === "chatbot-iva-agent" || c.family === "websocall") },
    { flow: t("listening", "شنیدن"), nodes: [
      ...setting(inst, t("Silence that ends a phrase (s)", "سکوت پایان عبارت (ثانیه)"), "AGENT_VAD_MIN_SILENCE_DURATION"),
      ...pair(inst, t("Speech to text", "گفتار به نوشتار"), "stt", "AGENT_STT_CLIENT", "AGENT_STT_MODEL", " / "),
      ...setting(inst, t("End of turn", "پایان نوبت"), "AGENT_TURN_MODEL"),
      ...pair(inst, t("Wait after caller stops (s)", "انتظار پس از سکوت (ثانیه)"), "wait", "AGENT_MIN_ENDPOINTING_DELAY", "AGENT_MAX_ENDPOINTING_DELAY", " to "),
    ] },
    { flow: t("caller's words", "گفتهٔ تماس‌گیرنده"), nodes: brain },
    { flow: t("answer", "پاسخ"), nodes: pair(inst, t("Text to speech", "نوشتار به گفتار"), "tts", "AGENT_TTS_MODEL", "AGENT_TTS_SPEED", " × ") },
    { flow: t("after the call", "پس از تماس"), nodes: [
      ...p.take((c) => c.family === "egress" || c.family === "vector"),
      ...setting(inst, t("Call summary topic", "تاپیک خلاصهٔ تماس"), "AGENT_KAFKA_TOPIC"),
    ] },
  ];
};

const brainLayers = (inst: Instance, p: ReturnType<typeof pool>): GraphLayer[] => {
  const hasVoice = inst.components.some((c) => c.role === "voice");
  const toolList = tools(inst.config.brain.AGENT_ENABLED_TOOLS);
  return [
    { nodes: [hasVoice ? actor("agent", PART_TITLE["chatbot-iva-agent"]) : actor("user", t("User message", "پیام کاربر"))] },
    { flow: t("each turn", "هر نوبت"), nodes: p.take((c) => !isWorker(c)) },
    { flow: t("checks and looks up", "بررسی و جست‌وجو"), nodes: [
      ...setting(inst, t("Guardrails", "گاردریل‌ها"), "GUARDRAIL_COLLECTION_NAME"),
      ...setting(inst, t("Knowledge", "دانش"), "CONTEXTS_COLLECTION_NAME"),
      ...setting(inst, t("Instructions", "دستورالعمل‌ها"), "INSTRUCTIONS_COLLECTION_NAME"),
      ...setting(inst, t("Filler line while waiting", "جملهٔ میانی هنگام انتظار"), "VOICE_BRIDGE_ENABLED"),
    ] },
    { flow: t("writes the answer", "نوشتن پاسخ"), nodes: [
      ...setting(inst, t("Language model", "مدل زبانی"), "AGENT_LLM_MODEL"),
      ...(toolList ? [{ id: "tools", kind: "setting" as const, title: t("Tools", "ابزارها"), value: toolList }] : []),
    ] },
    { flow: t("in the background", "در پس‌زمینه"), nodes: [
      ...p.take(isWorker),
      ...setting(inst, t("Trace project", "پروژهٔ ردگیری"), "PHOENIX_PROJECT_NAME"),
    ] },
  ];
};

const kbLayers = (inst: Instance, p: ReturnType<typeof pool>): GraphLayer[] => [
  { nodes: [actor("content", t("Approved content", "محتوای تأییدشده"))] },
  { flow: t("edited and imported", "ویرایش و ورود"), nodes: p.take((c) => !isWorker(c)) },
  { flow: t("indexed", "نمایه‌سازی"), nodes: p.take(isWorker) },
  { flow: t("stored in", "ذخیره در"), nodes: [
    ...setting(inst, t("Knowledge", "دانش"), "CONTEXTS_COLLECTION_NAME"),
    ...setting(inst, t("Phone knowledge", "دانش تلفنی"), "IVA_CONTEXTS_COLLECTION_NAME"),
  ] },
  { flow: t("searched on each question", "جست‌وجو در هر پرسش"), nodes: inst.brain ? [actor("brain", PART_TITLE[inst.brain.family] ?? t(inst.brain.family, inst.brain.family))] : [] },
];

const analyticsLayers = (inst: Instance, p: ReturnType<typeof pool>): GraphLayer[] => [
  { nodes: [
    ...setting(inst, t("Calls", "تماس‌ها"), "KAFKA_CALL_TOPIC"),
    ...setting(inst, t("Telecom calls", "تماس‌های مخابراتی"), "KAFKA_TELC_CALL_TOPIC"),
    ...setting(inst, t("Assistant sessions", "جلسه‌های دستیار"), "KAFKA_IVA_TOPIC"),
    ...setting(inst, t("Tickets", "تیکت‌ها"), "KAFKA_TICKET_TOPIC"),
    ...setting(inst, t("Campaign", "کمپین"), "CAMPAIGN_NAME"),
  ] },
  { flow: t("taken in", "دریافت"), nodes: p.take((c) => c.family === "grogu") },
  { flow: t("transcripts", "متن تماس"), nodes: setting(inst, t("Transcripts topic", "تاپیک متن تماس"), "KAFKA_CALL_ASR_TOPIC") },
  { flow: t("analysed", "تحلیل"), nodes: p.take((c) => c.family === "coa-ai" || c.family === "coa-scoring") },
  { flow: t("results", "نتایج"), nodes: [
    ...setting(inst, t("Analytics database", "پایگاه دادهٔ تحلیلی"), "CLICKHOUSE_DATABASE"),
    ...setting(inst, t("Analysis files", "فایل‌های تحلیل"), "MINIO_BUCKET_NAME"),
    ...setting(inst, t("Assistant recordings", "ضبط‌های دستیار"), "MINIO_IVA_BUCKET_NAME"),
  ] },
  { flow: t("kept in step", "همگام‌سازی"), nodes: p.take(isSync) },
  { flow: t("stored for the panel", "ذخیره برای پنل"), nodes: setting(inst, t("Main database", "پایگاه دادهٔ اصلی"), "POSTGRES_DATABASE") },
  { flow: t("shown to people", "نمایش به افراد"), nodes: p.take(() => true) },
];

const opsLayers = (inst: Instance, p: ReturnType<typeof pool>): GraphLayer[] => [
  { nodes: [actor("traffic", t("Incoming traffic", "ترافیک ورودی"))] },
  { flow: t("enters through", "ورود از"), nodes: p.take((c) => c.role === "gateway") },
  { flow: t("signs people in", "ورود کاربران"), nodes: p.take((c) => c.role === "auth") },
  { flow: t("screens and helpers", "صفحه‌ها و کمکی‌ها"), nodes: p.take((c) => c.role === "ui" || c.role === "cache") },
  { flow: t("shared models and services", "مدل‌ها و سرویس‌های مشترک"), nodes: inst.deps.map((d) => ({ id: d, kind: "setting" as const, title: t("Shared service", "سرویس مشترک"), value: d })) },
  { flow: t("watched by", "پایش با"), nodes: [
    ...setting(inst, t("Share of calls traced", "سهم تماس‌های ردگیری‌شده"), "AGENT_APM_TRANSACTION_SAMPLE_RATE"),
    ...setting(inst, t("Trace project", "پروژهٔ ردگیری"), "PHOENIX_PROJECT_NAME"),
  ] },
];

const BUILDERS: Record<PipelineStageId, (inst: Instance, p: ReturnType<typeof pool>) => GraphLayer[]> = {
  call: callLayers, brain: brainLayers, kb: kbLayers, analytics: analyticsLayers, ops: opsLayers,
};

/**
 * One step of one instance as a flow, built only from what ops states for it. A layer with
 * nothing to show is dropped, and any part no layer claims is listed at the end.
 */
export function stepGraph(inst: Instance, detail: StageDetail): GraphLayer[] {
  const p = pool(detail);
  const layers = BUILDERS[detail.stage.id](inst, p);
  const rest = p.rest();
  if (rest.length) layers.push({ flow: t("also part of this step", "بخش‌های دیگر این مرحله"), nodes: rest });
  return layers.filter((l) => l.nodes.length);
}
