from typing import Any

from pydantic import HttpUrl

from dsets.lib.doctree import Document
from dsets.lib.pydantic_util import CamelCaseMixin

from .fields import PythonIdentifier


class Dataset(Document, CamelCaseMixin):
    """Model for dataset family data files."""

    data_url: HttpUrl | None = None
    parameters: dict[PythonIdentifier, str | None] = {}
    extra: dict[str, Any] = {}
