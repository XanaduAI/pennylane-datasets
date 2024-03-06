from typing import Annotated, Self

from pydantic import (
    AwareDatetime,
    BaseModel,
    Field,
    ValidationError,
    model_validator,
)

from dsets.lib.json_ref import DocumentTreeModel, Reference
from dsets.lib.pydantic_util import CamelCaseMixin

from ._fields import ParameterDefaults


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


class DatasetData(BaseModel, CamelCaseMixin):
    """Model for dataset data files."""

    data_url: str
    parameter_values: dict[str, str] | None = None
    variables: dict[str, str] | None = None


class DatasetFamily(DocumentTreeModel, CamelCaseMixin):
    """Model for dataset family, which may include one or more
    Pennylane dataset files.

    Attributes:
        slug: Unique identifier for this dataset family
        title: Title for this dataset family
        type_: `DatasetType` for this family, or a reference
            a document containing one
        authors: List of authors
        tags: List of tags
        citation: Citation
        about: Markdown document describing the dataset
            family
        date_of_publication: Date created
        date_of_last_modification: Date last modified

    """

    slug: str
    title: str
    type_: Annotated[Reference[DatasetType], Field(alias="type")]

    authors: list[str]
    tags: Annotated[list[str], Field(default_factory=list)]

    citation: Reference[str]
    about: Reference[str]

    date_of_publication: AwareDatetime
    date_of_last_modification: AwareDatetime

    parameter_labels: Annotated[list[str], Field(default_factory=list)]
    parameter_defaults: ParameterDefaults

    variables: Annotated[dict[str, str], Field(default_factory=dict)]
    data: Annotated[list[DatasetData], Field(default_factory=list)]
