import type { Body, Status } from "../types";
import { md, type LinkCtx } from "../md";

export function Md({ text, ctx, as = "span" }: { text: string; ctx: LinkCtx; as?: "span" | "p" | "div" }) {
  const Tag = as;
  return <Tag dangerouslySetInnerHTML={{ __html: md(text, ctx) }} />;
}

/** Renders one section body in the same formats the static site supports. */
export function BodyView({ body, ctx }: { body: Body; ctx: LinkCtx }) {
  if (typeof body === "string")
    return <>{body.split("\n\n").map((p, i) => <Md key={i} as="p" text={p} ctx={ctx} />)}</>;
  if (Array.isArray(body))
    return <ul>{body.map((b, i) => <li key={i}><Md text={b} ctx={ctx} /></li>)}</ul>;
  if ("multi" in body) return <>{body.multi.map((b, i) => <BodyView key={i} body={b} ctx={ctx} />)}</>;
  if ("table" in body) {
    const [head, ...rows] = body.table;
    return (
      <div className="tw">
        <table>
          <thead><tr>{head.map((c, i) => <th key={i}><Md text={c} ctx={ctx} /></th>)}</tr></thead>
          <tbody>{rows.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j}><Md text={c} ctx={ctx} /></td>)}</tr>)}</tbody>
        </table>
      </div>
    );
  }
  if ("ol" in body) return <ol>{body.ol.map((b, i) => <li key={i}><Md text={b} ctx={ctx} /></li>)}</ol>;
  if ("code" in body) return <pre><code>{body.code}</code></pre>;
  return <div className={`note ${body.kind ?? ""}`}><Md text={body.note} ctx={ctx} /></div>;
}

export function Badge({ status, label }: { status: Status; label: string }) {
  return <span className={`badge s-${status}`}>{label}</span>;
}

export function Sections({ sections, ctx }: { sections: [string, Body][]; ctx: LinkCtx }) {
  return (
    <>
      {sections.map(([h, b], i) => (
        <section className="sec" key={i}>
          <h3><Md text={h} ctx={ctx} /></h3>
          <BodyView body={b} ctx={ctx} />
        </section>
      ))}
    </>
  );
}
