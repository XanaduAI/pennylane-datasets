from pathlib import Path
from typing import Annotated

import typer

from dsets.lib import progress, s3, time
from dsets.lib.context import Context
from dsets.schemas.dataset import Dataset, DatasetType, DocumentRef

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
    prefix: Annotated[str, typer.Argument(help="Prefix for data bucket")],
) -> None:
    """Upload a new dataset file to the data bucket, and create an upload
    receipt in pennylane-datasets/data.
    """
    ctx = Context()
    src_file = src_file.expanduser()
    prefix = s3.S3Path(prefix)

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


TYPE_DEFAULTS = {
    "qchem": {
        "type_": DocumentRef[DatasetType](path="/_meta/qchem.json"),
        "tags": ["qchem"],
        "parameter_labels": ["molname", "basis", "bondlength"],
        "variable_names": ["hamiltonianEquation"],
    },
    "qspin": {
        "type_": DocumentRef[DatasetType](path="/_meta/qspin.json"),
        "tags": ["qspin"],
        "parameter_labels": ["sysname", "layout", "periodicty", "lattice"],
    },
}


@app.command(name="add")
def add_dataset(
    type_: Annotated[str, typer.Option("--type", prompt=True)],
    name: Annotated[str, typer.Option(prompt=True)],
    title: Annotated[str, typer.Option(prompt=True)],
    parameter_labels: Annotated[list[str], typer.Option(default_factory=list)],
    tags: Annotated[list[str], typer.Option(default_factory=list)],
):
    ctx = Context()
    dataset_dir = Path(ctx.datasets_dir) / type_ / name

    if (dataset_json_path := dataset_dir / "dataset.json").exists():
        raise RuntimeError(f"Dataset already exists at {dataset_json_path}")

    type_defaults = TYPE_DEFAULTS.get(type_, {})

    if not parameter_labels:
        parameter_labels = typer.prompt(
            "Enter parameter labels",
            default=", ".join(type_defaults.get("parameter_labels", [])),
            value_proc=lambda s: [t.strip() for t in s.split(",")],
            show_default=True,
        )

    if not tags:
        tags = typer.prompt(
            "Enter tags",
            default=", ".join(type_defaults.get("tags", [])),
            value_proc=lambda s: [t.strip() for t in s.split(",")],
            show_default=True,
        )

    timestamp = time.utcnow()
    dataset = Dataset(
        title=title,
        slug=f"{type_}-{name}",
        authors=[],
        tags=tags,
        citation=DocumentRef[str](path="citatation.txt"),
        about=DocumentRef[str](path="about.md"),
        type_=type_defaults.get("type_", DatasetType(name=name, attribute_list=[])),
        date_of_publication=timestamp,
        date_of_last_modification=timestamp,
        parameter_labels=parameter_labels,
        variable_names=type_defaults.get("variable_names", []),
        data=[],
    )

    dataset_dir.mkdir(parents=True, exist_ok=True)

    with open(dataset_dir / "about.md", "w", encoding="utf-8") as about:
        about.write("# Using This Dataset")

    with open(dataset_dir / "citation.txt", "w", encoding="utf-8") as citation:
        citation.write("{Enter Citation}")

    with open(dataset_dir / "dataset.json", "w", encoding="utf-8") as f:
        f.write(dataset.model_dump_json(indent=2, exclude_unset=True, by_alias=True))
