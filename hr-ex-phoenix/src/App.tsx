import { useEffect, useMemo, useState } from "react";
import { DATA } from "./lib/data";
import { ctxFor, plain } from "./lib/md";
import type { Status } from "./lib/types";
import MapView, { LANE_COLOR, type MapFilters } from "./components/map/MapView";
import { BodyView, Md } from "./components/Blocks";
import { Search } from "./components/Search";
import { DocsView } from "./views/DocsView";
import { GuideView } from "./views/GuideView";
import { ModelPage } from "./views/ModelPage";
import { ModelsView } from "./views/ModelsView";
import { RisksView } from "./views/RisksView";
import { StepPanel } from "./views/StepPanel";

type Route = { view: "map" | "step" | "models" | "model" | "guide" | "risks" | "docs"; id?: string; lane?: string };

function parse(hash: string): Route {
  const p = hash.replace(/^#\/?/, "").split("/");
  if (p[0] === "step" && p[1]) return { view: "step", id: p[1] };
  if (p[0] === "model" && p[1]) return { view: "model", id: p[1] };
  if (p[0] === "models" || p[0] === "guide" || p[0] === "risks" || p[0] === "docs") return { view: p[0] };
  if (p[0] === "map" && p[1] === "lane" && p[2]) return { view: "map", lane: p[2] };
  return { view: "map" };
}

const store = {
  get: (k: string) => { try { return localStorage.getItem(k); } catch { return null; } },
  set: (k: string, v: string) => { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
};
const ALL: Status[] = ["live", "off", "notdeployed", "external", "unknown"];

export default function App() {
  const [route, setRoute] = useState<Route>(() => parse(window.location.hash));
  const [lang, setLang] = useState<"en" | "fa">(() => (store.get("pp-lang") === "fa" ? "fa" : "en"));
  const [theme, setTheme] = useState<"dark" | "light">(() =>
    (store.get("pp-theme") as "dark" | "light") ?? (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark"));
  const [searchOpen, setSearchOpen] = useState(false);
  const [aboutOpen, setAboutOpen] = useState(false);
  const [filters, setFilters] = useState<MapFilters>({ model: "", statuses: new Set(ALL), query: "", cross: false });
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
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); setSearchOpen(true); }
      if (e.key === "Escape" && route.view === "step") window.location.hash = "#/map";
    };
    window.addEventListener("keydown", k);
    return () => window.removeEventListener("keydown", k);
  }, [route.view]);
  useEffect(() => { if (route.view !== "map" && route.view !== "step") window.scrollTo(0, 0); }, [route]);

  const onMap = route.view === "map" || route.view === "step";
  const ui = d.ui;
  const tabs: [Route["view"], string][] = [["map", ui.nav_map], ["models", ui.nav_models], ["guide", ui.nav_guide ?? "Guide"], ["risks", ui.nav_risks], ["docs", lang === "fa" ? "اسناد" : "Documents"]];
  const toggleStatus = (s: Status) => setFilters((f) => {
    const st = new Set(f.statuses); if (st.has(s) && st.size > 1) st.delete(s); else st.add(s);
    return { ...f, statuses: st };
  });

  return (
    <div className={`app ${onMap ? "on-map" : ""}`}>
      <header className="top">
        <a className="brand" href="#/map"><span className="logo">◆</span>{ui.brand}</a>
        <nav className="tabs">
          {tabs.map(([v, label]) => (
            <a key={v} href={`#/${v}`} className={(route.view === v || (v === "map" && route.view === "step") || (v === "models" && route.view === "model")) ? "on" : ""}>{label}</a>
          ))}
        </nav>
        <div className="tools">
          <button className="search-btn" onClick={() => setSearchOpen(true)}>⌕ <span>{lang === "fa" ? "جست‌وجو" : "Search"}</span><kbd>Ctrl K</kbd></button>
          <button onClick={() => setAboutOpen(true)} title="About">ⓘ</button>
          <button onClick={() => setLang(lang === "en" ? "fa" : "en")}>{lang === "en" ? "فارسی" : "English"}</button>
          <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")} aria-label="theme">{theme === "dark" ? "☀" : "☾"}</button>
        </div>
      </header>

      {onMap && (
        <div className="mapwrap">
          <div className="toolbar">
            <select value={filters.model} onChange={(e) => setFilters({ ...filters, model: e.target.value })}>
              <option value="">{lang === "fa" ? "برجسته‌سازی بر اساس مدل…" : "Highlight steps by model…"}</option>
              {d.models.cards.filter((c) => c.steps?.length).map((c) => <option key={c.id ?? c.name} value={c.id}>{plain(c.name)} — {plain(c.size)}</option>)}
            </select>
            <input value={filters.query} onChange={(e) => setFilters({ ...filters, query: e.target.value })}
              placeholder={lang === "fa" ? "فیلتر گام‌ها…" : "Filter steps…"} />
            <div className="statuses">
              {ALL.map((s) => (
                <button key={s} className={`badge s-${s} ${filters.statuses.has(s) ? "" : "off"}`} onClick={() => toggleStatus(s)}>{ui.status[s]}</button>
              ))}
            </div>
            <label className="chk"><input type="checkbox" checked={filters.cross} onChange={(e) => setFilters({ ...filters, cross: e.target.checked })} />{lang === "fa" ? "همهٔ جریان‌های بین مسیرها" : "All cross-lane flows"}</label>
            <div className="lanes">
              {d.lanes.map((l) => (
                <a key={l.id} href={`#/map/lane/${l.id}`} style={{ ["--lc" as string]: LANE_COLOR[l.color] }} title={plain(l.title)}>{l.prefix}</a>
              ))}
              <a href="#/map/lane/all" title={lang === "fa" ? "نمای کامل" : "Fit everything"}>⤢</a>
            </div>
          </div>
          <MapView d={d} filters={filters} selected={route.view === "step" ? route.id : undefined} lane={route.lane} theme={theme}
            onOpen={(id) => { window.location.hash = `#/step/${id}`; }} />
          {route.view === "step" && route.id && <StepPanel d={d} id={route.id} />}
        </div>
      )}
      {route.view === "models" && <ModelsView d={d} />}
      {route.view === "model" && route.id && <ModelPage d={d} id={route.id} />}
      {route.view === "guide" && <GuideView d={d} />}
      {route.view === "risks" && <RisksView d={d} />}
      {route.view === "docs" && <DocsView d={d} />}

      {searchOpen && <Search d={d} onClose={() => setSearchOpen(false)} />}
      {aboutOpen && (
        <div className="overlay" onClick={() => setAboutOpen(false)}>
          <div className="about" onClick={(e) => e.stopPropagation()}>
            <button className="icon close" onClick={() => setAboutOpen(false)}>✕</button>
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
