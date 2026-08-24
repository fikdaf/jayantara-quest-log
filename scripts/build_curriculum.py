#!/usr/bin/env python3
"""Generate a machine-readable curriculum index from quest frontmatter."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "quests.generated.json"


def scalar(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [scalar(item) for item in inner.split(",") if item.strip()]
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
    current = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, sep, raw = line.strip().partition(":")
        if not sep:
            continue
        if indent == 0:
            current = key
            result[key] = scalar(raw)
        elif indent > 0 and current:
            if not isinstance(result.get(current), dict):
                result[current] = {}
            result[current][key] = scalar(raw)
    return result


quests = []
for path in sorted((ROOT / "quests").glob("day-*.md")):
    meta = frontmatter(path.read_text(encoding="utf-8"))
    if not meta:
        raise SystemExit(f"Missing frontmatter: {path.relative_to(ROOT)}")
    meta["path"] = str(path.relative_to(ROOT))
    quests.append(meta)

if len(quests) != 30:
    raise SystemExit(f"Expected 30 quest files, found {len(quests)}")

OUT.write_text(
    json.dumps({"version": 1, "source": "quests/*.md", "quests": quests}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(f"Generated {OUT.relative_to(ROOT)} from {len(quests)} quest files.")
