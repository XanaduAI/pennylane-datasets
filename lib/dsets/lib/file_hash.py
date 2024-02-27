import hashlib
from collections.abc import Callable
from pathlib import Path


def file_sha1_hash(
    path: Path,
    *,
    chunk_size: int = 4194304,
    progress_cb: Callable[[int], None] | None = None,
) -> bytes:
    """Compute SHA1 hash of file at `path`.

    Args:
        path: Path to file
        chunk_size: Number of bytes to read at a time. Defaults to 4MB
        progress_cb: Callable that accepts the number of bytes
            read in each iteration

    Returns:
        bytes: SHA1 hash of file
    """
    with open(path, mode="rb") as f:
        digest = hashlib.sha1()
        while chunk := f.read(chunk_size):
            digest.update(chunk)
            if progress_cb:
                progress_cb(len(chunk))

        return digest.digest()
