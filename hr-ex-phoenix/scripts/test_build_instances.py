#!/usr/bin/env python3
"""Tests for the Instances generator. Run: python3 -m unittest scripts/test_build_instances.py"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(APP / "scripts"), str(APP / "content")]

import build_instances as gen  # noqa: E402
import instances_catalog as cat  # noqa: E402

CANARY = "canary-Do-Not-Publish-91"
AGENT = """
agent:
  replicaCount: 3
  image: {{repository: docker.mci.dev/darkube/mci/chatbot/chatbot-iva-agent, tag: v0.40.0}}
  servicemonitor: {{enabled: true}}
  env:
    - {{name: AGENT_STT_CLIENT, value: soniox}}
    - {{name: AGENT_STT_MODEL, value: "http://user:{canary}@10.1.2.3/model"}}
    - {{name: AGENT_TTS_MODEL, value: "10.1.2.3:8000"}}
    - {{name: DATABASE_PASSWORD, value: {canary}}}
    - {{name: SOME_NEW_SETTING, value: {canary}}}
"""


def ops_repo(root: Path, releases: dict[str, str]) -> Path:
    for name, values in releases.items():
        folder = root / "prod" / name
        folder.mkdir(parents=True)
        (folder / "values.yaml").write_text(values, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q",
                    "--allow-empty", "-m", "x"], check=True)
    return root


class Secrets(unittest.TestCase):
    def test_nothing_unsafe_reaches_the_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = gen.build(ops_repo(Path(tmp), {"chatbot-new-iva": AGENT.format(canary=CANARY)}))
        text = json.dumps(snapshot)
        self.assertNotIn(CANARY, text)
        self.assertNotIn("10.1.2.3", text)
        self.assertNotIn("docker.mci.dev", text)
        self.assertNotIn("SOME_NEW_SETTING", text)
        self.assertEqual(snapshot["releases"][0]["config"]["voice"], {"AGENT_STT_CLIENT": "soniox"})

    def test_clean_rejects(self):
        for name, value in [("X", "https://a.b"), ("X", "10.0.0.1"), ("X", "a@b"), ("X", "svc.ns.svc"),
                            ("X", "a.mci.dev"), ("X", "y" * 201), ("MY_PASSWORD", "plain"), ("X", None)]:
            self.assertIsNone(gen.clean(name, value), (name, value))
        self.assertEqual(gen.clean("AGENT_TTS_SPEED", "1.2"), "1.2")

    def test_assert_clean_rejects_each_pattern(self):
        for text in ['"a": "http://x"', '"a": "10.0.0.1"', '"a": "b.mci.dev"', '"a": "eyJhbGciOiJIUzI1NiJ9"',
                     '"DB_PASSWORD": "x"']:
            with self.assertRaises(SystemExit, msg=text):
                cat.assert_clean(text)
        cat.assert_clean('"AGENT_TTS_SPEED": "1.2"')


class Parsing(unittest.TestCase):
    def test_tabs_are_repaired(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "values.yaml"
            path.write_text("a:\n  b: 1\t\n", encoding="utf-8")
            self.assertEqual(gen.load(path), {"a": {"b": 1}})


class Cron(unittest.TestCase):
    def test_a_schedule_with_no_real_date_never_runs(self):
        for schedule in ("0 0 31 2 *", "0 0 30 2 *", "0 0 31 4 *", "0 0 31 6,9 *"):
            self.assertTrue(gen.never_runs(schedule), schedule)

    def test_anything_else_may_run(self):
        for schedule in ("*/5 * * * *", "0 0 1 1 *", "0 0 30 4 *", "0 0 29 2 *", "0 0 31 2 1", "@daily", "0 0 L 2 *"):
            self.assertFalse(gen.never_runs(schedule), schedule)

    def test_component_records_its_schedule(self):
        values = "job:\n  cronjob: true\n  schedule: '0 0 31 2 *'\n  image: {repository: x/y, tag: v1}\n"
        part = gen.components_of(gen.yaml.safe_load(values))[0] if hasattr(gen, "yaml") else None
        if part is None:
            import yaml
            part = gen.components_of(yaml.safe_load(values))[0]
        self.assertEqual((part["schedule"], part["neverRuns"]), ("0 0 31 2 *", True))

    def test_a_job_that_never_runs_does_not_count_as_on(self):
        out = cat.merge({"source": {}, "releases": [{"id": "thing", "companions": [], "config": {"voice": {}, "brain": {}, "data": {}, "campaign": {}}, "deps": [],
            "components": [{"name": "job", "family": "y", "role": "other", "version": "v1", "replicas": None, "autoscaled": False, "metrics": False,
                            "schedule": "0 0 31 2 *", "neverRuns": True}]}]})
        self.assertEqual(out["instances"][0]["state"], "off")


class Config(unittest.TestCase):
    def test_settings_come_from_the_main_brain(self):
        values = """
chatbot:
  replicaCount: 1
  image: {repository: x/adcs-chatbot, tag: v1}
  env: [{name: CONTEXTS_COLLECTION_NAME, value: chat-contexts}]
iva-chatbot:
  replicaCount: 4
  image: {repository: x/aiva, tag: v2}
  env: [{name: CONTEXTS_COLLECTION_NAME, value: phone-contexts}]
