#!/usr/bin/env python3
"""End-to-end regression test for canonical progress lifecycle."""
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

resolver = load("resolve_progress")
saver = load("save_progress")


def main():
    completed = []
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "progress.json"
        for day in range(1, 31):
            completed.append(day)
            state = resolver.resolve(completed)
            saver.save(state, path)
            persisted = json.loads(path.read_text(encoding="utf-8"))
            assert persisted == state, f"persisted state diverged on day {day}"
            assert persisted["completed_quests"] == list(range(1, day + 1))
            assert persisted["current_day"] == (day + 1 if day < 30 else 30)

        final = resolver.resolve(completed)
        assert final["xp"] == 3500
        assert "gold-jayantara" in final["badges"]
        assert len(final["completed_quests"]) == 30
        assert final["current_phase"] == "career"

        reloaded = json.loads(path.read_text(encoding="utf-8"))
        assert reloaded == final

    print("Progress E2E tests passed: 30-day resolve/persist lifecycle is canonical.")


if __name__ == "__main__":
    main()
