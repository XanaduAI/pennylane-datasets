import re

import pytest
from dsets.schemas.fields import PythonIdentifier
from pydantic import TypeAdapter, ValidationError


@pytest.mark.parametrize("val", ["a", "a_variable", "a1", "A1", "A"])
def test_python_identifier(val):
    """Check that valid python identifiers pass validation."""

    assert TypeAdapter(PythonIdentifier).validate_python(val) == val


@pytest.mark.parametrize("val", ["1", "1a", "kabob-case"])
def test_python_identifier_invalid(val):
    """Check that invalid Python identifiers fail validation."""

    with pytest.raises(
        ValidationError,
        match=f".*Not a valid Python identifier: {re.escape(repr(val))}.*",
    ):
        TypeAdapter(PythonIdentifier).validate_python(val)
