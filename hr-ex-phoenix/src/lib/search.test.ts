import { describe, expect, it } from "vitest";
import { DATA } from "./data";
import { buildIndex, score, search, terms, type SearchEntry } from "./search";

const e = (label: string, hay: string, type: SearchEntry["type"] = "step"): SearchEntry =>
  ({ type, kind: "X", label, sub: "", hay: `${label} ${hay}`.toLowerCase(), to: `#/${label}` });

describe("terms", () => {
  it("lower-cases and splits on whitespace", () => {
    expect(terms("  Voice   AGENT ")).toEqual(["voice", "agent"]);
    expect(terms("   ")).toEqual([]);
  });
});

describe("score", () => {
  it("requires every term (AND)", () => {
    const x = e("Guardrail", "checks replies for safety");
    expect(score(x, ["guardrail", "safety"])).toBeGreaterThan(0);
    expect(score(x, ["guardrail", "banana"])).toBe(0);
  });
  it("boosts terms found in the label", () => {
    const inLabel = e("Guardrail", "x");
    const inBody = e("Reply", "uses a guardrail");
    expect(score(inLabel, ["guardrail"])).toBeGreaterThan(score(inBody, ["guardrail"]));
  });
});

describe("search", () => {
  const index = [e("Alpha", "shared"), e("Beta", "shared alpha mention"), e("Gamma", "nothing")];
  it("returns the first entries for an empty query", () => {
    expect(search(index, "", 30, 2).map((x) => x.label)).toEqual(["Alpha", "Beta"]);
  });
  it("ranks label matches first and drops non-matches", () => {
    expect(search(index, "alpha").map((x) => x.label)).toEqual(["Alpha", "Beta"]);
  });
  it("applies multi-term AND", () => {
    expect(search(index, "shared mention").map((x) => x.label)).toEqual(["Beta"]);
    expect(search(index, "alpha nothing")).toEqual([]);
  });
  it("respects the limit", () => {
    expect(search(index, "shared", 1)).toHaveLength(1);
  });
});

describe("buildIndex on exported data", () => {
  for (const lang of ["en", "fa"] as const) {
    const d = DATA[lang];
    const idx = buildIndex(d);
    it(`${lang}: covers every kind with the right counts`, () => {
      const n = (t: SearchEntry["type"]) => idx.filter((x) => x.type === t).length;
      expect(n("step")).toBe(d.lanes.reduce((a, l) => a + l.steps.length, 0));
      expect(n("model")).toBe(d.models.cards.filter((c) => c.id).length);
      expect(n("guide")).toBe(d.guide?.sections.length ?? 0);
      expect(n("risk")).toBe(d.risks.items.length);
    });
    it(`${lang}: steps use lane numbering and guide entries deep-link`, () => {
      const react = idx.find((x) => x.to === "#/step/b-react");
      expect(react?.kind).toMatch(/^B\d+$/);
      expect(idx.filter((x) => x.type === "guide").map((x) => x.to)[0]).toBe("#/guide/1");
      expect(idx.every((x) => !/[`*]/.test(x.label))).toBe(true);
    });
  }
  it("finds a model by its name", () => {
    const hits = search(buildIndex(DATA.en), "gemma dedicated");
    expect(hits[0]).toMatchObject({ type: "model", to: "#/model/gemma-4-31b-dedicated" });
  });
  it("finds Persian text in the Persian index", () => {
    const hits = search(buildIndex(DATA.fa), "استخر");
    expect(hits.length).toBeGreaterThan(0);
  });
});
