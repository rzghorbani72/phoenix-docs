#!/usr/bin/env python3
"""Export the pipeline content (content_en / content_fa DATA) as JSON for the React app.

Tuples that hold several section bodies become {"multi": [...]} so the app can tell them
apart from bullet lists. Output: ../src/data/{en,fa}.json, plus the documents manifest
../src/data/docs.json (build_docs_manifest.py).
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "src" / "data"
sys.path.insert(0, str(HERE))


def body(b):
    if isinstance(b, tuple):
        return {"multi": [body(x) for x in b]}
    return b


def sections(secs):
    return [[h, body(b)] for h, b in secs]


def step(s):
    s = dict(s)
    s["sections"] = sections(s.get("sections", []))
    s["facts"] = [list(f) for f in s.get("facts", [])]
    return s


def export(lang):
    d = importlib.import_module(f"content_{lang}").DATA
    models = dict(d["models"])
    models["sections"] = sections(models.get("sections", []))
    models["pages"] = {k: step(v) for k, v in models.get("pages", {}).items()}
    out = {
        "lang": d["lang"], "dir": d["dir"], "ui": d["ui"], "meta": d["meta"],
        "lanes": d["lanes"], "system_edges": d["system_edges"],
        "key_points": [body(k) for k in d.get("key_points", [])],
        "steps": {k: step(v) for k, v in d["steps"].items()},
        "models": models, "risks": d["risks"],
    }
    if d.get("guide"):
        out["guide"] = dict(d["guide"], sections=sections(d["guide"]["sections"]))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{lang}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{lang}: {len(out['steps'])} steps, {len(models['pages'])} model pages, guide={'guide' in out}")


if __name__ == "__main__":
    for lang in sys.argv[1:] or ["en", "fa"]:
        export(lang)
    import build_docs_manifest  # documents library manifest -> src/data/docs.json

    build_docs_manifest.main()
