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
    """Manages `Asset` objects (e.g images) used by datasets content. Local
    assets added will be copied into `asset_dir` under a unique name that
    includes the file hash of the asset.

    Attributes:
        build_dir: The content build directory
        asset_destination_url_prefix: The public URL under which assets
            will be accessible after upload.
    """

    def __init__(self, build_dir: Path, asset_destination_url_prefix: str):
        self.build_dir = Path(build_dir)
        self.asset_destination_url_prefix = asset_destination_url_prefix.strip("/")
        self.copied_asset_names: dict[Path, str] = {}

        self.asset_dir.mkdir(exist_ok=True)

    @property
    def asset_dir(self) -> Path:
        """The asset directory in the build directory."""
        return self.build_dir / "assets"

    @property
    def assets(self) -> Iterator[Path]:
        """Yields the paths to all assets in the asset directory."""
        yield from self.asset_dir.iterdir()

    def asset_destination_url(self, asset_name: str) -> HttpUrl:
        """Returns the URL under `asset_destination_url_prefix` of the
        asset with the given name.

        >>> loader = AssetLoader("_build", "https://datasets.cloud.pennylane.ai/assets")
        >>> loader.asset_destination_url("qchem_hero-e98e34a7d58e039da35f793cb6d9bd0da78847f9.jpg")
        'https://datasets.cloud.pennylane.ai/assets/qchem_hero-e98e34a7d58e039da35f793cb6d9bd0da78847f9.jpg'
        """
        return f"{self.asset_destination_url_prefix}/{asset_name}"

    def add_asset(self, asset: Asset) -> HttpUrl:
        """
        Add an asset to the build and return its destination url.

        If `asset` is not a local asset, e.g it is an HTTP URL, return the
        URL.

        If `asset` is a local asset, copy it to the asset directory under a unique
        name and return its destination URL.
        """
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
        """Upload all assets in the asset directory to the given bucket, under
        the given prefix. Return the number of assets uploaded."""
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
