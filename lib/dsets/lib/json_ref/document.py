import json
import typing
import warnings
from collections.abc import Hashable, Mapping
from pathlib import Path
from typing import Annotated, Any, Self

from pydantic import (
    BaseModel,
    PrivateAttr,
    TypeAdapter,
    ValidationInfo,
    model_validator,
)

from .context import DocumentContext
from .reference import DocumentRef, ResolveType


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
            json.dump({"created_at": "2024-03-05T16:44:35.176071Z"}, f)

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
            docpath_root="data/",
            resolve_refs=True)

        >>> model
        Model(
            name='model',
            citation='Me, September',
            about='This is a model!',
            reference=ReferencedModel(
                name='referenced',
                user_list=UserList(users=['A. User', 'Foo']),
                meta={'created_at': '2024-03-05T16:44:35.176071Z'}
            )
        )
    """

    _document_context: Annotated[DocumentContext | None, PrivateAttr()] = None

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
        cls: type[Self],
        docpath_root: Path | str,
        path: Path | str,
        resolve_refs: bool = False,
    ) -> Self:
        """Validate a document from a document tree.

        Args:
            docpath_root: Root path for resolving document references
            path: Path to the document
            resolve_refs: Whether document refs should be resolved.

        Returns: Model instance
        """
        ctx = DocumentContext.create(docpath_root, path)

        with open(path, "r", encoding="utf-8") as f:
            ret = typing.cast(
                Self,
                cls.model_validate_json(f.read(), context=ctx.pydantic_context),
            )

        if resolve_refs:
            ret.resolve_document_refs()

        return ret

    def resolve_document_refs(self: Self) -> Self:
        """Resolve all unresolved document refs on this instance.

        If any of the referenced also contain document references,
        they will be recursively resolved."""
        for field_name in self.model_fields:
            attr = getattr(self, field_name)

            if isinstance(attr, DocumentTreeModel):
                attr.resolve_document_refs()
            elif isinstance(attr, DocumentRef):
                setattr(self, field_name, _resolve_document_ref(attr, self, field_name))

        return self

    @model_validator(mode="after")
    def _set_document_context(self: Self, info: ValidationInfo) -> Self:
        """Model validator called after `_validate_document_refs`. Sets the document
        context.
        """
        if ctx := DocumentContext.from_pydantic_info(info):
            self._document_context = ctx

        # for field_name in self.model_fields:
        #    attr = getattr(self, field_name)

        return self


def get_document_context(doc: DocumentTreeModel) -> DocumentContext | None:
    """Get document context from `doc`, if it has one."""
    try:
        return doc.document_context
    except RuntimeError:
        return None


def _resolve_document_ref(
    ref: DocumentRef[ResolveType], parent: DocumentTreeModel, field_name: str
) -> Any:
    """Resolve a document reference.

    Args:
        ref: The document reference
        parent: Model containing the document reference
        field_name: Name of the field the document reference is assigned to.
    """
    ctx = DocumentContext.from_referencing_context(parent.document_context, ref.ref)
    try:
        resolve_type = ref.resolve_type()
    except TypeError as exc:
        warnings.warn(
            "Could not determine resolve type for document ref"
            f" '{type(parent).__name__}.{field_name}'.",
            source=exc,
        )
        resolve_type = Any

    if existing := _document_cache_get(ctx, resolve_type):
        return existing

    with open(ctx.path, "r", encoding="utf-8") as f:
        if ctx.path.suffix == ".json":
            data = json.load(f)
        else:
            data = f.read()

    resolved = TypeAdapter(resolve_type).validate_python(
        data, context=ctx.pydantic_context
    )

    _document_cache_update(ctx, resolve_type, resolved)
    if isinstance(resolved, DocumentTreeModel):
        resolved.resolve_document_refs()

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
