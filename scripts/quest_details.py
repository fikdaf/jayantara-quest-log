#!/usr/bin/env python3
"""Read structured quest metadata for the player-facing CLI."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"


def parse(day):
    path = QUESTS / f"day-{day:02d}.md"
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing frontmatter for day-{day:02d}")
    data = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith("  "):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            data[key.strip()] = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        elif value.isdigit():
            data[key.strip()] = int(value)
        else:
            data[key.strip()] = value
    return data
