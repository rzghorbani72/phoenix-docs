import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ErrorBoundary } from "./ErrorBoundary";

function Boom(): never {
  throw new Error("kaboom");
}

afterEach(() => { vi.restoreAllMocks(); document.documentElement.lang = ""; try { localStorage.clear(); } catch { /* */ } });

describe("ErrorBoundary", () => {
  it("renders children when nothing throws", () => {
    render(<ErrorBoundary><p>fine</p></ErrorBoundary>);
    expect(screen.getByText("fine")).toBeInTheDocument();
  });

  it("shows an English fallback with a working reload button", async () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    const onReload = vi.fn();
    render(<ErrorBoundary onReload={onReload}><Boom /></ErrorBoundary>);
    expect(screen.getByRole("alert")).toHaveAttribute("lang", "en");
    expect(screen.getByRole("heading")).toHaveTextContent("Something went wrong");
    expect(screen.getByText("kaboom")).toBeInTheDocument();
    await userEvent.setup().click(screen.getByRole("button", { name: "Reload" }));
    expect(onReload).toHaveBeenCalledOnce();
  });

  it("shows a Persian RTL fallback when the app language is Persian", () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    localStorage.setItem("pp-lang", "fa");
    render(<ErrorBoundary onReload={() => {}}><Boom /></ErrorBoundary>);
    const alert = screen.getByRole("alert");
    expect(alert).toHaveAttribute("dir", "rtl");
    expect(screen.getByRole("button", { name: "بارگذاری دوباره" })).toBeInTheDocument();
  });
});
