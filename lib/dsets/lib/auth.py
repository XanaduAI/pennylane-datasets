import json
from datetime import datetime, timezone
from pathlib import Path

from .time import utcnow


def check_local_token(auth_path: Path) -> bool:
    """Returns True if valid token found in `.auth/` local dir."""
    files = auth_path.glob("*.json")

    for file in files:
        with file.open("r") as f:
            token_data = json.load(f)

        token_expires_at = datetime.fromtimestamp(
            token_data["expires_at"], tz=timezone.utc
        )
        if token_expires_at < utcnow():
            print("Found expired token...")
            Path.unlink(file)
            print("Removed expired token.")
        elif token_expires_at > utcnow():
            return True

    return False
