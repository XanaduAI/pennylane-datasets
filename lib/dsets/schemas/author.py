from pydantic import ConfigDict


class Author:
    """Model for dataset authors represented by their name.

    Attributes:
        name: Name of the author
    """

    model_config = ConfigDict(extra="forbid")

    name: str
    username: str | None = None
