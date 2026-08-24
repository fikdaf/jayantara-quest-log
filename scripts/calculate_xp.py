#!/usr/bin/env python3
"""Calculate deterministic XP totals from quest metadata."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"
XP = {"lesson": 100, "checkpoint": 250, "final_exam": 500}
PHASE_BONUS = 250
COURSE_BONUS = 1000


def quest_type(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^type:[ \t]*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def main():
    total = 0
    counts = {}
    for day in range(1, 31):
        path = QUESTS / f"day-{day:02d}.md"
        if not path.exists():
            print(f"missing quest: day-{day:02d}", file=sys.stderr)
            return 1
        kind = quest_type(path)
        if kind not in XP:
            print(f"invalid type for day-{day:02d}: {kind}", file=sys.stderr)
            return 1
        total += XP[kind]
        counts[kind] = counts.get(kind, 0) + 1

    total_with_phase_bonuses = total + (6 * PHASE_BONUS)
    total_course = total_with_phase_bonuses + COURSE_BONUS
    print(f"Quest XP: {total}")
    print(f"Phase bonuses: {6 * PHASE_BONUS}")
    print(f"Course completion bonus: {COURSE_BONUS}")
    print(f"Maximum XP: {total_course}")
    print(f"Quest types: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
