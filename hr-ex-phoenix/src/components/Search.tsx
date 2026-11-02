import { useEffect, useId, useMemo, useRef, useState } from "react";
import type { Data } from "../lib/types";
import { buildIndex, search } from "../lib/search";
import { go } from "./Common";

/** Ctrl/Cmd+K palette over steps, models, guide sections and risks (WAI-ARIA combobox in a modal dialog). */
export function Search({ d, onClose }: { d: Data; onClose: () => void }) {
  const [q, setQ] = useState("");
  const [sel, setSel] = useState(0);
  const index = useMemo(() => buildIndex(d), [d]);
  const hits = useMemo(() => search(index, q), [index, q]);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLUListElement>(null);
  const uid = useId();
  const listId = `${uid}-list`;
  const optId = (i: number) => `${uid}-opt-${i}`;
  const fa = d.lang === "fa";
  const label = fa ? "جست‌وجو" : "Search";

  // Remember who had focus and give it back when the dialog closes.
  useEffect(() => {
    const prev = document.activeElement as HTMLElement | null;
    inputRef.current?.focus();
    return () => { if (prev && document.contains(prev)) prev.focus(); };
  }, []);

  // Keep the active option visible while arrowing through a long list.
  useEffect(() => {
    const el = listRef.current?.querySelector<HTMLElement>(`[data-i="${sel}"]`);
    el?.scrollIntoView?.({ block: "nearest" });
  }, [sel]);

  const pick = (to: string) => { go(to); onClose(); };
  const active = hits[sel] ? optId(sel) : undefined;

  return (
    <div className="overlay" onClick={onClose}>
      <div className="palette" role="dialog" aria-modal="true" aria-label={label} dir={d.dir} lang={d.lang}
        onClick={(e) => e.stopPropagation()}
        onKeyDown={(e) => {
          // Focus trap: the input is the only tabbable element, so Tab stays on it.
          if (e.key === "Tab") { e.preventDefault(); inputRef.current?.focus(); }
          if (e.key === "Escape") { e.stopPropagation(); onClose(); }
        }}>
        <input ref={inputRef} value={q} type="text"
          role="combobox" aria-expanded="true" aria-controls={listId} aria-autocomplete="list"
          aria-activedescendant={active} aria-label={label}
          placeholder={fa ? "جست‌وجو در گام‌ها، مدل‌ها، راهنما، ریسک‌ها…" : "Search steps, models, guide, risks…"}
          onChange={(e) => { setQ(e.target.value); setSel(0); }}
          onKeyDown={(e) => {
            if (e.key === "ArrowDown") { e.preventDefault(); setSel((s) => Math.min(s + 1, hits.length - 1)); }
            if (e.key === "ArrowUp") { e.preventDefault(); setSel((s) => Math.max(s - 1, 0)); }
            if (e.key === "Home" && e.ctrlKey) { e.preventDefault(); setSel(0); }
            if (e.key === "End" && e.ctrlKey) { e.preventDefault(); setSel(Math.max(hits.length - 1, 0)); }
            if (e.key === "Enter" && hits[sel]) { e.preventDefault(); pick(hits[sel].to); }
          }} />
        <ul ref={listRef} id={listId} role="listbox" aria-label={label}>
          {hits.map((h, i) => (
            <li key={`${i}-${h.to}`}id={optId(i)} data-i={i} role="option" aria-selected={i === sel}
              className={i === sel ? "on" : ""} onMouseEnter={() => setSel(i)} onClick={() => pick(h.to)}>
              <span className="kind">{h.kind}</span><span className="lbl">{h.label}</span><span className="sub">{h.sub}</span>
            </li>
          ))}
        </ul>
        {!hits.length && <p className="empty" role="status">{fa ? "نتیجه‌ای پیدا نشد" : "No results"}</p>}
      </div>
    </div>
  );
}
