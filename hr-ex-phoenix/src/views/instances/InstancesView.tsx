import { useId, useState } from "react";
import type { Instance, InstanceCategory } from "../../lib/instanceTypes";
import { INSTANCES, connectedPipeline, hasSurface, voiceDiff } from "../../lib/instances";
import { T, settingLabel, type Lang } from "./i18n";
import { Surfaces } from "./Surfaces";
import { ALL, CATEGORIES, partsOn } from "./model";
import { ConfirmMark, InstanceLink, SettingValue, SourceNote, StageCell, StateChip, Tpl } from "./parts";
import "./instances.css";

export type InstancesMode = "all" | "pipelines" | "compare" | "shared";

const MODES: InstancesMode[] = ["all", "pipelines", "compare", "shared"];

/** Mode is held by the caller, so coming back from an instance page keeps the same view. */
export function InstancesView({ lang, mode, onMode }: { lang: Lang; mode: InstancesMode; onMode: (m: InstancesMode) => void }) {
  const s = T(lang);
  const modeLabel: Record<InstancesMode, string> = { all: s.modeAll, pipelines: s.modePipelines, compare: s.modeCompare, shared: s.modeShared };
  const tiles: [string, number][] = [
    [s.tileInstances, ALL.length],
    [s.tilePhone, ALL.filter((i) => hasSurface(i, "phone")).length],
    [s.tileOff, ALL.filter((i) => i.state === "off").length],
  ];
  return (
    <div className="page ins">
      <h1>{s.title}</h1>
      <p>{s.lede}</p>
      <SourceNote lang={lang} source={INSTANCES.source} />
      <div className="facts">
        {tiles.map(([k, v]) => <div key={k} className="fact"><div className="k">{k}</div><div className="v ins-tile">{v}</div></div>)}
      </div>
      <div className="seg ins-modes" role="group" aria-label={s.modesLabel}>
        {MODES.map((m) => (
          <button key={m} type="button" className={m === mode ? "on" : ""} aria-pressed={m === mode} onClick={() => onMode(m)}>{modeLabel[m]}</button>
        ))}
      </div>
      {mode === "all" && <AllInstances lang={lang} />}
      {mode === "pipelines" && <Pipelines lang={lang} />}
      {mode === "compare" && <Compare lang={lang} />}
      {mode === "shared" && <Shared lang={lang} />}
    </div>
  );
}

const hasVoiceSettings = (i: Instance) => Object.keys(i.config.voice).length > 0;
const nameText = (i: Instance) => `${i.name.en} ${i.name.fa} ${i.releases.join(" ")} ${i.id}`.toLowerCase();

function AllInstances({ lang }: { lang: Lang }) {
  const s = T(lang);
  const [q, setQ] = useState("");
  const [cat, setCat] = useState<InstanceCategory | "all">("all");
  const filterId = useId();
  const needle = q.trim().toLowerCase();
  const hits = ALL.filter((i) => !needle || nameText(i).includes(needle));
  const shown = hits.filter((i) => cat === "all" || i.category === cat);
  const categories = CATEGORIES.filter((c) => ALL.some((i) => i.category === c));
  const chip = (id: InstanceCategory | "all", label: string, count: number) => (
    <button key={id} type="button" className={`chip ins-chip${cat === id ? " on" : ""}`} aria-pressed={cat === id} onClick={() => setCat(id)}>{label} ({count})</button>
  );
  return (
    <>
      <div className="row ins-chips" role="group" aria-label={s.categoryLabel}>
        {chip("all", s.allCategories, hits.length)}
        {categories.map((c) => chip(c, s.categories[c], hits.filter((i) => i.category === c).length))}
      </div>
      <label htmlFor={filterId} className="sr-only">{s.filterLabel}</label>
      <input id={filterId} type="search" className="filter" placeholder={`${s.filterLabel}…`} value={q} onChange={(e) => setQ(e.target.value)} />
      <p className="sr-only" role="status" aria-live="polite"><Tpl plain text={s.shownOf} values={{ shown: shown.length, total: ALL.length }} /></p>
      {categories.map((c) => {
        const list = shown.filter((i) => i.category === c);
        if (!list.length) return null;
        return (
          <section key={c}>
            <h2 className="ins-h">{s.categories[c]}</h2>
            <div className="mgrid">{list.map((i) => <Card key={i.id} inst={i} lang={lang} />)}</div>
          </section>
        );
      })}
      {!shown.length && <p className="muted">{s.noMatch}</p>}
    </>
  );
}

