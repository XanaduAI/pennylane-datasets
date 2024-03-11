from collections.abc import Callable, Mapping, MutableSequence
from functools import cache, partial
from typing import Any

import pydantic.alias_generators
from pydantic import AfterValidator, BaseModel, ConfigDict


class CamelCaseMixin:
    """Mixin class for pydantic models that automatically aliases
    field names to 'camelCase'."""

    model_config = ConfigDict(
        alias_generator=pydantic.alias_generators.to_camel, populate_by_name=True
    )


@cache
def get_model_alias_mapping(model_cls: type[BaseModel]) -> Mapping[str, str]:
    """Return a mapping of field aliases for `model_cls`
    to the field name."""
    return {
        info.alias: name
        for name, info in model_cls.model_fields.items()
        if info.alias is not None
    }


def _sortedfield_validator(
    key: Callable[[Any], Any] | None, val: list[Any]
) -> MutableSequence[Any]:
    """Validator function for `SortedField`."""
    val.sort(key=key)

    return val


class SortedField(AfterValidator):
    """Pydantic validator for sorting a list field."""

    def __init__(self, key: Callable[[Any], Any] | None = None) -> None:
        """Pydantic validator for sorting a list field.

        Args:
            key: Key used for sort
        """
        super().__init__(partial(_sortedfield_validator, key))
