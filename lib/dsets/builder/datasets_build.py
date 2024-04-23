import typing

from pydantic import BaseModel

from dsets.lib.doctree import Asset, Doctree
from dsets.lib.pydantic_util import CamelCaseMixin
from dsets.schemas import DatasetClass, DatasetFamily
from dsets.settings import CLIContext

from .asset import AssetLoader


class DatasetBuild(BaseModel, CamelCaseMixin):
    """
    Model for the 'datasets-buid.json' file. Contains all dataset families
    and types defined in the `content/` directory, and an inventory of
    every asset used.
    """

    assets: set[Asset]
    dataset_classes: dict[str, DatasetClass]
    dataset_families: dict[str, DatasetFamily]


def build_dataset_site(cli_context: CLIContext) -> dict[str, typing.Any]:
    """Compiles all `dataset.json` files in the `content/` directory into
    a single JSON document. All referenced documents will be included,
    and local assets will be uploaded to the assets directory in the datasets bucket.

    Args:
        cli_context: The CLI context

    Returns:
        A JSON-able dict containing all dataset content
    """
    build_dir = cli_context.repo_root / "_build"
    build_dir.mkdir(exist_ok=True)

    doctree = Doctree(cli_context.content_dir)

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

    asset_loader = AssetLoader(
        cli_context.build_dir, cli_context.settings.asset_url_prefix
    )
    for asset in doctree.get_objects(Asset):
        asset.root = asset_loader.add_asset(asset)

    return DatasetBuild(
        assets=doctree.get_objects(Asset),
        dataset_classes=dataset_classes,
        dataset_families=dataset_families,
    ).model_dump(
        mode="json",
        by_alias=True,
    )
