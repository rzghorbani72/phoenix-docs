import type { Instance } from "../../lib/instanceTypes";
import type { PipelineStageId, StageDetail } from "../../lib/instances";
import type { Lang } from "./i18n";
import { settingLabel } from "./i18n";

export interface Highlight { label: string; value: string }

type Row = { label?: { en: string; fa: string }; key?: string; keys?: string[]; sep?: string };

const L = (en: string, fa: string) => ({ en, fa });

/** The few values that say what a step is actually set to, in the order a reader looks for them. */
const ROWS: Record<PipelineStageId, Row[]> = {
  call: [
    { label: L("Speech to text", "گفتار به نوشتار"), keys: ["AGENT_STT_CLIENT", "AGENT_STT_MODEL"], sep: " / " },
    { label: L("Text to speech", "نوشتار به گفتار"), keys: ["AGENT_TTS_MODEL", "AGENT_TTS_SPEED"], sep: " × " },
    { key: "AGENT_TURN_MODEL" },
    { label: L("Wait after caller stops (s)", "انتظار پس از سکوت (ثانیه)"), keys: ["AGENT_MIN_ENDPOINTING_DELAY", "AGENT_MAX_ENDPOINTING_DELAY"], sep: " – " },
    { key: "AGENT_VAD_MIN_SILENCE_DURATION" },
  ],
  brain: [
    { key: "AGENT_LLM_MODEL" },
    { key: "AGENT_ENABLED_TOOLS" },
    { key: "CONTEXTS_COLLECTION_NAME" },
    { key: "GUARDRAIL_COLLECTION_NAME" },
    { key: "INSTRUCTIONS_COLLECTION_NAME" },
  ],
  kb: [
    { key: "CONTEXTS_COLLECTION_NAME" },
    { key: "IVA_CONTEXTS_COLLECTION_NAME" },
  ],
  analytics: [
    { key: "CAMPAIGN_NAME" },
    { key: "KAFKA_CALL_TOPIC" },
    { key: "CLICKHOUSE_DATABASE" },
    { key: "POSTGRES_DATABASE" },
    { key: "MINIO_BUCKET_NAME" },
  ],
  ops: [
    { key: "AGENT_APM_TRANSACTION_SAMPLE_RATE" },
    { key: "PHOENIX_PROJECT_NAME" },
  ],
};

const lookup = (inst: Instance, key: string): string | undefined => {
  for (const g of Object.values(inst.config)) if (g[key] !== undefined) return g[key];
  return undefined;
};

const listTools = (raw: string): string => {
  try { return (JSON.parse(raw) as string[]).join(", "); } catch { return raw; }
};

/** Up to `max` real values of one step. Rows with no value for this instance are skipped, never invented. */
export function highlights(inst: Instance, detail: StageDetail, lang: Lang, max = 5): Highlight[] {
  const out: Highlight[] = [];
  for (const row of ROWS[detail.stage.id]) {
    const keys = row.keys ?? (row.key ? [row.key] : []);
    let value = keys.map((k) => lookup(inst, k)).filter((v): v is string => !!v).join(row.sep ?? "");
    if (!value) continue;
    if (row.key === "AGENT_ENABLED_TOOLS") value = listTools(value);
    out.push({ label: row.label?.[lang] ?? settingLabel(lang, keys[0]), value });
  }
  if (detail.stage.id === "ops" && inst.deps.length) out.push({ label: lang === "fa" ? "سرویس‌های مشترک" : "Shared services", value: inst.deps.join(", ") });
  return out.slice(0, max);
}
