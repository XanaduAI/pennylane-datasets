from pydantic import BaseModel

from dsets.lib.pydantic_util import CamelCaseMixin


class Tag(BaseModel, CamelCaseMixin):
    """Model for tags.

    Attributes:
        slug: Unique name for the tag
        title: Human-readable name for tag
    """

    slug: str
    title: str
