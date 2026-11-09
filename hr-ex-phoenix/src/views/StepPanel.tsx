import { useEffect, useRef, useState } from "react";
import type { Data } from "../lib/types";
import { laneOf, modelsForStep } from "../lib/data";
import { ctxFor } from "../lib/md";
import { Badge, Md, Sections } from "../components/Blocks";
import { EnTag, Facts, go } from "../components/Common";
import { RuntimeDiagram } from "../components/RuntimeDiagram";
import { LANE_COLOR } from "../components/map/shared";
import { STEP_NODE } from "../lib/runtimeDiagram";
import { T } from "../components/map/i18n";
import "./stepPanel.css";

/**
 * Deep dive for one step. A side panel on desktop (docks left in RTL); a bottom sheet below 860px that
 * can be expanded, so the diagram stays visible and usable above it.
 */
export function StepPanel({ d, id, tour = false, theme = "dark" }: { d: Data; id: string; tour?: boolean; theme?: "dark" | "light" }) {
  const ref = useRef<HTMLElement>(null);
  const [tall, setTall] = useState(false);
  useEffect(() => { ref.current?.scrollTo({ top: 0 }); }, [id]);
  const s = d.steps[id];
  const where = laneOf(d, id);
  if (!s || !where) return null;
  const t = T(d.lang);
  const { lane, num } = where;
  const ctx = ctxFor(d, 1);
  const i = num - 1;
  const prev = lane.steps[i - 1], next = lane.steps[i + 1];
  const models = modelsForStep(d, id);
  return (
    <aside ref={ref} className={`panel${tall ? " tall" : ""}${tour ? " in-tour" : ""}`} style={{ ["--lc" as string]: LANE_COLOR[lane.color] }}
      aria-label={s.title_plain ?? s.title}>
      <button className="sheet-grip" onClick={() => setTall(!tall)} aria-label={tall ? t.collapse : t.expand} aria-expanded={tall}><span /></button>
      <div className="panel-top">
        <button className="link" onClick={() => go(`#/map/lane/${lane.id}`)}><Md text={lane.title} ctx={ctx} /> · {lane.prefix}{num}</button>
        <button className="icon" aria-label={t.close} title={`${t.close} (Esc)`} onClick={() => go("#/map")}>✕</button>
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
      {STEP_NODE[id] && <RuntimeDiagram id="aiva" lang={d.lang} theme={theme} node={STEP_NODE[id]} />}
      <Sections sections={s.sections} ctx={ctx} />
      <div className="pn">
        {prev ? <button onClick={() => go(`#/step/${prev}`)}>{d.ui.prev} {d.steps[prev].title_plain ?? d.steps[prev].title}</button> : <span />}
        {next ? <button onClick={() => go(`#/step/${next}`)}>{d.steps[next].title_plain ?? d.steps[next].title} {d.ui.next}</button> : <span />}
      </div>
      <p className="panel-keys muted">{t.keys}</p>
    </aside>
  );
}
