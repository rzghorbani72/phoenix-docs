import { useMemo, useState } from "react";
import type { Data, Page } from "../types";
import { laneOf, modelsForStep } from "../data";
import { ctxFor } from "../md";
import { Badge, BodyView, Md, Sections } from "./Blocks";
import { LANE_COLOR } from "./MapView";

const go = (h: string) => { window.location.hash = h; };

function Facts({ page, d, depth }: { page: Page; d: Data; depth: 0 | 1 }) {
  const ctx = ctxFor(d, depth);
  if (!page.facts?.length) return null;
  return (
    <div className="facts">
      {page.facts.map(([k, v], i) => (
        <div className="fact" key={i}><div className="k"><Md text={k} ctx={ctx} /></div><div className="v"><Md text={v} ctx={ctx} /></div></div>
      ))}
    </div>
  );
}

const EnTag = ({ d }: { d: Data }) => (d.lang === "fa" ? <span className="entag">English</span> : null);

/** Slide-over panel with the full deep dive for one step; the diagram stays visible behind it. */
export function StepPanel({ d, id }: { d: Data; id: string }) {
  const s = d.steps[id];
  const where = laneOf(d, id);
  if (!s || !where) return null;
  const { lane, num } = where;
  const ctx = ctxFor(d, 1);
  const i = num - 1;
  const prev = lane.steps[i - 1], next = lane.steps[i + 1];
  const models = modelsForStep(d, id);
  return (
    <aside className="panel" style={{ ["--lc" as string]: LANE_COLOR[lane.color] }}>
      <div className="panel-top">
        <button className="link" onClick={() => go(`#/map/lane/${lane.id}`)}><Md text={lane.title} ctx={ctx} /> · {lane.prefix}{num}</button>
        <button className="icon" aria-label="close" onClick={() => go("#/map")}>✕</button>
      </div>
      <h2 className="panel-title"><Md text={s.title} ctx={ctx} /></h2>
      <div className="row"><Badge status={s.status} label={d.ui.status[s.status]} />{s.chip && <span className="chip"><Md text={s.chip} ctx={ctx} /></span>}{s.fallback && <EnTag d={d} />}</div>
      <Md as="p" text={s.summary} ctx={ctx} />
      {models.length > 0 && (
        <div className="usedmodels">
          {models.map((m) => <button key={m.name} className="mpill" onClick={() => m.id && go(`#/model/${m.id}`)}><Md text={m.name} ctx={ctx} /> <small><Md text={m.size} ctx={ctx} /></small></button>)}
        </div>
      )}
      <Facts page={s} d={d} depth={1} />
      <Sections sections={s.sections} ctx={ctx} />
      <div className="pn">
        {prev ? <button onClick={() => go(`#/step/${prev}`)}>{d.ui.prev} {d.steps[prev].title_plain ?? d.steps[prev].title}</button> : <span />}
        {next ? <button onClick={() => go(`#/step/${next}`)}>{d.steps[next].title_plain ?? d.steps[next].title} {d.ui.next}</button> : <span />}
      </div>
    </aside>
  );
}

export function ModelsView({ d }: { d: Data }) {
  const ctx = ctxFor(d, 0);
  const [q, setQ] = useState("");
  const cards = d.models.cards.filter((c) => !q || `${c.name} ${c.size} ${JSON.stringify(c.facts)}`.toLowerCase().includes(q.toLowerCase()));
  return (
    <div className="page">
      <h1><Md text={d.models.title} ctx={ctx} /> {d.models.fallback && <EnTag d={d} />}</h1>
      <Md as="p" text={d.models.lede} ctx={ctx} />
      <input className="filter" placeholder={d.lang === "fa" ? "فیلتر مدل‌ها…" : "Filter models…"} value={q} onChange={(e) => setQ(e.target.value)} />
      <div className="mgrid">
        {cards.map((c) => (
          <article key={c.name} className="mcard" onClick={() => c.id && go(`#/model/${c.id}`)} tabIndex={0}
            onKeyDown={(e) => e.key === "Enter" && c.id && go(`#/model/${c.id}`)}>
            <div className="row"><h3><Md text={c.name} ctx={ctx} /></h3><Badge status={c.status} label={d.ui.status[c.status]} /></div>
            <div className="size"><Md text={c.size} ctx={ctx} /></div>
            <BodyView body={c.facts} ctx={ctx} />
            {!!c.steps?.length && (
              <div className="steps-row">
                {c.steps.map((s) => { const w = laneOf(d, s); return w ? <button key={s} className="spill" onClick={(e) => { e.stopPropagation(); go(`#/step/${s}`); }}>{w.lane.prefix}{w.num}</button> : null; })}
              </div>
            )}
          </article>
        ))}
      </div>
      <Sections sections={d.models.sections} ctx={ctx} />
    </div>
  );
}

