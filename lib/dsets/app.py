import json
import logging
from pathlib import Path
from typing import Annotated

import typer

from dsets.lib import json_fmt, msg, progress, s3
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
        build_dir, ctx.content_dir, ctx.settings.public_url_root_assets
    )

    with open(build_file, "w", encoding="utf-8") as f:
        json.dump(site_build, f, indent=2)

    msg.structured_print("Created build", file=build_file)


@app.command(name="upload-assets")
def upload_assets():
    """Upload assets from the build directory."""
    ctx = CLIContext()

    asset_loader = AssetLoader(ctx.build_dir, ctx.settings.public_url_root_assets)

    uploaded = asset_loader.upload_assets(
        ctx.s3_client, ctx.settings.bucket_name, ctx.settings.bucket_asset_key_prefix
    )
    msg.structured_print("Uploaded assets", count=uploaded)


@app.command(name="push-build")
def push_build(branch: str, ref: str, latest: bool = False):
    ctx = CLIContext()

    name = f"{ref}.json"

    key = str(ctx.settings.bucket_build_key_prefix / branch / name)
    ctx.s3_client.upload_file(
        Filename=str(ctx.build_dir / "datasets-build.json"),
        Bucket=ctx.settings.bucket_name,
        Key=key,
    )

    msg.structured_print(
        "Pushed datasets build", bucket=ctx.settings.bucket_name, key=key
    )
    if latest:
        ctx.s3_client.put_object(
            Bucket=ctx.settings.bucket_name,
            Key=str(ctx.settings.bucket_build_key_prefix / branch / ".latest"),
            Body=ref.encode("utf-8"),
        )
        msg.structured_print("Tagged latest", branch=branch, ref=ref)


@app.command(name="deploy-build")
def deploy_build(branch: str, ref: str = "latest"):
    ctx = CLIContext()

    bucket = ctx.settings.bucket_name
    build_key_prefix = ctx.settings.bucket_build_key_prefix

    deploy_file_key = ctx.settings.bucket_build_key_prefix / ".deploy"

    if ref == "latest":
        ref = s3.object_text(
            ctx.s3_client, bucket, build_key_prefix / branch / ".latest"
        )

    build_file_key = (build_key_prefix / branch / ref).with_suffix(".json")
    if not s3.object_exists(
        ctx.s3_client, bucket=ctx.settings.bucket_name, key=build_file_key
    ):
        raise RuntimeError(
            msg.structured(
                "Build not found", branch=branch, ref=ref, key=build_file_key
            )
        )

    ctx.s3_client.put_object(
        Bucket=ctx.settings.bucket_name,
        Key=str(deploy_file_key),
        Body=str(s3.S3Path(branch, ref).with_suffix(".json")).encode("utf-8"),
    )

    msg.structured_print("Deployed build", branch=branch, ref=ref, key=build_file_key)


@app.command(name="deploy")
def deploy():
    ctx = CLIContext()

    bucket = ctx.settings.bucket_name
    build_key_prefix = ctx.settings.bucket_build_key_prefix

    build_file_key = build_key_prefix / "datasets-build.json"

    ctx.s3_client.upload_file(
        Bucket=ctx.settings.bucket_name,
        Key=str(build_file_key),
        Filename=str(ctx.build_dir / "datasets-build.json"),
    )

    msg.structured_print("Deployed build", bucket=bucket, key=build_file_key)


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
