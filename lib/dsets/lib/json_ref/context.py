from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Self

from pydantic import (
    ValidationInfo,
)


@dataclass(frozen=True)
class DocumentContext:
    """Contains context for a model loaded from a document
    tree. Used to resolve `DocumentRef` fields in models.

    See `DocumentRef.resolve()`.

    Attributes:
        docpath_root: Absolute path of the folder containing all related
            documents
        path: Path of a document within a document tree
    """

    docpath_root: Path
    path: Path

    @classmethod
    def create(cls: type[Self], docpath_root: Path | str, path: Path | str) -> Self:
        """Create a document context. Ensures that `docpath_root` is absolute,
        and that `path` is relative to `docpath_root`."""

        docpath_root = Path(docpath_root).absolute().resolve()
        path = Path(path).absolute().resolve()

        if not path.is_relative_to(docpath_root):
            raise ValueError(
                f"Document path '{path}' is not relative to document"
                f" root path '{docpath_root}'"
            )

        return cls(docpath_root, path)

    @classmethod
    def from_referencing_context(
        cls: type[Self], ref_ctx: Self, ref_path: PurePosixPath
    ) -> Self:
        """Create a document context from the context of a referencing document."""
        if ref_path.is_absolute():
            path = ref_ctx.docpath_root / ref_path.relative_to("/")
        else:
            path = ref_ctx.path.parent / ref_path

        path = path.resolve()

        return cls(ref_ctx.docpath_root, path)

    @property
    def pydantic_context(self: Self) -> dict[str, Any]:
        """Return Pydantic validation context containing
        this context."""
        return {"document_context": self}

    @classmethod
    def from_pydantic_info(cls: type[Self], info: ValidationInfo) -> Self | None:
        """Get document context from Pydantic validation info.

        Returns `None` if the validation info does not contain a document
        context.
        """
        if info.context:
            return info.context.get("document_context")

        return None
