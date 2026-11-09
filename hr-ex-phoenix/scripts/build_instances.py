#!/usr/bin/env python3
"""Extract the deployed Phoenix instances from a chatbot-ops checkout.

Writes content/instances_snapshot.json, which is committed: the Docker build has no access to the
ops repository. Run it where the ops checkout exists (scripts/sync_daily.py does):

    npm run instances                      # uses .source-sync/ops-live
    python3 scripts/build_instances.py --ops /path/to/chatbot-ops

values.yaml holds passwords and tokens, so this is an ALLOWLIST: only the fields named here can
reach the snapshot, and each value must also pass clean(). Never widen it to "all env except
secrets". Needs PyYAML, on the sync machine only; the app build does not.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
OUT = APP / "content" / "instances_snapshot.json"
sys.path.insert(0, str(APP / "content"))
from instances_catalog import PROJECT_RELEASES, shared_group  # noqa: E402

# What each image does. Anything else is "other".
ROLES = {
    "voice": {"chatbot-iva-agent"},
    "brain": {"aiva", "aiva-poll", "adcs-chatbot", "chatbot-iva-api", "chatbot-mci-api", "chatbot-mci-survey",
              "chatbot-mci-arabic-api", "chatbot-mci-english-api", "chatbot-mobinnet-api", "chatbot-ewano-api",
              "chatbot-tejarat-api", "chatbot-telecom-api", "chatbot-xperix-assistant-api", "chatbot-service",
              "mci-general-chatbot", "chatbot-mymci-redirector-api"},
    "knowledge": {"adcs-kb", "aiva-knowledgebase"},
    "analytics": {"coa-api", "coa-api-archive-old-calls", "coa-ai", "grogu", "coa-scoring"},
    "media": {"egress", "websocall", "websocall-ui", "vector", "synapse"},
    "auth": {"adcs-auth"},
    "gateway": {"envoy", "ratelimit", "nginx"},
    "cache": {"redis"},
    "ui": {"chatbot-lib-ui", "agent-ui", "iva-front", "mci", "chatbot", "frontend", "ewano", "mobinnet", "telecom", "agent"},
}
ROLE_OF = {image: role for role, images in ROLES.items() for image in images}
# When a release has several brains, the phone-facing, newest one describes it.
BRAIN_ORDER = ["aiva", "aiva-poll", "chatbot-iva-api", "adcs-chatbot", "chatbot-mci-survey"]

VOICE_KEYS = (
    "AGENT_GREETING_MESSAGE", "AGENT_GREETING_ALLOW_INTERRUPTION", "AGENT_STT_CLIENT", "AGENT_STT_MODEL",
    "AGENT_TTS_MODEL", "AGENT_TTS_SPEED", "AGENT_TURN_MODEL", "AGENT_MIN_ENDPOINTING_DELAY",
    "AGENT_MAX_ENDPOINTING_DELAY", "AGENT_MIN_INTERRUPTION_DURATION", "AGENT_VAD_MIN_SILENCE_DURATION",
    "AGENT_VAD_PREFIX_PADDING_DURATION", "AGENT_NUM_IDLE_PROCESSES", "AGENT_SIP_RTP_STABILIZATION_DELAY",
    "AGENT_APM_TRANSACTION_SAMPLE_RATE", "AGENT_KAFKA_TOPIC",
)
BRAIN_KEYS = (
    "AGENT_LLM_MODEL", "AGENT_ENABLED_TOOLS", "CONTEXTS_COLLECTION_NAME", "GUARDRAIL_COLLECTION_NAME",
    "INSTRUCTIONS_COLLECTION_NAME", "IVA_CONTEXTS_COLLECTION_NAME", "VOICE_BRIDGE_ENABLED",
    "CONTEXTS_FILTER_LLM_ENABLED", "PHOENIX_PROJECT_NAME",
)
DATA_KEYS = (
    "POSTGRES_DATABASE", "CLICKHOUSE_DATABASE", "KAFKA_CALL_TOPIC", "KAFKA_TELC_CALL_TOPIC",
    "KAFKA_CALL_ASR_TOPIC", "KAFKA_IVA_TOPIC", "KAFKA_TICKET_TOPIC", "MINIO_BUCKET_NAME",
    "MINIO_IVA_BUCKET_NAME",
)
CAMPAIGN_KEYS = ("CAMPAIGN_CODE", "CAMPAIGN_NAME", "CAMPAIGN_END_AT", "SCORING_AGENT_ID", "AI_AGENT")

SECRET_NAME = re.compile(r"pass|secret|token|api_?key|credential|dsn|cookie|private", re.I)
UNSAFE_VALUE = re.compile(
    r"://|\b\d{1,3}(?:\.\d{1,3}){3}\b|@|\.mci\.dev|\.svc\b|\bey[A-Za-z0-9_-]{10,}|\b(?:sk|gh[ps]|glpat)[-_][A-Za-z0-9]{8,}")
PLACEHOLDER = {"", "-", "unknown", "none", "null"}
MAX_VALUE = 200


def clean(name: str, value: object) -> str | None:
    """The value if it is safe to publish, else None."""
    if value is None or isinstance(value, (dict, list)):
        return None
    text = str(value).strip()
    if text.lower() in PLACEHOLDER or SECRET_NAME.search(name):
        return None
    if len(text) > MAX_VALUE or UNSAFE_VALUE.search(text):
        return None
    return text


def load(path: Path):
    """Parse a values file. Some contain tabs that strict YAML rejects, though Helm tolerates them."""
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8").replace("\t", "  "))


def env_of(component: dict) -> dict[str, object]:
    env = component.get("env") or component.get("envs") or []
    if isinstance(env, dict):
        return dict(env)
    return {e["name"]: e.get("value") for e in env if isinstance(e, dict) and "name" in e}


def version(tag: object) -> str:
    """Release tags stay as they are; commit tags are cut to 8 characters."""
    text = str(tag or "")
    return text if text.startswith("v") else text[:8]


DAYS_IN_MONTH = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
CRON_SAFE = re.compile(r"^[\d*/,\- ]{1,40}$")


def never_runs(schedule: str) -> bool:
    """True when a cron schedule names only dates that do not exist, like 31 February.

    That is a common way to keep a job defined but switched off. Anything this cannot read
    with certainty counts as "may run", so a real schedule is never reported as dormant.
    """
    fields = schedule.split()
    if len(fields) != 5 or fields[4] not in ("*", "?"):
        return False
    numbers = [re.fullmatch(r"\d+(,\d+)*", f) and [int(x) for x in f.split(",")] for f in fields[2:4]]
    if not all(numbers):
        return False
    days, months = numbers
    return all(day > DAYS_IN_MONTH.get(month, 0) for month in months for day in days)


def components_of(values: dict) -> list[dict]:
    out = []
    for name, comp in values.items():
        if not isinstance(comp, dict) or not comp.get("image"):
            continue
        image = comp["image"] if isinstance(comp["image"], dict) else {}
        family = str(image.get("repository", "")).rsplit("/", 1)[-1]
        replicas = comp.get("replicaCount")
        autoscaling = comp.get("autoscaling") or comp.get("hpa") or {}
        schedule = comp.get("schedule") if comp.get("cronjob") else None
        schedule = schedule.strip() if isinstance(schedule, str) and CRON_SAFE.match(schedule) else None
        out.append({
            "name": name, "family": family, "role": ROLE_OF.get(family, "other"),
            "version": version(image.get("tag")),
            "replicas": replicas if isinstance(replicas, int) else None,
            "autoscaled": bool(isinstance(autoscaling, dict) and autoscaling.get("enabled")),
            "metrics": bool((comp.get("servicemonitor") or {}).get("enabled")),
            **({"schedule": schedule, "neverRuns": never_runs(schedule)} if schedule else {}),
        })
    return out


def config_of(values: dict, components: list[dict]) -> dict:
    """Allowlisted settings only, grouped. On conflict, the main brain wins, then parts that are on.

    A release can hold two brains with different values, such as a chat one and a phone one, so the
    order here decides which instance's truth is shown.
    """
    brain = brain_of(components)
    main = brain["component"] if brain else None

    def take(keys, roles):
        got = {}
        ordered = sorted(components, key=lambda c: (c["name"] != main, c["replicas"] == 0))
        for comp in ordered:
            if comp["role"] not in roles:
                continue
            env = env_of(values[comp["name"]])
            for key in keys:
                if key not in got and key in env:
                    safe = clean(key, env[key])
                    if safe is not None:
                        got[key] = safe
        return got

    return {"voice": take(VOICE_KEYS, {"voice"}), "brain": take(BRAIN_KEYS, {"brain"}),
            "data": take(DATA_KEYS, {"analytics"}), "campaign": take(CAMPAIGN_KEYS, {"analytics"})}


def iva_topics(values: dict, components: list[dict]) -> list[str]:
    """Every assistant-session topic the analytics parts read, which ties a dashboard to its phone line."""
    found = {clean("KAFKA_IVA_TOPIC", env_of(values[c["name"]]).get("KAFKA_IVA_TOPIC"))
             for c in components if c["role"] == "analytics"}
    return sorted(t for t in found if t)


def strings_in(node: object):
    if isinstance(node, dict):
        for value in node.values():
            yield from strings_in(value)
    elif isinstance(node, list):
        for value in node:
            yield from strings_in(value)
    elif isinstance(node, str):
        yield node


def panel_apps(values: dict, components: list[dict]) -> list[str]:
    """What the release's admin panel serves, read from the routes of its gateways. Records labels only."""
    if not any(c["family"] == "agent-ui" for c in components):
        return []
    routes = "\n".join(s for c in components if c["role"] == "gateway" for s in strings_in(values[c["name"]]))
    return ["COA", "CCA"] if re.search(r"proxy_pass\s+https?://[^/;\s]*cca", routes) else ["COA"]


