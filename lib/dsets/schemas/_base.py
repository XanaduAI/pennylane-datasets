import json
import typing
import warnings
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Annotated, Any, Self, TypeVar

import pydantic.fields
from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Field,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    Tag,
    TypeAdapter,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    model_validator,
)

from ._pydantic_util import get_model_alias_mapping


@dataclass
class DocumentContext:
    """Contains context for a model loaded from a document
    tree. Used to resolve `DocumentRef` fields in models.

    See `DocumentRef.resolve()`.

    Attributes:
        doctree_root: Absolute path of the folder containing all related
            documents
        path: Path of a document within a document tree. May
            be relative to the current working directory, or
            `root`.
    """

    doctree_root: Path
    path: Path

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


ResolveType = TypeVar("ResolveType")


class DocumentRef(BaseModel):
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


def _reference_discriminator(v: Any) -> str:
    if isinstance(v, DocumentRef):
        return "ref"

    try:
        if v.keys() == {"$ref"}:
            return "ref"
    except AttributeError:
        pass

    return "value"


"""Pydantic field type for fields that may contain document refs."""
Reference = Annotated[
    Annotated[DocumentRef, Tag("ref")] | Annotated[ResolveType, Tag("value")],
    Discriminator(_reference_discriminator),
]


class DocumentTreeModel(BaseModel):
    """Base class for Pydantic models in a document tree, that
    can contain `Reference` fields referencing other documents.


    Example:

        Example of three inter-related models, using a mix of absolute
        and relative references.

        class UserList(BaseModel):

            users: list[str]

        class ReferencedModel(DocumentTreeModel):

            name: str
            user_list: Reference[UserList]
            meta: Reference[dict[str, Any]]

        class Model(DocumentTreeModel):

            name: str
            citation: Reference[str]
            about: Reference[str]
            reference: Reference[ReferencedModel]


        with open("data/users/userlist.json", "w") as f:
            json.dump({"users": ["A. User", "Foo"]}, f)

        with open("data/models/meta.json", "w") as f:
            json.dump({"created_at": datetime.now().isoformat()}, f)

        with open("data/models/referenced_model.json", "w") as f:
            json.dump(
                {
                    "name": "referenced",
                    "user_list": {"$ref": "/users/userlist.json"}, # Absolute path
                    "meta": {"$ref": "meta.json"}
                }, f)

        with open("data/models/about.txt", "w") as f:
            f.write("This is a model!")

        with open("data/models/model.json", "w") as f:
            json.dump(
                {
                    "name": "model",
                    "citation": "Me, September",
                    "about": {"$ref": "about.txt"},
                    "reference": {"$ref": "referenced_model.json"}
                }

        model = Model.load_from_path(
            path="data/models/model.json",
            doctree_root="data/",
            resolve_refs=True)


    """

    _document_context: Annotated[DocumentContext | None, Field(exclude=True)] = None

    @property
    def document_context(self) -> DocumentContext:
        """The context from which this document was loaded."""
        if (ctx := self._document_context) is None:
            raise RuntimeError("Instance does not have a document context")

        return ctx

    @property
    def document_refs(self) -> Mapping[str, DocumentRef]:
        """Mapping of attributes with unresolved document refs."""
        return {
            field_name: ref
            for field_name, ref in (
                (field_name, getattr(self, field_name))
                for field_name in self.model_fields_set
            )
            if isinstance(ref, DocumentRef)
        }

    @classmethod
    def load_from_path(
        cls: type[Self], path: Path, doctree_root: Path, resolve_refs: bool = False
    ) -> Self:
        """Validate a document from a document tree.

        Args:
            path: Path to the document
            doctree_root: Path to the document tree that contains this
                document
            resolve_refs: Whether document refs should be resolved.

        Returns: Model instance
        """
        path = Path(path)
        doctree_root = Path(doctree_root)

        with open(path, "r", encoding="utf-8") as f:
            ret = typing.cast(
                Self,
                cls.model_validate_json(
                    f.read(),
                    context=DocumentContext(
                        doctree_root=doctree_root, path=path
                    ).pydantic_context,
                ),
            )

        if resolve_refs:
            ret.resolve_document_refs()

        return ret

    def resolve_document_refs(self: Self) -> Self:
        """Resolve all unresolved document refs on this instance.

        If any of the referenced also contain document references,
        they will be recursively resolved."""
        for field_name, ref in self.document_refs.items():
            setattr(self, field_name, _resolve_document_ref(ref, self, field_name))

        return self

    # @model_validator(mode="wrap")
    @classmethod
    def _validate_document_refs(
        cls: type[Self],
        data_in: Any,
        handler: ValidatorFunctionWrapHandler,
    ) -> Any:
        """Model validator for loading documents with references. Wraps the default
        pydantic validator.
        """
        if not isinstance(data_in, Mapping):
            return handler(data_in)

        field_aliases = get_model_alias_mapping(cls)

        data: dict[str, Any] = {}

        for key, val in data_in.items():
            if key.startswith("$"):
                key = key.lstrip("$")
                field_name = field_aliases.get(key, key)

                try:
                    field_info = cls.model_fields[field_name]
                    ref_type = DocumentRef[_resolve_type_from_field_info(field_info)]
                except (KeyError, TypeError) as exc:
                    warnings.warn(
                        f"Could not determine resolve type for field '{cls.__name__}.{field_name}'. "
                        " Defaulting to 'str'.",
                        source=exc,
                    )
                    ref_type = DocumentRef[str]

                data[key] = ref_type.model_validate(val)
            else:
                data[key] = val

        return handler(data)

    @model_validator(mode="after")
    def _set_document_context(self: Self, info: ValidationInfo) -> Self:
        """Model validator called after `_validate_document_refs`. Sets the document
        context.
        """
        if ctx := DocumentContext.from_pydantic_info(info):
            self._document_context = ctx

        return self

    # @model_serializer(mode="wrap", when_used="json")
    def _serialize_document_refs(
        self: Self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Any:
        """Model serializer wrapping the default Pydantic serializer. Prefixes
        any fields containing document refs with '$' in the serialized doc."""
        ref_fields = [
            field_name
            for field_name in self.model_fields
            if isinstance(getattr(self, field_name), DocumentRef)
        ]
        jsonable = handler(self)

        for field_name in ref_fields:
            if info.by_alias:
                ser_key = self.model_fields[field_name].alias or field_name
            else:
                ser_key = field_name

            jsonable[f"${ser_key}"] = jsonable.pop(ser_key)

        return jsonable


def _resolve_document_ref(
    ref: DocumentRef, parent: DocumentTreeModel, field_name: str
) -> Any:
    """Resolve a document reference.

    Args:
        ref: The document reference
        parent: Model containing the document reference
        field_name: Name of the field the document reference is assigned to.
    """
    if ref.ref.is_absolute():
        tree_path = parent.document_context.doctree_root / ref.ref.relative_to("/")
    else:
        tree_path = parent.document_context.path.parent / ref.ref

    if ref.ref.suffix == ".json":
        content_type = "json"
    else:
        content_type = "text"

    with open(tree_path, "r", encoding="utf-8") as f:
        if content_type == "json":
            data = json.load(f)
        else:
            data = f.read()

    try:
        resolve_type = _resolve_type_from_field_info(parent.model_fields[field_name])
    except (KeyError, TypeError) as exc:
        warnings.warn(
            "Could not determine resolve type for document ref"
            f" '{type(parent).__name__}.{field_name}'.",
            source=exc,
        )
        return data

    resolved = TypeAdapter(resolve_type).validate_python(
        data,
        context=DocumentContext(
            parent.document_context.doctree_root, tree_path
        ).pydantic_context,
    )

    if isinstance(resolved, DocumentTreeModel):
        resolved.resolve_document_refs()

    return resolved


def _resolve_type_from_field_info(info: pydantic.fields.FieldInfo) -> type:
    """Attempt to derive the `ResolveType` argument to a pydantic field annotated
    with `Reference`.

    Raises:
        TypeError: if the annotation is not compatible with `Reference`.
    """
    try:
        return typing.get_args(info.annotation)[1]
    except IndexError as exc:
        raise TypeError(
            "Field annotation is not compatible with `Reference[ResolveType]`:"
            f" {repr(info.annotation)}"
        ) from exc
