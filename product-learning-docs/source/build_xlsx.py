#!/usr/bin/env python3
"""Build the EX Fit-Gap tracker .xlsx without third-party libraries.

openpyxl / xlsxwriter are unavailable in this environment (no pip), so this
writes the OOXML package directly.  An .xlsx is a zip of XML parts; we emit the
minimum valid set plus styles, RTL sheet views, freeze panes and autofilter.

Usage:  python3 build_xlsx.py
Output: ../product-management/FIT_GAP_TRACKER.xlsx
"""

from __future__ import annotations

import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "product-management" / "FIT_GAP_TRACKER.xlsx"
# Same sheets rendered as a page; apply_theme.py styles it and build.sh publishes it.
HTML_OUT = HERE / "fit_gap_tracker_fa.html"
# Quoted because the sheet name contains a ZWNJ (U+200C).
ROWS_REF = "'ردیف‌ها'"

# --------------------------------------------------------------------------
# XML helpers
# --------------------------------------------------------------------------

def esc(text: object) -> str:
    """Escape text for XML character data and attribute values."""
    s = "" if text is None else str(text)
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def col_letter(idx: int) -> str:
    """1 -> A, 27 -> AA."""
    out = ""
    while idx > 0:
        idx, rem = divmod(idx - 1, 26)
        out = chr(65 + rem) + out
    return out


# --------------------------------------------------------------------------
# Style indices (must match styles.xml below)
# --------------------------------------------------------------------------
S_BASE = 0        # plain, wrapped, top-aligned
S_HEADER = 1      # white bold on dark blue
S_TITLE = 2       # large bold, no border
S_OK = 3          # green fill      - confirmed
S_BAD = 4         # red fill        - refuted / critical
S_WARN = 5        # amber fill      - partial
S_GAP = 6         # grey fill       - absent
S_EDIT = 7        # blue fill       - you fill this in
S_MONO = 8        # small mono-ish, for file:line evidence
S_NOTE = 9        # italic grey
S_NUM = 10        # centred number
S_SUBHEAD = 11    # bold on light grey

STATUS_STYLE = {
    "تأییدشده": S_OK,
    "تأییدشده (ارتقا)": S_OK,
    "تأییدشده (ارتقا از Customization)": S_OK,
    "رد شد (نقص امنیتی بحرانی)": S_BAD,
    "رد شد (ادعا نادرست)": S_BAD,
    "رد شد": S_BAD,
    "رد شد (جزئی)": S_BAD,
    "رد شد (واقعیت بهتر از ادعا)": S_WARN,
    "جزئی": S_WARN,
    "جزئی → «تنظیم» نه «توسعه»": S_WARN,
    "غایب": S_GAP,
    "غایب (فرایند)": S_GAP,
    "غایب (در ریپوهای فعال)": S_GAP,
    "تنظیم": S_BASE,
    "تنظیم / زیرساخت": S_BASE,
    "خارج از کد": S_BASE,
}


def status_style(value: str) -> int:
    if value in STATUS_STYLE:
        return STATUS_STYLE[value]
    if value.startswith("رد شد"):
        return S_BAD
    if value.startswith("تأییدشده"):
        return S_OK
    if value.startswith("جزئی"):
        return S_WARN
    if value.startswith("غایب"):
        return S_GAP
    if value.startswith("خالی"):
        return S_EDIT
    if value.startswith("نامشخص"):
        return S_WARN
    return S_BASE


# --------------------------------------------------------------------------
# Sheet construction
# --------------------------------------------------------------------------

