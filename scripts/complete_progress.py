#!/usr/bin/env python3
"""Atomically validate quest completion and emit canonical progress state.

Usage:
  python scripts/complete_progress.py 5 1 2 3 4
  python scripts/complete_progress.py --json 5 1 2 3 4
"""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

complete_quest = load_module("complete_quest", "complete_quest.py")
resolve_progress = load_module("resolve_progress", "resolve_progress.py")


def complete(day, completed):
    updated = complete_quest.complete(day, completed)
    return resolve_progress.resolve(updated)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("completed", nargs="*", type=int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        state = complete(args.day, args.completed)
    except (OSError, ValueError) as exc:
        print(str(exc), file=__import__("sys").stderr)
        return 1
    if args.json:
        print(json.dumps(state, indent=2))
    else:
        print(f"Completed day: {args.day}")
        print(f"XP: {state['xp']}")
        print(f"Badges: {state['badges'] or 'none'}")
        print(f"Current day: {state['current_day']}")
        print(f"Current phase: {state['current_phase']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
