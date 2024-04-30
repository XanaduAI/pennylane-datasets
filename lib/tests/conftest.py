from pathlib import Path

import pytest
from dulwich.repo import Repo


@pytest.fixture
def test_support_dir():
    repo = Repo.discover()

    return Path(repo.path, "lib", "tests", "support")
