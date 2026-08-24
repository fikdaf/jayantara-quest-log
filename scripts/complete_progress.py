#!/usr/bin/env python3
"""Validate quest completion, resolve state, and optionally persist it."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


complete_quest = load_module("complete_quest", "complete_quest.py")
resolve_progress = load_module("resolve_progress", "resolve_progress.py")
save_progress = load_module("save_progress", "save_progress.py")


def complete(day, completed):
    updated = complete_quest.complete(day, completed)
    return resolve_progress.resolve(updated)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("completed", nargs="*", type=int)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--save", action="store_true", help="persist to data/state/progress-state.json")
    parser.add_argument("--state-file", type=Path, help="override the persistence path")
    args = parser.parse_args()
    try:
        state = complete(args.day, args.completed)
        if args.save:
            path = save_progress.save(state, args.state_file or save_progress.DEFAULT_STATE)
        else:
            path = None
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(state, indent=2))
    else:
        print(f"Completed day: {args.day}")
        print(f"XP: {state['xp']}")
        print(f"Badges: {state['badges'] or 'none'}")
        print(f"Current day: {state['current_day']}")
        print(f"Current phase: {state['current_phase']}")
        if path:
            print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
