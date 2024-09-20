import json
import logging
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import inflection
import typer
from pennylane.data import Dataset

from dsets import schemas
from dsets.lib import (
    auth,
    bibtex,
    device_auth,
    doctree,
    json_fmt,
    markdown,
    msg,
    progress,
    s3,
    time,
)
from dsets.schemas import fields
from dsets.settings import CLIContext

from .builder import AssetLoader, compile_dataset_build

AUTH_URL = "https://auth.dev.cloud.pennylane.ai/oauth"
CLIENT_ID = "5miHebfuYvVwUW68nVoPOjdRAjioS483"

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

    datasets_build = compile_dataset_build(
        build_dir, ctx.content_dir, ctx.settings.url_prefix_assets
    )
    with open(build_file, "w", encoding="utf-8") as f:
        json.dump(datasets_build, f, indent=2)

    msg.structured_print("Created build", file=build_file)


@app.command(name="add")
def add(dataset_file: Path, class_slug: Annotated[str, typer.Option(prompt=True)]):
    """
    Add a new dataset to an existing family, or create a new one.
    """
    ctx = CLIContext()

    content_doctree = doctree.Doctree(ctx.content_dir)

    fields.validate(fields.Slug, class_slug)

    dataset = Dataset.open(dataset_file)

    class_dir = ctx.content_dir / class_slug
    class_doc = class_dir / "_meta" / "class.json"
    if not class_doc.exists():
        typer.confirm(
            f"Class {repr(class_slug)} does not exist. Create it?",
            abort=True,
            default=True,
        )

        class_name = fields.validate(
            fields.PythonIdentifier,
            inflection.camelize(class_slug.replace("-", "_")),
            err=False,
        )

        while True:
            class_name = typer.prompt("Enter class name", default=class_name).strip()
            if not fields.validate(fields.PythonIdentifier, class_name):
                print(
                    f"Invalid class name: {repr(class_name)} (must be a valid Python identifier)"
                )
            else:
                break

        params = []
        define_params = typer.confirm(
            f"Define parameters for class {repr(class_slug)}?", default=True
        )

        while define_params:
            name = typer.prompt(
                "Enter parameter name (leave blank to finish)",
                default="",
                show_default=False,
            )
            if not name:
                break
            if not fields.validate(fields.PythonIdentifier, name):
                print(
                    f"Invalid parameter name: {repr(name)} (must be a valid Python identifer)"
                )
                continue

            title = inflection.titleize(name)
            title = typer.prompt(
                f"\tEnter title for parameter {repr(name)} ({repr(title)})",
                default=title,
            )

            description = typer.prompt(
                f"\tEnter description for parameter {repr(name)}",
                default="",
                show_default=False,
            )

            params.append(
                schemas.DatasetParameter(
                    name=name, title=title, description=description
                )
            )

        attrs = [
            schemas.DatasetAttribute(
                name=name, python_type=str(info.py_type), doc=info.doc or ""
            )
            for name, info in dataset.attr_info.items()
        ]

        class_ = schemas.DatasetClass(
            slug=class_slug,
            name=class_name,
            attribute_list=attrs,
            parameter_list=params,
        )

        class_doc.parent.mkdir(parents=True, exist_ok=True)
        with open(class_doc, "w", encoding="utf-8") as f:
            f.write(class_.model_dump_json(indent=2, by_alias=True))
            print(f"Created class file: {class_doc}")
    else:
        class_ = schemas.DatasetClass.from_os_path(content_doctree, class_doc)

    family_slug = dataset_file.stem.split("_")[0].lower()
    family_slug = typer.prompt(
        "Enter family slug", default=family_slug, show_default=True
    )
    fields.validate(fields.Slug, family_slug)
    family_doc = ctx.content_dir / class_slug / family_slug / "dataset.json"

    today = str(datetime.now().date())

    if family_doc.exists():
        family = schemas.DatasetFamily.from_os_path(content_doctree, family_doc)
        family.date_of_last_modification = today
    else:
        print(f"Creating new family with slug {repr(family_slug)}")
        family_title = typer.prompt(
            "Enter title", default=inflection.humanize(family_slug.replace("-", "_"))
        )
        download_name = typer.prompt("Enter download name", default="name")
        description = typer.prompt("Enter description", default="description")

        family = schemas.DatasetFamily(
            slug=family_slug,
            class_=doctree.Reference[schemas.DatasetClass](
                path=doctree.DocPath("/", class_doc.relative_to(ctx.content_dir))
            ),
            download_name=download_name,
            features=[
                schemas.DatasetFeature(
                    slug="example-feature",
                    title="Example Feature",
                    content=doctree.Reference[str](
                        path="features/dataset-attributes.md"
                    ),
                )
            ],
            meta=doctree.Reference[schemas.DatasetFamilyMeta](path="meta.json"),
        )

        authors = [
            author.strip()
            for author in typer.prompt("Enter authors (author1,author2,...)")
            .strip()
            .split(",")
        ]

        meta = schemas.DatasetFamilyMeta(
            title=family_title,
            description=description,
            citation=doctree.Reference[fields.BibtexStr](path="citation.txt"),
            using_this_dataset=doctree.Reference[str](path="using_this_dataset.md"),
            license="[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en)",
            authors=authors,
            date_of_last_modification=today,
            date_of_publication=today,
        )
        family_doc.parent.mkdir(parents=True, exist_ok=True)

        with open(family_doc.parent / "meta.json", "w", encoding="utf-8") as f:
            f.write(meta.model_dump_json(indent=2, by_alias=True))

        with open(family_doc.parent / "citation.txt", "w", encoding="utf-8") as f:
            f.write(
                bibtex.generate_bibtex(
                    family_slug,
                    family_title,
                    authors=authors,
                    publication_url=f"https://pennylane.ai/datasets/{class_slug}/{family_slug}",
                )
            )

        with open(
            family_doc.parent / "using_this_dataset.md", "w", encoding="utf-8"
        ) as f:
            f.write("# Using this Dataset")

        features_dir = family_doc.parent / "features"
        features_dir.mkdir()

        with open(features_dir / "dataset-attributes.md", "w", encoding="utf-8") as f:
            f.write(
                markdown.make_markdown_table(
                    ("Name", "Type", "Description"),
                    [
                        (attribute.name, attribute.python_type, attribute.doc)
                        for attribute in class_.attribute_list
                    ],
                )
            )

    param_values = {}
    for param in class_.parameter_list:
        if param.optional:
            default = "N/A"
        else:
            default = None

        value = typer.prompt(
            f"Enter value for parameter {repr(param.name)}", default=default
        ).strip()
        param_values[param.name] = value

    family.data.append(schemas.Dataset(parameters=param_values))

    with open(family_doc, "w", encoding="utf-8") as f:
        f.write(family.model_dump_json(indent=2, by_alias=True))

    print(f"Wrote data to {family_doc}")


