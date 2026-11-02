import { useMemo, useState } from "react";
import type { Data } from "../lib/types";
import { go } from "./Common";

/** Ctrl/Cmd+K palette over steps, models, guide sections and risks. */
export function Search({ d, onClose }: { d: Data; onClose: () => void }) {
  const [q, setQ] = useState("");
  const [sel, setSel] = useState(0);
  const index = useMemo(() => {
    const strip = (s: string) => s.replace(/[`*]/g, "");
    const out: { kind: string; label: string; sub: string; hay: string; to: string }[] = [];
    for (const lane of d.lanes) lane.steps.forEach((id, i) => {
      const s = d.steps[id];
      out.push({ kind: `${lane.prefix}${i + 1}`, label: strip(s.title), sub: strip(s.chip ?? ""), hay: `${s.title} ${s.chip} ${s.summary} ${JSON.stringify(s.sections)}`.toLowerCase(), to: `#/step/${id}` });
    });
    for (const c of d.models.cards) if (c.id) out.push({ kind: "MODEL", label: strip(c.name), sub: strip(c.size), hay: `${c.name} ${c.size} ${JSON.stringify(d.models.pages[c.id])}`.toLowerCase(), to: `#/model/${c.id}` });
    d.guide?.sections.forEach(([h, b]) => out.push({ kind: "GUIDE", label: strip(h), sub: "", hay: `${h} ${JSON.stringify(b)}`.toLowerCase(), to: "#/guide" }));
    d.risks.items.forEach((r) => out.push({ kind: "RISK", label: strip(r.title), sub: strip(r.why), hay: `${r.title} ${r.why}`.toLowerCase(), to: "#/risks" }));
    return out;
  }, [d]);
  const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
  const hits = terms.length
    ? index.map((x) => ({ x, score: terms.reduce((a, t) => a + (x.label.toLowerCase().includes(t) ? 5 : 0) + (x.hay.includes(t) ? 1 : -100), 0) }))
        .filter((h) => h.score > 0).sort((a, b) => b.score - a.score).slice(0, 30).map((h) => h.x)
    : index.slice(0, 12);
  const pick = (to: string) => { go(to); onClose(); };
  return (
    <div className="overlay" onClick={onClose}>
      <div className="palette" onClick={(e) => e.stopPropagation()}>
        <input autoFocus value={q} placeholder={d.lang === "fa" ? "جست‌وجو در گام‌ها، مدل‌ها، راهنما، ریسک‌ها…" : "Search steps, models, guide, risks…"}
          onChange={(e) => { setQ(e.target.value); setSel(0); }}
          onKeyDown={(e) => {
            if (e.key === "Escape") onClose();
            if (e.key === "ArrowDown") { e.preventDefault(); setSel((s) => Math.min(s + 1, hits.length - 1)); }
            if (e.key === "ArrowUp") { e.preventDefault(); setSel((s) => Math.max(s - 1, 0)); }
            if (e.key === "Enter" && hits[sel]) pick(hits[sel].to);
          }} />
        <ul>
          {hits.map((h, i) => (
            <li key={i} className={i === sel ? "on" : ""} onMouseEnter={() => setSel(i)} onClick={() => pick(h.to)}>
              <span className="kind">{h.kind}</span><span className="lbl">{h.label}</span><span className="sub">{h.sub}</span>
            </li>
          ))}
          {!hits.length && <li className="empty">—</li>}
        </ul>
      </div>
    </div>
  );
}
