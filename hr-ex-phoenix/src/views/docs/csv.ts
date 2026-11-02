/**
 * Minimal RFC 4180 CSV parser: quoted fields, "" escapes, commas and newlines inside quotes, CRLF.
 * Stops after `maxRows` rows. With `partial` (the text is the head of a bigger file) the last,
 * possibly cut-off row is dropped.
 */
export function parseCsv(text: string, maxRows = Infinity, partial = false): { rows: string[][]; truncated: boolean } {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let quoted = false;
  let i = text.charCodeAt(0) === 0xfeff ? 1 : 0;
  for (; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; } else quoted = false;
      } else field += c;
      continue;
    }
    if (c === '"') quoted = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); field = "";
      rows.push(row); row = [];
      if (rows.length >= maxRows) return { rows, truncated: partial || i < text.length - 1 };
    } else field += c;
  }
  if (partial) return { rows, truncated: true };
  if (field !== "" || row.length) { row.push(field); rows.push(row); }
  return { rows, truncated: false };
}

/** Read at most `limit` bytes of a URL as UTF-8 text (big CSVs only need their first rows). */
export async function fetchHead(url: string, limit: number, signal?: AbortSignal): Promise<{ text: string; partial: boolean }> {
  const res = await fetch(url, { signal });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  if (!res.body) return { text: await res.text(), partial: false };
  const reader = res.body.getReader();
  const dec = new TextDecoder("utf-8");
  let text = "";
  let read = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) return { text: text + dec.decode(), partial: false };
    read += value.byteLength;
    text += dec.decode(value, { stream: true });
    if (read >= limit) { void reader.cancel(); return { text, partial: true }; }
  }
}
