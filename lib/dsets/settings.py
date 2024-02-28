from pydantic_settings import BaseSettings

from .lib.s3 import S3Path


class Settings(BaseSettings):
    """Global settings for pennylane-datasets."""

    data_bucket_name: str = "swc-prod-pennylane-datasets"
    data_bucket_key_prefix: S3Path = S3Path("data")
