import json
from pathlib import Path


def format_json(path: Path) -> None:
    """Format JSON file at `path`.

    Uses an indent of 2. Keys are not sorted.
    """

    with open(path, "r", encoding="utf-8") as json_in:
        data = json.load(json_in)

    with open(path, "w", encoding="utf-8") as json_out:
        json.dump(data, json_out, indent=2)
