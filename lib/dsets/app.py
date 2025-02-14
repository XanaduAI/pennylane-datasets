import hashlib
import json
import logging
import shutil
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Annotated

import inflection
import rich
import typer
from pennylane.data import Dataset

from dsets import schemas
from dsets.lib import (
    auth,
    bibtex,
    deploy,
    device_auth,
    doctree,
    graphql,
    json_fmt,
    markdown,
    msg,
    progress,
)
from dsets.schemas import Author, fields
from dsets.settings import CLIContext, Settings

from .builder import AssetLoader, compile_dataset_build

app = typer.Typer(name="dsets", add_completion=True)


def _get_gql_client(ctx: CLIContext) -> graphql.Client:
    """Get a GraphQL client for the datasets API, with the user's
    authentication token."""
    if not (token := auth.get_valid_token(ctx.auth_path)):
        rich.print(
            "You must be logged in to your pennylane.ai account to perform this action.\n"
            "Login in with: [bold]dsets login[/bold]."
        )
        raise typer.Exit(1)

    return graphql.client(ctx.settings.graphql_url, token)


def _prompt_for_image(prompt: str, dest_dir: Path) -> Path | None:
    """Prompt the user for an image. And attempt to move it to directory
    `dest`."""

    src = typer.prompt(prompt).strip()
    if not src:
        return None

    src = Path(src)
    if not src.exists():
        print(f"Image file does not exist: {src}")
        return _prompt_for_image(prompt, dest_dir)

    shutil.copy(src, dest_dir / src.name)

    return dest_dir / src.name


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
) -> None:
    """Upload a new dataset file."""
    ctx = CLIContext()
    src_file = src_file.expanduser()
    name = src_file.name

    gql_client = _get_gql_client(ctx)

    size = src_file.stat().st_size
    with open(src_file, "rb") as f:
        digest = hashlib.file_digest(f, "sha256").digest()

    error = None
    with open(src_file, "rb") as f, progress.IOProgressBarManager() as pbar:
        cb = pbar.add_bar(size, f"Upload {src_file}")
        try:
            graphql.files.upload_file(gql_client, f, name, size, digest, callback=cb)
        except graphql.files.APIError as exc:
            error = exc.args[0]

    if error:
        print(f"Error: {error}")
        raise typer.Exit(1)


@app.command(name="list-files")
def list_files():
    """List datasets files owned by the calling user."""
    ctx = CLIContext()
    gql_client = _get_gql_client(ctx)

    files = graphql.files.get_files(gql_client)
    print(json.dumps(files, indent=2))


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
def add(dataset_file: Path):
    """
    Add a new dataset to an existing family, or create a new one.
    """
    ctx = CLIContext()

    content_doctree = doctree.Doctree(ctx.content_dir)

    rich.print(
        "A dataset's [bold]class[/bold] defines its [bold]attributes[/bold] and parameters."
    )
    class_slug = typer.prompt(
        "Choose an existing class [qchem, qspin], or enter a new class name"
    )

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
            f"Define parameters for class {repr(class_slug)} (Y/n)?", default=True
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

    today = datetime.now().date()

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

        authors = []
        while True:
            name = typer.prompt("Enter author name", default="").strip()
            if not name:
                if not authors:
                    continue
                else:
                    break

            username = typer.prompt(
                "Enter author PennyLane profile handle", default=""
            ).strip()
            authors.append(Author(name=name, username=username if username else None))

        family_doc.parent.mkdir(parents=True, exist_ok=True)
        hero_image = _prompt_for_image(
            "Enter path to banner image (leave blank to continue)", family_doc.parent
        )
        thumbnail_image = _prompt_for_image(
            "Enter path to thumbnail image (leave blank to conintue)", family_doc.parent
        )

        meta = schemas.DatasetFamilyMeta(
            title=family_title,
            description=description,
            citation=doctree.Reference[fields.BibtexStr](path="citation.txt"),
            using_this_dataset=doctree.Reference[str](path="using_this_dataset.md"),
            license="[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en)",
            authors=authors,
            date_of_last_modification=today,
            date_of_publication=today,
            hero_image=hero_image.name if hero_image else None,
            thumbnail=thumbnail_image.name if thumbnail_image else None,
        )

        with open(family_doc.parent / "meta.json", "w", encoding="utf-8") as f:
            f.write(meta.model_dump_json(indent=2, by_alias=True))

        with open(family_doc.parent / "citation.txt", "w", encoding="utf-8") as f:
            f.write(
                bibtex.generate_bibtex(
                    family_slug,
                    family_title,
                    authors=[author.name for author in authors],
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
def deploy_build():
    """Deploy datasets-build.json to the datasets service."""
    ctx = CLIContext()
    short_sha = ctx.commit_sha(short=True)
    build_path = ctx.build_dir / "datasets-build.json"

    if (admin_url := ctx.settings.datasets_admin_api_url) is not None:
        deploy.deploy_datasets_build(admin_url, build_path, commit_sha=short_sha)
        msg.structured_print(
            "Deployed build to new datasets service",
            commmit_sha=short_sha,
            url=admin_url,
        )
    else:
        msg.structured_print(
            "Environment variable 'DATASETS_ADMIN_API_URL' is unset, cannot deploy."
        )
        typer.Exit(1)


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
    """Login to PennyLane account."""
    ctx = CLIContext()
    auth_path = ctx.auth_path

    print("Checking credentials...")
    if auth.get_valid_token(auth_path):
        print("Found a valid token.")
        rich.print(
            "[bold green]You are logged into your PennyLane account.[/bold green]"
        )
        return

    settings = Settings()
    grant = device_auth.OAuthDeviceCodeGrant(
        oauth_base_url=settings.auth_url,
        client_id=settings.client_id,
        audience=settings.audience_url,
    )

    device_code = grant.get_device_code()

    rich.print(f"User code is [bold]{device_code['user_code']}[/bold]")
    rich.print(
        f"Go to [bold]{device_code['verification_uri_complete']}[/bold] to complete authentication."
    )

    webbrowser.open(device_code["verification_uri_complete"])

    token = grant.poll_for_token()

    with open(f"{ctx.repo_root}/.auth.json", "w", encoding="utf-8") as f:
        json.dump(token, f, indent=2)

    rich.print("[bold green]You are logged into your PennyLane account[/bold green].")


def configure_logging(level=logging.INFO):
    logging.basicConfig(level=level)


def main():
    configure_logging()
    app()
