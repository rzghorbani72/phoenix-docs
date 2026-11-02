import type { Data } from "../../lib/types";
import { laneOf } from "../../lib/data";
import { plain } from "../../lib/md";
import { LANE_COLOR } from "./shared";
import { T } from "./i18n";
import { TOUR, tourHash } from "./tourData";

/** Caption card with Back / Next / Exit; the camera and the step panel follow the route. */
export function TourBar({ d, index }: { d: Data; index: number }) {
  const t = T(d.lang);
  const stop = TOUR[index];
  const where = laneOf(d, stop.id);
  const s = d.steps[stop.id];
  const last = index === TOUR.length - 1;
  const go = (h: string) => { window.location.hash = h; };
  return (
    <div className="tourbar" role="region" aria-label={t.tour} style={{ ["--lc" as string]: where ? LANE_COLOR[where.lane.color] : "var(--accent)" }}>
      <div className="tour-top">
        <span className="tour-kicker">▶ {t.tour}</span>
        <span className="tour-count">{t.tourStep} {index + 1} {t.tourOf} {TOUR.length}</span>
        <button className="tour-x" onClick={() => go(`#/step/${stop.id}`)} aria-label={t.stop} title={t.stop}>✕</button>
      </div>
      <div className="tour-progress" aria-hidden>
        {TOUR.map((x, i) => (
          <button key={x.id} className={i === index ? "on" : i < index ? "done" : ""} onClick={() => go(tourHash(i))} tabIndex={-1}
            title={plain(d.steps[x.id]?.title ?? x.id)} />
        ))}
      </div>
      <div className="tour-title"><span className="tour-num">{where ? `${where.lane.prefix}${where.num}` : ""}</span>{s ? plain(s.title) : stop.id}</div>
      <p className="tour-cap">{d.lang === "fa" ? stop.fa : stop.en}</p>
      <div className="tour-nav">
        <button onClick={() => go(tourHash(index - 1))} disabled={index === 0}>{d.lang === "fa" ? "→" : "←"} {t.prev}</button>
        <span className="tour-keys">{t.tourKeys}</span>
        {last
          ? <button className="primary" onClick={() => go(`#/step/${stop.id}`)}>{t.finish} ✓</button>
          : <button className="primary" onClick={() => go(tourHash(index + 1))}>{t.next} {d.lang === "fa" ? "←" : "→"}</button>}
      </div>
    </div>
  );
}
