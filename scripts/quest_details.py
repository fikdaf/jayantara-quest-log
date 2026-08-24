#!/usr/bin/env python3
"""Read structured quest metadata using the shared frontmatter parser."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_parser():
    spec = importlib.util.spec_from_file_location("check_frontmatter", ROOT / "scripts" / "check_frontmatter.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse(day):
    parser = _load_parser()
    data, _ = parser.load_quest(day)
    return data
