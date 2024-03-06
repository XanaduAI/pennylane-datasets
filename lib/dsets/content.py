import typing
from pathlib import Path
from typing import Self

from pydantic import BaseModel

from dsets.lib.json_ref import get_document_context

from .schemas import DatasetFamily, DatasetType


class DatasetContentBuilder(BaseModel):
    """Builds dataset content.

    Attributes:
        dataset_types: Mapping of dataset types by name
        dataset_families: Mapping of dataset families by slug
    """

    dataset_types: dict[str, DatasetType]
    dataset_families: dict[str, DatasetFamily]

    @classmethod
    def load_content(cls: type[Self], content_dir: Path | str) -> Self:
        """Load datasets content from content dir."""
        content_dir = Path(content_dir)
        dataset_types: dict[str, DatasetType] = {}
        dataset_families: dict[str, DatasetFamily] = {}

        for dataset_json_path in content_dir.rglob("**/dataset.json"):
            family = DatasetFamily.load_from_path(
                content_dir, dataset_json_path, resolve_refs=True
            )

            if family.slug in dataset_families:
                raise RuntimeError(
                    f"DatasetFamily with slug '{family.slug}' already exists"
                )

            type_ = typing.cast(DatasetType, family.type_)
            if not (existing_type := dataset_types.get(type_.name)):
                dataset_types[type_.name] = type_
            elif get_document_context(existing_type) != get_document_context(type_):
                raise RuntimeError(
                    f"Duplicate 'DatasetType' definition on family '{family.slug}'"
                )

            dataset_families[family.slug] = family

        return cls(dataset_types=dataset_types, dataset_families=dataset_families)

    def datasets_build(self, out_path: Path | str) -> None:
        """Compile all datasets content into a JSON file."""
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=2, by_alias=True))
