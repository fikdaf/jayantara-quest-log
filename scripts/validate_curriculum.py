#!/usr/bin/env python3
"""Validate the canonical 30-day curriculum against quest frontmatter."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
phase_by_day = {
    **{day: "foundation" for day in range(1, 6)},
    **{day: "novice" for day in range(6, 11)},
    **{day: "adept" for day in range(11, 16)},
    **{day: "kanji" for day in range(16, 21)},
    **{day: "workplace" for day in range(21, 26)},
    **{day: "career" for day in range(26, 31)},
}
expected_types = {5: "checkpoint", 10: "checkpoint", 15: "checkpoint", 20: "checkpoint", 30: "final_exam"}

for day in range(1, 31):
    path = ROOT / "quests" / f"day-{day:02d}.md"
    if not path.exists():
        errors.append(f"Day {day}: missing file")
        continue
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append(f"Day {day}: missing/malformed frontmatter")
        continue
    front = match.group(1)

    def get(key):
        m = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", front, re.MULTILINE)
        return m.group(1) if m else None

    if get("id") != f"day-{day:02d}":
        errors.append(f"Day {day}: id mismatch")
    if get("day") != str(day):
        errors.append(f"Day {day}: day mismatch")
    if get("phase") != phase_by_day[day]:
        errors.append(f"Day {day}: phase mismatch")
    if get("level") != "N5":
        errors.append(f"Day {day}: level must be N5")
    if day in expected_types and get("type") != expected_types[day]:
        errors.append(f"Day {day}: expected type {expected_types[day]}")

    prereqs = get("prerequisites")
    if prereqs is None or not prereqs.startswith("[") or not prereqs.endswith("]"):
        errors.append(f"Day {day}: prerequisites must be a list")
    else:
        for item in prereqs[1:-1].split(","):
            item = item.strip()
            if item and not re.fullmatch(r"day-(0[1-9]|[12][0-9]|30)", item):
                errors.append(f"Day {day}: invalid prerequisite {item}")

if errors:
    print("Curriculum validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)

print("Curriculum validation passed: canonical 30-day curriculum is consistent.")
