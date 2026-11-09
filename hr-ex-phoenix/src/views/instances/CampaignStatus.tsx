import type { ReactNode } from "react";
import type { Instance, InstanceComponent } from "../../lib/instanceTypes";
import { campaignStatus, INSTANCES } from "../../lib/instances";
import { scoringPartWhy } from "./explain";
import { T, type Lang } from "./i18n";
import { replicaText } from "./model";
import { Tpl } from "./parts";

/** The campaign end and the snapshot date on one line, in the order they happened. */
function Timeline({ end, date, days, ended, lang }: { end: string; date: string; days: number; ended: boolean; lang: Lang }) {
  const s = T(lang);
  const first = ended ? { label: s.tlEnded, date: end } : { label: s.tlSnapshot, date };
  const last = ended ? { label: s.tlSnapshot, date } : { label: s.tlEnded, date: end };
  const gap = (ended ? s.tlDaysAfter : s.tlDaysBefore).replace("{days}", String(days));
  return (
    <div className={`ins-timeline${ended ? " over" : ""}`} role="group" aria-label={`${first.label} ${first.date}, ${gap}, ${last.label} ${last.date}`}>
      <div className="ins-tl-point"><span className="ins-tl-dot" aria-hidden="true" /><b>{first.label}</b><code dir="ltr">{first.date}</code></div>
      <div className="ins-tl-line"><span>{gap}</span></div>
      <div className="ins-tl-point"><span className="ins-tl-dot" aria-hidden="true" /><b>{last.label}</b><code dir="ltr">{last.date}</code></div>
    </div>
  );
}

function Part({ c, lang, why }: { c: InstanceComponent; lang: Lang; why: ReactNode }) {
  return (
    <li>
      <div className="ins-part-top"><code dir="ltr">{c.name}</code><span className="muted">{replicaText(c, lang)}</span></div>
      <p className="ins-why">{scoringPartWhy(lang, c.name)}</p>
      <p className="ins-why">{why}</p>
    </li>
  );
}

/** For a campaign: which parts are still going and which have ended, with the reason for each. */
export function CampaignStatus({ inst, lang }: { inst: Instance; lang: Lang }) {
  const status = campaignStatus(inst);
  if (!status) return null;
  const s = T(lang);
  const date = INSTANCES.source.date;
  const stoppedWhy = (c: InstanceComponent) =>
    c.neverRuns && c.schedule ? <Tpl text={s.campaignNeverRuns} values={{ schedule: c.schedule }} /> : s.campaignZero;
  const remainingWhy = (c: InstanceComponent) =>
    c.schedule ? <Tpl text={s.campaignScheduled} values={{ schedule: c.schedule }} /> : null;
  return (
    <section className="ins-campaign">
      <h2 className="ins-h">{s.campaignTitle}</h2>
      <Timeline end={status.end.slice(0, 10)} date={date} days={Math.abs(status.daysSinceEnd)} ended={status.ended} lang={lang} />
      <div className="ins-campaign-groups">
        <div className={`ins-campaign-group ${status.ended ? "attention" : "open"}`}>
          <h3 className="ins-sub">{status.ended ? s.campaignRemainEnded : s.campaignRemainOpen} · {status.remaining.length}</h3>
          {status.ended && !!status.remaining.length && <p className="muted">{s.campaignRemainEndedHint}</p>}
          {status.remaining.length
            ? <ul className="ins-parts">{status.remaining.map((c) => <Part key={c.name} c={c} lang={lang} why={remainingWhy(c)} />)}</ul>
            : <p className="muted">{s.campaignNothing}</p>}
        </div>
        <div className="ins-campaign-group stopped">
          <h3 className="ins-sub">{s.campaignStopped} · {status.stopped.length}</h3>
          <p className="muted">{s.campaignStoppedHint}</p>
          <ul className="ins-parts">{status.stopped.map((c) => <Part key={c.name} c={c} lang={lang} why={stoppedWhy(c)} />)}</ul>
        </div>
      </div>
    </section>
  );
}
