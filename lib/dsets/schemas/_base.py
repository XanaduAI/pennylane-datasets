import json
import typing
from collections.abc import Mapping
from dataclasses import dataclass
from functools import cache
from logging import getLogger
from pathlib import Path, PurePosixPath
from typing import Annotated, Any, Generic, Literal, Self, TypeVar

import pydantic.alias_generators
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    TypeAdapter,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    model_serializer,
    model_validator,
)

logger = getLogger(__name__)


class CamelCaseModel(BaseModel):
    """Base class for models that automatically aliases
    field names to 'camelCase'."""

    model_config = ConfigDict(
        alias_generator=pydantic.alias_generators.to_camel, populate_by_name=True
    )


@dataclass
class DocumentContext:
    root: Path
    path: Path
    resolve_refs: bool = False

    @property
    def pydantic_context(self: Self) -> dict[str, Any]:
        return {"document_context": self}

    @classmethod
    def from_pydantic_info(cls: type[Self], info: ValidationInfo) -> Self | None:
        if info.context:
            return info.context.get("document_context")

        return None


ResolveType = TypeVar("ResolveType")


class DocumentRef(CamelCaseModel, Generic[ResolveType]):
    path: PurePosixPath
    content_type: Literal["text", "json", None] = None

    def resolve(self, parent_context: DocumentContext) -> ResolveType:
        if self.path.is_absolute():
            abs_path = parent_context.root / self.path.relative_to("/")
        else:
            abs_path = parent_context.path.parent / self.path

        content_type = self.content_type
        if content_type is None:
            if self.path.suffix == ".json":
                content_type = "json"
            else:
                content_type = "text"

        with open(abs_path, "r", encoding="utf-8") as f:
            if content_type == "json":
                data = json.load(f)
            else:
                data = f.read()

        try:
            resolve_type = self.__pydantic_generic_metadata__["args"][0]
        except (KeyError, IndexError):
            logger.warn(
                f"Could not determine resolve type for document ref {repr(self)}"
            )
            return data

        ctx = DocumentContext(
            parent_context.root, abs_path, resolve_refs=parent_context.resolve_refs
        )

        return TypeAdapter(resolve_type).validate_python(
            data, context=ctx.pydantic_context
        )


@cache
def _get_alias_mapping(model_cls: type[BaseModel]) -> Mapping[str, str]:
    """Return a mapping of field aliases for `model_cls`
    to the field name."""
    return {
        info.alias: name
        for name, info in model_cls.model_fields.items()
        if info.alias is not None
    }


class DocumetRefMixin(BaseModel):
    _document_context: Annotated[DocumentContext | None, Field(exclude=True)] = None

    @property
    def document_context(self) -> DocumentContext:
        if (ctx := self._document_context) is None:
            raise RuntimeError("Instance does not have a document context")

        return ctx

    @property
    def document_refs(self) -> Mapping[str, DocumentRef[Any]]:
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
        cls: type[Self], path: Path, doc_root: Path, resolve_refs: bool = False
    ) -> Self:
        with open(path, "r", encoding="utf-8") as f:
            ret = typing.cast(
                Self,
                cls.model_validate_json(
                    f.read(),
                    context=DocumentContext(
                        root=doc_root, path=path, resolve_refs=resolve_refs
                    ).pydantic_context,
                ),
            )

        return ret

    def _resolve_document_refs(self: Self) -> Self:
        ctx = self.document_context
        for field_name, ref in self.document_refs.items():
            setattr(self, field_name, ref.resolve(ctx))

        return self

    @model_validator(mode="wrap")
    @classmethod
    def _get_document_refs(
        cls: type[Self], data_in: Any, handler: ValidatorFunctionWrapHandler
    ) -> Any:
        if not isinstance(data_in, Mapping):
            return handler(data_in)

        field_aliases = _get_alias_mapping(cls)

        data: dict[str, Any] = {}
        ref_attrs: list[str] = []

        for key, val in data_in.items():
            if key.startswith("$"):
                key = key.lstrip("$")
                data[key] = val
                ref_attrs.append(field_aliases.get(key, key))
            else:
                data[key] = val

        model = handler(data)

        for ref_attr in ref_attrs:
            setattr(
                model, ref_attr, DocumentRef.model_validate(getattr(model, ref_attr))
            )

        return model

    @model_validator(mode="after")
    def _set_document_context(self: Self, info: ValidationInfo) -> Self:
        if ctx := DocumentContext.from_pydantic_info(info):
            self._document_context = ctx

            if ctx.resolve_refs:
                self._resolve_document_refs()

        return self

    @model_serializer(mode="wrap", when_used="json")
    def _serialize_document_refs(
        self: Self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Any:
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