export function ModelPage({ d, id }: { d: Data; id: string }) {
  const m = d.models.pages[id];
  const card = d.models.cards.find((c) => c.id === id);
  if (!m || !card) return <div className="page"><p>Not found: {id}</p></div>;
  const ctx = ctxFor(d, 1);
  const order = d.models.cards.map((c) => c.id).filter((x): x is string => !!x && !!d.models.pages[x]);
  const i = order.indexOf(id);
  return (
    <div className="page">
      <button className="link" onClick={() => go("#/models")}>{d.ui.nav_models}</button>
      <h1><Md text={m.title} ctx={ctx} /></h1>
      <div className="row"><Badge status={m.status} label={d.ui.status[m.status]} /><span className="size"><Md text={card.size} ctx={ctx} /></span>{m.fallback && <EnTag d={d} />}</div>
      <Md as="p" text={m.summary} ctx={ctx} />
      {!!card.steps?.length && (
        <div className="steps-row">
          <span className="muted">{d.ui.used_in}:</span>
          {card.steps.map((s) => { const w = laneOf(d, s); return w ? <button key={s} className="spill wide" onClick={() => go(`#/step/${s}`)}>{w.lane.prefix}{w.num} · {d.steps[s].title_plain ?? d.steps[s].title}</button> : null; })}
        </div>
      )}
      <Facts page={m} d={d} depth={1} />
      <Sections sections={m.sections} ctx={ctx} />
      <div className="pn">
        {i > 0 ? <button onClick={() => go(`#/model/${order[i - 1]}`)}>{d.ui.prev} {d.models.pages[order[i - 1]].title_plain}</button> : <span />}
        {i < order.length - 1 ? <button onClick={() => go(`#/model/${order[i + 1]}`)}>{d.models.pages[order[i + 1]].title_plain} {d.ui.next}</button> : <span />}
      </div>
    </div>
  );
}

export function GuideView({ d }: { d: Data }) {
  const g = d.guide;
  const ctx = ctxFor(d, 0);
  if (!g) return null;
  const jump = (i: number) => document.getElementById(`g${i}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
  return (
    <div className="page guide">
      <nav className="toc">
        {g.sections.map(([h], i) => <button key={i} onClick={() => jump(i)}><span>{i + 1}</span><Md text={h} ctx={ctx} /></button>)}
      </nav>
      <div>
        <h1><Md text={g.title} ctx={ctx} /> {g.fallback && <EnTag d={d} />}</h1>
        <Md as="p" text={g.lede} ctx={ctx} />
        {g.sections.map(([h, b], i) => (
          <section className="sec" id={`g${i}`} key={i}><h3><Md text={h} ctx={ctx} /></h3><BodyView body={b} ctx={ctx} /></section>
        ))}
      </div>
    </div>
  );
}

export function RisksView({ d }: { d: Data }) {
  const ctx = ctxFor(d, 0);
  const [sev, setSev] = useState<string>("all");
  const items = d.risks.items.filter((r) => sev === "all" || r.sev === sev);
  return (
    <div className="page">
      <h1><Md text={d.risks.title} ctx={ctx} /></h1>
      <Md as="p" text={d.risks.lede} ctx={ctx} />
      <div className="seg">
        {["all", "high", "med", "low"].map((s) => (
          <button key={s} className={sev === s ? "on" : ""} onClick={() => setSev(s)}>
            {s === "all" ? (d.lang === "fa" ? "همه" : "All") : d.ui.sev[s]} ({s === "all" ? d.risks.items.length : d.risks.items.filter((r) => r.sev === s).length})
          </button>
        ))}
      </div>
      <div className="risks">
        {items.map((r, i) => (
          <article key={i} className={`risk sev-${r.sev}`}>
            <span className={`sev sev-${r.sev}`}>{d.ui.sev[r.sev]}</span>
            <div>
              <h3><Md text={r.title} ctx={ctx} /></h3>
              <Md as="p" text={r.why} ctx={ctx} />
              <div className="steps-row">
                {(r.steps ?? []).map((s) => { const w = laneOf(d, s); return w ? <button key={s} className="spill wide" onClick={() => go(`#/step/${s}`)}>{w.lane.prefix}{w.num} · {d.steps[s].title_plain ?? d.steps[s].title}</button> : null; })}
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}

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
