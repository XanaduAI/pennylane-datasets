import hashlib
import shutil
from logging import getLogger
from pathlib import Path

from dsets.lib.doctree import Asset

logger = getLogger(__name__)


class AssetUploader:
    def __init__(
        self,
        asset_build_dir: Path,
    ):
        self.asset_build_dir = asset_build_dir
        self.assets = {}
        self.resolved_local_assets: dict[Path, str] = {}

    def add_asset(self, asset: Asset) -> None:
        if not asset.is_local:
            return

        os_path = asset.os_path
        if (name := self.resolved_local_assets.get(os_path)):
            ref = {"$ref": f"#/assets/{name}"}
        else:
            with open(os_path, "rb") as f:
                digest = hashlib.file_digest(f, "sha1").hexdigest()

            name = f"{os_path.stem}-{digest}{os_path.suffix}"

            shutil.copy(os_path, self.asset_build_dir / name)
            
            self.resolved_local_assets[os_path] = name
            ref = {"$ref": f"#/assets/{name}"}

        asset.root = ref

    

