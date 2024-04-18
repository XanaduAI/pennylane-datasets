from typing import Annotated, Literal

from pydantic import Field

from dsets.lib.doctree import Asset, Document, Ref
from dsets.lib.pydantic_util import CamelCaseMixin

from .dataset import Dataset
from .dataset_class import DatasetClass
from .fields import BibtexStr


class DatasetFeature(Document, CamelCaseMixin):
    """Model for dataset family features.

    Attributes:
        slug: Unique name for feature
        title: Human-readable name for feature
        type_: Whether this is a 'DATA' or 'SAMPLES' feature
        content: Feature content. May use Markdown
    """

    slug: str
    title: str
    type_: Literal["DATA", "SAMPLES"] = "DATA"
    content: Ref[str]


class DatasetFamilyMeta(Document, CamelCaseMixin):
    """
    Metadata for a dataset family.

    Attributes:
        abstract: Short, 1-paragraph description of the dataset
        authors: List of authors
        citation: Citation, in Nibtex format
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
    authors: list[str] = []
    citation: Ref[BibtexStr] | None = None
    source_code_url: str | None = None
    tags: list[str] = []
    title: str
    using_this_dataset: Ref[str] | None = None

    hero_image: Asset | None = None
    thumbnail: Asset | None = None


class DatasetFamily(Document, CamelCaseMixin):
    """Model for dataset family, which may include one or more
    Pennylane dataset files.

    Attributes:
        slug: Unique identifier for this dataset family
        class_: `DatasetClass` for this family, or a reference
            to a document containing one
        download_name: Suggested instance name for this dataset
            family
        data: `Datasets` belonging to this family
        features: Data features for this family
        meta: Extended metadata
    """

    slug: str

    class_: Annotated[Ref[DatasetClass], Field(alias="class")]
    data: list[Dataset] = []
    download_name: str = "dataset"
    features: list[DatasetFeature] = []

    meta: Ref[DatasetFamilyMeta]
