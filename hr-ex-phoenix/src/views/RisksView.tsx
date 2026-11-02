import { useState } from "react";
import type { Data, Risk } from "../lib/types";
import { laneOf } from "../lib/data";
import { ctxFor, plain } from "../lib/md";
import { Md } from "../components/Blocks";

type Sev = "all" | Risk["sev"];
const SEVS: Sev[] = ["all", "high", "med", "low"];

export function RisksView({ d }: { d: Data }) {
  const ctx = ctxFor(d, 0);
  const [sev, setSev] = useState<Sev>("all");
  const fa = d.lang === "fa";
  const all = d.risks.items;
  const items = all.filter((r) => sev === "all" || r.sev === sev);
  const count = (s: Sev) => (s === "all" ? all.length : all.filter((r) => r.sev === s).length);
  return (
    <div className="page">
      <h1><Md text={d.risks.title} ctx={ctx} /></h1>
      <Md as="p" text={d.risks.lede} ctx={ctx} />
      <div className="seg" role="group" aria-label={d.ui.col_sev ?? (fa ? "شدت" : "Severity")}>
        {SEVS.map((s) => (
          <button key={s} type="button" className={sev === s ? "on" : ""} aria-pressed={sev === s} onClick={() => setSev(s)}>
            {s === "all" ? (fa ? "همه" : "All") : d.ui.sev[s]} ({count(s)})
          </button>
        ))}
      </div>
      <p className="sr-only" role="status" aria-live="polite">
        {fa ? `${items.length} ریسک نمایش داده می‌شود` : `Showing ${items.length} risks`}
      </p>
      <div className="risks">
        {items.map((r) => (
          <article key={`${r.sev}-${r.title}`} className={`risk sev-${r.sev}`}>
            <span className={`sev sev-${r.sev}`}>{d.ui.sev[r.sev]}</span>
            <div>
              <h2><Md text={r.title} ctx={ctx} /></h2>
              <Md as="p" text={r.why} ctx={ctx} />
              {!!r.steps?.length && (
                <div className="steps-row">
                  {r.steps.map((s) => {
                    const w = laneOf(d, s);
                    return w ? <a key={s} className="spill wide" href={`#/step/${s}`}>{w.lane.prefix}{w.num} · {plain(d.steps[s].title_plain ?? d.steps[s].title)}</a> : null;
                  })}
                </div>
              )}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
