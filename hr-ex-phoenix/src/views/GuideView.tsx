import type { Data } from "../lib/types";
import { ctxFor } from "../lib/md";
import { BodyView, Md } from "../components/Blocks";
import { EnTag } from "../components/Common";

export function GuideView({ d }: { d: Data }) {
  const g = d.guide;
  const ctx = ctxFor(d, 0);
  if (!g) return null;
  const jump = (i: number) => document.getElementById(`g${i}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
  return (
    <div className="page guide">
      <nav className="toc">
        {g.sections.map(([h], i) => <button key={i} onClick={() => jump(i)}><span>{i + 1}</span><Md text={h} ctx={ctx} /></button>)}
      </nav>
      <div>
        <h1><Md text={g.title} ctx={ctx} /> {g.fallback && <EnTag d={d} />}</h1>
        <Md as="p" text={g.lede} ctx={ctx} />
        {g.sections.map(([h, b], i) => (
          <section className="sec" id={`g${i}`} key={i}><h3><Md text={h} ctx={ctx} /></h3><BodyView body={b} ctx={ctx} /></section>
        ))}
      </div>
    </div>
  );
}
