from typing import Annotated, Any

from pydantic import (
    AwareDatetime,
    BeforeValidator,
    Field,
    PlainSerializer,
    SerializationInfo,
    TypeAdapter,
    ValidationError,
    ValidationInfo,
)

from ._base import CamelCaseModel, DocumentRef, DocumetRefMixin

_ParameterDefaultsAdapter = TypeAdapter(list[tuple[tuple[str, ...], str]])


def _validate_parameter_defaults(
    val: Any, info: ValidationInfo
) -> dict[tuple[str, ...], str]:
    if info.mode == "json":
        val_parsed = _ParameterDefaultsAdapter.validate_json(val)
    else:
        val_parsed = _ParameterDefaultsAdapter.validate_python(val)

    labels: list[str] = info.data["labels"]
    defaults: dict[tuple[str, ...], str] = {}

    for parameter_match, default_ in val_parsed:
        if len(parameter_match) >= len(labels):
            raise ValidationError(
                "Length of matched parameter values must be"
                " less than number of parameters."
            )

        if existing_match := defaults.get(parameter_match):
            raise ValidationError(
                f"Duplicate default for parameters {repr(parameter_match)}:"
                f" {repr(existing_match)}"
            )

        defaults[parameter_match] = default_

    return defaults


def _serialize_parameter_defaults(
    val: dict[tuple[str, ...], str], info: SerializationInfo
):
    val_list = [[match, default_] for match, default_ in val.items()]

    if info.mode_is_json():
        return _ParameterDefaultsAdapter.serializer.to_json(val_list)

    return _ParameterDefaultsAdapter.serializer.to_python(val_list)


class DatasetParameters(CamelCaseModel):
    labels: list[str]
    defaults: Annotated[
        dict[tuple[str, ...], str],
        Field(default_factory=dict),
        BeforeValidator(_validate_parameter_defaults),
        PlainSerializer(_serialize_parameter_defaults),
    ]


class DatasetData(CamelCaseModel):
    data_url: str
    parameter_values: dict[str, str] | None = None
    variables: dict[str, str] | None = None


class Dataset(CamelCaseModel, DocumetRefMixin):
    """Model for dataset family metadata."""

    title: str
    slug: str
    authors: list[str]
    tags: Annotated[list[str], Field(default_factory=list)]

    citation: str | DocumentRef[str]
    about: str | DocumentRef[str]
    meta: DocumentRef[dict[str, Any]] | dict[str, Any] | None = None
    type_: Annotated[str | None, Field(alias="type")]

    date_of_publication: AwareDatetime
    date_of_last_modification: AwareDatetime

    parameters: DatasetParameters | None = None
    data: list[DatasetData]
