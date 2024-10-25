from pathlib import Path
from unittest.mock import MagicMock, patch

import dsets
from dsets.lib.auth import has_valid_token


# pylint:disable=unused-argument
def post_mock(url, json, timeout, headers):
    """Returns a response with 200 status code."""
    resp = MagicMock(ok=True)
    resp.status_code = 200
    return resp


class TestHasValidToken:
    """Tests for the ``has_valid_token()`` function."""

    @patch.object(dsets.lib.auth, "post", post_mock)
    def test_valid_token(self):
        """Tests that if a valid token is found, the function returns `True`."""
        path = Path.cwd() / "lib" / "tests" / "support" / "mock_token.json"
        assert has_valid_token(path)

    def test_no_token(self):
        """Tests that the function returns `False` if no token is found."""
        assert not has_valid_token(Path("not_a_token.txt"))
