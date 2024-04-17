from pathlib import Path
from typing import Annotated

import typer

from dsets.lib import progress, s3
from dsets.lib.context import Context

from .content import build as builder
from .content import make_asset_uploader

app = typer.Typer(name="dsets", add_completion=True)


@app.command()
def version():
    """Print version and exit."""
    print("0.1.0")


@app.command(name="upload")
def upload(
    src_file: Annotated[
        Path,
        typer.Argument(help="Path to dataset .h5 file", file_okay=True, dir_okay=False),
    ],
    prefix_: Annotated[
        str,
        typer.Option(
            "--prefix",
            help="Prefix for file in data bucket",
        ),
    ] = "",
) -> None:
    """Upload a new dataset file to the data bucket, and create an upload
    receipt in pennylane-datasets/data.
    """
    ctx = Context()
    src_file = src_file.expanduser()
    prefix = s3.S3Path(prefix_)

    repo = s3.S3DatasetRepo(
        ctx.data_dir,
        ctx.s3_client,
        ctx.settings.data_bucket_name,
        ctx.settings.data_bucket_key_prefix,
    )

    print(f"Uploading '{src_file.absolute()}'")
    file_size = src_file.stat().st_size

    with progress.IOProgressBarManager() as pbars:
        key = repo.upload_file(
            src_file,
            prefix,
            hash_progress_cb=pbars.add_bar(file_size, "Generating SHA1 hash..."),
            upload_progress_cb=pbars.add_bar(file_size, "Uploading..."),
        )

    print(f"File uploaded to '{key}'. Be sure to commit upload receipt!")


@app.command(name="build")
def build():
    """Compile 'datasets-build.json' from content directory."""

    ctx = Context()
    build_dir = ctx.repo_root / "_build"
    build_dir.mkdir(exist_ok=True)
    build_file = build_dir / "datasets-build.json"

    builder(
        ctx.content_dir,
        make_asset_uploader(
            ctx.settings.data_bucket_name,
            ctx.settings.data_bucket_assets_prefix,
            ctx.settings.assert_url_prefix,
        ),
    )

    print(f"Created build in '{build_file}'")
