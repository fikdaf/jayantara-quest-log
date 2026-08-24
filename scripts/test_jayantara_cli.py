#!/usr/bin/env python3
"""Regression tests for the player-facing CLI commands."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "jayantara.py"


def run(*args):
    return subprocess.run([sys.executable, str(CLI), *args], text=True, capture_output=True)


def main():
    with tempfile.TemporaryDirectory() as directory:
        state = str(Path(directory) / "progress.json")
        result = run("--state-file", state, "start")
        assert result.returncode == 0, result.stderr
        assert "Day 1:" in result.stdout
        assert "Gerbang Hiragana Pass" in result.stdout

        result = run("--state-file", state, "start", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["day"] == 1
        assert payload["id"] == "day-01"
        assert payload["prerequisites"] == []

        result = run("--state-file", state, "complete", "2")
        assert result.returncode != 0
        assert "current quest is day 1" in result.stderr
        assert not Path(state).exists()

        result = run("--state-file", state, "complete", "1")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["completed_quests"] == [1]
        assert payload["current_day"] == 2
        assert payload["xp"] == 100

        result = run("--state-file", state, "status")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["current_day"] == 2
        assert payload["completed_quests"] == [1]
        assert payload["xp"] == 100

        result = run("--state-file", state, "complete", "3")
        assert result.returncode != 0
        assert "current quest is day 2" in result.stderr
        payload = json.loads(Path(state).read_text(encoding="utf-8"))
        assert payload["completed_quests"] == [1]

        result = run("--state-file", state, "complete", "2")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["completed_quests"] == [1, 2]
        assert payload["current_day"] == 3
        assert payload["xp"] == 200

        result = run("--state-file", state, "start", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["day"] == 3
        assert payload["id"] == "day-03"

    print("JAYANTARA CLI tests passed: sequential completion and state persistence verified.")


if __name__ == "__main__":
    main()
