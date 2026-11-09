import { memo, useMemo } from "react";
import {
  Background, Controls, Handle, MarkerType, Position, ReactFlow, ReactFlowProvider,
  type Edge, type Node, type NodeProps,
} from "@xyflow/react";
import type { Data, Lane, Status } from "../../lib/types";
import type { Instance } from "../../lib/instanceTypes";
import { instanceLane, isStage } from "../../lib/instances";
import { T as instanceStrings } from "../../views/instances/i18n";
import { stepLook, stepWordText } from "../../views/instances/model";
import { plain } from "../../lib/md";
import { CROSS, LANE_COLOR, STATUSES } from "./shared";
import { T } from "./i18n";
import { useNarrow } from "./useNarrow";
import "./map.css";

const CW = 330, CH = 214, GX = 210, GY = 140;
/** Grid slot per lane (LTR column, row); mirrored for RTL. The framework sits under the KB/brain it powers. */
const SLOT: Record<string, [number, number]> = {
  call: [0, 0], brain: [1, 0], kb: [2, 0], ops: [3, 0], analytics: [0, 1], memory: [1, 1], framework: [2, 1],
};
const COLS = 4;

type Side = "l" | "r" | "t" | "b";
/** Handle spec "side:percent" for each hand-off, written for LTR. */
const ROUTE: Record<string, [string, string]> = {
  "call>brain": ["r:35", "l:35"], "brain>call": ["l:65", "r:65"],
  "brain>kb": ["r:35", "l:35"], "kb>brain": ["l:65", "r:65"],
  "kb>ops": ["r:50", "l:50"], "call>analytics": ["b:50", "t:50"], "brain>memory": ["b:50", "t:50"],
  "framework>brain": ["t:20", "b:80"],
};
const HANDLES: [Side, number][] = [
  ["l", 35], ["l", 50], ["l", 65], ["r", 35], ["r", 50], ["r", 65],
  ["t", 20], ["t", 50], ["t", 80], ["b", 20], ["b", 50], ["b", 80],
];
const POS: Record<Side, Position> = { l: Position.Left, r: Position.Right, t: Position.Top, b: Position.Bottom };
const mirror = (spec: string, rtl: boolean) => {
  if (!rtl) return spec;
  const [s, p] = spec.split(":");
  if (s === "l") return `r:${p}`;
  if (s === "r") return `l:${p}`;
  return `${s}:${100 - Number(p)}`;
};

type LaneStats = {
  lane: Lane; steps: number; models: number; risks: number; high: number; status: Record<Status, number>;
  out: { to: Lane; label: string }[];
};

function laneStats(d: Data): LaneStats[] {
  const flows = handoffs(d);
  return d.lanes.map((lane) => {
    const ids = new Set(lane.steps);
    const status = Object.fromEntries(STATUSES.map((s) => [s, 0])) as Record<Status, number>;
    lane.steps.forEach((id) => { const s = d.steps[id]; if (s) status[s.status]++; });
    const risks = d.risks.items.filter((r) => r.steps?.some((s) => ids.has(s)));
    return {
      lane, steps: lane.steps.length, status,
      models: d.models.cards.filter((c) => c.steps?.some((s) => ids.has(s))).length,
      risks: risks.length, high: risks.filter((r) => r.sev === "high").length,
      out: flows.filter((f) => f.from === lane.id).map((f) => ({ to: d.lanes.find((l) => l.id === f.to)!, label: f.label })).filter((o) => o.to),
    };
  });
}

/** Lane-level hand-offs: the content's system edges plus step-level hand-offs they do not cover. */
function handoffs(d: Data) {
  const laneOfStep = (id: string) => d.lanes.find((l) => l.steps.includes(id))?.id;
  const list = d.system_edges.map((e) => ({ from: e.from, to: e.to, label: e.label }));
  for (const c of CROSS) {
    const from = laneOfStep(c.from), to = laneOfStep(c.to);
    if (from && to && !list.some((e) => e.from === from && e.to === to)) list.push({ from, to, label: d.lang === "fa" ? c.fa : c.en });
  }
  return list;
}

type CardData = LaneStats & { color: string; lang: "en" | "fa"; statusLabel: Record<string, string>; instance?: Instance };

