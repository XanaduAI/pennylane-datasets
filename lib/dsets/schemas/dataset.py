from typing import Annotated, Self

from pydantic import (
    AwareDatetime,
    BaseModel,
    Field,
    ValidationError,
    model_validator,
)

from ._base import DocumentTreeModel, Reference
from ._fields import ParameterDefaults
from ._pydantic_util import CamelCaseMixin


class DatasetAttribute(BaseModel, CamelCaseMixin):
    name: str
    python_type: str
    doc: str
    optional: bool = False


class DatasetType(DocumentTreeModel, CamelCaseMixin):
    name: str
    attribute_list: list[DatasetAttribute]
    doc: str | None = None

    @property
    def attributes(self) -> dict[str, DatasetAttribute]:
        return {attribute.name: attribute for attribute in self.attribute_list}

    @model_validator(mode="after")
    def _validate_attribute_list(self: Self) -> Self:
        attr_names = set()
        for attr in self.attribute_list:
            if attr.name in attr_names:
                raise ValidationError(f"Duplicate attribute name: {attr.name}")

        return self


class DatasetData(BaseModel, CamelCaseMixin):
    data_url: str
    parameter_values: dict[str, str] | None = None
    variables: dict[str, str] | None = None


class Dataset(DocumentTreeModel, CamelCaseMixin):
    """Model for dataset.json file."""

    slug: str
    title: str
    type_: Annotated[Reference[DatasetType] | None, Field(alias="type")]

    authors: list[str]
    tags: Annotated[list[str], Field(default_factory=list)]

    citation: Reference[str]
    about: Reference[str]

    date_of_publication: AwareDatetime
    date_of_last_modification: AwareDatetime

    parameter_labels: Annotated[list[str], Field(default_factory=list)]
    parameter_defaults: ParameterDefaults
    variable_names: Annotated[list[str], Field(default_factory=list)]
    data: Annotated[list[DatasetData], Field(default_factory=list)]
