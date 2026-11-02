#!/usr/bin/env python3
"""Render the feature catalog Markdown to themed HTML, in English and Persian.

FEATURE_CATALOG.md (English, LTR) and FEATURE_CATALOG_FA.md (Persian, RTL) stay the sources
of truth: edit the Markdown, then run ./build.sh, which renders this file, themes it with
apply_theme.py and publishes FEATURE_CATALOG.html and FEATURE_CATALOG_FA.html.
Only the Markdown the catalog uses is supported: headings, pipe tables, ordered and
unordered lists (nested by indentation), paragraphs, rules, **bold**, *italic*, `code`
and [links](url). A heading may end in {#id} to set its anchor (the Persian file uses this so
its ids match the English ones); otherwise the id follows GitHub's slug rule.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PM = HERE.parent / "product-management"
DOCS = [
    {
        "src": PM / "FEATURE_CATALOG.md",
        "out": HERE / "feature_catalog.html",
        "lang": "en",
        "dir": "ltr",
        "title": "Phoenix EX Feature Catalog",
        "note": 'Generated from <code>product-management/FEATURE_CATALOG.md</code>. Edit the Markdown, then run <code>source/build.sh</code>.',
    },
    {
        "src": PM / "FEATURE_CATALOG_FA.md",
        "out": HERE / "feature_catalog_fa.html",
        "lang": "fa",
        "dir": "rtl",
        "title": "کاتالوگ قابلیت‌های Phoenix EX",
        "note": 'تولیدشده از <code>product-management/FEATURE_CATALOG_FA.md</code>. فایل Markdown را ویرایش کنید، سپس <code>source/build.sh</code> را اجرا کنید.',
    },
]

THEME_HEAD = "<!-- theme:head:start --><!-- theme:head:end -->"
THEME_SCRIPT = "<!-- theme:script:start --><!-- theme:script:end -->"


def slug(text: str) -> str:
    """GitHub-style anchor: lower case, drop punctuation, spaces to hyphens."""
    text = re.sub(r"[*`]", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def inline(text: str) -> str:
    codes: list[str] = []

    def keep_code(m: re.Match[str]) -> str:
        codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>',
        text,
    )
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def cells(row: str) -> list[str]:
    row = row.strip().strip("|")
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", row)]


def table(rows: list[str]) -> str:
    head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
    out = ["<table>", "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>", "<tbody>"]
    out += ["<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body]
    out.append("</tbody></table>")
    return "\n".join(out)


LIST_ITEM = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def lists(rows: list[str]) -> str:
    out: list[str] = []
    stack: list[tuple[int, str]] = []  # (indent, tag)
    for row in rows:
        m = LIST_ITEM.match(row)
        if not m:  # continuation line of the previous item
            out[-1] = out[-1][: -len("</li>")] + " " + inline(row.strip()) + "</li>"
            continue
        indent, tag = len(m.group(1)), "ol" if m.group(2)[0].isdigit() else "ul"
        while stack and stack[-1][0] > indent:
            closed = stack.pop()[1]
            out.append(f"</{closed.removesuffix('-nested')}>" + ("</li>" if closed.endswith("-nested") else ""))
        if not stack or stack[-1][0] < indent:
            if stack and out and out[-1].endswith("</li>"):
                out[-1] = out[-1][: -len("</li>")]  # nest inside the open item
                stack.append((indent, tag + "-nested"))
            else:
                stack.append((indent, tag))
            out.append(f"<{tag}>")
        out.append(f"<li>{inline(m.group(3))}</li>")
    while stack:
        indent, tag = stack.pop()
        out.append(f"</{tag.removesuffix('-nested')}>" + ("</li>" if tag.endswith("-nested") else ""))
    return "\n".join(out)


def render(md: str) -> tuple[str, str]:
    lines = md.split("\n")
    title, intro, blocks = "", [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
        elif s.startswith("#"):
            level = len(s) - len(s.lstrip("#"))
            text = s[level:].strip()
            explicit = re.search(r"\s*\{#([^}]+)\}$", text)
            if explicit:
                text = text[: explicit.start()].strip()
            if level == 1:
                title = text
            else:
                hid = explicit.group(1) if explicit else ("toc" if text.lower() == "contents" else slug(text))
                blocks.append(f'<h{level} id="{hid}">{inline(text)}</h{level}>')
            i += 1
        elif s == "---":
            i += 1
        elif s.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            p = f'<p class="box">{inline(" ".join(quote))}</p>'
            (blocks if blocks else intro).append(p)
        elif s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            blocks.append(table(rows))
        elif LIST_ITEM.match(line):
            rows = []
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(("#", "|")):
                rows.append(lines[i])
                i += 1
            blocks.append(lists(rows))
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"\s*(#|\||>|---$)", lines[i]) and not LIST_ITEM.match(lines[i]):
                para.append(lines[i].strip())
                i += 1
            p = f"<p>{inline(' '.join(para))}</p>"
            # paragraphs before the first heading form the cover, like the other docs
            (blocks if blocks else intro).append(p)
    return title, "\n".join(intro), "\n".join(blocks)


def build(doc: dict) -> None:
    title, intro, body = render(doc["src"].read_text(encoding="utf-8"))
    page = f"""<!doctype html>
<html lang="{doc["lang"]}" dir="{doc["dir"]}">
  <head>
    <meta charset="utf-8" />
    <title>{doc["title"]}</title>
    {THEME_HEAD}
  </head>
  <body>
    <div class="cover">
      <h1>{inline(title)}</h1>
      {intro}
      <p class="small">{doc["note"]}</p>
    </div>
{body}
    {THEME_SCRIPT}
  </body>
</html>
"""
    doc["out"].write_text(page, encoding="utf-8")
    print(f"rendered {doc['src'].name} -> {doc['out'].name}: {len(page):,} bytes")


def main() -> None:
    for doc in DOCS:
        build(doc)


if __name__ == "__main__":
    main()
