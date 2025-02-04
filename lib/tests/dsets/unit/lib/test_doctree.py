import json
from pathlib import Path
from typing import Any

import pytest
from dsets.lib.doctree import (
    Doctree,
    Document,
    Ref,
    Reference,
)
from pydantic import BaseModel


class UserList(BaseModel):
    """Non-referencing model for tests."""

    users: list[str]


class ReferencedModel(Document):
    """A referenced model."""

    name: str
    user_list: Ref[UserList]
    meta: Ref[dict[str, Any]]


class RootModel(Document):
    """A referencing model."""

    name: str
    citation: Ref[str]
    about: Ref[str]
    references: dict[str, Ref[ReferencedModel]]
    user_list: Ref[UserList]
    maybe_null: Ref[dict[str, Any]] | None


@pytest.fixture
def docpath_root(tmpdir):
    """Document root dir."""

    root = Path(tmpdir) / "data"
    root.mkdir()

    return root


@pytest.fixture
def doctree(docpath_root):
    return Doctree(docpath_root)


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
                "user_list": {"$path": "/users/userlist.json"},  # Absolute path
                "meta": {"$path": "meta.json"},
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
                "about": {"$path": "text/about.txt"},
                "references": {
                    "full_ref": {"$path": "referenced_model.json"},
                    "inline": {
                        "name": "inline",
                        "user_list": {"$path": "/users/userlist.json"},
                        "meta": {"$path": "meta.json"},
                    },
                },
                "user_list": {"$path": "../users/userlist.json"},
                "maybe_null": None,
            },
            f,
        )


@pytest.mark.usefixtures("setup_test_docs")
def test_load_from_path(doctree: Doctree):
    """Test that `load_from_path` can resolve a mix of absolute
    and relative document references."""

    model = RootModel.from_os_path(
        doctree,
        doctree.docpath_root / "models" / "root_model.json",
        resolve_refs=True,
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
def test_load_from_path_no_resolve_refs(doctree: Doctree):
    """Test that `load_from_path` can load documents without
    resolving references."""

    model = RootModel.from_os_path(
        doctree,
        doctree.docpath_root / "models" / "root_model.json",
        resolve_refs=False,
    )

    # Check that types are preserved
    assert isinstance(model, RootModel)
    assert isinstance(model.references["full_ref"], Reference)
    assert isinstance(model.references["inline"], ReferencedModel)
    assert isinstance(model.references["inline"].user_list, Reference)
    assert isinstance(model.user_list, Reference)

    assert model.model_dump(mode="json", by_alias=True) == {
        "name": "model",
        "citation": "Me, September",
        "about": {"$path": "text/about.txt"},
        "references": {
            "full_ref": {"$path": "referenced_model.json"},
            "inline": {
                "name": "inline",
                "user_list": {"$path": "/users/userlist.json"},
                "meta": {"$path": "meta.json"},
            },
        },
        "user_list": {"$path": "../users/userlist.json"},
        "maybe_null": None,
    }


def test_model_dump_reference():
    """Test that unresolved references can be serialized."""

    assert ReferencedModel(
        name="test",
        user_list=Reference[UserList](path="/a/b/c"),
        meta=Reference[dict[str, Any]](path="x"),
    ).model_dump(mode="json", by_alias=True) == {
        "name": "test",
        "user_list": {"$path": "/a/b/c"},
        "meta": {"$path": "x"},
    }
