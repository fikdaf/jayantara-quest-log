#!/usr/bin/env python3
"""Complete a quest only when Day N-1 and declared prerequisites are satisfied."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_frontmatter():
    spec = importlib.util.spec_from_file_location("check_frontmatter", ROOT / "scripts" / "check_frontmatter.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_prerequisites(day):
    parser = load_frontmatter()
    data, _ = parser.load_quest(day)
    declared = []
    for value in data.get("prerequisites", []):
        value = str(value)
        if value.startswith("day-"):
            value = value[4:]
        declared.append(int(value))
    if day > 1:
        declared.append(day - 1)
    return sorted(set(declared))


def complete(day, completed):
    if not 1 <= day <= 30:
        raise ValueError("day must be between 1 and 30")
    completed = set(completed)
    missing = sorted(set(load_prerequisites(day)) - completed)
    if missing:
        raise ValueError(f"Day {day}: missing prerequisites {missing}")
    completed.add(day)
    return sorted(completed)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("completed", nargs="*", type=int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        completed = complete(args.day, args.completed)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    result = {"completed_quests": completed, "completed_day": args.day}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Completed day: {args.day}")
        print(f"Completed quests: {completed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
