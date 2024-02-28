from pathlib import Path

import pytest
from dsets.lib.file_hash import file_sha1_hash


def test_fail():
    raise ValueError


@pytest.mark.parametrize("chunk_size", [1, 16])
def test_file_sha1_hash(tmp_path: Path, chunk_size):
    """Test that `file_sha1_hash()` returns the correct SHA1 hash
    of the file contents."""
    with open(tmp_path / "file.txt", "w", encoding="utf-8") as f:
        f.write("abcdefghijklmnop")

    assert (
        file_sha1_hash(tmp_path / "file.txt", chunk_size=chunk_size).hex()
        == "14f3995288acd189e6e50a7af47ee7099aa682b9"
    )
