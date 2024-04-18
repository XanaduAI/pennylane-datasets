import hashlib
from logging import getLogger
from pathlib import Path

from dsets.lib import s3
from dsets.lib.doctree import Asset

logger = getLogger(__name__)


class AssetUploader:
    def __init__(
        self,
        destination_url_prefix: str,
        s3_client: s3.S3Client,
        bucket: str,
        prefix: str,
    ):
        self.destination_url_prefix = destination_url_prefix.strip("/")
        self.s3_client = s3_client
        self.bucket = bucket
        self.prefix = prefix

        self.resolved_asset_urls: dict[Path, str] = {}
        self.resolved_asset_names: dict[Path, str] = {}

    def add_asset(self, asset: Asset) -> str:
        if not asset.is_local:
            return str(asset.root)

        os_path = asset.os_path
        if resolved := self.resolved_asset_urls.get(os_path):
            return resolved

        with open(os_path, "rb") as f:
            digest = hashlib.file_digest(f, "sha1").hexdigest()

        name = f"{os_path.stem}-{digest}{os_path.suffix}"
        url = f"{self.destination_url_prefix}/{name}"

        key = f"{self.prefix}/{name}"
        if s3.object_exists(self.s3_client, self.bucket, key):
            print(f"Asset already uploaded, skipping: path={os_path}, s3_key={key}")
            return url

        self.s3_client.upload_file(Filename=str(os_path), Bucket=self.bucket, Key=key)
        print(f"Uploaded new asset: path={os_path}, key={key}")

        self.resolved_asset_urls[os_path] = url

        return url
