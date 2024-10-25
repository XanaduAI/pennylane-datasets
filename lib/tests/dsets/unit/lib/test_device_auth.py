import time
from unittest.mock import MagicMock, patch

import dsets
import pytest
from dsets.lib.device_auth import OAuthDeviceCodeGrant

mock_device_code_data = {
    "device_code": "mock_device_code",
    "user_code": "mock_user_code",
    "verification_uri": "https://mock/verification/uri",
    "expires_in": 900,
    "interval": 5,
    "verification_uri_complete": "https://mock/verification/complete/uri",
}

mock_access_token = {
    "access_token": "mock_access_token",
    "expires_in": 86400,
    "token_type": "Bearer",
}


def post_mock(url, data, headers):
    """Returns a mock device code data."""
    resp = MagicMock(ok=True)
    resp.json.return_value = mock_device_code_data
    return resp


def token_request_mock(self, req):
    """Returns mocked access token and `None`."""
    return (mock_access_token, None)


def token_request_expired_token_mock(self, req):
    """Returns an expired token error."""
    return (None, {"error": "expired_token"})


def token_request_unexpected_error_mock(self, req):
    """Returns an unexpected error."""
    return (None, {"error": "An unexpected error ocurred."})


class TestOAuthDeviceCodeGrant:
    """Tests for ``OAuthDeviceCodeGrant`` class."""

    grant = OAuthDeviceCodeGrant(oauth_base_url="test/url", client_id="test_id")

    @patch.object(dsets.lib.device_auth, "post", post_mock)
    def test_get_device_code(self):
        """Tests that the ``get_device_code()`` method responds with the expected data."""
        device_code = self.grant.get_device_code()
        for k, v in mock_device_code_data.items():
            assert device_code[k] == v

        assert "expires_at" in list(device_code.keys())

    def test_existing_device_code(self):
        """Tests that that the ``get_device_code()`` method returns the existing device
        code data if it already exists."""
        expire_time = time.time() + (24 * 60 * 60)
        device_code_data = {
            "device_code": "mock_device_code",
            "expires_at": expire_time,
        }

        grant = OAuthDeviceCodeGrant(oauth_base_url="test/url", client_id="test_id")
        grant._device_code_data = device_code_data

        assert grant.get_device_code() == device_code_data

    @patch.object(dsets.lib.device_auth, "post", post_mock)
    @patch.object(
        dsets.lib.device_auth.OAuthDeviceCodeGrant,
        "_do_token_request",
        token_request_mock,
    )
    def test_poll_for_token_success(self):
        """Tests that the ``poll_for_token`` method returns the expected data."""
        token_data = self.grant.poll_for_token()
        for k, v in mock_access_token.items():
            assert token_data[k] == v
        assert "expires_at" in list(token_data.keys())

    @patch.object(dsets.lib.device_auth, "post", post_mock)
    @patch.object(
        dsets.lib.device_auth.OAuthDeviceCodeGrant,
        "_do_token_request",
        token_request_expired_token_mock,
    )
    def test_poll_for_token_expired_token_error(self):
        """Tests that the ``poll_for_token`` method raises the expected error for expired tokens."""
        msg = "Authorization timed out"
        with pytest.raises(TimeoutError, match=msg):
            self.grant.poll_for_token()

    @patch.object(dsets.lib.device_auth, "post", post_mock)
    @patch.object(
        dsets.lib.device_auth.OAuthDeviceCodeGrant,
        "_do_token_request",
        token_request_unexpected_error_mock,
    )
    def test_poll_for_token_unexpected_error(self):
        """Tests that the ``poll_for_token`` method raises the expected error for"""
        msg = 'Authorization endpoint test/url/token returned error: {"error": "An unexpected error ocurred."}'
        with pytest.raises(RuntimeError, match=msg):
            self.grant.poll_for_token()
