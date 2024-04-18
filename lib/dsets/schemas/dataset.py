from typing import Annotated, Literal

from pydantic import (
    AwareDatetime,
    Field,
)

from dsets.lib.doctree import Asset, Document, Ref
from dsets.lib.pydantic_util import CamelCaseMixin, SortedField

from .dataset_type import DatasetType


class Dataset(Document, CamelCaseMixin):
    """Model for dataset family data files."""

    slug: str
    data_url: str
    parameters: dict[str, str | None] = {}
    parameter_search_priority: Annotated[int | None, Field(ge=0)] = None


class DatasetFeature(Document, CamelCaseMixin):
    """Model for dataset family features.

    Attributes:
        slug: Unique name for feature
        title: Human-readable name for feature
        content: Feature content
    """

    slug: str
    type_: Literal["DATA", "SAMPLES"] = "DATA"
    title: str
    content: Ref[str]


class DatasetFeatureTemplate(Document, CamelCaseMixin):
    slug: str
    type_: Literal["DATA", "SAMPLES"] = "DATA"
    title: str
    variables: dict[str, str]
    template: Ref[str]


class DatasetFamily(Document, CamelCaseMixin):
    """Model for dataset family, which may include one or more
    Pennylane dataset files.

    Attributes:
        slug: Unique identifier for this dataset family
        type_: `DatasetType` for this family, or a reference
            to a document containing one
        download_name: Suggested instance name for this dataset
            family
        data: `Datasets` belonging to this family
        features: Data features for this family
    """

    slug: str
    type_: Annotated[Ref[DatasetType], Field(alias="type")]

    title: str
    authors: list[str] = []
    tags: list[str] = []
    citation: Ref[str]
    about: Ref[str]

    hero_image: Asset | None = None
    thumbnail: Asset | None = None

    date_of_publication: AwareDatetime
    date_of_last_modification: AwareDatetime

    download_name: str = "dataset"

    features: list[DatasetFeature | DatasetFeatureTemplate] = []

    data: Annotated[
        list[Dataset], SortedField(lambda d: tuple(d.parameters.values()))
    ] = []
