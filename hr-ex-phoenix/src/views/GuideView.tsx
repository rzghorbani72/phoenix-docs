import { useEffect, useState, type MouseEvent } from "react";
import type { Data } from "../lib/types";
import { ctxFor } from "../lib/md";
import { BodyView, Md } from "../components/Blocks";
import { EnTag } from "../components/Common";

/** 0-based section index from a `#/guide/<n>` hash (n is 1-based, as shown in the TOC); undefined for plain `#/guide`. */
function guideSectionFromHash(hash: string, count: number): number | undefined {
  const m = /^#\/?guide\/(\d+)\/?$/.exec(hash);
  if (!m) return undefined;
  const n = Number(m[1]);
  return n >= 1 && n <= count ? n - 1 : undefined;
}

const secId = (i: number) => `g${i + 1}`;

function scrollToSection(i: number, smooth: boolean) {
  const el = document.getElementById(secId(i));
  el?.scrollIntoView?.({ behavior: smooth ? "smooth" : "auto", block: "start" });
  const h = el?.querySelector<HTMLElement>("h2");
  if (h) { h.tabIndex = -1; h.focus({ preventScroll: true }); }
}

export function GuideView({ d }: { d: Data }) {
  const g = d.guide;
  const ctx = ctxFor(d, 0);
  const count = g?.sections.length ?? 0;
  const [active, setActive] = useState<number>(() => guideSectionFromHash(window.location.hash, count) ?? 0);

  // Deep links: #/guide/<n> on load or on any later hash change. The scroll is deferred one tick
  // because App scrolls to the top after a route change, in an effect that runs after ours.
  useEffect(() => {
    let t: ReturnType<typeof setTimeout> | undefined;
    const follow = () => {
      const i = guideSectionFromHash(window.location.hash, count);
      if (i === undefined) return;
      setActive(i);
      clearTimeout(t);
      t = setTimeout(() => scrollToSection(i, false), 0);
    };
    follow();
    window.addEventListener("hashchange", follow);
    return () => { window.removeEventListener("hashchange", follow); clearTimeout(t); };
  }, [count]);

  // Highlight the TOC entry of the section currently in view.
  useEffect(() => {
    if (!count || typeof IntersectionObserver === "undefined") return;
    const visible = new Set<number>();
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        const i = Number((e.target as HTMLElement).dataset.sec);
        if (e.isIntersecting) visible.add(i); else visible.delete(i);
      }
      if (visible.size) setActive(Math.min(...visible));
    }, { rootMargin: "-72px 0px -55% 0px", threshold: 0 });
    for (let i = 0; i < count; i++) {
      const el = document.getElementById(secId(i));
      if (el) io.observe(el);
    }
    return () => io.disconnect();
  }, [count, d]);

  if (!g) return null;
  const fa = d.lang === "fa";
  const langProps = g.fallback && fa ? { lang: "en", dir: "ltr" as const } : {};

  const jump = (e: MouseEvent<HTMLAnchorElement>, i: number) => {
    // Plain clicks scroll smoothly and update the URL without a hashchange (so App does not re-route
    // and jump to the top); modified clicks keep normal link behaviour (new tab etc.).
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    setActive(i);
    try { history.replaceState(history.state, "", `#/guide/${i + 1}`); } catch { /* sandboxed */ }
    scrollToSection(i, true);
  };

  return (
    <div className="page guide">
      <nav className="toc" aria-label={fa ? "فهرست راهنما" : "Guide contents"}>
        {g.sections.map(([h], i) => (
          <a key={i} href={`#/guide/${i + 1}`} aria-current={active === i ? "location" : undefined} onClick={(e) => jump(e, i)}>
            <span aria-hidden="true">{i + 1}</span><Md text={h} ctx={ctx} />
          </a>
        ))}
      </nav>
      <div {...langProps}>
        <h1><Md text={g.title} ctx={ctx} /> {g.fallback && <EnTag d={d} />}</h1>
        <Md as="p" text={g.lede} ctx={ctx} />
        {g.sections.map(([h, b], i) => (
          <section className="sec" id={secId(i)} data-sec={i} key={i} aria-labelledby={`${secId(i)}-h`}>
            <h2 id={`${secId(i)}-h`}><Md text={h} ctx={ctx} /></h2>
            <BodyView body={b} ctx={ctx} />
          </section>
        ))}
      </div>
    </div>
  );
}
