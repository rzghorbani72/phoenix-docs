#!/usr/bin/env python3
"""Human names for the Helm releases in chatbot-ops, and how they group into instances.

This is the curated half of the Instances section. scripts/build_instances.py extracts the facts
from chatbot-ops into instances_snapshot.json; merge() adds the names below at build time, so a
rename needs no access to the ops repository.

Rules for names:
- Say what the thing is, for someone who has never seen the release name.
- `confirm: True` means the name is a reading of the config, not a fact. The app shows it with a
  "name to confirm" mark. Remove the flag once the owner of the instance has confirmed it.
- One entry is one project. `release` and `also` name the Helm releases it spans, the first winning
  when two set the same setting. Its admin panel, phone line and chatbot are worked out from the
  parts ops really deploys, so a project is never listed twice.
- A new release that is neither here nor matched by SHARED_RULES shows up as "unclassified" in the
  app. It never disappears silently.
"""

from __future__ import annotations

import re

PANEL, PHONE, CHAT, CAMPAIGN, TOOLS, UNCLASSIFIED = (
    "panel", "phone", "chat", "campaign", "tools", "unclassified",
)


def entry(category, en, fa, about_en, about_fa, **extra):
    return {"category": category, "name": {"en": en, "fa": fa},
            "about": {"en": about_en, "fa": about_fa}, **extra}


