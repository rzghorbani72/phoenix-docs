import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeAll, describe, expect, it, vi } from "vitest";
import { DATA } from "../../lib/data";
import { byId, instanceLane } from "../../lib/instances";
import { T } from "../../views/instances/i18n";
import { MapToolbar } from "./MapToolbar";
import OverviewMap from "./OverviewMap";
import { STATUSES, type MapFilters } from "./shared";

// jsdom cannot lay out the diagram, so these tests use the phone layout: the same cards as a list.
beforeAll(() => {
  window.matchMedia = ((q: string) => ({ matches: true, media: q, addEventListener() {}, removeEventListener() {} })) as unknown as typeof window.matchMedia;
});

const filters: MapFilters = { model: "", statuses: new Set(STATUSES), query: "", cross: false, instance: "" };

describe.each(["en", "fa"] as const)("the overview for one instance (%s)", (lang) => {
  const d = DATA[lang];
  const s = T(lang);
  const card = (prefix: string) => screen.getAllByRole("button").find((b) => within(b).queryByText(prefix))!;

  it("shows the general pipeline until an instance is chosen", () => {
    render(<OverviewMap d={d} theme="dark" onLane={() => {}} />);
    expect(screen.queryByText(s.statParts)).not.toBeInTheDocument();
  });

  it("shows the selected instance's own brain on the brain card", () => {
    const ex = byId("chatbot-ex")!;
    render(<OverviewMap d={d} theme="dark" onLane={() => {}} instance={ex} />);
    const brain = card("B");
    expect(within(brain).getByText("aiva")).toBeInTheDocument();
    const { detail } = instanceLane(ex, "brain");
    expect(brain).toHaveTextContent(`${detail!.on}/${detail!.components.length}`);
  });

  it("changes when another instance is chosen", () => {
    const { rerender } = render(<OverviewMap d={d} theme="dark" onLane={() => {}} instance={byId("chatbot-ex")!} />);
    rerender(<OverviewMap d={d} theme="dark" onLane={() => {}} instance={byId("chatbot-shaad-iva")!} />);
    expect(within(card("B")).getByText("adcs-chatbot")).toBeInTheDocument();
    expect(within(card("B")).getByText(s.stages.brain)).toBeInTheDocument(); // not the map's title, which names aiva
  });

  it("tells what ops cannot show, and dims it", () => {
    render(<OverviewMap d={d} theme="dark" onLane={() => {}} instance={byId("chatbot-shaad-iva")!} />);
    expect(card("M")).toHaveTextContent(s.laneNotInOps);
    expect(card("M")).toHaveClass("ov-unused");
    expect(card("B")).not.toHaveClass("ov-unused");
  });

  it("marks memory as part of an aiva brain", () => {
    render(<OverviewMap d={d} theme="dark" onLane={() => {}} instance={byId("chatbot-ex")!} />);
    expect(card("M")).toHaveTextContent(s.laneBuiltIn);
    expect(card("M")).not.toHaveClass("ov-unused");
  });

  it("focuses the lane when a card is selected", async () => {
    const onLane = vi.fn();
    render(<OverviewMap d={d} theme="dark" onLane={onLane} instance={byId("chatbot-ex")!} />);
    await userEvent.setup().click(card("B"));
    expect(onLane).toHaveBeenCalledWith("brain");
  });
});

describe("the instance picker", () => {
  it("is on the overview and sets the filter", async () => {
    const setFilters = vi.fn();
    render(<MapToolbar d={DATA.en} filters={filters} setFilters={setFilters} overview tourActive={false} />);
    const user = userEvent.setup();
    await user.click(screen.getByRole("button", { expanded: false, name: /Filters/ }));
    await user.selectOptions(screen.getByRole("combobox", { name: "Instance" }), "chatbot-ex");
    expect(setFilters).toHaveBeenCalledWith({ ...filters, instance: "chatbot-ex" });
  });
});
