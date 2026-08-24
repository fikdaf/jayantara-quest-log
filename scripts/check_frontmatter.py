#!/usr/bin/env python3
"""Check that every quest starts with required YAML frontmatter."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
required = ["id", "day", "title", "type", "phase", "level"]

for day in range(1, 31):
    path = ROOT / "quests" / f"day-{day:02d}.md"
    if not path.exists():
        errors.append(f"missing: {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"Day {day}: missing YAML frontmatter")
        continue
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append(f"Day {day}: malformed YAML frontmatter")
        continue
    front = match.group(1)
    for key in required:
        if not re.search(rf"^{re.escape(key)}:\s*.+$", front, re.MULTILINE):
            errors.append(f"Day {day}: missing frontmatter key '{key}'")
    if f"id: day-{day:02d}" not in front:
        errors.append(f"Day {day}: id must be day-{day:02d}")
    if not re.search(rf"^day:\s*{day}\s*$", front, re.MULTILINE):
        errors.append(f"Day {day}: day metadata mismatch")

if errors:
    print("Frontmatter validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)

print("Frontmatter validation passed: 30/30 quest files.")
