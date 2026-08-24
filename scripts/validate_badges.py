#!/usr/bin/env python3
"""Validate badge unlock rules against the 30-day quest curriculum."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BADGES = ROOT / "data" / "badges.yaml"

text = BADGES.read_text(encoding="utf-8")
errors = []
badges = {}
current = None
for line in text.splitlines():
    match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
    if match:
        current = match.group(1)
        badges[current] = {}
        continue
    if current:
        match = re.match(r"^    (name|unlock_day):[ \t]*(.+)$", line)
        if match:
            value = match.group(2).strip().strip("\"'")
            badges[current][match.group(1)] = int(value) if value.isdigit() else value
        match = re.match(r"^    requires:[ \t]*\[(.*?)\][ \t]*$", line)
        if match:
            badges[current]["requires"] = [int(x.strip()) for x in match.group(1).split(",") if x.strip()]

if not badges:
    errors.append("no badges found")

for badge_id, badge in badges.items():
    if not badge.get("name"):
        errors.append(f"{badge_id}: missing name")
    day = badge.get("unlock_day")
    if not isinstance(day, int) or not 1 <= day <= 30:
        errors.append(f"{badge_id}: unlock_day must be between 1 and 30")
        continue
    requires = badge.get("requires", [day])
    if len(requires) != len(set(requires)):
        errors.append(f"{badge_id}: duplicate required days")
    for required_day in requires:
        if not 1 <= required_day <= 30:
            errors.append(f"{badge_id}: invalid required day {required_day}")
        elif required_day > day:
            errors.append(f"{badge_id}: requires future day {required_day}")

expected = {5: "bronze", 10: "silver", 15: "adept-warrior", 20: "kanji-apprentice", 25: "japan-ready", 29: "interview-master", 30: "gold-jayantara"}
for day, badge_id in expected.items():
    if badge_id not in badges:
        errors.append(f"missing milestone badge: {badge_id}")
    elif badges[badge_id].get("unlock_day") != day:
        errors.append(f"{badge_id}: expected unlock_day {day}")

if errors:
    print("Badge validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)

print(f"Badge validation passed: {len(badges)} badges are valid.")
