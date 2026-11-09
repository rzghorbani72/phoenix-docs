/** Shape of src/data/instances.json, written by content/export_json.py from the ops snapshot. */

export type InstanceCategory = "panel" | "phone" | "chat" | "campaign" | "tools" | "unclassified";
export type InstanceState = "running" | "partial" | "off";
export type ComponentRole =
  | "voice" | "brain" | "knowledge" | "analytics" | "media" | "auth" | "gateway" | "cache" | "ui" | "other";
export type Localized = { en: string; fa: string };

export interface InstanceComponent {
  name: string;
  /** Image name, without the registry. */
  family: string;
  role: ComponentRole;
  /** A release tag such as v0.36.0, or an 8-character commit. */
  version: string;
  /** null means the chart default or a cron job, not zero. */
  replicas: number | null;
  autoscaled: boolean;
  /** A Prometheus ServiceMonitor is enabled. */
  metrics: boolean;
  /** Cron expression of a scheduled job. */
  schedule?: string;
  /** The schedule names only dates that do not exist, such as 31 February, so the job never starts. */
  neverRuns?: boolean;
  /** The Helm release that deploys this part. */
  release: string;
  /** The side of the project it serves; base parts such as auth serve them all. */
  surface: SurfaceKind | "base";
}

export type SurfaceKind = "panel" | "phone" | "chatbot";

/** One side of a project, built from the parts ops deploys for it. */
export interface Surface {
  kind: SurfaceKind;
  state: InstanceState;
  parts: string[];
  releases: string[];
  /** What an admin panel serves, read from its gateway routes. */
  apps?: string[];
}

export type ConfigGroup = "voice" | "brain" | "data" | "campaign";

export interface Instance {
  id: string;
  /** The main Helm release. */
  release: string;
  /** Every Helm release of this project. */
  releases: string[];
  category: InstanceCategory;
  name: Localized;
  about: Localized;
  /** The name is a reading of the config, not confirmed by the owner. */
  confirm: boolean;
  state: InstanceState;
  components: InstanceComponent[];
  /** Gateway releases that belong to this instance. */
  companions: string[];
  /** Allowlisted env settings by group; an absent key means not set in ops. */
  config: Record<ConfigGroup, Record<string, string>>;
  /** Shared releases this instance calls. */
  deps: string[];
  brain: { family: string; version: string; component: string } | null;
  /** Cut out of a release that also holds another instance. */
  slice: boolean;
  surfaces: Surface[];
  links: InstanceLink[];
}

/** A panel that reads a phone line deployed as another project. */
export interface InstanceLink {
  id: string;
  kind: "phone" | "panel";
}

export interface SharedItem {
  id: string;
  usedBy: string[];
  state: InstanceState;
}

export interface SharedGroup {
  group: string;
  name: Localized;
  items: SharedItem[];
}

export interface InstancesData {
  source: { repo: string; branch: string; commit: string; date: string; releases: number };
  instances: Instance[];
  shared: SharedGroup[];
}