CATALOG = {
    # --- Phone assistants -------------------------------------------------------------------
    "chatbot-ex": entry(
        PHONE, "Employee Voice (EX)", "صدای کارکنان (EX)",
        "Where employees give feedback, by phone or chat.",
        "محل دریافت بازخورد کارکنان، با تماس تلفنی یا چت."),
    "aiva": entry(
        PHONE, "Raya Personal Assistant", "دستیار شخصی رایا",
        "Personal phone assistant with memory. Hosts the Raya beta campaign.",
        "دستیار تلفنی شخصی با حافظه. کمپین بتای رایا هم روی همین استقرار است.",
        confirm=True, exclude_prefix="coa-scoring"),
    "aiva-neda": entry(
        PHONE, "Neda Assistant", "دستیار ندا",
        "Assistant on phone, SMS and Bale.",
        "دستیار روی تلفن، پیامک و بله.",
        confirm=True),
    "aiva-poll": entry(
        PHONE, "Phone Survey Bot", "ربات نظرسنجی تلفنی",
        "Calls run a short spoken survey, one question at a time.",
        "در تماس یک نظرسنجی کوتاه گفتاری، سؤال به سؤال اجرا می‌شود."),
    "chatbot-mobinnet-iva": entry(
        PHONE, "Mobinnet", "مبین‌نت",
        "Assistant for Mobinnet customers.",
        "دستیار مشتریان مبین‌نت.",
        also=["chatbot-mobinnet"], confirm=True),
    "chatbot-rubika-iva": entry(
        PHONE, "Rubika", "روبیکا",
        "Assistant for Rubika.",
        "دستیار روبیکا.",
        also=["chatbot-rubika"], confirm=True),
    "chatbot-shaad-iva": entry(
        PHONE, "Shad", "شاد",
        "Assistant for Shad.",
        "دستیار شاد."),
    "chatbot-front-iva": entry(
        PHONE, "Front Phone Assistant", "دستیار تلفنی فرانت",
        "Phone assistant on its own stack. The config does not say who it serves.",
        "دستیار تلفنی روی استقرار مستقل. در پیکربندی نیامده مخاطبش کیست.",
        confirm=True),
    "chatbot-mci-survey": entry(
        PHONE, "MCI Customer Survey", "نظرسنجی مشتریان همراه اول",
        "Survey over web calls.",
        "نظرسنجی از طریق تماس وب."),

    # --- The assistant of the CCA app. Its dashboard is in COA_APPS. ---------------------------
    "mci-agentic": entry(
        CHAT, "CCA", "CCA",
        "Customer care for MCI. Its panel is the main COA panel and reads this phone line.",
        "خدمات مشتریان همراه اول. پنل آن پنل اصلی COA است و همین خط تلفنی را می‌خواند.",
        release="chatbot-mci-iva", also=["mci-agentic"], confirm=True),

    # --- Campaigns (a part of a release, shown on its own) -----------------------------------
    "raya-beta": entry(
        CAMPAIGN, "Raya Beta Campaign", "کمپین بتای رایا",
        "Scoring and rewards for Raya beta users. Runs inside the Raya deployment.",
        "امتیازدهی و جایزه برای کاربران بتای رایا. درون استقرار رایا اجرا می‌شود.",
        release="aiva", only_prefix="coa-scoring"),

    # --- Chat assistants with an analytics panel ---------------------------------------------
    "chatbot-complaint": entry(
        CHAT, "Complaints Assistant", "دستیار شکایات",
        "Assistant with a knowledge base for complaints.",
        "دستیار با پایگاه دانش برای شکایات."),
    "chatbot-sales-agent": entry(
        CHAT, "Sales Assistant", "دستیار فروش",
        "Assistant with a knowledge base for sales.",
        "دستیار با پایگاه دانش برای فروش."),
    "chatbot-dhd": entry(
        CHAT, "DHD Assistant", "دستیار DHD",
        "Assistant with a knowledge base. The config does not expand DHD.",
        "دستیار با پایگاه دانش. معنی DHD در پیکربندی نیامده.",
        confirm=True),
    "chatbot-setare-yek": entry(
        CHAT, "Setare Yek Assistant", "دستیار ستاره یک",
        "Assistant with a knowledge base.",
        "دستیار با پایگاه دانش.",
        confirm=True),
    "chatbot-ewano-new": entry(
        CHAT, "Ewano", "ایوانو",
        "Assistant for Ewano. The old and the new chatbot both run.",
        "دستیار ایوانو. چت‌بات قدیمی و جدید هر دو در حال اجرا هستند.",
        also=["chatbot-ewano"], confirm=True),

    # --- Chat assistants ---------------------------------------------------------------------
    "chatbot-mci": entry(CHAT, "MCI Chatbot", "چت‌بات همراه اول",
                         "Main MCI customer chatbot.", "چت‌بات اصلی مشتریان همراه اول.", also=["chatbot-mci-clone", "chatbot-mci-fa", "chatbot-mci-en", "chatbot-mci-ar", "chatbot-mci-multilingual"]),
    "chatbot-mci-sms": entry(CHAT, "MCI SMS Assistant", "دستیار پیامکی همراه اول",
                             "Answers customers over SMS.", "پاسخ به مشتریان از طریق پیامک."),
    "chatbot-mci-general": entry(CHAT, "MCI General Chatbot", "چت‌بات عمومی همراه اول",
                                 "General-purpose MCI chatbot.", "چت‌بات عمومی همراه اول."),
    "chatbot-mci-agent-chat": entry(
        CHAT, "MCI Agent Chat", "چت کارشناس همراه اول",
        "Chat product with its own agent screen and user registration.",
        "محصول چت با صفحهٔ کارشناس و ثبت‌نام کاربر.", confirm=True),
    "chatbot-mci-telecom": entry(CHAT, "MCI Telecom Chatbot", "چت‌بات مخابراتی همراه اول",
                                 "Telecom-focused MCI chatbot.", "چت‌بات همراه اول با تمرکز بر خدمات مخابراتی."),
    "chatbot-mcymci-redirector": entry(CHAT, "MyMCI Assistant Redirector", "مسیریاب دستیار همراه من",
                                       "Sends MyMCI users to the right assistant.", "کاربران همراه من را به دستیار مناسب می‌فرستد."),
    "chatbot-arbaeen": entry(CHAT, "Arbaeen Assistant", "دستیار اربعین",
                             "Seasonal Arbaeen assistant.", "دستیار مناسبتی اربعین.", also=["chatbot-mymci-arbaeen"]),
    "chatbot-bale": entry(CHAT, "Bale Bot", "ربات بله",
                          "Assistant on the Bale messenger.", "دستیار در پیام‌رسان بله."),
    "chatbot-tejarat": entry(CHAT, "Tejarat Bank Assistant", "دستیار بانک تجارت",
                             "Chatbot for Tejarat Bank.", "چت‌بات بانک تجارت.", also=["chatbot-tejarat-local", "chatbot-tejarat-temp"]),
    "chatbot-telecom": entry(CHAT, "Telecom Chatbot", "چت‌بات مخابرات",
                             "Telecom chatbot.", "چت‌بات مخابرات.", confirm=True),
    "chatbot-xperix-assistant": entry(CHAT, "Xperix Assistant", "دستیار اکسپریکس",
                                      "Assistant for Xperix.", "دستیار اکسپریکس."),
    "chatbot-xperix-crm": entry(CHAT, "Xperix CRM", "CRM اکسپریکس",
                                "CRM side of Xperix.", "بخش CRM اکسپریکس."),
    "chatbot-judiciary": entry(CHAT, "Judiciary Assistant", "دستیار قوهٔ قضاییه",
                               "Judiciary assistant.", "دستیار قوهٔ قضاییه."),
    "chatbot-revolution": entry(CHAT, "Revolution Assistant", "دستیار انقلاب",
                                "Revolution assistant.", "دستیار انقلاب.", confirm=True),
    "chatbot-dual-agent": entry(CHAT, "Dual Agent Chat", "چت دوعاملی",
                                "Chat screen with two agents.", "صفحهٔ چت با دو عامل.", confirm=True),

    # --- Internal tools, demos and tests -----------------------------------------------------
    "aqa": entry(TOOLS, "Ask-Your-Data Analyst", "تحلیل‌گر پرسش از داده",
                 "Asks analytics questions in plain language (AQA).", "پرسش تحلیلی به زبان ساده از داده (AQA)."),
    "aiva-aqa": entry(TOOLS, "Ask-Your-Data Analyst, AIVA", "تحلیل‌گر پرسش از داده، AIVA",
                      "AQA pointed at AIVA data.", "AQA روی دادهٔ AIVA."),
    "aqa-backoffice": entry(TOOLS, "Analyst Back Office", "پیشخوان تحلیل‌گر",
                            "Manages AQA prompts and examples.", "مدیریت پرامپت‌ها و نمونه‌های AQA."),
    "sentiment-analysis": entry(TOOLS, "Sentiment Analysis", "تحلیل احساسات",
                                "Sentiment analysis service with its own screen.", "سرویس تحلیل احساسات با صفحهٔ مستقل."),
    "mci-navigator": entry(TOOLS, "MCI Navigator", "راهنمای همراه اول",
                           "Navigator assistant with a chat screen.", "دستیار راهنما با صفحهٔ چت.", confirm=True),
    "se-agent": entry(TOOLS, "SE Agent", "عامل SE",
                      "Internal agent application.", "برنامهٔ عامل داخلی.", confirm=True),
    "hrm": entry(TOOLS, "HRM (Odoo)", "منابع انسانی (Odoo)",
                 "Odoo application for human-resources work.", "برنامهٔ Odoo برای منابع انسانی."),
    "zazu": entry(TOOLS, "Zazu", "زازو",
                  "Internal service. The config does not describe it.", "سرویس داخلی. در پیکربندی توضیحی ندارد.",
                  confirm=True),
    "iva-record": entry(TOOLS, "Voice Sample Recorder", "ضبط نمونهٔ صدا",
                        "Phone line that asks callers to repeat text, to collect voice samples.",
                        "خط تلفنی که از تماس‌گیرنده می‌خواهد متن را تکرار کند تا نمونهٔ صدا جمع شود."),
    "demo-iva-sales": entry(TOOLS, "Sales Phone Demo", "دموی تلفنی فروش",
                            "Demo of a sales phone assistant.", "دموی دستیار تلفنی فروش."),
    "chatbot-mci-iva-load-test": entry(TOOLS, "Phone Load Test", "آزمون بار تلفن",
                                       "Load-test copy of the MCI phone assistant.", "نسخهٔ آزمون بار دستیار تلفنی همراه اول."),
    "chatbot-mci-iva-avatar": entry(TOOLS, "Avatar Assistant, Persian", "دستیار آواتار فارسی",
                                    "Talking-avatar version of the phone assistant.", "نسخهٔ آواتار سخن‌گو از دستیار تلفنی.", also=["chatbot-mci-english-iva-avatar"]),
}

