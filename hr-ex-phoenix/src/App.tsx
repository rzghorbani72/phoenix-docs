import { useEffect, useMemo, useState } from "react";
import { DATA, laneOf } from "./lib/data";
import { ctxFor } from "./lib/md";
import MapView from "./components/map/MapView";
import OverviewMap from "./components/map/OverviewMap";
import { MapToolbar } from "./components/map/MapToolbar";
import { TourBar } from "./components/map/Tour";
import { TOUR_IDS, tourHash } from "./components/map/tourData";
import { STATUSES, type MapFilters } from "./components/map/shared";
import { BodyView, Md } from "./components/Blocks";
import { Search } from "./components/Search";
import { DocsView } from "./views/DocsView";
import { GuideView } from "./views/GuideView";
import { ModelPage } from "./views/ModelPage";
import { ModelsView } from "./views/ModelsView";
import { RisksView } from "./views/RisksView";
import { StepPanel } from "./views/StepPanel";

type Route = {
  view: "map" | "step" | "models" | "model" | "guide" | "risks" | "docs"; id?: string; lane?: string;
  /** Map level: lane cards instead of the step-level diagram (#/map/overview). */
  overview?: boolean;
  /** 0-based stop of the "follow one turn" tour (#/tour/1 … #/tour/16). */
  tour?: number;
};

