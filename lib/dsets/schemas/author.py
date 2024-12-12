from pydantic import ConfigDict


class Author:
    """Model for dataset authors represented by their PennyLane.ai username.

    Attributes:
        name: Name of the author
        username: PennyLane.ai profile username of the author
    """

    model_config = ConfigDict(extra="forbid")

    name: str
    username: str | None = None
