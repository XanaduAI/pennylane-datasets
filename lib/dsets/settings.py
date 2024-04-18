from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global settings for pennylane-datasets."""

    asset_url_prefix: str = "https://datasets.cloud.pennylane.ai/assets"

    bucket_name: str = "swc-prod-pennylane-datasets"
    bucket_data_key_prefix: str = "data"
    bucket_asset_key_prefix: str = "assets"
