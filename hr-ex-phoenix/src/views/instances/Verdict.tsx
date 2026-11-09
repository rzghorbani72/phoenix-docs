import type { Instance } from "../../lib/instanceTypes";
import { campaignStatus, isStopped } from "../../lib/instances";
import { T, type Lang } from "./i18n";
import { Tpl } from "./parts";

const SHOWN = 4;
const names = (list: string[]) => list.slice(0, SHOWN).join(", ") + (list.length > SHOWN ? ` +${list.length - SHOWN}` : "");

/** The answer to "is it OK?" as one sentence that names what is off. */
export function Verdict({ inst, lang }: { inst: Instance; lang: Lang }) {
  const s = T(lang);
  const parts = inst.components;
  const stopped = parts.filter(isStopped);
  const campaign = campaignStatus(inst);
  let tone: "ok" | "warn" | "off" = "ok";
  let line;
  if (inst.state === "off") {
    tone = "off";
    line = s.verdictOff;
  } else if (campaign?.ended && campaign.remaining.length) {
    tone = "warn";
    line = <Tpl text={s.verdictCampaignOver} values={{ parts: names(campaign.remaining.map((c) => c.name)) }} />;
  } else if (stopped.length) {
    line = <Tpl text={s.verdictPartly} values={{ on: parts.length - stopped.length, total: parts.length, parts: names(stopped.map((c) => c.name)) }} />;
  } else {
    line = <Tpl text={s.verdictAllOn} values={{ total: parts.length }} />;
  }
  return (
    <div className={`ins-verdict ${tone}`}>
      <div className="ins-verdict-line">{line}</div>
    </div>
  );
}
