import manifest from "../../data/docs.json";

/** One file under public/docs (path is relative to the app, e.g. "docs/technical/X.pdf"). */
export interface DocFile { path: string; type: string; size: number }

/** One library entry; HTML/PDF (or md/html, csv/docx) twins share an entry. */
export interface DocEntry {
  id: string;
  category: string;
  folder: string;
  title: string;
  lang: "en" | "fa";
  start: boolean;
  desc: { en: string; fa: string };
  files: DocFile[];
}

export const DOCS = (manifest as { categories: string[]; docs: DocEntry[] }).docs;
export const CATEGORIES = (manifest as { categories: string[] }).categories;

/** Types the side panel can show without leaving the app. */
export const PREVIEWABLE = new Set(["html", "pdf", "png", "jpg", "jpeg", "svg", "csv", "md", "json"]);

/** The file to preview first: the first previewable one (the manifest lists html before pdf, md, csv …). */
export const previewFile = (e: DocEntry) => e.files.find((f) => PREVIEWABLE.has(f.type));

/** URL of a file relative to the app; encodes spaces and other unsafe characters. */
export const fileUrl = (f: DocFile) => encodeURI(f.path);

export const fileName = (f: DocFile) => f.path.split("/").pop() ?? f.path;

export function fmtSize(bytes: number, lang: "en" | "fa"): string {
  const loc = lang === "fa" ? "fa-IR" : "en-US";
  const [n, u] = bytes >= 1048576 ? [bytes / 1048576, "MB"] : [bytes / 1024, "KB"];
  return `${n.toLocaleString(loc, { maximumFractionDigits: n < 10 ? 1 : 0 })} ${u}`;
}
