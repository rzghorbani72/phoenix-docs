#!/usr/bin/env python3
"""Build public/phoenix-pipelines.drawio from the English content: one swimlane per pipeline with a
linked box per step, plus a second page with one linked box per model. Box links open the React app
(index.html#/step/<id>, index.html#/model/<id>), which is served next to the drawio file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "public" / "phoenix-pipelines.drawio"
sys.path.insert(0, str(HERE))

FILL = {"teal": "#d5f5ef", "violet": "#ebe3fc", "orange": "#fdebd7",
        "pink": "#fbe3ef", "cyan": "#d9f6fb", "blue": "#dfe9fb", "green": "#dff3e1"}
LINE = {"teal": "#0f9e87", "violet": "#7b54d6", "orange": "#d97a1c",
        "pink": "#cf4f8f", "cyan": "#1597ad", "blue": "#3c6fc4", "green": "#3d9a47"}
STATUS_FILL = {"live": "#dff3e1", "external": "#fbf0d2", "unknown": "#e2edfb", "off": "#eceff3", "notdeployed": "#fbe4e2"}
APP = "index.html#/"


def lane_cells(d):
    """Swimlane per pipeline, one node per step linked to its app route; layout is a simple grid."""
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    y, per_row, cw, ch, gx, gy = 20, 6, 190, 70, 30, 26
    for l in d["lanes"]:
        rows = (len(l["steps"]) + per_row - 1) // per_row
        lh = 44 + rows * (ch + gy) + 10
        lw = 30 + per_row * (cw + gx)
        lane_id = f"lane_{l['id']}"
        cells.append(f'<mxCell id="{lane_id}" value={quoteattr(l["title_plain"])} style="swimlane;horizontal=1;startSize=34;fontStyle=1;fontSize=15;'
                     f'fillColor={FILL[l["color"]]};strokeColor={LINE[l["color"]]};swimlaneFillColor=#ffffff;rounded=1;arcSize=4;" vertex="1" parent="1">'
                     f'<mxGeometry x="20" y="{y}" width="{lw}" height="{lh}" as="geometry"/></mxCell>')
        prev = None
        for i, sid in enumerate(l["steps"]):
            s = d["steps"][sid]
            r, c = divmod(i, per_row)
            dashed = "dashed=1;" if s["status"] in ("off", "notdeployed", "unknown") else ""
            label = f'{l["prefix"]}{i + 1}. {s["title_plain"]}\n{s.get("chip_plain", "")}'
            cells.append(f'<UserObject id="s_{sid}" label={quoteattr(label)} link={quoteattr(APP + "step/" + sid)} status="{s["status"]}">'
                         f'<mxCell style="rounded=1;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor={LINE[l["color"]]};strokeWidth=2;fontSize=12;{dashed}" vertex="1" parent="{lane_id}">'
                         f'<mxGeometry x="{20 + c * (cw + gx)}" y="{44 + r * (ch + gy)}" width="{cw}" height="{ch}" as="geometry"/></mxCell></UserObject>')
            if prev:
                cells.append(f'<mxCell id="e_{prev}_{sid}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=block;strokeColor={LINE[l["color"]]};" edge="1" parent="{lane_id}" source="s_{prev}" target="s_{sid}">'
                             '<mxGeometry relative="1" as="geometry"/></mxCell>')
            prev = sid
        y += lh + 30
    return cells


def model_cells(d):
    """One linked box per model page, in card order, coloured by status."""
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    per_row, cw, ch, gx, gy = 5, 230, 84, 26, 26
    cards = [c for c in d["models"]["cards"] if c.get("id") in d["models"]["pages"]]
    for i, c in enumerate(cards):
        r, col = divmod(i, per_row)
        label = re.sub(r"[`*]", "", f'{d["models"]["pages"][c["id"]]["title_plain"]}\n{c["size"]}')
        cells.append(f'<UserObject id="m_{c["id"]}" label={quoteattr(label)} link={quoteattr(APP + "model/" + c["id"])} status="{c["status"]}">'
                     f'<mxCell style="rounded=1;whiteSpace=wrap;html=0;fillColor={STATUS_FILL.get(c["status"], "#ffffff")};strokeColor=#3c6fc4;fontSize=12;" vertex="1" parent="1">'
                     f'<mxGeometry x="{20 + col * (cw + gx)}" y="{20 + r * (ch + gy)}" width="{cw}" height="{ch}" as="geometry"/></mxCell></UserObject>')
    return cells


def main():
    from content_en import DATA
    head = ('<mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
            'fold="1" page="0" pageScale="1" math="0" shadow="0"><root>')
    pages = [("ex", "EX pipelines", lane_cells(DATA)), ("models", "Model catalog", model_cells(DATA))]
    OUT.write_text('<mxfile host="phoenix-pipelines">' + "".join(
        f'<diagram id="{i}" name="{n}">{head}{"".join(c)}</root></mxGraphModel></diagram>' for i, n, c in pages) + "</mxfile>",
        encoding="utf-8")
    print(f"drawio: {sum(len(l['steps']) for l in DATA['lanes'])} steps, {len(DATA['models']['pages'])} models -> {OUT}")


if __name__ == "__main__":
    main()
