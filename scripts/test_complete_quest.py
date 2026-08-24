#!/usr/bin/env python3
"""Regression tests for prerequisite-aware quest completion."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("complete_quest", ROOT / "scripts" / "complete_quest.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def expect_error(fn, message):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError(message)


def main():
    # Current migrated quest metadata explicitly declares no prerequisites for
    # these early quests, so completion must not invent sequential dependencies.
    assert module.load_prerequisites(1) == []
    assert module.load_prerequisites(2) == []
    assert module.complete(1, []) == [1]
    assert module.complete(2, []) == [2]
    assert module.complete(2, [1]) == [1, 2]
    assert module.complete(5, [1, 2, 3, 4]) == [1, 2, 3, 4, 5]
    assert module.complete(5, [5, 1, 2, 3, 4]) == [1, 2, 3, 4, 5]
    expect_error(lambda: module.complete(31, []), "day 31 must be rejected")
    print("Quest completion tests passed: 6 scenarios.")


if __name__ == "__main__":
    main()
