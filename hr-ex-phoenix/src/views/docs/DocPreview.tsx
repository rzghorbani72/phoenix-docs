import { useEffect, useState } from "react";
import type { Labels } from "./labels";
import { fileName, fileUrl, PREVIEWABLE, type DocEntry, type DocFile } from "./manifest";
import { fetchHead, parseCsv } from "./csv";

const CSV_ROWS = 50;
const TEXT_LIMIT = 400_000; // bytes read for csv/md/json previews

type Loaded = { kind: "loading" } | { kind: "error" } | { kind: "text"; text: string; partial: boolean } | { kind: "csv"; rows: string[][]; more: boolean };

/** Fetches csv/md/json for the preview (mounted with key=file, so it starts in "loading"). */
function useFileText(file: DocFile): Loaded {
  const [state, setState] = useState<Loaded>({ kind: "loading" });
  useEffect(() => {
    if (!["csv", "md", "json"].includes(file.type)) return;
    const ctl = new AbortController();
    fetchHead(fileUrl(file), TEXT_LIMIT, ctl.signal)
      .then(({ text, partial }) => {
        if (file.type !== "csv") return setState({ kind: "text", text, partial });
        const { rows, truncated } = parseCsv(text, CSV_ROWS + 1, partial);
        const kept = rows.filter((r) => r.some((c) => c.trim()));
        setState({ kind: "csv", rows: kept, more: truncated || kept.length > CSV_ROWS });
      })
      .catch((e: unknown) => { if (!ctl.signal.aborted) { console.warn("docs preview:", e); setState({ kind: "error" }); } });
    return () => ctl.abort();
  }, [file]);
  return state;
}

function TextBody({ file, L }: { file: DocFile; L: Labels }) {
  const s = useFileText(file);
  if (s.kind === "loading") return <p className="muted dp-msg">{L.loading}</p>;
  if (s.kind === "error") return <div className="note warn dp-msg">{L.fetchFail}</div>;
  if (s.kind === "text") return <pre className="dp-pre" dir="auto">{s.text}{s.partial ? "\n…" : ""}</pre>;
  const [head = [], ...rows] = s.rows;
  return (
    <div className="dp-csv">
      <p className="muted">{L.rowsOf(Math.min(rows.length, CSV_ROWS), s.more)}</p>
      <div className="tw">
        <table>
          <thead><tr><th>#</th>{head.map((c, i) => <th key={i} dir="auto">{c}</th>)}</tr></thead>
          <tbody>
            {rows.slice(0, CSV_ROWS).map((r, i) => (
              <tr key={i}><td className="dp-n">{i + 1}</td>{r.map((c, j) => <td key={j} dir="auto"><div className="dp-cell">{c}</div></td>)}</tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Body({ file, title, L }: { file: DocFile; title: string; L: Labels }) {
  const url = fileUrl(file);
  if (file.type === "html" || file.type === "pdf") return <iframe key={url} className="dp-frame" src={url} title={title} />;
  if (["png", "jpg", "jpeg", "svg"].includes(file.type)) return <div className="dp-img"><img src={url} alt={title} /></div>;
  if (PREVIEWABLE.has(file.type)) return <TextBody key={url} file={file} L={L} />;
  return <p className="muted dp-msg">{L.noPreview}</p>;
}

/** Side panel with the document inside the app; twins (html/pdf …) switch with the type tabs. */
export function DocPreview({ entry, file, L, onFile, onClose }: {
  entry: DocEntry; file: DocFile; L: Labels; onFile: (f: DocFile) => void; onClose: () => void;
}) {
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", k);
    return () => window.removeEventListener("keydown", k);
  }, [onClose]);
  const previewable = entry.files.filter((f) => PREVIEWABLE.has(f.type));
  return (
    <aside className="dp" role="dialog" aria-label={entry.title}>
      <div className="dp-top">
        <div className="dp-title">
          <strong dir="auto">{entry.title}</strong>
          <span className="dp-file" dir="ltr">{fileName(file)}</span>
        </div>
        <div className="dp-actions">
          {previewable.length > 1 && (
            <div className="seg dp-seg">
              {previewable.map((f) => (
                <button key={f.path} className={f === file ? "on" : ""} onClick={() => onFile(f)}>{f.type.toUpperCase()}</button>
              ))}
            </div>
          )}
          <a className="doc-btn" href={fileUrl(file)} target="_blank" rel="noopener" title={L.openNew}>↗</a>
          <button className="icon" onClick={onClose} aria-label={L.close} title={L.close}>✕</button>
        </div>
      </div>
      <div className="dp-body"><Body file={file} title={entry.title} L={L} /></div>
    </aside>
  );
}
