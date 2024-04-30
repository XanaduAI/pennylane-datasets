import json
import logging
from pathlib import Path
from typing import Annotated, Optional

import typer

from dsets.lib import json_fmt, msg, progress, s3
from dsets.settings import CLIContext

from .builder import AssetLoader, compile_dataset_build

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
        ctx.settings.bucket_prefix_data,
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

    site_build = compile_dataset_build(
        build_dir, ctx.content_dir, ctx.settings.asset_url_prefix
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
        ctx.s3_client, ctx.settings.bucket_name, ctx.settings.bucket_prefix_assets
    )
    msg.structured_print("Uploaded assets", count=uploaded)


@app.command(name="deploy-build")
def deploy_build(
    env: str,
    tags: Annotated[Optional[list[str]], typer.Argument(help="Extra tags")] = None,
):
    """Deploy datasets-build.json to S3.
    Args:
        env: Targeted environment, e.g 'dev', 'staging', 'prod'.
        tags: Extra tags for deployment
    """
    ctx = CLIContext()
    env = env.strip()
    tagset: set[str] = set(tag.strip() for tag in tags) if tags else set()
    tagset.add(ctx.commit_sha(short=True))

    if (short_sha := ctx.commit_sha(short=True)) not in tagset:
        tagset.add(short_sha)

    bucket = ctx.settings.bucket_name
    build_key_prefix = ctx.settings.bucket_prefix_build
    build_file_key = str(build_key_prefix / "datasets-build.json")

    ctx.s3_client.upload_file(
        Bucket=bucket,
        Key=build_file_key,
        Filename=str(ctx.build_dir / "datasets-build.json"),
        ExtraArgs={"ContentType": "application/json"},
    )

    build_info_file_key = str(build_key_prefix / ".datasets-build-info.json")
    build_info_json = json.dumps(
        {"commit_sha": ctx.commit_sha(), "env": env, "tags": list(tagset)}
    ).encode("utf-8")

    ctx.s3_client.put_object(
        Bucket=bucket,
        Key=build_info_file_key,
        Body=build_info_json,
        ContentType="application/json",
    )

    msg.structured_print(
        "Deployed build", bucket=bucket, key=build_file_key, tags=tagset
    )


@app.command(name="format")
def format(check: bool = False):
    """Format dataset metadata files in the content directory."""
    changed_msg_template = (
        "{path} would be reformatted" if check else "{path} reformatted"
    )
    ctx = CLIContext()

    changed = 0
    unchanged = 0
    for json_file in ctx.content_dir.rglob("**/*.json"):
        if json_fmt.format(json_file, check=check):
            changed += 1
            print(changed_msg_template.format(path=str(json_file)))
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
