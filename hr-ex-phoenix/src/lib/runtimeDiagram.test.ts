// @ts-expect-error Node types are not installed; this test only reads a file.
import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { DIAGRAM_FILES, STEP_NODE, diagramForBrain, diagramUrl } from "./runtimeDiagram";
import { DATA } from "./data";

const html = (id: keyof typeof DIAGRAM_FILES): string => readFileSync(`public/${DIAGRAM_FILES[id]}`, "utf8");

describe("runtime diagrams", () => {
  it("point at nodes that exist, so a new diagram cannot silently lose a highlight", () => {
    for (const [step, node] of Object.entries(STEP_NODE)) expect(html("aiva"), `${step} -> ${node}`).toContain(`data-node-id="${node}"`);
  });

  it("only name steps that exist on the map", () => {
    for (const step of Object.keys(STEP_NODE)) expect(DATA.en.steps[step], step).toBeTruthy();
  });

  it("carry no outside dependency or secret", () => {
    for (const id of ["aiva", "aiva-poll"] as const) expect(html(id)).not.toMatch(/(?:src|href)="https?:|password|api[_-]?key/i);
  });

  it("builds the preview and full links", () => {
    expect(diagramUrl("aiva", { embed: true, theme: "light", node: "gate" })).toBe("diagrams/aiva-runtime.html?embed=1&theme=light#focus=gate");
    expect(diagramUrl("aiva-poll", { embed: false, theme: "dark" })).toBe("diagrams/aiva-poll-runtime.html?theme=dark");
  });

  it("matches a diagram to its brain only", () => {
    expect(diagramForBrain("aiva")).toBe("aiva");
    expect(diagramForBrain("adcs-chatbot")).toBeUndefined();
  });
});
