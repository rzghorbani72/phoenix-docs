import { useCallback, useEffect, useMemo, useRef } from "react";
import type { Data } from "../lib/types";
import { ctxFor, resolveHref } from "../lib/md";
import { LABELS } from "./docs/labels";
import { fileUrl, HTML_DOCS } from "./docs/manifest";
import "./docs/docs.css";

/**
 * One HTML document inside the app layout (#/doc/<key>[/<anchor>]). The header's language picks the
 * EN or FA file, the header's theme is pushed into the page, and links inside the page that point at
 * other documents or app pages become app routes instead of navigating the frame.
 */
export function DocView({ d, id, anchor, theme }: { d: Data; id: string; anchor?: string; theme: "dark" | "light" }) {
  const L = LABELS[d.lang];
  const versions = HTML_DOCS.get(id);
  const other = d.lang === "fa" ? "en" : "fa";
  const shown = versions?.[d.lang] ?? versions?.[other];
  const frame = useRef<HTMLIFrameElement>(null);
  const ctx = useMemo(() => ctxFor(d, 0), [d]);

  const syncTheme = useCallback(() => {
    const root = frame.current?.contentDocument?.documentElement;
    if (root) root.dataset.theme = theme;
  }, [theme]);
  useEffect(syncTheme, [syncTheme]);

  const onLoad = () => {
    syncTheme();
    const doc = frame.current?.contentDocument;
    if (!doc) return; // file:// or another origin: the page keeps its own links
    doc.addEventListener("click", (e) => {
      // The event comes from the frame's realm, so instanceof checks against this window would fail.
      const a = (e.target as Element | null)?.closest?.("a[href]") as HTMLAnchorElement | null;
      const raw = a?.getAttribute("href");
      if (!a || !raw || raw.startsWith("#") || e.defaultPrevented || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey) return;
      e.preventDefault();
      const r = resolveHref(raw, ctx);
      if (!r.external) window.location.hash = r.href;
      else window.open(a.href, "_blank", "noopener");
    });
  };

  if (!shown) {
    return (
      <div className="page">
        <p>{L.missing}</p>
        <a className="doc-btn" href="#/docs">← {L.back}</a>
      </div>
    );
  }
  const url = fileUrl(shown.file);
  return (
    <div className="docview">
      <div className="docview-bar">
        <a className="doc-btn" href="#/docs">{d.dir === "rtl" ? "→" : "←"} {L.back}</a>
        <strong className="docview-title" dir="auto">{shown.entry.title}</strong>
        {!versions?.[d.lang] && <span className="note warn docview-note">{L.onlyIn(L.langName[other])}</span>}
        <a className="doc-btn" href={url} target="_blank" rel="noopener" title={L.openNew}>↗</a>
      </div>
      {/* Remounts on a language switch; an anchor change on the same file only scrolls the page. */}
      <iframe key={url} ref={frame} className="docview-frame" src={anchor ? `${url}#${anchor}` : url} title={shown.entry.title} onLoad={onLoad} />
    </div>
  );
}
