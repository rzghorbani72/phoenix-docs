import { useMemo } from "react";
import { INSTANCES, STAGE_IDS, byId, connectedPipeline, stageDetail, type PipelineStageId } from "../../lib/instances";
import { T, type Lang } from "./i18n";
import { InstanceMap } from "./InstanceMap";
import { CampaignStatus } from "./CampaignStatus";
import { Verdict } from "./Verdict";
import { ConfirmMark, SourceNote, StateChip } from "./parts";
import { StagePanel } from "./StagePanel";
import { Surfaces } from "./Surfaces";
import "./instances.css";

interface Props { lang: Lang; id: string; stage?: string; theme?: "dark" | "light" }

export function InstancePage({ lang, id, stage, theme = "dark" }: Props) {
  const s = T(lang);
  const inst = byId(id);
  const steps = useMemo(() => (inst ? connectedPipeline(inst).map(({ stage, owner }) => ({ owner, detail: stageDetail(owner, stage) })) : []), [inst]);
  if (!inst)
    return (
      <div className="page ins">
        <a className="link" href="#/instances">{s.back}</a>
        <h1>{s.notFound}</h1>
        <p><code dir="ltr">{id}</code></p>
      </div>
    );
  const selected = STAGE_IDS.find((x) => x === stage);
  const open = steps.find((x) => x.detail.stage.id === selected);
  const select = (x: PipelineStageId) => { window.location.hash = `#/instance/${inst.id}/${x}`; };
  return (
    <div className="page ins ins-page">
      <a className="link" href="#/instances">{s.back}</a>
      <h1>{inst.name[lang]}</h1>
      <div className="row"><StateChip state={inst.state} lang={lang} /><span className="chip">{s.categories[inst.category]}</span><ConfirmMark inst={inst} lang={lang} /></div>
      <p>{inst.about[lang]}</p>
      <div className="ins-release">{s.release}: {inst.releases.map((r) => <code key={r} dir="ltr">{r}</code>)}</div>
      <Verdict inst={inst} lang={lang} />
      <Surfaces inst={inst} lang={lang} />
      <SourceNote lang={lang} source={INSTANCES.source} />

      <h2 className="ins-h">{s.pipeline}</h2>
      <p className="muted">{s.selectStep}</p>
      <InstanceMap steps={steps} page={inst} lang={lang} theme={theme} selected={selected} onSelect={select} />

      <CampaignStatus inst={inst} lang={lang} />

      {open && <StagePanel inst={open.owner} pageId={inst.id} detail={open.detail} lang={lang} theme={theme} />}
    </div>
  );
}
