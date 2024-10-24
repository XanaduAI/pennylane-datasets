import http.client
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterable, Mapping
from typing import TypedDict


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


class OAuthTokenError(TypedDict):
    error: str
    description: str


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
        """Gets device code data from ``device_code_url()``"""
        if (data := self._device_code_data) is not None:
            if data["expires_at"] <= time.time():
                self._device_code_data = None

                return self.get_device_code()

            return data

        ts = time.time()
        resp: http.client.HTTPResponse = urllib.request.urlopen(
            urllib.request.Request(
                self.device_code_url,
                data=urllib.parse.urlencode({"client_id": self.client_id}).encode(
                    "ascii"
                ),
                headers=self.headers,
            )
        )

        device_code_data: DeviceCodeData = json.loads(resp.read())
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
            data["scopes"] = " ".join(self.scopes)

        req = urllib.request.Request(
            url=self.token_url,
            headers=self.headers,
            data=urllib.parse.urlencode(data).encode("ascii"),
        )

        while True:
            ts = time.time()
            token_data, error = self._do_token_request(req)
            if error is not None:
                if error["error"] == "slow_down":
                    polling_interval += 1
                elif error["error"] == "expired_token":
                    raise TimeoutError("Authorization timed out")
                elif error["error"] != "authorization_pending":
                    raise RuntimeError(
                        f"Authorization endpoint {self.token_url} returned error: {json.dumps(error)}"
                    )

                time.sleep(polling_interval)

            elif token_data is not None:
                token_data["expires_at"] = ts + token_data["expires_in"]
                self._token_data = token_data
                return token_data

    def _do_token_request(
        self, req: urllib.request.Request
    ) -> tuple[TokenData, None] | tuple[None, OAuthTokenError]:
        """Internal function to make requests to retrieve token data."""
        try:
            resp: http.client.HTTPResponse = urllib.request.urlopen(req)
        except urllib.error.HTTPError as exc:
            try:
                error_body: OAuthTokenError = json.loads(exc.read())
                return (None, error_body)
            except json.JSONDecodeError:
                raise exc

        token_data: TokenData = json.loads(resp.read())
        return (token_data, None)
