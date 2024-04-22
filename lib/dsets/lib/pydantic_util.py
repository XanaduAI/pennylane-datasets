import pydantic.alias_generators
from pydantic import ConfigDict


class CamelCaseMixin:
    """Mixin class for pydantic models that automatically aliases
    field names to 'camelCase'."""

    model_config = ConfigDict(
        alias_generator=pydantic.alias_generators.to_camel, populate_by_name=True
    )
