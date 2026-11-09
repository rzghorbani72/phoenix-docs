import { Fragment } from "react";
import type { Instance, InstanceState } from "../../lib/instanceTypes";
import { byId, type PipelineStage } from "../../lib/instances";
import { T, type Lang } from "./i18n";
import { isProse } from "./model";

/** Fills {name} slots of a template. Values render as plain text, identifiers kept left-to-right. */
export function Tpl({ text, values, plain }: { text: string; values: Record<string, string | number>; plain?: boolean }) {
  return text.split(/(\{\w+\})/).map((part, i) => {
    const slot = /^\{(\w+)\}$/.exec(part);
    const value = slot ? values[slot[1]] : undefined;
    if (value === undefined) return <Fragment key={i}>{part}</Fragment>;
    return plain || typeof value === "number" ? <Fragment key={i}>{value}</Fragment> : <code key={i} dir="ltr">{value}</code>;
  });
}

export function StateChip({ state, lang }: { state: InstanceState; lang: Lang }) {
  return <span className={`chip ins-state ins-state-${state}`}>{T(lang).states[state]}</span>;
}

/** The small mark on a name that is a reading of the config, not confirmed by its owner. */
export function ConfirmMark({ inst, lang }: { inst: Instance; lang: Lang }) {
  return inst.confirm ? <span className="ins-confirm">{T(lang).nameToConfirm}</span> : null;
}

/** A link to an instance by its display name; an id with no instance stays a plain identifier. */
export function InstanceLink({ id, lang }: { id: string; lang: Lang }) {
  const inst = byId(id);
  return inst ? <a className="link" href={`#/instance/${id}`}>{inst.name[lang]}</a> : <code dir="ltr">{id}</code>;
}

export function SettingValue({ k, value, lang }: { k: string; value: string | undefined; lang: Lang }) {
  if (value === undefined) return <span className="muted">{T(lang).notSet}</span>;
  return isProse(k) ? <bdi>{value}</bdi> : <code dir="ltr">{value}</code>;
}

export function SourceNote({ lang, source }: { lang: Lang; source: Record<string, string | number> }) {
  return <p className="note"><Tpl text={T(lang).source} values={source} /></p>;
}

/** One stage of an instance's pipeline. The state is always in words, never only a colour. */
export function StageCell({ stage, lang }: { stage: PipelineStage; lang: Lang }) {
  const s = T(lang);
  if (stage.state === "none") return <span className="ins-stage none">{s.stageNone}</span>;
  if (stage.state === "off") return <span className="ins-stage off">{s.stageOff}</span>;
  return (
    <span className="ins-stage on">
      {stage.family ? <><code dir="ltr">{stage.family}</code> <code dir="ltr">{stage.version}</code></> : s.stageOn}
    </span>
  );
}
