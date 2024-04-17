from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path, PurePosixPath
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Hashable,
    Self,
    TypedDict,
    TypeVar,
)

from pydantic import PrivateAttr

if TYPE_CHECKING:
    from .document import Document


class DoctreeObj:
    _document_context: Annotated["DoctreeContext", PrivateAttr()]

    @property
    def document_context(self) -> "DoctreeContext":
        return self._document_context


DoctreeObjT = TypeVar("DoctreeObjT", bound=DoctreeObj)
DocumentT = TypeVar("DocumentT", bound="Document")


class Doctree:
    docpath_root: Path

    def __init__(self, docpath_root: Path | str) -> None:
        self.docpath_root = Path(docpath_root).absolute().resolve()

        self._document_cache = {}
        self._objects = defaultdict(list)
        self._documents = defaultdict(list)

    def get_documents(self) -> Mapping[type["Document"], Sequence["Document"]]:
        return self._documents

    def get_objects(self, type_: type[DoctreeObjT]) -> Sequence[DoctreeObjT]:
        return self._objects.get(type_, [])

    def document_cache_get(
        self, os_path: Path, resolve_type: type | Hashable
    ) -> Any | None:
        return self._document_cache.get((os_path, resolve_type))

    def document_cache_update(self, os_path, resolve_type: type | Hashable, data: Any):
        if (os_path, resolve_type) in self._document_cache:
            raise RuntimeError(f"Duplicate cache key: {repr((os_path, resolve_type))}")

        self._document_cache[(os_path, resolve_type)] = data


@dataclass
class DoctreeContext:
    """Contains context for a model loaded from a document
    tree. Used to resolve `DocumentRef` fields in models.

    See `DocumentRef.resolve()`.

    Attributes:
        doctree:
        path: Path of a document within a document tree
    """

    doctree: Doctree
    path: PurePosixPath

    @cached_property
    def os_path(self) -> Path:
        return (self.doctree.docpath_root / self.path).absolute().resolve()

    @classmethod
    def from_os_path(cls: type[Self], doctree: Doctree, os_path: Path | str) -> Self:
        """Create a root document context. Ensures that `docpath_root` is absolute,
        and that `path` is relative to `docpath_root`."""

        path = Path(os_path).absolute().resolve()

        try:
            doctree_path = PurePosixPath(path.relative_to(doctree.docpath_root))
        except ValueError as exc:
            raise ValueError(
                f"Document path '{path}' is not relative to document tree root path"
                f" '{doctree.docpath_root}'"
            ) from exc

        return cls(doctree, doctree_path)

    def make_reference_context(self, ref_path: PurePosixPath) -> "DoctreeContext":
        if ref_path.is_absolute():
            doctree_path = ref_path.relative_to("/")
        else:
            doctree_path = self.path.parent / ref_path

        return DoctreeContext(self.doctree, doctree_path)


class DoctreeValidationContext(TypedDict):
    """Pydantic context for document tree validation."""

    document_context: DoctreeContext
    resolve_refs: bool


def make_doctree_context(
    document_context: DoctreeContext, resolve_refs: bool
) -> dict[str, Any]:
    """Create a Pydantic context for reference validation and resolution."""
    return {
        "doctree": {
            "document_context": document_context,
            "resolve_refs": resolve_refs,
        }
    }


def get_doctree_context(pydantic_context: Any) -> DoctreeValidationContext | None:
    """Get reference validation context from Pydantic context,
    if it was set."""

    if pydantic_context:
        return pydantic_context.get("doctree")

    return None
