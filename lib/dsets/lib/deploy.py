import json
from pathlib import Path

import requests
import requests.exceptions
from requests_auth_aws_sigv4 import AWSSigV4


def deploy_datasets_build(
    datasets_admin_api_url: str, build_path: Path, commit_sha: str
) -> None:
    """Deploy datasets build to new datasets service using the admin endpoint.

    Args:
        datasets_admin_api_url: URL of the datasets admin API
        build_path: Path to datasets-build.json
        tags: Extra tags for the build

    Raises:
        requests.exceptions.RequestException: If the request returns a non-200 status code
    """
    auth = AWSSigV4(
        "execute-api",
    )

    with open(build_path, "r") as f:
        build = json.load(f)

    resp = requests.put(
        f"{datasets_admin_api_url}/build",
        json={"commitSha": commit_sha, "build": build},
        auth=auth,
    )
    if resp.status_code != 200:
        raise ValueError(resp.content)
    resp.raise_for_status()
