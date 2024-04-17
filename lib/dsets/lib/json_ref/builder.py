import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

from .asset import Asset
from .doctree import Doctree

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


class AssetUploader:
    def __init__(
        self,
        destination_url_prefix: str,
        s3_client: "S3Client",
        bucket: str,
        prefix: str,
    ):
        self.destination_url_prefix = destination_url_prefix.strip("/")
        self.s3_client = s3_client
        self.bucket = bucket
        self.prefix = prefix

        self.resolved_asset_urls: dict[Path, str] = {}
        self.resolved_asset_names: dict[Path, str] = {}

    def add_asset(self, asset: Asset) -> str:
        if not asset.is_local:
            return str(asset.root)

        os_path = asset.os_path
        if resolved := self.resolved_asset_urls.get(os_path):
            return resolved

        with open(os_path, "rb") as f:
            digest = hashlib.file_digest(f, "sha1").hexdigest()

        name = f"{os_path.stem}-{digest}{os_path.suffix}"
        url = f"{self.destination_url_prefix}/{name}"

        self.resolved_asset_names[os_path] = name
        self.resolved_asset_urls[os_path] = url

        return url

    def upload(self):
        for path, name in self.resolved_asset_names.items():
            key = f"{self.prefix}/{name}"
            if _s3_object_exists(self.s3_client, self.bucket, key):
                continue

            self.s3_client.upload_file(Filename=str(path), Bucket=self.bucket, Key=key)
            print(f"Uploaded asset: path={path}, key={key}")


def compile_doctree(doctree: Doctree, asset_uploader: AssetUploader) -> dict:
    documents = {}

    for asset in doctree.get_objects(Asset):
        new_url = asset_uploader.add_asset(asset)
        asset.root = new_url

    asset_uploader.upload()

    for document_type, document_list in doctree.get_documents().items():
        documents[document_type.__name__] = [
            document.model_dump(mode="json") for document in document_list
        ]

    return documents


def _s3_object_exists(s3_client: "S3Client", bucket: str, key: str) -> bool:
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
    except s3_client.exceptions.NoSuchKey:
        return False
    except s3_client.exceptions.ClientError as exc:
        if exc.response["Error"]["Code"] == "404":
            return False
        raise exc

    return True
