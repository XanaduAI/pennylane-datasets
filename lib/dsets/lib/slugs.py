import re

from anyascii import anyascii

_WHITESPACE_PATTERN = re.compile(r"[\s]+")


def slugify(s: str) -> str:
    """Convert ``s`` to a string containing only lowercase ASCII characters,
    with whitespace replaced by '-'. Leading and trailing whitespace will be
    stripped."""
    s = anyascii(s.strip()).lower()
    return re.sub(_WHITESPACE_PATTERN, "-", s)
