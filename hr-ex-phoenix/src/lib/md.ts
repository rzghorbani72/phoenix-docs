import type { Data } from "./types";
import docsManifest from "../data/docs.json";
import { docKey, docRoute, HTML_DOCS } from "../views/docs/manifest";

export interface LinkCtx {
  steps: Set<string>;
  models: Set<string>;
  /** 1 when the text came from a step/model page (kept for callers; links are resolved the same way at any depth). */
  depth: 0 | 1;
  /** Lane ids, so `index.html#lane-x` only becomes a lane route when lane x exists. */
  lanes?: Set<string>;
  /** Document file name (lower case) → path relative to the app, e.g. "docs/technical/AI_LEARNING_GUIDE_FA.html". */
  docs?: Map<string, string>;
}

interface Manifest { docs: { files: { path: string }[] }[] }

/** Every file under public/docs, by file name (the content was written for older folder layouts). */
export const DOC_INDEX: Map<string, string> = (() => {
  const m = new Map<string, string>();
  for (const e of (docsManifest as Manifest).docs) for (const f of e.files) m.set(f.path.split("/").pop()!.toLowerCase(), f.path);
  return m;
})();

export const ctxFor = (d: Data, depth: 0 | 1): LinkCtx => ({
  steps: new Set(Object.keys(d.steps)),
  models: new Set(Object.keys(d.models.pages)),
  lanes: new Set(d.lanes.map((l) => l.id)),
  docs: DOC_INDEX,
  depth,
});

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const attr = (s: string) => s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");

/** Pages of the retired static site that are app views now. */
const PAGES = new Set(["models", "risks", "guide", "docs"]);

/**
 * Map a link written for the retired static site to an in-app route or to a document file.
 *
 * - `https:` / `mailto:` → unchanged, new tab
 * - `index.html#lane-x` (any folder depth) → `#/map/lane/x`; `index.html` → `#/map`
 * - `[../]steps/<id>.html`, `<id>.html` → `#/step/<id>`; `[../]models/<id>.html` → `#/model/<id>`
 * - `models.html`, `risks.html`, `guide.html`, `docs.html` → `#/models` …
 * - an HTML document (`../../AI_LEARNING_GUIDE_FA.html#x`) → `#/doc/AI_LEARNING_GUIDE/x`, shown inside the app
 * - any other document (`../../../product-management/X.pdf`, `docs/…`) →
 *   `docs/<folder>/<file>`, looked up by file name in the documents manifest, new tab
 * - `#/…` app routes pass through
 */
export function resolveHref(href: string, ctx: LinkCtx): { href: string; external: boolean } {
  if (/^(https?:|mailto:)/i.test(href)) return { href, external: true };
  if (href.startsWith("#/")) return { href, external: false };
  const [path, hash = ""] = href.split("#");
  const file = path.split("/").pop() ?? "";
  const base = file.replace(/\.html?$/i, "");
  const parent = path.split("/").slice(-2, -1)[0] ?? "";
  if (base === "index" || base === "") {
    const lane = hash.startsWith("lane-") ? hash.slice(5) : "";
    if (lane && (!ctx.lanes || ctx.lanes.has(lane))) return { href: `#/map/lane/${lane}`, external: false };
    if (base === "index") return { href: "#/map", external: false };
  }
  if (file === `${base}.html`) {
    // A folder in the path disambiguates (models/x.html vs steps/x.html); otherwise steps win, then models.
    if (parent === "models" && ctx.models.has(base)) return { href: `#/model/${base}`, external: false };
    if (ctx.steps.has(base) && parent !== "models") return { href: `#/step/${base}`, external: false };
    if (ctx.models.has(base)) return { href: `#/model/${base}`, external: false };
    if (PAGES.has(base)) return { href: `#/${base}`, external: false };
  }
  const tail = hash ? `#${hash}` : "";
  let name = file;
  try { name = decodeURIComponent(file); } catch { /* keep the raw name */ }
  const doc = (ctx.docs ?? DOC_INDEX).get(name.toLowerCase());
  // HTML documents open inside the app, in the reader's language when that version exists.
  if (doc && /\.html?$/i.test(doc) && HTML_DOCS.has(docKey(doc))) return { href: docRoute(docKey(doc), hash), external: false };
  if (doc) return { href: encodeURI(doc) + tail, external: true };
  // Unknown file: drop the static site's "../" prefixes so it stays relative to the app (public/).
  const rel = path.replace(/^(\.\.?\/)+/, "");
  const i = rel.indexOf("docs/");
  return { href: (i > 0 ? rel.slice(i) : rel) + tail, external: true };
}

/** Inline markup used by the content files: `code`, **bold**, [label](url), (inferred). */
export function md(text: string, ctx: LinkCtx): string {
  // Code spans are cut out first, so ** or [..](..) inside them stay literal.
  const codes: string[] = [];
  let o = esc(String(text)).replace(/`([^`]+)`/g, (_m, c: string) => `\u0000${codes.push(c) - 1}\u0000`);
  o = o.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  o = o.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_m, label: string, href: string) => {
    const r = resolveHref(href.replace(/&amp;/g, "&"), ctx);
    return `<a href="${attr(r.href)}"${r.external ? ' target="_blank" rel="noopener"' : ""}>${label}</a>`;
  });
  o = o.replace(/\((inferred|استنباطی|استنباط)\)/g, '<span class="inf">($1)</span>');
  // \u0000 delimits the code-span placeholders inserted above (never present in content)
  // eslint-disable-next-line no-control-regex
  return o.replace(/\u0000(\d+)\u0000/g, (_m, i: string) => `<code>${codes[Number(i)]}</code>`);
}

/** Plain text for search and tooltips. */
export const plain = (text: string) =>
  String(text).replace(/`([^`]+)`/g, "$1").replace(/\*\*([^*]+)\*\*/g, "$1").replace(/\[([^\]]+)\]\([^)]*\)/g, "$1");
