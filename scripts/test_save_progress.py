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

    invalid = dict(state, completed_quests=[1, 1])
    try:
        module.validate(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("duplicate quests must be rejected")

    print("Progress persistence tests passed.")


if __name__ == "__main__":
    main()
