"""Persian content for lane 7 (the agentlib framework). Code refs follow content_en_framework.py."""

from content_fa_framework_p1 import STEPS1
from content_fa_framework_p2 import STEPS2

FRAMEWORK_LANE = {
    "id": "framework", "prefix": "F", "color": "green",
    "short": "7 · فریم‌ورک agentlib",
    "tagline": "باس رویداد، عامل، LLM، بازیابی",
    "title": "7 · agentlib: فریم‌ورک داخلی عامل زیر aiva",
    "title_plain": "7. agentlib: فریم‌ورک عامل زیر aiva",
    "desc": "`agentlib` کتابخانهٔ Python خود تیم برای ساخت عامل‌های چت است. aiva (مسیر 2) روی آن ساخته شده: هر مرحلهٔ aiva یک handler رویداد، عامل یا فراخوانی LLM در agentlib است. این مسیر اجزای سازنده را توضیح می‌دهد، اینکه EX واقعاً چه چیزی استفاده می‌کند و از نسخه‌ای که prod اجرا می‌کند چه چیزی در کتابخانه تغییر کرده است. Prod **agentlib 0.45.0** را اجرا می‌کند (پین‌شده توسط aiva)، با اینکه مخزن از قبل روی 0.47.5 است.",
    "handoff": "منطق مختص aiva که از این قطعه‌ها ساخته شده (intent، clarifying، classification، انتخاب شاخه) در مسیر 2 است. داشبوردهای ردیابی و متریک در مسیر 6 هستند.",
    "steps": ["f-overview", "f-bus", "f-orch-base", "f-orch-guard", "f-context", "f-channels", "f-embedding",
              "f-retrieve", "f-llm", "f-builders", "f-react", "f-guardrail", "f-memory", "f-monitoring",
              "f-plugins", "f-aiva"],
}

FRAMEWORK_STEPS = {**STEPS1, **STEPS2}
assert FRAMEWORK_LANE["steps"] == list(FRAMEWORK_STEPS)
