import type { Instance } from "../../lib/instanceTypes";
import { isStopped, type StageDetail } from "../../lib/instances";
import { T, type Lang } from "./i18n";
import { replicaText } from "./model";
import { stepGraph, type GraphNode } from "./stepGraph";

function Node({ node, lang }: { node: GraphNode; lang: Lang }) {
  const off = !!node.part && isStopped(node.part);
  return (
    <div className={`ins-flow-node ${node.kind}${off ? " off" : ""}`}>
      <div className="ins-flow-title">{node.title[lang]}</div>
      {node.value && <code dir="ltr">{node.value}</code>}
      {node.part && <div className="ins-flow-sub">{replicaText(node.part, lang)}</div>}
    </div>
  );
}

/** This instance's own version of the step, in the order things happen. */
export function StepDiagram({ inst, detail, lang }: { inst: Instance; detail: StageDetail; lang: Lang }) {
  const layers = stepGraph(inst, detail);
  if (!layers.length) return null;
  const s = T(lang);
  return (
    <section>
      <h3 className="ins-h">{s.stepFlow}</h3>
      <ol className="ins-flow">
        {layers.map((layer, i) => (
          <li key={i}>
            {i > 0 && <div className="ins-flow-arrow" aria-hidden="true">↓{layer.flow ? ` ${layer.flow[lang]}` : ""}</div>}
            {i > 0 && layer.flow && <span className="sr-only">{layer.flow[lang]}</span>}
            <div className="ins-flow-row">{layer.nodes.map((n) => <Node key={n.id} node={n} lang={lang} />)}</div>
          </li>
        ))}
      </ol>
    </section>
  );
}
