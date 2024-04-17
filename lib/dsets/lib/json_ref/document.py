import typing
from collections.abc import Mapping
from pathlib import Path
from typing import Self

from pydantic import BaseModel

from .doctree import (
    Doctree,
    DoctreeContext,
    DoctreeObj,
    get_doctree_context,
    make_doctree_context,
)
from .reference import DocumentRef


class Document(BaseModel, DoctreeObj):
    """Base class for Pydantic models in a document tree, that
    can contain `Reference` fields referencing other documents.

    Example:

        Example of three inter-related models, using a mix of absolute
        and relative references.

        class UserList(BaseModel):

            users: list[str]

        class ReferencedModel(Document):

            name: str
            user_list: Reference[UserList]
            meta: Reference[dict[str, Any]]

        class Model(Document):

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
    def from_os_path(
        cls: type[Self],
        doctree: Doctree,
        path: Path | str,
        resolve_refs: bool = False,
    ) -> Self:
        """Validate a document from a document tree.

        Args:
            doctree: Document tree context
            path: Real path to the document
            resolve_refs: Whether document refs should be resolved.

        Returns: Model instance
        """
        document_ctx = DoctreeContext.from_os_path(doctree, path)

        with open(path, "r", encoding="utf-8") as f:
            ret = typing.cast(
                Self,
                cls.model_validate_json(
                    f.read(),
                    context=make_doctree_context(document_ctx, resolve_refs),
                ),
            )

        return ret

    def model_post_init(self, __context: typing.Any) -> None:
        if ctx := get_doctree_context(__context):
            self._document_context = ctx["document_context"]
            ctx["document_context"].doctree._objects[type(self)].append(self)
            ctx["document_context"].doctree._documents[type(self)].append(self)

        return super().model_post_init(__context)
