import hashlib
import typing
from collections.abc import Callable
from pathlib import Path, PurePosixPath
from typing import ClassVar

import botocore.exceptions

from .time import compact_isoformat, utcnow

if typing.TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
else:
    S3Client = typing.Any


S3Path = PurePosixPath


def object_exists(s3_client: S3Client, bucket: str, key: S3Path) -> bool:
    """Return ``True`` iff object with ``key`` exists in ``bucket``."""
    try:
        s3_client.head_object(Bucket=bucket, Key=str(key))
    except botocore.exceptions.ClientError as exc:
        if exc.response["Error"]["Code"] == "404":
            return False

        raise exc

    return True


class S3DatasetRepo:
    """Class for managing the S3 dataset repo and the git
    mirror.

    Attributes:
        local_mirror: Path to the directory that contains
            the receipt files for uploaded datasets
        s3_client: S3 client
        s3_bucket: Name of S3 bucket
        s3_prefix: Prefix of the data rpo in the
            S3 bucket
    """

    hashfile_key_prefix: ClassVar[S3Path] = S3Path("_by_hash")

    def __init__(
        self,
        local_mirror: Path,
        s3_client: S3Client,
        s3_bucket: str,
        s3_prefix: S3Path | None = None,
    ):
        self.local_mirror = local_mirror
        self.s3_client = s3_client
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix or S3Path()

    def s3_key_from_file_hash(self, file_sha1: bytes) -> S3Path | None:
        """Returns the S3 path for an object in the S3 repo with the given hash,
        if one exists.

        Args:
            file_sha1: File SHA1 digest
            relative: If True, the returned key will be relative to ``s3_prefix``.
                Otherwise, it will be an relative to the bucket root.

        Returns:
            S3Path: Path to f with hash, if it exists
            None: If no object exists with the given hash
        """
        try:
            resp = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=str(self.s3_prefix / self.hashfile_key_prefix / file_sha1.hex()),
            )
        except self.s3_client.exceptions.NoSuchKey:
            return None

        return S3Path(resp["Body"].read().decode("utf-8"))

    def upload_file(
        self,
        path: Path,
        *,
        hash_progress_cb: Callable[[int], None] | None = None,
        upload_progress_cb: Callable[[int], None] | None = None,
    ) -> S3Path:
        """Upload file at ``path`` to the S3 repo, and write a receipt for its
        upload to the local mirror.

        Args:
            path: Path to local file
            hash_progress_cb: A callable that is updated with the progress
                of the file hash. The argument is the number of bytes processed
                since the last call
            upload_progress_cb: A callable that is updated with the progress
                of the upload (for a progress bar, etc). The argument is the number
                of bytes uploaded since the last call

        Returns:
            S3 key of the newly uploaded file
        """
        with open(path, mode="rb") as f:
            digest = hashlib.sha1()
            while chunk := f.read(2**22):
                digest.update(chunk)
                if hash_progress_cb:
                    hash_progress_cb(len(chunk))

            file_sha1 = digest.digest()

        if existing_key := self.s3_key_from_file_hash(file_sha1):
            raise FileExistsError(
                f"Object with identical hash ({file_sha1.hex()}) already exists at path '{existing_key}'"
            )

        timestamp = utcnow()
        file_key = S3Path(
            path.name, f"{compact_isoformat(timestamp)}-{file_sha1.hex()}"
        )
        s3_key = self.s3_prefix / file_key

        self.s3_client.upload_file(
            Filename=str(path),
            Bucket=self.s3_bucket,
            Key=str(self.s3_prefix / file_key),
            Callback=upload_progress_cb,
        )

        hash_file_key = str(self.s3_prefix / self.hashfile_key_prefix / file_sha1.hex())
        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=hash_file_key,
            Body=str(s3_key).encode("utf-8"),
            ContentType="text/plain",
        )

        reciept_file = self.local_mirror / file_key

        reciept_file.parent.mkdir(parents=True, exist_ok=True)
        reciept_file.touch()

        return s3_key
