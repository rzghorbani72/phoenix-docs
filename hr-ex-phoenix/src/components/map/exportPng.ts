import { toPng } from "html-to-image";

const SKIP = ["react-flow__minimap", "react-flow__controls", "react-flow__panel", "nodetip"];

/** Save what the map canvas currently shows (no toolbar, minimap or controls) on the theme background. */
export async function exportPng(fileBase: string) {
  const el = document.querySelector<HTMLElement>(".mapwrap .react-flow");
  if (!el) throw new Error("no map");
  const bg = getComputedStyle(document.body).backgroundColor || "#0b1017";
  const opts = {
    backgroundColor: bg, pixelRatio: Math.min(2, window.devicePixelRatio * 1.5 || 2), cacheBust: true,
    filter: (n: HTMLElement) => !(n.classList && SKIP.some((c) => n.classList.contains(c))),
  };
  let url: string;
  try {
    url = await toPng(el, opts);
  } catch {
    // Web-font embedding can fail (offline, CORS); the image is still useful with fallback fonts.
    url = await toPng(el, { ...opts, skipFonts: true });
  }
  const a = document.createElement("a");
  a.href = url;
  a.download = `${fileBase}-${new Date().toISOString().slice(0, 10)}.png`;
  document.body.appendChild(a);
  a.click();
  a.remove();
}
