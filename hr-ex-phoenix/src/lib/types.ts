export type Status = "live" | "off" | "notdeployed" | "external" | "unknown";

/** A section body as exported by export_json.py: paragraphs, bullets, table, ordered list, note, code, or several of them. */
export type Body =
  | string
  | string[]
  | { table: string[][] }
  | { ol: string[] }
  | { note: string; kind?: string }
  | { code: string }
  | { multi: Body[] };

export interface Page {
  title: string;
  title_plain?: string;
  status: Status;
  chip?: string;
  chip_plain?: string;
  summary: string;
  facts: [string, string][];
  sections: [string, Body][];
  fallback?: boolean; // shown in English because the translation is missing
}

export interface Lane {
  id: string;
  prefix: string;
  color: string;
  short: string;
  tagline: string;
  title: string;
  title_plain: string;
  desc: string;
  handoff?: string;
  steps: string[];
  band?: boolean;
}

export interface ModelCard {
  id?: string;
  name: string;
  size: string;
  status: Status;
  facts: Body;
  steps?: string[];
}

export interface Risk {
  sev: "high" | "med" | "low";
  title: string;
  why: string;
  steps?: string[];
}

export interface Data {
  lang: "en" | "fa";
  dir: "ltr" | "rtl";
  // UI strings are a loose JSON bag (nested maps such as `status` and `sev`); typed per use site.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  ui: Record<string, any>;
  meta: { title: string; title_plain: string; lede: string; source: string; footer: string };
  lanes: Lane[];
  system_edges: { from: string; to: string; label: string }[];
  key_points: Body[];
  steps: Record<string, Page>;
  models: {
    title: string;
    lede: string;
    cards: ModelCard[];
    sections: [string, Body][];
    pages: Record<string, Page>;
    fallback?: boolean;
  };
  risks: { title: string; lede: string; items: Risk[] };
  guide?: { title: string; lede: string; sections: [string, Body][]; fallback?: boolean };
}
