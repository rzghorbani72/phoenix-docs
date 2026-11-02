import type { Data } from "../lib/types";

/** Library of the project documents served from public/docs (placeholder until the Documents view is built). */
export function DocsView({ d }: { d: Data }) {
  return <div className="page"><h1>{d.lang === "fa" ? "اسناد" : "Documents"}</h1></div>;
}
