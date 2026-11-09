/** Interactive runtime diagrams, copied from the Phoenix repo into public/diagrams by the daily sync. */
export type RuntimeDiagramId = "aiva" | "aiva-poll";

export const DIAGRAM_FILES: Record<RuntimeDiagramId, string> = {
  aiva: "diagrams/aiva-runtime.html",
  "aiva-poll": "diagrams/aiva-poll-runtime.html",
};

/** Map step -> the node of the AIVA diagram showing it. Steps not listed here have no node there. */
export const STEP_NODE: Record<string, string> = {
  "v-aiva": "endpoint",
  "b-setup": "pipeline",
  "b-signal": "endpoint",
  "b-intent": "intent",
  "b-clarify": "classification",
  "b-retrieve": "retrieval",
  "b-guardrail": "guardrail-agent",
  "b-classify": "classification",
  "b-branch": "gate",
  "b-react": "react-agent",
  "b-tools": "react-agent",
  "b-guard-reply": "response",
  "b-voicebridge": "voice",
};

/** Which diagram describes this brain. Other brains have none. */
export const diagramForBrain = (family: string | undefined): RuntimeDiagramId | undefined =>
  family === "aiva" || family === "aiva-poll" ? family : undefined;

/** Theme and focus are read by the page itself, so changing them only changes this URL. */
export function diagramUrl(id: RuntimeDiagramId, opts: { embed: boolean; theme: "dark" | "light"; node?: string }): string {
  const query = `?${opts.embed ? "embed=1&" : ""}theme=${opts.theme}`;
  return `${DIAGRAM_FILES[id]}${query}${opts.node ? `#focus=${encodeURIComponent(opts.node)}` : ""}`;
}
