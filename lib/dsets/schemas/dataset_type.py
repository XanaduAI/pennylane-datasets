from typing import Self

from pydantic import (
    BaseModel,
    ValidationError,
    model_validator,
)

from dsets.lib.json_ref import DocumentTreeModel
from dsets.lib.pydantic_util import CamelCaseMixin


class DatasetAttribute(BaseModel, CamelCaseMixin):
    """Model for a `DatasetType.attribute_list`.

    Attributes:
        name: Name of the attribute
        python_type: Python type for this attribute. May
            contain markdown
        doc: Docstring for this attribute
        optional: Whether this attribute may not exist
            on the dataset instance
    """

    name: str
    python_type: str
    doc: str
    optional: bool = False


class DatasetType(DocumentTreeModel, CamelCaseMixin):
    """Model for a dataset type, e.g `qchem` or `qspin`.

    Attributes:
        name: Unique name for this type
        attribute_list: List of expected attributes on
            a dataset instance
        doc: A doc string for this type
    """

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
