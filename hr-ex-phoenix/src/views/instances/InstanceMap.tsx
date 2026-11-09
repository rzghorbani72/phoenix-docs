import { memo, useMemo } from "react";
import {
  Background, Controls, Handle, MarkerType, Position, ReactFlow, ReactFlowProvider,
  type Edge, type Node, type NodeProps,
} from "@xyflow/react";
import type { Instance } from "../../lib/instanceTypes";
import type { PipelineStageId, StageDetail } from "../../lib/instances";
import { useNarrow } from "../../components/map/useNarrow";
import { T, type Lang } from "./i18n";
import { STAGE_LOOK, stepLook, stepWordText } from "./model";
import { highlights } from "./highlights";
import "../../components/map/map.css";

const W = 360, H = 330, GX = 130, GY = 90;
const COLS = 3;
/** Column and row of each step, written for LTR and mirrored for RTL. */
const SLOT: Record<PipelineStageId, [number, number]> = { call: [0, 0], brain: [1, 0], kb: [2, 0], analytics: [0, 1], ops: [1, 1] };
const FLOWS = [
  { from: "call", to: "brain", down: false, label: "call_brain" }, { from: "brain", to: "kb", down: false, label: "brain_kb" },
  { from: "call", to: "analytics", down: true, label: "call_analytics" }, { from: "brain", to: "ops", down: true, label: "brain_ops" },
] as const;

function StageCard({ detail, lang, from, owner }: { detail: StageDetail; lang: Lang; from?: Instance; owner: Instance }) {
  const s = T(lang);
  const { stage } = detail;
  const look = STAGE_LOOK[stage.id];
  const state = stepLook(detail);
  const word = stepWordText(state.word, lang);
  const rows = highlights(owner, detail, lang);
  const tag = stage.state === "none" ? s.stageNone : stage.state === "off" ? s.stageOff : stage.family ?? s.stageOn;
  return (
    <>
      <div className="ov-head">
        <span className="ov-prefix" aria-hidden="true">{look.letter}</span>
        <div className="ov-names">
          <div className="ov-short">{s.stages[stage.id]}</div>
          <div className="ov-tag"><bdi>{stage.state === "none" ? "" : tag}</bdi>{stage.version ? <> · <bdi>{stage.version}</bdi></> : null}</div>
          {from && <div className="ov-tag ins-from"><bdi>{from.name[lang]}</bdi></div>}
        </div>
      </div>
      <div className={`ins-step-status ${state.tone}`}>
        <span className="ins-light" aria-hidden="true" />
        <strong>{word}</strong>
      </div>
      {rows.length > 0 && (
        <dl className="ins-facts">
          {rows.map((r) => (
            <div key={r.label}><dt>{r.label}</dt><dd><code dir="ltr">{r.value}</code></dd></div>
          ))}
        </dl>
      )}
      {detail.components.length > 0 && (
        <div className="ins-card-foot">{detail.on}/{detail.components.length} {s.statParts} · {detail.replicas} {s.statReplicas}</div>
      )}
      <div className="ov-cta">{s.openStep} {lang === "fa" ? "←" : "→"}</div>
    </>
  );
}

type Step = { detail: StageDetail; owner: Instance };
type CardData = { detail: StageDetail; lang: Lang; selected: boolean; from?: Instance; owner: Instance };

const cardClass = (d: StageDetail, selected: boolean) =>
  `ovcard ins-node ins-node-${d.stage.state}${selected ? " ins-node-sel" : ""}`;

const StageNode = memo(function StageNode({ data }: NodeProps<Node<CardData>>) {
  return (
    <div className={cardClass(data.detail, data.selected)} style={{ ["--lc" as string]: STAGE_LOOK[data.detail.stage.id].color }}>
      <Handle type="source" id="r" position={Position.Right} /><Handle type="target" id="l" position={Position.Left} />
      <Handle type="source" id="l-out" position={Position.Left} /><Handle type="target" id="r-in" position={Position.Right} />
      <Handle type="source" id="b" position={Position.Bottom} /><Handle type="target" id="t" position={Position.Top} />
      <StageCard detail={data.detail} lang={data.lang} from={data.from} owner={data.owner} />
    </div>
  );
});

