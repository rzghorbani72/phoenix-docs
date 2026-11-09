import { describe, expect, it } from "vitest";
import { INSTANCES, byId, pipelineOf, stageDetail } from "../../lib/instances";
import { stepGraph } from "./stepGraph";

const all = INSTANCES.instances;
const graph = (id: string, stage: string) => {
  const inst = byId(id)!;
  const detail = pipelineOf(inst).map((p) => stageDetail(inst, p)).find((d) => d.stage.id === stage)!;
  return stepGraph(inst, detail);
};
const nodes = (id: string, stage: string) => graph(id, stage).flatMap((l) => l.nodes);
const values = (id: string, stage: string) => nodes(id, stage).map((n) => n.value);

describe("stepGraph", () => {
  it.each(all.map((i) => [i.id, i] as const))("shows every part of %s exactly once", (_, inst) => {
    const shown = pipelineOf(inst).flatMap((p) =>
      stepGraph(inst, stageDetail(inst, p)).flatMap((l) => l.nodes.flatMap((n) => (n.part ? [n.part.name] : []))));
    expect(shown.sort()).toEqual(inst.components.map((c) => c.name).sort());
  });

  it.each(all.map((i) => [i.id, i] as const))("draws no empty layer or nameless node for %s", (_, inst) => {
    for (const p of pipelineOf(inst))
      for (const layer of stepGraph(inst, stageDetail(inst, p))) {
        expect(layer.nodes.length).toBeGreaterThan(0);
        for (const n of layer.nodes) expect(n.title.fa && n.title.en, n.id).toBeTruthy();
      }
  });

  it("uses each instance's own values, not one shared example", () => {
    expect(values("chatbot-ex", "kb")).toContain("chatbot-ex-aiva-contexts");
    expect(values("chatbot-ex", "call").join()).toContain("soniox");
    expect(values("chatbot-mobinnet-iva", "call")).toContain("mobinnet_prod_vad");
    expect(values("chatbot-mobinnet-iva", "analytics")).toContain("coa_mobinnet");
  });

  it("tells apart parts of the same kind", () => {
    const titles = nodes("mci-agentic", "analytics").filter((n) => n.part?.family === "grogu").map((n) => n.title.en);
    expect(titles.length).toBeGreaterThan(1);
    expect(new Set(titles).size).toBe(titles.length);
  });

  it("does not draw an empty voice flow for an instance with no voice", () => {
    expect(nodes("raya-beta", "call").every((n) => n.kind === "actor")).toBe(true);
  });
});
