import typing
from pydantic import BaseModel

from dsets.lib.doctree import Asset, Doctree
from dsets.schemas import (
    DatasetFamily,
    DatasetClass
)
from dsets.settings import CLIContext

from .asset import AssetUploader


class DatasetSite(BaseModel):
    assets: set[Asset]
    dataset_classes: dict[str, DatasetClass]
    dataset_families: dict[str, DatasetFamily]


def build_dataset_site(cli_context: CLIContext) -> DatasetSite:
    settings = cli_context.settings
    asset_uploader = AssetUploader(
        destination_url_prefix=settings.asset_url_prefix,
        s3_client=cli_context.s3_client,
        bucket=settings.bucket_name,
        prefix=settings.bucket_asset_key_prefix,
    )

    doctree = Doctree(cli_context.content_dir)

    assets: set[Asset] = set()
    dataset_classes: dict[str, DatasetClass] = {}
    dataset_families: dict[str, DatasetFamily] = {}

    for dataset_json_path in cli_context.content_dir.rglob("**/dataset.json"):
        family = DatasetFamily.from_os_path(
            doctree, dataset_json_path, resolve_refs=True
        )

        if family.slug in dataset_families:
            raise RuntimeError(
                f"DatasetFamily with slug '{family.slug}' already exists"
            )

        class_ = typing.cast(DatasetClass, family.class_)
        if not (existing_type := dataset_classes.get(class_.name)):
            dataset_classes[class_.name] = class_
        elif existing_type.document_context.os_path != class_.document_context.os_path:
            raise RuntimeError(
                f"Duplicate 'DatasetType' definition on family '{family.slug}'"
            )

        dataset_families[family.slug] = family

    for asset in doctree.get_objects(Asset):
        if asset.is_local:
            url = asset_uploader.add_asset(asset)
            asset.root = url
            assets.add(asset)

    return DatasetSite(
        assets=assets, dataset_classes=dataset_classes, dataset_families=dataset_families
    )


