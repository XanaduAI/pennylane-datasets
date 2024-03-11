from typing import Annotated, Literal

from pydantic import (
    AwareDatetime,
    BaseModel,
    Field,
)

from dsets.lib.json_ref import DocumentTreeModel, Reference
from dsets.lib.pydantic_util import CamelCaseMixin

from .dataset_type import DatasetType


class Dataset(BaseModel, CamelCaseMixin):
    """Model for dataset family data files."""

    slug: str
    data_url: str
    parameters: dict[str, str | None] = {}
    parameter_search_priority: Annotated[int | None, Field(ge=0)] = None


class DatasetFeature(BaseModel, CamelCaseMixin):
    """Model for dataset family features.

    Attributes:
        slug: Unique name for feature
        title: Human-readable name for feature
        content: Feature content
    """

    slug: str
    type_: Literal["DATA", "SAMPLES"] = "DATA"
    title: str
    content: Reference[str]


class DatasetFeatureTemplate(BaseModel, CamelCaseMixin):
    slug: str
    type_: Literal["DATA", "SAMPLES"] = "DATA"
    title: str
    variables: dict[str, str]
    template: Reference[str]


class DatasetFamilyMeta(DocumentTreeModel, CamelCaseMixin):
    """
    Metadata for a dataset family. Consumed by pennylane.ai/datasets

    Attributes:
        title: Title for this dataset family
        authors: List of authors
        tags: List of tags
        citation: Citation
        about: Markdown document describing the dataset
            family
        hero_image_url: URL to a hero image
        thumbnail_url: URL to a thumbnail image
        date_of_publication: Date created
        date_of_last_modification: Date last modified
    """


class DatasetFamily(DocumentTreeModel, CamelCaseMixin):
    """Model for dataset family, which may include one or more
    Pennylane dataset files.

    Attributes:
        slug: Unique identifier for this dataset family
        type_: `DatasetType` for this family, or a reference
            a document containing one
        meta: `DatasetFamilyMeta` for this family
        download_name: Suggested instance name for this dataset
            family
        data: `Datasets` belonging to this family
        features: Data features for this family
    """

    slug: str
    type_: Annotated[Reference[DatasetType], Field(alias="type")]

    title: str
    authors: list[str] = []
    tags: list[str] = []
    citation: Reference[str]
    about: Reference[str]

    hero_image_url: str | None = None
    thumbnail_url: str | None = None

    date_of_publication: AwareDatetime
    date_of_last_modification: AwareDatetime

    download_name: str = "dataset"

    features: list[DatasetFeature] = []
    feature_templates: list[DatasetFeatureTemplate] = []

    data: list[Dataset] = []
