#!/usr/bin/env python3
"""Pull Phoenix and chatbot-ops daily, ask local Codex to refresh the EX docs when needed.

The repositories are cached under .source-sync/ (ignored). Codex is instructed to edit only the
documentation app, never the source repositories. The script rebuilds generated app data and the
Draw.io diagram after a successful review. It does not commit or push changes.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
WORKSPACE = APP  # the app is its own git repository
CACHE = APP / ".source-sync"
STATE = CACHE / "state.json"
RESULT = CACHE / "changed-docs.json"
LOG = CACHE / "sync.log"
SOURCES = {
    "phoenix": {
        "url": "git@git.mci.dev:mse/sre/phoenix.git",
        "branch": "main",
        "cache": "phoenix-live",
        "documented": "7b7c602eba4543a38a01932d8e84cb8459713d0b",
    },
    "chatbot-ops": {
        "url": "git@git.mci.dev:chatbot/chatbot-ops.git",
        "branch": "prod",
        "cache": "ops-live",
        "documented": "dd851385e",
    },
}


RUNTIME_DIAGRAMS = {"aiva": "aiva-runtime.html", "aiva-poll": "aiva-poll-runtime.html"}


def run(args: list[str], *, cwd: Path | None = None, check: bool = True) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(args)}\n"
            f"{result.stdout}{result.stderr}"
        )
    return result.stdout.strip()


def log(message: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat()} {message}"
    print(line, flush=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")


def sync_source(name: str, spec: dict[str, str]) -> tuple[Path, str]:
    repo = CACHE / spec["cache"]
    repo.parent.mkdir(parents=True, exist_ok=True)
    if not (repo / ".git").exists():
        if repo.exists() and any(repo.iterdir()):
            raise RuntimeError(f"Refusing to use non-empty, non-git source path: {repo}")
        run([
            "git", "clone", "--filter=blob:none", "--branch", spec["branch"],
            "--single-branch", spec["url"], str(repo),
        ])
    else:
        remote = run(["git", "-C", str(repo), "remote", "get-url", "origin"])
        if remote != spec["url"]:
            raise RuntimeError(f"Unexpected origin for {name}: {remote}")
        dirty = run(["git", "-C", str(repo), "status", "--porcelain"])
        if dirty:
            raise RuntimeError(f"Source cache {name} has local changes; refusing to pull")
        run(["git", "-C", str(repo), "pull", "--ff-only", "origin", spec["branch"]])
        run(["git", "-C", str(repo), "checkout", "--detach", f"origin/{spec['branch']}"])
    head = run(["git", "-C", str(repo), "rev-parse", "HEAD"])
    return repo, head


def main() -> int:
    if not shutil.which("codex"):
        raise RuntimeError("Codex CLI is not on PATH")

    previous = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    repositories: dict[str, Path] = {}
    current: dict[str, str] = {}
    for name, spec in SOURCES.items():
        repositories[name], current[name] = sync_source(name, spec)
        previous.setdefault(name, spec["documented"])

    changed = {name: (previous[name], head) for name, head in current.items()
               if previous[name] != head}
    if not changed:
        RESULT.write_text("[]\n", encoding="utf-8")
        log("No new source commits; documentation review skipped.")
        return 0

    dirty = run([
        "git", "-C", str(WORKSPACE), "status", "--porcelain", "--untracked-files=all",
        "--", "content", "scripts/docs",
        "public/phoenix-pipelines.drawio", "public/diagrams",
    ])
    if dirty:
        raise RuntimeError(
            "Workspace has uncommitted changes. Review or commit them before the sync edits docs.\n"
            f"{dirty}"
        )

    sections: list[str] = []
    for name, (old, new) in changed.items():
        repo = repositories[name]
        sections.append(
            f"## {name} ({SOURCES[name]['branch']})\n"
            f"- Previous documented revision: `{old}`\n- Current revision: `{new}`\n"
            f"- Commits:\n{run(['git', '-C', str(repo), 'log', '--oneline', f'{old}..{new}']) or '(none)'}\n"
            f"- Changed paths:\n{run(['git', '-C', str(repo), 'diff', '--name-status', f'{old}..{new}']) or '(none)'}"
        )

    source_paths = "\n".join(f"- `{path}`" for path in repositories.values())
    prompt = f"""Daily source review for the Phoenix HR/EX documentation app.

Review the upstream changes below against the current documentation. Treat these source checkouts
as read-only inputs; do not modify them:
{source_paths}
Only edit curated app sources
under `{APP / 'content'}` and, if needed, the relevant source HTML/Markdown under
`{APP / 'scripts/docs'}`. Keep English and Persian versions aligned. Treat source code and config
as the authority. Update the app's interactive diagrams only for verified changes that affect
the EX pipelines, models, integrations, or risks; unrelated changes do not belong in this app.
Keep file:line and commit evidence current, label inference, and do not claim product behavior
from commit messages alone. Do not commit, push, or broaden the HR/EX scope.
Never edit `content/instances_snapshot.json`; it is generated from chatbot-ops after this review.

If documentation changed, regenerate the app data and Draw.io file with `npm run content` from
`{APP}`. Do not run tests. End with a short summary of changes or why no documentation update was
needed.

Upstream changes:
{os.linesep.join(sections)}
"""
    log(f"Reviewing source updates: {', '.join(changed)}")
    last_message = CACHE / "last-review.md"
    result = subprocess.run(
        ["codex", "--ask-for-approval", "never", "exec", "--cd", str(WORKSPACE),
         "--sandbox", "workspace-write", "--output-last-message", str(last_message), prompt],
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if result.stderr:
        log(result.stderr.rstrip())
    if result.returncode:
        raise RuntimeError(f"Codex review failed with exit code {result.returncode}")

    # The app shows these generated diagrams as they are, so they are copied, never reviewed.
    for name, target in RUNTIME_DIAGRAMS.items():
        source = repositories["phoenix"] / "python" / name / "docs" / "aiva-runtime-architecture.html"
        shutil.copyfile(source, APP / "public" / "diagrams" / target)

    # Facts for the Instances section. Deterministic, so it is not left to the review above, and it
    # runs after it because a failed review must not leave content/ dirty for the next run.
    run([sys.executable, str(APP / "scripts" / "build_instances.py"), "--ops", str(repositories["chatbot-ops"])])
    run(["npm", "run", "content"], cwd=APP)
    status = run([
        "git", "-C", str(WORKSPACE), "status", "--porcelain", "--untracked-files=all",
        "--", "content", "scripts/docs",
        "public/phoenix-pipelines.drawio", "public/diagrams",
    ])
    changed_docs = [line.split(None, 1)[1] for line in status.splitlines() if len(line.split(None, 1)) == 2]
    RESULT.write_text(json.dumps(changed_docs, indent=2) + "\n", encoding="utf-8")
    STATE.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    summary = last_message.read_text(encoding="utf-8").strip() if last_message.exists() else "No summary returned."
    log(summary)
    log("Review completed. Changes are left uncommitted for human review.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        CACHE.mkdir(parents=True, exist_ok=True)
        log(f"ERROR: {exc}")
        raise SystemExit(1)
