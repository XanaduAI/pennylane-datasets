from pathlib import Path

from pennylane.data import Dataset


def check_file_is_dataset(path: Path):
    """Check that the file at ``path`` is a valid dataset. Raise an informative
    exception if it is not."""

    dataset = Dataset.open(path)
    dataset.close()
