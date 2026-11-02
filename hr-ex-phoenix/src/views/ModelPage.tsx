import type { Data } from "../lib/types";
import { laneOf } from "../lib/data";
import { ctxFor, plain } from "../lib/md";
import { Badge, Md, Sections } from "../components/Blocks";
import { EnTag, Facts } from "../components/Common";

export function ModelPage({ d, id }: { d: Data; id: string }) {
  const m = d.models.pages[id];
  const card = d.models.cards.find((c) => c.id === id);
  const fa = d.lang === "fa";
  if (!m || !card)
    return (
      <div className="page">
        <a className="link" href="#/models">{d.ui.nav_models}</a>
        <h1>{fa ? "مدل پیدا نشد" : "Model not found"}</h1>
        <p><code>{id}</code></p>
      </div>
    );
  const ctx = ctxFor(d, 1);
  const order = d.models.cards.map((c) => c.id).filter((x): x is string => !!x && !!d.models.pages[x]);
  const i = order.indexOf(id);
  const titleOf = (x: string) => plain(d.models.pages[x].title_plain ?? d.models.pages[x].title);
  // A page still in English inside the Persian build is marked as such for screen readers and layout.
  const langProps = m.fallback && fa ? { lang: "en", dir: "ltr" as const } : {};
  return (
    <div className="page">
      <a className="link" href="#/models">{d.ui.back_models ?? d.ui.nav_models}</a>
      <article {...langProps}>
        <h1><Md text={m.title} ctx={ctx} /></h1>
        <div className="row"><Badge status={m.status} label={d.ui.status[m.status]} /><span className="size"><Md text={card.size} ctx={ctx} /></span>{m.fallback && <EnTag d={d} />}</div>
        <Md as="p" text={m.summary} ctx={ctx} />
        {!!card.steps?.length && (
          <div className="steps-row">
            <span className="muted">{d.ui.used_in}:</span>
            {card.steps.map((s) => {
              const w = laneOf(d, s);
              return w ? <a key={s} className="spill wide" href={`#/step/${s}`}>{w.lane.prefix}{w.num} · {plain(d.steps[s].title_plain ?? d.steps[s].title)}</a> : null;
            })}
          </div>
        )}
        <Facts page={m} d={d} depth={1} />
        <Sections sections={m.sections} ctx={ctx} level={2} />
      </article>
      <nav className="pn" aria-label={fa ? "مدل قبلی و بعدی" : "Previous and next model"}>
        {i > 0 ? <a rel="prev" href={`#/model/${order[i - 1]}`}>{d.ui.prev} {titleOf(order[i - 1])}</a> : <span />}
        {i >= 0 && i < order.length - 1 ? <a rel="next" href={`#/model/${order[i + 1]}`}>{titleOf(order[i + 1])} {d.ui.next}</a> : <span />}
      </nav>
    </div>
  );
}
