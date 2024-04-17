from pydantic_settings import BaseSettings

from .lib.s3 import S3Path


class Settings(BaseSettings):
    """Global settings for pennylane-datasets."""

    data_bucket_name: str = "swc-prod-pennylane-datasets"
    data_bucket_key_prefix: S3Path = S3Path("data")

    data_bucket_assets_prefix: str = "assets"
    assert_url_prefix: str = "https://datasets.cloud.pennylane.ai/assets"
