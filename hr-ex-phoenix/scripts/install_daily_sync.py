#!/usr/bin/env python3
"""Install or remove the local 07:00 daily source-sync cron entry."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
CACHE = APP / ".source-sync"
MARKER = "# hr-ex-phoenix-daily-sync"


def crontab() -> list[str]:
    result = subprocess.run(["crontab", "-l"], text=True, capture_output=True)
    if result.returncode == 0:
        return result.stdout.splitlines()
    if "no crontab for" in result.stderr.lower():
        return []
    raise RuntimeError(result.stderr.strip() or "Could not read the current crontab")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remove", action="store_true", help="remove the daily sync entry")
    args = parser.parse_args()

    lines = [line for line in crontab() if MARKER not in line]
    if not args.remove:
        codex = shutil.which("codex")
        if not codex:
            raise RuntimeError("Codex CLI is not on PATH")
        CACHE.mkdir(parents=True, exist_ok=True)
        cron_path = f"{Path(codex).parent}:/usr/local/bin:/usr/bin:/bin"
        command = (
            f"0 7 * * * PATH={cron_path} {sys.executable} "
            f"{APP / 'scripts' / 'sync_daily.py'} >> {CACHE / 'cron.log'} 2>&1 {MARKER}"
        )
        lines.append(command)

    result = subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True)
    if result.returncode:
        raise RuntimeError("Could not update the current crontab")
    print("Daily sync removed." if args.remove else "Daily sync installed for 07:00 local time.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