@app.command(name="upload-assets")
def upload_assets():
    """Upload assets from the build directory."""
    ctx = CLIContext()

    asset_loader = AssetLoader(ctx.build_dir, ctx.settings.url_prefix_assets)

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

    metadata = {"commit_sha": ctx.commit_sha(), "env": "env", "tags": list(tagset)}

    ctx.s3_client.upload_file(
        Bucket=bucket,
        Key=build_file_key,
        Filename=str(ctx.build_dir / "datasets-build.json"),
        ExtraArgs={
            "ContentType": "application/json",
            "Metadata": {
                ctx.settings.datasets_build_s3_metadata_key: json.dumps(metadata)
            },
        },
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


@app.command(name="login")
def login():
    """Login to pennylane.ai account."""
    ctx = CLIContext()
    auth_path = ctx.auth_dir

    print("Checking credentials...")
    if auth.check_local_token(auth_path):
        print("Found a valid token")
        print("You are logged into your pennylane.ai account.")
        return

    if not auth_path.exists():
        auth_path.mkdir()

    print("No valid credentials found.")
    print(f"Starting login to '{AUTH_URL}'")
    grant = device_auth.OAuthDeviceCodeGrant(
        oauth_base_url=AUTH_URL, client_id=CLIENT_ID
    )
    print(f"Getting device code from '{grant.device_code_url}'")

    device_code = grant.get_device_code()

    print(f"User code is '{device_code['user_code']}'")
    print(f"Go to '{device_code['verification_uri']}' to complete authentication.")

    webbrowser.open(device_code["verification_uri_complete"])

    token = grant.poll_for_token()

    timestamp = time.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(auth_path / f"token_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(token, f, indent=2)

    print("Successfully saved new token.")
    print("You are logged into your pennylane.ai account.")


def configure_logging(level=logging.INFO):
    logging.basicConfig(level=level)


def main():
    configure_logging()
    app()
