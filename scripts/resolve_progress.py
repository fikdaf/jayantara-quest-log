#!/usr/bin/env python3
"""Resolve completed quests into the canonical JAYANTARA progress state."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"
BADGES_FILE = ROOT / "data" / "badges.yaml"
XP = {"lesson": 100, "checkpoint": 250, "final_exam": 500}
PHASES = [("foundation", 1, 5), ("novice", 6, 10), ("adept", 11, 15), ("kanji", 16, 20), ("workplace", 21, 25), ("career", 26, 30)]


def quest_xp(day):
    text = (QUESTS / f"day-{day:02d}.md").read_text(encoding="utf-8")
    match = re.search(r"^type:[ \t]*(.+)$", text, re.MULTILINE)
    if not match or match.group(1).strip() not in XP:
        raise ValueError(f"invalid or missing type for day-{day:02d}")
    return XP[match.group(1).strip()]


def load_badges():
    text = BADGES_FILE.read_text(encoding="utf-8")
    badges = {}
    current = None
    for line in text.splitlines():
        match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
        if match:
            current = match.group(1)
            badges[current] = {"requires": []}
            continue
        if not current:
            continue
        match = re.match(r"^    unlock_day:[ \t]*(\d+)\s*$", line)
        if match:
            badges[current]["unlock_day"] = int(match.group(1))
            continue
        match = re.match(r"^    requires:[ \t]*\[(.*?)\]\s*$", line)
        if match:
            badges[current]["requires"] = [int(x.strip()) for x in match.group(1).split(",") if x.strip()]
    return badges


def resolve(days):
    completed = set(days)
    xp = sum(quest_xp(day) for day in completed)
    badges = load_badges()
    unlocked = sorted(
        badge_id for badge_id, badge in badges.items()
        if set(badge.get("requires", [])) <= completed
        and (not badge.get("requires") or badge.get("unlock_day") in completed)
    )

    if len(completed) == 30:
        current_day = 30
        current_phase = "career"
    else:
        current_day = min(day for day in range(1, 31) if day not in completed)
        current_phase = next(name for name, start, end in PHASES if start <= current_day <= end)

    return {
        "version": 1,
        "completed_quests": sorted(completed),
        "xp": xp,
        "badges": unlocked,
        "current_day": current_day,
        "current_phase": current_phase,
    }


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    args = [arg for arg in args if arg != "--json"]
    try:
        days = sorted(set(int(x) for x in args))
    except ValueError:
        print("Days must be integers.", file=sys.stderr)
        return 2
    if any(day < 1 or day > 30 for day in days):
        print("Days must be between 1 and 30.", file=sys.stderr)
        return 2
    try:
        state = resolve(days)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if as_json:
        print(json.dumps(state, indent=2))
    else:
        print(f"Completed: {state['completed_quests']}")
        print(f"XP: {state['xp']}")
        print(f"Badges unlocked: {state['badges'] or 'none'}")
        print(f"Current day: {state['current_day']}")
        print(f"Current phase: {state['current_phase']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