"""
        with tempfile.TemporaryDirectory() as tmp:
            release = gen.build(ops_repo(Path(tmp), {"thing": values}))["releases"][0]
        self.assertEqual(release["config"]["brain"]["CONTEXTS_COLLECTION_NAME"], "phone-contexts")


class Classification(unittest.TestCase):
    def merged(self, releases):
        with tempfile.TemporaryDirectory() as tmp:
            return cat.merge(gen.build(ops_repo(Path(tmp), releases)))

    def test_unknown_release_is_shown_not_dropped(self):
        out = self.merged({"brand-new-thing": AGENT.format(canary=CANARY)})
        self.assertEqual([(i["id"], i["category"]) for i in out["instances"]], [("brand-new-thing", "unclassified")])

    def test_zero_replicas_with_autoscaling_is_not_off(self):
        values = "app:\n  replicaCount: 0\n  autoscaling: {enabled: true}\n  image: {repository: x/y, tag: v1}\n"
        self.assertEqual(self.merged({"thing": values})["instances"][0]["state"], "running")

    def test_zero_replicas_is_off(self):
        values = "app:\n  replicaCount: 0\n  image: {repository: x/y, tag: v1}\n"
        self.assertEqual(self.merged({"thing": values})["instances"][0]["state"], "off")


class CommittedSnapshot(unittest.TestCase):
    def setUp(self):
        self.text = (APP / "content" / "instances_snapshot.json").read_text(encoding="utf-8")
        self.snapshot = json.loads(self.text)
        self.merged = cat.merge(self.snapshot)

    def test_is_clean(self):
        cat.assert_clean(self.text)

    def by_id(self):
        return {i["id"]: i for i in self.merged["instances"]}

    def sides(self, iid):
        return {x["kind"] for x in self.by_id()[iid]["surfaces"]}

    def test_every_release_appears_exactly_once(self):
        placed = [r for i in self.merged["instances"] if not i["slice"] for r in i["releases"]]
        placed += [x["id"] for g in self.merged["shared"] for x in g["items"]]
        placed += [r["id"] for r in self.snapshot["releases"] if r.get("companion_of")]
        expected = [r["id"] for r in self.snapshot["releases"]]
        self.assertEqual(sorted(placed), sorted(expected))
        self.assertEqual(len(expected), self.snapshot["source"]["releases"])

    def test_every_part_lands_in_exactly_one_project(self):
        for release in self.snapshot["releases"]:
            names = [c["name"].removeprefix(f"{release['id']}/") for i in self.merged["instances"]
                     for c in i["components"] if c["release"] == release["id"]]
            if names:
                self.assertEqual(sorted(names), sorted(c["name"] for c in release["components"]), release["id"])

    def test_part_names_are_unique_within_a_project(self):
        for inst in self.merged["instances"]:
            names = [c["name"] for c in inst["components"]]
            self.assertEqual(len(names), len(set(names)), inst["id"])

    def test_a_project_has_one_entry_with_its_sides(self):
        self.assertEqual(self.sides("chatbot-ex"), {"panel", "phone", "chatbot"})
        self.assertEqual(self.sides("mci-agentic"), {"panel", "phone", "chatbot"})
        self.assertEqual(self.sides("chatbot-mobinnet-iva"), {"panel", "phone", "chatbot"})
        self.assertEqual(self.sides("chatbot-shaad-iva"), {"panel", "phone"})

    def test_a_project_with_no_voice_route_has_no_phone(self):
        for iid in ("chatbot-complaint", "chatbot-sales-agent", "chatbot-dhd", "chatbot-setare-yek", "chatbot-ewano-new"):
            self.assertEqual(self.sides(iid), {"panel", "chatbot"}, iid)

    def test_each_admin_panel_is_grouped_and_serves_coa_and_cca(self):
        panels = [i for i in self.merged["instances"] if i["category"] == "panel"]
        self.assertEqual(len(panels), 12)
        for project in panels:
            panel = next(x for x in project["surfaces"] if x["kind"] == "panel")
            self.assertEqual(panel["apps"], ["COA", "CCA"], project["id"])
            self.assertTrue(project["config"]["data"], project["id"])

    def test_a_project_keeps_the_settings_of_each_release(self):
        cca = self.by_id()["mci-agentic"]
        self.assertTrue(cca["config"]["voice"])
        self.assertTrue(cca["config"]["data"])
        self.assertEqual(self.by_id()["chatbot-ex"]["config"]["data"]["POSTGRES_DATABASE"], "coa_ex")

    def test_a_panel_connects_to_every_phone_line_it_reads(self):
        by_id = self.by_id()
        self.assertEqual({l["id"] for l in by_id["aiva"]["links"] if l["kind"] == "phone"}, {"aiva-neda", "aiva-poll"})
        self.assertEqual(by_id["aiva-neda"]["links"], [{"id": "aiva", "kind": "panel"}])

    def test_raya_is_split_from_its_release(self):
        by_id = {i["id"]: i for i in self.merged["instances"]}
        campaign, raya = by_id["raya-beta"], by_id["aiva"]
        self.assertTrue(campaign["components"])
        self.assertTrue(all(c["name"].startswith("coa-scoring") for c in campaign["components"]))
        self.assertFalse(any(c["name"].startswith("coa-scoring") for c in raya["components"]))


if __name__ == "__main__":
    unittest.main()
