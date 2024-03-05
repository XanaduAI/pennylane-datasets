from typing import Annotated, Any

from pydantic import (
    BeforeValidator,
    Field,
    PlainSerializer,
    SerializationInfo,
    TypeAdapter,
    ValidationError,
    ValidationInfo,
)

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


ParameterDefaults = Annotated[
    dict[tuple[str, ...], str],
    Field(default_factory=dict),
    BeforeValidator(_validate_parameter_defaults),
    PlainSerializer(_serialize_parameter_defaults),
]
