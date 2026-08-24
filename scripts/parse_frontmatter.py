#!/usr/bin/env python3
"""Parse quest frontmatter without requiring third-party dependencies."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "quests"

def parse_scalar(value):
    value = value.strip()
    if not value:
        return None
    if value.startswith("[") and value.endswith("]"):
        return [parse_scalar(x) for x in value[1:-1].split(",") if x.strip()]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value

def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.startswith(" "):
            continue
        key, sep, value = line.partition(":")
        if sep:
            data[key.strip()] = parse_scalar(value)
    return data

quests = []
for path in sorted(QUESTS.glob("day-*.md")):
    meta = parse_frontmatter(path.read_text(encoding="utf-8"))
    if meta:
        meta["path"] = str(path.relative_to(ROOT))
        quests.append(meta)

print(json.dumps({"version": 1, "quests": quests}, ensure_ascii=False, indent=2))
