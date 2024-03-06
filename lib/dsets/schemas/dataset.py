from typing import Annotated

from pydantic import (
    AwareDatetime,
    BaseModel,
    Field,
)

from dsets.lib.json_ref import DocumentTreeModel, Reference
from dsets.lib.pydantic_util import CamelCaseMixin

from ._fields import ParameterDefaults
from .dataset_type import DatasetType


class DatasetData(BaseModel, CamelCaseMixin):
    """Model for dataset family data files."""

    data_url: str
    parameter_values: dict[str, str] | None = None
    variables: dict[str, str] | None = None


class DatasetFeature(BaseModel, CamelCaseMixin):
    """Model for dataset family features.

    Attributes:
        slug: Unique name for feature
        title: Human-readable name for feature
        content: Feature content
    """

    slug: str
    title: str
    content: Reference[str]


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

    data: Annotated[list[DatasetData], Field(default_factory=list)]
