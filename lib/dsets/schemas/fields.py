from typing import Annotated

import bibtexparser
from pydantic import AfterValidator, Field

"""
Field type for a legal Python identifier (name for a variable, class etc.)
"""
PythonIdentifier = Annotated[str, Field(pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$")]


def _bibtex_str_validator(val: str) -> str:
    """Validator for ``BibtexStr``. Checks that the entire string validates
    correctly and that it contains at least one '@entry`."""
    parsed = bibtexparser.parse_string(val)

    if parsed.failed_blocks:
        raise ValueError(
            f"Failed to parse Bibtex citation blocks: {repr(parsed.failed_blocks)}"
        )
    if not parsed.entries:
        raise ValueError("Bibtex citation has no entries.")

    return val


"""Field type for a Bibtex citation string."""
BibtexStr = Annotated[str, AfterValidator(_bibtex_str_validator)]
