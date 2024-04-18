import json
import warnings
from typing import Annotated, Any, Generic, TypeVar, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Field,
    Tag,
    TypeAdapter,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)
from typing_extensions import TypeAliasType

from .doctree import (
    DocPathAbsolute,
    DocPathRelative,
    DoctreeContext,
    DoctreeObj,
    get_doctree_context,
    make_doctree_context,
    set_document_context,
)

ResolveType = TypeVar("ResolveType")


class Reference(BaseModel, DoctreeObj, Generic[ResolveType]):
    """Model used to define fields that may reference another file in a
    document tree.

    Attributes:
        ref: Docpath to referenced file. If the path is relative it will be resolved
            relative to the referencing document. If the path is absolute, it will be
            resolved relative to the root of the document tree.

    See `Document` for example usage.
    """

    model_config = ConfigDict(populate_by_name=True)

    ref: Annotated[DocPathAbsolute | DocPathRelative, Field(alias="$ref")]

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

        Returns:
            ResolveType: Resolved reference

        Raises:
            FileNotFoundError: if the referenced document could not be found
            RuntimeError: if `self.document_context` is unset.
        """
        return _resolve_reference(self)

    def model_post_init(self, __context: Any) -> None:
        set_document_context(self, __context)
        return super().model_post_init(__context)


def _reference_validator(
    val: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
):
    ref: Reference = handler(val)

    ctx = get_doctree_context(info.context)
    if ctx is None:
        return ref

    if ctx["resolve_refs"]:
        return _resolve_reference(ref, field_name=info.field_name)

    return ref


def _reference_discriminator(v: Any) -> str:
    """Pydantic discriminator for determining whether a reference field
    is a reference or a value.

    See:
    https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions-with-callable-discriminator
    """
    if isinstance(v, Reference):
        return "ref"

    try:
        if v.keys() == {"$ref"}:
            return "ref"
    except AttributeError:
        pass

    return "value"


"""Pydantic field type for fields that may contain refs.
Uses `TypeAliasType` from typing extensions. See:
https://docs.pydantic.dev/latest/concepts/types/#named-type-aliases
"""
Ref = TypeAliasType(
    "Ref",
    Annotated[
        Union[
            Annotated[
                Annotated[Reference[ResolveType], WrapValidator(_reference_validator)],
                Tag("ref"),
            ],
            Annotated[ResolveType, Tag("value")],
        ],
        Discriminator(_reference_discriminator),
    ],
    type_params=(ResolveType,),
)


def _resolve_reference(
    ref: Reference[ResolveType],
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

    referencing_ctx = ref.document_context
    doctree = referencing_ctx.doctree

    docpath = referencing_ctx.resolve_reference_path(ref.ref)
    os_path = doctree.get_os_path(docpath)

    if existing := doctree.object_cache_get(os_path, resolve_type):
        return existing

    with open(os_path, "r", encoding="utf-8") as f:
        if os_path.suffix == ".json":
            data = json.load(f)
        else:
            data = f.read()

    resolved = TypeAdapter(resolve_type).validate_python(
        data,
        context=make_doctree_context(
            DoctreeContext.from_os_path(doctree, os_path), resolve_refs=True
        ),
    )

    doctree.object_cache_update(os_path, resolve_type, resolved)

    return resolved
