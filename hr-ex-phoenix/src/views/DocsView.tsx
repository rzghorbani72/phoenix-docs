import { useCallback, useMemo, useState } from "react";
import type { Data } from "../lib/types";
import { LABELS, type Labels } from "./docs/labels";
import { CATEGORIES, DOCS, fileName, fileUrl, fmtSize, previewFile, type DocEntry, type DocFile } from "./docs/manifest";
import { DocPreview } from "./docs/DocPreview";
import "./docs/docs.css";

const ALL_TYPES = [...new Set(DOCS.flatMap((e) => e.files.map((f) => f.type)))].sort();
const IMAGE = new Set(["png", "jpg", "jpeg", "svg"]);
const norm = (s: string) => s.toLowerCase().replace(/[‌_-]+/g, " ");

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
          <a key={f.path} className={`doc-type t-${f.type}`} href={fileUrl(f)} target="_blank" rel="noopener" title={`${fileName(f)} · ${fmtSize(f.size, d.lang)}`}>{f.type.toUpperCase()}</a>
        ))}
        <span className="doc-size">{fmtSize(total, d.lang)}</span>
        <span className="doc-lang">{L.langName[e.lang]}</span>
        {e.folder && <span className="doc-folder" dir="ltr">{e.folder}/</span>}
      </div>
      <div className="doc-actions">
        <a className="doc-btn primary" href={fileUrl(main)} target="_blank" rel="noopener">{L.open} ↗</a>
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
      (!lang || e.lang === lang) &&
      words.every((w) => index.get(e)!.includes(w)));
  }, [q, types, lang, index]);
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
        return (
          <section key={c} className="docs-cat" id={`docs-${c}`}>
            <header className="docs-cat-head">
              <h2>{name} <span className="docs-n">{count(items.length)}</span></h2>
              {!filtering && blurb && <p className="muted">{blurb}</p>}
            </header>
            <div className="docs-grid">
              {items.map((e) => <DocCard key={e.id} e={e} d={d} L={L} onPreview={(en, f) => setOpen({ e: en, f })} />)}
            </div>
          </section>
        );
      })}

      {open && <DocPreview entry={open.e} file={open.f} L={L} onFile={(f) => setOpen({ e: open.e, f })} onClose={close} />}
    </div>
  );
}
