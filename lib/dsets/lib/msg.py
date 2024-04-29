from typing import Any


def structured(msg: str, **kwargs: Any) -> str:
    kwds = ", ".join(f"{key}={repr(val)}" for key, val in kwargs.items())

    return f"{msg}: {kwds}"


def structured_print(msg: str, **kwargs: Any) -> None:
    print(structured(msg, **kwargs))
