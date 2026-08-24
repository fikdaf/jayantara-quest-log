#!/usr/bin/env python3
"""Player-facing JAYANTARA CLI built on the canonical progress engine."""
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

resolve_progress = load_module("resolve_progress", "resolve_progress.py")
complete_progress = load_module("complete_progress", "complete_progress.py")
save_progress = load_module("save_progress", "save_progress.py")


def load_state(path):
    if not path.exists():
        return resolve_progress.resolve([])
    return save_progress.validate(json.loads(path.read_text(encoding="utf-8")))


def main():
    parser = argparse.ArgumentParser(prog="jayantara")
    parser.add_argument("--state-file", type=Path, default=save_progress.DEFAULT_STATE)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("start", help="show the first/current quest")
    sub.add_parser("status", help="show canonical progress")
    complete = sub.add_parser("complete", help="complete the current quest")
    complete.add_argument("day", type=int)

    args = parser.parse_args()
    try:
        state = load_state(args.state_file)
        if args.command in {"start", "status"}:
            if args.command == "start":
                print(f"Quest day: {state['current_day']}")
                print(f"Phase: {state['current_phase']}")
            else:
                print(json.dumps(state, indent=2))
            return 0

        if args.day != state["current_day"]:
            raise ValueError(f"current quest is day {state['current_day']}")
        new_state = complete_progress.complete(args.day, state["completed_quests"])
        save_progress.save(new_state, args.state_file)
        print(json.dumps(new_state, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
