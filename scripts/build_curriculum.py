#!/usr/bin/env python3
"""Generate a compact machine-readable curriculum index from quest frontmatter."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "quests.generated.json"

def scalar(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [scalar(x) for x in value[1:-1].split(",") if x.strip()]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value

def frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        key, sep, value = line.partition(":")
        if sep:
            result[key.strip()] = scalar(value)
    return result

quests = []
for path in sorted((ROOT / "quests").glob("day-*.md")):
    meta = frontmatter(path.read_text(encoding="utf-8"))
    if meta:
        meta["path"] = str(path.relative_to(ROOT))
        quests.append(meta)

OUT.write_text(json.dumps({"version": 1, "quests": quests}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Generated {OUT.relative_to(ROOT)} from {len(quests)} quest files.")
