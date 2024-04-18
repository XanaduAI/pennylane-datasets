from pathlib import Path
from typing import Annotated

import typer

from dsets.context import Context
from dsets.lib import progress, s3

from .content import build_dataset_site

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
        ctx.settings.bucket_name,
        ctx.settings.bucket_data_key_prefix,
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

    site_build = build_dataset_site(ctx)
    with open(build_file, "w", encoding="utf-8") as f:
        f.write(site_build.model_dump_json(indent=2))

    print(f"Created build in '{build_file}'")
