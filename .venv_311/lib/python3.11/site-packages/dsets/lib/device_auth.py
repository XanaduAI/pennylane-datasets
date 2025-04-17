import json
import time
from collections.abc import Iterable, Mapping
from typing import TypedDict

from requests import Response, post
from requests.exceptions import HTTPError


class DeviceCodeData(TypedDict):
    device_code: str
    expires_at: float
    expires_in: int
    interval: int
    user_code: str
    verification_uri: str
    verification_uri_complete: str


class TokenData(TypedDict):
    access_token: str
    expires_at: float
    expires_in: int
    token_type: str


class OAuthTokenError(Exception):
    pass


class OAuthDeviceCodeGrant:
    """
    Manages the device authorization flow for pennylane.ai accounts.
    """

    def __init__(
        self,
        oauth_base_url: str,
        client_id: str,
        *,
        audience: str | None = None,
        headers: Mapping[str, str] | None = None,
        scopes: Iterable[str] | None = None,
    ) -> None:
        self.oauth_base_url = oauth_base_url.rstrip("/")
        self.client_id = client_id

        self.audience = audience
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if headers:
            self.headers.update(headers)

        self.scopes = set(scopes) if scopes else None

        self._device_code_data: DeviceCodeData | None = None
        self._token_data: TokenData | None = None

    @property
    def device_code_url(self) -> str:
        """Returns the Auth0 authorization server endpoint"""
        return f"{self.oauth_base_url}/device/code"

    @property
    def token_url(self) -> str:
        """Returns the Auth0 authorization token endpoint"""
        return f"{self.oauth_base_url}/token"

    def get_device_code(self) -> DeviceCodeData:
        """Gets device code data from ``device_code_url()`` if no device code data has
        been cached."""
        if (data := self._device_code_data) and data["expires_at"] > time.time():
            return data

        ts = time.time()
        resp: Response = post(
            self.device_code_url,
            data={
                "client_id": self.client_id,
                "audience": self.audience,
            },
            headers=self.headers,
        )

        device_code_data: DeviceCodeData = resp.json()
        device_code_data["expires_at"] = ts + device_code_data["expires_in"]

        self._device_code_data = device_code_data

        return device_code_data

    def poll_for_token(self) -> TokenData:
        """Uses device code data to periodically attempt to retrieve token data from the
        Auth0 authorization token endpoint.
        """
        device_code_data = self.get_device_code()
        polling_interval = device_code_data["interval"]

        data = {
            "client_id": self.client_id,
            "device_code": device_code_data["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }

        if self.audience is not None:
            data["audience"] = self.audience

        if self.scopes is not None:
            data["scope"] = " ".join(self.scopes)

        req = {
            "url": self.token_url,
            "headers": self.headers,
            "data": data,
        }

        while True:
            ts = time.time()
            try:
                token_data = self._do_token_request(req)
                token_data["expires_at"] = ts + token_data["expires_in"]
                self._token_data = token_data
                return token_data
            except OAuthTokenError as error:
                error_type = error.args[0]["error"]
                if error_type == "slow_down":
                    polling_interval += 1
                elif error_type == "expired_token":
                    raise TimeoutError("Authorization timed out")
                elif error_type != "authorization_pending":
                    raise RuntimeError(
                        f"Authorization endpoint {self.token_url} returned error: {error}"
                    )

                time.sleep(polling_interval)

    def _do_token_request(self, req: dict) -> TokenData:
        """Internal function to make requests to retrieve token data."""

        try:
            resp: Response = post(
                url=req["url"], data=req["data"], headers=req["headers"]
            )
            resp.raise_for_status()
        except HTTPError as exc:
            try:
                error_body = OAuthTokenError(resp.json())
                raise error_body
            except json.JSONDecodeError:
                raise exc

        token_data: TokenData = resp.json()
        return token_data
