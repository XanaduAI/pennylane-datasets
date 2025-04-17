from collections.abc import Callable
from typing import BinaryIO, TypedDict

import gql
import requests

from dsets.lib.graphql import queries


class APIError(RuntimeError):
    def __init__(self, operation: str, error: str):
        self.operation = operation
        self.error = error

        super().__init__(f"{operation} failed: {error}")


class File(TypedDict):
    """File information returned from the GraphQL API."""

    name: str
    status: str
    size: str
    downloadUrl: str
    checksumSha256: str


class FileUploadPart(TypedDict):
    """Part of a ``FileUpload``."""

    url: str
    bytesStart: str
    bytesEnd: str


class FileUpload(TypedDict):
    """File upload information returned by the GraphQL API."""

    numParts: int
    numUploadedParts: int
    uploadParts: list[FileUploadPart]


def _create_file_upload(
    client: gql.Client, name: str, size: int, checksum_sha256: bytes
):
    """Create a new file upload."""
    resp = client.execute(
        queries.UPLOAD_CREATE,
        {"name": name, "size": str(size), "checksum_sha256": checksum_sha256.hex()},
        parse_result=True,
    )["datasetFileUploadCreate"]
    if resp.get("userError"):
        raise APIError("create-upload", resp["userError"]["message"])


def _get_file_upload(client: gql.Client, name: str) -> FileUpload | None:
    """Get pending upload for file with ``name``."""
    resp = client.execute(queries.UPLOAD_GET, {"name": name})

    if upload := resp["datasetFileUpload"]:
        return upload

    return None


def upload_file(
    client: gql.Client,
    stream: BinaryIO,
    name: str,
    size: int,
    checksum_sha256: bytes,
    callback: Callable[[int], None] | None = None,
) -> File:
    """Upload a file to the datasets service.

    Args:
        client: Authenticated GraphQL client
        stream: Stream of file data to upload
        name: User's name for file
        size: Total number of bytes to be read from ``stream``
        checksum_sha256: SHA256 sum of data in ``stream``
        callback: Progress callback, accepts a number of bytes uploaded

    Returns:
        File: information on uploaded file

    Raises:
        APIErrror: An API error occurs
    """
    _create_file_upload(client, name, size, checksum_sha256)

    while (upload := _get_file_upload(client, name)) is not None:
        for part in upload["uploadParts"]:
            start, end = int(part["bytesStart"]), int(part["bytesEnd"])
            stream.seek(start)

            requests.put(part["url"], data=stream.read(end - start)).raise_for_status()
            if callback:
                callback(end - start)

    if not (file := get_file(client, name)):
        raise APIError(
            "Upload file",
            (
                "Something went wrong - please try again and"
                " contact support if the issue persists."
            ),
        )

    return file


def get_file(client: gql.Client, name: str) -> File | None:
    """Return file information owned by the calling user."""
    resp = client.execute(queries.FILE_GET, {"name": name}, parse_result=True)
    if (file := resp["datasetFile"]) is not None:
        return file

    return None


def get_files(client: gql.Client) -> list[File]:
    """Return all ``File``s owned by calling user."""
    resp = client.execute(queries.FILES_GET)

    return resp["datasetFiles"]
