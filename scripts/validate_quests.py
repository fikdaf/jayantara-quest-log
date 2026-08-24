#!/usr/bin/env python3
"""Validate the 30-day quest content and curriculum metadata."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"
errors = []

for day in range(1, 31):
    path = QUESTS / f"day-{day:02d}.md"
    if not path.exists():
        errors.append(f"missing quest: {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    if not re.search(rf"^# Day {day:02d}:|^# Day {day}:", text, re.MULTILINE):
        errors.append(f"Day {day}: heading does not identify the correct day")
    required = ["## 🎯 Materi & Output Skill", "## 📝 Checklist Belajar Hari Ini", "## 🗒️ Catatan Pribadi", "## ✅ Status"]
    for heading in required:
        if heading not in text:
            errors.append(f"Day {day}: missing section '{heading}'")
    if "- [ ] Quest selesai" not in text:
        errors.append(f"Day {day}: missing completion checkbox")

if errors:
    print("Quest validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)

print("Quest validation passed: 30/30 quest files have the required structure.")
