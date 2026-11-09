// @ts-expect-error The project does not install Node's types; this file runs only under vitest.
import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const SNAPSHOT = "content/instances_snapshot.json";

const UNSAFE_TEXT: Record<string, RegExp> = {
  url: /[a-z][a-z0-9+.-]*:\/\/\S/i,
  "IP address": /\b\d{1,3}(?:\.\d{1,3}){3}\b/,
  "internal host": /\.mci\.dev\b|\.svc\b/i,
  "JWT or key blob": /\beyJ[A-Za-z0-9_-]{10,}|-----BEGIN [A-Z ]*KEY-----/,
  "provider token": /\b(?:sk|pk|rk)[-_][A-Za-z0-9_-]{16,}|\b(?:ghp|gho|glpat|xox[abp])[-_][A-Za-z0-9_-]{10,}/,
  "bearer token": /\bbearer\s+[A-Za-z0-9._-]{8,}/i,
  "long token": /\b[A-Fa-f0-9]{32,}\b|\b[A-Za-z0-9+/_-]{40,}={0,2}(?![A-Za-z0-9+/_-])/,
};

const SECRET_KEY = /secret|passw|pwd|token|api[_-]?key|access[_-]?key|private[_-]?key|credential|\bdsn\b|auth/i;

function allKeys(value: unknown, out: string[] = []): string[] {
  if (Array.isArray(value)) value.forEach((v) => allKeys(v, out));
  else if (value && typeof value === "object")
    for (const [k, v] of Object.entries(value)) {
      out.push(k);
      allKeys(v, out);
    }
  return out;
}

const unsafeIn = (text: string) =>
  Object.entries(UNSAFE_TEXT)
    .filter(([, re]) => re.test(text))
    .map(([label]) => label);

describe("ops snapshot stays free of connection details and secrets", () => {
  const text: string = readFileSync(SNAPSHOT, "utf8");

  it("holds no URLs, IPs, internal hosts or tokens", () => {
    expect(unsafeIn(text)).toEqual([]);
  });

  it("holds no secret-named keys", () => {
    expect(allKeys(JSON.parse(text)).filter((k) => SECRET_KEY.test(k))).toEqual([]);
  });

  it("the guards do catch what they claim to", () => {
    const planted: [string, string][] = [
      ["https://example.org/x", "url"],
      ["redis://cache:6379", "url"],
      ["10.0.12.7", "IP address"],
      ["kafka.mci.dev", "internal host"],
      ["eyJhbGciOiJIUzI1NiJ9.e30.abc", "JWT or key blob"],
      ["sk-abcdefghijklmnopqrstuv", "provider token"],
      ["Bearer abc123def456", "bearer token"],
      ["0123456789abcdef0123456789abcdef", "long token"],
    ];
    for (const [sample, label] of planted) expect(unsafeIn(sample)).toContain(label);
    expect(allKeys({ a: [{ MINIO_SECRET_KEY: "x" }] }).filter((k) => SECRET_KEY.test(k))).toHaveLength(1);
  });
});
