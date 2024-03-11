import json
import warnings
from collections.abc import Hashable
from pathlib import PurePosixPath
from typing import Annotated, Any, Generic, TypeVar, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Field,
    PrivateAttr,
    Tag,
    TypeAdapter,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)
from typing_extensions import TypeAliasType

from .context import (
    DocumentContext,
    get_reference_validation_context,
    reference_validation_pydantic_context,
)

ResolveType = TypeVar("ResolveType")


class DocumentRef(BaseModel, Generic[ResolveType]):
    """Model used to define fields that can reference another document in a
    document tree.

    Attributes:
        ref: Path to referenced document. If the path is relative (no leading '/')
            it will be resolved relative to the referencing document. If the path
            is absolute, it will be resolved relative to the root of the document
            tree (`DocumentContext.root`)

    See `DocumentTreeModel` for example usage.
    """

    model_config = ConfigDict(populate_by_name=True)

    ref: Annotated[PurePosixPath, Field(alias="$ref")]

    _document_context: Annotated[DocumentContext | None, PrivateAttr()] = None

    @property
    def document_context(self) -> DocumentContext:
        """The context from which this reference was loaded."""
        if (ctx := self._document_context) is None:
            raise RuntimeError(f"'{repr(self)}' does not have a document context")

        return ctx

    @classmethod
    def resolve_type(cls) -> type[ResolveType]:
        """Get the resolve type for this class from its type annotation."""
        try:
            return cls.__pydantic_generic_metadata__["args"][0]
        except (KeyError, IndexError) as exc:
            raise TypeError(
                f"Could not determine resolve type for {repr(cls)}"
            ) from exc

    def resolve(
        self, *, document_context: DocumentContext | None = None
    ) -> ResolveType:
        """Resolve this reference.

        Args:
            document_context: Context to use for resolving this reference. If
                unset, `self.document_context` will be used

        Returns:
            ResolveType: Resolved reference

        Raises:
            FileNotFoundError: if the referenced document could not be found
            RuntimeError: if `document_context` is `None` and `self.document_context`
                is unset.
        """
        return _resolve_document_ref(self, document_context=document_context)


def _docref_validator(
    val: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
):
    ref: DocumentRef = handler(val)

    ctx = get_reference_validation_context(info)
    if ctx is None:
        return ref

    ref._document_context = DocumentContext.from_referencing_context(
        ctx["document_context"], ref.ref
    )

    if ctx["resolve_refs"]:
        return _resolve_document_ref(ref, field_name=info.field_name)

    return ref


def _reference_discriminator(v: Any) -> str:
    """Pydantic discriminator for determining whether a reference field
    is a reference or a value.

    See:
    https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions-with-callable-discriminator
    """
    if isinstance(v, DocumentRef):
        return "ref"

    try:
        if v.keys() == {"$ref"}:
            return "ref"
    except AttributeError:
        pass

    return "value"


"""Pydantic field type for fields that may contain document refs.
Uses `TypeAliasType` from typing extensions. See:
https://docs.pydantic.dev/latest/concepts/types/#named-type-aliases
"""
Reference = TypeAliasType(
    "Reference",
    Annotated[
        Union[
            Annotated[
                Annotated[DocumentRef[ResolveType], WrapValidator(_docref_validator)],
                Tag("ref"),
            ],
            Annotated[ResolveType, Tag("value")],
        ],
        Discriminator(_reference_discriminator),
    ],
    type_params=(ResolveType,),
)


def _resolve_document_ref(
    ref: DocumentRef[ResolveType],
    document_context: DocumentContext | None = None,
    field_name: str | None = None,
) -> Any:
    """Resolve a document reference.

    Args:
        ref: The document reference
        document_context: Alternative context
        field_name: Name of the field the document reference is assigned to.
    """
    try:
        resolve_type = ref.resolve_type()
    except TypeError as exc:
        warnings.warn(
            "Could not determine resolve type for document ref"
            f" on field '{field_name}'.",
            source=exc,
        )
        resolve_type = Any

    ctx = document_context or ref.document_context
    if existing := _document_cache_get(ctx, resolve_type):
        return existing

    with open(ctx.path, "r", encoding="utf-8") as f:
        if ctx.path.suffix == ".json":
            data = json.load(f)
        else:
            data = f.read()

    resolved = TypeAdapter(resolve_type).validate_python(
        data, context=reference_validation_pydantic_context(ctx, resolve_refs=True)
    )

    _document_cache_update(ctx, resolve_type, resolved)

    return resolved


_DOCUMENT_CACHE = {}


def _document_cache_get(
    ctx: DocumentContext, resolve_type: type | Hashable
) -> Any | None:
    """Returns a global cache of resolved documents."""
    global _DOCUMENT_CACHE

    return _DOCUMENT_CACHE.get((ctx, resolve_type))


def _document_cache_update(
    ctx: DocumentContext, resolve_type: type | Hashable, resolved: Any
) -> None:
    global _DOCUMENT_CACHE

    _DOCUMENT_CACHE[(ctx, resolve_type)] = resolved
