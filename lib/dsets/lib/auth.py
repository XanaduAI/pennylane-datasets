import json
from pathlib import Path
from typing import Any, Optional

from requests import post

from .device_auth import TokenData


GRAPHQL_URL = "https://dev.cloud.pennylane.ai/graphql"  # TODO: Update to prod


def get_graphql(
    url: str,
    query: str,
    variables: Optional[dict[str, Any]] = None,
    headers=dict[str, str],
):
    """
    Args:
        url: The URL to send a query to.
        query: The main body of the query to be sent.
        variables: Additional input variables to the query body.
        headers: Headers for the query.
    Returns:
        string: json response.
    """

    json = {"query": query}

    if variables:
        json["variables"] = variables

    response = post(url=url, json=json, timeout=10, headers=headers)
    return response


def has_valid_token(auth_path: Path) -> TokenData | None:
    """Queries the profile service using the local token as the authorization header.
    Returns `True` if a 200 response status is received or `False` otherwise.`"""

    token_data = None
    files = auth_path.glob("*.json")
    for file in files:
        with file.open("r") as f:
            token_data = json.load(f)

    if token_data is None:
        return False

    local_token = token_data["access_token"]
    response = get_graphql(
        GRAPHQL_URL,
        """
        query Profile($handle: String) {
          profile(handle: $handle) {
            id
          }
        }
        """,
        {"handle": "handle"},
        {"content-type": "application/json", "Authorization": f"Bearer {local_token}"},
    )
    return response.status_code == 200
