#!/usr/bin/env python3
"""Validate quest metadata where frontmatter has been migrated.

Legacy Markdown without frontmatter is allowed during the migration window;
its day/phase/type data remains governed by data/curriculum.yaml.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
phase_by_day = {}
for days, phase in [
    (range(1, 6), "foundation"),
    (range(6, 11), "novice"),
    (range(11, 16), "adept"),
    (range(16, 21), "kanji"),
    (range(21, 26), "workplace"),
    (range(26, 31), "career"),
]:
    for day in days:
        phase_by_day[day] = phase

migrated = 0
legacy = 0
for day in range(1, 31):
    path = ROOT / "quests" / f"day-{day:02d}.md"
    if not path.exists():
        errors.append(f"Day {day}: missing file")
        continue
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        legacy += 1
        continue
    migrated += 1
    front = match.group(1)
    expected = {
        "id": f"day-{day:02d}",
        "day": str(day),
        "phase": phase_by_day[day],
        "level": "N5",
    }
    for key, value in expected.items():
        if not re.search(rf"^{key}:\s*{re.escape(value)}\s*$", front, re.MULTILINE):
            errors.append(f"Day {day}: expected {key}: {value}")
    if not re.search(r"^type:\s*(lesson|checkpoint|final_exam)\s*$", front, re.MULTILINE):
        errors.append(f"Day {day}: invalid type")
    if "reward:" not in front or not re.search(r"^  badge:\s*.+$", front, re.MULTILINE):
        errors.append(f"Day {day}: missing reward.badge")

if errors:
    print("Curriculum validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print(f"Curriculum validation passed: {migrated}/30 migrated, {legacy}/30 legacy quest files.")
