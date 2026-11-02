import type { Data } from "./types";

export type SearchKind = "step" | "model" | "guide" | "risk";

export interface SearchEntry {
  /** What sort of thing this is. */
  type: SearchKind;
  /** Short tag shown in the palette: lane step number (e.g. B10), MODEL, GUIDE or RISK. */
  kind: string;
  label: string;
  sub: string;
  /** Lower-cased text the query is matched against. */
  hay: string;
  /** Hash route to open. */
  to: string;
}

const strip = (s: string) => s.replace(/[`*]/g, "");

/** Flat index over steps (in lane order), model pages, guide sections and risks. */
export function buildIndex(d: Data): SearchEntry[] {
  const out: SearchEntry[] = [];
  for (const lane of d.lanes)
    lane.steps.forEach((id, i) => {
      const s = d.steps[id];
      if (!s) return;
      out.push({
        type: "step",
        kind: `${lane.prefix}${i + 1}`,
        label: strip(s.title),
        sub: strip(s.chip ?? ""),
        hay: `${s.title} ${s.chip ?? ""} ${s.summary} ${JSON.stringify(s.sections)}`.toLowerCase(),
        to: `#/step/${id}`,
      });
    });
  for (const c of d.models.cards)
    if (c.id)
      out.push({
        type: "model",
        kind: "MODEL",
        label: strip(c.name),
        sub: strip(c.size),
        hay: `${c.name} ${c.size} ${JSON.stringify(d.models.pages[c.id] ?? "")}`.toLowerCase(),
        to: `#/model/${c.id}`,
      });
  d.guide?.sections.forEach(([h, b], i) =>
    out.push({ type: "guide", kind: "GUIDE", label: strip(h), sub: "", hay: `${h} ${JSON.stringify(b)}`.toLowerCase(), to: `#/guide/${i + 1}` }),
  );
  d.risks.items.forEach((r) =>
    out.push({ type: "risk", kind: "RISK", label: strip(r.title), sub: strip(r.why), hay: `${r.title} ${r.why}`.toLowerCase(), to: "#/risks" }),
  );
  return out;
}

export const terms = (q: string) => q.toLowerCase().split(/\s+/).filter(Boolean);

/**
 * Score one entry: every term must appear somewhere (AND); each term found in the label adds 5,
 * each term found anywhere adds 1. Returns 0 when any term is missing.
 */
export function score(e: SearchEntry, ts: string[]): number {
  let s = 0;
  const label = e.label.toLowerCase();
  for (const t of ts) {
    if (!e.hay.includes(t) && !label.includes(t)) return 0;
    s += 1 + (label.includes(t) ? 5 : 0);
  }
  return s;
}

/** Best matches first (stable for equal scores); an empty query returns the first `empty` entries. */
export function search(index: SearchEntry[], q: string, limit = 30, empty = 12): SearchEntry[] {
  const ts = terms(q);
  if (!ts.length) return index.slice(0, empty);
  return index
    .map((x, i) => ({ x, i, s: score(x, ts) }))
    .filter((h) => h.s > 0)
    .sort((a, b) => b.s - a.s || a.i - b.i)
    .slice(0, limit)
    .map((h) => h.x);
}
