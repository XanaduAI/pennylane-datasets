from datetime import datetime, timedelta, timezone

import pytest
from dsets.lib.time import urlsafe_isoformat


@pytest.mark.parametrize(
    "dt",
    [
        datetime(2024, 2, 1, 8, 12, 34, 567, tzinfo=timezone.utc),
        datetime(2024, 2, 1, 5, 12, 34, 789, tzinfo=timezone(timedelta(hours=-3))),
    ],
)
def test_urlsafe_isoformat(dt):
    """Test that `urlsafe_isoformat()` returns a timestamp in the expected
    format."""

    assert urlsafe_isoformat(dt) == "2024-02-01T081234Z"


def test_urlsafe_isoformat_fromisoformat():
    """Test that the string resulting from `urlsafe_isoformat()` is
    correctly parsed by `datetime.isoformat()`."""

    dt = datetime(2024, 2, 1, 8, 12, 34, tzinfo=timezone.utc)

    assert datetime.fromisoformat(urlsafe_isoformat(dt)) == dt


def test_urlsafe_isoformat_naive_exc():
    """Test that `urlsafe_isoformat()` raises a `ValueError` if `dt` is not
    timezone-aware."""
    with pytest.raises(ValueError, match="Datetime must be timezone-aware"):
        urlsafe_isoformat(datetime(2024, 2, 1, 8, 12, 34, tzinfo=None))
