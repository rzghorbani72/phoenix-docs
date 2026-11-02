import type { Data } from "./types";

export interface LinkCtx {
  steps: Set<string>;
  models: Set<string>;
  /** 1 when the text came from a step/model page (its relative links start one folder deeper than the app). */
  depth: 0 | 1;
}

export const ctxFor = (d: Data, depth: 0 | 1): LinkCtx => ({
  steps: new Set(Object.keys(d.steps)),
  models: new Set(Object.keys(d.models.pages)),
  depth,
});

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/** Map a link written for the static site to an in-app route, or to a file relative to the app. */
export function resolveHref(href: string, ctx: LinkCtx): { href: string; external: boolean } {
  if (/^(https?:|mailto:)/.test(href)) return { href, external: true };
  const [path, hash = ""] = href.split("#");
  const base = (path.split("/").pop() ?? "").replace(/\.html$/, "");
  if (hash.startsWith("lane-") && (base === "index" || base === "")) return { href: `#/map/lane/${hash.slice(5)}`, external: false };
  if (ctx.steps.has(base)) return { href: `#/step/${base}`, external: false };
  if (ctx.models.has(base)) return { href: `#/model/${base}`, external: false };
  if (base === "index") return { href: "#/map", external: false };
  if (base === "models" || base === "risks" || base === "guide") return { href: `#/${base}`, external: false };
  // Another document in the repo: the app sits next to en/ and fa/, so only step/model pages need one "../" less.
  const rel = ctx.depth === 1 && path.startsWith("../") ? path.slice(3) : path;
  return { href: rel + (hash ? `#${hash}` : ""), external: true };
}

/** Inline markup used by the content files: `code`, **bold**, [label](url), (inferred). */
export function md(text: string, ctx: LinkCtx): string {
  let o = esc(String(text));
  o = o.replace(/`([^`]+)`/g, "<code>$1</code>");
  o = o.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  o = o.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_m, label: string, href: string) => {
    const r = resolveHref(href.replace(/&amp;/g, "&"), ctx);
    return `<a href="${r.href}"${r.external ? ' target="_blank" rel="noopener"' : ""}>${label}</a>`;
  });
  return o.replace(/\((inferred|استنباطی|استنباط)\)/g, '<span class="inf">($1)</span>');
}

/** Plain text for search and tooltips. */
export const plain = (text: string) =>
  String(text).replace(/`([^`]+)`/g, "$1").replace(/\*\*([^*]+)\*\*/g, "$1").replace(/\[([^\]]+)\]\([^)]*\)/g, "$1");
