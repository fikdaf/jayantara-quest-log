#!/usr/bin/env python3
"""Regression tests for structured quest metadata."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("quest_details", ROOT / "scripts" / "quest_details.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def main():
    quest = module.parse(1)
    assert quest["id"] == "day-01"
    assert quest["day"] == 1
    assert quest["title"] == "Gerbang Hiragana Pass"
    assert quest["skills"] == ["hiragana", "pronunciation", "reading"]
    assert quest["prerequisites"] == []

    print("Quest details tests passed.")


if __name__ == "__main__":
    main()
