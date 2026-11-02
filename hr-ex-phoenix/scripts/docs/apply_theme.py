#!/usr/bin/env python3
"""Inline the shared design system (theme/phoenix_fa.css + .js) into every HTML source.

Idempotent: the theme lives between marker comments and is replaced on each run, so
edit theme/ and re-run (build.sh does this first). Any other <style> inside <head>
is a legacy per-file stylesheet and is removed on the first run.
"""

from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS = (HERE / "theme" / "phoenix_fa.css").read_text(encoding="utf-8")
JS = (HERE / "theme" / "phoenix_fa.js").read_text(encoding="utf-8")
FILES = [
    "product_dossier_fa.html",
    "technical_dossier_fa.html",
    "roadmap_fa.html",
    "answer_pack_fa.html",
    "fit_gap_tracker_fa.html",
    "inspiration_playbook_fa.html",
    "market_alignment_fa.html",
    "ai_learning_guide_fa.html",
    "iva_ex_prompt_requirements_fa.html",
    "feature_catalog.html",
    "feature_catalog_fa.html",
]

HEAD_START, HEAD_END = "<!-- theme:head:start -->", "<!-- theme:head:end -->"
BODY_START, BODY_END = "<!-- theme:script:start -->", "<!-- theme:script:end -->"

HEAD_BLOCK = f"""{HEAD_START}
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <meta name="color-scheme" content="dark light" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Vazirmatn:wght@400;500;700;800&display=swap" />
    <style>
{CSS}
    </style>
    {HEAD_END}"""

BODY_BLOCK = f"""{BODY_START}
    <script>
{JS}
    </script>
    {BODY_END}"""


def theme(html: str) -> str:
    head_end = html.index("</head>")
    head, rest = html[:head_end], html[head_end:]
    # drop a previous theme block, then any legacy head-level styles / viewport metas
    head = re.sub(re.escape(HEAD_START) + r".*?" + re.escape(HEAD_END), "", head, flags=re.S)
    head = re.sub(r"\s*<style>.*?</style>", "", head, flags=re.S)
    head = re.sub(r'\s*<meta name="(viewport|color-scheme)"[^>]*>', "", head)
    head = re.sub(r'\s*<link rel="(preconnect|stylesheet)"[^>]*>', "", head)
    html = head.rstrip() + "\n    " + HEAD_BLOCK + "\n  " + rest

    html = re.sub(r"\s*" + re.escape(BODY_START) + r".*?" + re.escape(BODY_END), "", html, flags=re.S)
    body_end = html.rindex("</body>")
    return html[:body_end].rstrip() + "\n    " + BODY_BLOCK + "\n  " + html[body_end:]


def main() -> None:
    for name in FILES:
        path = HERE / name
        before = path.read_text(encoding="utf-8")
        if not before.strip():
            raise SystemExit(f"{name} is empty — refusing to theme it (restore it first)")
        after = theme(before)
        path.write_text(after, encoding="utf-8")
        print(f"themed {name}: {len(before):,} -> {len(after):,} bytes")


if __name__ == "__main__":
    main()
