#!/usr/bin/env python3
"""Regression tests for persistent progress state validation and atomic save."""
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("save_progress", ROOT / "scripts" / "save_progress.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def expect_error(state, message):
    try:
        module.validate(state)
    except ValueError:
        return
    raise AssertionError(message)


def main():
    state = {
        "version": 1,
        "completed_quests": [1, 2],
        "xp": 200,
        "badges": [],
        "current_day": 3,
        "current_phase": "foundation",
    }
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "progress-state.json"
        module.save(state, path)
        assert json.loads(path.read_text(encoding="utf-8")) == state
        assert not path.with_suffix(".json.tmp").exists()

    expect_error(dict(state, completed_quests=[1, 1]), "duplicate quests must be rejected")
    expect_error(dict(state, completed_quests=[0]), "day zero must be rejected")
    expect_error(dict(state, completed_quests=[31]), "day 31 must be rejected")
    expect_error(dict(state, xp=-1), "negative XP must be rejected")
    expect_error(dict(state, badges=["bronze", "bronze"]), "duplicate badges must be rejected")
    expect_error(dict(state, current_day=0), "invalid current day must be rejected")
    expect_error(dict(state, current_day=31), "current day 31 must be rejected")
    expect_error(dict(state, version=2), "unsupported state version must be rejected")
    expect_error({key: value for key, value in state.items() if key != "xp"}, "missing required field must be rejected")

    print("Progress persistence tests passed: validation and atomic save contract verified.")


if __name__ == "__main__":
    main()
