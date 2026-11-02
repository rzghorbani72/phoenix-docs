import { useEffect, useRef, useState, type RefObject } from "react";
import type { Data } from "../../lib/types";
import { laneOf } from "../../lib/data";
import { plain } from "../../lib/md";
import { LANE_COLOR } from "./shared";

export interface TipApi { show: (id: string, el: Element) => void; hide: () => void }

const W = 330;

/**
 * Hover card for a step box. It owns its own state and is driven through `api`, so hovering never
 * re-renders the flow canvas or rebuilds nodes.
 */
export function NodeTip({ d, apiRef }: { d: Data; apiRef: RefObject<TipApi | null> }) {
  const [tip, setTip] = useState<{ id: string; x: number; y: number; above: boolean } | null>(null);
  const timer = useRef(0);
  useEffect(() => {
    apiRef.current = {
      show: (id, el) => {
        window.clearTimeout(timer.current);
        timer.current = window.setTimeout(() => {
          if (!el.isConnected) return;
          const r = el.getBoundingClientRect();
          const x = Math.max(8, Math.min(r.left + r.width / 2 - W / 2, window.innerWidth - W - 8));
          const above = r.bottom + 230 > window.innerHeight;
          setTip({ id, x, y: above ? r.top - 10 : r.bottom + 10, above });
        }, 350);
      },
      hide: () => { window.clearTimeout(timer.current); setTip(null); },
    };
    return () => { window.clearTimeout(timer.current); apiRef.current = null; };
  }, [apiRef]);
  if (!tip) return null;
  const s = d.steps[tip.id];
  const where = laneOf(d, tip.id);
  if (!s || !where) return null;
  return (
    <div className={`nodetip${tip.above ? " above" : ""}`} role="tooltip"
      style={{ left: tip.x, top: tip.y, width: W, ["--lc" as string]: LANE_COLOR[where.lane.color] }}>
      <div className="nodetip-head">
        <span className="nodetip-num">{where.lane.prefix}{where.num}</span>
        <span className={`badge s-${s.status}`}>{d.ui.status[s.status]}</span>
      </div>
      <div className="nodetip-title">{plain(s.title)}</div>
      <p className="nodetip-sum">{plain(s.summary)}</p>
      {s.facts?.slice(0, 2).map(([k, v], i) => (
        <div className="nodetip-fact" key={i}><span>{plain(k)}</span><b>{plain(v)}</b></div>
      ))}
    </div>
  );
}
