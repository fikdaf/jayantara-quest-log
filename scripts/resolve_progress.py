#!/usr/bin/env python3
"""Resolve completed quests into the canonical JAYANTARA progress state.

Usage:
  python scripts/resolve_progress.py 1 2 3 4 5
  python scripts/resolve_progress.py --json 1 2 3 4 5
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"
XP = {"lesson": 100, "checkpoint": 250, "final_exam": 500}
PHASES = [("foundation", 1, 5), ("novice", 6, 10), ("adept", 11, 15), ("kanji", 16, 20), ("workplace", 21, 25), ("career", 26, 30)]
BADGES = {"bronze": [1,2,3,4], "silver": [6,7,8,9], "adept-warrior": [11,12,13,14], "kanji-apprentice": [16,17,18,19], "japan-ready": [21,22,23,24,25], "interview-master": [26,27,28,29], "gold-jayantara": list(range(1,31))}


def quest_xp(day):
    text = (QUESTS / f"day-{day:02d}.md").read_text(encoding="utf-8")
    match = re.search(r"^type:[ \t]*(.+)$", text, re.MULTILINE)
    return XP.get(match.group(1).strip(), 0) if match else 0


def resolve(days):
    completed = set(days)
    xp = sum(quest_xp(day) for day in completed)
    unlocked = sorted(badge for badge, required in BADGES.items() if set(required).issubset(completed))
    phases = [name for name, start, end in PHASES if all(day in completed for day in range(start, end + 1))]

    if len(completed) == 30:
        current_day = 30
        current_phase = "career"
    else:
        current_day = min((day for day in range(1, 31) if day not in completed), default=30)
        current_phase = next(name for name, start, end in PHASES if start <= current_day <= end)

    return {
        "version": 1,
        "completed_quests": sorted(completed),
        "xp": xp,
        "badges": unlocked,
        "current_day": current_day,
        "current_phase": current_phase,
    }


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    args = [arg for arg in args if arg != "--json"]
    try:
        days = sorted(set(int(x) for x in args))
    except ValueError:
        print("Days must be integers.", file=sys.stderr)
        return 2
    if any(day < 1 or day > 30 for day in days):
        print("Days must be between 1 and 30.", file=sys.stderr)
        return 2
    state = resolve(days)
    if as_json:
        print(json.dumps(state, indent=2))
    else:
        print(f"Completed: {state['completed_quests']}")
        print(f"XP: {state['xp']}")
        print(f"Badges unlocked: {state['badges'] or 'none'}")
        print(f"Current day: {state['current_day']}")
        print(f"Current phase: {state['current_phase']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
