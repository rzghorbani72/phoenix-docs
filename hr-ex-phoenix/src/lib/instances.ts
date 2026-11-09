import raw from "../data/instances.json";
import type { ConfigGroup, Instance, InstanceComponent, InstancesData, SurfaceKind } from "./instanceTypes";

export const INSTANCES = raw as unknown as InstancesData;

const VOICE_DIFF_BRAIN_KEYS = ["AGENT_LLM_MODEL", "AGENT_ENABLED_TOOLS", "VOICE_BRIDGE_ENABLED"];

/** Replicas null is a chart default or a cron job and an autoscaled 0 is normal, so neither is off. */
/** Stopped on purpose: no replicas, or a job whose schedule never fires. A missing count is not stopped. */
export const isStopped = (c: InstanceComponent): boolean => !!c.neverRuns || (c.replicas === 0 && !c.autoscaled);
const isOn = (c: InstanceComponent) => !isStopped(c);

export interface CampaignStatus {
  /** CAMPAIGN_END_AT as written in ops. */
  end: string;
  ended: boolean;
  /** Whole days between the end and the ops snapshot; negative while the campaign is still open. */
  daysSinceEnd: number;
  /** Parts that can still run. After the end, these are the ones to look at. */
  remaining: InstanceComponent[];
  /** Parts that are off, or whose schedule never fires. */
  stopped: InstanceComponent[];
}

const DAY_MS = 86_400_000;

/**
 * Which parts of a campaign are still going and which have ended. Compared with the date of the
 * ops snapshot, not today, so the answer is the one the snapshot supports.
 */
export function campaignStatus(inst: Instance): CampaignStatus | undefined {
  const end = inst.config.campaign.CAMPAIGN_END_AT;
  if (end === undefined || Number.isNaN(Date.parse(end))) return undefined;
  const parts = inst.components;
  const daysSinceEnd = Math.floor((Date.parse(INSTANCES.source.date) - Date.parse(end)) / DAY_MS);
  return {
    end,
    ended: Date.parse(end) < Date.parse(INSTANCES.source.date),
    daysSinceEnd,
    remaining: parts.filter((c) => !isStopped(c)),
    stopped: parts.filter(isStopped),
  };
}

export const byId = (id: string): Instance | undefined => INSTANCES.instances.find((i) => i.id === id);

/** Data settings of this instance that hold the same value in another instance; `with` lists their ids. */
export function sharedData(inst: Instance, all: Instance[]): { key: string; value: string; with: string[] }[] {
  return Object.entries(inst.config.data).flatMap(([key, value]) => {
    const others = all.filter((o) => o.id !== inst.id && o.config.data[key] === value).map((o) => o.id);
    return others.length ? [{ key, value, with: others }] : [];
  });
}

/** 1 and 1.0, or .4 and 0.4, are the same setting written differently. */
function comparable(value: string | undefined): string | undefined {
  if (value === undefined) return undefined;
  const text = value.trim();
  return /^[+-]?(\d+\.?\d*|\.\d+)$/.test(text) ? String(Number(text)) : text;
}

/** One row per setting, in the order first seen; `values` is keyed by instance id. */
export function voiceDiff(
  list: Instance[],
): { key: string; values: Record<string, string | undefined>; differs: boolean }[] {
  const voiceKeys = list.flatMap((i) => Object.keys(i.config.voice));
  const brainKeys = VOICE_DIFF_BRAIN_KEYS.filter((k) => list.some((i) => i.config.brain[k] !== undefined));
  return [...new Set([...voiceKeys, ...brainKeys])].map((key) => {
    const values: Record<string, string | undefined> = {};
    for (const i of list) values[i.id] = i.config.voice[key] ?? i.config.brain[key];
    return { key, values, differs: new Set(Object.values(values).map(comparable)).size > 1 };
  });
}

export type PipelineStageId = "call" | "brain" | "kb" | "analytics" | "ops";
export interface PipelineStage {
  id: PipelineStageId;
  /** "off" is deployed but switched off; "none" means this instance does not have the stage. */
  state: "on" | "off" | "none";
  /** The main image of the stage. */
  family?: string;
  version?: string;
}

export const STAGE_IDS: PipelineStageId[] = ["call", "brain", "kb", "analytics", "ops"];

/** Every role belongs to exactly one stage, so no component is left out of the diagram. */
const STAGE_ROLES: Record<PipelineStageId, InstanceComponent["role"][]> = {
  call: ["voice", "media"],
  brain: ["brain"],
  kb: ["knowledge"],
  analytics: ["analytics"],
  ops: ["gateway", "cache", "auth", "ui", "other"],
};

const partsOf = (inst: Instance, id: PipelineStageId) =>
  inst.components
    .filter((c) => STAGE_ROLES[id].includes(c.role))
    .sort((a, b) => STAGE_ROLES[id].indexOf(a.role) - STAGE_ROLES[id].indexOf(b.role));

/**
 * Which stages of the pipeline map this instance actually runs. The stage ids are the map's lane
 * ids, so each one can link to #/map/lane/<id>.
 */
