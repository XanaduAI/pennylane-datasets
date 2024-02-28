from functools import cached_property
from pathlib import Path

import boto3
from dulwich.repo import Repo

from dsets.settings import Settings

from .s3 import S3Client


class Context:
    """Context object for CLI commands."""

    settings: Settings

    @property
    def repo_root(self) -> Path:
        """Path to repository root, relative to the
        current working directory."""
        return Path(self.repo.path).relative_to(Path.cwd())

    @property
    def data_dir(self) -> Path:
        """Path to data directory, relative to the
        current working directory."""
        return self.repo_root / "data"

    @cached_property
    def repo(self) -> Repo:
        """dulwich ``Repo`` object for the pennylane-datasets
        repo."""
        return Repo.discover()

    @cached_property
    def aws_client(self) -> boto3.Session:
        """AWS client."""
        return boto3.Session()

    @cached_property
    def s3_client(self) -> S3Client:
        """S3 Client."""
        return self.aws_client.client("s3")

    def __init__(self) -> None:
        self.settings = Settings()
