from typing import TYPE_CHECKING, Annotated

from pydantic import PrivateAttr

if TYPE_CHECKING:
    from dsets.lib.doctree.doctree import DoctreeContext


class DoctreeObj:
    _document_context: Annotated["DoctreeContext", PrivateAttr()]

    @property
    def document_context(self) -> "DoctreeContext":
        return self._document_context
