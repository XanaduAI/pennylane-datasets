from pathlib import PurePosixPath
from typing import Annotated, Any, Generic, TypeVar, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Field,
    Tag,
)
from typing_extensions import TypeAliasType

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

    ref: Annotated[PurePosixPath, Field(alias="$ref", serialization_alias="$ref")]

    @classmethod
    def resolve_type(cls) -> type[ResolveType]:
        """Get the resolve type for this class from its type annotation."""
        try:
            return cls.__pydantic_generic_metadata__["args"][0]
        except (KeyError, IndexError) as exc:
            raise TypeError(
                f"Could not determine resolve type for {repr(cls)}"
            ) from exc


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
            Annotated[DocumentRef[ResolveType], Tag("ref")],
            Annotated[ResolveType, Tag("value")],
        ],
        Discriminator(_reference_discriminator),
    ],
    type_params=(ResolveType,),
)
