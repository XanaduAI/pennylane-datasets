from typing import Annotated, Any, Literal, TypedDict

from pydantic import Field

from dsets.lib.doctree import Asset, Document, Ref
from dsets.lib.pydantic_util import CamelCaseMixin

from .dataset import Dataset
from .dataset_class import DatasetClass
from .dataset_collection import DatasetCollection
from .dataset_tags import Tag
from .fields import BibtexStr, Slug


class DatasetFeature(Document, CamelCaseMixin):
    """Model for dataset family features.

    Attributes:
        slug: Unique name for feature
        title: Human-readable name for feature
        type_: Whether this is a 'DATA' or 'SAMPLES' feature
        content: Feature content. May use Markdown
    """

    slug: Slug
    title: str
    type_: Annotated[Literal["DATA", "SAMPLES"], Field(alias="type")] = "DATA"
    content: Ref[str]


class DatasetFamilyMeta(Document, CamelCaseMixin):
    """
    Metadata for a dataset family.

    Attributes:
        abstract: Short, 1-paragraph description of the dataset
        authors: List of authors
        citation: Citation, in Bibtex format
        license: License information
        source_code_url: Link to source code for reproducing the
            dataset
        tags: List of tags
        title: Human-readable title
        using_this_dataset: Description of the dataset and
            instructions for use. May use Markdown
        hero_image: Banner image
        thumbnail: Small image
    """

    abstract: Ref[str] | None = None
    authors: list[str]
    citation: Ref[BibtexStr]
    changelog: list[str] = []
    license: str
    source_code_url: str | None = None
    tags: list[str | Tag] = []
    title: str
    using_this_dataset: Ref[str]

    hero_image: Asset | None = None
    thumbnail: Asset | None = None

    extra: dict[str, Any] = {}


class DatasetParameterNode(TypedDict, total=False):
    """Model for the parameter defaults map of a dataset class."""

    default: str
    next_: "DatasetParameterTree"


DatasetParameterTree = dict[str, DatasetParameterNode | None]


class DatasetFamily(Document, CamelCaseMixin):
    """Model for dataset family, which may include one or more
    Pennylane dataset files.

    Attributes:
        slug: Unique identifier for this dataset family
        class_: `DatasetClass` for this family, or a reference
            to a document containing one
        download_name: First parameter for download form
        data: `Datasets` belonging to this family
        features: Data features for this family
        meta: Extended metadata
    """

    slug: Slug

    class_: Annotated[Ref[DatasetClass], Field(alias="class")]
    collection: Ref[DatasetCollection] | None = None
    data: list[Dataset] = []
    download_name: str
    features: list[DatasetFeature] = []
    meta: Ref[DatasetFamilyMeta]
    parameter_tree: DatasetParameterTree = {}

    extra: dict[str, Any] = {}


def insert_parameters(dataset: Dataset, partial: DatasetParameterTree):
    for value in dataset.parameters.values():
        ...


def build_parameter_tree(family: DatasetFamily):
    partial = family.parameter_tree

    for dataset in family.data:
        insert_parameters(dataset, partial)
