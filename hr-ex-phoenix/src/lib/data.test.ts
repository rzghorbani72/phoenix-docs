import { describe, expect, it } from "vitest";
import { DATA, laneOf, mergeFa, modelsForStep } from "./data";
import type { Data, Page } from "./types";

const page = (title: string): Page => ({ title, status: "live", summary: `${title} summary`, facts: [], sections: [] });

function fixture(lang: "en" | "fa", over: Partial<Data> = {}): Data {
  return {
    lang,
    dir: lang === "fa" ? "rtl" : "ltr",
    ui: { brand: `${lang} brand`, nav_map: `${lang} map`, only_en: "only en" },
    meta: { title: "t", title_plain: "t", lede: "", source: "", footer: "" },
    lanes: [
      { id: "a", prefix: "A", color: "blue", short: "", tagline: "", title: `${lang} lane a`, title_plain: "", desc: "", steps: ["s1", "s2"] },
      { id: "b", prefix: "B", color: "red", short: "", tagline: "", title: `${lang} lane b`, title_plain: "", desc: "", steps: ["s3"] },
    ],
    system_edges: [],
    key_points: [],
    steps: { s1: page(`${lang} s1`), s2: page(`${lang} s2`), s3: page(`${lang} s3`) },
    models: {
      title: `${lang} models`,
      lede: "",
      cards: [
        { id: "m1", name: "M1", size: "1B", status: "live", facts: [], steps: ["s1", "s3"] },
        { id: "m2", name: "M2", size: "2B", status: "off", facts: [], steps: ["s3"] },
        { name: "no id", size: "?", status: "unknown", facts: [] },
      ],
      sections: [],
      pages: { m1: page(`${lang} m1`), m2: page(`${lang} m2`) },
    },
    risks: { title: "r", lede: "", items: [] },
    guide: { title: `${lang} guide`, lede: "", sections: [["h", "b"]] },
    ...over,
  };
}

describe("mergeFa", () => {
  const en = fixture("en");

  it("keeps translated items and falls back to English per step, marked as fallback", () => {
    const fa = fixture("fa");
    delete (fa.steps as Record<string, Page>).s2;
    const m = mergeFa(en, fa);
    expect(m.lang).toBe("fa");
    expect(m.dir).toBe("rtl");
    expect(m.steps.s1.title).toBe("fa s1");
    expect(m.steps.s1.fallback).toBeUndefined();
    expect(m.steps.s2.title).toBe("en s2");
    expect(m.steps.s2.fallback).toBe(true);
    // The English source object is not mutated.
    expect(en.steps.s2.fallback).toBeUndefined();
  });

  it("falls back per model page and keeps Persian model metadata when some pages exist", () => {
    const fa = fixture("fa");
    delete (fa.models.pages as Record<string, Page>).m2;
    const m = mergeFa(en, fa);
    expect(m.models.title).toBe("fa models");
    expect(m.models.fallback).toBeUndefined();
    expect(m.models.pages.m1.title).toBe("fa m1");
    expect(m.models.pages.m2.title).toBe("en m2");
    expect(m.models.pages.m2.fallback).toBe(true);
  });

  it("uses the whole English models block, flagged, when Persian has no model pages", () => {
    const fa = fixture("fa");
    fa.models = { ...fa.models, pages: {} };
    const m = mergeFa(en, fa);
    expect(m.models.title).toBe("en models");
    expect(m.models.fallback).toBe(true);
    expect(Object.values(m.models.pages).every((p) => p.fallback)).toBe(true);
  });

  it("falls back to the English guide when the Persian guide is missing", () => {
    const fa = fixture("fa", { guide: undefined });
    const m = mergeFa(en, fa);
    expect(m.guide?.title).toBe("en guide");
    expect(m.guide?.fallback).toBe(true);
    expect(mergeFa(en, fixture("fa")).guide?.title).toBe("fa guide");
  });

  it("falls back per lane, keeping English lane order", () => {
    const fa = fixture("fa");
    fa.lanes = [fa.lanes[1]];
    const m = mergeFa(en, fa);
    expect(m.lanes.map((l) => l.id)).toEqual(["a", "b"]);
    expect(m.lanes[0].title).toBe("en lane a");
    expect(m.lanes[1].title).toBe("fa lane b");
  });

  it("merges UI strings with Persian winning", () => {
    const m = mergeFa(en, fixture("fa"));
    expect(m.ui.brand).toBe("fa brand");
    expect(m.ui.only_en).toBe("only en");
  });
});

describe("laneOf", () => {
  const d = fixture("en");
  it("numbers steps from 1 within their lane", () => {
    expect(laneOf(d, "s1")).toMatchObject({ lane: { id: "a" }, num: 1 });
    expect(laneOf(d, "s2")).toMatchObject({ lane: { id: "a" }, num: 2 });
    expect(laneOf(d, "s3")).toMatchObject({ lane: { id: "b" }, num: 1 });
  });
  it("returns undefined for unknown steps", () => {
    expect(laneOf(d, "nope")).toBeUndefined();
  });
});

describe("modelsForStep", () => {
  const d = fixture("en");
  it("lists every card that uses the step, in card order", () => {
    expect(modelsForStep(d, "s3").map((c) => c.id)).toEqual(["m1", "m2"]);
    expect(modelsForStep(d, "s1").map((c) => c.id)).toEqual(["m1"]);
    expect(modelsForStep(d, "s2")).toEqual([]);
  });
});

describe("exported DATA", () => {
  it("has the same steps, lanes and model pages in both languages", () => {
    expect(Object.keys(DATA.fa.steps).sort()).toEqual(Object.keys(DATA.en.steps).sort());
    expect(DATA.fa.lanes.map((l) => l.id)).toEqual(DATA.en.lanes.map((l) => l.id));
    expect(Object.keys(DATA.fa.models.pages).sort()).toEqual(Object.keys(DATA.en.models.pages).sort());
    expect(DATA.fa.dir).toBe("rtl");
    expect(DATA.en.dir).toBe("ltr");
  });

  it("every lane step resolves to a page, and B10 is the ReAct answer agent", () => {
    for (const d of [DATA.en, DATA.fa])
      for (const lane of d.lanes) for (const id of lane.steps) expect(d.steps[id], id).toBeDefined();
    const w = laneOf(DATA.en, "b-react");
    expect(w && `${w.lane.prefix}${w.num}`).toMatch(/^B\d+$/);
  });

  it("every step a model card lists is a real step", () => {
    for (const c of DATA.en.models.cards) for (const s of c.steps ?? []) expect(laneOf(DATA.en, s), `${c.id} -> ${s}`).toBeDefined();
    expect(modelsForStep(DATA.en, "b-react").map((c) => c.id)).toContain("gemma-4-31b-dedicated");
  });
});
