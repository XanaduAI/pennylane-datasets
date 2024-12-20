from pathlib import Path
from typing import Union

from pydantic import AnyHttpUrl, TypeAdapter, ValidationError

_TA = TypeAdapter[Path | AnyHttpUrl](Union[Path, AnyHttpUrl])


def parse_path_or_url(val: str) -> Path | AnyHttpUrl:
    try:
        return _TA.validate_python(val)
    except ValidationError as exc:
        raise ValueError("Not a valid filesystem path or HTTP URL") from exc
