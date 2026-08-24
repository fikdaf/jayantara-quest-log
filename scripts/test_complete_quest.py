#!/usr/bin/env python3
"""Regression tests for sequential quest completion."""
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
    assert module.complete(1, []) == [1]
    expect_error(lambda: module.complete(2, []), "day 2 must require day 1")
    assert module.complete(2, [1]) == [1, 2]
    expect_error(lambda: module.complete(5, [1, 2]), "day 5 must require day 4")
    assert module.complete(5, [1, 2, 3, 4]) == [1, 2, 3, 4, 5]
    assert module.complete(5, [5, 1, 2, 3, 4]) == [1, 2, 3, 4, 5]
    expect_error(lambda: module.complete(31, []), "day 31 must be rejected")
    print("Quest completion tests passed: 6 scenarios.")


if __name__ == "__main__":
    main()
