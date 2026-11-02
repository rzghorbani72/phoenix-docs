import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  BaseEdge, Background, Controls, EdgeLabelRenderer, Handle, MarkerType, MiniMap, Position, ReactFlow, ReactFlowProvider, useReactFlow,
  type Edge, type EdgeProps, type Node, type NodeMouseHandler, type NodeProps,
} from "@xyflow/react";
import type { Data, Status } from "../../lib/types";
import { plain } from "../../lib/md";
import { CROSS, HEX, LANE_COLOR, type MapFilters } from "./shared";
import { NodeTip, type TipApi } from "./NodeTip";
import { isNarrow } from "./useNarrow";
import "./map.css";

export { CROSS, LANE_COLOR, type MapFilters } from "./shared";

// Layout: lanes stacked vertically, steps snake through rows so wrap edges stay short.
const NW = 236, NH = 116, GX = 56, GY = 52, PAD = 28, HEAD = 104, PER_ROW = 6, LANE_GAP = 80;
const INNER_W = PER_ROW * NW + (PER_ROW - 1) * GX;
const LANE_W = INNER_W + 2 * PAD;
/** Hand-off edges run in gutters outside the lanes; this is how far the outermost one (and its label) reaches. */
const GUTTER = 300;

type StepData = {
  num: string; title: string; chip: string; status: Status; statusLabel: string; color: string;
  dim: boolean; hl: boolean; rtl: boolean; fallback: boolean; hex: string; onTour: boolean; offTour: boolean;
};
type LaneData = { title: string; desc: string; color: string; count: string; hex: string };
type CrossData = { path: string; lx: number; ly: number; side: "l" | "r"; label: string; active: boolean };
type Box = { x: number; y: number; width: number; height: number };

