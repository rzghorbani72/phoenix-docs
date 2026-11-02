import type { Data, Page } from "../lib/types";
import { ctxFor } from "../lib/md";
import { Md } from "./Blocks";

export const go = (h: string) => { window.location.hash = h; };

export function Facts({ page, d, depth }: { page: Page; d: Data; depth: 0 | 1 }) {
  const ctx = ctxFor(d, depth);
  if (!page.facts?.length) return null;
  return (
    <div className="facts">
      {page.facts.map(([k, v], i) => (
        <div className="fact" key={i}><div className="k"><Md text={k} ctx={ctx} /></div><div className="v"><Md text={v} ctx={ctx} /></div></div>
      ))}
    </div>
  );
}

export const EnTag = ({ d }: { d: Data }) => (d.lang === "fa" ? <span className="entag">English</span> : null);