class Sheet:
    def __init__(self, name: str, widths: list[float], freeze: str | None = None,
                 autofilter: str | None = None, rtl: bool = True) -> None:
        self.name = name
        self.widths = widths
        self.freeze = freeze
        self.autofilter = autofilter
        self.rtl = rtl
        self.rows: list[tuple[int | None, list[tuple[object, int, bool]]]] = []

    def add(self, cells: list[tuple[object, int]] | list[tuple[object, int, bool]],
            height: int | None = None) -> None:
        norm: list[tuple[object, int, bool]] = []
        for cell in cells:
            if len(cell) == 3:
                norm.append((cell[0], cell[1], cell[2]))  # type: ignore[misc]
            else:
                norm.append((cell[0], cell[1], False))
        self.rows.append((height, norm))

    def xml(self) -> str:
        parts: list[str] = []
        parts.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
        parts.append(
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        )
        # sheetView: rightToLeft for Persian, optional frozen pane
        view = f'<sheetView workbookViewId="0" rightToLeft="{1 if self.rtl else 0}"'
        if self.freeze:
            col = "".join(c for c in self.freeze if c.isalpha())
            row = "".join(c for c in self.freeze if c.isdigit())
            xsplit = 0 if col == "A" else len(col) and (ord(col[-1]) - 64)
            view += ">"
            view += (
                f'<pane xSplit="{xsplit}" ySplit="{int(row) - 1}" topLeftCell="{self.freeze}"'
                f' activePane="bottomRight" state="frozen"/>'
            )
            view += "</sheetView>"
        else:
            view += "/>"
        parts.append(f"<sheetViews>{view}</sheetViews>")
        parts.append('<sheetFormatPr defaultRowHeight="15"/>')

        if self.widths:
            parts.append("<cols>")
            for i, w in enumerate(self.widths, start=1):
                parts.append(f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>')
            parts.append("</cols>")

        parts.append("<sheetData>")
        for r_idx, (height, cells) in enumerate(self.rows, start=1):
            attr = f' ht="{height}" customHeight="1"' if height else ""
            parts.append(f'<row r="{r_idx}"{attr}>')
            for c_idx, (value, style, is_formula) in enumerate(cells, start=1):
                if value is None or value == "":
                    parts.append(f'<c r="{col_letter(c_idx)}{r_idx}" s="{style}"/>')
                    continue
                ref = f"{col_letter(c_idx)}{r_idx}"
                if is_formula:
                    parts.append(
                        f'<c r="{ref}" s="{style}"><f>{esc(str(value).lstrip("="))}</f></c>'
                    )
                elif isinstance(value, (int, float)) and not isinstance(value, bool):
                    parts.append(f'<c r="{ref}" s="{style}"><v>{value}</v></c>')
                else:
                    parts.append(
                        f'<c r="{ref}" s="{style}" t="inlineStr">'
                        f"<is><t xml:space=\"preserve\">{esc(value)}</t></is></c>"
                    )
            parts.append("</row>")
        parts.append("</sheetData>")

        if self.autofilter:
            parts.append(f'<autoFilter ref="{self.autofilter}"/>')
        parts.append(
            '<pageMargins left="0.3" right="0.3" top="0.4" bottom="0.4"'
            ' header="0.2" footer="0.2"/>'
        )
        parts.append("</worksheet>")
        return "".join(parts)


STYLES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="7">
  <font><sz val="10"/><name val="Arial"/></font>
  <font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Arial"/></font>
  <font><b/><sz val="14"/><color rgb="FF1F3864"/><name val="Arial"/></font>
  <font><sz val="8"/><color rgb="FF444444"/><name val="Consolas"/></font>
  <font><i/><sz val="9"/><color rgb="FF666666"/><name val="Arial"/></font>
  <font><b/><sz val="10"/><color rgb="FF1F3864"/><name val="Arial"/></font>
  <font><b/><sz val="10"/><color rgb="FFC00000"/><name val="Arial"/></font>
</fonts>
<fills count="8">
  <fill><patternFill patternType="none"/></fill>
  <fill><patternFill patternType="gray125"/></fill>
  <fill><patternFill patternType="solid"><fgColor rgb="FF1F3864"/><bgColor indexed="64"/></patternFill></fill>
  <fill><patternFill patternType="solid"><fgColor rgb="FFD9EAD3"/><bgColor indexed="64"/></patternFill></fill>
  <fill><patternFill patternType="solid"><fgColor rgb="FFF4CCCC"/><bgColor indexed="64"/></patternFill></fill>
  <fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/><bgColor indexed="64"/></patternFill></fill>
  <fill><patternFill patternType="solid"><fgColor rgb="FFEFEFEF"/><bgColor indexed="64"/></patternFill></fill>
  <fill><patternFill patternType="solid"><fgColor rgb="FFDEEAF6"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="2">
  <border><left/><right/><top/><bottom/><diagonal/></border>
  <border>
    <left style="thin"><color rgb="FFBFBFBF"/></left>
    <right style="thin"><color rgb="FFBFBFBF"/></right>
    <top style="thin"><color rgb="FFBFBFBF"/></top>
    <bottom style="thin"><color rgb="FFBFBFBF"/></bottom>
    <diagonal/>
  </border>
</borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="12">
  <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment vertical="center" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="6" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="0" fillId="5" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="0" fillId="6" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="0" fillId="7" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="3" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1" readingOrder="1"/></xf>
  <xf numFmtId="0" fontId="4" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" readingOrder="2"/></xf>
  <xf numFmtId="0" fontId="5" fillId="6" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1" readingOrder="2"/></xf>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
<dxfs count="0"/>
<tableStyles count="0" defaultTableStyle="TableStyleMedium9"/>
</styleSheet>"""


def write_workbook(sheets: list[Sheet], path: Path) -> None:
    n = len(sheets)
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
          '<Default Extension="xml" ContentType="application/xml"/>',
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>']
    for i in range(1, n + 1):
        ct.append(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml"'
            ' ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    ct.append("</Types>")

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Target="xl/workbook.xml"'
        ' Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"/>'
        "</Relationships>"
    )

    wb = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
          ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
          "<sheets>"]
    for i, sh in enumerate(sheets, start=1):
        wb.append(f'<sheet name="{esc(sh.name)}" sheetId="{i}" r:id="rId{i}"/>')
    wb.append("</sheets></workbook>")

    wb_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for i in range(1, n + 1):
        wb_rels.append(
            f'<Relationship Id="rId{i}" Target="worksheets/sheet{i}.xml"'
            ' Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"/>'
        )
    wb_rels.append(
        f'<Relationship Id="rId{n + 1}" Target="styles.xml"'
        ' Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"/>'
    )
    wb_rels.append("</Relationships>")

    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", "".join(wb))
        z.writestr("xl/_rels/workbook.xml.rels", "".join(wb_rels))
        z.writestr("xl/styles.xml", STYLES_XML)
        for i, sh in enumerate(sheets, start=1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sh.xml())


# --------------------------------------------------------------------------
# Load data
# --------------------------------------------------------------------------
# HTML view of the same sheets
# --------------------------------------------------------------------------

CELL_CLASS = {
    S_OK: "c-ok", S_BAD: "c-bad", S_WARN: "c-warn", S_GAP: "c-gap", S_EDIT: "c-edit",
    S_MONO: "c-mono", S_NOTE: "c-note", S_NUM: "c-num",
}
STATUS_TAG = {S_OK: "t-ok", S_BAD: "t-bad", S_WARN: "t-warn", S_GAP: "t-gap", S_EDIT: "t-info"}


def eval_formula(formula: str, rows_sheet: Sheet) -> str:
    """Evaluate the COUNTIF / COUNTBLANK formulas used on the summary sheet."""
    import re

    m = re.search(r"\$([A-Z]+)\$2:\$[A-Z]+\$(\d+)", formula)
    if not m:
        return ""
    col = 0
    for ch in m.group(1):
        col = col * 26 + ord(ch) - 64
    values = [str(cells[col - 1][0] or "") for _, cells in rows_sheet.rows[1:]]
    crit = re.search(r',"([^"]*)"\)', formula)
    if "COUNTBLANK" in formula:
        n = sum(1 for v in values if not v.strip())
    elif crit:
        pat = crit.group(1)
        n = sum(1 for v in values if (v.startswith(pat[:-1]) if pat.endswith("*") else v == pat))
    else:
        return ""
    total = re.search(r"/(\d+),", formula)
    if total:
        return f"{n / int(total.group(1)):.0%}"
    return str(n)


def sheet_html(sheet: Sheet, rows_sheet: Sheet, anchor: str, filterable: bool) -> str:
    out: list[str] = [f'<h2 id="{anchor}">{esc(sheet.name)}</h2>']
    rows = sheet.rows
    if rows and all(style == S_TITLE for _, style, _ in rows[0][1]):
        out.append(f'<p class="lede">{esc(rows[0][1][0][0])}</p>')
        rows = rows[1:]
    if filterable:
        out.append(
            '<div class="filters"><input type="search" id="q" placeholder="جست‌وجو در ID، نیازمندی، شاهد…" '
            'aria-label="جست‌وجو">'
            '<select id="st" aria-label="فیلتر وضعیت"><option value="">همه وضعیت‌ها</option>'
            '<option value="c-ok">تأییدشده</option><option value="c-warn">جزئی / نامشخص</option>'
            '<option value="c-bad">رد شد</option><option value="c-gap">غایب</option>'
            '<option value="c-edit">خالی در توافق</option><option value="plain">تنظیم / خارج از کد</option></select>'
            '<span id="cnt" class="small"></span></div>'
        )
    ncols = max((len(c) for _, c in rows), default=0)
    wide = ncols > 6
    total = sum(sheet.widths) or 1
    if wide:  # Excel character widths -> pixels, so the page keeps the sheet's proportions
        cols = "".join(f'<col style="width:{round(w * 8.5)}px">' for w in sheet.widths)
        out.append(f'<div class="scroll-x"><table class="sheet wide" style="width:{round(total * 8.5)}px">')
    else:
        cols = "".join(f'<col style="width:{w / total:.1%}">' for w in sheet.widths)
        out.append('<div class="scroll-x"><table class="sheet">')
    out.append(f"<colgroup>{cols}</colgroup>")
    body_open = False
    for _, cells in rows:
        if all((v is None or v == "") for v, _, _ in cells):
            continue
        styles = [s for _, s, _ in cells]
        if all(s == S_HEADER for s in styles):
            out.append("<thead><tr>" + "".join(f"<th>{esc(v)}</th>" for v, _, _ in cells) + "</tr></thead>")
            continue
        if not body_open:
            out.append("<tbody>")
            body_open = True
        if styles[0] == S_SUBHEAD and all(not v for v, _, _ in cells[1:]):
            out.append(f'<tr class="sub"><td colspan="{ncols}">{esc(cells[0][0])}</td></tr>')
            continue
        tds = []
        row_status = ""
        for i, (value, style, is_formula) in enumerate(cells):
            text = eval_formula(str(value), rows_sheet) if is_formula else ("" if value is None else str(value))
            cls = CELL_CLASS.get(style, "")
            if style == S_SUBHEAD:
                cls = "c-key"
            inner = esc(text)
            if filterable and i == 7:  # verified status column -> pill
                row_status = cls or "plain"
                tag = STATUS_TAG.get(style)
                inner = f'<span class="tag {tag}">{inner}</span>' if tag and text else inner
                cls = ""
            tds.append(f'<td class="{cls}">{inner}</td>' if cls else f"<td>{inner}</td>")
        attr = f' data-st="{row_status}"' if filterable else ""
        out.append(f"<tr{attr}>" + "".join(tds) + "</tr>")
    if body_open:
        out.append("</tbody>")
    out.append("</table></div>")
    return "\n".join(out)


FILTER_JS = """
(function () {
  var q = document.getElementById('q'), st = document.getElementById('st'), cnt = document.getElementById('cnt');
  if (!q) return;
  var rows = [].slice.call(document.querySelectorAll('tr[data-st]'));
  function run() {
    var term = q.value.trim().toLowerCase(), want = st.value, n = 0;
    rows.forEach(function (r) {
      var ok = (!want || r.getAttribute('data-st') === want) && (!term || r.textContent.toLowerCase().indexOf(term) > -1);
      r.hidden = !ok; if (ok) n++;
    });
    cnt.textContent = n + ' از ' + rows.length + ' ردیف';
  }
  q.addEventListener('input', run); st.addEventListener('change', run); run();
})();
"""


def write_html(sheets: list[Sheet], rows_sheet: Sheet, path: Path) -> None:
    anchors = ["guide", "rows", "summary", "findings", "architecture"]
    nav = "".join(
        f'<li><a href="#{a}">{esc(s.name)}</a></li>' for a, s in zip(anchors, sheets)
    )
    sections = "\n".join(
        sheet_html(s, rows_sheet, a, filterable=(s is rows_sheet)) for a, s in zip(anchors, sheets)
    )
    page = f"""<!doctype html>
<html lang="fa" dir="rtl">
  <head>
    <meta charset="utf-8" />
    <title>Phoenix — ردیاب Fit-Gap</title>
  </head>
  <body>
    <section class="cover">
      <div class="small">محرمانه — داخلی MCINEXT</div>
      <h1>ردیاب Fit-Gap پایلوت صدای کارکنان</h1>
      <div class="sub">۸۷ نیازمندی توافق MCINEXT × EX همراه اول، با وضعیت تأییدشده از کد، شاهد، مالک وابستگی و ددلاین پیشنهادی</div>
      <p class="meta">نسخه قابل ویرایش: <code>FIT_GAP_TRACKER.xlsx</code> (همین داده؛ ستون‌های «اولویت EX» و «ددلاین نهایی» را در Excel پر کنید) · تولیدشده از <code>source/verdicts.tsv</code> و <code>fitgap_part*.tsv</code></p>
      <nav class="menu"><div class="menu-grp">شیت‌ها</div><ul>{nav}</ul></nav>
    </section>
{sections}
    <script>{FILTER_JS}</script>
  </body>
</html>
"""
    path.write_text(page, encoding="utf-8")


# --------------------------------------------------------------------------

def load_tsv(name: str, expected: int) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in (HERE / name).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        fields = line.split("\t")
        fields += [""] * (expected - len(fields))
        rows.append(fields[:expected])
    return rows


def main() -> None:
    src = (
        load_tsv("fitgap_part1.tsv", 7)
        + load_tsv("fitgap_part2.tsv", 7)
        + load_tsv("fitgap_part3.tsv", 7)
    )
    verdict_rows = load_tsv("verdicts.tsv", 7)
    verdicts = {r[0]: r for r in verdict_rows}

    missing = [r[1] for r in src if r[1] not in verdicts]
    if missing:
        raise SystemExit(f"verdicts.tsv is missing IDs: {missing}")
    print(f"loaded {len(src)} requirements, {len(verdicts)} verdicts")

    # ---------------- Sheet 1: راهنما ----------------
    guide = Sheet("راهنما", [34, 96], rtl=True)
    guide.add([("راهنمای استفاده از این فایل", S_TITLE), ("", S_TITLE)], 26)
    guide.add([("", S_BASE), ("", S_BASE)])
    info = [
        ("موضوع", "توافق Fit-Gap پایلوت صدای کارکنان (EX) — MCINEXT × اداره تجربه کارکنان همراه اول"),
        ("تعداد نیازمندی", "۸۷ ردیف در ۸ بلوک"),
        ("مبنای ستون «وضعیت تأییدشده»", "خوانش مستقیم کد مخزن phoenix — فقط پروژه‌های پایتونِ فعال در ۳ ماه گذشته"),
        ("تاریخ بررسی کد", "۱۴۰۵/۰۷/۰۶ — معادل 2026-09-28"),
        ("دامنه بررسی", "coa-api, aiva, adcs, aqa, chatbot-iva-agent, agentlib, adcs-auth, adcs-knowledgebase, aiva-knowledgebase, fastlib"),
        ("خارج از دامنه", "python/coa-ai — موتور تحلیل احساسات/خلاصه/موضوع. آخرین کامیت 2025-07-13 (۱۴ ماه فریز)"),
        ("", ""),
        ("ستون‌هایی که شما پر می‌کنید", "«اولویت EX» را EX پر می‌کند. «ددلاین نهایی» را شما بر اساس ستون «ددلاین پیشنهادی» تثبیت می‌کنید."),
        ("قاعده ددلاین", "هیچ تاریخ تقویمی ننویسید. بنویسید «T + n روز کاری از دریافت [ورودی مشخص]». مبنای این قاعده معیار پذیرش خودِ ردیف TEC-14 است."),
        ("", ""),
        ("معنای رنگ‌ها", ""),
    ]
    for k, v in info:
        style = S_SUBHEAD if k and not v else S_BASE
        guide.add([(k, S_SUBHEAD if k else S_BASE), (v, style if not v else S_BASE)])
    legend = [
        ("سبز — تأییدشده", "در کد پیدا شد و کار می‌کند. قابل دفاع در UAT."),
        ("زرد — جزئی", "بخشی پیاده شده. بدون توضیح، در UAT رد می‌شود."),
        ("قرمز — رد شد", "ادعای توافق با کد نمی‌خواند. پیش از جلسه اصلاح کنید."),
        ("طوسی — غایب", "هیچ کدی وجود ندارد. توسعه واقعی لازم است."),
        ("آبی — خالی", "ستون در توافق خالی مانده و باید پر شود."),
        ("بدون رنگ — تنظیم/زیرساخت", "کد لازم نیست؛ Configuration یا فرایند است."),
    ]
    for k, v in legend:
        guide.add([(k, status_style(k.split(" — ")[1] if " — " in k else "")), (v, S_BASE)])
    guide.add([("", S_BASE), ("", S_BASE)])
    guide.add([("نمونه سطر پرشده", S_SUBHEAD),
               ("مثال: PRV-03 | ادعا: موجود در محصول | تأییدشده: رد شد | شاهد: coa/apps/files/views.py:19 | ددلاین: پیش از UAT، T+3 روز کاری", S_BASE)])

    # ---------------- Sheet 2: ردیف‌ها ----------------
    headers = [
        "بلوک", "ID", "نیازمندی", "شرح نیاز / رفتار مورد انتظار",
        "سناریو یا معیار پذیرش", "اولویت EX", "وضعیت اعلامی MCINEXT",
        "وضعیت تأییدشده با کد", "شاهد در کد (file:line)", "اطمینان",
        "مالک وابستگی", "ددلاین پیشنهادی", "اقدام لازم / ریسک",
        "توضیحات فنی توافق", "ددلاین نهایی",
    ]
    widths = [22, 9, 26, 52, 46, 10, 20, 22, 46, 9, 16, 30, 52, 40, 16]
    rows_sheet = Sheet("ردیف‌ها", widths, freeze="A2",
                       autofilter=f"A1:{col_letter(len(headers))}1")
    rows_sheet.add([(h, S_HEADER) for h in headers], 44)
    for r in src:
        block, rid, req, desc, crit, claimed, notes = r
        v = verdicts[rid]
        _, vstatus, evidence, conf, owner, deadline, action = v
        st = status_style(vstatus)
        rows_sheet.add([
            (block, S_BASE), (rid, S_NUM), (req, S_BASE), (desc, S_BASE),
            (crit, S_BASE), ("", S_EDIT), (claimed, S_BASE),
            (vstatus, st), (evidence, S_MONO), (conf, S_NUM),
            (owner, S_BASE), (deadline, S_BASE), (action, st),
            (notes, S_NOTE), ("", S_EDIT),
        ])

    # ---------------- Sheet 3: خلاصه ----------------
    last = len(src) + 1
    summ = Sheet("خلاصه", [34, 14, 14, 62])
    summ.add([("خلاصه وضعیت — محاسبه زنده از شیت «ردیف‌ها»", S_TITLE), ("", S_TITLE), ("", S_TITLE), ("", S_TITLE)], 26)
    summ.add([("", S_BASE)] * 4)
    summ.add([(h, S_HEADER) for h in ("دسته", "تعداد", "درصد", "تفسیر")], 30)

    claimed_groups = [
        ("موجود در محصول", "ادعای «ساخته شده» — بیشترین فشار UAT روی این‌هاست"),
        ("نیازمند تنظیم / Configuration", "بدون کد جدید؛ سریع‌ترین بخش"),
        ("نیازمند توسعه / Customization", "توسعه واقعی؛ منبع اصلی ریسک زمان‌بندی"),
        ("نیازمند بررسی فنی", "باید به آیتم برآوردشده تبدیل شود"),
        ("فعلاً خارج از Scope", "هر دو ردیف با کد نمی‌خوانند — AI-02 و PRV-08"),
    ]
    summ.add([("— وضعیت اعلامی در توافق —", S_SUBHEAD), ("", S_SUBHEAD), ("", S_SUBHEAD), ("", S_SUBHEAD)])
    for label, meaning in claimed_groups:
        summ.add([
            (label, S_BASE),
            (f'=COUNTIF({ROWS_REF}!$G$2:$G${last},"{label}")', S_NUM, True),
            (f'=IFERROR(COUNTIF({ROWS_REF}!$G$2:$G${last},"{label}")/{len(src)},"")', S_NUM, True),
            (meaning, S_BASE),
        ])
    summ.add([
        ("بدون وضعیت (خالی)", S_BASE),
        (f'=COUNTBLANK({ROWS_REF}!$G$2:$G${last})', S_NUM, True),
        (f'=IFERROR(COUNTBLANK({ROWS_REF}!$G$2:$G${last})/{len(src)},"")', S_NUM, True),
        ("KB-02 و TEC-12 تا TEC-15", S_BASE),
    ])
    summ.add([("", S_BASE)] * 4)
    summ.add([("— وضعیت تأییدشده با کد —", S_SUBHEAD), ("", S_SUBHEAD), ("", S_SUBHEAD), ("", S_SUBHEAD)])
    verified_groups = [
        ("تأییدشده*", "در کد اثبات شد — قابل دفاع"),
        ("جزئی*", "بخشی پیاده — نیازمند توضیح دقیق در جلسه"),
        ("رد شد*", "ادعای توافق نادرست — پیش از جلسه اصلاح شود"),
        ("غایب*", "هیچ کدی نیست — توسعه واقعی"),
        ("نامشخص*", "در coa-ai فریزشده — بدون داده سرعت تیم"),
        ("تنظیم*", "Configuration یا زیرساخت"),
        ("خارج از کد*", "فرایند یا وظیفه EX"),
        ("خالی*", "ستون توافق خالی است"),
    ]
    for label, meaning in verified_groups:
        summ.add([
            (label.replace("*", ""), S_BASE),
            (f'=COUNTIF({ROWS_REF}!$H$2:$H${last},"{label}")', S_NUM, True),
            (f'=IFERROR(COUNTIF({ROWS_REF}!$H$2:$H${last},"{label}")/{len(src)},"")', S_NUM, True),
            (meaning, S_BASE),
        ])
    summ.add([("", S_BASE)] * 4)
    summ.add([("— وابستگی —", S_SUBHEAD), ("", S_SUBHEAD), ("", S_SUBHEAD), ("", S_SUBHEAD)])
    for owner_label, meaning in [
        ("EX*", "ساعت شما شروع نمی‌شود تا EX ورودی را تحویل دهد"),
        ("MCINEXT*", "تعهد مستقیم تیم شما"),
        ("مشترک*", "نیازمند تصمیم دوطرفه"),
        ("MCI-IT*", "خارج از کنترل هر دو تیم — مثل دسترسی SAP"),
    ]:
        summ.add([
            (owner_label.replace("*", ""), S_BASE),
            (f'=COUNTIF({ROWS_REF}!$K$2:$K${last},"{owner_label}")', S_NUM, True),
            (f'=IFERROR(COUNTIF({ROWS_REF}!$K$2:$K${last},"{owner_label}")/{len(src)},"")', S_NUM, True),
            (meaning, S_BASE),
        ])
    summ.add([("", S_BASE)] * 4)
    summ.add([
        ("یادداشت", S_SUBHEAD),
        ("", S_BASE), ("", S_BASE),
        ("درصدها با فرمول COUNTIF محاسبه می‌شوند؛ اگر وضعیتی را در شیت «ردیف‌ها» تغییر دهید این جدول خودکار به‌روز می‌شود. "
         "ستاره در الگوی جست‌وجو به معنای «شروع‌شده با» است.", S_NOTE),
    ])

    # ---------------- Sheet 4: یافته‌های بحرانی ----------------
    find = Sheet("یافته‌های بحرانی", [8, 26, 34, 58, 30])
    find.add([("یافته‌های بحرانی از خوانش کد", S_TITLE), ("", S_TITLE), ("", S_TITLE), ("", S_TITLE), ("", S_TITLE)], 26)
    find.add([("", S_BASE)] * 5)
    find.add([(h, S_HEADER) for h in ("#", "عنوان", "شاهد در کد", "معنا برای کسب‌وکار", "اقدام")], 34)
    findings = [
        ("۱", "IDOR روی فایل صوتی خام",
         "coa/apps/files/views.py:19 — @with_permissions({view_calls}) و سپس minio.download(name) بدون بررسی مالکیت",
         "هر کاربر دارای view_calls می‌تواند صوت هر تماسی را دانلود کند. نام فایل از call_id مشتق می‌شود. "
         "ردیف PRV-03 «موجود» علامت خورده و نیست. روی داده صوتی کارکنان، این یافته می‌تواند پایلوت را متوقف کند.",
         "⛔ اصلاح پیش از UAT — T+3 روز کاری", S_BAD),
        ("۲", "Transcript ذخیره می‌شود ولی «خارج از Scope» اعلام شده",
         "coa/apps/main/models.py:397 (raw_input) · services/call.py:771 · chatbot-iva-agent/src/schema.py (messages[].text)",
         "متن مکالمه ذخیره و روی Kafka منتشر می‌شود و حتی transcript_confidence دارد. ادعای AI-02 و دلیل PRV-08 نادرست است. "
         "هم اعتبار فنی را می‌برد و هم یک ریسک حریم خصوصی اعلام‌نشده ایجاد می‌کند.",
         "تصمیم سیاست در ۲ روز: نگهداری و اعلام، یا توقف ذخیره", S_BAD),
        ("۳", "Audit Log وجود ندارد",
         "جست‌وجوی audit|LogEntry|access_log|viewed_by|actor_id در ۸ سرویس → صفر نتیجه",
         "ردیف PRV-06 «موجود» علامت خورده است. آنچه هست coa/middlewares.py:26 است که لاگ زیرساختی است نه Audit Trail قابل کوئری. "
         "ضمناً همان میدل‌ویر تمام هدرها را لاگ می‌کند؛ یعنی توکن‌های Authorization وارد لاگ می‌شوند.",
         "Downgrade در توافق + برآورد T+10 روز کاری", S_BAD),
        ("۴", "موتور تحلیل ۱۴ ماه فریز است",
         "python/coa-ai — آخرین کامیت 2025-07-13، در حالی که coa-api در 2026-09-27 کامیت دارد",
         "تمام ردیف‌های کیفیت بلوک ۳ (AI-04 تا AI-07، AI-12، AI-13) از کدی می‌گذرند که هیچ داده سرعتِ به‌روز ندارد. "
         "برای این بلوک ددلاین تهاجمی ندهید.",
         "بازفعال‌سازی یا تأیید پایداری پیش از تعهد", S_WARN),
        ("۵", "هیچ سنجش کیفیتی برای AIVA و CCA وجود ندارد",
         "تنها Eval موجود: aqa POST /api/v1/eval/run — هیچ معادلی برای WER، Faithfulness یا دقت Theme نیست",
         "۴۳ ردیف «موجود در محصول» شامل ۱۱ ادعای کیفیتی است. «موجود» یعنی implemented نه measured، "
         "ولی EX آن را measured تست می‌کند (معیار AI-06 صریحاً مقایسه با نمونه Human-coded است).",
         "Golden Set حداقلی پیش از UAT", S_WARN),
        ("۶", "خبر خوب: Pruner مخرب وجود ندارد",
         "تمام مسیرهای حذف بررسی شد: archive_old_calls.py (آرشیو→حذف) · trends/services/sync.py:388 (بازسازی کامل) · services/call.py:448",
         "آنچه روی وایت‌بورد به‌عنوان «حذف topic و تماس‌هایش» طراحی شده بود پیاده نشده است. "
         "همچنین TrendAnnotation عمداً denormalize شده تا یادداشت‌های انسانی از بازسازی جان سالم ببرند.",
         "اقدامی لازم نیست — این را به‌عنوان نقطه قوت ارائه کنید", S_OK),
        ("۷", "خبر خوب: Retention بهتر از ادعاست",
         "archive_old_calls.py — pg_dump → MinIO → حذف → VACUUM، با abort-on-failure و --dry-run",
         "PRV-07 درست است و PRV-08 هم عملاً پوشش داده شده چون call_ai_tags هم آرشیو و حذف می‌شود. "
         "شما دارید کمتر از توان واقعی‌تان ادعا می‌کنید.",
         "PRV-08 را از «خارج از Scope» خارج کنید", S_OK),
        ("۸", "خبر خوب: پیامک ساخته شده",
         "aiva/tools/sms.py → POST resan.mci.dev/api/messages/send/to/ · در AGENT_ENABLED_TOOLS پیش‌فرض فعال",
         "KB-06 به‌اشتباه «نیازمند توسعه» علامت خورده است. اما LLM خودش تصمیم ارسال می‌گیرد، "
         "پس وابستگی واقعی «سناریوهای EX» یک نیاز Guardrail است نه یک نیاز یکپارچه‌سازی.",
         "ارتقا به «موجود» + Rate limit در T+5 روز کاری", S_OK),
        ("۹", "Whitelist هست ولی جای اشتباه",
         "aiva/memory/config.py:20-21 — PHONE_WHITELIST=[] و BYPASS_WHITELIST=True · aiva_consume_kafka.py:310",
         "این Whitelist فقط «جمع‌آوری memory» را گیت می‌کند، نه «پذیرش تماس». نیاز VIA-02 پذیرش تماس است "
         "که باید در لایه SIP پیاده شود. ضمناً پیش‌فرض روی Bypass است.",
         "گیت SIP + پرکردن PHONE_WHITELIST و BYPASS_WHITELIST=false", S_WARN),
        ("۱۰", "AQA قوی‌ترین دارایی نمایشی شماست",
         "python/aqa — 9,119 خط · POST /api/v1/chat/message (SSE) · /configs/prompts قابل ویرایش در Runtime · /eval/run",
         "ردیف AN-12 (دستیار تحلیل با زبان طبیعی) که بلندپروازانه‌ترین ردیف توافق است، واقعاً ساخته شده "
         "و تنها سرویسی است که Eval Harness دارد.",
         "در جلسه Demo زنده بگیرید", S_OK),
        ("۱۱", "Long-term Memory بین تماس‌ها",
         "aiva/memory/management/commands/aiva_consume_kafka.py · ChatbotUser.memory · aiva/chat/views/session.py",
         "پس از هر تماس یک خلاصه از کاربر ساخته و در تماس بعدی به Context داده می‌شود؛ شماره و Memory در Tracing Span هم ثبت می‌شوند. "
         "برای کارکنان یک تصمیم Privacy است.",
         "اعلام در Privacy Notice یا خاموش‌کردن Consumer برای EX", S_WARN),
        ("۱۲", "Chat APIها بدون Authentication",
         "permission_classes = () در همه Viewهای چت aiva و adcs",
         "امنیت به Gateway سپرده شده. هرکس Session را با شماره دلخواه بسازد، Memory آن شماره را در Context می‌گیرد.",
         "Gateway تنها مسیر ورود در Pilot", S_BAD),
        ("۱۳", "AQA مسیر دوم به هویت",
         "aqa/agents/tools/sql_executor.py — Query آزاد، Read-only فقط با کاربر DB",
         "PRV-02 «هر مسیر دیگر» بازیابی هویت را منع می‌کند؛ AQA می‌تواند ستون شماره را برگرداند.",
         "View بدون ستون هویتی برای کاربر DB مخصوص AQA", S_WARN),
    ]
    for num, title, ev, meaning, action, st in findings:
        find.add([(num, S_NUM), (title, st), (ev, S_MONO), (meaning, S_BASE), (action, st)])

    # ---------------- Sheet 5: معماری ----------------
    arch = Sheet("معماری", [26, 10, 10, 46, 30])
    arch.add([("سرویس‌های فعال پایتون — کامیت در ۳ ماه گذشته", S_TITLE), ("", S_TITLE), ("", S_TITLE), ("", S_TITLE), ("", S_TITLE)], 26)
    arch.add([("", S_BASE)] * 5)
    arch.add([(h, S_HEADER) for h in ("سرویس", "خط کد", "فایل", "نقش", "آخرین کامیت")], 30)
    services = [
        ("python/coa-api", 31596, 325, "لایه سرویس‌دهی CCA — تحلیل، Trend، تیکت، کارشناس، داشبورد IVA، Sync با ClickHouse، آرشیو", "2026-09-27"),
        ("python/agentlib", 19188, 444, "کتابخانه هسته Agent — LLM، ابزار، ReAct، Monitoring. ۱۴۰ فایل تست", "2026-09-27"),
        ("python/aiva", 11492, 121, "مغز چت IVA — Orchestrator رویدادمحور: Guardrail، Intent، Classification، Clarifying، VoiceBridge، ReAct", "2026-09-28"),
        ("python/adcs", 11411, 230, "نسل قبلی/موازی aiva — Chat API، پروکسی ASR/TTS، داشبورد چت، بازخورد", "2026-09-25"),
        ("python/aqa", 9119, 156, "Agentic Query Analyzer — تبدیل زبان طبیعی به SQL روی داده تحلیلی. دارای Eval", "2026-09-27"),
        ("python/chatbot-iva-agent", 5671, 26, "Agent صوتی Realtime روی LiveKit — SIP، VAD، Turn detection، STT/TTS، ضبط، Kafka", "2026-09-28"),
        ("python/adcs-knowledgebase", 4716, 84, "میکروسرویس دانش — CRUD سؤال/پاسخ، Guardrail، Tag، Summarize، Import/Export", "فعال"),
        ("python/adcs-auth", 2610, 67, "احراز هویت مرکزی — صدور JWT. ⚠️ صفر فایل تست", "فعال"),
        ("python/fastlib", 1740, 40, "زیرساخت مشترک FastAPI — لاگ درخواست، پوشش خطا، healthz", "فعال"),
        ("python/aiva-knowledgebase", 730, 17, "میکروسرویس دانش AIVA — Embedding با کلاینت OpenAI-compatible", "فعال"),
        ("golang/grogu", 0, 0, "Ingestion اصلی CCA (Go): Kafka، MinIO، ASR با Circuit Breaker، MyMCI، Upsert در Postgres، Dead-letter", "2026-09-27"),
        ("golang/neurobox-gateway", 0, 0, "Gateway مدل‌های ASR/TTS روی Triton (gRPC)", "2026-09-13"),
        ("golang/websocall", 0, 0, "Voice روی WebSocket برای مرورگر", "2026-09-28"),
        ("golang/dobby", 0, 0, "MCP Server برای Toolهای AIVA", "2026-09-27"),
        ("python/coa-ai", 0, 0, "⚠️ موتور تحلیل (احساسات، خلاصه، موضوع) — خارج از دامنه بررسی، ۱۴ ماه فریز", "2025-07-13"),
    ]
    for name, loc, files, role, commit in services:
        st = S_WARN if name == "python/coa-ai" else S_BASE
        arch.add([
            (name, st), (loc if loc else "—", S_NUM), (files if files else "—", S_NUM),
            (role, st), (commit, S_NUM),
        ])
    arch.add([("", S_BASE)] * 5)
    arch.add([("زیرساخت داده", S_SUBHEAD), ("", S_SUBHEAD), ("", S_SUBHEAD), ("", S_SUBHEAD), ("", S_SUBHEAD)])
    infra = [
        ("PostgreSQL", "۱۹ جدول اصلی: voices، calls، call_ai_tags، call_records، trends، subjects، trend_annotations، tickets، experts …"),
        ("ClickHouse", "منبع نتایج تحلیل؛ چهار Daemon همگام‌سازی: clickhouse_sync، clickhouse_update_sync، failed_calls_sync، sync_canonical_mappings"),
        ("Qdrant (gRPC)", "کالکشن‌های AIVA: guardrail، aiva-contexts، aiva-instructions، aiva-classification، aiva-jokes — آستانه و top-k قابل تنظیم"),
        ("MinIO / S3", "باکت chatbot-mci-iva برای ضبط تماس + مقصد آرشیو pg_dump"),
        ("Kafka", "تولید: chatbot-mci-iva (از Agent صوتی) · مصرف: chatbot-mci-iva-intent (ماژول memory در aiva)"),
        ("مدل‌های LLM", "google/gemma-4-31B-it (میزبانی داخلی) و openai/gpt-oss-120b — هفت نقش مستقل و هرکدام جداگانه قابل تنظیم"),
        ("رصدپذیری", "Prometheus، Elastic APM، Phoenix/OpenTelemetry tracing"),
    ]
    for k, v in infra:
        arch.add([(k, S_BASE), ("", S_BASE), ("", S_BASE), (v, S_BASE), ("", S_BASE)])

    write_workbook([guide, rows_sheet, summ, find, arch], OUT)
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    write_html([guide, rows_sheet, summ, find, arch], rows_sheet, HTML_OUT)
    print(f"wrote {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
