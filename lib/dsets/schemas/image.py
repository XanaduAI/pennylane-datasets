from pathlib import PurePosixPath
from typing import Any, Self

from pydantic import (
    HttpUrl,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    model_validator,
)

from dsets.lib.json_ref import DocumentTreeModel
from dsets.lib.json_ref.context import DocumentContext, get_reference_validation_context


def _get_image_cache(ctx: DocumentContext) -> dict[PurePosixPath, "Image"]:
    if (cache := ctx.cache.get(Image)) is not None:
        return cache

    ctx.cache[Image] = {}
    return ctx.cache[Image]


class Image(DocumentTreeModel):
    url: HttpUrl | PurePosixPath

    @model_validator(mode="wrap")
    @classmethod
    def _validate_image(
        cls, data: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
    ) -> Self:
        data: Image = handler(data)

        if not isinstance(data.url, PurePosixPath):
            return data

        if (ctx := get_reference_validation_context(info)) is None:
            return data

        image_cache = _get_image_cache(ctx)
        if existing := image_cache.get(data.url):
            return existing

        return data
