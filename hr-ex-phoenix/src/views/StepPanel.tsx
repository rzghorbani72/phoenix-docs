import type { Data } from "../lib/types";
import { laneOf, modelsForStep } from "../lib/data";
import { ctxFor } from "../lib/md";
import { Badge, Md, Sections } from "../components/Blocks";
import { EnTag, Facts, go } from "../components/Common";
import { LANE_COLOR } from "../components/map/MapView";

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
