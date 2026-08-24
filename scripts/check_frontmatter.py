#!/usr/bin/env python3
"""Shared YAML frontmatter parser and strict validation for all quests."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"
PHASES = {**{day: "foundation" for day in range(1, 6)}, **{day: "novice" for day in range(6, 11)}, **{day: "adept" for day in range(11, 16)}, **{day: "kanji" for day in range(16, 21)}, **{day: "workplace" for day in range(21, 26)}, **{day: "career" for day in range(26, 31)}}
TYPES = {"lesson", "checkpoint", "final_exam"}
REQUIRED = {"id", "day", "title", "type", "phase", "level", "estimated_minutes", "skills", "prerequisites", "reward"}
BADGES = {"rookie-i", "rookie-ii", "rookie-iii", "rookie-iv", "bronze", "novice-i", "novice-ii", "novice-iii", "novice-iv", "silver", "adept-warrior", "kanji-apprentice", "japan-ready", "interview-master", "gold-jayantara"}


def _scalar(raw):
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [x.strip().strip("\"'") for x in raw[1:-1].split(",") if x.strip()]
    if raw.isdigit():
        return int(raw)
    return raw.strip("\"'")


def parse_frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("missing or malformed YAML frontmatter")
    lines = match.group(1).splitlines()
    data = {}
    stack = [(0, data)]
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)$", line)
        if not match:
            i += 1
            continue
        key, raw = match.group(1), match.group(2).strip()
        while stack and indent < stack[-1][0]:
            stack.pop()
        target = stack[-1][1]
        if raw:
            target[key] = _scalar(raw)
            i += 1
            continue
        child = {}
        target[key] = child
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and len(lines[j]) - len(lines[j].lstrip(" ")) > indent and re.match(r"^\s+-\s+", lines[j]):
            items = []
            while j < len(lines):
                item = re.match(r"^\s+-\s+(.*)$", lines[j])
                if not item or len(lines[j]) - len(lines[j].lstrip(" ")) <= indent:
                    break
                items.append(_scalar(item.group(1)))
                j += 1
            target[key] = items
            i = j
            continue
        stack.append((indent + 2, child))
        i += 1
    return data


def load_quest(day):
    path = QUESTS / f"day-{day:02d}.md"
    text = path.read_text(encoding="utf-8")
    return parse_frontmatter(text), text


def validate():
    errors = []
    seen_ids = set()
    for day in range(1, 31):
        path = QUESTS / f"day-{day:02d}.md"
        if not path.exists():
            errors.append(f"Day {day}: missing file")
            continue
        text = path.read_text(encoding="utf-8")
        try:
            front = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(f"Day {day}: {exc}")
            continue
        for key in REQUIRED:
            if key not in front:
                errors.append(f"Day {day}: missing '{key}'")
        quest_id = front.get("id")
        if quest_id != f"day-{day:02d}":
            errors.append(f"Day {day}: id must be day-{day:02d}")
        if quest_id in seen_ids:
            errors.append(f"Day {day}: duplicate id '{quest_id}'")
        seen_ids.add(quest_id)
        if front.get("day") != day:
            errors.append(f"Day {day}: day metadata mismatch")
        if front.get("phase") != PHASES[day]:
            errors.append(f"Day {day}: phase must be {PHASES[day]}")
        if front.get("level") != "N5":
            errors.append(f"Day {day}: level must be N5")
        if front.get("type") not in TYPES:
            errors.append(f"Day {day}: invalid type '{front.get('type')}'")
        minutes = front.get("estimated_minutes")
        if not isinstance(minutes, int) or not 5 <= minutes <= 180:
            errors.append(f"Day {day}: estimated_minutes must be 5..180")
        if not isinstance(front.get("skills"), list):
            errors.append(f"Day {day}: skills must be a list")
        if not isinstance(front.get("prerequisites"), list):
            errors.append(f"Day {day}: prerequisites must be a list")
        reward = front.get("reward")
        if not isinstance(reward, dict) or reward.get("badge") not in BADGES:
            errors.append(f"Day {day}: invalid or missing reward.badge")
        for prereq in front.get("prerequisites", []):
            if not re.fullmatch(r"day-(0[1-9]|[12][0-9]|30)", str(prereq)):
                errors.append(f"Day {day}: invalid prerequisite '{prereq}'")
        heading = re.search(rf"^# Day {day:02d}:[ \t]*(.+)$", text, re.MULTILINE)
        if not heading:
            errors.append(f"Day {day}: missing title heading")
        elif heading.group(1).strip() != front.get("title"):
            errors.append(f"Day {day}: frontmatter title does not match H1")
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        print("Frontmatter schema validation failed:\n" + "\n".join(f"- {e}" for e in errors))
        sys.exit(1)
    print("Frontmatter schema validation passed: 30/30 quest files.")
