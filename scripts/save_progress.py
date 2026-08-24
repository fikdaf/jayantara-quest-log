#!/usr/bin/env python3
"""Persist canonical progress state with schema validation and atomic replacement."""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "data" / "state"
DEFAULT_STATE = STATE_DIR / "progress-state.json"
SCHEMA = ROOT / "schemas" / "progress-state.schema.json"


def validate(state):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = schema["required"]
    missing = [key for key in required if key not in state]
    if missing:
        raise ValueError("missing state fields: " + ", ".join(missing))
    if state["version"] != 1:
        raise ValueError("unsupported progress state version")
    if not isinstance(state["completed_quests"], list) or len(set(state["completed_quests"])) != len(state["completed_quests"]):
        raise ValueError("completed_quests must be a unique list")
    if any(not isinstance(day, int) or day < 1 or day > 30 for day in state["completed_quests"]):
        raise ValueError("completed_quests contains an invalid day")
    if not isinstance(state["xp"], int) or state["xp"] < 0:
        raise ValueError("xp must be a non-negative integer")
    if not isinstance(state["badges"], list) or len(set(state["badges"])) != len(state["badges"]):
        raise ValueError("badges must be a unique list")
    if not isinstance(state["current_day"], int) or not 1 <= state["current_day"] <= 30:
        raise ValueError("current_day must be between 1 and 30")
    return state


def save(state, path=DEFAULT_STATE):
    validate(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("state_file", type=Path)
    args = parser.parse_args()
    state = json.loads(args.state_file.read_text(encoding="utf-8"))
    print(save(state))


if __name__ == "__main__":
    main()