/** The same lane as this instance runs it: read from ops, and only what ops really shows. */
function InstanceCard({ st, inst, lang }: { st: LaneStats; inst: Instance; lang: "en" | "fa" }) {
  const t = T(lang);
  const s = instanceStrings(lang);
  const { owner, detail, builtIn } = instanceLane(inst, st.lane.id);
  const look = detail && stepLook(detail);
  return (
    <>
      <div className="ov-head">
        <span className="ov-prefix">{st.lane.prefix}</span>
        <div className="ov-names">
          <div className="ov-short">{isStage(st.lane.id) ? s.stages[st.lane.id] : plain(st.lane.short)}</div>
          <div className="ov-tag"><bdi>{detail?.stage.family ?? ""}</bdi>{detail?.stage.version ? <> · <bdi>{detail.stage.version}</bdi></> : null}</div>
          {owner.id !== inst.id && <div className="ov-tag ins-from"><bdi>{owner.name[lang]}</bdi></div>}
        </div>
      </div>
      {detail && detail.components.length > 0 && (
        <div className="ov-stats">
          <div><b>{detail.on}/{detail.components.length}</b><span>{s.statParts}</span></div>
          <div><b>{detail.replicas}</b><span>{s.statReplicas}</span></div>
          <div><b>{detail.settings.length}</b><span>{s.settings}</span></div>
        </div>
      )}
      <div className="ov-foot">
        <div className={`ins-step-status ${look?.tone ?? "off"}`}>
          <strong>{look ? stepWordText(look.word, lang) : builtIn ? s.laneBuiltIn : s.laneNotInOps}</strong>
        </div>
        <div className="ov-cta">{detail ? s.openStep : t.openLane} {lang === "fa" ? "←" : "→"}</div>
      </div>
    </>
  );
}

function Card({ st, lang, statusLabel }: { st: LaneStats; lang: "en" | "fa"; statusLabel: Record<string, string> }) {
  const t = T(lang);
  return (
    <>
      <div className="ov-head">
        <span className="ov-prefix">{st.lane.prefix}</span>
        <div className="ov-names"><div className="ov-short">{plain(st.lane.short)}</div><div className="ov-tag">{plain(st.lane.tagline)}</div></div>
      </div>
      <div className="ov-stats">
        <div><b>{st.steps}</b><span>{t.steps}</span></div>
        <div><b>{st.models}</b><span>{t.models}</span></div>
        <div className={st.high ? "risky" : ""}><b>{st.risks}</b><span>{t.risks}{st.high ? ` · ${st.high} ${t.high}` : ""}</span></div>
      </div>
      <div className="ov-bar" aria-label={t.status}>
        {STATUSES.filter((s) => st.status[s]).map((s) => (
          <span key={s} className={`s-${s}`} style={{ flexGrow: st.status[s] }} title={`${statusLabel[s]}: ${st.status[s]}`} />
        ))}
      </div>
      <div className="ov-cta">{t.openLane} {lang === "fa" ? "←" : "→"}</div>
    </>
  );
}

const cardClass = (lane: string, inst?: Instance) => `ovcard${inst && !instanceLane(inst, lane).used ? " ov-unused" : ""}`;

const LaneCard = memo(function LaneCard({ data }: NodeProps<Node<CardData>>) {
  return (
    <div className={cardClass(data.lane.id, data.instance)} style={{ ["--lc" as string]: data.color }}>
      {HANDLES.map(([s, p]) => {
        const style = s === "l" || s === "r" ? { top: `${p}%` } : { left: `${p}%` };
        return [
          <Handle key={`s${s}${p}`} type="source" id={`s-${s}:${p}`} position={POS[s]} style={style} />,
          <Handle key={`t${s}${p}`} type="target" id={`t-${s}:${p}`} position={POS[s]} style={style} />,
        ];
      })}
      {data.instance ? <InstanceCard st={data} inst={data.instance} lang={data.lang} /> : <Card st={data} lang={data.lang} statusLabel={data.statusLabel} />}
    </div>
  );
});

const nodeTypes = { lanecard: LaneCard };

