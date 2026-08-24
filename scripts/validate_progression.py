#!/usr/bin/env python3
"""Validate XP and phase progression configuration against quest metadata."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"

VALID_TYPES = {"lesson", "checkpoint", "final_exam"}
PHASES = [
    ("foundation", range(1, 6)),
    ("novice", range(6, 11)),
    ("adept", range(11, 16)),
    ("kanji", range(16, 21)),
    ("workplace", range(21, 26)),
    ("career", range(26, 31)),
]


def meta(day):
    text = (QUESTS / f"day-{day:02d}.md").read_text(encoding="utf-8")
    result = {}
    match = re.search(r"^type:[ \t]*(.+)$", text, re.MULTILINE)
    result["type"] = match.group(1).strip() if match else None
    match = re.search(r"^phase:[ \t]*(.+)$", text, re.MULTILINE)
    result["phase"] = match.group(1).strip() if match else None
    return result


def main():
    errors = []
    phase_by_day = {}
    for phase, days in PHASES:
        for day in days:
            phase_by_day[day] = phase

    for day in range(1, 31):
        path = QUESTS / f"day-{day:02d}.md"
        if not path.exists():
            errors.append(f"Day {day}: missing quest")
            continue
        m = meta(day)
        if m["type"] not in VALID_TYPES:
            errors.append(f"Day {day}: invalid type '{m['type']}'")
        if m["phase"] != phase_by_day[day]:
            errors.append(f"Day {day}: expected phase '{phase_by_day[day]}', got '{m['phase']}'")

    checkpoints = {5, 10, 15, 20}
    for day in checkpoints:
        if meta(day)["type"] != "checkpoint":
            errors.append(f"Day {day}: must be checkpoint")
    if meta(30)["type"] != "final_exam":
        errors.append("Day 30: must be final_exam")

    if errors:
        print("Progression validation failed:")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print("Progression validation passed: 30 quests match the six-phase progression rules.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
