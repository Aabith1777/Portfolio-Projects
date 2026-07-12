"""Utility helpers for JSON I/O used by LineageEngine."""
import json
from pathlib import Path


def load_json(path: Path) -> dict | list:
    """Load and return the parsed content of a JSON file."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(data: dict | list, path: Path, indent: int = 4) -> None:
    """Serialize *data* to *path* as pretty-printed JSON."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=indent, ensure_ascii=False)
