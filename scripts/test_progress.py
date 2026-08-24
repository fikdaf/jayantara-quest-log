#!/usr/bin/env python3
"""Regression tests for the canonical progress resolver."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("resolve_progress", ROOT / "scripts" / "resolve_progress.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    state = module.resolve([])
    check(state["completed_quests"] == [], "empty completion set")
    check(state["xp"] == 0, "empty XP")
    check(state["badges"] == [], "empty badges")
    check(state["current_day"] == 1, "initial current day")
    check(state["current_phase"] == "foundation", "initial phase")

    state = module.resolve([1])
    check(state["badges"] == ["rookie-i"], "day 1 rookie badge")

    state = module.resolve([1, 2, 3, 4, 5])
    check(state["current_day"] == 6, "day after foundation")
    check(state["current_phase"] == "novice", "phase after foundation")
    check("bronze" in state["badges"], "bronze milestone")
    check(state["xp"] > 0, "foundation XP")
    check(all(badge in state["badges"] for badge in ["rookie-i", "rookie-ii", "rookie-iii", "rookie-iv"]), "rookie badges retained")

    state = module.resolve([5, 1, 3, 2, 4])
    check(state["completed_quests"] == [1, 2, 3, 4, 5], "ordering is canonical")
    check("bronze" in state["badges"], "unordered completion milestone")

    state = module.resolve(list(range(1, 30)))
    check(state["current_day"] == 30, "final quest remains current")
    check(state["current_phase"] == "career", "final phase before exam")
    check("interview-master" in state["badges"], "interview milestone")
    check("gold-jayantara" not in state["badges"], "gold requires final quest")

    state = module.resolve(list(range(1, 31)))
    check(state["current_day"] == 30, "completed course current day")
    check(state["current_phase"] == "career", "completed course phase")
    check("gold-jayantara" in state["badges"], "gold milestone")
    check(len(state["completed_quests"]) == 30, "all quests completed")

    encoded = json.dumps(state)
    check(json.loads(encoded)["version"] == 1, "state is JSON serializable")
    print("Progress resolver tests passed: 7 scenarios.")


if __name__ == "__main__":
    main()
