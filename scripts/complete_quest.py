#!/usr/bin/env python3
"""Complete a quest only when Day N-1 and declared prerequisites are satisfied.

The curriculum is intentionally sequential: Day N requires Day N-1.
Additional prerequisites declared in quest frontmatter are enforced too.

Usage:
  python scripts/complete_quest.py 5 1 2 3 4
  python scripts/complete_quest.py --json 5 1 2 3 4
"""
from pathlib import Path
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"


def load_prerequisites(day):
    path = QUESTS / f"day-{day:02d}.md"
    if not path.exists():
        raise ValueError(f"quest day-{day:02d} does not exist")
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^prerequisites:\s*\n((?:  - .+\n?)*)", text, re.MULTILINE)
    declared = [] if not match else [
        int(value) for value in re.findall(r"^  - (?:day-)?(\d+)\s*$", match.group(1), re.MULTILINE)
    ]
    if day > 1:
        declared.append(day - 1)
    return sorted(set(declared))


def complete(day, completed):
    if not 1 <= day <= 30:
        raise ValueError("day must be between 1 and 30")
    completed = set(completed)
    missing = sorted(set(load_prerequisites(day)) - completed)
    if missing:
        raise ValueError(f"Day {day}: missing prerequisites {missing}")
    completed.add(day)
    return sorted(completed)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("completed", nargs="*", type=int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        completed = complete(args.day, args.completed)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    result = {"completed_quests": completed, "completed_day": args.day}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Completed day: {args.day}")
        print(f"Completed quests: {completed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