def brain_of(components: list[dict]) -> dict | None:
    brains = [c for c in components if c["role"] == "brain"]
    if not brains:
        return None
    rank = lambda c: (c["replicas"] == 0,
                      BRAIN_ORDER.index(c["family"]) if c["family"] in BRAIN_ORDER else len(BRAIN_ORDER))
    best = sorted(brains, key=rank)[0]
    return {"family": best["family"], "version": best["version"], "component": best["name"]}


def deps_of(values: dict, shared_ids: list[str]) -> list[str]:
    """Shared releases this one calls, found by name in its service addresses."""
    blob = []
    for comp in values.values():
        if isinstance(comp, dict):
            blob += [str(v) for v in env_of(comp).values() if v is not None]
    text = "\n".join(blob)
    return sorted(s for s in shared_ids if re.search(rf"(?<![\w-]){re.escape(s)}(?![\w-])", text))


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, check=True).stdout.strip()


def build(ops: Path) -> dict:
    prod = ops / "prod"
    if not prod.is_dir():
        raise SystemExit(f"No prod/ folder in {ops}. Is this a chatbot-ops prod checkout?")
    ids = sorted(p.name for p in prod.iterdir() if p.is_dir())
    shared_ids = [r for r in ids if r not in PROJECT_RELEASES and shared_group(r)]
    releases = []
    for rid in ids:
        path = prod / rid / "values.yaml"
        values = load(path) if path.exists() else None
        if not isinstance(values, dict):
            values = {}  # exporters and similar: plain manifests, listed by name only
        components = components_of(values)
        release = {"id": rid, "components": components, "companions": [],
                   "config": config_of(values, components), "deps": deps_of(values, shared_ids)}
        brain = brain_of(components)
        if brain:
            release["brain"] = brain
        release["ivaTopics"] = iva_topics(values, components)
        release["panelApps"] = panel_apps(values, components)
        releases.append(release)
    by_id = {r["id"]: r for r in releases}
    for release in releases:
        rid = release["id"]
        if rid.endswith("-gw") and rid[:-3] in by_id and rid[:-3] in PROJECT_RELEASES:
            release["companion_of"] = rid[:-3]
            by_id[rid[:-3]]["companions"].append(rid)
    return {
        "source": {"repo": "chatbot-ops", "branch": "prod", "commit": git(ops, "rev-parse", "--short=8", "HEAD"),
                   "date": git(ops, "log", "-1", "--format=%cs"), "releases": len(ids)},
        "releases": releases,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ops", type=Path, default=APP / ".source-sync" / "ops-live")
    args = parser.parse_args()
    snapshot = build(args.ops)
    OUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"instances: {snapshot['source']['releases']} releases at {snapshot['source']['commit']} -> {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
