from pydantic import BaseModel, ConfigDict


class AuthorHandle(BaseModel):
    """Model for dataset authors represented by their PennyLane.ai username.

    Attributes:
        username: Username of the PennyLane.ai profile of the author
    """

    model_config = ConfigDict(extra="forbid")

    username: str


class AuthorName(BaseModel):
    """Model for dataset authors represented by their name.

    Attributes:
        name: Name of the author
    """

    model_config = ConfigDict(extra="forbid")

    name: str


Author = AuthorHandle | AuthorName
