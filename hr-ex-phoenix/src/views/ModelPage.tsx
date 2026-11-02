import type { Data } from "../lib/types";
import { laneOf } from "../lib/data";
import { ctxFor } from "../lib/md";
import { Badge, Md, Sections } from "../components/Blocks";
import { EnTag, Facts, go } from "../components/Common";

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
