import { useId, useState } from "react";
import type { Data } from "../lib/types";
import { laneOf } from "../lib/data";
import { ctxFor, plain } from "../lib/md";
import { Badge, BodyView, Md, Sections } from "../components/Blocks";
import { EnTag } from "../components/Common";

/** Lower-cased text a model card is filtered on. */
const cardText = (c: Data["models"]["cards"][number]) => `${c.name} ${c.size} ${JSON.stringify(c.facts)}`.toLowerCase();

export function ModelsView({ d }: { d: Data }) {
  const ctx = ctxFor(d, 0);
  const [q, setQ] = useState("");
  const fa = d.lang === "fa";
  const filterId = useId();
  const needle = q.trim().toLowerCase();
  const cards = d.models.cards.filter((c) => !needle || cardText(c).includes(needle));
  const filterLabel = fa ? "فیلتر مدل‌ها" : "Filter models";
  return (
    <div className="page">
      <h1><Md text={d.models.title} ctx={ctx} /> {d.models.fallback && <EnTag d={d} />}</h1>
      <Md as="p" text={d.models.lede} ctx={ctx} />
      <label htmlFor={filterId} className="sr-only">{filterLabel}</label>
      <input id={filterId} type="search" className="filter" placeholder={`${filterLabel}…`} value={q} onChange={(e) => setQ(e.target.value)} />
      <p className="sr-only" role="status" aria-live="polite">
        {fa ? `${cards.length} از ${d.models.cards.length} مدل` : `${cards.length} of ${d.models.cards.length} models`}
      </p>
      <div className="mgrid">
        {cards.map((c) => (
          <article key={c.id ?? c.name} className="mcard">
            <div className="row">
              <h2>{c.id ? <a className="mcard-link" href={`#/model/${c.id}`}><Md text={c.name} ctx={ctx} /></a> : <Md text={c.name} ctx={ctx} />}</h2>
              <Badge status={c.status} label={d.ui.status[c.status]} />
            </div>
            <div className="size"><Md text={c.size} ctx={ctx} /></div>
            <BodyView body={c.facts} ctx={ctx} />
            {!!c.steps?.length && (
              <div className="steps-row" aria-label={d.ui.used_in}>
                {c.steps.map((s) => {
                  const w = laneOf(d, s);
                  if (!w) return null;
                  const st = d.steps[s];
                  const title = st ? plain(st.title_plain ?? st.title) : s;
                  return <a key={s} className="spill" href={`#/step/${s}`} title={title} aria-label={`${w.lane.prefix}${w.num} · ${title}`}>{w.lane.prefix}{w.num}</a>;
                })}
              </div>
            )}
          </article>
        ))}
      </div>
      {!cards.length && <p className="muted">{fa ? "مدلی با این فیلتر پیدا نشد." : "No models match this filter."}</p>}
      <Sections sections={d.models.sections} ctx={ctx} level={2} />
    </div>
  );
}
