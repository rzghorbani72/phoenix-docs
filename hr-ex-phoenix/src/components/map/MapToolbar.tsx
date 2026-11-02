import { useEffect, useMemo, useRef, useState } from "react";
import type { Data, Status } from "../../lib/types";
import { plain } from "../../lib/md";
import { LANE_COLOR, STATUSES, type MapFilters } from "./shared";
import { T } from "./i18n";
import { exportPng } from "./exportPng";
import { tourHash } from "./tourData";
import { useNarrow } from "./useNarrow";

interface Props {
  d: Data; filters: MapFilters; setFilters: (f: MapFilters) => void;
  overview: boolean; tourActive: boolean; lane?: string;
  /** Fold filters behind a menu button (a side panel is open); always on for narrow screens. */
  compact?: boolean;
}

/** Compact map toolbar: level switch, tour, filters, lane jump, legend and PNG export. Folds on narrow screens. */
export function MapToolbar({ d, filters, setFilters, overview, tourActive, lane, compact }: Props) {
  const narrow = useNarrow();
  const t = T(d.lang);
  const [pop, setPop] = useState<"" | "status" | "legend">("");
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState<"" | "export" | "fail">("");
  const ref = useRef<HTMLDivElement>(null);
  const counts = useMemo(() => {
    const c = Object.fromEntries(STATUSES.map((s) => [s, 0])) as Record<Status, number>;
    Object.values(d.steps).forEach((s) => c[s.status]++);
    return c;
  }, [d]);

  useEffect(() => {
    if (!pop && !open) return;
    const close = (e: PointerEvent) => { if (!ref.current?.contains(e.target as Node)) { setPop(""); setOpen(false); } };
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") { e.preventDefault(); setPop(""); setOpen(false); } };
    document.addEventListener("pointerdown", close);
    document.addEventListener("keydown", esc);
    return () => { document.removeEventListener("pointerdown", close); document.removeEventListener("keydown", esc); };
  }, [pop, open]);

  const toggleStatus = (s: Status) => {
    const st = new Set(filters.statuses);
    if (st.has(s) && st.size > 1) st.delete(s); else st.add(s);
    setFilters({ ...filters, statuses: st });
  };
  const active = (filters.model ? 1 : 0) + (filters.query.trim() ? 1 : 0) + (filters.statuses.size < STATUSES.length ? 1 : 0) + (filters.cross ? 1 : 0);
  const doExport = async () => {
    setBusy("export");
    try { await exportPng(overview ? "phoenix-ex-overview" : "phoenix-ex-map"); setBusy(""); }
    catch { setBusy("fail"); setTimeout(() => setBusy(""), 2500); }
  };

  return (
    <div ref={ref} className={`mtb${compact || narrow ? " compact" : ""}${open ? " open" : ""}`} role="toolbar" aria-label={t.mode}>
      <div className="mtb-mode" role="group" aria-label={t.mode}>
        <a href="#/map/overview" className={overview ? "on" : ""} aria-current={overview}>{t.overview}</a>
        <a href={lane ? `#/map/lane/${lane}` : "#/map"} className={overview ? "" : "on"} aria-current={!overview}>{t.detail}</a>
      </div>
      <a className={`mtb-tour${tourActive ? " on" : ""}`} href={tourHash(0)} title={t.tourTitle}>
        <span aria-hidden>▶</span><span className="mtb-tour-l">{t.tour}</span>
      </a>

      <div className="mtb-fold">
        {!overview && <>
          <select value={filters.model} onChange={(e) => setFilters({ ...filters, model: e.target.value })} aria-label={t.highlightModel}>
            <option value="">{t.highlightModel}</option>
            {d.models.cards.filter((c) => c.steps?.length).map((c) => <option key={c.id ?? c.name} value={c.id}>{plain(c.name)} — {plain(c.size)}</option>)}
          </select>
          <input type="search" value={filters.query} onChange={(e) => setFilters({ ...filters, query: e.target.value })} placeholder={t.filterSteps} aria-label={t.filterSteps} />
          <div className="mtb-popwrap">
            <button className={`mtb-btn${filters.statuses.size < STATUSES.length ? " lit" : ""}`} aria-expanded={pop === "status"} onClick={() => setPop(pop === "status" ? "" : "status")}>
              <span className="mtb-dots" aria-hidden>{STATUSES.map((s) => <i key={s} className={`s-${s}${filters.statuses.has(s) ? "" : " off"}`} />)}</span>
              {t.status} <small>{filters.statuses.size}/{STATUSES.length}</small> ▾
            </button>
            {pop === "status" && (
              <div className="mtb-pop">
                {STATUSES.map((s) => (
                  <button key={s} className={`mtb-st${filters.statuses.has(s) ? "" : " off"}`} onClick={() => toggleStatus(s)} aria-pressed={filters.statuses.has(s)}>
                    <span className={`badge s-${s}`}>{d.ui.status[s]}</span><small>{counts[s]}</small>
                  </button>
                ))}
                <button className="mtb-link" onClick={() => setFilters({ ...filters, statuses: new Set(STATUSES) })}>{d.lang === "fa" ? "همه" : "All"}</button>
              </div>
            )}
          </div>
          <button className={`mtb-btn${filters.cross ? " lit" : ""}`} aria-pressed={filters.cross} title={t.handoffsTitle}
            onClick={() => setFilters({ ...filters, cross: !filters.cross })}>
            <span className="mtb-dash" aria-hidden /> {t.handoffs}
          </button>
        </>}
        <div className="mtb-lanes" role="group" aria-label={t.laneJump}>
          {d.lanes.map((l) => (
            <a key={l.id} href={`#/map/lane/${l.id}`} className={lane === l.id && !overview ? "on" : ""}
              style={{ ["--lc" as string]: LANE_COLOR[l.color] }} title={plain(l.title)}>{l.prefix}</a>
          ))}
          <a href="#/map/lane/all" title={t.fit} aria-label={t.fit}>⤢</a>
        </div>
      </div>

      <div className="mtb-end">
        <div className="mtb-popwrap">
          <button className="mtb-icon" aria-expanded={pop === "legend"} title={t.legend} aria-label={t.legend} onClick={() => setPop(pop === "legend" ? "" : "legend")}>?</button>
          {pop === "legend" && <Legend d={d} />}
        </div>
        <button className="mtb-icon" onClick={doExport} disabled={busy === "export"} title={busy === "fail" ? t.exportFailed : t.exportTitle} aria-label={t.exportPng}>
          {busy === "export" ? "…" : busy === "fail" ? "!" : "⤓"}
        </button>
        <button className={`mtb-more${active ? " lit" : ""}`} aria-expanded={open} onClick={() => setOpen(!open)}>
          ☰ <span className="mtb-more-l">{t.filters}</span>{active ? <small>{active}</small> : null}
        </button>
      </div>
    </div>
  );
}

