#!/usr/bin/env python3
"""Regression tests for the transactional completion + progress command."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("complete_progress", ROOT / "scripts" / "complete_progress.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def expect_error(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError("expected completion failure")


def main():
    state = module.complete(1, [])
    assert state["completed_quests"] == [1]
    assert state["current_day"] == 2
    assert state["current_phase"] == "foundation"

    expect_error(lambda: module.complete(3, [1]))

    state = module.complete(2, [1])
    assert state["completed_quests"] == [1, 2]
    assert state["xp"] > 0

    state = module.complete(5, [1, 2, 3, 4])
    assert state["current_day"] == 6
    assert "bronze" in state["badges"]

    print("Transactional progress tests passed.")


if __name__ == "__main__":
    main()
