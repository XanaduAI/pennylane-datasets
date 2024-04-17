import json
import typing
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import boto3
import jinja2
from pydantic import BaseModel

from dsets.lib.json_ref import Doctree
from dsets.lib.json_ref.builder import AssetUploader, compile_doctree

from .schemas import DatasetFamily, DatasetFeature, DatasetFeatureTemplate, DatasetType


class DatasetSite(BaseModel):
    dataset_types: dict[str, DatasetType]
    dataset_families: dict[str, DatasetFamily]
    assets: list[str]


@dataclass
class DatasetContentBuilder:
    """Builds dataset content.

    Attributes:
        dataset_types: Mapping of dataset types by name
        dataset_families: Mapping of dataset families by slug
    """

    dataset_types: dict[str, DatasetType]
    dataset_families: dict[str, DatasetFamily]

    doctree: Doctree
    destination_url: str
    assets_prefix: str = "assets"

    @classmethod
    def load_content(
        cls: type[Self], content_dir: Path | str, destination_url: str
    ) -> Self:
        """Load datasets content from content dir."""
        content_dir = Path(content_dir)
        dataset_types: dict[str, DatasetType] = {}
        dataset_families: dict[str, DatasetFamily] = {}

        doctree = Doctree(content_dir)

        for dataset_json_path in content_dir.rglob("**/dataset.json"):
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

        return cls(
            doctree=doctree,
            destination_url=destination_url,
            dataset_types=dataset_types,
            dataset_families=dataset_families,
        )

    def datasets_build(self, out_path: Path | str) -> None:
        """Compile all datasets content into a JSON file."""
        for dataset_family in self.dataset_families.values():
            compile_feature_templates(dataset_family)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(
                self.model_dump(mode="json", exclude_defaults=True, by_alias=True),
                f,
                indent=2,
                sort_keys=True,
            )


def make_asset_uploader(
    bucket: str, prefix: str, destination_url_prefix: str
) -> AssetUploader:
    return AssetUploader(destination_url_prefix, boto3.client("s3"), bucket, prefix)


def build(content_dir: Path, asset_uploader: AssetUploader):
    doctree = Doctree(content_dir)

    dataset_types: dict[str, DatasetType] = {}
    dataset_families: dict[str, DatasetFamily] = {}

    for dataset_json_path in content_dir.rglob("**/dataset.json"):
        family = DatasetFamily.from_os_path(
            doctree, dataset_json_path, resolve_refs=True
        )

        doctree = Doctree(content_dir)

        for dataset_json_path in content_dir.rglob("**/dataset.json"):
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

    for dataset_family in dataset_families.values():
        compile_feature_templates(dataset_family)

    compiled = compile_doctree(doctree, asset_uploader)

    with open("datasets-build.json", "w", encoding="utf-8") as f:
        json.dump(compiled, f, indent=2)


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
