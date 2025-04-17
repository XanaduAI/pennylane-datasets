from pathlib import Path
from typing import Annotated, Any

from pydantic import Field, HttpUrl, RootModel

from .doctree import DocPath, DoctreeObj, set_document_context


class Asset(RootModel, DoctreeObj):
    root: Annotated[HttpUrl | DocPath, Field(union_mode="left_to_right")]

    @property
    def is_local(self) -> bool:
        return isinstance(self.root, DocPath)

    @property
    def os_path(self) -> Path:
        if not self.is_local:
            raise ValueError("Not a local asset")

        return self.document_context.doctree.get_os_path(
            self.document_context.resolve_reference_path(self.root)
        )

    def model_post_init(self, __context: Any) -> None:
        set_document_context(self, __context)
        return super().model_post_init(__context)

    def __hash__(self) -> int:
        return hash(self.root)
