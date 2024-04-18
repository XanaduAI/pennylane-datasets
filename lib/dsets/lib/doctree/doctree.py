from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path, PurePosixPath
from typing import Any, Hashable, NewType, Self, TypedDict, TypeGuard, TypeVar

from .object import DoctreeObj

DoctreeObjT = TypeVar("DoctreeObjT", bound=DoctreeObj)

DocPath = PurePosixPath
DocPathRelative = NewType("DocPathRelative", DocPath)
DocPathAbsolute = NewType("DocPathAbsolute", DocPath)


def docpath_is_absolute(path: DocPath) -> TypeGuard[DocPathAbsolute]:
    return path.is_absolute()


class Doctree:
    docpath_root: Path

    def __init__(self, docpath_root: Path | str) -> None:
        self.docpath_root = Path(docpath_root).absolute().resolve()

        self._object_cache: dict[tuple[Path, type | Hashable], Any] = {}
        self._objects: dict[type[DoctreeObj], list[DoctreeObj]] = defaultdict(list)

    def get_os_path(self, docpath: DocPathAbsolute) -> Path:
        return self.docpath_root / docpath.relative_to("/")

    def get_objects(self, type_: type[DoctreeObjT]) -> Sequence[DoctreeObjT]:
        return self._objects.get(type_, [])

    def object_cache_get(
        self, os_path: Path, resolve_type: type | Hashable
    ) -> Any | None:
        return self._object_cache.get((os_path, resolve_type))

    def object_cache_update(
        self, os_path: Path, resolve_type: type | Hashable, data: Any
    ):
        if (os_path, resolve_type) in self._object_cache:
            raise RuntimeError(f"Duplicate cache key: {repr((os_path, resolve_type))}")

        self._object_cache[(os_path, resolve_type)] = data


@dataclass
class DoctreeContext:
    """Contains context for a model loaded from a document
    tree. Used to resolve references and local assets.

    Attributes:
        doctree: Document tree that contains this model
        path: Absolute document path of the source file
    """

    doctree: Doctree
    path: DocPathAbsolute

    @cached_property
    def os_path(self) -> Path:
        return (
            (self.doctree.docpath_root / self.path.relative_to("/"))
            .absolute()
            .resolve()
        )

    @classmethod
    def from_os_path(cls: type[Self], doctree: Doctree, os_path: Path | str) -> Self:
        """Create a context for document loaded from ``os_path``.

        Args:
            doctree: Document tree
            os_path: Path of document. Must be within ``doctree.root``.

        Returns:
            New context
        """
        try:
            docpath = (
                Path(os_path).absolute().resolve().relative_to(doctree.docpath_root)
            )
        except ValueError as exc:
            raise ValueError(
                f"Document path '{os_path}' is not relative to document tree root path"
                f" '{doctree.docpath_root}'"
            ) from exc

        return cls(doctree, DocPath("/", docpath))

    def resolve_reference_path(self, ref_docpath: DocPath) -> DocPathAbsolute:
        """Return ``ref_path`` relative to this context."""
        if docpath_is_absolute(ref_docpath):
            return ref_docpath

        return self.path.parent / ref_docpath

    def make_reference_context(self, ref_docpath: DocPath) -> "DoctreeContext":
        """Return a new context for a docpath that is either relative to this
        context, or absolute."""
        return DoctreeContext(self.doctree, self.resolve_reference_path(ref_docpath))


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


def get_doctree_context(
    pydantic_context: DoctreeValidationContext | Any,
) -> DoctreeValidationContext | None:
    """Get reference validation context from Pydantic context,
    if it was set."""

    if pydantic_context:
        return pydantic_context.get("doctree")

    return None


def set_document_context(
    obj: DoctreeObj, pydantic_context: DoctreeValidationContext | Any
) -> DoctreeContext | None:
    if ctx := get_doctree_context(pydantic_context):
        obj._document_context = ctx["document_context"]
        ctx["document_context"].doctree._objects[type(obj)].append(obj)

        return ctx["document_context"]

    return None