function build(d: Data, instance?: Instance) {
  const rtl = d.dir === "rtl";
  const stats = laneStats(d);
  const nodes: Node[] = stats.map((st, i) => {
    const [c, r] = SLOT[st.lane.id] ?? [i % COLS, 2];
    const col = rtl ? COLS - 1 - c : c;
    return {
      id: st.lane.id, type: "lanecard", position: { x: col * (CW + GX), y: r * (CH + GY) }, draggable: false,
      width: CW, height: CH, style: { width: CW, height: CH },
      data: { ...st, color: LANE_COLOR[st.lane.color] ?? "var(--accent)", lang: d.lang, statusLabel: d.ui.status, instance } satisfies CardData,
    };
  });
  const runs = (lane: string) => !instance || instanceLane(instance, lane).used;
  const edges: Edge[] = handoffs(d).filter((h) => runs(h.from) && runs(h.to)).map((h) => {
    const color = LANE_COLOR[d.lanes.find((l) => l.id === h.from)?.color ?? ""] ?? "var(--accent)";
    const spec = ROUTE[`${h.from}>${h.to}`];
    return {
      id: `o:${h.from}>${h.to}`, source: h.from, target: h.to, label: h.label, animated: true,
      type: spec && spec[0][0] !== spec[1][0] && !(spec[0][0] === "t" || spec[0][0] === "b") ? "straight" : "default",
      sourceHandle: `s-${mirror(spec?.[0] ?? "b:50", rtl)}`, targetHandle: `t-${mirror(spec?.[1] ?? "t:50", rtl)}`,
      className: "ovedge", style: { stroke: color, strokeWidth: 2.5 },
      labelBgPadding: [8, 4] as [number, number], labelBgBorderRadius: 6,
      markerEnd: { type: MarkerType.ArrowClosed, color, width: 18, height: 18 },
    };
  });
  return { nodes, edges, stats };
}

interface Props { d: Data; theme: "dark" | "light"; onLane: (id: string) => void; instance?: Instance }

/** One card per lane with its counts and the hand-offs between lanes; click a card to zoom into it. */
export default function OverviewMap({ d, theme, onLane, instance }: Props) {
  const narrow = useNarrow();
  const { nodes, edges, stats } = useMemo(() => build(d, instance), [d, instance]);
  if (narrow) return <OverviewList d={d} stats={stats} onLane={onLane} instance={instance} />;
  return (
    <ReactFlowProvider>
      <ReactFlow
        className="overview" nodes={nodes} edges={edges} nodeTypes={nodeTypes} colorMode={theme}
        onNodeClick={(_, n) => onLane(n.id)} fitView fitViewOptions={{ padding: { top: "84px", bottom: "36px", x: "48px" } }}
        nodesConnectable={false} elementsSelectable={false} edgesFocusable={false} minZoom={0.2} maxZoom={1.6}
        proOptions={{ hideAttribution: true }}
      >
        <Background gap={24} size={1.2} />
        <Controls showInteractive={false} position={d.dir === "rtl" ? "bottom-right" : "bottom-left"} />
      </ReactFlow>
    </ReactFlowProvider>
  );
}

/** Phone layout: the same cards as a scrolling list, hand-offs written out under each card. */
function OverviewList({ d, stats, onLane, instance }: { d: Data; stats: LaneStats[]; onLane: (id: string) => void; instance?: Instance }) {
  const t = T(d.lang);
  return (
    <div className="ovlist">
      {stats.map((st) => (
        <button key={st.lane.id} className={cardClass(st.lane.id, instance)} style={{ ["--lc" as string]: LANE_COLOR[st.lane.color] }} onClick={() => onLane(st.lane.id)}>
          {instance ? <InstanceCard st={st} inst={instance} lang={d.lang} /> : <Card st={st} lang={d.lang} statusLabel={d.ui.status} />}
          {!instance && st.out.length > 0 && (
            <div className="ov-out">
              {st.out.map((o) => (
                <span key={o.to.id} style={{ ["--tc" as string]: LANE_COLOR[o.to.color] }} title={t.handoffsOut}>
                  {d.lang === "fa" ? "←" : "→"} <b>{o.to.prefix}</b> {o.label}
                </span>
              ))}
            </div>
          )}
        </button>
      ))}
    </div>
  );
}