function parse(hash: string): Route {
  const p = hash.replace(/^#\/?/, "").split("/");
  if (p[0] === "step" && p[1]) return { view: "step", id: p[1] };
  if (p[0] === "tour") {
    const i = Math.min(Math.max(Number(p[1]) || 1, 1), TOUR_IDS.length) - 1;
    return { view: "step", id: TOUR_IDS[i], tour: i };
  }
  if (p[0] === "map" && p[1] === "overview") return { view: "map", overview: true };
  if (p[0] === "model" && p[1]) return { view: "model", id: p[1] };
  if (p[0] === "models" || p[0] === "guide" || p[0] === "risks" || p[0] === "docs") return { view: p[0] };
  if (p[0] === "map" && p[1] === "lane" && p[2]) return { view: "map", lane: p[2] };
  return { view: "map" };
}

const store = {
  get: (k: string) => { try { return localStorage.getItem(k); } catch { return null; } },
  set: (k: string, v: string) => { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
};
const go = (h: string) => { window.location.hash = h; };
/** ?lang=fa / ?theme=light override the stored choice (handy for links and screenshots). */
const param = (k: string) => { try { return new URLSearchParams(window.location.search).get(k); } catch { return null; } };
const typing = (t: EventTarget | null) =>
  t instanceof HTMLElement && (t.isContentEditable || ["INPUT", "SELECT", "TEXTAREA"].includes(t.tagName));

export default function App() {
  const [route, setRoute] = useState<Route>(() => parse(window.location.hash));
  const [lang, setLang] = useState<"en" | "fa">(() => {
    const q = param("lang");
    return q === "fa" || q === "en" ? q : store.get("pp-lang") === "fa" ? "fa" : "en";
  });
  const [theme, setTheme] = useState<"dark" | "light">(() => {
    const q = param("theme");
    if (q === "dark" || q === "light") return q;
    return (store.get("pp-theme") as "dark" | "light") ?? (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
  });
  const [searchOpen, setSearchOpen] = useState(false);
  const [aboutOpen, setAboutOpen] = useState(false);
  const [filters, setFilters] = useState<MapFilters>({ model: "", statuses: new Set(STATUSES), query: "", cross: false });
  const d = DATA[lang];
  const ctx = useMemo(() => ctxFor(d, 0), [d]);

  useEffect(() => {
    const on = () => setRoute(parse(window.location.hash));
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = d.dir;
    document.documentElement.dataset.theme = theme;
    document.title = lang === "fa" ? "پایپ‌لاین‌های Phoenix EX" : "Phoenix EX Pipelines";
    store.set("pp-lang", lang); store.set("pp-theme", theme);
  }, [lang, theme, d.dir]);
  useEffect(() => {
    const k = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); setSearchOpen(true); return; }
      if (route.view !== "step" || !route.id || searchOpen || aboutOpen || e.defaultPrevented) return;
      if (e.key === "Escape") {
        // First Esc leaves the tour (panel stays on that step), the next one closes the panel.
        go(route.tour !== undefined ? `#/step/${route.id}` : "#/map");
        return;
      }
      if ((e.key !== "ArrowLeft" && e.key !== "ArrowRight") || e.altKey || e.ctrlKey || e.metaKey || e.shiftKey || typing(e.target)) return;
      // Arrows follow the reading direction: in RTL the left arrow moves forward.
      const step = (e.key === "ArrowRight") === (d.dir === "ltr") ? 1 : -1;
      if (route.tour !== undefined) {
        const n = route.tour + step;
        if (n >= 0 && n < TOUR_IDS.length) { e.preventDefault(); go(tourHash(n)); }
        return;
      }
      const w = laneOf(d, route.id);
      const next = w?.lane.steps[w.num - 1 + step];
      if (next) { e.preventDefault(); go(`#/step/${next}`); }
    };
    window.addEventListener("keydown", k);
    return () => window.removeEventListener("keydown", k);
  }, [route, d, searchOpen, aboutOpen]);
  useEffect(() => { if (route.view !== "map" && route.view !== "step") window.scrollTo(0, 0); }, [route]);

  const onMap = route.view === "map" || route.view === "step";
  const ui = d.ui;
  const tabs: [Route["view"], string][] = [["map", ui.nav_map], ["models", ui.nav_models], ["guide", ui.nav_guide ?? "Guide"], ["risks", ui.nav_risks], ["docs", lang === "fa" ? "اسناد" : "Documents"]];
  const stepLane = route.view === "step" && route.id ? laneOf(d, route.id)?.lane.id : undefined;
  const inTour = route.tour !== undefined;

  return (
    <div className={`app ${onMap ? "on-map" : ""}`}>
      <header className="top">
        <a className="brand" href="#/map"><span className="logo">◆</span>{ui.brand}</a>
        <nav className="tabs">
          {tabs.map(([v, label]) => {
            const on = route.view === v || (v === "map" && (route.view === "step")) || (v === "models" && route.view === "model");
            return (
            <a key={v} href={`#/${v}`} className={on ? "on" : ""} aria-current={on ? "page" : undefined}>{label}</a>
            );
          })}
        </nav>
        <div className="tools">
          <button className="search-btn" onClick={() => setSearchOpen(true)}>⌕ <span>{lang === "fa" ? "جست‌وجو" : "Search"}</span><kbd>Ctrl K</kbd></button>
          <button onClick={() => setAboutOpen(true)} title={lang === "fa" ? "دربارهٔ این نقشه" : "About this map"} aria-label={lang === "fa" ? "دربارهٔ این نقشه" : "About this map"}>ⓘ</button>
          <button onClick={() => setLang(lang === "en" ? "fa" : "en")}>{lang === "en" ? "فارسی" : "English"}</button>
          <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")} aria-label={theme === "dark" ? (lang === "fa" ? "تم روشن" : "Switch to light theme") : (lang === "fa" ? "تم تیره" : "Switch to dark theme")}>{theme === "dark" ? "☀" : "☾"}</button>
        </div>
      </header>

      {onMap && (
        <div className={`mapwrap${route.view === "step" ? " has-panel" : ""}${inTour ? " in-tour" : ""}`}>
          <MapToolbar d={d} filters={filters} setFilters={setFilters} overview={!!route.overview} tourActive={inTour}
            lane={route.lane ?? stepLane} compact={route.view === "step"} />
          {route.overview
            ? <OverviewMap d={d} theme={theme} onLane={(id) => go(`#/map/lane/${id}`)} />
            : <MapView d={d} filters={filters} selected={route.view === "step" ? route.id : undefined} lane={route.lane} theme={theme}
                tour={inTour ? TOUR_IDS : undefined} onOpen={(id) => go(`#/step/${id}`)} />}
          {route.view === "step" && route.id && <StepPanel d={d} id={route.id} tour={inTour} />}
          {inTour && <TourBar d={d} index={route.tour!} />}
        </div>
      )}
      {route.view === "models" && <ModelsView d={d} />}
      {route.view === "model" && route.id && <ModelPage d={d} id={route.id} />}
      {route.view === "guide" && <GuideView d={d} />}
      {route.view === "risks" && <RisksView d={d} />}
      {route.view === "docs" && <DocsView d={d} />}

      <footer className="app-footer">Developed by Reza.Ghorbani</footer>

      {searchOpen && <Search d={d} onClose={() => setSearchOpen(false)} />}
      {aboutOpen && (
        <div className="overlay" onClick={() => setAboutOpen(false)}>
          <div className="about" role="dialog" aria-modal="true" aria-label={d.meta.title_plain} onClick={(e) => e.stopPropagation()}>
            <button className="icon close" aria-label={lang === "fa" ? "بستن" : "Close"} onClick={() => setAboutOpen(false)}>✕</button>
            <h2><Md text={d.meta.title} ctx={ctx} /></h2>
            <Md as="p" text={d.meta.lede} ctx={ctx} />
            {d.key_points.map((k, i) => <BodyView key={i} body={k} ctx={ctx} />)}
            <p className="muted"><Md text={d.meta.source} ctx={ctx} /></p>
            <p className="muted"><Md text={d.meta.footer} ctx={ctx} /></p>
          </div>
        </div>
      )}
    </div>
  );
}
