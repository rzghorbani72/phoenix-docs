import { describe, expect, it } from "vitest";
import { DOC_INDEX, md, plain, resolveHref, type LinkCtx } from "./md";

const docs = new Map([
  ["ai_learning_guide_fa.html", "docs/technical/AI_LEARNING_GUIDE_FA.html"],
  ["product_dossier_fa.pdf", "docs/product-management/PRODUCT_DOSSIER_FA.pdf"],
  ["start_here_fa.html", "docs/product-management/START_HERE_FA.html"],
  ["hr - meet uat agreement - fit-gap mvp.csv", "docs/requirements/HR - meet UAT agreement - Fit-Gap MVP.csv"],
]);
const ctx: LinkCtx = {
  steps: new Set(["b-react", "v-turn", "gemma-twin"]),
  models: new Set(["gemma-4-31b", "gemma-twin"]),
  lanes: new Set(["brain", "kb"]),
  docs,
  depth: 0,
};
const deep: LinkCtx = { ...ctx, depth: 1 };
const r = (h: string, c: LinkCtx = ctx) => resolveHref(h, c);

describe("resolveHref", () => {
  it("keeps external links external", () => {
    expect(r("https://example.com/a?b=1")).toEqual({ href: "https://example.com/a?b=1", external: true });
    expect(r("mailto:a@b.c")).toEqual({ href: "mailto:a@b.c", external: true });
  });
  it("passes app routes through", () => {
    expect(r("#/step/b-react")).toEqual({ href: "#/step/b-react", external: false });
  });
  it("maps lane anchors and the index page", () => {
    expect(r("index.html#lane-brain")).toEqual({ href: "#/map/lane/brain", external: false });
    expect(r("../index.html#lane-kb", deep)).toEqual({ href: "#/map/lane/kb", external: false });
    expect(r("#lane-brain")).toEqual({ href: "#/map/lane/brain", external: false });
    expect(r("index.html")).toEqual({ href: "#/map", external: false });
    expect(r("index.html#lane-nope")).toEqual({ href: "#/map", external: false });
  });
  it("maps step pages in every folder form", () => {
    for (const h of ["b-react.html", "steps/b-react.html", "../steps/b-react.html", "../../en/steps/b-react.html"])
      expect(r(h, deep)).toEqual({ href: "#/step/b-react", external: false });
  });
  it("maps model pages, using the folder to disambiguate", () => {
    expect(r("models/gemma-4-31b.html")).toEqual({ href: "#/model/gemma-4-31b", external: false });
    expect(r("gemma-4-31b.html", deep)).toEqual({ href: "#/model/gemma-4-31b", external: false });
    expect(r("models/gemma-twin.html")).toEqual({ href: "#/model/gemma-twin", external: false });
    expect(r("steps/gemma-twin.html")).toEqual({ href: "#/step/gemma-twin", external: false });
  });
  it("maps the old top-level pages to views", () => {
    for (const p of ["models", "risks", "guide", "docs"]) expect(r(`${p}.html`)).toEqual({ href: `#/${p}`, external: false });
    expect(r("../risks.html", deep)).toEqual({ href: "#/risks", external: false });
  });
  it("maps document links of any old layout to docs/<folder>/<file>", () => {
    const guide = { href: "docs/technical/AI_LEARNING_GUIDE_FA.html", external: true };
    expect(r("../../AI_LEARNING_GUIDE_FA.html")).toEqual(guide);
    expect(r("../../../product-management/AI_LEARNING_GUIDE_FA.html", deep)).toEqual(guide);
    expect(r("docs/technical/AI_LEARNING_GUIDE_FA.html")).toEqual(guide);
    expect(r("../../../product-management/START_HERE_FA.html#map")).toEqual({ href: "docs/product-management/START_HERE_FA.html#map", external: true });
    expect(r("product_dossier_fa.pdf")).toEqual({ href: "docs/product-management/PRODUCT_DOSSIER_FA.pdf", external: true });
  });
  it("URL-encodes document paths with spaces", () => {
    expect(r("../requirements/HR%20-%20meet%20UAT%20agreement%20-%20Fit-Gap%20MVP.csv").href)
      .toBe("docs/requirements/HR%20-%20meet%20UAT%20agreement%20-%20Fit-Gap%20MVP.csv");
  });
  it("falls back to a path relative to the app for unknown files", () => {
    expect(r("../../docs/other/NEW.html")).toEqual({ href: "docs/other/NEW.html", external: true });
    expect(r("../unknown.txt", deep)).toEqual({ href: "unknown.txt", external: true });
  });
  it("uses the generated manifest by default", () => {
    expect(DOC_INDEX.size).toBeGreaterThan(0);
    const { docs: _omit, ...noDocs } = ctx;
    expect(r("../../AI_LEARNING_GUIDE_FA.html", noDocs).href).toBe(DOC_INDEX.get("ai_learning_guide_fa.html"));
  });
});

describe("md", () => {
  it("escapes HTML", () => {
    expect(md("<b>a & b</b>", ctx)).toBe("&lt;b&gt;a &amp; b&lt;/b&gt;");
  });
  it("renders code and keeps markup inside it literal", () => {
    expect(md("run `npm run dev`", ctx)).toBe("run <code>npm run dev</code>");
    expect(md("`**kwargs` and **bold**", ctx)).toBe("<code>**kwargs</code> and <strong>bold</strong>");
    expect(md("`[a](b-react.html)`", ctx)).toBe("<code>[a](b-react.html)</code>");
    expect(md("`<T>`", ctx)).toBe("<code>&lt;T&gt;</code>");
  });
  it("renders bold", () => {
    expect(md("a **b** c", ctx)).toBe("a <strong>b</strong> c");
  });
  it("renders internal links in the same tab", () => {
    expect(md("see [ReAct](steps/b-react.html)", ctx)).toBe('see <a href="#/step/b-react">ReAct</a>');
  });
  it("renders document and web links in a new tab", () => {
    expect(md("[guide](../../AI_LEARNING_GUIDE_FA.html)", ctx))
      .toBe('<a href="docs/technical/AI_LEARNING_GUIDE_FA.html" target="_blank" rel="noopener">guide</a>');
    expect(md("[q](https://x.io/?a=1&b=2)", ctx))
      .toBe('<a href="https://x.io/?a=1&amp;b=2" target="_blank" rel="noopener">q</a>');
  });
  it("renders code and bold inside link labels", () => {
    expect(md("[`b-react`](b-react.html)", ctx)).toBe('<a href="#/step/b-react"><code>b-react</code></a>');
    expect(md("[**x**](risks.html)", ctx)).toBe('<a href="#/risks"><strong>x</strong></a>');
  });
  it("does not let an href break out of its attribute", () => {
    expect(md('[x](a"onmouseover=alert(1).html)', ctx)).not.toContain('"onmouseover');
  });
  it("marks inferred claims in English and Persian", () => {
    expect(md("fast (inferred)", ctx)).toBe('fast <span class="inf">(inferred)</span>');
    expect(md("سریع (استنباطی)", ctx)).toBe('سریع <span class="inf">(استنباطی)</span>');
    expect(md("سریع (استنباط)", ctx)).toBe('سریع <span class="inf">(استنباط)</span>');
  });
});

describe("plain", () => {
  it("strips markup", () => {
    expect(plain("`a` **b** [c](d.html)")).toBe("a b c");
  });
});
