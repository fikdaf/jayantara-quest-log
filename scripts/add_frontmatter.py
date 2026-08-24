#!/usr/bin/env python3
"""Add normalized YAML frontmatter to legacy day-XX Markdown quests.

Idempotent: files that already start with YAML frontmatter are skipped.
Run from the repository root with: python3 scripts/add_frontmatter.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"

PHASES = {
    1: ("foundation", "lesson"), 2: ("foundation", "lesson"), 3: ("foundation", "lesson"),
    4: ("foundation", "lesson"), 5: ("foundation", "checkpoint"),
    6: ("novice", "lesson"), 7: ("novice", "lesson"), 8: ("novice", "lesson"),
    9: ("novice", "lesson"), 10: ("novice", "checkpoint"),
    11: ("adept", "lesson"), 12: ("adept", "lesson"), 13: ("adept", "lesson"),
    14: ("adept", "lesson"), 15: ("adept", "checkpoint"),
    16: ("kanji", "lesson"), 17: ("kanji", "lesson"), 18: ("kanji", "lesson"),
    19: ("kanji", "lesson"), 20: ("kanji", "checkpoint"),
    21: ("workplace", "lesson"), 22: ("workplace", "lesson"), 23: ("workplace", "lesson"),
    24: ("workplace", "lesson"), 25: ("workplace", "lesson"),
    26: ("career", "lesson"), 27: ("career", "lesson"), 28: ("career", "lesson"),
    29: ("career", "lesson"), 30: ("career", "final_exam"),
}
BADGES = {
    1: "rookie-i", 2: "rookie-ii", 3: "rookie-iii", 4: "rookie-iv", 5: "bronze",
    6: "novice-i", 7: "novice-ii", 8: "novice-iii", 9: "novice-iv", 10: "silver",
    11: "adept-warrior", 12: "adept-warrior", 13: "adept-warrior", 14: "adept-warrior", 15: "adept-warrior",
    16: "kanji-apprentice", 17: "kanji-apprentice", 18: "kanji-apprentice", 19: "kanji-apprentice", 20: "kanji-apprentice",
    21: "japan-ready", 22: "japan-ready", 23: "japan-ready", 24: "japan-ready", 25: "japan-ready",
    26: "interview-master", 27: "interview-master", 28: "interview-master", 29: "interview-master", 30: "gold-jayantara",
}

for day in range(1, 31):
    path = QUESTS / f"day-{day:02d}.md"
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        continue
    match = re.match(r"^# Day \d+: (.+)$", text, re.MULTILINE)
    if not match:
        raise SystemExit(f"Cannot find title in {path}")
    title = match.group(1).strip()
    # Keep the visible Markdown title unchanged; metadata is additive.
    phase, quest_type = PHASES[day]
    badge = BADGES[day]
    prerequisites = []
    if day in (5, 10, 15, 20):
        start = day - 4
        prerequisites = [f"day-{n:02d}" for n in range(start, day)]
    elif day == 30:
        prerequisites = [f"day-{n:02d}" for n in range(1, 30)]
    prereq_yaml = "[]" if not prerequisites else "[" + ", ".join(prerequisites) + "]"
    frontmatter = (
        "---\n"
        f"id: day-{day:02d}\n"
        f"day: {day}\n"
        f"title: {title}\n"
        f"type: {quest_type}\n"
        f"phase: {phase}\n"
        "level: N5\n"
        "estimated_minutes: 30\n"
        "skills: []\n"
        f"prerequisites: {prereq_yaml}\n"
        "reward:\n"
        f"  badge: {badge}\n"
        "---\n\n"
    )
    path.write_text(frontmatter + text, encoding="utf-8")
    print(f"migrated {path.relative_to(ROOT)}")
