import json
from datetime import datetime, timezone
from pathlib import Path

from .device_auth import TokenData
from .time import utcnow


def check_local_token(auth_path: Path) -> TokenData | None:
    """Returns the token data if valid token found in `auth_path` local dir or `None`
    if no valid token is found."""
    files = auth_path.glob("*.json")

    for file in files:
        with file.open("r") as f:
            token_data = json.load(f)

        token_expires_at = datetime.fromtimestamp(
            token_data["expires_at"], tz=timezone.utc
        )
        if token_expires_at < utcnow():
            Path.unlink(file)
        elif token_expires_at > utcnow():
            return token_data

    return None
