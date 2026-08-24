#!/usr/bin/env python3
"""Strict schema validation for all 30 quest frontmatter blocks."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"
PHASES = {
    **{day: "foundation" for day in range(1, 6)},
    **{day: "novice" for day in range(6, 11)},
    **{day: "adept" for day in range(11, 16)},
    **{day: "kanji" for day in range(16, 21)},
    **{day: "workplace" for day in range(21, 26)},
    **{day: "career" for day in range(26, 31)},
}
TYPES = {"lesson", "checkpoint", "final_exam"}
REQUIRED = {"id", "day", "title", "type", "phase", "level", "estimated_minutes", "skills", "prerequisites"}
BADGES = {
    "rookie-i", "rookie-ii", "rookie-iii", "rookie-iv", "bronze",
    "novice-i", "novice-ii", "novice-iii", "novice-iv", "silver",
    "adept-warrior", "kanji-apprentice", "japan-ready", "interview-master",
    "gold-jayantara",
}


def block(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    return match.group(1) if match else None


def value(front, key):
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", front, re.MULTILINE)
    return match.group(1) if match else None


def list_items(front, key):
    """Support both inline YAML lists and indented block lists."""
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", front, re.MULTILINE)
    if not match:
        return None
    inline = match.group(1).strip()
    if inline:
        if not (inline.startswith("[") and inline.endswith("]")):
            return None
        body = inline[1:-1].strip()
        return [item.strip().strip("\"'") for item in body.split(",") if item.strip()]

    tail = front[match.end():]
    items = []
    for line in tail.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\s+-\s+", line):
            items.append(re.sub(r"^\s+-\s+", "", line).strip().strip("\"'"))
            continue
        if re.match(r"^\S[\w-]*:", line):
            break
        if not line.startswith(" "):
            break
    return items if items else None


errors = []
seen_ids = set()
for day in range(1, 31):
    path = QUESTS / f"day-{day:02d}.md"
    if not path.exists():
        errors.append(f"Day {day}: missing file")
        continue
    text = path.read_text(encoding="utf-8")
    front = block(text)
    if front is None:
        errors.append(f"Day {day}: missing or malformed YAML frontmatter")
        continue

    keys = {m.group(1) for m in re.finditer(r"^([A-Za-z_][A-Za-z0-9_-]*):", front, re.MULTILINE)}
    for key in REQUIRED:
        if key not in keys:
            errors.append(f"Day {day}: missing '{key}'")

    quest_id = value(front, "id")
    if quest_id != f"day-{day:02d}":
        errors.append(f"Day {day}: id must be day-{day:02d}")
    if quest_id in seen_ids:
        errors.append(f"Day {day}: duplicate id '{quest_id}'")
    seen_ids.add(quest_id)

    if value(front, "day") != str(day):
        errors.append(f"Day {day}: day metadata mismatch")
    if value(front, "phase") != PHASES[day]:
        errors.append(f"Day {day}: phase must be {PHASES[day]}")
    if value(front, "level") != "N5":
        errors.append(f"Day {day}: level must be N5")
    if value(front, "type") not in TYPES:
        errors.append(f"Day {day}: invalid type '{value(front, 'type')}'")

    minutes = value(front, "estimated_minutes")
    if not minutes or not minutes.isdigit() or not (5 <= int(minutes) <= 180):
        errors.append(f"Day {day}: estimated_minutes must be 5..180")

    skills = list_items(front, "skills")
    prerequisites = list_items(front, "prerequisites")
    if skills is None:
        errors.append(f"Day {day}: skills must be a list")
    if prerequisites is None:
        errors.append(f"Day {day}: prerequisites must be a list")
    else:
        for prereq in prerequisites:
            if prereq and not re.fullmatch(r"day-(0[1-9]|[12][0-9]|30)", prereq):
                errors.append(f"Day {day}: invalid prerequisite '{prereq}'")

    badge = re.search(r"^\s+badge:\s*([^\s#]+)\s*$", front, re.MULTILINE)
    if not badge:
        errors.append(f"Day {day}: missing reward.badge")
    elif badge.group(1) not in BADGES:
        errors.append(f"Day {day}: unknown badge '{badge.group(1)}'")

    heading = re.search(rf"^# Day {day:02d}:\s*(.+)$", text, re.MULTILINE)
    title = value(front, "title")
    if not heading:
        errors.append(f"Day {day}: missing title heading")
    elif heading.group(1).strip() != title:
        errors.append(f"Day {day}: frontmatter title does not match H1")

if errors:
    print("Frontmatter schema validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)

print("Frontmatter schema validation passed: 30/30 quest files.")
