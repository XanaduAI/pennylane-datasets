import json
import warnings
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

from .doctree import (
    DoctreeContext,
    get_doctree_context,
    make_doctree_context,
)

ResolveType = TypeVar("ResolveType")


class DocumentRef(BaseModel, Generic[ResolveType]):
    """Model used to define fields that can reference another document in a
    document tree.

    Attributes:
        ref: Path to referenced document. If the path is relative (no leading '/')
            it will be resolved relative to the referencing document. If the path
            is absolute, it will be resolved relative to the root of the document
            tree.

    See `Document` for example usage.
    """

    model_config = ConfigDict(populate_by_name=True)

    ref: Annotated[PurePosixPath, Field(alias="$ref")]

    _document_context: Annotated[DoctreeContext, PrivateAttr()]

    @property
    def document_context(self) -> DoctreeContext:
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
        self,
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
        return _resolve_document_ref(self)


def _docref_validator(
    val: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
):
    ref: DocumentRef = handler(val)

    ctx = get_doctree_context(info.context)
    if ctx is None:
        return ref

    doc_ctx = ctx["document_context"]
    ref._document_context = doc_ctx.make_reference_context(ref.ref)

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
    field_name: str | None = None,
) -> Any:
    """Resolve a document reference.

    Args:
        ref: The document reference
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

    ctx = ref.document_context
    if existing := ctx.doctree.document_cache_get(ctx.os_path, resolve_type):
        return existing

    with open(ctx.os_path, "r", encoding="utf-8") as f:
        if ctx.path.suffix == ".json":
            data = json.load(f)
        else:
            data = f.read()

    resolved = TypeAdapter(resolve_type).validate_python(
        data, context=make_doctree_context(ctx, resolve_refs=True)
    )

    ctx.doctree.document_cache_update(ctx.os_path, resolve_type, resolved)

    return resolved
