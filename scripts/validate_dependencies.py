#!/usr/bin/env python3
"""Validate explicitly declared quest prerequisites."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"


def frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    return match.group(1) if match else None


def block_list(front, key):
    match = re.search(rf"^{re.escape(key)}:[ \t]*(.*)$", front, re.MULTILINE)
    if not match:
        return None
    inline = match.group(1).strip()
    if inline:
        if not (inline.startswith("[") and inline.endswith("]")):
            return None
        return [x.strip().strip("\"'") for x in inline[1:-1].split(",") if x.strip()]
    items = []
    tail = front[match.end():]
    for line in tail.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\s+-\s+", line):
            items.append(re.sub(r"^\s+-\s+", "", line).strip().strip("\"'"))
            continue
        if not line.startswith(" "):
            break
        if re.match(r"^\s*\w[\w-]*:", line):
            break
    return items


quests = {}
errors = []
for day in range(1, 31):
    path = QUESTS / f"day-{day:02d}.md"
    if not path.exists():
        errors.append(f"Day {day}: missing file")
        continue
    front = frontmatter(path.read_text(encoding="utf-8"))
    if front is None:
        errors.append(f"Day {day}: missing frontmatter")
        continue
    quest_id = re.search(r"^id:[ \t]*(.+)$", front, re.MULTILINE)
    quest_type = re.search(r"^type:[ \t]*(.+)$", front, re.MULTILINE)
    prerequisites = block_list(front, "prerequisites")
    if prerequisites is None:
        errors.append(f"Day {day}: prerequisites must be a list")
        prerequisites = []
    if not quest_id or not quest_type:
        continue
    quest_id = quest_id.group(1).strip()
    if quest_id in quests:
        errors.append(f"Day {day}: duplicate quest id '{quest_id}'")
        continue
    quests[quest_id] = {
        "day": day,
        "type": quest_type.group(1).strip(),
        "prerequisites": prerequisites,
    }

for quest_id, meta in quests.items():
    for prereq in meta["prerequisites"]:
        if prereq not in quests:
            errors.append(f"{quest_id}: prerequisite '{prereq}' does not exist")
            continue
        if quests[prereq]["day"] >= meta["day"]:
            errors.append(f"{quest_id}: prerequisite '{prereq}' must be an earlier day")

if errors:
    print("Dependency validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)

print("Dependency validation passed: all explicitly declared prerequisites are valid.")
