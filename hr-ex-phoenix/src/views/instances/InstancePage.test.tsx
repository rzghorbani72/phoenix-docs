import { fireEvent, render, screen, within } from "@testing-library/react";
import { beforeAll, describe, expect, it } from "vitest";
import { INSTANCES, byId, pipelineOf, stageDetail } from "../../lib/instances";
import { SETTING_WHY, STEP_WHY, partWhy } from "./explain";
import { T, settingLabel } from "./i18n";
import { InstancePage } from "./InstancePage";
import { StagePanel } from "./StagePanel";

const all = INSTANCES.instances;

// jsdom cannot lay out the diagram, so these tests use the phone layout: the same cards as a list.
beforeAll(() => {
  window.matchMedia = ((q: string) => ({ matches: true, media: q, addEventListener() {}, removeEventListener() {} })) as unknown as typeof window.matchMedia;
});

describe.each(["en", "fa"] as const)("InstancePage (%s)", (lang) => {
  const s = T(lang);
  const inst = byId("chatbot-ex")!;

  it("shows a project's admin panel, phone call and chatbot on one page", () => {
    render(<InstancePage lang={lang} id={inst.id} />);
    const sides = within(screen.getByRole("heading", { level: 2, name: s.surfaces }).closest("section")!);
    expect(sides.getByText(s.surfacePanel)).toBeInTheDocument();
    expect(sides.getByText("COA + CCA")).toBeInTheDocument();
    expect(sides.getByText(s.surfacePhone)).toBeInTheDocument();
    expect(sides.getByText(s.surfaceChatbot)).toBeInTheDocument();
    expect(sides.queryByText(s.surfaceNone)).not.toBeInTheDocument();
  });

  it("says when a project has no phone call", () => {
    render(<InstancePage lang={lang} id="chatbot-complaint" />);
    const sides = within(screen.getByRole("heading", { level: 2, name: s.surfaces }).closest("section")!);
    expect(sides.getByText(s.surfaceNone).closest(".ins-surface")).toHaveTextContent(s.surfacePhone);
  });

  it("links a phone line to the panel it shares, and back", () => {
    const raya = byId("aiva")!;
    const { unmount } = render(<InstancePage lang={lang} id="aiva-neda" />);
    const sides = within(screen.getByRole("heading", { level: 2, name: s.surfaces }).closest("section")!);
    expect(sides.getByRole("link", { name: raya.name[lang] })).toHaveAttribute("href", `#/instance/${raya.id}`);
    unmount();
    render(<InstancePage lang={lang} id={raya.id} />);
    expect(screen.getByRole("link", { name: byId("aiva-neda")!.name[lang] })).toBeInTheDocument();
  });

  it("opens a shared panel's analytics with its owner", () => {
    render(<InstancePage lang={lang} id="aiva-neda" stage="analytics" />);
    const panel = screen.getByRole("complementary", { name: s.stages.analytics });
    expect(within(panel).getByRole("link", { name: byId("aiva")!.name[lang] })).toBeInTheDocument();
  });

  it("shows name, about, release, state and a way back", () => {
    render(<InstancePage lang={lang} id={inst.id} />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(inst.name[lang]);
    expect(screen.getByText(inst.about[lang])).toBeInTheDocument();
    expect(screen.getAllByText(inst.release).length).toBeGreaterThan(0);
    expect(screen.getByText(s.states[inst.state])).toBeInTheDocument();
    expect(screen.getByRole("link", { name: s.back })).toHaveAttribute("href", "#/instances");
  });

  it("has no What to watch section", () => {
    render(<InstancePage lang={lang} id={inst.id} />);
    expect(screen.queryByRole("heading", { name: /what to watch|موارد قابل توجه/i })).toBeNull();
    expect(document.body.textContent).not.toMatch(/what to watch|موارد قابل توجه/i);
  });

  it("names what remains and what ended for a campaign, with no unfilled slot", () => {
    render(<InstancePage lang={lang} id="raya-beta" />);
    const section = screen.getByRole("heading", { name: s.campaignTitle }).closest("section")!;
    const groups = Array.from(section.querySelectorAll(".ins-campaign-group"));
    expect(groups).toHaveLength(2);
    expect(within(groups[0] as HTMLElement).getByText("coa-scoring-api")).toBeInTheDocument();
    for (const name of ["coa-scoring-syncer", "coa-scoring-sms-worker", "coa-scoring-campaign-events", "coa-scoring-maintenance"])
      expect(within(groups[1] as HTMLElement).getByText(name)).toBeInTheDocument();
    expect(within(groups[1] as HTMLElement).getAllByText(/0 0 31 2 \*/)).toHaveLength(2);
    expect(section.textContent).not.toMatch(/\{\w+\}/);
  });

  it("shows no campaign section for an instance that is no campaign", () => {
    render(<InstancePage lang={lang} id={inst.id} />);
    expect(screen.queryByRole("heading", { name: s.campaignTitle })).toBeNull();
  });

  it("lists the steps of the pipeline, marking the ones this instance does not have", () => {
    render(<InstancePage lang={lang} id="raya-beta" />);
    for (const name of Object.values(s.stages)) expect(screen.getByRole("button", { name: new RegExp(name) })).toBeInTheDocument();
    expect(screen.getAllByText(s.stageNone).length).toBeGreaterThan(0);
  });

  it("opens no panel until a step is selected, and selecting one goes to its link", async () => {
    render(<InstancePage lang={lang} id={inst.id} />);
    expect(screen.queryByRole("complementary")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: new RegExp(s.stages.call) }));
    expect(window.location.hash).toBe(`#/instance/${inst.id}/call`);
  });

  it("shows a step's parts and plain settings in the panel, with no warnings", () => {
    render(<InstancePage lang={lang} id={inst.id} stage="call" />);
    const panel = within(screen.getByRole("complementary", { name: s.stages.call }));
    expect(panel.getByText("agent")).toBeInTheDocument();
    expect(panel.getByText(settingLabel(lang, "AGENT_STT_CLIENT"))).toBeInTheDocument();
    expect(panel.getByRole("link", { name: s.howItWorks })).toHaveAttribute("href", "#/map/lane/call");
    expect(document.querySelector(".ins-panel .note")).toBeNull();
    expect(panel.getByText(new RegExp(s.liveNote))).toBeInTheDocument();
    expect(panel.getByText(STEP_WHY.call.what[lang])).toBeInTheDocument();
    expect(panel.getByText(STEP_WHY.call.why[lang])).toBeInTheDocument();
    expect(panel.getByText(SETTING_WHY.AGENT_TTS_SPEED[lang])).toBeInTheDocument();
    expect(panel.getByText(partWhy(lang, "egress", "media"))).toBeInTheDocument();
  });

  it("labels a missing replica count in plain words", () => {
    // CCA's phone line runs `vector` with no replica count in ops: the chart default.
    render(<InstancePage lang={lang} id="mci-agentic" stage="call" />);
    expect(screen.getAllByText(s.chartDefault).length).toBeGreaterThan(0);
  });

  it("has a label and a reason for every setting in the data", () => {
    const keys = new Set(all.flatMap((i) => Object.values(i.config).flatMap((g) => Object.keys(g))));
    for (const k of keys) {
      expect(settingLabel(lang, k), k).not.toBe(k);
      expect(SETTING_WHY[k]?.[lang], k).toBeTruthy();
    }
  });

  it("explains the step even when this instance does not have it", () => {
    render(<InstancePage lang={lang} id="raya-beta" stage="call" />);
    expect(screen.getByText(STEP_WHY.call.what[lang])).toBeInTheDocument();
    expect(screen.getByText(s.stepNone)).toBeInTheDocument();
  });

  it("shows the runtime diagram of the brain the instance runs, and none for other brains", () => {
    const { unmount } = render(<InstancePage lang={lang} id="aiva-poll" stage="brain" />);
    expect(document.querySelector("iframe")?.getAttribute("src")).toContain("diagrams/aiva-poll-runtime.html");
    unmount();
    render(<InstancePage lang={lang} id="chatbot-mobinnet-iva" stage="brain" />);
    expect(document.querySelector("iframe")).toBeNull();
  });

  it("ignores an unknown step in the link", () => {
    render(<InstancePage lang={lang} id={inst.id} stage="nope" />);
    expect(screen.queryByRole("complementary")).toBeNull();
  });

  it("shows an off instance as switched off", () => {
    const off = all.find((i) => i.state === "off")!;
    render(<InstancePage lang={lang} id={off.id} />);
    expect(document.querySelector(".ins-state")).toHaveTextContent(s.states.off);
    expect(document.querySelector(".ins-verdict")).toHaveClass("off");
  });

  it("answers in one sentence that names what remains, with no rows of dots", () => {
    render(<InstancePage lang={lang} id="raya-beta" />);
    const verdict = document.querySelector(".ins-verdict")!;
    expect(verdict).toHaveClass("warn");
    expect(within(verdict as HTMLElement).getByText("coa-scoring-api")).toBeInTheDocument();
    expect(verdict.textContent).not.toMatch(/\{\w+\}/);
    expect(document.querySelector(".ins-dots, .ins-dot, .ins-legend")).toBeNull();
  });

  it("shows each step as its name and one state word, nothing else", () => {
    render(<InstancePage lang={lang} id="chatbot-ex" />);
    const cards = Array.from(document.querySelectorAll(".ins-node"));
    expect(cards).toHaveLength(5);
    const words = [s.stepWordOn, s.stepWordPartly, s.stepWordOff, s.stageNone];
    for (const card of cards) {
      expect(words).toContain(card.querySelector(".ins-step-status strong")?.textContent);
      expect(card.querySelector(".ov-stats, .ins-step-parts, .ins-warn-badge, .ins-dot")).toBeNull();
    }
  });

  it("draws the campaign as a timeline from its end to the snapshot", () => {
    render(<InstancePage lang={lang} id="raya-beta" />);
    const timeline = document.querySelector(".ins-timeline")!;
    expect(timeline).toHaveClass("over");
    expect(timeline.textContent).toContain("2026-09-23");
    expect(timeline.textContent).toContain(INSTANCES.source.date);
    expect(timeline.textContent).toContain("42");
  });

  it("shows a scheduled job as scheduled, and one that never fires as never running", () => {
    render(<InstancePage lang={lang} id="raya-beta" stage="analytics" />);
    expect(screen.getAllByText(s.neverRuns).length).toBeGreaterThan(0);
  });

  it("explains an unknown id", () => {
    render(<InstancePage lang={lang} id="no-such-instance" />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(s.notFound);
    expect(screen.getByText("no-such-instance")).toBeInTheDocument();
  });
});

describe("the step panel beside the map", () => {
  it("moves along the map and closes to the overview", () => {
    const inst = byId("chatbot-ex")!;
    const detail = stageDetail(inst, pipelineOf(inst).find((p) => p.id === "brain")!);
    render(<StagePanel inst={inst} pageId={inst.id} detail={detail} lang="en" theme="dark" onMap />);
    const panel = screen.getByRole("complementary");
    const s = T("en");
    expect(within(panel).getByRole("link", { name: s.close })).toHaveAttribute("href", "#/map/overview");
    expect(within(panel).getAllByRole("link").map((a) => a.getAttribute("href"))).toContain("#/map/lane/kb");
  });
});
