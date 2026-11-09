import type { Instance, InstanceCategory } from "../../lib/instanceTypes";
import { INSTANCES, isStopped, type PipelineStageId, type StageDetail } from "../../lib/instances";
import { LANE_COLOR } from "../../components/map/shared";
import type { InstanceComponent } from "../../lib/instanceTypes";
import { T, type Lang } from "./i18n";

export const ALL = INSTANCES.instances;

export type StepWord = "on" | "partly" | "off" | "none";
/** The one word a step card leads with, and how it is coloured. */
export function stepLook(detail: StageDetail): { word: StepWord; tone: "ok" | "warn" | "off" } {
  if (detail.stage.state === "none") return { word: "none", tone: "off" };
  const total = detail.components.length;
  const stopped = detail.components.filter(isStopped).length;
  if (total > 0 && stopped === total) return { word: "off", tone: "off" };
  if (stopped > 0) return { word: "partly", tone: "warn" };
  return { word: "on", tone: "ok" };
}

/** The one word a step shows for its state. */
export function stepWordText(word: StepWord, lang: Lang): string {
  const s = T(lang);
  return { none: s.stageNone, off: s.stepWordOff, partly: s.stepWordPartly, on: s.stepWordOn }[word];
}

export function replicaText(c: InstanceComponent, lang: Lang): string {
  const s = T(lang);
  if (c.neverRuns) return s.neverRuns;
  if (c.schedule) return `${s.scheduledJob}: ${c.schedule}`;
  if (c.autoscaled) return s.autoscaled;
  if (c.replicas === null) return s.chartDefault;
  return c.replicas === 0 ? s.stageOff : `${s.statReplicas}: ${c.replicas}`;
}
/** Same colours and letters as the lanes of the main map. */
export const STAGE_LOOK: Record<PipelineStageId, { color: string; letter: string }> = {
  call: { color: LANE_COLOR.teal, letter: "V" }, brain: { color: LANE_COLOR.violet, letter: "B" }, kb: { color: LANE_COLOR.orange, letter: "K" },
  analytics: { color: LANE_COLOR.pink, letter: "A" }, ops: { color: LANE_COLOR.blue, letter: "P" },
};
export const CATEGORIES: InstanceCategory[] = ["panel", "phone", "campaign", "chat", "tools", "unclassified"];

/** replicas null is the chart default, which is on; only an explicit 0 is off. */
export const partsOn = (i: Instance): number => i.components.filter((c) => !isStopped(c)).length;
/** Settings holding human text rather than an identifier. */
export const isProse = (key: string): boolean => key === "AGENT_GREETING_MESSAGE" || key === "CAMPAIGN_NAME";
