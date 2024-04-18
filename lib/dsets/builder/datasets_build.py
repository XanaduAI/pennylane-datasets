import typing

import jinja2
from pydantic import BaseModel

from dsets.lib.doctree import Asset, Doctree
from dsets.schemas import (
    DatasetFamily,
    DatasetFeature,
    DatasetFeatureTemplate,
    DatasetType,
)
from dsets.settings import CLIContext

from .asset import AssetUploader


class DatasetSite(BaseModel):
    assets: set[Asset]
    dataset_types: dict[str, DatasetType]
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
    dataset_types: dict[str, DatasetType] = {}
    dataset_families: dict[str, DatasetFamily] = {}

    for dataset_json_path in cli_context.content_dir.rglob("**/dataset.json"):
        family = DatasetFamily.from_os_path(
            doctree, dataset_json_path, resolve_refs=True
        )

        if family.slug in dataset_families:
            raise RuntimeError(
                f"DatasetFamily with slug '{family.slug}' already exists"
            )

        type_ = typing.cast(DatasetType, family.type_)
        if not (existing_type := dataset_types.get(type_.name)):
            dataset_types[type_.name] = type_
        elif existing_type.document_context.os_path != type_.document_context.os_path:
            raise RuntimeError(
                f"Duplicate 'DatasetType' definition on family '{family.slug}'"
            )

        dataset_families[family.slug] = family

    for asset in doctree.get_objects(Asset):
        if asset.is_local:
            url = asset_uploader.add_asset(asset)
            asset.root = url
            assets.add(asset)

    for dataset_family in dataset_families.values():
        compile_feature_templates(dataset_family)

    return DatasetSite(
        assets=assets, dataset_types=dataset_types, dataset_families=dataset_families
    )


def compile_feature_templates(family: DatasetFamily) -> None:
    for i, feature in enumerate(family.features):
        if not isinstance(feature, DatasetFeatureTemplate):
            continue

        content_template = jinja2.Template(feature.template)

        family.features[i] = DatasetFeature(
            slug=feature.slug,
            type_=feature.type_,
            title=feature.title,
            content=content_template.render(**feature.variables),
        )
