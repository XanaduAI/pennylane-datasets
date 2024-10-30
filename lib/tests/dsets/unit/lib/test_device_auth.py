import time
from unittest.mock import patch

import dsets
import pytest
import responses
from dsets.lib.device_auth import OAuthDeviceCodeGrant, OAuthTokenError

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


@pytest.fixture
def add_response():
    """Returns a function that places a JSON serialization of its argument
    inside the body of an HTTP response to a POST request to the given URL."""

    def add_response_(body, url):
        return responses.add(responses.POST, url, json=body)

    return add_response_


def raise_expired_token_mock(self, req):
    """Raise an expired token error."""
    error = OAuthTokenError()
    error.args = ({"error": "expired_token"},)
    raise error


def raise_unexpected_error_mock(self, req):
    """Raise an unexpected error."""
    error = OAuthTokenError()
    error.args = ({"error": "An unexpected error ocurred."},)
    raise error


class TestOAuthDeviceCodeGrant:
    """Tests for ``OAuthDeviceCodeGrant`` class."""

    grant = OAuthDeviceCodeGrant(
        oauth_base_url="https://test/url", client_id="https://test_id"
    )

    @responses.activate
    def test_get_device_code(self, add_response):
        """Tests that the ``get_device_code()`` method responds with the expected data."""
        add_response(mock_device_code_data, "https://test/url/device/code")
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

        grant = OAuthDeviceCodeGrant(
            oauth_base_url="https://test/url", client_id="test_id"
        )
        grant._device_code_data = device_code_data

        assert grant.get_device_code() == device_code_data

    @responses.activate
    def test_poll_for_token_success(self, add_response):
        """Tests that the ``poll_for_token`` method returns the expected data."""
        add_response(mock_device_code_data, "https://test/url/device/code")
        add_response(mock_access_token, "https://test/url/token")

        token_data = self.grant.poll_for_token()
        for k, v in mock_access_token.items():
            assert token_data[k] == v

        assert "expires_at" in list(token_data.keys())

    @responses.activate
    @patch.object(
        dsets.lib.device_auth.OAuthDeviceCodeGrant,
        "_do_token_request",
        raise_expired_token_mock,
    )
    def test_poll_for_token_expired_token_error(self, add_response):
        """Tests that the ``poll_for_token`` method raises the expected error for expired tokens."""
        add_response(mock_device_code_data, "https://test/url/device/code")

        msg = "Authorization timed out"
        with pytest.raises(TimeoutError, match=msg):
            self.grant.poll_for_token()

    @responses.activate
    @patch.object(
        dsets.lib.device_auth.OAuthDeviceCodeGrant,
        "_do_token_request",
        raise_unexpected_error_mock,
    )
    def test_poll_for_token_unexpected_error(self, add_response):
        """Tests that the ``poll_for_token`` method raises the expected error for"""
        add_response(mock_device_code_data, "https://test/url/device/code")

        msg = r"Authorization endpoint https://test/url/token returned error: {'error': 'An unexpected error ocurred.'}"
        with pytest.raises(RuntimeError, match=msg):
            self.grant.poll_for_token()
