import { useState } from "react";
import type { Data } from "../lib/types";
import { laneOf } from "../lib/data";
import { ctxFor } from "../lib/md";
import { Md } from "../components/Blocks";
import { go } from "../components/Common";

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
