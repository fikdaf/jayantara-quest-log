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
    assert quest["reward"]["badge"] == "rookie-i"

    quest20 = module.parse(20)
    assert quest20["id"] == "day-20"
    assert isinstance(quest20["skills"], list)
    assert isinstance(quest20["reward"], dict)
    assert "badge" in quest20["reward"]

    quest30 = module.parse(30)
    assert quest30["id"] == "day-30"
    assert quest30["prerequisites"] == [f"day-{day:02d}" for day in range(1, 30)]

    print("Quest details tests passed: nested reward and prerequisite metadata verified.")


if __name__ == "__main__":
    main()