# One panel per project: the agent-ui, its gateway and the COA services behind it.
PANEL_PARTS = r"^(coa-(?!scoring)|grogu|general-ai|dashboard-cache|syncer|ch-update-syncer|trends-syncer|archive-old-calls|ticket-upload)"
SURFACES = ("panel", "phone", "chatbot")
# Every release a project covers, whether it is the entry itself or listed in `also`.
PROJECT_RELEASES = {r for iid, spec in CATALOG.items() for r in (spec.get("release", iid), *spec.get("also", ()))}


# Everything an instance leans on. First match wins; order matters.
SHARED_RULES = [
    ("models", r"^(gemma|gpt-oss|qwen|hakim-|chatbot-custom-embedding|model-respository)"),
    ("gateways", r"(-gw|-lb|gateway.*|-ratelimiter|^openai-trtllm)$"),
    ("data", r"^(chatbot-postgres|chatbot-qdrant|qdrant-backup|prompt-inventory)"),
    ("observability", r"(exporter|monitoring|^chatbot-alerts|^chatbot-phoenix|^ewano-ping)"),
    ("platform", r"^(auth-system|chatbot-audio-wrapper|chatbot-sms-wrapper|chatbot-magika|chatbot-ray|ray-|"
                 r"web-search|tts-service|front$|chatbot-service|chatbot-ui|chatbot-golang|"
                 r"chatbot-feedback-service|chatbot-generator-service)"),
]
SHARED_NAMES = {
    "models": {"en": "Model serving", "fa": "سرو مدل"},
    "gateways": {"en": "Gateways and load balancers", "fa": "درگاه‌ها و توزیع بار"},
    "data": {"en": "Shared data stores", "fa": "پایگاه‌های دادهٔ مشترک"},
    "observability": {"en": "Monitoring", "fa": "پایش"},
    "platform": {"en": "Platform services", "fa": "سرویس‌های پلتفرم"},
}


