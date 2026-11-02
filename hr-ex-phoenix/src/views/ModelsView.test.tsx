import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { DATA } from "../lib/data";
import { plain } from "../lib/md";
import { ModelsView } from "./ModelsView";

describe.each(["en", "fa"] as const)("ModelsView (%s)", (lang) => {
  const d = DATA[lang];

  it("renders one card per model with a real link to its page", () => {
    render(<ModelsView d={d} />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(plain(d.models.title).replace(/[`*]/g, "").trim().slice(0, 10));
    const cards = screen.getAllByRole("article");
    expect(cards).toHaveLength(d.models.cards.length);
    for (const c of d.models.cards.filter((x) => x.id)) {
      const link = screen.getAllByRole("link").find((a) => a.getAttribute("href") === `#/model/${c.id}`);
      expect(link, c.id).toBeDefined();
      expect(link!.closest("h2")).not.toBeNull();
    }
  });

  it("step pills are links with descriptive labels", () => {
    render(<ModelsView d={d} />);
    const card = d.models.cards.find((c) => c.steps?.length)!;
    const pill = screen.getAllByRole("link").find((a) => a.getAttribute("href") === `#/step/${card.steps![0]}`);
    expect(pill).toBeDefined();
    expect(pill!.getAttribute("aria-label")).toMatch(/^[A-Z]+\d+ · .+/);
  });

  it("filters cards by text and shows an empty state", async () => {
    const user = userEvent.setup();
    render(<ModelsView d={d} />);
    const box = screen.getByRole("searchbox");
    await user.type(box, "soniox");
    const cards = screen.getAllByRole("article");
    expect(cards).toHaveLength(1);
    const title = within(cards[0]).getByRole("heading", { level: 2 });
    expect(title).toHaveTextContent(/soniox/i);
    expect(within(title).getByRole("link")).toHaveAttribute("href", expect.stringMatching(/^#\/model\//));
    expect(screen.getByRole("status")).toHaveTextContent(/1/);
    await user.clear(box);
    await user.type(box, "zzzz-no-such-model");
    expect(screen.queryAllByRole("article")).toHaveLength(0);
    await user.clear(box);
    expect(screen.getAllByRole("article")).toHaveLength(d.models.cards.length);
  });
});
