import hashlib
import shutil
from logging import getLogger
from pathlib import Path

from pydantic import HttpUrl

from dsets.lib.doctree import Asset

logger = getLogger(__name__)


class AssetLoader:
    def __init__(self, build_dir: Path, asset_destination_url_prefix: str):
        self.build_dir = build_dir
        self.asset_destination_url_prefix = asset_destination_url_prefix.strip("/")

        self.asset_build_dir.mkdir(exist_ok=True)
        self.local_asset_destination_urls: dict[Path, HttpUrl] = {}

    @property
    def asset_build_dir(self) -> Path:
        return self.build_dir / "assets"

    def add_asset(self, asset: Asset) -> HttpUrl:
        if not asset.is_local:
            return asset.root

        os_path = asset.os_path
        if not (destination_url := self.local_asset_destination_urls.get(os_path)):
            with open(os_path, "rb") as f:
                digest = hashlib.file_digest(f, "sha1").hexdigest()

            name = f"{os_path.stem}-{digest}{os_path.suffix}"
            build_dest = self.asset_build_dir / name
            if not build_dest.exists():
                shutil.copy(os_path, build_dest)

            destination_url = f"{self.asset_destination_url_prefix}/{name}"
            self.local_asset_destination_urls[os_path] = HttpUrl(
                f"{self.asset_destination_url_prefix}/{name}"
            )

        return destination_url
