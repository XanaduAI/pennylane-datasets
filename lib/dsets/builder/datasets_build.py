import shutil
import typing
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from dsets.lib.doctree import Asset, Doctree
from dsets.lib.pydantic_util import CamelCaseMixin
from dsets.schemas import DatasetClass, DatasetCollection, DatasetFamily

from .assets import AssetLoader


class DatasetBuild(BaseModel, CamelCaseMixin):
    """
    Model for the 'datasets-build.json' file. Contains all dataset families
    and types defined in the `content/` directory, and an inventory of
    every asset used.
    """

    assets: set[Asset]
    dataset_classes: dict[str, DatasetClass]
    dataset_families: dict[str, DatasetFamily]
    dataset_collections: dict[str, DatasetCollection]


def compile_dataset_build(
    build_dir: Path, content_dir: Path, asset_destination_url_prefix: str
) -> dict[str, Any]:
    """Compiles all `dataset.json` files in the `content/` directory into
    a single JSON document. All referenced documents will be included,
    and local assets will be uploaded to the assets directory in the datasets bucket.

    Args:
        build_dir: The build directory
        content_dir: The content directory
        asset_destination_url_prefix: The URL prefix where uploaded assets (images, etc)
            can be accessed.

    Returns:
        A JSON-able dict containing all dataset content
    """
    if build_dir.exists():
        shutil.rmtree(build_dir)

    build_dir.mkdir()
    doctree = Doctree(content_dir)

    dataset_classes: dict[str, DatasetClass] = {}
    dataset_families: dict[str, DatasetFamily] = {}
    dataset_collections: dict[str, DatasetCollection] = {}

    for dataset_json_path in content_dir.rglob("**/dataset.json"):
        family = DatasetFamily.from_os_path(
            doctree, dataset_json_path, resolve_refs=True
        )

        if family.slug in dataset_families:
            raise RuntimeError(
                f"DatasetFamily with slug '{family.slug}' already exists"
            )

        class_ = typing.cast(DatasetClass, family.class_)
        if not (existing_type := dataset_classes.get(class_.slug)):
            dataset_classes[class_.slug] = class_
        elif existing_type.document_context.os_path != class_.document_context.os_path:
            raise RuntimeError(
                f"Duplicate 'DatasetClass' definition on family '{family.slug}'"
            )

        collection = typing.cast(DatasetCollection | None, family.collection)
        if collection:
            existing = existing = dataset_collections.get(collection.slug)
            if not existing:
                dataset_collections[collection.slug] = collection
            elif (
                existing.document_context.os_path != collection.document_context.os_path
            ):
                raise RuntimeError(
                    f"Duplicate 'DatasetCollection' definition on family '{family.slug}'"
                )

        dataset_families[family.slug] = family

    asset_loader = AssetLoader(build_dir, asset_destination_url_prefix)
    for asset in doctree.get_objects(Asset):
        asset.root = asset_loader.add_asset(asset)

    build = DatasetBuild(
        assets=doctree.get_objects(Asset),
        dataset_classes=dataset_classes,
        dataset_families=dataset_families,
        dataset_collections=dataset_collections,
    ).model_dump(
        mode="json",
        by_alias=True,
    )

    build["assets"].sort()

    return build
