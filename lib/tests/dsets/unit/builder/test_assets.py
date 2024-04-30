from dataclasses import dataclass
from pathlib import Path

import pytest
from dsets.builder.assets import AssetLoader


@pytest.fixture
def content_dir(tmp_path: Path):
    return tmp_path


@pytest.fixture
def build_dir(tmp_path: Path):
    return tmp_path


@pytest.fixture
def asset_loader(build_dir: Path):
    """AssetLoader fixture."""

    return AssetLoader(
        build_dir=build_dir,
        asset_destination_url_prefix="https://test.pennylane.ai/assets",
    )


@dataclass
class MockAsset:
    root: str

    is_local: bool
    os_path: Path | None


class TestAssetLoader:
    def test_asset_destination_url(self, asset_loader: AssetLoader):
        """Test that ``asset_destination_url()`` returns a URL in
        the expected form."""

        assert (
            asset_loader.asset_destination_url("my_asset")
            == "https://test.pennylane.ai/assets/my_asset"
        )

    def test_add_local_asset(self, asset_loader: AssetLoader, content_dir: Path):
        """Test that adding a local asset:

        1. copies the asset file to the build directory with a filename
        that includes the sha1 hash
        2. Returns the destination url of the asset
        """

        content, digest = "abcdefghijklmop", "0626a7b36aa3227e844ba5d81a6fc2ab9e099204"
        name = f"my_asset-{digest}.asset"

        with open(content_dir / "my_asset.asset", "w", encoding="utf-8") as f:
            f.write(content)

        destination_url = asset_loader.add_asset(
            MockAsset("", True, content_dir / "my_asset.asset")
        )

        assert destination_url == f"https://test.pennylane.ai/assets/{name}"

        with open(asset_loader.asset_dir / name, "r", encoding="utf-8") as f:
            assert f.read() == content

    def test_add_remote_asset(self, asset_loader: AssetLoader):
        """Test that adding a remote asset returns the asset's url."""
        assert (
            asset_loader.add_asset(MockAsset("https://asset.com/asset", False, None))
            == "https://asset.com/asset"
        )
