import hashlib
import shutil
from collections.abc import Iterator
from logging import getLogger
from pathlib import Path

from pydantic import HttpUrl

from dsets.lib import s3
from dsets.lib.doctree import Asset

logger = getLogger(__name__)


class AssetLoader:
    def __init__(self, build_dir: Path, asset_destination_url_prefix: str):
        self.build_dir = build_dir
        self.asset_destination_url_prefix = asset_destination_url_prefix.strip("/")
        self.copied_asset_names: dict[Path, str] = {}

        self.asset_dir.mkdir(exist_ok=True)

    @property
    def asset_dir(self) -> Path:
        return self.build_dir / "assets"

    @property
    def assets(self) -> Iterator[Path]:
        yield from self.asset_dir.iterdir()

    def asset_destination_url(self, asset_name: str) -> HttpUrl:
        return f"{self.asset_destination_url_prefix}/{asset_name}"

    def add_asset(self, asset: Asset) -> HttpUrl:
        if not asset.is_local:
            return asset.root

        os_path = asset.os_path
        if not (name := self.copied_asset_names[os_path]):
            with open(os_path, "rb") as f:
                digest = hashlib.file_digest(f, "sha1").hexdigest()

            name = f"{os_path.stem}-{digest}{os_path.suffix}"
            copy_dest = self.asset_dir / name
            if not copy_dest.exists():
                shutil.copy(os_path, copy_dest)

            self.copied_asset_names[os_path] = name

        return self.asset_destination_url(name)

    def upload_assets(
        self, s3_client: s3.S3Client, bucket: str, prefix: s3.S3Path
    ) -> int:
        prefix = s3.S3Path(prefix)
        uploaded_count = 0

        for asset_path in self.assets:
            name = asset_path.name
            key = prefix / name

            if s3.object_exists(s3_client, bucket, key):
                logger.info(
                    "Asset already uploaded, skipping: asset_name=%s, key=%s", name, key
                )
                continue

            s3_client.upload_file(Filename=str(asset_path), Bucket=bucket, Key=str(key))
            logger.info("Uploaded asset: name=%s, key=%s", name, key)
            uploaded_count += 1

        return uploaded_count
