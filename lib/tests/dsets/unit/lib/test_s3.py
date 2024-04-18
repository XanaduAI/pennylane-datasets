import re
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import boto3
import moto
import pytest
from dsets.lib.s3 import S3Client, S3DatasetRepo, S3Path, object_exists


@pytest.fixture
def s3_client() -> Iterator[S3Client]:
    with moto.mock_aws():
        yield boto3.client("s3")


@pytest.fixture
def s3_bucket(s3_client: S3Client) -> str:
    s3_client.create_bucket(Bucket="mock_bucket")

    return "mock_bucket"


@pytest.fixture
def local_mirror_dir(tmpdir: Path) -> Path:
    data_dir = tmpdir / "data"

    data_dir.mkdir()

    return Path(data_dir)


@pytest.fixture
def s3_repo(local_mirror_dir: Path, s3_client, s3_bucket: str) -> S3DatasetRepo:
    return S3DatasetRepo(
        local_mirror_dir,
        s3_client,
        s3_bucket,
        S3Path("data"),
    )


def test_object_exists(s3_client: S3Client, s3_bucket: str):
    """Test that `object_exists()` returns True if `key` exists
    in the bucket."""
    key = S3Path("path", "to", "object")
    s3_client.put_object(Bucket=s3_bucket, Key=str(key))

    assert object_exists(s3_client, s3_bucket, S3Path(key)) is True


def test_object_exists_not_exists(s3_client: S3Client, s3_bucket: str):
    """Test that `object_exists()` returns False if `key` does not exist
    in the bucket."""
    assert object_exists(s3_client, s3_bucket, S3Path("not", "a", "path")) is False


class TestS3DatasetRepo:
    """Tests for `S3DatasetRepo`."""

    def test_get_object_with_hash(self, s3_repo: S3DatasetRepo):
        """Tests that `get_object_with_hash()` returns the
        path contained in the hashfile with the given hash."""
        s3_repo.s3_client.put_object(
            Bucket=s3_repo.s3_bucket,
            Key=f"data/{s3_repo.hashfile_key_prefix}/abcd",
            Body="path/to/object",
        )

        assert s3_repo.get_obj_with_hash(bytes.fromhex("abcd")) == S3Path(
            "path", "to", "object"
        )

    def test_get_object_with_hash_not_exists(self, s3_repo: S3DatasetRepo):
        """Test that `get_object_with_hash()` returns None if no file
        exists with the given hash."""
        assert s3_repo.get_obj_with_hash(bytes.fromhex("abcd")) is None

    @patch("dsets.lib.s3.utcnow")
    def test_upload_file(self, utcnow: MagicMock, s3_repo: S3DatasetRepo, tmpdir: Path):
        """Test that `upload_file()` uploads the file to an object with the
        expected key, and that the object's path can be retrieved from
        its hash."""
        utcnow.return_value = datetime(2000, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
        content = "abcdefghijklmnop"
        content_hash = "14f3995288acd189e6e50a7af47ee7099aa682b9"
        s3_path = S3Path("data", "file.data", f"2000-01-02T030405Z-{content_hash}")

        file_path = Path(tmpdir / "file.data")

        with open(file_path, "w", encoding="utf-8") as data_file:
            data_file.write(content)

        assert s3_repo.upload_file(file_path) == s3_path
        assert s3_repo.get_obj_with_hash(bytes.fromhex(content_hash)) == s3_path

    @patch("dsets.lib.s3.utcnow")
    def test_upload_file_content_exists(
        self, utcnow: MagicMock, s3_repo: S3DatasetRepo, tmpdir: Path
    ):
        """Test that `upload_file()` raises a `FileExistsError` if an object already
        exists in the repo with the same content hash."""
        utcnow.return_value = datetime(2000, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
        content = "abcdefghijklmnop"
        content_hash = "14f3995288acd189e6e50a7af47ee7099aa682b9"
        s3_path = S3Path("data", "file.data", f"2000-01-02T030405Z-{content_hash}")

        file_path = Path(tmpdir / "file.data")

        with open(file_path, "w", encoding="utf-8") as data_file:
            data_file.write(content)

        s3_repo.upload_file(file_path)

        with open(tmpdir / "same_content.data", "w", encoding="utf-8") as data_file:
            data_file.write(content)

        with pytest.raises(
            FileExistsError,
            match=re.escape(
                f"Object with identical hash ({content_hash})"
                f" already exists at path '{s3_path}'"
            ),
        ):
            s3_repo.upload_file(Path(tmpdir / "same_content.data"))
