import logging
from pathlib import Path
from typing import Annotated

import typer

from dsets.lib import progress, s3
from dsets.settings import CLIContext

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
    ctx = CLIContext()
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


def configure_logging(level=logging.INFO):
    logging.basicConfig(level=level)


def main():
    configure_logging()
    app()
