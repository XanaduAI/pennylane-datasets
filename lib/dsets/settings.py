from functools import cached_property
from pathlib import Path

import boto3
from dulwich.repo import Repo
from pydantic_settings import BaseSettings

from .lib.s3 import S3Client, S3Path


class Settings(BaseSettings):
    """Global settings for pennylane-datasets."""

    bucket_public_domain: str = "datasets.cloud.pennylane.ai"
    bucket_name: str = "swc-staging-pennylane-datasets"

    bucket_build_key_prefix: S3Path = S3Path("build")
    bucket_data_key_prefix: S3Path = S3Path("data")
    bucket_asset_key_prefix: S3Path = S3Path("assets")

    @property
    def public_url_root_assets(self) -> str:
        return f"https://{self.bucket_public_domain}/{self.bucket_asset_key_prefix}"


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

    @property
    def build_dir(self) -> Path:
        return self.repo_root / "_build"

    @cached_property
    def repo(self) -> Repo:
        """dulwich ``Repo`` object for the pennylane-datasets
        repo."""
        return Repo.discover()

    @cached_property
    def commit_sha(self) -> str:
        """Return full-length git SHA for currently checked out
        ref."""
        return self.repo.head().hex()

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
