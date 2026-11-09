import { useEffect, useRef, useState } from "react";
import type { Instance, InstanceComponent } from "../../lib/instanceTypes";
import { STAGE_IDS, comparePeers, isStopped, sharedData, type StageDetail } from "../../lib/instances";
import { RuntimeDiagram } from "../../components/RuntimeDiagram";
import { diagramForBrain } from "../../lib/runtimeDiagram";
import { STEP_WHY, partWhy, settingWhy } from "./explain";
import { T, settingLabel, type Lang } from "./i18n";
import { ALL, STAGE_LOOK, isProse, replicaText } from "./model";
import { StepDiagram } from "./StepDiagram";
import { InstanceLink, SettingValue, StageCell, Tpl } from "./parts";
import "../stepPanel.css";

function PartList({ parts, lang }: { parts: InstanceComponent[]; lang: Lang }) {
  const s = T(lang);
  return (
    <ul className="ins-parts">
      {parts.map((c) => (
        <li key={c.name} className={isStopped(c) ? "off" : ""}>
          <div className="ins-part-top"><code dir="ltr">{c.name}</code><span className="muted">{s.roles[c.role]}</span></div>
          <p className="ins-why">{partWhy(lang, c.family, c.role)}</p>
          <div className="ins-part-meta">
            <span>{replicaText(c, lang)}</span>
            <code dir="ltr">{c.version}</code>
            <span>{c.metrics ? s.metricsOn : s.metricsOff}</span>
          </div>
        </li>
      ))}
    </ul>
  );
}

function Peers({ inst, k, value, lang }: { inst: Instance; k: string; value: string; lang: Lang }) {
  const s = T(lang);
  const peers = isProse(k) ? undefined : comparePeers(inst, k, value, ALL);
  if (!peers) return null;
  const { total, same, common, commonCount } = peers;
  const cls = `ins-peer${same * 2 >= total ? "" : " differs"}`;
  if (same === total) return <p className={cls}><Tpl plain text={s.peerAll} values={{ total }} /></p>;
  if (same * 2 >= total) return <p className={cls}><Tpl plain text={s.peerMost} values={{ same, total }} /></p>;
  if (commonCount === 1) return <p className={cls}>{s.peerOnly}</p>;
  return <p className={cls}><Tpl text={s.peerDiff} values={{ count: commonCount, total, value: common }} /></p>;
}

function SharedRows({ inst, keys, lang }: { inst: Instance; keys: string[]; lang: Lang }) {
  const s = T(lang);
  const rows = sharedData(inst, ALL).filter((r) => keys.includes(r.key));
  if (!rows.length) return null;
  return (
    <section>
      <h3 className="ins-h">{s.sharedData}</h3>
      {rows.map((r) => (
        <div key={r.key} className="ins-shared">
          <div>{settingLabel(lang, r.key)}: <code dir="ltr">{r.value}</code></div>
          <div className="ins-used">{s.sharedWith}: {r.with.map((id) => <InstanceLink key={id} id={id} lang={lang} />)}</div>
        </div>
      ))}
    </section>
  );
}

const Names = ({ title, names }: { title: string; names: string[] }) =>
  names.length ? (
    <section>
      <h3 className="ins-h">{title}</h3>
      <div className="row">{names.map((n) => <code key={n} dir="ltr">{n}</code>)}</div>
    </section>
  ) : null;

/** The data of one step: a side panel on desktop, a bottom sheet on phones, like the map's step panel. */
interface PanelProps {
  inst: Instance;
  pageId: string;
  detail: StageDetail;
  lang: Lang;
  theme: "dark" | "light";
  /** Opened beside the pipeline map: steps move along the map, closing returns to the overview. */
  onMap?: boolean;
}

