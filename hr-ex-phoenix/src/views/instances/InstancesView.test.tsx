import { useState } from "react";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { INSTANCES, hasSurface, voiceDiff } from "../../lib/instances";
import { T } from "./i18n";
import { InstancesView, type InstancesMode } from "./InstancesView";

const all = INSTANCES.instances;

function Harness({ lang, start = "all" }: { lang: "en" | "fa"; start?: InstancesMode }) {
  const [mode, setMode] = useState<InstancesMode>(start);
  return <InstancesView lang={lang} mode={mode} onMode={setMode} />;
}

describe.each(["en", "fa"] as const)("InstancesView (%s)", (lang) => {
  const s = T(lang);

  it("lists every instance against every pipeline stage, linked to the map", () => {
    render(<Harness lang={lang} start="pipelines" />);
    expect(screen.getAllByRole("rowheader")).toHaveLength(all.length);
    expect(screen.getByRole("link", { name: s.stages.analytics })).toHaveAttribute("href", "#/map/lane/analytics");
  });

  it("states this is configured state, not live health", () => {
    render(<Harness lang={lang} />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(s.title);
    const note = document.querySelector(".note")!;
    expect(note).toHaveTextContent(INSTANCES.source.commit);
    expect(note).toHaveTextContent(INSTANCES.source.date);
    expect(document.body.textContent).not.toMatch(/\b(healthy|is up|is down)\b/i);
  });

  it("lists one card per instance with its name and a real link", () => {
    render(<Harness lang={lang} />);
    const cards = screen.getAllByRole("article");
    expect(cards).toHaveLength(all.length);
    for (const i of all) {
      const link = screen.getAllByRole("link").find((a) => a.getAttribute("href") === `#/instance/${i.id}`);
      expect(link, i.id).toHaveTextContent(i.name[lang]);
    }
  });

  it("marks names that still need confirming", () => {
    render(<Harness lang={lang} />);
    expect(screen.getAllByText(s.nameToConfirm)).toHaveLength(all.filter((i) => i.confirm).length);
  });

  it("filters by category and by name in either language or release", async () => {
    const user = userEvent.setup();
    render(<Harness lang={lang} />);
    const phones = all.filter((i) => i.category === "phone");
    await user.click(screen.getByRole("button", { name: `${s.categories.phone} (${phones.length})` }));
    expect(screen.getAllByRole("article")).toHaveLength(phones.length);
    await user.click(screen.getByRole("button", { name: `${s.allCategories} (${all.length})` }));

    const box = screen.getByRole("searchbox");
    for (const needle of ["صدای کارکنان", "Employee Voice", "chatbot-ex"]) {
      await user.clear(box);
      await user.type(box, needle);
      const cards = screen.getAllByRole("article");
      expect(cards.length).toBeGreaterThan(0);
      expect(cards.some((c) => within(c).queryByText(all[0].name[lang]))).toBe(true);
    }
    await user.clear(box);
    await user.type(box, "zzzz-no-such-instance");
    expect(screen.queryAllByRole("article")).toHaveLength(0);
    expect(screen.getByText(s.noMatch)).toBeInTheDocument();
  });

  it("switches modes", async () => {
    const user = userEvent.setup();
    render(<Harness lang={lang} />);
    const button = (name: string) => screen.getByRole("button", { name });
    expect(button(s.modeAll)).toHaveAttribute("aria-pressed", "true");

    await user.click(button(s.modeCompare));
    expect(button(s.modeCompare)).toHaveAttribute("aria-pressed", "true");
    expect(button(s.modeAll)).toHaveAttribute("aria-pressed", "false");
    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.queryAllByRole("article")).toHaveLength(0);

    await user.click(button(s.modeShared));
    for (const g of INSTANCES.shared) expect(screen.getByRole("heading", { name: `${g.name[lang]} (${g.items.length})` })).toBeInTheDocument();
  });

  it("compares live phone assistants and shows only differences by default", async () => {
    const user = userEvent.setup();
    render(<Harness lang={lang} start="compare" />);
    const phones = all.filter((i) => hasSurface(i, "phone") && i.state !== "off");
    const list = phones.filter((i) => Object.keys(i.config.voice).length);
    const skipped = phones.filter((i) => !list.includes(i));
    for (const i of skipped) expect(screen.getByText(new RegExp(i.name[lang].replace(/[()]/g, "\\$&")))).toBeInTheDocument();
    const rows = voiceDiff(list);
    const differing = rows.filter((r) => r.differs).length;
    expect(differing).toBeLessThan(rows.length);

    expect(screen.getAllByRole("columnheader")).toHaveLength(list.length + 1);
    expect(screen.getByRole("columnheader", { name: list[0].name[lang] })).toBeInTheDocument();
    expect(screen.getAllByRole("rowheader")).toHaveLength(differing);

    await user.click(screen.getByRole("checkbox", { name: s.showAll }));
    expect(screen.getAllByRole("rowheader")).toHaveLength(rows.length);
    await user.click(screen.getByRole("checkbox", { name: s.showAll }));
    expect(screen.getAllByRole("rowheader")).toHaveLength(differing);
  });

  it("has no What to watch view, tile or chip", () => {
    render(<Harness lang={lang} />);
    expect(screen.queryByRole("button", { name: /what to watch|موارد قابل توجه/i })).toBeNull();
    expect(document.body.textContent).not.toMatch(/what to watch|to watch:|needing attention|موارد قابل توجه|قابل توجه:|نیازمند توجه/i);
  });

  it("names the instances using a shared service", () => {
    render(<Harness lang={lang} start="shared" />);
    const item = INSTANCES.shared.flatMap((g) => g.items).find((x) => x.usedBy.length)!;
    const row = screen.getAllByRole("listitem").find((li) => within(li).queryByText(item.id))!;
    expect(within(row).getAllByRole("link").length).toBeGreaterThan(0);
  });
});

describe("projects", () => {
  const s = T("en");
  const panels = all.filter((i) => i.category === "panel");

  it("groups the projects that have an admin panel, with no call center or COA group", () => {
    render(<Harness lang="en" />);
    expect(screen.getByRole("heading", { name: s.categories.panel })).toBeInTheDocument();
    expect(screen.queryByText("Call center")).not.toBeInTheDocument();
    expect(screen.queryByText("COA dashboards")).not.toBeInTheDocument();
  });

  it("lists a project once, not once per side", () => {
    expect(panels).toHaveLength(12);
    render(<Harness lang="en" />);
    expect(screen.getAllByRole("link", { name: "Employee Voice (EX)" })).toHaveLength(1);
  });
});