/** Every instance against every pipeline stage. Stage headers open that lane of the map. */
function Pipelines({ lang }: { lang: Lang }) {
  const s = T(lang);
  const order = CATEGORIES.flatMap((c) => ALL.filter((i) => i.category === c));
  const stages = connectedPipeline(order[0]).map((p) => p.stage.id);
  return (
    <section>
      <p className="muted">{s.pipelineNote}</p>
      <div className="tw ins-compare">
        <table>
          <thead>
            <tr>
              <th scope="col">{s.colInstance}</th>
              {stages.map((id) => <th key={id} scope="col"><a href={`#/map/lane/${id}`}>{s.stages[id]}</a></th>)}
            </tr>
          </thead>
          <tbody>
            {order.map((inst) => (
              <tr key={inst.id}>
                <th scope="row"><InstanceLink id={inst.id} lang={lang} /></th>
                {connectedPipeline(inst).map(({ stage: p }) => <td key={p.id}>{p.state === "none" ? <StageCell stage={p} lang={lang} /> : <a href={`#/instance/${inst.id}/${p.id}`}><StageCell stage={p} lang={lang} /></a>}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function Card({ inst, lang }: { inst: Instance; lang: Lang }) {
  const s = T(lang);
  const speech = inst.config.voice.AGENT_STT_CLIENT ?? inst.config.voice.AGENT_STT_MODEL;
  return (
    <article className="mcard ins-card">
      <h3><a className="mcard-link" href={`#/instance/${inst.id}`}>{inst.name[lang]}</a></h3>
      <div className="ins-release"><code dir="ltr">{inst.release}</code> <ConfirmMark inst={inst} lang={lang} /></div>
      <div className="row ins-card-state">
        <StateChip state={inst.state} lang={lang} />
      </div>
      <p className="ins-about">{inst.about[lang]}</p>
      <Surfaces inst={inst} lang={lang} compact />
      <div className="facts ins-card-facts">
        {hasSurface(inst, "phone") ? (
          <>
            <div className="fact"><div className="k">{s.factSpeech}</div><div className="v">{speech ? <code dir="ltr">{speech}</code> : <span className="muted">{s.notSet}</span>}</div></div>
            <div className="fact"><div className="k">{s.factBrain}</div><div className="v">{inst.brain ? <code dir="ltr">{inst.brain.family}</code> : <span className="muted">{s.none}</span>}</div></div>
          </>
        ) : (
          <div className="fact"><div className="k">{s.factPartsOn}</div><div className="v"><Tpl plain text={s.partsOn} values={{ on: partsOn(inst), total: inst.components.length }} /></div></div>
        )}
      </div>
    </article>
  );
}

function Compare({ lang }: { lang: Lang }) {
  const s = T(lang);
  const [showAll, setShowAll] = useState(false);
  const phones = ALL.filter((i) => hasSurface(i, "phone") && i.state !== "off");
  // An assistant with no voice settings would mark every row as different, so it gets a line instead.
  const list = phones.filter(hasVoiceSettings);
  const skipped = phones.filter((i) => !hasVoiceSettings(i));
  const rows = voiceDiff(list);
  const differs = rows.filter((r) => r.differs).length;
  const shown = showAll ? rows : rows.filter((r) => r.differs);
  return (
    <>
      <div className="row ins-compare-bar">
        <label className="ins-toggle"><input type="checkbox" checked={showAll} onChange={(e) => setShowAll(e.target.checked)} /> {s.showAll}</label>
        <span className="muted"><Tpl plain text={s.differCount} values={{ differs, total: rows.length }} /></span>
      </div>
      {!!skipped.length && <p className="muted"><Tpl plain text={s.compareSkipped} values={{ names: skipped.map((i) => i.name[lang]).join(s.listSep) }} /></p>}
      {!shown.length ? <p className="muted">{s.noDiffs}</p> : (
        <div className="tw ins-compare">
          <table>
            <caption className="sr-only">{s.compareCaption}</caption>
            <thead>
              <tr>
                <th scope="col">{s.settingCol}</th>
                {list.map((i) => <th key={i.id} scope="col"><InstanceLink id={i.id} lang={lang} /></th>)}
              </tr>
            </thead>
            <tbody>
              {shown.map((r) => (
                <tr key={r.key} className={showAll && r.differs ? "ins-differs" : undefined}>
                  <th scope="row" title={r.key}>{settingLabel(lang, r.key)}</th>
                  {list.map((i) => <td key={i.id}><SettingValue k={r.key} value={r.values[i.id]} lang={lang} /></td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}

function Shared({ lang }: { lang: Lang }) {
  const s = T(lang);
  return (
    <>
      <p>{s.sharedLede}</p>
      {INSTANCES.shared.map((g) => (
        <section key={g.group}>
          <h2 className="ins-h">{g.name[lang]} ({g.items.length})</h2>
          <ul className="ins-list">
            {g.items.map((item) => (
              <li key={item.id}>
                <div className="row"><code dir="ltr">{item.id}</code><StateChip state={item.state} lang={lang} /></div>
                {item.usedBy.length ? (
                  <div className="ins-used"><span className="muted">{s.usedBy}:</span> {item.usedBy.map((id) => <InstanceLink key={id} id={id} lang={lang} />)}</div>
                ) : <div className="muted">{s.usedByNone}</div>}
              </li>
            ))}
          </ul>
        </section>
      ))}
    </>
  );
}
