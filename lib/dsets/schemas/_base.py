import json
import typing
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Generic, Literal, Self, TypeVar

import pydantic.alias_generators
from pydantic import (
    BaseModel,
    ConfigDict,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    TypeAdapter,
    ValidationError,
    ValidationInfo,
    model_serializer,
    model_validator,
)


class CamelCaseModel(BaseModel):
    """Base class for models that automatically aliases
    field names to 'camelCase'."""

    model_config = ConfigDict(
        alias_generator=pydantic.alias_generators.to_camel, populate_by_name=True
    )


ResolveType = TypeVar("ResolveType")


class DocumentRef(CamelCaseModel, Generic[ResolveType]):
    path: PurePosixPath
    content_type: Literal["text", "json", None] = None

    def resolve(self, datasets_root: Path, referencing_doc_path: Path) -> ResolveType:
        if self.path.is_absolute():
            abs_path = datasets_root / self.path
        else:
            abs_path = referencing_doc_path.parent / self.path

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
            return data

        return TypeAdapter(resolve_type).validate_python(data)


@dataclass
class DocumentSerializationContext:
    datasets_root: Path
    document_path: Path
    resolve_refs: bool

    @classmethod
    def get(cls: type[Self], info: ValidationInfo) -> Self | None:
        if info.context:
            return info.context.get("dataset_context")

        return None


class DocumetRefMixin:
    @classmethod
    def load_from_path(
        cls: type[Self],
        document_path: Path,
        datasets_root: Path,
        resolve_refs: bool = False,
    ) -> Self:
        cls_ = typing.cast(BaseModel, cls)
        ctx = DocumentSerializationContext(datasets_root, document_path, resolve_refs)

        with open(document_path, "r", encoding="utf-8") as f:
            return typing.cast(
                Self,
                cls_.model_validate_json(f.read(), context={"dataset_context": ctx}),
            )

    @model_validator(mode="before")
    @classmethod
    def _get_document_refs(cls: type[Self], data_in: Any) -> Any:
        data_out: dict[str, Any] = {}
        if not isinstance(data_in, Mapping):
            return data_in

        for key, val in data_in.items():
            if key.startswith("$"):
                data_out[key.lstrip("$")] = val
            else:
                data_out[key] = val

        return data_out

    @model_validator(mode="after")
    def _resolve_document_refs(self: Self, info: ValidationInfo) -> Self:
        if (
            ctx := DocumentSerializationContext.get(info)
        ) is None or not ctx.resolve_refs:
            return self

        self_ = typing.cast(BaseModel, self)

        for field in self_.model_fields_set:
            if isinstance(ref := getattr(self, field), DocumentRef):
                try:
                    resolved = ref.resolve(ctx.datasets_root, ctx.document_path)
                except FileNotFoundError as exc:
                    raise ValidationError(
                        f"Could not resolve document ref: {ref.path}"
                    ) from exc

                setattr(self, field, resolved)

        return self

    @model_serializer(mode="wrap", when_used="json")
    def _serialize_document_refs(
        self: Self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Any:
        self_ = typing.cast(BaseModel, self)

        ref_fields = [
            field_name
            for field_name in self_.model_fields
            if isinstance(getattr(self_, field_name), DocumentRef)
        ]
        jsonable = handler(self)

        for field_name in ref_fields:
            if info.by_alias:
                ser_key = self_.model_fields[field_name].alias or field_name
            else:
                ser_key = field_name

            jsonable[f"${ser_key}"] = jsonable.pop(ser_key)

        return jsonable
