import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { DATA } from "../lib/data";
import { ModelPage } from "./ModelPage";

describe.each(["en", "fa"] as const)("ModelPage (%s)", (lang) => {
  const d = DATA[lang];
  const ids = d.models.cards.map((c) => c.id).filter((x): x is string => !!x && !!d.models.pages[x]);

  it("links back, to used-in steps, and to prev/next models", () => {
    render(<ModelPage d={d} id={ids[1]} />);
    const hrefs = screen.getAllByRole("link").map((a) => a.getAttribute("href"));
    expect(hrefs).toContain("#/models");
    expect(hrefs).toContain(`#/model/${ids[0]}`);
    expect(hrefs).toContain(`#/model/${ids[2]}`);
    for (const s of d.models.cards[1].steps ?? []) expect(hrefs).toContain(`#/step/${s}`);
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
  });

  it("first and last models have only one neighbour link", () => {
    const { unmount } = render(<ModelPage d={d} id={ids[0]} />);
    expect(screen.queryByRole("link", { name: new RegExp(d.ui.prev) })).toBeNull();
    unmount();
    render(<ModelPage d={d} id={ids[ids.length - 1]} />);
    expect(screen.queryByRole("link", { name: new RegExp(d.ui.next) })).toBeNull();
  });

  it("shows a not-found page with a way back", () => {
    render(<ModelPage d={d} id="nope" />);
    expect(screen.getByRole("heading", { level: 1 })).toBeInTheDocument();
    expect(screen.getByRole("link")).toHaveAttribute("href", "#/models");
  });
});