const StepNode = memo(function StepNode({ data, selected }: NodeProps<Node<StepData>>) {
  const fwd = data.rtl ? Position.Left : Position.Right;
  const back = data.rtl ? Position.Right : Position.Left;
  const cls = `fnode${data.dim ? " dim" : ""}${data.hl ? " hl" : ""}${selected ? " sel" : ""}${data.onTour ? " tour" : ""}${data.offTour ? " offtour" : ""}`;
  return (
    <div className={cls} style={{ ["--lc" as string]: data.color }}>
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
});

const LaneNode = memo(function LaneNode({ data }: NodeProps<Node<LaneData>>) {
  return (
    <div className="flane" style={{ ["--lc" as string]: data.color }}>
      <div className="flane-head"><strong>{data.title}</strong><span>{data.count}</span></div>
      <div className="flane-desc">{data.desc}</div>
    </div>
  );
});

/** A hand-off edge with a precomputed orthogonal route; hovering the line or its label highlights both. */
const CrossEdge = memo(function CrossEdge({ id, data, markerEnd }: EdgeProps<Edge<CrossData>>) {
  const [hover, setHover] = useState(false);
  if (!data) return null;
  const on = { onMouseEnter: () => setHover(true), onMouseLeave: () => setHover(false) };
  const state = `${hover ? " hover" : ""}${data.active ? " active" : ""}`;
  return (
    <>
      <g className={`xroute${state}`} {...on}>
        <BaseEdge id={id} path={data.path} markerEnd={markerEnd} interactionWidth={24} />
      </g>
      <EdgeLabelRenderer>
        <div className={`xlabel nodrag nopan ${data.side}${state}`} {...on}
          style={{ transform: `translate(${data.side === "l" ? "-100%" : "0"}, -50%) translate(${data.lx}px, ${data.ly}px)` }}>
          {data.label}
        </div>
      </EdgeLabelRenderer>
    </>
  );
});

const nodeTypes = { step: StepNode, lane: LaneNode };
const edgeTypes = { cross: CrossEdge };

/** Polyline through `pts` with rounded corners. */
function rounded(pts: [number, number][], r: number) {
  let p = `M${pts[0][0]},${pts[0][1]}`;
  for (let i = 1; i < pts.length - 1; i++) {
    const [ax, ay] = pts[i - 1], [bx, by] = pts[i], [cx, cy] = pts[i + 1];
    const d1 = Math.hypot(bx - ax, by - ay), d2 = Math.hypot(cx - bx, cy - by);
    if (d1 < 0.5 || d2 < 0.5) continue;
    const r1 = Math.min(r, d1 / 2), r2 = Math.min(r, d2 / 2);
    p += ` L${bx - ((bx - ax) / d1) * r1},${by - ((by - ay) / d1) * r1} Q${bx},${by} ${bx + ((cx - bx) / d2) * r2},${by + ((cy - by) / d2) * r2}`;
  }
  const [lx, ly] = pts[pts.length - 1];
  return `${p} L${lx},${ly}`;
}

type Meta = { box: Box; lane: number; row: number; rows: number };

/**
 * Route every hand-off once per layout: leave the step through the row gap next to it, run to the
 * nearer outer gutter (left or right of all lanes), travel along the gutter to the target lane and
 * enter the target through its row gap. Nothing crosses a step box; parallel routes get offsets.
 */
function routeCross(meta: Record<string, Meta>, lang: "en" | "fa") {
  const valid = CROSS.filter((c) => meta[c.from] && meta[c.to]);
  const ports: Record<string, string[]> = {};
  const plan = valid.map((c) => {
    const S = meta[c.from], T = meta[c.to];
    const down = T.lane > S.lane;
    const sSide = down ? "b" : "t", tSide = down ? "t" : "b";
    (ports[`${c.from}:${sSide}`] ??= []).push(`${c.from}>${c.to}`);
    (ports[`${c.to}:${tSide}`] ??= []).push(`${c.from}>${c.to}`);
    return { c, S, T, down, sSide, tSide };
  });
  const sideCount = { l: 0, r: 0 };
  const placed: Record<"l" | "r", number[]> = { l: [], r: [] };
  const out: Record<string, CrossData> = {};
  plan.forEach(({ c, S, T, down, sSide, tSide }, i) => {
    const key = `${c.from}>${c.to}`;
    const off = (port: string) => { const l = ports[port]; return (l.indexOf(key) - (l.length - 1) / 2) * 48; };
    const sx = S.box.x + S.box.width / 2 + off(`${c.from}:${sSide}`);
    const tx = T.box.x + T.box.width / 2 + off(`${c.to}:${tSide}`);
    const jitter = ((i % 3) - 1) * 5;
    const chan = (m: Meta, bottom: boolean) => bottom
      ? m.box.y + m.box.height + (m.row === m.rows - 1 ? PAD / 2 : GY / 2 + jitter)
      : m.box.y - (m.row === 0 ? 10 : GY / 2 + jitter);
    const sy = down ? S.box.y + S.box.height : S.box.y;
    const ty = down ? T.box.y : T.box.y + T.box.height;
    const yS = chan(S, down), yT = chan(T, !down);
    const side: "l" | "r" = sx + tx <= LANE_W ? "l" : "r";
    const k = sideCount[side]++;
    const gx = side === "l" ? -40 - k * 22 : LANE_W + 40 + k * 22;
    let ly = (yS + yT) / 2;
    while (placed[side].some((p) => Math.abs(p - ly) < 30)) ly += 32;
    placed[side].push(ly);
    out[key] = {
      path: rounded([[sx, sy], [sx, yS], [gx, yS], [gx, yT], [tx, yT], [tx, ty]], 14),
      lx: side === "l" ? gx - 10 : gx + 10, ly, side, label: lang === "fa" ? c.fa : c.en, active: false,
    };
  });
  return out;
}

function build(d: Data, f: MapFilters, selected: string | undefined, tour: string[] | undefined, allCross: boolean) {
  const rtl = d.dir === "rtl";
  const modelSteps = f.model ? new Set(d.models.cards.find((c) => c.id === f.model)?.steps ?? []) : null;
  const q = f.query.trim().toLowerCase();
  const tourSet = tour ? new Set(tour) : null;
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const boxes: Record<string, Box> = {};
  const meta: Record<string, Meta> = {};
  let y = 0;
  d.lanes.forEach((lane, li) => {
    const rows = Math.ceil(lane.steps.length / PER_ROW);
    const h = HEAD + rows * NH + (rows - 1) * GY + PAD;
    const color = LANE_COLOR[lane.color] ?? "var(--accent)";
    boxes[`lane:${lane.id}`] = { x: 0, y, width: LANE_W, height: h };
    nodes.push({
      id: `lane:${lane.id}`, type: "lane", position: { x: 0, y }, draggable: false, selectable: false, focusable: false,
      width: LANE_W, height: h, style: { width: LANE_W, height: h }, zIndex: -1,
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
      const box = { x: PAD + col * (NW + GX), y: y + HEAD + row * (NH + GY), width: NW, height: NH };
      boxes[sid] = box;
      meta[sid] = { box, lane: li, row, rows };
      nodes.push({
        id: sid, type: "step", parentId: `lane:${lane.id}`, extent: "parent", draggable: false,
        position: { x: box.x, y: box.y - y },
        width: NW, height: NH, style: { width: NW, height: NH }, selected: sid === selected,
        data: {
          num: `${lane.prefix}${i + 1}`, title: plain(s.title), chip: plain(s.chip ?? ""), status: s.status,
          statusLabel: d.ui.status[s.status], color, rtl, hex: HEX[lane.color] ?? "#888", fallback: !!s.fallback,
          dim: !pass, hl: pass && (!!modelSteps || !!q),
          onTour: !!tourSet?.has(sid), offTour: !!tourSet && !tourSet.has(sid),
        } satisfies StepData,
      });
      if (i > 0) {
        const prevRow = Math.floor((i - 1) / PER_ROW);
        const wrap = prevRow !== row;
        // Even rows run in reading direction, odd rows run back (snake).
        const forward = prevRow % 2 === 0;
        edges.push({
          id: `e:${lane.steps[i - 1]}>${sid}`, source: lane.steps[i - 1], target: sid, type: "smoothstep", focusable: false,
          sourceHandle: wrap ? "out-bottom" : forward ? "out-fwd" : "out-back",
          targetHandle: wrap ? "in-top" : forward ? "in-back" : "in-fwd",
          className: tourSet && !(tourSet.has(sid) && tourSet.has(lane.steps[i - 1])) ? "offtour" : undefined,
          style: { stroke: color, strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color },
        });
      }
    });
    y += h + LANE_GAP;
  });
  const routes = routeCross(meta, d.lang);
  const selLane = selected ? d.lanes.find((l) => l.steps.includes(selected)) : undefined;
  for (const c of CROSS) {
    const r = routes[`${c.from}>${c.to}`];
    if (!r) continue;
    const show = tourSet
      ? (tourSet.has(c.from) || c.from === "k-carry") && tourSet.has(c.to)
      : f.cross || allCross || (selLane && (selLane.steps.includes(c.from) || selLane.steps.includes(c.to)));
    if (!show) continue;
    const active = !!selected && (c.from === selected || c.to === selected);
    edges.push({
      id: `x:${c.from}>${c.to}`, source: c.from, target: c.to, type: "cross", animated: true, focusable: false,
      sourceHandle: "out-bottom", targetHandle: "in-top", className: `xedge${active ? " active" : ""}`,
      data: { ...r, active }, markerEnd: { type: MarkerType.ArrowClosed, color: "var(--accent)", width: 16, height: 16 }, zIndex: 5,
    });
  }
  return { nodes, edges, boxes };
}

const PANEL_W = 620;
/** Fitted content keeps clear of the floating toolbar at the top (px). */
const FIT_TOP = 70, FIT_BOTTOM = 18, FIT_X = 28;

function Canvas({ d, filters, selected, lane, onOpen, theme, tour }: Props) {
  const rf = useReactFlow();
  const [inited, setInited] = useState(false);
  const tip = useRef<TipApi | null>(null);
  const tourKey = tour?.join(",");
  const { nodes, edges, boxes } = useMemo(
    () => build(d, filters, selected, tourKey ? tourKey.split(",") : undefined, lane === "all"), [d, filters, selected, tourKey, lane]);
  // Camera from our own layout boxes (no dependence on DOM measurement): a selected step is centred in the
  // part of the canvas the detail panel (side panel, or bottom sheet on narrow screens) leaves visible.
  useEffect(() => {
    if (!inited) return;
    const union = (ids: string[]) => {
      const bs = ids.map((i) => boxes[i]).filter(Boolean);
      const x = Math.min(...bs.map((b) => b.x)), y = Math.min(...bs.map((b) => b.y));
      return { x, y, width: Math.max(...bs.map((b) => b.x + b.width)) - x, height: Math.max(...bs.map((b) => b.y + b.height)) - y };
    };
    // Fit a box below the toolbar (fitBounds only takes symmetric padding).
    const fit = (b: Box, duration: number) => {
      const el = document.querySelector(".mapwrap");
      const W = el?.clientWidth ?? window.innerWidth, H = el?.clientHeight ?? window.innerHeight - 56;
      const zoom = Math.max(0.06, Math.min(1.2, (W - 2 * FIT_X) / b.width, (H - FIT_TOP - FIT_BOTTOM) / b.height));
      rf.setViewport({
        x: (W - b.width * zoom) / 2 - b.x * zoom,
        y: FIT_TOP + (H - FIT_TOP - FIT_BOTTOM - b.height * zoom) / 2 - b.y * zoom, zoom,
      }, { duration });
    };
    const t = setTimeout(() => {
      const narrow = isNarrow();
      if (selected && boxes[selected]) {
        const b = boxes[selected];
        const cx = b.x + b.width / 2, cy = b.y + b.height / 2;
        if (narrow) {
          // Sheet covers the lower ~58%; the tour caption (if any) covers the top. Aim for the gap.
          const H = window.innerHeight - 56, zoom = 0.62;
          const target = tourKey ? 0.3 : 0.21;
          rf.setCenter(cx, cy + ((0.5 - target) * H) / zoom, { zoom, duration: 500 });
        } else {
          const zoom = 0.95;
          const shift = Math.min(PANEL_W, window.innerWidth * 0.6) / 2 / zoom;
          rf.setCenter(cx + (d.dir === "rtl" ? -shift : shift), cy + (tourKey ? 70 / zoom : 0), { zoom, duration: 500 });
        }
      } else if (lane === "all") {
        const u = union(Object.keys(boxes).filter((k) => k.startsWith("lane:")));
        fit({ ...u, x: u.x - GUTTER, width: u.width + 2 * GUTTER }, 500);
      } else if (lane && boxes[`lane:${lane}`]) fit(boxes[`lane:${lane}`], 600);
      else fit(union([`lane:${d.lanes[0].id}`, `lane:${d.lanes[1].id}`]), 300);
    }, 20);
    return () => clearTimeout(t);
    // boxes only change with language/filters; camera should not jump when filters change
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [inited, selected, lane, d.lang]);

  const onEnter: NodeMouseHandler = useCallback((e, n) => {
    if (n.type !== "step") return;
    const el = (e.target as Element).closest(".react-flow__node");
    if (el) tip.current?.show(n.id, el);
  }, []);
  const onLeave = useCallback(() => tip.current?.hide(), []);
  const onClick: NodeMouseHandler = useCallback((_, n) => { tip.current?.hide(); if (n.type === "step") onOpen(n.id); }, [onOpen]);

  return (
    <>
      <ReactFlow
        nodes={nodes} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes} colorMode={theme}
        onNodeClick={onClick} onNodeMouseEnter={onEnter} onNodeMouseLeave={onLeave} onMoveStart={onLeave}
        onInit={() => setInited(true)} nodesConnectable={false} edgesFocusable={false} elementsSelectable={false}
        minZoom={0.06} maxZoom={2} proOptions={{ hideAttribution: true }}
      >
        <Background gap={24} size={1.2} />
        <Controls showInteractive={false} position={d.dir === "rtl" ? "bottom-right" : "bottom-left"} />
        <MiniMap pannable zoomable position={d.dir === "rtl" ? "bottom-left" : "bottom-right"} maskColor="rgba(120,140,170,.18)"
          nodeColor={(n) => (n.type === "lane" ? "transparent" : (n.data as StepData).hex)}
          nodeStrokeColor={(n) => (n.type === "lane" ? (n.data as LaneData).hex : "transparent")} nodeStrokeWidth={8} />
      </ReactFlow>
      <NodeTip d={d} apiRef={tip} />
    </>
  );
}

interface Props {
  d: Data; filters: MapFilters; selected?: string; lane?: string; theme: "dark" | "light";
  onOpen: (id: string) => void;
  /** Step ids of an active guided tour: they stay bright, everything else fades. */
  tour?: string[];
}

export default function MapView(p: Props) {
  return <ReactFlowProvider><Canvas {...p} /></ReactFlowProvider>;
}
