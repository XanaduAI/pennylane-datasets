import json
from pathlib import Path
from typing import Any

import pytest
from dsets.lib.json_ref import DocumentRef, DocumentTreeModel, Reference
from pydantic import BaseModel


class UserList(BaseModel):
    """Non-referencing model for tests."""

    users: list[str]


class ReferencedModel(DocumentTreeModel):
    """A referenced model."""

    name: str
    user_list: Reference[UserList]
    meta: Reference[dict[str, Any]]


class RootModel(DocumentTreeModel):
    """A referencing model."""

    name: str
    citation: Reference[str]
    about: Reference[str]
    references: dict[str, Reference[ReferencedModel]]
    user_list: Reference[UserList]
    maybe_null: Reference[dict[str, Any]] | None


@pytest.fixture
def docpath_root(tmpdir):
    """Document root dir."""

    root = Path(tmpdir) / "data"
    root.mkdir()

    return root


@pytest.fixture
def setup_test_docs(docpath_root: Path):
    users_dir = docpath_root / "users"
    users_dir.mkdir()

    with open(users_dir / "userlist.json", "w") as f:
        json.dump({"users": ["A. User", "Foo"]}, f)

    models_dir = docpath_root / "models"
    models_dir.mkdir()

    with open(models_dir / "meta.json", "w") as f:
        json.dump({"created_at": "2024-03-05T14:02:01.604165Z"}, f)

    with open(models_dir / "referenced_model.json", "w") as f:
        json.dump(
            {
                "name": "referenced",
                "user_list": {"$ref": "/users/userlist.json"},  # Absolute path
                "meta": {"$ref": "meta.json"},
            },
            f,
        )

    text_dir = models_dir / "text"
    text_dir.mkdir()

    with open(text_dir / "about.txt", "w") as f:
        f.write("This is a model!")

    with open(models_dir / "root_model.json", "w") as f:
        json.dump(
            {
                "name": "model",
                "citation": "Me, September",
                "about": {"$ref": "text/about.txt"},
                "references": {
                    "full_ref": {"$ref": "referenced_model.json"},
                    "inline": {
                        "name": "inline",
                        "user_list": {"$ref": "/users/userlist.json"},
                        "meta": {"$ref": "meta.json"},
                    },
                },
                "user_list": {"$ref": "../users/userlist.json"},
                "maybe_null": None,
            },
            f,
        )


@pytest.mark.usefixtures("setup_test_docs")
def test_load_from_path(docpath_root: Path):
    """Test that `load_from_path` can resolve a mix of absolute
    and relative document references."""

    model = RootModel.load_from_path(
        docpath_root, docpath_root / "models" / "root_model.json", resolve_refs=True
    )

    # Check that types are preserved
    assert isinstance(model, RootModel)
    assert isinstance(model.references["full_ref"], ReferencedModel)
    assert isinstance(model.references["full_ref"].user_list, UserList)
    assert isinstance(model.references["inline"], ReferencedModel)
    assert isinstance(model.references["inline"].user_list, UserList)
    assert isinstance(model.user_list, UserList)

    assert model.model_dump() == {
        "name": "model",
        "citation": "Me, September",
        "about": "This is a model!",
        "references": {
            "full_ref": {
                "name": "referenced",
                "user_list": {"users": ["A. User", "Foo"]},
                "meta": {"created_at": "2024-03-05T14:02:01.604165Z"},
            },
            "inline": {
                "name": "inline",
                "user_list": {"users": ["A. User", "Foo"]},
                "meta": {"created_at": "2024-03-05T14:02:01.604165Z"},
            },
        },
        "user_list": {"users": ["A. User", "Foo"]},
        "maybe_null": None,
    }


@pytest.mark.usefixtures("setup_test_docs")
def test_load_from_path_no_resolve_refs(docpath_root: Path):
    """Test that `load_from_path` can load documents without
    resolving references."""

    model = RootModel.load_from_path(
        docpath_root, docpath_root / "models" / "root_model.json", resolve_refs=False
    )

    # Check that types are preserved
    assert isinstance(model, RootModel)
    assert isinstance(model.references["full_ref"], DocumentRef)
    assert isinstance(model.references["inline"], ReferencedModel)
    assert isinstance(model.references["inline"].user_list, DocumentRef)
    assert isinstance(model.user_list, DocumentRef)

    assert model.model_dump(mode="json", by_alias=True) == {
        "name": "model",
        "citation": "Me, September",
        "about": {"$ref": "text/about.txt"},
        "references": {
            "full_ref": {"$ref": "referenced_model.json"},
            "inline": {
                "name": "inline",
                "user_list": {"$ref": "/users/userlist.json"},
                "meta": {"$ref": "meta.json"},
            },
        },
        "user_list": {"$ref": "../users/userlist.json"},
        "maybe_null": None,
    }


def test_model_dump_reference():
    """Test that unresolved references can be serialized."""

    assert ReferencedModel(
        name="test",
        user_list=DocumentRef[UserList](ref="/a/b/c"),
        meta=DocumentRef[dict[str, Any]](ref="x"),
    ).model_dump(mode="json", by_alias=True) == {
        "name": "test",
        "user_list": {"$ref": "/a/b/c"},
        "meta": {"$ref": "x"},
    }
