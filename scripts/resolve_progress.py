#!/usr/bin/env python3
"""Resolve XP, badges, and phase progress from completed quest days.

Usage:
  python scripts/resolve_progress.py 1 2 3 4 5
"""
from pathlib import Path
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
    unlocked = [badge for badge, required in BADGES.items() if set(required).issubset(completed)]
    phases = []
    for name, start, end in PHASES:
        if all(day in completed for day in range(start, end + 1)):
            phases.append(name)
    return xp, unlocked, phases

def main():
    try:
        days = sorted(set(int(x) for x in sys.argv[1:]))
    except ValueError:
        print("Days must be integers.", file=sys.stderr)
        return 2
    if any(day < 1 or day > 30 for day in days):
        print("Days must be between 1 and 30.", file=sys.stderr)
        return 2
    xp, badges, phases = resolve(days)
    print(f"Completed: {days}")
    print(f"XP: {xp}")
    print(f"Badges unlocked: {badges or 'none'}")
    print(f"Phases completed: {phases or 'none'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