export function StagePanel({ inst, pageId, detail, lang, theme, onMap = false }: PanelProps) {
  const s = T(lang);
  const { stage, components, settings, on, replicas } = detail;
  const ref = useRef<HTMLElement>(null);
  const [tall, setTall] = useState(false);
  const home = onMap ? "#/map/overview" : `#/instance/${pageId}`;
  const stepHref = (id: string) => (onMap ? `#/map/lane/${id}` : `${home}/${id}`);
  useEffect(() => { if (ref.current) ref.current.scrollTop = 0; }, [stage.id]);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") window.location.hash = home; };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [home]);
  const i = STAGE_IDS.indexOf(stage.id);
  const diagram = stage.id === "brain" ? diagramForBrain(inst.brain?.family) : undefined;
  const prev = STAGE_IDS[i - 1], next = STAGE_IDS[i + 1];
  return (
    <aside ref={ref} className={`panel ins-panel${tall ? " tall" : ""}`} style={{ ["--lc" as string]: STAGE_LOOK[stage.id].color }} aria-label={s.stages[stage.id]}>
      <button type="button" className="sheet-grip" onClick={() => setTall(!tall)} aria-label={s.expand} aria-expanded={tall}><span /></button>
      <div className="panel-top">
        {onMap ? <span /> : <a className="link" href={`#/map/lane/${stage.id}`}>{s.howItWorks}</a>}
        <a className="icon" href={home} aria-label={s.close} title={`${s.close} (Esc)`}>✕</a>
      </div>
      <h2 className="panel-title">{s.stages[stage.id]}</h2>
      <p className="muted">{inst.id === pageId ? <bdi>{inst.name[lang]}</bdi> : <InstanceLink id={inst.id} lang={lang} />} · <StageCell stage={stage} lang={lang} /></p>

      <h3 className="ins-h">{s.whatItDoes}</h3>
      <p>{STEP_WHY[stage.id].what[lang]}</p>
      <h3 className="ins-h">{s.whyItMatters}</h3>
      <p>{STEP_WHY[stage.id].why[lang]}</p>
      <StepDiagram inst={inst} detail={detail} lang={lang} />
      {diagram && <RuntimeDiagram id={diagram} lang={lang} theme={theme} />}

      {stage.state === "none" && !components.length ? <p className="muted">{s.stepNone}</p> : (
        <>
          <div className="ins-kpis">
            <div className="ins-kpi"><b>{on}/{components.length}</b><span>{s.statParts}</span></div>
            <div className="ins-kpi"><b>{replicas}</b><span>{s.statReplicas}</span></div>
            <div className="ins-kpi"><b>{settings.length}</b><span>{s.settings}</span></div>
          </div>
          {!!components.length && (
            <section>
              <h3 className="ins-h">{s.components}</h3>
              <PartList parts={components} lang={lang} />
            </section>
          )}
          {!!settings.length && (
            <section>
              <h3 className="ins-h">{s.settings}</h3>
              <dl className="ins-values">
                {settings.map(({ key, value }) => (
                  <div key={key}>
                    <dt title={key}>{settingLabel(lang, key)}</dt>
                    <dd><SettingValue k={key} value={value} lang={lang} /></dd>
                    <dd className="ins-value-why">
                      <p className="ins-why">{settingWhy(lang, key)}</p>
                      <Peers inst={inst} k={key} value={value} lang={lang} />
                    </dd>
                  </div>
                ))}
              </dl>
            </section>
          )}
          {stage.id === "analytics" && <SharedRows inst={inst} keys={settings.map((x) => x.key)} lang={lang} />}
          {stage.id === "ops" && <Names title={s.dependencies} names={inst.deps} />}
          {stage.id === "ops" && <Names title={s.companions} names={inst.companions} />}
        </>
      )}

      <p className="muted ins-limit">{s.whyNote} {s.liveNote}</p>
      <div className="pn">
        {prev ? <a href={stepHref(prev)}>{s.stages[prev]}</a> : <span />}
        {next ? <a href={stepHref(next)}>{s.stages[next]}</a> : <span />}
      </div>
    </aside>
  );
}
