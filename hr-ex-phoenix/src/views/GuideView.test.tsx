import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { DATA } from "../lib/data";
import { GuideView } from "./GuideView";

afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers(); });

describe.each(["en", "fa"] as const)("GuideView (%s)", (lang) => {
  const d = DATA[lang];
  const g = d.guide!;

  it("renders a TOC link and an h2 section per guide section", () => {
    render(<GuideView d={d} />);
    const nav = screen.getByRole("navigation");
    const links = nav.querySelectorAll("a");
    expect(links).toHaveLength(g.sections.length);
    expect(links[2]).toHaveAttribute("href", "#/guide/3");
    expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(g.sections.length);
    expect(screen.getAllByRole("region")).toHaveLength(g.sections.length);
    expect(links[0]).toHaveAttribute("aria-current", "location");
  });

  it("clicking a TOC entry marks it current and updates the URL without a route change", async () => {
    const user = userEvent.setup();
    const routed: string[] = [];
    const onHash = (e: HashChangeEvent) => routed.push(e.newURL);
    window.addEventListener("hashchange", onHash);
    render(<GuideView d={d} />);
    const links = screen.getByRole("navigation").querySelectorAll("a");
    await user.click(links[4]);
    expect(links[4]).toHaveAttribute("aria-current", "location");
    expect(links[0]).not.toHaveAttribute("aria-current");
    expect(window.location.hash).toBe("#/guide/5");
    expect(routed.filter((u) => u.endsWith("#/guide/5"))).toEqual([]);
    window.removeEventListener("hashchange", onHash);
  });
});

describe("GuideView deep links and scroll spy", () => {
  const d = DATA.en;

  it("opens at #/guide/<n> and scrolls to that section", () => {
    vi.useFakeTimers();
    const spy = vi.fn();
    Element.prototype.scrollIntoView = spy;
    window.location.hash = "#/guide/4";
    render(<GuideView d={d} />);
    act(() => { vi.runAllTimers(); });
    const links = screen.getByRole("navigation").querySelectorAll("a");
    expect(links[3]).toHaveAttribute("aria-current", "location");
    expect(spy).toHaveBeenCalled();
    expect(spy.mock.contexts.at(-1)).toHaveProperty("id", "g4");
  });

  it("ignores out-of-range and plain #/guide", () => {
    window.location.hash = "#/guide/999";
    render(<GuideView d={d} />);
    expect(screen.getByRole("navigation").querySelectorAll("a")[0]).toHaveAttribute("aria-current", "location");
  });

  it("highlights the TOC entry of the section in view", () => {
    let cb: IntersectionObserverCallback = () => {};
    const observed: Element[] = [];
    vi.stubGlobal("IntersectionObserver", class {
      constructor(c: IntersectionObserverCallback) { cb = c; }
      observe(el: Element) { observed.push(el); }
      disconnect() {}
      unobserve() {}
      takeRecords() { return []; }
    });
    render(<GuideView d={d} />);
    expect(observed).toHaveLength(d.guide!.sections.length);
    act(() => cb([{ target: observed[6], isIntersecting: true }, { target: observed[7], isIntersecting: true }] as unknown as IntersectionObserverEntry[], {} as IntersectionObserver));
    const links = screen.getByRole("navigation").querySelectorAll("a");
    expect(links[6]).toHaveAttribute("aria-current", "location");
    act(() => cb([{ target: observed[6], isIntersecting: false }] as unknown as IntersectionObserverEntry[], {} as IntersectionObserver));
    expect(links[7]).toHaveAttribute("aria-current", "location");
  });
});
