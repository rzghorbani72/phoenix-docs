import { useState } from "react";
import type { Data } from "../lib/types";
import { laneOf } from "../lib/data";
import { ctxFor } from "../lib/md";
import { Badge, BodyView, Md, Sections } from "../components/Blocks";
import { EnTag, go } from "../components/Common";

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
