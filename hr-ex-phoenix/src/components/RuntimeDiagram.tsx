import { diagramUrl, type RuntimeDiagramId } from "../lib/runtimeDiagram";

interface Props {
  id: RuntimeDiagramId;
  lang: "en" | "fa";
  theme: "dark" | "light";
  /** Node to highlight when the diagram opens. */
  node?: string;
}

/**
 * A step's runtime diagram: a read-only preview in the panel, the full explorer in its own tab.
 * The page is generated outside this app, so it stays sandboxed. It is only reloaded when its URL changes.
 */
export function RuntimeDiagram({ id, lang, theme, node }: Props) {
  const fa = lang === "fa";
  const title = fa ? "نمودار اجرای این مرحله" : "How this runs";
  return (
    <section className="runtime-diagram">
      <h3 className="sub">{title}</h3>
      <iframe key={`${id}-${theme}-${node ?? ""}`} className="runtime-frame" title={title} loading="lazy" sandbox="allow-scripts"
        src={diagramUrl(id, { embed: true, theme, node })} />
      <p className="muted runtime-note">
        <a href={diagramUrl(id, { embed: false, theme, node })} target="_blank" rel="noopener">{fa ? "باز کردن نمودار کامل ↗" : "Open the full diagram ↗"}</a>
        {" · "}{fa ? "از مخزن Phoenix؛ متن نمودار انگلیسی است." : "From the Phoenix repo."}
      </p>
    </section>
  );
}
