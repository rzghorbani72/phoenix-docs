import enJson from "../data/en.json";
import faJson from "../data/fa.json";
import type { Data, Lane, ModelCard, Page } from "./types";

const en = enJson as unknown as Data;
const fa = faJson as unknown as Data;

const mark = <T extends object>(o: T): T => ({ ...o, fallback: true });

/** Persian falls back to English item by item, so a half-translated build still shows everything. */
function mergeFa(): Data {
  const steps: Record<string, Page> = {};
  for (const [id, s] of Object.entries(en.steps)) steps[id] = fa.steps[id] ?? mark(s);
  const faLanes = new Map(fa.lanes.map((l) => [l.id, l]));
  const lanes: Lane[] = en.lanes.map((l) => faLanes.get(l.id) ?? l);
  const hasPages = Object.keys(fa.models.pages ?? {}).length > 0;
  const pages: Record<string, Page> = {};
  for (const [id, p] of Object.entries(en.models.pages)) pages[id] = fa.models.pages?.[id] ?? mark(p);
  const models = hasPages
    ? { ...fa.models, pages }
    : { ...en.models, pages, fallback: true };
  return {
    ...fa,
    steps,
    lanes,
    models,
    guide: fa.guide ?? (en.guide ? mark(en.guide) : undefined),
    ui: { ...en.ui, ...fa.ui },
  };
}

export const DATA: Record<"en" | "fa", Data> = { en, fa: mergeFa() };

/** Which lane a step belongs to, and its 1-based number in that lane (e.g. B10). */
export function laneOf(d: Data, stepId: string): { lane: Lane; num: number } | undefined {
  for (const lane of d.lanes) {
    const i = lane.steps.indexOf(stepId);
    if (i >= 0) return { lane, num: i + 1 };
  }
  return undefined;
}

/** Model cards that list this step as a place they are used. */
export function modelsForStep(d: Data, stepId: string): ModelCard[] {
  return d.models.cards.filter((c) => c.steps?.includes(stepId));
}
