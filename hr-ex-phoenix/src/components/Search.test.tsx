import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { DATA } from "../lib/data";
import { Search } from "./Search";

describe("Search palette", () => {
  it("is a modal dialog with a combobox driving a listbox", () => {
    render(<Search d={DATA.en} onClose={() => {}} />);
    const dialog = screen.getByRole("dialog");
    expect(dialog).toHaveAttribute("aria-modal", "true");
    const input = screen.getByRole("combobox");
    expect(input).toHaveFocus();
    const list = screen.getByRole("listbox");
    expect(input).toHaveAttribute("aria-controls", list.id);
    const opts = screen.getAllByRole("option");
    expect(opts.length).toBe(12);
    expect(input).toHaveAttribute("aria-activedescendant", opts[0].id);
    expect(opts[0]).toHaveAttribute("aria-selected", "true");
  });

  it("arrows move the active option; Enter navigates and closes", async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();
    render(<Search d={DATA.en} onClose={onClose} />);
    await user.type(screen.getByRole("combobox"), "gemma");
    const opts = screen.getAllByRole("option");
    expect(opts.length).toBeGreaterThan(1);
    await user.keyboard("{ArrowDown}");
    expect(screen.getByRole("combobox")).toHaveAttribute("aria-activedescendant", opts[1].id);
    expect(opts[1]).toHaveAttribute("aria-selected", "true");
    await user.keyboard("{Enter}");
    expect(onClose).toHaveBeenCalledOnce();
    expect(window.location.hash).not.toBe("");
  });

  it("traps Tab inside, closes on Escape and restores focus", async () => {
    const user = userEvent.setup();
    const opener = document.createElement("button");
    document.body.append(opener);
    opener.focus();
    const onClose = vi.fn();
    const { unmount } = render(<Search d={DATA.fa} onClose={onClose} />);
    expect(screen.getByRole("dialog")).toHaveAttribute("dir", "rtl");
    await user.tab();
    expect(screen.getByRole("combobox")).toHaveFocus();
    await user.keyboard("{Escape}");
    expect(onClose).toHaveBeenCalledOnce();
    unmount();
    expect(opener).toHaveFocus();
    opener.remove();
  });

  it("shows a status message when nothing matches", async () => {
    const user = userEvent.setup();
    render(<Search d={DATA.en} onClose={() => {}} />);
    await user.type(screen.getByRole("combobox"), "qqqzzz nothing");
    expect(screen.queryAllByRole("option")).toHaveLength(0);
    expect(screen.getByRole("status")).toHaveTextContent("No results");
    expect(screen.getByRole("combobox")).not.toHaveAttribute("aria-activedescendant");
  });
});