UNSAFE_SNAPSHOT = {
    "URL": r"[a-z][a-z0-9+.-]*://",
    "IP address": r"\b\d{1,3}(?:\.\d{1,3}){3}\b",
    "internal hostname": r"\.mci\.dev|\.svc\b",
    "credential": r"\beyJ[A-Za-z0-9_-]{10,}|\b(?:sk|gh[ps]|glpat)[-_][A-Za-z0-9]{8,}",
    "secret key": r'"[A-Z0-9_]*(?:PASSWORD|SECRET|TOKEN|API_KEY|CREDENTIAL)[A-Z0-9_]*"',
}


def shared_group(release: str) -> str | None:
    for group, pattern in SHARED_RULES:
        if re.search(pattern, release):
            return group
    return None


def _pick(components, spec):
    """The components of a release that belong to this instance."""
    if spec.get("only_prefix"):
        return [c for c in components if c["name"].startswith(spec["only_prefix"])]
    if spec.get("exclude_prefix"):
        return [c for c in components if not c["name"].startswith(spec["exclude_prefix"])]
    return components


def _state(components) -> str:
    main = [c for c in components if c["role"] not in ("gateway", "cache", "ui")] or components
    # No replicaCount means the chart default or a cron job, and an autoscaled component may
    # legitimately say 0, so neither counts as off. A job whose schedule never fires is off.
    on = [c for c in main if (c["replicas"] is None or c["replicas"] > 0 or c["autoscaled"]) and not c.get("neverRuns")]
    if not on:
        return "off"
    return "running" if len(on) == len(main) else "partial"


def assert_clean(snapshot_text: str) -> None:
    """Last line of defence, run by every build: CI runs no tests, so this is what stops a leak."""
    for label, pattern in UNSAFE_SNAPSHOT.items():
        hit = re.search(pattern, snapshot_text)
        if hit:
            at = snapshot_text.count("\n", 0, hit.start()) + 1
            raise SystemExit(f"instances_snapshot.json line {at} looks like a {label}. Fix build_instances.py.")


def _surface(component, rid, parts) -> str:
    """Which side of a project a deployed part serves."""
    if any(c["family"] == "agent-ui" for c in parts) and re.search(PANEL_PARTS, component["name"]):
        return "panel"
    if component["role"] in ("gateway", "auth", "cache") or component["family"] == "hodor":
        return "base"
    if rid.endswith("-iva") or rid.startswith("aiva"):
        return "phone"
    if component["role"] in ("voice", "media") or component["name"].startswith("iva"):
        return "phone"
    return "chatbot"


def _parts(release, spec, primary):
    """A release's parts, each marked with its side. Later releases of a project keep names unique."""
    rid = release["id"]
    return [{**c, "name": c["name"] if primary else f"{rid}/{c['name']}", "release": rid,
             "surface": _surface(c, rid, release["components"])} for c in _pick(release["components"], spec)]


