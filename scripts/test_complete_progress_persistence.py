#!/usr/bin/env python3
"""Test completion command persistence without modifying repository state."""
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("complete_progress", ROOT / "scripts" / "complete_progress.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "progress-state.json"
        state = module.complete(1, [])
        module.save_progress.save(state, path)
        saved = json.loads(path.read_text(encoding="utf-8"))
        assert saved == state
        assert saved["completed_quests"] == [1]

    print("Completion persistence integration test passed.")


if __name__ == "__main__":
    main()
