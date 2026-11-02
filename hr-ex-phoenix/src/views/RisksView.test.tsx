import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { DATA } from "../lib/data";
import { RisksView } from "./RisksView";

describe.each(["en", "fa"] as const)("RisksView (%s)", (lang) => {
  const d = DATA[lang];
  const n = (s: string) => d.risks.items.filter((r) => r.sev === s).length;

  it("shows every risk with an h2 under the h1, and counts per severity", () => {
    render(<RisksView d={d} />);
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(d.risks.items.length);
    const buttons = screen.getAllByRole("button");
    expect(buttons).toHaveLength(4);
    expect(buttons[0]).toHaveTextContent(`(${d.risks.items.length})`);
    expect(buttons[0]).toHaveAttribute("aria-pressed", "true");
    expect(buttons[1]).toHaveTextContent(`${d.ui.sev.high} (${n("high")})`);
    expect(buttons[2]).toHaveTextContent(`${d.ui.sev.med} (${n("med")})`);
    expect(buttons[3]).toHaveTextContent(`${d.ui.sev.low} (${n("low")})`);
    expect(n("high") + n("med") + n("low")).toBe(d.risks.items.length);
  });

  it("filters by severity and back to all", async () => {
    const user = userEvent.setup();
    render(<RisksView d={d} />);
    for (const [i, s] of [[1, "high"], [2, "med"], [3, "low"]] as const) {
      await user.click(screen.getAllByRole("button")[i]);
      const arts = screen.getAllByRole("article");
      expect(arts).toHaveLength(n(s));
      expect(arts.every((a) => a.classList.contains(`sev-${s}`))).toBe(true);
      expect(screen.getAllByRole("button")[i]).toHaveAttribute("aria-pressed", "true");
      expect(screen.getAllByRole("button")[0]).toHaveAttribute("aria-pressed", "false");
    }
    await user.click(screen.getAllByRole("button")[0]);
    expect(screen.getAllByRole("article")).toHaveLength(d.risks.items.length);
  });

  it("links risk steps to step pages", () => {
    render(<RisksView d={d} />);
    const withSteps = d.risks.items.find((r) => r.steps?.length);
    if (!withSteps) return;
    const hrefs = screen.getAllByRole("link").map((a) => a.getAttribute("href"));
    expect(hrefs).toContain(`#/step/${withSteps.steps![0]}`);
  });
});
