from collections.abc import Iterator

from dsets.lib.doctree import Doctree
from dsets.schemas import DatasetClass


def load_all_classes(doctree: Doctree) -> Iterator[DatasetClass]:
    """Get all classes defin"""
    for class_json_path in doctree.docpath_root.rglob("**/class.json"):
        yield DatasetClass.from_os_path(doctree, class_json_path)
