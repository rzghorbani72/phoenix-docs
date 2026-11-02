import { useEffect, useMemo, useState } from "react";
import {
  Background, Controls, Handle, MiniMap, Position, ReactFlow, ReactFlowProvider, useReactFlow,
  type Edge, type Node, type NodeProps,
} from "@xyflow/react";
import type { Data, Status } from "../../lib/types";
import { plain } from "../../lib/md";

export const LANE_COLOR: Record<string, string> = {
  teal: "var(--c-teal)", violet: "var(--c-violet)", orange: "var(--c-orange)", pink: "var(--c-pink)",
  cyan: "var(--c-cyan)", blue: "var(--c-blue)", green: "var(--c-green)",
};

// Layout: lanes stacked vertically, steps snake through rows so wrap edges stay short.
const NW = 236, NH = 116, GX = 56, GY = 52, PAD = 28, HEAD = 104, PER_ROW = 6, LANE_GAP = 80;
const INNER_W = PER_ROW * NW + (PER_ROW - 1) * GX;

// Solid colours for the minimap (SVG fill attributes cannot use CSS variables).
const HEX: Record<string, string> = { teal: "#14b8a6", violet: "#8b5cf6", orange: "#f97316", pink: "#ec4899", cyan: "#06b6d4", blue: "#3b82f6", green: "#22c55e" };

// Hand-off points between lanes; the label explains what crosses.
const CROSS: { from: string; to: string; en: string; fa: string }[] = [
  { from: "v-aiva", to: "b-setup", en: "each user turn", fa: "هر نوبت کاربر" },
  { from: "b-react", to: "v-tts", en: "streamed answer → TTS", fa: "پاسخ استریم → TTS" },
  { from: "b-retrieve", to: "k-search", en: "embed + search", fa: "embedding + جست‌وجو" },
  { from: "k-carry", to: "b-react", en: "approved contexts", fa: "زمینه‌های تأییدشده" },
  { from: "b-setup", to: "m-history", en: "history · memory", fa: "سابقه · حافظه" },
  { from: "v-summary", to: "a-ingest", en: "Kafka summary + .ogg", fa: "خلاصه Kafka + .ogg" },
  { from: "f-aiva", to: "b-setup", en: "aiva is built on agentlib", fa: "aiva روی agentlib ساخته شده" },
];

type StepData = {
  num: string; title: string; chip: string; status: Status; statusLabel: string; color: string;
  dim: boolean; hl: boolean; rtl: boolean; fallback: boolean; hex: string;
};
type LaneData = { title: string; desc: string; color: string; count: string; hex: string };

function StepNode({ data, selected }: NodeProps<Node<StepData>>) {
  const fwd = data.rtl ? Position.Left : Position.Right;
  const back = data.rtl ? Position.Right : Position.Left;
  return (
    <div className={`fnode${data.dim ? " dim" : ""}${data.hl ? " hl" : ""}${selected ? " sel" : ""}`} style={{ ["--lc" as string]: data.color }}>
      <Handle type="target" position={back} id="in-back" />
      <Handle type="source" position={fwd} id="out-fwd" />
      <Handle type="target" position={fwd} id="in-fwd" />
      <Handle type="source" position={back} id="out-back" />
      <Handle type="target" position={Position.Top} id="in-top" />
      <Handle type="source" position={Position.Bottom} id="out-bottom" />
      <div className="fnode-head"><span className="fnode-num">{data.num}</span><span className={`dot s-${data.status}`} title={data.statusLabel} /></div>
      <div className="fnode-title">{data.title}</div>
      <div className="fnode-chip">{data.chip}</div>
      {data.fallback && <span className="fnode-en">EN</span>}
    </div>
  );
}

function LaneNode({ data }: NodeProps<Node<LaneData>>) {
  return (
    <div className="flane" style={{ ["--lc" as string]: data.color }}>
      <div className="flane-head"><strong>{data.title}</strong><span>{data.count}</span></div>
      <div className="flane-desc">{data.desc}</div>
    </div>
  );
}

const nodeTypes = { step: StepNode, lane: LaneNode };

export interface MapFilters { model: string; statuses: Set<Status>; query: string; cross: boolean }

