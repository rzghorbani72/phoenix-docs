#!/usr/bin/env python3
"""Build the Phoenix EX pipeline map: an index page with a clickable pipeline diagram,
one deep-dive page per step, a model inventory page and a risks page, in English and
Persian, plus an editable .drawio copy of the map whose boxes link to the step pages.

Content lives in content_en.py / content_fa.py (same keys). This file is layout only.
Output: ../../technical/phoenix-pipelines/{en,fa}/ and phoenix-pipelines.drawio
"""

from __future__ import annotations

import html
import importlib
import re
import shutil
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "technical" / "phoenix-pipelines"
sys.path.insert(0, str(HERE))

LANE_COLORS = {  # css var name per lane colour key
    "teal": "--c-teal", "violet": "--c-violet", "orange": "--c-orange",
    "pink": "--c-pink", "cyan": "--c-cyan", "blue": "--accent", "green": "--ok",
}
DRAWIO_FILL = {"teal": "#d5f5ef", "violet": "#ebe3fc", "orange": "#fdebd7",
               "pink": "#fbe3ef", "cyan": "#d9f6fb", "blue": "#dfe9fb", "green": "#dff3e1"}
DRAWIO_LINE = {"teal": "#0f9e87", "violet": "#7b54d6", "orange": "#d97a1c",
               "pink": "#cf4f8f", "cyan": "#1597ad", "blue": "#3c6fc4", "green": "#3d9a47"}


