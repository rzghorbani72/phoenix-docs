#!/usr/bin/env python3
"""Build the documents manifest for the app's Documents library (#/docs).

Walks public/docs and writes src/data/docs.json (generated, gitignored). Files that share a folder
and a stem (PRODUCT_DOSSIER_FA.html + .pdf, FEATURE_CATALOG.md + .html, a .csv + its .docx) become
one entry with several files. Titles come from <title> (html) or the first heading (md), otherwise
from the file name. Curated EN/FA one-liners for the important documents follow README.md and
public/docs/knowledge-base/README.md.

Run directly or through export_json.py (`npm run content`).
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parent
PUBLIC = APP / "public"
DOCS = PUBLIC / "docs"
OUT = APP / "src" / "data" / "docs.json"

CATEGORIES = ["product-management", "technical", "knowledge-base", "requirements", "diagrams"]
TYPES = {"html", "pdf", "md", "csv", "xlsx", "docx", "png", "jpg", "jpeg", "svg", "json"}
# Which file of a twin group opens first (and is previewed).
PRIMARY = ["html", "pdf", "md", "csv", "png", "jpg", "jpeg", "svg", "json", "xlsx", "docx"]
PERSIAN = re.compile(r"[؀-ۿ]")

# The documents a newcomer should open first.
START = {"START_HERE_FA", "README", "README_FA"}

# Curated one-liners, keyed by file stem (README.md tables; knowledge-base/README.md).
DESC: dict[str, tuple[str, str]] = {
    "START_HERE_FA": (
        "Hub page: question-to-document router, map of every file, HR requirements per pipeline stage, sensitive and emergency call handling, AI models and the pilot gate.",
        "صفحهٔ شروع: راهنمای «کدام سؤال، کدام سند»، نقشهٔ همهٔ فایل‌ها، نیازمندی‌های HR در هر مرحلهٔ پایپ‌لاین، تماس‌های حساس و اضطراری، مدل‌ها و دروازهٔ پایلوت.",
    ),
    "HR_TECH_CHECKLIST_FA": (
        "Technical study checklist: which models run where (ASR, LLM, embedding, TTS, VAD), ASR in depth, aiva, COA, the HR Fit-Gap blocks and questions for the team.",
        "چک‌لیست مطالعهٔ فنی: کدام مدل کجا اجرا می‌شود (ASR، LLM، embedding، TTS، VAD)، ASR به تفصیل، aiva، COA، بلوک‌های Fit-Gap و پرسش‌ها برای تیم.",
    ),
    "PRODUCT_DOSSIER_FA": (
        "Product dossier §1–10, §25, §27: feature catalog, Fit-Gap verdict, critical findings, risks, unit economics, scope, competitors and HCM vendors.",
        "پروندهٔ محصول (§۱–۱۰، §۲۵، §۲۷): کاتالوگ قابلیت‌ها، حکم Fit-Gap، یافته‌های بحرانی، ریسک‌ها، اقتصاد واحد، دامنه، رقبا و فروشندگان HCM.",
    ),
    "FIT_GAP_TRACKER": (
        "The 87 agreement rows with code-verified status, evidence, confidence, owner, conditional deadline and action. RTL, filterable, with a live summary sheet.",
        "۸۷ ردیف توافق‌نامه با وضعیت تأییدشده از کد، شاهد، اطمینان، مالک وابستگی، ددلاین شرطی و اقدام؛ راست‌به‌چپ و قابل فیلتر با برگهٔ خلاصهٔ زنده.",
    ),
    "FIT_GAP_TRACKER_FA": (
        "Web view of the Fit-Gap tracker: the 87 agreement rows with code-verified status, evidence and proposed conditional deadlines.",
        "نسخهٔ وب ردیاب Fit-Gap: ۸۷ ردیف توافق‌نامه با وضعیت تأییدشده از کد، شاهد و ددلاین شرطی پیشنهادی.",
    ),
    "ROADMAP_FA": (
        "Decision principles, table stakes vs differentiators, wave roadmap with exit criteria, operating model, technical direction, metrics tree and the first 20 days.",
        "اصول تصمیم‌گیری، الزامات پایه در برابر تمایزها، نقشهٔ راه موجی با معیار خروج، مدل عملیاتی تیم، جهت فنی، درخت شاخص‌ها و ۲۰ روز اول.",
    ),
    "INSPIRATION_PLAYBOOK_FA": (
        "Iranian competitors and foreign inspirations closest to Phoenix: how their key features work, what we have, how to build it; ends with a versioned feature list.",
        "رقبای ایرانی و نمونه‌های خارجی شبیه Phoenix: قابلیت‌های کلیدی‌شان چطور کار می‌کند، ما چه داریم و چطور بسازیم؛ با فهرست قابلیت نسخه‌بندی‌شده.",
    ),
    "MARKET_ALIGNMENT_FA": (
        "MCI Fit-Gap needs translated into market patterns: 9 product building blocks, all 87 rows tagged Generic / Config / MCI-only, access models of global vendors.",
        "ترجمهٔ نیازهای Fit-Gap همراه اول به الگوهای بازار: ۹ بلوک محصول، برچسب Generic / Config / MCI-only برای ۸۷ ردیف و مدل دسترسی فروشندگان جهانی.",
    ),
    "ANSWER_PACK_FA": (
        "Buyer-facing draft answering Chargoon's HR software selection guide: scope tiers, testable criteria, role × data matrix, demo scenario and acceptance criteria.",
        "پیش‌نویس پاسخ به راهنمای انتخاب نرم‌افزار منابع انسانی چارگون: سطوح دامنه، معیارهای آزمون‌پذیر، ماتریس نقش × داده، سناریوی دمو و معیار پذیرش.",
    ),
    "FEATURE_CATALOG": (
        "Master feature list for the EX product: 180 features in 18 domains with need, options, what world leaders do, Phoenix status, priority, effort and release cut R0–R4.",
        "فهرست جامع قابلیت‌های محصول EX: ۱۸۰ قابلیت در ۱۸ حوزه با نیاز، گزینه‌ها، کار رهبران جهانی، وضعیت Phoenix، اولویت، تلاش و برش انتشار R0–R4.",
    ),
    "FEATURE_CATALOG_FA": (
        "Persian translation of the master feature catalog (180 features, 18 domains, key judgments, release cut R0–R4, red lines).",
        "ترجمهٔ فارسی کاتالوگ جامع قابلیت‌ها (۱۸۰ قابلیت، ۱۸ حوزه، قضاوت‌های کلیدی، برش انتشار R0–R4، خطوط قرمز).",
    ),
    "AI_LEARNING_GUIDE_FA": (
        "Plain-Persian guide to staying current in AI: core concepts, reading a model card, benchmarks and pitfalls, voice metrics (WER, RTFx, MOS), leaderboards and a weekly routine.",
        "راهنمای ساده برای به‌روز ماندن در هوش مصنوعی: مفاهیم پایه، خواندن کارت مدل، بنچمارک‌ها و دام‌هایشان، شاخص‌های صوت (WER، RTFx، MOS)، لیدربوردها و روال هفتگی.",
    ),
    "IVA_EX_PROMPT_REQUIREMENTS_FA": (
        "PRD for the EX voice agent: ~70 testable prompt requirements, tool contract, prompt skeleton, 25 eval scenarios, release gate and traceability matrix.",
        "سند نیازمندی ایجنت صدای کارکنان: حدود ۷۰ نیازمندی آزمون‌پذیر پرامپت، قرارداد ابزار، اسکلت پرامپت، ۲۵ سناریوی ارزیابی، دروازهٔ انتشار و ماتریس ردیابی.",
    ),
    "TECHNICAL_DOSSIER_FA": (
        "Technical dossier §11–24: voice AI basics, call path to the agent, repo map, architecture, agentlib, AIVA, IVA, CCA, auth, data model, CI/deploy, tech debt and endpoints.",
        "پروندهٔ فنی (§۱۱–۲۴): مبانی صوت، مسیر تماس تا ایجنت، نقشهٔ مخزن، معماری، agentlib، AIVA، IVA، CCA، احراز هویت، مدل داده، CI/استقرار، بدهی فنی و endpointها.",
    ),
    "IVA_COA_PIPELINES": (
        "Older IVA and COA pipeline walkthrough (MCI defaults as of 2026-10-05); superseded by this app's pipeline map for EX.",
        "مرور قدیمی‌تر پایپ‌لاین‌های IVA و COA (پیش‌فرض‌های همراه اول تا ۱۴۰۵/۰۷/۱۳)؛ برای EX نقشهٔ پایپ‌لاین همین برنامه جایگزین آن است.",
    ),
    "README": (
        "What the knowledge-base folder holds: customer package, sensitive/emergency taxonomy, tones and ready-to-import KB CSVs.",
        "محتوای پوشهٔ پایگاه دانش: بستهٔ مشتری، طبقه‌بندی موضوعات حساس و اضطراری، لحن‌ها و CSVهای آمادهٔ ورود به KB.",
    ),
    "README_FA": (
        "Explains the sensitive / emergency seed data: which file goes to which layer, status (draft for review) and how to import it.",
        "توضیح دادهٔ اولیهٔ موضوعات حساس و اضطراری: هر فایل به کدام لایه می‌رود، وضعیت (پیش‌نویس برای بازبینی) و روش ورود.",
    ),
    "Employee_Voice_Agent_Instruction_v2": (
        "Customer package: the EX voice-agent instruction v2 (CSV in KB import format + Word original).",
        "بستهٔ مشتری: دستورالعمل ایجنت صدای کارکنان نسخهٔ ۲ (CSV با قالب ورود KB و نسخهٔ Word).",
    ),
    "Employee_Voice_Knowledge_Base_v2": (
        "Customer package: the EX knowledge base v2 (Word).",
        "بستهٔ مشتری: پایگاه دانش صدای کارکنان نسخهٔ ۲ (Word).",
    ),
    "taxonomy_v1": ("Sensitive / emergency topic taxonomy.", "طبقه‌بندی موضوعات حساس و اضطراری."),
    "detector_keywords_v1": ("Keywords for the sensitive / emergency detector.", "کلیدواژه‌های آشکارساز موضوعات حساس و اضطراری."),
    "default_features_v1": ("Default features per sensitive / emergency topic.", "قابلیت‌های پیش‌فرض برای هر موضوع حساس و اضطراری."),
    "incident_config_v1": ("Incident routing configuration for sensitive / emergency voices.", "پیکربندی مسیریابی رخداد برای صداهای حساس و اضطراری."),
    "kb_import_v1": ("KB rows for sensitive / emergency topics, ready to import.", "ردیف‌های KB برای موضوعات حساس و اضطراری، آمادهٔ ورود."),
    "behavior_codes_tones_v1": ("Tone variants of the «behavior codes» KB (v1, revised).", "نسخه‌های لحن پایگاه دانش «کدهای رفتاری» (v1، بازبینی‌شده)."),
    "behavior_codes_question_sets_v1": ("Five question sets per tone for the «behavior codes» KB.", "پنج مجموعه سؤال برای «کدهای رفتاری» بر اساس لحن."),
    "behavior_codes_T08_colloquial_v1": ("Behavior codes in tone T08 (colloquial).", "کدهای رفتاری با لحن T08 (محاوره‌ای)."),
    "behavior_codes_tone_samples_v1": ("Tone samples for the behavior codes.", "نمونه‌های لحن برای کدهای رفتاری."),
    "ex_results_1405_kb": ("Ready-to-import KB: EX survey results 1405.", "KB آمادهٔ ورود: نتایج نظرسنجی EX سال ۱۴۰۵."),
    "merged_revised_kb": ("Ready-to-import KB: merged and revised KB (930 lines).", "KB آمادهٔ ورود: KB ادغام و بازبینی‌شده (۹۳۰ خط)."),
    "instruction_14-05": (
        "21,311 lines of telecom customer-service Q&A; origin not documented, so verify before using for EX.",
        "۲۱٬۳۱۱ خط پرسش‌وپاسخ خدمات مشتری مخابراتی؛ منشأ مستند نیست، پیش از استفاده برای EX بررسی شود.",
    ),
    "HR - meet UAT agreement - Fit-Gap MVP": (
        "The UAT agreement Fit-Gap between MCINEXT and MCI's EX department: 87 rows in 8 blocks, verbatim.",
        "Fit-Gap توافق‌نامهٔ UAT میان MCINEXT و ادارهٔ EX همراه اول: ۸۷ ردیف در ۸ بلوک، عین متن.",
    ),
    "Continuous_Listening_MVP_Detailed_FitGap_v1": (
        "Detailed fit-gap for the Continuous Listening MVP.",
        "Fit-Gap تفصیلی MVP شنیدن مستمر (Continuous Listening).",
    ),
    "iva-call-flow_notes": ("Photo of hand-drawn notes: the IVA call flow.", "عکس یادداشت دست‌نویس: جریان تماس IVA."),
    "coa-cca-analysis-flow_notes": ("Photo of hand-drawn notes: the COA/CCA analysis flow.", "عکس یادداشت دست‌نویس: جریان تحلیل COA/CCA."),
    "cca-topic-mapper_notes": ("Photo of hand-drawn notes: the CCA topic mapper.", "عکس یادداشت دست‌نویس: نگاشت‌گر موضوع CCA."),
}


# Names that the generic humanizer gets wrong (acronyms, dashes in the original name).
TITLES = {
    "FIT_GAP_TRACKER": "Fit-Gap tracker (Excel)",
    "HR - meet UAT agreement - Fit-Gap MVP": "HR UAT agreement — Fit-Gap MVP",
    "Continuous_Listening_MVP_Detailed_FitGap_v1": "Continuous Listening MVP — detailed Fit-Gap v1",
    "instruction_14-05": "Instruction 14-05 (telecom Q&A)",
    "ex_results_1405_kb": "EX results 1405 KB",
    "merged_revised_kb": "Merged revised KB",
    "kb_import_v1": "KB import v1",
    "behavior_codes_T08_colloquial_v1": "Behavior codes — T08 colloquial v1",
    "behavior_codes_tone_samples_v1": "Behavior codes — tone samples v1",
    "iva-call-flow_notes": "IVA call flow (notes)",
    "coa-cca-analysis-flow_notes": "COA/CCA analysis flow (notes)",
    "cca-topic-mapper_notes": "CCA topic mapper (notes)",
}


def humanize(stem: str) -> str:
    if stem in TITLES:
        return TITLES[stem]
    s = re.sub(r"[_\-\s]+", " ", stem).strip()
    s = re.sub(r"\bnotes$", "(notes)", s)
    s = re.sub(r"\s+FA$", "", s)
    return s[:1].upper() + s[1:] if s.islower() else s


def read_title(p: Path, ext: str) -> str | None:
    try:
        head = p.read_text(encoding="utf-8", errors="ignore")[:20000]
    except OSError:
        return None
    if ext == "html":
        m = re.search(r"<title>(.*?)</title>", head, re.S | re.I)
        return html.unescape(m.group(1)).strip() if m else None
    if ext == "md":
        m = re.search(r"^#\s+(.+)$", head, re.M)
        return m.group(1).strip() if m else None
    return None


def persian_text(p: Path) -> bool:
    """Text data (csv/md/json) whose first lines are mostly Persian."""
    if p.suffix.lower() not in (".csv", ".md", ".json"):
        return False
    try:
        head = p.read_text(encoding="utf-8", errors="ignore")[:4000]
    except OSError:
        return False
    letters = re.findall(r"[A-Za-z\u0600-\u06FF]", head)
    return bool(letters) and sum(bool(PERSIAN.match(c)) for c in letters) / len(letters) > 0.4


def build() -> list[dict]:
    groups: dict[tuple[str, str], list[Path]] = {}
    for p in sorted(DOCS.rglob("*")):
        if not p.is_file() or p.name.startswith((".", "~")) or p.name.endswith("#"):
            continue
        ext = p.suffix.lower().lstrip(".")
        if ext not in TYPES:
            continue
        groups.setdefault((str(p.parent), p.stem), []).append(p)

    entries = []
    for (_, stem), paths in groups.items():
        paths.sort(key=lambda p: PRIMARY.index(p.suffix.lower().lstrip(".")))
        rel_dir = paths[0].parent.relative_to(DOCS).parts
        category = rel_dir[0] if rel_dir else "other"
        files = [{"path": p.relative_to(PUBLIC).as_posix(), "type": p.suffix.lower().lstrip("."), "size": p.stat().st_size} for p in paths]
        title = TITLES.get(stem) or next((t for p in paths if (t := read_title(p, p.suffix.lower().lstrip(".")))), None) or humanize(stem)
        # FEATURE_CATALOG (EN) pairs .md + .html; the folder README keeps its folder in the title.
        if stem.startswith("README") and len(rel_dir) > 1 and "/" not in title:
            title = f"{title} — {rel_dir[-1]}"
        lang = "fa" if stem.endswith("_FA") or PERSIAN.search(title) or persian_text(paths[0]) else "en"
        en, fa = DESC.get(stem, ("", ""))
        entries.append({
            "id": "/".join(rel_dir + (stem,)),
            "category": category,
            "folder": "/".join(rel_dir[1:]),
            "title": title,
            "lang": lang,
            "start": stem in START,
            "desc": {"en": en, "fa": fa},
            "files": files,
        })
    order = {c: i for i, c in enumerate(CATEGORIES)}
    entries.sort(key=lambda e: (order.get(e["category"], 99), not e["start"], e["folder"], not e["desc"]["en"], e["id"].lower()))
    return entries


def main() -> None:
    entries = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"categories": CATEGORIES, "docs": entries}, ensure_ascii=False, indent=1), encoding="utf-8")
    nfiles = sum(len(e["files"]) for e in entries)
    print(f"docs: {len(entries)} entries, {nfiles} files")


if __name__ == "__main__":
    main()