function Legend({ d }: { d: Data }) {
  const t = T(d.lang);
  return (
    <div className="mtb-pop legend">
      <h4>{t.legendStatus}</h4>
      <div className="lg-grid">{STATUSES.map((s) => <span key={s} className={`badge s-${s}`}>{d.ui.status[s]}</span>)}</div>
      <h4>{t.legendLanes}</h4>
      <div className="lg-lanes">
        {d.lanes.map((l) => (
          <span key={l.id} style={{ ["--lc" as string]: LANE_COLOR[l.color] }}><i />{l.prefix} · {plain(l.short).replace(/^\d+\s*·\s*/, "")}</span>
        ))}
      </div>
      <h4>{t.legendEdges}</h4>
      <ul className="lg-edges">
        <li><svg width="44" height="10" aria-hidden><line x1="2" y1="5" x2="36" y2="5" stroke="var(--c-teal)" strokeWidth="2" /><path d="M36 1 L43 5 L36 9z" fill="var(--c-teal)" /></svg>{t.edgeLane}</li>
        <li><svg width="44" height="10" aria-hidden><line className="lg-anim" x1="2" y1="5" x2="36" y2="5" stroke="var(--accent)" strokeWidth="2" strokeDasharray="6 5" /><path d="M36 1 L43 5 L36 9z" fill="var(--accent)" /></svg>{t.edgeCross}</li>
        <li><span className="lg-box dim" />{t.dimmed}</li>
        <li><span className="lg-box glow" />{t.glow}</li>
        <li><span className="fnode-en lg-en">EN</span>{t.enTag}</li>
      </ul>
    </div>
  );
}
