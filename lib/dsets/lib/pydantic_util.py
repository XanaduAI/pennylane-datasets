from collections.abc import Mapping
from functools import cache

import pydantic.alias_generators
from pydantic import BaseModel, ConfigDict


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
