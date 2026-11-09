import type { Status } from "../../lib/types";

export const LANE_COLOR: Record<string, string> = {
  teal: "var(--c-teal)", violet: "var(--c-violet)", orange: "var(--c-orange)", pink: "var(--c-pink)",
  cyan: "var(--c-cyan)", blue: "var(--c-blue)", green: "var(--c-green)",
};

/** Solid colours for the minimap (SVG fill attributes cannot use CSS variables). */
export const HEX: Record<string, string> = { teal: "#14b8a6", violet: "#8b5cf6", orange: "#f97316", pink: "#ec4899", cyan: "#06b6d4", blue: "#3b82f6", green: "#22c55e" };

export const STATUSES: Status[] = ["live", "off", "notdeployed", "external", "unknown"];

export interface MapFilters { model: string; statuses: Set<Status>; query: string; cross: boolean; /** Instance id; "" shows the general pipeline. */ instance: string }

/** Hand-off points between lanes; the label explains what crosses. */
export const CROSS: { from: string; to: string; en: string; fa: string }[] = [
  { from: "v-aiva", to: "b-setup", en: "each user turn", fa: "هر نوبت کاربر" },
  { from: "b-react", to: "v-tts", en: "streamed answer → TTS", fa: "پاسخ استریم → TTS" },
  { from: "b-retrieve", to: "k-search", en: "embed + search", fa: "embedding + جست‌وجو" },
  { from: "k-carry", to: "b-react", en: "approved contexts", fa: "زمینه‌های تأییدشده" },
  { from: "b-setup", to: "m-history", en: "history · memory", fa: "سابقه · حافظه" },
  { from: "v-summary", to: "a-ingest", en: "Kafka summary + .ogg", fa: "خلاصه Kafka + .ogg" },
  { from: "f-aiva", to: "b-setup", en: "aiva is built on agentlib", fa: "aiva روی agentlib ساخته شده" },
];
