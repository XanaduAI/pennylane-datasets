import json
from pathlib import Path

from requests import post
from requests.exceptions import HTTPError

from dsets.settings import Settings


def get_valid_token(auth_path: Path) -> str | None:
    """Queries the profile service using the local token as the authorization header.
    Returns the auth token if a 200 response status is received or `None` otherwise.`"""

    try:
        with auth_path.open("r") as f:
            token_data = json.load(f)
    except FileNotFoundError:
        return None

    local_token = token_data["access_token"]

    # Any valid query would be sufficient here to obtain a 200 response if the auth token is valid.
    query = """
        query Profile($handle: String) {
          profile(handle: $handle) {
            id
          }
        }
        """
    json_body = {"query": query, "variables": {"handle": "handle"}}
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {local_token}",
    }
    try:
        post(
            url=Settings().graphql_url, json=json_body, timeout=10, headers=headers
        ).raise_for_status()
    except HTTPError:
        auth_path.unlink(missing_ok=True)
        return None

    return local_token
