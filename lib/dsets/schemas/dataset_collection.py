from dsets.lib.doctree import Asset, Document
from dsets.lib.pydantic_util import CamelCaseMixin

from .fields import Slug


class DatasetCollection(Document, CamelCaseMixin):
    """Model for a collection of datasets, e.g 'Benchmarks'

    Attributes:
        slug: Slug for this collection
        title: Human-readable title for this collection
        about: Short description of this collection
        thumbnail: Small image
    """

    slug: Slug
    title: str
    about: str
    thumbnail: Asset
