from typing import Annotated, Self

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)

from dsets.lib.json_ref import DocumentTreeModel
from dsets.lib.pydantic_util import CamelCaseMixin


class DatasetAttribute(BaseModel, CamelCaseMixin):
    """Model for a `DatasetType.attribute_list`.

    Attributes:
        name: Name of the attribute. Must be a legal python
            variable name
        python_type: Python type for this attribute. May
            contain markdown
        doc: Docstring for this attribute
        optional: Whether this attribute may not exist
            on the dataset instance
    """

    name: Annotated[str, Field(pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$")]
    python_type: str
    doc: str
    optional: bool = False


class DatasetParameter(BaseModel, CamelCaseMixin):
    """Model for a dataset parameter.

    Attributes:
        name: Short name for the parameter. Must be a legal
            python variable name
        title: Optional human-readable name for the parameter
        nullable: Whether this parameter may be null/None
    """

    name: Annotated[str, Field(pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$")]
    title: str | None = None
    description: str | None = None
    nullable: bool = False


class DatasetType(DocumentTreeModel, CamelCaseMixin):
    """Model for a dataset type, e.g `qchem` or `qspin`.

    Attributes:
        name: Unique name for this type
        attribute_list: List of expected attributes on
            a dataset instance
        parameter_list: List of parameter labels for
            a dataset instance
    """

    name: str
    attribute_list: list[DatasetAttribute] = []
    parameter_list: list[DatasetParameter] = []

    @property
    def attributes(self) -> dict[str, DatasetAttribute]:
        return {attribute.name: attribute for attribute in self.attribute_list}

    @model_validator(mode="after")
    def _validate_attribute_parameters(self: Self) -> Self:
        attr_names = set()
        for attr in self.attribute_list:
            if attr.name in attr_names:
                raise ValueError(f"Duplicate attribute name: {attr.name}")

        parameter_names = set()
        for parameter in self.parameter_list:
            if parameter.name in parameter_names:
                raise ValueError(f"Duplicate parameter name: {parameter.name}")

        return self
