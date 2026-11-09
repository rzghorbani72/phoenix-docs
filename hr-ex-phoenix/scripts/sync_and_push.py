#!/usr/bin/env python3
"""Pull source repos, refresh HR/EX docs, and push only files changed by that sync."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
WORKSPACE = APP  # the app is its own git repository
RESULT = APP / ".source-sync" / "changed-docs.json"
ALLOWED_PREFIXES = ("content/", "scripts/docs/", "public/diagrams/")
ALLOWED_FILES = {"public/phoenix-pipelines.drawio"}


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=WORKSPACE, text=True)
    if check and result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(args)}")
    return result


def main() -> int:
    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet", "--", "content",
         "scripts/docs", "public/phoenix-pipelines.drawio",
         "public/diagrams"],
        cwd=WORKSPACE,
    )
    if staged.returncode:
        raise RuntimeError("Relevant files are already staged; commit or unstage them before syncing.")

    run([sys.executable, str(APP / "scripts" / "sync_daily.py")])
    changed = json.loads(RESULT.read_text(encoding="utf-8")) if RESULT.exists() else []
    paths = sorted(set(changed))
    invalid = [path for path in paths if path not in ALLOWED_FILES and
               not path.startswith(ALLOWED_PREFIXES)]
    if invalid:
        raise RuntimeError(f"Sync reported files outside the docs allowlist: {invalid}")
    if not paths:
        print("No documentation changes to push.")
        return 0

    run(["git", "add", "--", *paths])
    staged_diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=WORKSPACE)
    if staged_diff.returncode == 0:
        print("No new staged documentation changes to push.")
        return 0
    run(["git", "commit", "-m", "docs: sync HR/EX from Phoenix sources"])
    run(["git", "push", "origin", "HEAD"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
