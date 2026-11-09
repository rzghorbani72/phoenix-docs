import { describe, expect, it } from "vitest";
import type { InstanceComponent } from "../../lib/instanceTypes";
import type { StageDetail } from "../../lib/instances";
import { stepLook } from "./model";

const part = (over: Partial<InstanceComponent> = {}): InstanceComponent => ({
  name: "x", family: "f", role: "other", version: "v1", replicas: 1, autoscaled: false, metrics: false, release: "r", surface: "base", ...over,
});
const detail = (state: "on" | "off" | "none", components: InstanceComponent[]): StageDetail =>
  ({ stage: { id: "call", state }, components, settings: [], on: 0, replicas: 0 });

describe("stepLook", () => {
  it("is on, partly on or off by how many parts are stopped", () => {
    expect(stepLook(detail("on", [part(), part()])).word).toBe("on");
    expect(stepLook(detail("on", [part(), part({ replicas: 0 })])).word).toBe("partly");
    expect(stepLook(detail("off", [part({ replicas: 0 })])).word).toBe("off");
  });
  it("calls a step with no parts none, and one with metrics only on", () => {
    expect(stepLook(detail("none", [])).word).toBe("none");
    expect(stepLook(detail("on", [])).word).toBe("on");
  });
  it("turns amber only when something in the step is stopped", () => {
    expect(stepLook(detail("on", [part()])).tone).toBe("ok");
    expect(stepLook(detail("on", [part(), part({ replicas: 0 })])).tone).toBe("warn");
    expect(stepLook(detail("off", [part({ replicas: 0 })])).tone).toBe("off");
  });
});
