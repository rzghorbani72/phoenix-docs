import { describe, expect, it } from "vitest";
import { byId, campaignStatus, comparePeers, connectedPipeline, hasSurface, INSTANCES, pipelineOf, sharedData, stageDetail, stageOwner, voiceDiff } from "./instances";
import type { Instance, InstanceComponent } from "./instanceTypes";

const comp = (over: Partial<InstanceComponent> = {}): InstanceComponent => ({
  name: "api",
  family: "x",
  role: "other",
  version: "v1.0.0",
  replicas: 2,
  autoscaled: false,
  metrics: true,
  release: "demo",
  surface: "chatbot",
  ...over,
});

type Over = Omit<Partial<Instance>, "config"> & { config?: Partial<Instance["config"]> };

const inst = ({ config, ...over }: Over = {}): Instance => ({
  id: "demo",
  release: "demo",
  releases: ["demo"],
  category: "chat",
  name: { en: "Demo", fa: "نمونه" },
  about: { en: "", fa: "" },
  confirm: false,
  state: "running",
  components: [comp()],
  companions: [],
  deps: [],
  brain: null,
  slice: false,
  surfaces: [],
  links: [],
  ...over,
  config: { voice: {}, brain: {}, data: {}, campaign: {}, ...config },
});

describe("byId", () => {
  it("finds an instance or returns undefined", () => {
    expect(byId("raya-beta")?.id).toBe("raya-beta");
    expect(byId("nope")).toBeUndefined();
  });
});

describe("sharedData", () => {
  it("lists settings with the same value elsewhere and who holds them", () => {
    const data = { KAFKA_TICKET_TOPIC: "t", POSTGRES_DATABASE: "own-a" };
    const a = inst({ id: "a", config: { data } });
    const b = inst({ id: "b", config: { data: { KAFKA_TICKET_TOPIC: "t", POSTGRES_DATABASE: "own-b" } } });
    expect(sharedData(a, [a, b])).toEqual([{ key: "KAFKA_TICKET_TOPIC", value: "t", with: ["b"] }]);
    expect(sharedData(a, [a])).toEqual([]);
  });
});

describe("voiceDiff", () => {
  const row = (list: Instance[], key: string) => voiceDiff(list).find((r) => r.key === key);
  const pair = (key: string, x: string, y: string) => [
    inst({ id: "a", config: { voice: { [key]: x } } }),
    inst({ id: "b", config: { voice: { [key]: y } } }),
  ];
  it("treats equal numbers as equal however they are written", () => {
    expect(row(pair("K", "1", "1.0"), "K")?.differs).toBe(false);
    expect(row(pair("K", ".4", "0.4"), "K")?.differs).toBe(false);
    expect(row(pair("K", "1.20", "1.2"), "K")?.differs).toBe(false);
    expect(row(pair("K", "1", "2"), "K")?.differs).toBe(true);
    expect(row(pair("K", "soniox", "local"), "K")?.differs).toBe(true);
  });
  it("keeps the values as written and counts a missing setting as different", () => {
    const list = [inst({ id: "a", config: { voice: { K: "1.0" } } }), inst({ id: "b" })];
    expect(row(list, "K")).toEqual({ key: "K", values: { a: "1.0", b: undefined }, differs: true });
  });
  it("adds the three brain settings and no others", () => {
    const list = [inst({ id: "a", config: { brain: { AGENT_LLM_MODEL: "m", PHOENIX_PROJECT_NAME: "p" } } })];
    expect(voiceDiff(list).map((r) => r.key)).toEqual(["AGENT_LLM_MODEL"]);
  });
});

