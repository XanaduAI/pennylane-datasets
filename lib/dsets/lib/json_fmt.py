import json
from pathlib import Path


def format(path: Path | str, check: bool, *, indent: int = 2) -> bool:
    """Format JSON file at ``path``.

    Args:
        path: Path to JSON file
        check: If True, do not write modified file
        indent: Indentation level, defaults to 2

    Returns:
        True: if file was not correctly formatted
        False: if file was already correctly formatted
    """
    with open(path, "r", encoding="utf-8") as f:
        raw_before = f.read()

    raw_after = json.dumps(json.loads(raw_before), indent=indent)
    if raw_before == raw_after:
        return False

    if not check:
        with open(path, "w", encoding="utf-8") as f:
            f.write(raw_after)

    return True
