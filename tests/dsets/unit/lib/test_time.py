from datetime import datetime, timedelta, timezone

import pytest
from dsets.lib.time import compact_isoformat


@pytest.mark.parametrize(
    "dt",
    [
        datetime(2024, 2, 1, 8, 12, 34, 567, tzinfo=timezone.utc),
        datetime(2024, 2, 1, 5, 12, 34, 789, tzinfo=timezone(timedelta(hours=-3))),
    ],
)
def test_compact_isoformat(dt):
    """Test that `compact_isoformat()` returns a timestamp in the expected
    format."""

    assert compact_isoformat(dt) == "2024-02-01T081234Z"


def test_compact_isoformat_fromisoformat():
    """Test that the string resulting from `compact_isoformat()` is
    correctly parsed by `datetime.isoformat()`."""

    dt = datetime(2024, 2, 1, 8, 12, 34, tzinfo=timezone.utc)

    assert datetime.fromisoformat(compact_isoformat(dt)) == dt