const nodeTypes = { stage: StageNode };

function build(steps: Step[], page: Instance, lang: Lang, selected?: string) {
  const details = steps.map((x) => x.detail);
  const rtl = lang === "fa";
  const s = T(lang);
  const nodes: Node[] = steps.map(({ detail, owner }) => {
    const [c, r] = SLOT[detail.stage.id];
    return {
      id: detail.stage.id, type: "stage", draggable: false, width: W, height: H, style: { width: W, height: H },
      position: { x: (rtl ? COLS - 1 - c : c) * (W + GX), y: r * (H + GY) },
      data: { detail, lang, selected: detail.stage.id === selected, from: owner.id === page.id ? undefined : owner, owner } satisfies CardData,
    };
  });
  const used = new Set(details.filter((d) => d.stage.state !== "none").map((d) => d.stage.id));
  const edges: Edge[] = FLOWS.filter((f) => used.has(f.from) && used.has(f.to)).map((f) => {
    const color = STAGE_LOOK[f.from].color;
    return {
      id: `${f.from}>${f.to}`, source: f.from, target: f.to, label: s.flows[f.label], animated: true,
      sourceHandle: f.down ? "b" : rtl ? "l-out" : "r", targetHandle: f.down ? "t" : rtl ? "r-in" : "l",
      className: "ovedge", style: { stroke: color, strokeWidth: 2.5 },
      labelBgPadding: [8, 4] as [number, number], labelBgBorderRadius: 6,
      markerEnd: { type: MarkerType.ArrowClosed, color, width: 18, height: 18 },
    };
  });
  return { nodes, edges };
}

interface Props {
  steps: Step[];
  page: Instance;
  lang: Lang;
  theme: "dark" | "light";
  selected?: PipelineStageId;
  onSelect: (id: PipelineStageId) => void;
}

/** This instance's pipeline: one card per step, drawn only with the hand-offs it actually has. */
export function InstanceMap({ steps, page, lang, theme, selected, onSelect }: Props) {
  const narrow = useNarrow();
  const { nodes, edges } = useMemo(() => build(steps, page, lang, selected), [steps, page, lang, selected]);
  if (narrow)
    return (
      <div className="ovlist ins-list">
        {steps.map(({ detail, owner }) => (
          <button key={detail.stage.id} type="button" className={cardClass(detail, detail.stage.id === selected)}
            style={{ ["--lc" as string]: STAGE_LOOK[detail.stage.id].color }} onClick={() => onSelect(detail.stage.id)}>
            <StageCard detail={detail} lang={lang} owner={owner} from={owner.id === page.id ? undefined : owner} />
          </button>
        ))}
      </div>
    );
  return (
    <div className="ins-map">
      <ReactFlowProvider>
        <ReactFlow
          className="overview" nodes={nodes} edges={edges} nodeTypes={nodeTypes} colorMode={theme}
          onNodeClick={(_, n) => onSelect(n.id as PipelineStageId)} fitView fitViewOptions={{ padding: { top: "24px", bottom: "24px", x: "24px" } }}
          nodesConnectable={false} elementsSelectable={false} edgesFocusable={false} minZoom={0.3} maxZoom={1.4}
          zoomOnScroll={false} preventScrolling={false} autoPanOnNodeFocus={false}
          proOptions={{ hideAttribution: true }}
        >
          <Background gap={24} size={1.2} />
          <Controls showInteractive={false} position={lang === "fa" ? "bottom-right" : "bottom-left"} />
        </ReactFlow>
      </ReactFlowProvider>
    </div>
  );
}
