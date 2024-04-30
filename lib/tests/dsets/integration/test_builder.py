import json

from dsets.builder import compile_dataset_build


def test_compile_dataset_build(test_support_dir, tmp_path):
    """Test that ``compile_dataset_build`` produces the expected
    output in the 'datasets-build.json' file."""
    asset_url_prefix = "https://test.datasets.com/assets"

    build = compile_dataset_build(
        tmp_path, test_support_dir / "content", asset_url_prefix
    )

    with open(test_support_dir / "datasets-build.json", "r", encoding="utf-8") as f:
        expected_build = json.load(f)

    assert build == expected_build
