from pathlib import Path, PurePosixPath
from typing import Any

from pydantic import HttpUrl, RootModel

from .doctree import DoctreeObj, get_doctree_context


class Asset(RootModel, DoctreeObj):
    root: PurePosixPath | HttpUrl

    @property
    def is_local(self) -> bool:
        return isinstance(self.root, PurePosixPath)

    @property
    def os_path(self) -> Path:
        if not self.is_local:
            raise ValueError("Not a local asset")

        return self.document_context.make_reference_context(self.root).os_path

    def model_post_init(self, __context: Any) -> None:
        if ctx := get_doctree_context(__context):
            self._document_context = ctx["document_context"]
            ctx["document_context"].doctree._objects[type(self)].append(self)

        return super().model_post_init(__context)
