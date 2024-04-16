from dataclasses import dataclass
from functools import cached_property
from pathlib import Path, PurePosixPath
from typing import Any, Hashable, Self, TypedDict

from pydantic import (
    ValidationInfo,
)


class DoctreeContext:
    docpath_root: Path

    def __init__(self, docpath_root: Path | str) -> None:
        self.docpath_root = Path(docpath_root).absolute().resolve()

        self._document_cache = {}

    def document_cache_get(
        self, os_path: Path, resolve_type: type | Hashable
    ) -> Any | None:
        return self._document_cache.get((os_path, resolve_type))

    def document_cache_update(self, os_path, resolve_type: type | Hashable, data: Any):
        if (os_path, resolve_type) in self._document_cache:
            raise RuntimeError(f"Duplicate cache key: {repr((os_path, resolve_type))}")

        self._document_cache[(os_path, resolve_type)] = data


@dataclass
class DocumentContext:
    """Contains context for a model loaded from a document
    tree. Used to resolve `DocumentRef` fields in models.

    See `DocumentRef.resolve()`.

    Attributes:
        docpath_root: Absolute path of the folder containing all related
            documents
        path: Path of a document within a document tree
    """

    doctree_ctx: DoctreeContext
    path: PurePosixPath

    @cached_property
    def os_path(self) -> Path:
        return (self.doctree_ctx.docpath_root / self.path).absolute().resolve()

    @classmethod
    def from_os_path(
        cls: type[Self], doctree_ctx: DoctreeContext, os_path: Path | str
    ) -> Self:
        """Create a root document context. Ensures that `docpath_root` is absolute,
        and that `path` is relative to `docpath_root`."""

        path = Path(os_path).absolute().resolve()

        try:
            doctree_path = PurePosixPath(path.relative_to(doctree_ctx.docpath_root))
        except ValueError as exc:
            raise ValueError(
                f"Document path '{path}' is not relative to document tree root path"
                f" '{doctree_ctx.docpath_root}'"
            ) from exc

        return cls(doctree_ctx, doctree_path)

    def make_reference_context(self, ref_path: PurePosixPath) -> "DocumentContext":
        if ref_path.is_absolute():
            doctree_path = ref_path.relative_to("/")
        else:
            doctree_path = self.path.parent / ref_path

        return DocumentContext(self.doctree_ctx, doctree_path)


class ReferenceValidationContext(TypedDict):
    """Pydantic context for reference validation."""

    document_context: DocumentContext
    resolve_refs: bool


def reference_validation_pydantic_context(
    document_context: DocumentContext, resolve_refs: bool
) -> dict[str, Any]:
    """Create a Pydantic context for reference validation and resolution."""
    return {
        "reference_context": {
            "document_context": document_context,
            "resolve_refs": resolve_refs,
        }
    }


def get_reference_validation_context(
    info: ValidationInfo,
) -> ReferenceValidationContext | None:
    """Get reference validation context from Pydantic context,
    if it was set."""
    if info.context:
        return info.context.get("reference_context")

    return None
