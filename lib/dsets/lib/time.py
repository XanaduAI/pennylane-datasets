from datetime import datetime, timezone


def utcnow() -> datetime:
    """Returns timezone-aware datetime of the current
    UTC time."""
    return datetime.now(timezone.utc)


def compact_isoformat(dt: datetime) -> str:
    """Return ``dt`` as an ISO-formatted UTC timestamp
    string in the compact form without '-' or ':'
    characters:

    'YYYY-MM-DDTHHMMSSZ'

    Args:
        dt: datetime, must be timezone-aware.

    Returns:
        ISO-formatted string
    """

    if dt.utcoffset() is None:
        raise ValueError("Datetime must be timezone-aware")

    dt = dt.astimezone(timezone.utc)

    return dt.strftime("%Y-%m-%dT%H%M%SZ")