function build(d: Data, f: MapFilters, selected: string | undefined) {
  const rtl = d.dir === "rtl";
  const modelSteps = f.model ? new Set(d.models.cards.find((c) => c.id === f.model)?.steps ?? []) : null;
  const q = f.query.trim().toLowerCase();
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const boxes: Record<string, { x: number; y: number; width: number; height: number }> = {};
  let y = 0;
  const laneW = INNER_W + 2 * PAD;
  for (const lane of d.lanes) {
    const rows = Math.ceil(lane.steps.length / PER_ROW);
    const h = HEAD + rows * NH + (rows - 1) * GY + PAD;
    const color = LANE_COLOR[lane.color] ?? "var(--accent)";
    boxes[`lane:${lane.id}`] = { x: 0, y, width: laneW, height: h };
    nodes.push({
      id: `lane:${lane.id}`, type: "lane", position: { x: 0, y }, draggable: false, selectable: false,
      width: laneW, height: h, style: { width: laneW, height: h }, zIndex: -1,
      data: { hex: HEX[lane.color] ?? "#888", title: plain(lane.title), desc: plain(lane.desc), color, count: `${lane.steps.length} ${d.ui.steps_word}` },
    });
    lane.steps.forEach((sid, i) => {
      const s = d.steps[sid];
      const row = Math.floor(i / PER_ROW);
      let col = i % PER_ROW;
      if (row % 2 === 1) col = PER_ROW - 1 - col;
      if (rtl) col = PER_ROW - 1 - col;
      const hay = `${s.title} ${s.chip ?? ""} ${s.summary}`.toLowerCase();
      const pass = (!modelSteps || modelSteps.has(sid)) && f.statuses.has(s.status) && (!q || hay.includes(q));
      boxes[sid] = { x: PAD + col * (NW + GX), y: y + HEAD + row * (NH + GY), width: NW, height: NH };
      nodes.push({
        id: sid, type: "step", parentId: `lane:${lane.id}`, extent: "parent", draggable: false,
        position: { x: PAD + col * (NW + GX), y: HEAD + row * (NH + GY) },
        width: NW, height: NH, style: { width: NW, height: NH }, selected: sid === selected,
        data: {
          num: `${lane.prefix}${i + 1}`, title: plain(s.title), chip: plain(s.chip ?? ""), status: s.status,
          statusLabel: d.ui.status[s.status], color, rtl, hex: HEX[lane.color] ?? "#888", fallback: !!s.fallback,
          dim: !pass, hl: pass && (!!modelSteps || !!q),
        } satisfies StepData,
      });
      if (i > 0) {
        const prevRow = Math.floor((i - 1) / PER_ROW);
        const wrap = prevRow !== row;
        // Even rows run in reading direction, odd rows run back (snake).
        const forward = prevRow % 2 === 0;
        edges.push({
          id: `e:${lane.steps[i - 1]}>${sid}`, source: lane.steps[i - 1], target: sid, type: "smoothstep",
          sourceHandle: wrap ? "out-bottom" : forward ? "out-fwd" : "out-back",
          targetHandle: wrap ? "in-top" : forward ? "in-back" : "in-fwd",
          style: { stroke: color, strokeWidth: 2 }, markerEnd: { type: "arrowclosed" as never, color },
        });
      }
    });
    y += h + LANE_GAP;
  }
  const selLane = selected ? d.lanes.find((l) => l.steps.includes(selected)) : undefined;
  {
    for (const c of CROSS) {
      if (!d.steps[c.from] || !d.steps[c.to]) continue;
      if (!f.cross && !(selLane && (selLane.steps.includes(c.from) || selLane.steps.includes(c.to)))) continue;
      edges.push({
        id: `x:${c.from}>${c.to}`, source: c.from, target: c.to, type: "default", animated: true,
        sourceHandle: "out-bottom", targetHandle: "in-top", label: d.lang === "fa" ? c.fa : c.en,
        className: "xedge", markerEnd: { type: "arrowclosed" as never }, zIndex: 5,
      });
    }
  }
  return { nodes, edges, boxes };
}

const PANEL_W = 620;

function Canvas({ d, filters, selected, lane, onOpen, theme }: Props) {
  const rf = useReactFlow();
  const [inited, setInited] = useState(false);
  const { nodes, edges, boxes } = useMemo(() => build(d, filters, selected), [d, filters, selected]);
  // Camera from our own layout boxes (no dependence on DOM measurement): a selected step is centred in the
  // part of the canvas the detail panel leaves visible; a lane fills the view; default = first two lanes.
  useEffect(() => {
    if (!inited) return;
    const union = (ids: string[]) => {
      const bs = ids.map((i) => boxes[i]).filter(Boolean);
      const x = Math.min(...bs.map((b) => b.x)), y = Math.min(...bs.map((b) => b.y));
      return { x, y, width: Math.max(...bs.map((b) => b.x + b.width)) - x, height: Math.max(...bs.map((b) => b.y + b.height)) - y };
    };
    const t = setTimeout(() => {
      if (selected && boxes[selected]) {
        const b = boxes[selected], zoom = 0.95;
        const shift = Math.min(PANEL_W, window.innerWidth * 0.6) / 2 / zoom;
        rf.setCenter(b.x + b.width / 2 + (d.dir === "rtl" ? -shift : shift), b.y + b.height / 2, { zoom, duration: 500 });
      } else if (lane === "all") rf.fitBounds(union(Object.keys(boxes).filter((k) => k.startsWith("lane:"))), { padding: 0.03, duration: 500 });
      else if (lane && boxes[`lane:${lane}`]) rf.fitBounds(boxes[`lane:${lane}`], { padding: 0.06, duration: 600 });
      else rf.fitBounds(union([`lane:${d.lanes[0].id}`, `lane:${d.lanes[1].id}`]), { padding: 0.05, duration: 300 });
    }, 20);
    return () => clearTimeout(t);
    // boxes only change with language/filters; camera should not jump when filters change
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [inited, selected, lane, d.lang]);
  return (
    <ReactFlow
      nodes={nodes} edges={edges} nodeTypes={nodeTypes} colorMode={theme}
      onNodeClick={(_, n) => n.type === "step" && onOpen(n.id)}
      onInit={() => setInited(true)} nodesConnectable={false} minZoom={0.08} maxZoom={2} proOptions={{ hideAttribution: true }}
    >
      <Background gap={24} size={1.2} />
      <Controls showInteractive={false} position={d.dir === "rtl" ? "bottom-right" : "bottom-left"} />
      <MiniMap pannable zoomable position={d.dir === "rtl" ? "bottom-left" : "bottom-right"} maskColor="rgba(120,140,170,.18)"
        nodeColor={(n) => (n.type === "lane" ? "transparent" : (n.data as StepData).hex)}
        nodeStrokeColor={(n) => (n.type === "lane" ? (n.data as LaneData).hex : "transparent")} nodeStrokeWidth={8} />
    </ReactFlow>
  );
}

interface Props {
  d: Data; filters: MapFilters; selected?: string; lane?: string; theme: "dark" | "light";
  onOpen: (id: string) => void;
}

export default function MapView(p: Props) {
  return <ReactFlowProvider><Canvas {...p} /></ReactFlowProvider>;
}