def _surfaces(components, category, members) -> list[dict]:
    if category in (TOOLS, CAMPAIGN):
        return []
    found = []
    for kind in SURFACES:
        parts = [c for c in components if c["surface"] == kind]
        if parts:
            apps = sorted({a for m in members for a in m.get("panelApps", [])}, key=("COA", "CCA").index)
            found.append({"kind": kind, "state": _state(parts), "parts": [c["name"] for c in parts],
                          "releases": sorted({c["release"] for c in parts}), **({"apps": apps} if kind == "panel" else {})})
    return found


def _connect(instances, releases) -> None:
    """A panel can read phone lines deployed elsewhere: the topics its analytics parts consume."""
    has = lambda inst, kind: any(x["kind"] == kind for x in inst["surfaces"])
    for owner in [i for i in instances if has(i, "panel")]:
        topics = {t for r in owner["releases"] for t in releases[r].get("ivaTopics", [])}
        for other in instances:
            if other is owner or has(other, "panel") or not has(other, "phone"):
                continue
            if other["config"]["voice"].get("AGENT_KAFKA_TOPIC") in topics or other["release"] in topics:
                owner["links"].append({"id": other["id"], "kind": "phone"})
                other["links"].append({"id": owner["id"], "kind": "panel"})


def _combine(configs) -> dict:
    return {group: {k: v for config in reversed(configs) for k, v in config[group].items()} for group in configs[0]}


def merge(snapshot: dict) -> dict:
    """Join the ops facts with the curated names into what the app reads."""
    releases = {r["id"]: r for r in snapshot["releases"]}
    instances, used = [], set()
    for iid, spec in CATALOG.items():
        members = [releases[r] for r in (spec.get("release", iid), *spec.get("also", ())) if r in releases]
        if not members:
            continue  # retired from ops: the catalog entry is simply unused
        used.update(m["id"] for m in members)
        comps = [c for n, m in enumerate(members) for c in _parts(m, spec, n == 0)]
        part = bool(spec.get("only_prefix"))  # a slice of a release has none of its stack-wide settings
        config = _combine([m["config"] for m in members])
        if spec.get("exclude_prefix"):  # the campaign settings belong to the part that was split off
            config = {**config, "campaign": {}}
        surfaces = _surfaces(comps, spec["category"], members)
        category = PANEL if any(x["kind"] == "panel" for x in surfaces) else spec["category"]
        instances.append({
            "id": iid, "release": members[0]["id"], "releases": [m["id"] for m in members], "category": category,
            "name": spec["name"], "about": spec["about"], "confirm": bool(spec.get("confirm")), "state": _state(comps),
            "components": comps, "companions": [] if part else sorted({x for m in members for x in m.get("companions", [])}),
            "config": {"voice": {}, "brain": {}, "data": {}, "campaign": config["campaign"]} if part else config,
            "deps": [] if part else sorted({x for m in members for x in m["deps"]}),
            "brain": None if part else next((m["brain"] for m in members if m.get("brain")), None),
            "slice": part, "surfaces": surfaces, "links": [],
        })
    _connect(instances, releases)
    shared = {g: [] for g in SHARED_NAMES}
    for rid, release in releases.items():
        if rid in used or release.get("companion_of"):
            continue
        group = shared_group(rid)
        if group:
            users = sorted({i["id"] for i in instances if rid in i["deps"]})
            shared[group].append({"id": rid, "usedBy": users, "state": _state(release["components"])
                                  if release["components"] else "running"})
        else:
            comps = _parts(release, {}, True)
            instances.append({
                "id": rid, "release": rid, "releases": [rid], "category": UNCLASSIFIED,
                "name": {"en": rid, "fa": rid}, "about": {"en": "", "fa": ""}, "confirm": True,
                "state": _state(comps) if comps else "running",
                "components": comps, "companions": [], "config": release["config"],
                "deps": release["deps"], "brain": release.get("brain"), "slice": False,
                "surfaces": _surfaces(comps, UNCLASSIFIED, [release]), "links": [],
            })
    return {
        "source": snapshot["source"],
        "instances": instances,
        "shared": [{"group": g, "name": SHARED_NAMES[g], "items": shared[g]} for g in SHARED_NAMES],
    }