# ---------------------------------------------------------------- inline markup
def md(text: str) -> str:
    """Tiny inline markup: `code`, **bold**, [label](url), (inferred) highlight."""
    out = html.escape(str(text), quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', out)
    out = re.sub(r"\((inferred|استنباط|استنباطی)\)", r'<span class="inf">(\1)</span>', out)
    return out


def block(body) -> str:
    """A section body: str = paragraph(s), list = bullets, dict = table/ol/code/note."""
    if isinstance(body, str):
        return "".join(f"<p>{md(p)}</p>" for p in body.split("\n\n"))
    if isinstance(body, list):
        return "<ul>" + "".join(f"<li>{md(i)}</li>" for i in body) + "</ul>"
    if "table" in body:
        rows = body["table"]
        head = "".join(f"<th>{md(c)}</th>" for c in rows[0])
        trs = "".join("<tr>" + "".join(f"<td>{md(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
        return f'<div class="tw"><table><thead><tr>{head}</tr></thead><tbody>{trs}</tbody></table></div>'
    if "ol" in body:
        return "<ol>" + "".join(f"<li>{md(i)}</li>" for i in body["ol"]) + "</ol>"
    if "code" in body:
        return f'<pre><code>{html.escape(body["code"])}</code></pre>'
    if "note" in body:
        return f'<div class="note {body.get("kind", "")}">{md(body["note"])}</div>'
    raise ValueError(body)


# ---------------------------------------------------------------- page shell
CSS = r"""
:root{--bg:#0f141a;--surface:#161d26;--surface-2:#1d2631;--ink:#e4e9ef;--muted:#9aa6b4;--line:#2c3744;
--accent:#8fb4ef;--ok:#84d48c;--ok-bg:#15301a;--warn:#f1c45c;--warn-bg:#34290b;--bad:#ff9289;--bad-bg:#3a1714;
--gap:#c9cdd3;--gap-bg:#2a3039;--info:#8fbfff;--info-bg:#142a47;--code-bg:#1b2430;
--c-violet:#b79cf5;--c-teal:#5eead4;--c-pink:#f9a8d4;--c-orange:#fdba74;--c-cyan:#67e8f9;
--f-body:"Vazirmatn","Noto Sans Arabic",system-ui,sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,monospace;--col:1240px}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#f4f6f8;--surface:#fff;--surface-2:#eef2f6;
--ink:#17202b;--muted:#5b6776;--line:#d6dde5;--accent:#2f62b8;--ok:#237a2e;--ok-bg:#e3f4e5;--warn:#8a6100;--warn-bg:#fbf0d2;
--bad:#b3261e;--bad-bg:#fbe4e2;--gap:#4b5563;--gap-bg:#eceff3;--info:#1d5fb8;--info-bg:#e2edfb;--code-bg:#eef2f6;
--c-violet:#6d44c9;--c-teal:#0b8a76;--c-pink:#b8377a;--c-orange:#b55d0c;--c-cyan:#0e7f93}}
:root[data-theme="light"]{--bg:#f4f6f8;--surface:#fff;--surface-2:#eef2f6;--ink:#17202b;--muted:#5b6776;--line:#d6dde5;
--accent:#2f62b8;--ok:#237a2e;--ok-bg:#e3f4e5;--warn:#8a6100;--warn-bg:#fbf0d2;--bad:#b3261e;--bad-bg:#fbe4e2;--gap:#4b5563;
--gap-bg:#eceff3;--info:#1d5fb8;--info-bg:#e2edfb;--code-bg:#eef2f6;--c-violet:#6d44c9;--c-teal:#0b8a76;--c-pink:#b8377a;
--c-orange:#b55d0c;--c-cyan:#0e7f93}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:15.5px/1.75 var(--f-body)}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
code{font-family:var(--f-mono);font-size:.86em;background:var(--code-bg);padding:.08em .35em;border-radius:5px;overflow-wrap:anywhere;direction:ltr;unicode-bidi:isolate}
pre{background:var(--code-bg);padding:12px 14px;border-radius:10px;overflow:auto;direction:ltr;text-align:left}pre code{background:none;padding:0}
.wrap{max-width:var(--col);margin:0 auto;padding:0 16px}
header.top{border-bottom:1px solid var(--line);background:var(--surface);position:sticky;top:0;z-index:5}
header.top .wrap{display:flex;gap:14px;align-items:center;min-height:52px;flex-wrap:wrap}
header.top .brand{font-weight:800;color:var(--ink)}header.top nav{display:flex;gap:14px;flex-wrap:wrap;margin-inline-start:auto;font-size:.92em}
header.top button{background:var(--surface-2);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:2px 10px;font:inherit;cursor:pointer}
h1{font-size:1.9em;line-height:1.3;margin:28px 0 6px}h2{font-size:1.3em;margin:34px 0 10px;padding-top:6px}h3{font-size:1.08em;margin:22px 0 6px}
.lede{color:var(--muted);max-width:860px;margin:0 0 10px}
.meta{color:var(--muted);font-size:.85em}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:.85em;color:var(--muted);margin:14px 0}
.badge{display:inline-flex;align-items:center;gap:6px;font-size:.78em;font-weight:600;padding:1px 9px;border-radius:999px;white-space:nowrap}
.badge::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.s-live{color:var(--ok);background:var(--ok-bg)}.s-off{color:var(--gap);background:var(--gap-bg)}
.s-notdeployed{color:var(--bad);background:var(--bad-bg)}.s-external{color:var(--warn);background:var(--warn-bg)}
.s-unknown{color:var(--info);background:var(--info-bg)}
/* system overview */
.sys{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px;margin:16px 0;overflow-x:auto}
.sys svg{width:100%;min-width:760px;height:auto;display:block}
.sys a text{fill:var(--ink)}.sys .sub{fill:var(--muted)}.sys .edge{stroke:var(--muted);fill:none;stroke-width:1.6}
.sys .elab{fill:var(--muted);font-size:12px}.sys a:hover rect{filter:brightness(1.25)}
/* lanes */
.lane{border:1px solid var(--line);border-radius:14px;margin:22px 0;background:var(--surface);overflow:hidden}
.lane>.lh{padding:12px 16px;border-bottom:1px solid var(--line);border-inline-start:6px solid var(--lc)}
.lane>.lh h2{margin:0;padding:0;font-size:1.15em}.lane>.lh p{margin:2px 0 0;color:var(--muted);font-size:.9em}
.flow{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px 30px;padding:16px;padding-inline-end:36px}
.card{position:relative;min-height:118px;background:var(--surface-2);border:1px solid var(--line);
border-top:3px solid var(--lc);border-radius:10px;padding:10px 12px;color:var(--ink);display:flex;flex-direction:column;gap:4px}
.card:hover{text-decoration:none;border-color:var(--lc);transform:translateY(-1px)}
.card .n{font-family:var(--f-mono);font-size:.75em;color:var(--lc)}
.card .t{font-weight:700;line-height:1.35}.card .m{font-size:.8em;color:var(--muted);line-height:1.4}
.card .b{margin-top:auto}
.card:not(:last-child)::after{content:"→";position:absolute;inset-inline-end:-22px;top:42%;color:var(--muted);font-size:1.1em}
[dir=rtl] .card:not(:last-child)::after{content:"←"}
.handoff{padding:0 16px 14px;color:var(--muted);font-size:.85em}
/* step page */
.crumbs{font-size:.85em;color:var(--muted);margin-top:18px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin:16px 0}
.fact{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:8px 12px}
.fact .k{font-size:.75em;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}.fact .v{font-weight:600;overflow-wrap:anywhere}
.sec{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:4px 18px 10px;margin:14px 0}
.sec h2{font-size:1.08em;margin:14px 0 6px}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:.9em;margin:6px 0}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:start;vertical-align:top}th{color:var(--muted);font-weight:600}
.note{border-inline-start:4px solid var(--info);background:var(--info-bg);padding:8px 12px;border-radius:8px;margin:8px 0}
.note.warn{border-color:var(--warn);background:var(--warn-bg)}.note.bad{border-color:var(--bad);background:var(--bad-bg)}
.inf{color:var(--warn);font-style:italic;font-size:.9em}
.pn{display:flex;justify-content:space-between;gap:12px;margin:26px 0 40px;flex-wrap:wrap}
.pn a{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:8px 14px;max-width:48%}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.mcard{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px}
.mcard h3{margin:0 0 4px}.mcard .size{font-family:var(--f-mono);color:var(--accent);font-size:.9em}
.sev{font-weight:700;font-size:.8em;padding:1px 8px;border-radius:6px}.sev-high{color:var(--bad);background:var(--bad-bg)}
.sev-med{color:var(--warn);background:var(--warn-bg)}.sev-low{color:var(--gap);background:var(--gap-bg)}
footer{color:var(--muted);font-size:.82em;border-top:1px solid var(--line);margin-top:40px;padding:16px 0 30px}
@media (max-width:640px){.flow{grid-template-columns:1fr;gap:30px;padding-inline-end:16px}.card:not(:last-child)::after{content:"↓";inset-inline-end:auto;inset-inline-start:50%;top:auto;bottom:-22px}
h1{font-size:1.5em}.pn a{max-width:100%}}
"""

JS = """
(function(){var k='pp-theme',r=document.documentElement;try{var t=localStorage.getItem(k);if(t)r.dataset.theme=t}catch(e){}
document.addEventListener('click',function(e){if(e.target.id!=='themeBtn')return;
var d=r.dataset.theme||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');
r.dataset.theme=d==='light'?'dark':'light';try{localStorage.setItem(k,r.dataset.theme)}catch(e){}});})();
"""


def page(d, title, body, depth=0, other=None):
    up = "../" * depth
    ui = d["ui"]
    other_link = f'<a href="{other}">{ui["other_lang"]}</a>' if other else ""
    guide_link = f'<a href="{up}guide.html">{ui.get("nav_guide", "Guide")}</a>' if d.get("guide") else ""
    return f"""<!doctype html>
<html lang="{d['lang']}" dir="{d['dir']}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark light"><title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Vazirmatn:wght@400;600;800&display=swap">
<style>{CSS}</style><script>{JS}</script></head>
<body><header class="top"><div class="wrap"><a class="brand" href="{up}index.html">{ui['brand']}</a>
<nav><a href="{up}index.html">{ui['nav_map']}</a><a href="{up}models.html">{ui['nav_models']}</a>
<a href="{up}risks.html">{ui['nav_risks']}</a>{guide_link}{other_link}<button id="themeBtn" type="button">◐</button></nav></div></header>
<main class="wrap">{body}</main>
<footer class="wrap">{md(d['meta']['footer'])}</footer></body></html>"""


def badge(d, status):
    return f'<span class="badge s-{status}">{d["ui"]["status"][status]}</span>'


# ---------------------------------------------------------------- system overview svg
def system_svg(d):
    """Six lane blocks in a 3x2 grid plus labelled hand-off arrows; each block jumps to its lane.
    Lanes marked "band" (e.g. the framework everything runs on) are drawn as a full-width foundation bar below."""
    lanes = {l["id"]: l for l in d["lanes"]}
    blocks = [l for l in d["lanes"] if not l.get("band")][:6]
    bands = [l for l in d["lanes"] if l.get("band")]
    W, bw, bh, band_h = 1180, 300, 104, 64
    xs, ys = [20, 440, 860], [24, 202]
    H = 330 + len(bands) * (band_h + 30)
    pos = {}
    for i, l in enumerate(blocks):
        pos[l["id"]] = (xs[i % 3], ys[i // 3])
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(d["ui"]["sys_title"])}">',
             '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M0,0 L10,5 L0,10 z" fill="var(--muted)"/></marker></defs>']
    for e in d["system_edges"]:
        a, b, lab = e["from"], e["to"], e["label"]
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if y1 == y2:  # same row: right edge -> left edge
            if x1 < x2:
                sx, sy, tx, ty = x1 + bw, y1 + bh / 2 + e.get("dy", 0), x2, y2 + bh / 2 + e.get("dy", 0)
            else:
                sx, sy, tx, ty = x1, y1 + bh / 2 + e.get("dy", 0), x2 + bw, y2 + bh / 2 + e.get("dy", 0)
            path = f"M{sx},{sy} L{tx},{ty}"
            lx, ly = (sx + tx) / 2, sy - 7
        else:  # vertical between rows
            cx1, cx2 = x1 + bw / 2 + e.get("dx", 0), x2 + bw / 2 + e.get("dx", 0)
            sy, ty = (y1 + bh, y2) if y1 < y2 else (y1, y2 + bh)
            mid = (sy + ty) / 2
            path = f"M{cx1},{sy} C{cx1},{mid} {cx2},{mid} {cx2},{ty}"
            lx, ly = (cx1 + cx2) / 2 + 8, mid + 4
        parts.append(f'<path class="edge" d="{path}" marker-end="url(#ar)"/>')
        anchor = "middle" if y1 == y2 else "start"
        parts.append(f'<text class="elab" x="{lx}" y="{ly}" text-anchor="{anchor}">{html.escape(lab)}</text>')
    for lid, (x, y) in pos.items():
        l = lanes[lid]
        col = f"var({LANE_COLORS[l['color']]})"
        n = len(l["steps"])
        parts.append(f'<a href="#lane-{lid}"><rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="12" fill="var(--surface-2)" stroke="{col}" stroke-width="2"/>'
                     f'<rect x="{x}" y="{y}" width="8" height="{bh}" rx="3" fill="{col}"/>'
                     f'<text x="{x + bw / 2}" y="{y + 40}" text-anchor="middle" font-weight="800" font-size="18">{html.escape(l["short"])}</text>'
                     f'<text class="sub" x="{x + bw / 2}" y="{y + 66}" text-anchor="middle" font-size="13">{html.escape(l["tagline"])}</text>'
                     f'<text class="sub" x="{x + bw / 2}" y="{y + 88}" text-anchor="middle" font-size="12">{n} {html.escape(d["ui"]["steps_word"])}</text></a>')
    for j, l in enumerate(bands):
        y = 336 + j * (band_h + 30)
        col = f"var({LANE_COLORS[l['color']]})"
        text = f'{l["short"]} · {l["tagline"]} · {len(l["steps"])} {d["ui"]["steps_word"]}'
        parts.append(f'<a href="#lane-{l["id"]}"><rect x="20" y="{y}" width="{W - 40}" height="{band_h}" rx="12" fill="var(--surface-2)" '
                     f'stroke="{col}" stroke-width="2" stroke-dasharray="6 4"/>'
                     f'<text x="{W / 2}" y="{y + band_h / 2 + 6}" text-anchor="middle" font-weight="700" font-size="16">{html.escape(text)}</text></a>')
    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------- pages
def build_index(d, other):
    ui, out = d["ui"], []
    out.append(f'<h1>{md(d["meta"]["title"])}</h1><p class="lede">{md(d["meta"]["lede"])}</p>')
    out.append(f'<p class="meta">{md(d["meta"]["source"])}</p>')
    out.append('<div class="legend">' + "".join(badge(d, s) for s in ui["status"]) + f'<span>{md(ui["legend_hint"])}</span></div>')
    out.append(f'<h2>{ui["sys_title"]}</h2><div class="sys">{system_svg(d)}</div>')
    for kp in d.get("key_points", []):
        out.append(block(kp))
    num = 0
    for l in d["lanes"]:
        col = f"var({LANE_COLORS[l['color']]})"
        cards = []
        for sid in l["steps"]:
            num += 1
            s = d["steps"][sid]
            cards.append(f'<a class="card" href="steps/{sid}.html"><span class="n">{l["prefix"]}{l["steps"].index(sid) + 1}</span>'
                         f'<span class="t">{md(s["title"])}</span><span class="m">{md(s.get("chip", ""))}</span>'
                         f'<span class="b">{badge(d, s["status"])}</span></a>')
        hand = f'<div class="handoff">{md(l["handoff"])}</div>' if l.get("handoff") else ""
        out.append(f'<section class="lane" id="lane-{l["id"]}" style="--lc:{col}"><div class="lh"><h2>{md(l["title"])}</h2>'
                   f'<p>{md(l["desc"])}</p></div><div class="flow">{"".join(cards)}</div>{hand}</section>')
    return page(d, d["meta"]["title_plain"], "".join(out), 0, other)


def build_step(d, l, sid, other):
    s, ui = d["steps"][sid], d["ui"]
    i = l["steps"].index(sid)
    col = f"var({LANE_COLORS[l['color']]})"
    out = [f'<div class="crumbs"><a href="../index.html#lane-{l["id"]}">{md(l["title"])}</a> · {l["prefix"]}{i + 1}</div>',
           f'<h1 style="border-inline-start:6px solid {col};padding-inline-start:12px">{md(s["title"])}</h1>',
           f'<p>{badge(d, s["status"])}</p><p class="lede">{md(s["summary"])}</p>']
    if s.get("facts"):
        out.append('<div class="facts">' + "".join(
            f'<div class="fact"><div class="k">{md(k)}</div><div class="v">{md(v)}</div></div>' for k, v in s["facts"]) + "</div>")
    for h, body in s.get("sections", []):
        bodies = body if isinstance(body, tuple) else (body,)
        out.append(f'<section class="sec"><h2>{md(h)}</h2>{"".join(block(b) for b in bodies)}</section>')
    prev_ = l["steps"][i - 1] if i > 0 else None
    next_ = l["steps"][i + 1] if i + 1 < len(l["steps"]) else None
    pn = '<div class="pn">'
    pn += f'<a href="{prev_}.html">{ui["prev"]} {md(d["steps"][prev_]["title"])}</a>' if prev_ else "<span></span>"
    pn += f'<a href="{next_}.html">{md(d["steps"][next_]["title"])} {ui["next"]}</a>' if next_ else f'<a href="../index.html#lane-{l["id"]}">{ui["back"]}</a>'
    out.append(pn + "</div>")
    return page(d, f'{s["title"]} · {d["ui"]["brand"]}', "".join(out), 1, other)


def build_models(d, other):
    out = [f'<h1>{md(d["models"]["title"])}</h1><p class="lede">{md(d["models"]["lede"])}</p>']
    out.append('<div class="grid">')
    pages = d["models"].get("pages", {})
    for m in d["models"]["cards"]:
        used = "".join(f'<li><a href="steps/{u}.html">{md(d["steps"][u]["title"])}</a></li>' for u in m.get("steps", []))
        name = f'<a href="models/{m["id"]}.html">{md(m["name"])}</a>' if m.get("id") in pages else md(m["name"])
        out.append(f'<div class="mcard"><h3>{name}</h3><div class="size">{md(m["size"])}</div>'
                   f'<p>{badge(d, m["status"])}</p>{block(m["facts"])}'
                   + (f'<p class="meta">{d["ui"]["used_in"]}</p><ul>{used}</ul>' if used else "") + "</div>")
    out.append("</div>")
    for h, body in d["models"].get("sections", []):
        bodies = body if isinstance(body, tuple) else (body,)
        out.append(f'<section class="sec"><h2>{md(h)}</h2>{"".join(block(b) for b in bodies)}</section>')
    return page(d, d["models"]["title"], "".join(out), 0, other)


def build_model_page(d, mid, other):
    """Deep-dive page for one model; same section format as a step page, ordered like the cards."""
    ui, m = d["ui"], d["models"]["pages"][mid]
    order = [c["id"] for c in d["models"]["cards"] if c.get("id") in d["models"]["pages"]]
    i = order.index(mid)
    card = next(c for c in d["models"]["cards"] if c.get("id") == mid)
    out = [f'<div class="crumbs"><a href="../models.html">{md(d["models"]["title"])}</a></div>',
           f'<h1 style="border-inline-start:6px solid var(--accent);padding-inline-start:12px">{md(m["title"])}</h1>',
           f'<p>{badge(d, m["status"])} <span class="size">{md(card["size"])}</span></p><p class="lede">{md(m["summary"])}</p>']
    if m.get("facts"):
        out.append('<div class="facts">' + "".join(
            f'<div class="fact"><div class="k">{md(k)}</div><div class="v">{md(v)}</div></div>' for k, v in m["facts"]) + "</div>")
    if card.get("steps"):
        out.append(f'<section class="sec"><h2>{ui["used_in"]}</h2><ul>' + "".join(
            f'<li><a href="../steps/{u}.html">{md(d["steps"][u]["title"])}</a></li>' for u in card["steps"]) + "</ul></section>")
    for h, body in m.get("sections", []):
        bodies = body if isinstance(body, tuple) else (body,)
        out.append(f'<section class="sec"><h2>{md(h)}</h2>{"".join(block(b) for b in bodies)}</section>')
    prev_ = order[i - 1] if i > 0 else None
    next_ = order[i + 1] if i + 1 < len(order) else None
    pages = d["models"]["pages"]
    pn = '<div class="pn">'
    pn += f'<a href="{prev_}.html">{ui["prev"]} {md(pages[prev_]["title"])}</a>' if prev_ else "<span></span>"
    pn += f'<a href="{next_}.html">{md(pages[next_]["title"])} {ui["next"]}</a>' if next_ else f'<a href="../models.html">{ui["back_models"] if "back_models" in ui else ui["back"]}</a>'
    out.append(pn + "</div>")
    return page(d, f'{m["title"]} · {ui["brand"]}', "".join(out), 1, other)


def build_guide(d, other):
    g = d["guide"]
    out = [f'<h1>{md(g["title"])}</h1><p class="lede">{md(g["lede"])}</p>']
    toc = "".join(f'<li><a href="#g{i}">{md(h)}</a></li>' for i, (h, _) in enumerate(g["sections"]))
    out.append(f'<section class="sec"><ol>{toc}</ol></section>')
    for i, (h, body) in enumerate(g["sections"]):
        bodies = body if isinstance(body, tuple) else (body,)
        out.append(f'<section class="sec" id="g{i}"><h2>{md(h)}</h2>{"".join(block(b) for b in bodies)}</section>')
    return page(d, g["title"], "".join(out), 0, other)


def build_risks(d, other):
    ui = d["ui"]
    out = [f'<h1>{md(d["risks"]["title"])}</h1><p class="lede">{md(d["risks"]["lede"])}</p>']
    rows = [[ui["col_sev"], ui["col_issue"], ui["col_why"], ui["col_where"]]]
    tbl = ['<div class="tw"><table><thead><tr>' + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr></thead><tbody>"]
    for r in d["risks"]["items"]:
        where = ", ".join(f'<a href="steps/{s}.html">{md(d["steps"][s]["title"])}</a>' for s in r.get("steps", []))
        tbl.append(f'<tr><td><span class="sev sev-{r["sev"]}">{ui["sev"][r["sev"]]}</span></td><td><strong>{md(r["title"])}</strong></td>'
                   f'<td>{md(r["why"])}</td><td>{where}</td></tr>')
    tbl.append("</tbody></table></div>")
    out.append("".join(tbl))
    return page(d, d["risks"]["title"], "".join(out), 0, other)


# ---------------------------------------------------------------- drawio
def build_drawio(d, base_href):
    """Swimlane per pipeline, one node per step linked to its page; layout is a simple grid."""
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    y, per_row, cw, ch, gx, gy = 20, 6, 190, 70, 30, 26
    for l in d["lanes"]:
        rows = (len(l["steps"]) + per_row - 1) // per_row
        lh = 44 + rows * (ch + gy) + 10
        lw = 30 + per_row * (cw + gx)
        fill, line = DRAWIO_FILL[l["color"]], DRAWIO_LINE[l["color"]]
        lane_id = f"lane_{l['id']}"
        cells.append(f'<mxCell id="{lane_id}" value={quoteattr(l["title_plain"])} style="swimlane;horizontal=1;startSize=34;fontStyle=1;fontSize=15;'
                     f'fillColor={fill};strokeColor={line};swimlaneFillColor=#ffffff;rounded=1;arcSize=4;" vertex="1" parent="1">'
                     f'<mxGeometry x="20" y="{y}" width="{lw}" height="{lh}" as="geometry"/></mxCell>')
        prev = None
        for i, sid in enumerate(l["steps"]):
            s = d["steps"][sid]
            r, c = divmod(i, per_row)
            x, yy = 20 + c * (cw + gx), 44 + r * (ch + gy)
            dashed = "dashed=1;" if s["status"] in ("off", "notdeployed", "unknown") else ""
            label = f'{l["prefix"]}{i + 1}. {s["title_plain"]}\n{s.get("chip_plain", "")}'
            nid = f"s_{sid}"
            cells.append(f'<UserObject id="{nid}" label={quoteattr(label)} link={quoteattr(base_href + sid + ".html")} status="{s["status"]}">'
                         f'<mxCell style="rounded=1;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor={line};strokeWidth=2;fontSize=12;{dashed}" vertex="1" parent="{lane_id}">'
                         f'<mxGeometry x="{x}" y="{yy}" width="{cw}" height="{ch}" as="geometry"/></mxCell></UserObject>')
            if prev:
                cells.append(f'<mxCell id="e_{prev}_{sid}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=block;strokeColor={line};" edge="1" parent="{lane_id}" source="s_{prev}" target="{nid}">'
                             '<mxGeometry relative="1" as="geometry"/></mxCell>')
            prev = sid
        y += lh + 30
    diagrams = [("ex", "EX pipelines", cells)]
    if d["models"].get("pages"):
        diagrams.append(("models", "Model catalog", model_cells(d, base_href.replace("steps/", "models/"))))
    head = ('<mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
            'fold="1" page="0" pageScale="1" math="0" shadow="0"><root>')
    return ('<mxfile host="phoenix-pipelines">' + "".join(
        f'<diagram id="{i}" name="{n}">{head}{"".join(c)}</root></mxGraphModel></diagram>' for i, n, c in diagrams) + "</mxfile>")


def model_cells(d, base_href):
    """One linked box per model page, in card order, coloured by status."""
    fill = {"live": "#dff3e1", "external": "#fbf0d2", "unknown": "#e2edfb", "off": "#eceff3", "notdeployed": "#fbe4e2"}
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    per_row, cw, ch, gx, gy = 5, 230, 84, 26, 26
    cards = [c for c in d["models"]["cards"] if c.get("id") in d["models"]["pages"]]
    for i, c in enumerate(cards):
        r, col = divmod(i, per_row)
        label = f'{d["models"]["pages"][c["id"]]["title_plain"]}\n{c["size"]}'
        label = re.sub(r"[`*]", "", label)
        cells.append(f'<UserObject id="m_{c["id"]}" label={quoteattr(label)} link={quoteattr(base_href + c["id"] + ".html")} status="{c["status"]}">'
                     f'<mxCell style="rounded=1;whiteSpace=wrap;html=0;fillColor={fill.get(c["status"], "#ffffff")};strokeColor=#3c6fc4;fontSize=12;" vertex="1" parent="1">'
                     f'<mxGeometry x="{20 + col * (cw + gx)}" y="{20 + r * (ch + gy)}" width="{cw}" height="{ch}" as="geometry"/></mxCell></UserObject>')
    return cells


# ---------------------------------------------------------------- main
def check(d):
    """Every lane step and every cross-reference must exist; fail loudly on content drift."""
    ids = set(d["steps"])
    laned = [s for l in d["lanes"] for s in l["steps"]]
    missing = [s for s in laned if s not in ids] + [s for s in ids if s not in laned]
    for m in d["models"]["cards"]:
        missing += [s for s in m.get("steps", []) if s not in ids]
    for r in d["risks"]["items"]:
        missing += [s for s in r.get("steps", []) if s not in ids]
    pages = d["models"].get("pages", {})
    if pages:
        card_ids = [c.get("id") for c in d["models"]["cards"]]
        missing += [f"model:{p}" for p in pages if p not in card_ids] + [f"model:{c}" for c in card_ids if c not in pages]
    if missing:
        raise SystemExit(f"{d['lang']}: unknown or orphan step ids: {sorted(set(missing))}")


def main():
    langs = [a for a in sys.argv[1:]] or ["en", "fa"]
    for lang in langs:
        d = importlib.import_module(f"content_{lang}").DATA
        check(d)
        other_lang = "fa" if lang == "en" else "en"
        dst = OUT / lang
        if dst.exists():
            shutil.rmtree(dst)
        (dst / "steps").mkdir(parents=True)
        (dst / "index.html").write_text(build_index(d, f"../{other_lang}/index.html"), encoding="utf-8")
        (dst / "models.html").write_text(build_models(d, f"../{other_lang}/models.html"), encoding="utf-8")
        (dst / "risks.html").write_text(build_risks(d, f"../{other_lang}/risks.html"), encoding="utf-8")
        for l in d["lanes"]:
            for sid in l["steps"]:
                (dst / "steps" / f"{sid}.html").write_text(
                    build_step(d, l, sid, f"../../{other_lang}/steps/{sid}.html"), encoding="utf-8")
        if d["models"].get("pages"):
            (dst / "models").mkdir()
            for mid in d["models"]["pages"]:
                (dst / "models" / f"{mid}.html").write_text(
                    build_model_page(d, mid, f"../../{other_lang}/models/{mid}.html"), encoding="utf-8")
        if d.get("guide"):
            (dst / "guide.html").write_text(build_guide(d, f"../{other_lang}/guide.html"), encoding="utf-8")
        if lang == "en":
            (OUT / "phoenix-pipelines.drawio").write_text(build_drawio(d, "en/steps/"), encoding="utf-8")
        print(f"{lang}: {sum(len(l['steps']) for l in d['lanes'])} step pages -> {dst}")


if __name__ == "__main__":
    main()
