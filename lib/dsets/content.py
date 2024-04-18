import hashlib
import typing
from pathlib import Path

import jinja2
from pydantic import BaseModel

from dsets.lib import s3
from dsets.lib.doctree import Asset, Doctree

from .context import Context
from .schemas import DatasetFamily, DatasetFeature, DatasetFeatureTemplate, DatasetType


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

        self.resolved_asset_names[os_path] = name
        self.resolved_asset_urls[os_path] = url

        return url

    def upload(self):
        for path, name in self.resolved_asset_names.items():
            key = f"{self.prefix}/{name}"
            if s3.object_exists(self.s3_client, self.bucket, key):
                continue

            self.s3_client.upload_file(Filename=str(path), Bucket=self.bucket, Key=key)
            print(f"Uploaded asset: path={path}, key={key}")


class DatasetSite(BaseModel):
    assets: set[Asset]
    dataset_types: dict[str, DatasetType]
    dataset_families: dict[str, DatasetFamily]


def build_dataset_site(cli_context: Context) -> DatasetSite:
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
            elif (
                existing_type.document_context.os_path != type_.document_context.os_path
            ):
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