export function pipelineOf(inst: Instance): PipelineStage[] {
  return STAGE_IDS.map((id): PipelineStage => {
    const parts = partsOf(inst, id);
    const metered = id === "ops" && inst.components.some((c) => c.metrics && isOn(c));
    if (!parts.length) return { id, state: metered ? "on" : "none" };
    const main = parts.find(isOn) ?? parts[0];
    const chosen = id === "brain" && inst.brain ? inst.brain : main;
    const state = metered || parts.some(isOn) ? "on" : "off";
    return id === "ops" ? { id, state } : { id, state, family: chosen.family, version: chosen.version };
  });
}

export const hasSurface = (inst: Instance, kind: SurfaceKind): boolean => inst.surfaces.some((x) => x.kind === kind);

/** The instance that actually runs a step: this one, or the project whose panel analyses its calls. */
export function stageOwner(inst: Instance, id: PipelineStageId): Instance {
  if (id !== "analytics" || partsOf(inst, id).length) return inst;
  const panel = inst.links.find((l) => l.kind === "panel");
  return (panel && byId(panel.id)) || inst;
}

/** The whole pipeline as this instance lives it, with each step read from whoever runs it. */
export function connectedPipeline(inst: Instance): { stage: PipelineStage; owner: Instance }[] {
  return STAGE_IDS.map((id) => {
    const owner = stageOwner(inst, id);
    return { owner, stage: pipelineOf(owner).find((p) => p.id === id)! };
  });
}

const SETTING_STAGE: Record<string, PipelineStageId> = {
  CONTEXTS_COLLECTION_NAME: "kb", GUARDRAIL_COLLECTION_NAME: "kb", INSTRUCTIONS_COLLECTION_NAME: "kb",
  IVA_CONTEXTS_COLLECTION_NAME: "kb", CONTEXTS_FILTER_LLM_ENABLED: "kb",
  AGENT_APM_TRANSACTION_SAMPLE_RATE: "ops", PHOENIX_PROJECT_NAME: "ops",
};
const GROUP_STAGE: Record<ConfigGroup, PipelineStageId> = { voice: "call", brain: "brain", data: "analytics", campaign: "analytics" };

export interface StageDetail {
  stage: PipelineStage;
  components: InstanceComponent[];
  settings: { key: string; value: string }[];
  /** Parts switched on. */
  on: number;
  /** Sum of the replicas stated in ops. Chart defaults and autoscaled parts have no number. */
  replicas: number;
}

export const isStage = (id: string): id is PipelineStageId => (STAGE_IDS as string[]).includes(id);

export interface InstanceLane {
  /** The instance that runs this lane: this one, or the one whose panel serves it. */
  owner: Instance;
  /** Read from ops. Lanes with no deployed parts of their own, such as memory, have none. */
  detail?: StageDetail;
  /** Code inside the aiva brain, not something ops deploys on its own. */
  builtIn: boolean;
  used: boolean;
}

/** What one lane of the pipeline map means for an instance. */
export function instanceLane(inst: Instance, lane: string): InstanceLane {
  if (isStage(lane)) {
    const { owner, stage } = connectedPipeline(inst).find((x) => x.stage.id === lane)!;
    const detail = stageDetail(owner, stage);
    return { owner, detail, builtIn: false, used: stage.state !== "none" };
  }
  const builtIn = (inst.brain?.family ?? "").startsWith("aiva");
  return { owner: inst, builtIn, used: builtIn };
}

/** Everything the diagram and the side panel show for one stage. */
export function stageDetail(inst: Instance, stage: PipelineStage): StageDetail {
  const components = partsOf(inst, stage.id);
  const settings = (Object.keys(GROUP_STAGE) as ConfigGroup[]).flatMap((group) =>
    Object.entries(inst.config[group])
      .filter(([key]) => (SETTING_STAGE[key] ?? GROUP_STAGE[group]) === stage.id)
      .map(([key, value]) => ({ key, value })),
  );
  return {
    stage,
    components,
    settings,
    on: components.filter(isOn).length,
    replicas: components.reduce((n, c) => n + (isOn(c) && !c.autoscaled ? c.replicas ?? 0 : 0), 0),
  };
}

export interface PeerComparison {
  /** Other instances that have this setting. */
  total: number;
  /** How many of them use the same value. */
  same: number;
  /** The most common value among them, and how many use it. */
  common: string;
  commonCount: number;
}

/** How one setting compares with the other instances. Undefined when too few have it to say anything. */
export function comparePeers(inst: Instance, key: string, value: string, all: Instance[]): PeerComparison | undefined {
  const others = all.flatMap((o) => {
    if (o.id === inst.id) return [];
    const found = (Object.keys(o.config) as ConfigGroup[]).map((g) => o.config[g][key]).find((v) => v !== undefined);
    return found === undefined ? [] : [found];
  });
  if (others.length < 2) return undefined;
  const counts = new Map<string, { raw: string; n: number }>();
  for (const v of others) {
    const k = comparable(v)!;
    counts.set(k, { raw: counts.get(k)?.raw ?? v, n: (counts.get(k)?.n ?? 0) + 1 });
  }
  const top = [...counts.values()].sort((a, b) => b.n - a.n)[0];
  return { total: others.length, same: counts.get(comparable(value)!)?.n ?? 0, common: top.raw, commonCount: top.n };
}
