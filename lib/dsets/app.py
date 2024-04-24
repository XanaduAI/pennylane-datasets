import json
import logging
from pathlib import Path
from typing import Annotated

import typer

from dsets.lib import json_fmt, progress, s3
from dsets.settings import CLIContext

from .builder import AssetLoader, build_dataset_site

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
    prefix = s3.S3Path(prefix_) if prefix_ else None

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

    ctx = CLIContext()
    build_dir = ctx.build_dir
    build_dir.mkdir(exist_ok=True)
    build_file = build_dir / "datasets-build.json"

    site_build = build_dataset_site(
        build_dir, ctx.content_dir, ctx.settings.asset_url_prefix
    )
    with open(build_file, "w", encoding="utf-8") as f:
        json.dump(site_build, f, indent=2)

    print(f"Created build in '{build_file}'")


@app.command(name="upload-assets")
def upload_assets():
    """Upload assets from the build directory."""
    ctx = CLIContext()

    asset_loader = AssetLoader(ctx.build_dir, ctx.settings.asset_url_prefix)

    uploaded = asset_loader.upload_assets(
        ctx.s3_client, ctx.settings.bucket_name, ctx.settings.bucket_asset_key_prefix
    )
    print(f"Uploaded {uploaded} assets")


@app.command(name="push-build")
def push_build(latest: bool = False):
    ctx = CLIContext()

    tags = [ctx.ref]
    if latest:
        tags.append("latest")

    for tag in tags:
        key = str(ctx.settings.bucket_build_key_prefix / ctx.branch / f"{tag}.json")
        ctx.s3_client.upload_file(
            Filename=str(ctx.build_dir / "datasets-build.json"),
            Bucket=ctx.settings.bucket_name,
            Key=key,
        )
        print(f"Pushed datasets build: bucket={ctx.settings.bucket_name}, key={key}")


@app.command(name="format")
def format(check: bool = False):
    """Format dataset metadata files in the content directory."""
    ctx = CLIContext()

    formatter = json_fmt.JSONFormatter()
    changed = 0
    unchanged = 0
    for json_file in ctx.content_dir.rglob("**/*.json"):
        if formatter.format(json_file, check=check):
            changed += 1
        else:
            unchanged += 1

    if check and changed:
        print(f"{changed} file(s) would be reformatted.")
        raise typer.Exit(1)

    if changed:
        print(f"{changed} file(s) reformatted.")


def configure_logging(level=logging.INFO):
    logging.basicConfig(level=level)


def main():
    configure_logging()
    app()