describe("campaignStatus", () => {
  const status = (parts: InstanceComponent[], end = "2020-01-01T00:00:00+03:30") =>
    campaignStatus(inst({ config: { campaign: { CAMPAIGN_END_AT: end } }, components: parts }))!;
  const api = comp({ name: "api", replicas: 2 });
  const worker = comp({ name: "worker", replicas: 0 });
  const job = comp({ name: "job", replicas: null, schedule: "0 0 31 2 *", neverRuns: true });
  const cron = comp({ name: "cron", replicas: null, schedule: "*/5 * * * *", neverRuns: false });
  const auto = comp({ name: "auto", replicas: 0, autoscaled: true });
  const names = (parts: InstanceComponent[]) => parts.map((c) => c.name);

  it("splits parts into those that remain and those that ended", () => {
    const s = status([api, worker, job]);
    expect(names(s.remaining)).toEqual(["api"]);
    expect(names(s.stopped)).toEqual(["worker", "job"]);
    expect(s.ended).toBe(true);
  });
  it("keeps a real schedule, an autoscaled part and a missing count in what remains", () => {
    expect(names(status([cron, auto, comp({ name: "default", replicas: null })]).remaining)).toEqual(["cron", "auto", "default"]);
  });
  it("puts every part in exactly one group", () => {
    const parts = [api, worker, job, cron, auto];
    const s = status(parts);
    expect(names([...s.remaining, ...s.stopped]).sort()).toEqual(names(parts).sort());
  });
  it("is not ended before its end date and counts days after it", () => {
    expect(status([api], "2999-01-01").ended).toBe(false);
    expect(status([api], "2999-01-01").daysSinceEnd).toBeLessThan(0);
    expect(status([api]).daysSinceEnd).toBeGreaterThan(1000);
  });
  it("is undefined for an instance that is no campaign", () => {
    expect(campaignStatus(inst({}))).toBeUndefined();
  });
  it("on real data: only the Raya API remains, and the jobs that never fire count as ended", () => {
    const s = campaignStatus(byId("raya-beta")!)!;
    expect(names(s.remaining)).toEqual(["coa-scoring-api"]);
    expect(names(s.stopped).sort()).toEqual(["coa-scoring-campaign-events", "coa-scoring-maintenance", "coa-scoring-sms-worker", "coa-scoring-syncer"]);
  });
});

describe("pipelineOf", () => {
  it("tells a missing stage from one that is switched off", () => {
    const stages = pipelineOf(inst({ components: [comp({ role: "voice" }), comp({ role: "knowledge", replicas: 0 })] }));
    expect(Object.fromEntries(stages.map((s) => [s.id, s.state]))).toEqual({
      call: "on", brain: "none", kb: "off", analytics: "none", ops: "on",
    });
  });
});

describe("stageDetail", () => {
  it.each(INSTANCES.instances.map((i) => [i.id, i] as const))("places every part and setting of %s in one step", (_, i) => {
    const details = pipelineOf(i).map((p) => stageDetail(i, p));
    expect(details.flatMap((d) => d.components.map((c) => c.name)).sort()).toEqual(i.components.map((c) => c.name).sort());
    const keys = Object.values(i.config).flatMap((g) => Object.keys(g)).sort();
    expect(details.flatMap((d) => d.settings.map((x) => x.key)).sort()).toEqual(keys);
  });
});

describe("comparePeers", () => {
  const withSpeed = (id: string, v: string) => inst({ id, config: { voice: { AGENT_TTS_SPEED: v } } });
  const all = [withSpeed("a", "1.2"), withSpeed("b", "1.20"), withSpeed("c", "1.1"), withSpeed("d", "1.2")];

  it("counts equal numbers written differently as the same", () => {
    expect(comparePeers(all[0], "AGENT_TTS_SPEED", "1.2", all)).toMatchObject({ total: 3, same: 2, commonCount: 2 });
  });
  it("reports the common value for a different one", () => {
    expect(comparePeers(all[2], "AGENT_TTS_SPEED", "1.1", all)).toMatchObject({ same: 0, common: "1.2", commonCount: 3 });
  });
  it("says nothing with fewer than two others", () => {
    expect(comparePeers(all[0], "AGENT_TTS_SPEED", "1.2", all.slice(0, 2))).toBeUndefined();
  });
});

describe("project steps", () => {
  it("runs every step of a project with its own parts", () => {
    const ex = byId("chatbot-ex")!;
    for (const { owner } of connectedPipeline(ex)) expect(owner.id).toBe("chatbot-ex");
    expect(pipelineOf(ex).find((p) => p.id === "analytics")?.state).not.toBe("none");
  });

  it("reads analytics from the panel that serves a phone line with none of its own", () => {
    expect(stageOwner(byId("aiva-neda")!, "analytics").id).toBe("aiva");
    expect(stageOwner(byId("aiva-neda")!, "call").id).toBe("aiva-neda");
  });

  it("gives every instance all five steps, each from itself or a linked instance", () => {
    for (const inst of INSTANCES.instances) {
      const steps = connectedPipeline(inst);
      expect(steps.map((x) => x.stage.id)).toEqual(pipelineOf(inst).map((x) => x.id));
      const allowed = new Set([inst.id, ...inst.links.map((l) => l.id)]);
      for (const { owner } of steps) expect(allowed.has(owner.id)).toBe(true);
    }
  });

  it("knows which sides a project has", () => {
    expect(hasSurface(byId("chatbot-ex")!, "phone")).toBe(true);
    expect(hasSurface(byId("chatbot-complaint")!, "phone")).toBe(false);
  });
});
