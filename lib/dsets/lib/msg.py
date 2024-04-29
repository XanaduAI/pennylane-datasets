from typing import Any


def structured(msg: str, **kwargs: Any) -> str:
    """Returns a message with the following structure, for each key and
    value in **kwargs:
        '{msg}: {key}={repr(val)} ...'
    """
    kwds = ", ".join(f"{key}={repr(val)}" for key, val in kwargs.items())

    return f"{msg}: {kwds}"


def structured_print(msg: str, **kwargs: Any) -> None:
    """Prints the result of ``structured(msg, **kwargs)``."""
    print(structured(msg, **kwargs))
