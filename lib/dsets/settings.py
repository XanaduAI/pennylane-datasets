from functools import cached_property
from pathlib import Path

import boto3
from dulwich.repo import Repo
from pydantic_settings import BaseSettings

from .lib.s3 import S3Client


class Settings(BaseSettings):
    """Global settings for pennylane-datasets."""

    asset_url_prefix: str = "https://datasets.cloud.pennylane.ai/assets"

    bucket_name: str = "swc-prod-pennylane-datasets"
    bucket_data_key_prefix: str = "data"
    bucket_asset_key_prefix: str = "assets"


class CLIContext:
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

    @property
    def content_dir(self) -> Path:
        """Path to the content dir, relative to the current
        working directory."""
        return self.repo_root / "content"

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

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
