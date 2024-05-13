from collections.abc import Iterable, Iterator, Sequence
from itertools import chain


def _row_iter(rows: Iterable[Sequence[str]]) -> Iterator[str]:
    for row in rows:
        yield "|" + "|".join(row) + "|"


def make_markdown_table(headers: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    return "\n".join(_row_iter(chain([headers, ["-" for _ in headers]], rows)))
