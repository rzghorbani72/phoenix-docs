import { useCallback, useMemo, useState } from "react";
import type { Data } from "../lib/types";
import { LABELS, type Labels } from "./docs/labels";
import { CATEGORIES, DOCS, docKey, docRoute, fileName, fileUrl, fmtSize, previewFile, twinKey, type DocEntry, type DocFile } from "./docs/manifest";
import { DocPreview } from "./docs/DocPreview";
import "./docs/docs.css";

const ALL_TYPES = [...new Set(DOCS.flatMap((e) => e.files.map((f) => f.type)))].sort();
const IMAGE = new Set(["png", "jpg", "jpeg", "svg"]);
/** Categories folded by default. Their cards open by themselves while a search or filter is active. */
const COLLAPSED = new Set<string>();
const norm = (s: string) => s.toLowerCase().replace(/[‌_-]+/g, " ");

/** Twin keys that have a version in each language: without a language filter only the reader's one is listed. */
const TWINS = (() => {
  const by = new Map<string, Set<string>>();
  for (const e of DOCS) by.set(twinKey(e), (by.get(twinKey(e)) ?? new Set()).add(e.lang));
  return new Set([...by].filter(([, l]) => l.size > 1).map(([k]) => k));
})();

/** Where a file opens: HTML inside the app layout, everything else in a new tab. */
const openProps = (f: DocFile) =>
  f.type === "html" ? { href: docRoute(docKey(f.path)) } : { href: fileUrl(f), target: "_blank", rel: "noopener" };

function haystack(e: DocEntry): string {
  return norm([e.title, e.desc.en, e.desc.fa, e.id, e.category, ...e.files.map(fileName)].join(" "));
}

function DocCard({ e, d, L, onPreview }: { e: DocEntry; d: Data; L: Labels; onPreview: (e: DocEntry, f: DocFile) => void }) {
  const main = e.files[0];
  const pv = previewFile(e);
  const desc = e.desc[d.lang] || e.desc[d.lang === "fa" ? "en" : "fa"];
  const total = e.files.reduce((n, f) => n + f.size, 0);
  return (
    <article className={`doc-card${e.start ? " start" : ""}`}>
      {IMAGE.has(main.type) && (
        <button className="doc-thumb" onClick={() => onPreview(e, main)} aria-label={L.preview}>
          <img src={fileUrl(main)} alt="" loading="lazy" />
        </button>
      )}
      <div className="doc-head">
        {e.start && <span className="doc-star">★ {L.startHere}</span>}
        <h3 dir="auto">{e.title}</h3>
      </div>
      {desc && <p className="doc-desc" dir="auto">{desc}</p>}
      <div className="doc-meta">
        {e.files.map((f) => (
          <a key={f.path} className={`doc-type t-${f.type}`} {...openProps(f)} title={`${fileName(f)} · ${fmtSize(f.size, d.lang)}`}>{f.type.toUpperCase()}</a>
        ))}
        <span className="doc-size">{fmtSize(total, d.lang)}</span>
        <span className="doc-lang">{L.langName[e.lang]}</span>
        {e.folder && <span className="doc-folder" dir="ltr">{e.folder}/</span>}
      </div>
      <div className="doc-actions">
        <a className="doc-btn primary" {...openProps(main)}>{L.open}{main.type === "html" ? "" : " ↗"}</a>
        {pv && <button className="doc-btn" onClick={() => onPreview(e, pv)}>{L.preview}</button>}
      </div>
    </article>
  );
}

/** Searchable library of every file under public/docs (manifest: content/build_docs_manifest.py). */
export function DocsView({ d }: { d: Data }) {
  const L = LABELS[d.lang];
  const [q, setQ] = useState("");
  const [types, setTypes] = useState<Set<string>>(new Set());
  const [lang, setLang] = useState<"" | "en" | "fa">("");
  const [open, setOpen] = useState<{ e: DocEntry; f: DocFile } | null>(null);
  const close = useCallback(() => setOpen(null), []);

  const index = useMemo(() => new Map(DOCS.map((e) => [e, haystack(e)])), []);
  const shown = useMemo(() => {
    const words = norm(q).split(/\s+/).filter(Boolean);
    return DOCS.filter((e) =>
      (!types.size || e.files.some((f) => types.has(f.type))) &&
      (lang ? e.lang === lang : e.lang === d.lang || !TWINS.has(twinKey(e))) &&
      words.every((w) => index.get(e)!.includes(w)));
  }, [q, types, lang, index, d.lang]);
  const filtering = q !== "" || types.size > 0 || lang !== "";
  const toggle = (t: string) => setTypes((s) => { const n = new Set(s); if (n.has(t)) n.delete(t); else n.add(t); return n; });
  const count = (n: number) => n.toLocaleString(d.lang === "fa" ? "fa-IR" : "en-US");

  return (
    <div className={`page docs-page${open ? " with-preview" : ""}`}>
      <h1>{L.title}</h1>
      <p className="docs-lede">{L.lede}</p>

      <div className="docs-bar">
        <input className="filter docs-q" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder={L.search} aria-label={L.search} />
        <div className="docs-types" role="group">
          <button className={`doc-chip${types.size ? "" : " on"}`} onClick={() => setTypes(new Set())}>{L.all}</button>
          {ALL_TYPES.map((t) => (
            <button key={t} className={`doc-chip t-${t}${types.has(t) ? " on" : ""}`} onClick={() => toggle(t)} aria-pressed={types.has(t)}>{t.toUpperCase()}</button>
          ))}
        </div>
        <div className="seg docs-seg" role="group" aria-label={L.lang}>
          {(["", "fa", "en"] as const).map((l) => (
            <button key={l || "all"} className={lang === l ? "on" : ""} onClick={() => setLang(l)}>{l ? L.langName[l] : L.all}</button>
          ))}
        </div>
        <span className="muted docs-count">{count(shown.length)} {L.docs} · {count(shown.reduce((n, e) => n + e.files.length, 0))} {L.files}</span>
      </div>

      {!shown.length && (
        <div className="docs-empty">
          <p>{L.none}</p>
          <button className="doc-btn" onClick={() => { setQ(""); setTypes(new Set()); setLang(""); }}>{L.clear}</button>
        </div>
      )}

      {CATEGORIES.map((c) => {
        const items = shown.filter((e) => e.category === c);
        if (!items.length) return null;
        const [name, blurb] = L.cats[c] ?? [c, ""];
        const head = (
          <header className="docs-cat-head">
            <h2>{name} <span className="docs-n">{count(items.length)}</span></h2>
            {!filtering && blurb && <p className="muted">{blurb}</p>}
          </header>
        );
        const grid = (
          <div className="docs-grid">
            {items.map((e) => <DocCard key={e.id} e={e} d={d} L={L} onPreview={(en, f) => setOpen({ e: en, f })} />)}
          </div>
        );
        return (
          <section key={c} className="docs-cat" id={`docs-${c}`}>
            {COLLAPSED.has(c)
              ? <details className="docs-fold" open={filtering}><summary>{head}</summary>{grid}</details>
              : <>{head}{grid}</>}
          </section>
        );
      })}

      {open && <DocPreview entry={open.e} file={open.f} L={L} onFile={(f) => setOpen({ e: open.e, f })} onClose={close} />}
    </div>
  );
}
