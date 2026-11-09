import { isStopped } from "../../lib/instances";
import type { Instance, InstanceState, Surface, SurfaceKind } from "../../lib/instanceTypes";
import { T, type Lang } from "./i18n";
import { InstanceLink, Tpl } from "./parts";

const TONE: Record<InstanceState, "ok" | "warn" | "off"> = { running: "ok", partial: "warn", off: "off" };

function Own({ inst, surface, lang, compact }: { inst: Instance; surface: Surface; lang: Lang; compact: boolean }) {
  const s = T(lang);
  const word = { running: s.stepWordOn, partial: s.stepWordPartly, off: s.stepWordOff }[surface.state];
  const on = inst.components.filter((c) => surface.parts.includes(c.name) && !isStopped(c)).length;
  return (
    <>
      {surface.apps && <span className="ins-surface-apps"><bdi>{surface.apps.join(" + ")}</bdi></span>}
      <span className={`ins-step-status ${TONE[surface.state]}`}><strong>{word}</strong></span>
      {!compact && <span className="muted">{s.factPartsOn}: <Tpl plain text={s.partsOn} values={{ on, total: surface.parts.length }} /></span>}
      {!compact && surface.releases.map((r) => <code key={r} dir="ltr">{r}</code>)}
    </>
  );
}

/** The sides of a project: admin panel, phone call and chatbot, and which of them it does not have. */
export function Surfaces({ inst, lang, compact = false }: { inst: Instance; lang: Lang; compact?: boolean }) {
  if (!inst.surfaces.length) return null;
  const s = T(lang);
  const label: Record<SurfaceKind, string> = { panel: s.surfacePanel, phone: s.surfacePhone, chatbot: s.surfaceChatbot };
  const of = (kind: "phone" | "panel") => inst.links.filter((l) => l.kind === kind);
  const rows = (Object.keys(label) as SurfaceKind[]).map((kind) => {
    const surface = inst.surfaces.find((x) => x.kind === kind);
    const shared = kind === "panel" ? of("panel") : [];
    return (
      <div key={kind} className="ins-surface">
        <span className="ins-surface-kind">{label[kind]}</span>
        <span className="ins-surface-value">
          {surface ? <Own inst={inst} surface={surface} lang={lang} compact={compact} />
            : shared.length ? <>{s.sharedPanel} {shared.map((l) => <InstanceLink key={l.id} id={l.id} lang={lang} />)}</>
            : <span className="muted">{s.surfaceNone}</span>}
          {kind === "panel" && !compact && of("phone").length > 0 && (
            <span className="muted">{s.alsoReads}: {of("phone").map((l) => <InstanceLink key={l.id} id={l.id} lang={lang} />)}</span>
          )}
        </span>
      </div>
    );
  });
  if (compact) return <div className="ins-surfaces compact">{rows}</div>;
  return (
    <section className="ins-surfaces">
      <h2 className="ins-h">{s.surfaces}</h2>
      {rows}
    </section>
  );
}
