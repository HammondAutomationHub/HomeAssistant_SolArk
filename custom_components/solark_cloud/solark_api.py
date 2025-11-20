"""Sol-Ark Cloud API Client with comprehensive error handling."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)

LOGIN_ENDPOINT = "/rest/account/login"
PLANT_DATA_ENDPOINT = "/rest/plant/getPlantData"
DEFAULT_TIMEOUT = 30
LOGIN_TIMEOUT = 15


class SolArkAPIError(Exception):
    """Base exception for Sol-Ark API errors."""


class SolArkAuthError(SolArkAPIError):
    """Exception for authentication errors."""


class SolArkConnectionError(SolArkAPIError):
    """Exception for connection errors."""


class SolArkRateLimitError(SolArkAPIError):
    """Exception for rate limit errors."""


class SolArkAPI:
    """API client for Sol-Ark Cloud."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        email: str,
        password: str,
        base_url: str = "https://api.solarkcloud.com",
        auth_mode: str = "Auto",
    ) -> None:
        """Initialize the API client."""
        self.session = session
        self.email = email
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.auth_mode = auth_mode
        self.token: str | None = None
        self._auth_lock = asyncio.Lock()

    async def authenticate(self) -> bool:
        """Authenticate with Sol-Ark Cloud API."""
        async with self._auth_lock:
            if self.auth_mode == "Auto":
                for mode in ["Strict", "Legacy"]:
                    try:
                        _LOGGER.debug("Attempting authentication with mode: %s", mode)
                        if await self._authenticate_with_mode(mode):
                            _LOGGER.info("Successfully authenticated with mode: %s", mode)
                            return True
                    except SolArkAuthError as err:
                        _LOGGER.debug(
                            "Authentication failed with mode %s: %s", mode, err
                        )
                        continue
                    except SolArkConnectionError:
                        raise
                
                raise SolArkAuthError(
                    "Authentication failed with all modes. Please verify your credentials."
                )
            else:
                return await self._authenticate_with_mode(self.auth_mode)

    async def _authenticate_with_mode(self, mode: str) -> bool:
        """Authenticate using a specific mode."""
        url = f"{self.base_url}{LOGIN_ENDPOINT}"
        
        if mode == "Strict":
            payload = {
                "email": self.email,
                "password": self.password,
                "grant_type": "password",
            }
        else:
            payload = {
                "username": self.email,
                "pwd": self.password,
            }

        try:
            async with async_timeout.timeout(LOGIN_TIMEOUT):
                async with self.session.post(url, json=payload) as response:
                    response_text = await response.text()
                    
                    _LOGGER.debug(
                        "Auth response status: %s, body: %s",
                        response.status,
                        response_text[:200] if response_text else "empty"
                    )

                    if response.status == 401:
                        raise SolArkAuthError(
                            f"Invalid credentials (401). Please verify your email and password."
                        )
                    elif response.status == 403:
                        raise SolArkAuthError(
                            f"Access forbidden (403). Your account may be locked or disabled."
                        )
                    elif response.status == 429:
                        raise SolArkRateLimitError(
                            "Rate limit exceeded (429). Please wait before trying again."
                        )
                    elif response.status >= 500:
                        raise SolArkConnectionError(
                            f"Sol-Ark server error ({response.status}). Please try again later."
                        )
                    elif response.status != 200:
                        raise SolArkAPIError(
                            f"Unexpected response status {response.status}: {response_text[:200]}"
                        )

                    try:
                        data = await response.json()
                    except aiohttp.ContentTypeError as err:
                        raise SolArkAPIError(
                            f"Invalid JSON response from server: {response_text[:200]}"
                        ) from err

                    if not isinstance(data, dict):
                        raise SolArkAPIError(
                            f"Invalid response format: expected dict, got {type(data)}"
                        )

                    if "data" in data and isinstance(data["data"], dict):
                        if "token" in data["data"]:
                            self.token = data["data"]["token"]
                            return True
                        elif "access_token" in data["data"]:
                            self.token = data["data"]["access_token"]
                            return True
                    
                    if "token" in data:
                        self.token = data["token"]
                        return True
                    elif "access_token" in data:
                        self.token = data["access_token"]
                        return True
                    
                    if data.get("success") is False or data.get("Success") is False:
                        error_msg = (
                            data.get("message")
                            or data.get("Message")
                            or data.get("msg")
                            or "Authentication failed"
                        )
                        raise SolArkAuthError(f"Authentication failed: {error_msg}")

                    raise SolArkAPIError(
                        f"Authentication response missing token: {data}"
                    )

        except asyncio.TimeoutError as err:
            raise SolArkConnectionError(
                f"Connection timeout after {LOGIN_TIMEOUT}s. Please check your internet connection."
            ) from err
        except aiohttp.ClientConnectorError as err:
            raise SolArkConnectionError(
                f"Cannot connect to {self.base_url}. Please verify the URL and your network connection: {err}"
            ) from err
        except aiohttp.ClientError as err:
            raise SolArkConnectionError(
                f"Network error during authentication: {err}"
            ) from err

    async def get_plant_data(self, plant_id: str) -> dict[str, Any] | None:
        """Get plant data from Sol-Ark Cloud."""
        if not self.token:
            raise SolArkAuthError("Not authenticated. Please call authenticate() first.")

        url = f"{self.base_url}{PLANT_DATA_ENDPOINT}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {"plantId": plant_id}

        _LOGGER.debug("Fetching plant data for Plant ID: %s from %s", plant_id, url)

        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                async with self.session.post(
                    url, json=payload, headers=headers
                ) as response:
                    response_text = await response.text()
                    
                    _LOGGER.debug(
                        "Plant data response status: %s, content-type: %s",
                        response.status,
                        response.headers.get('content-type', 'unknown')
                    )
                    _LOGGER.debug("Response body (first 500 chars): %s", response_text[:500])

                    if response.status == 400:
                        raise SolArkAPIError(
                            f"Bad request (400). The Plant ID format may be invalid."
                        )
                    elif response.status == 401:
                        # Token may have expired
                        self.token = None
                        raise SolArkAuthError(
                            "Authentication token expired or invalid. Please re-authenticate."
                        )
                    elif response.status == 403:
                        raise SolArkAPIError(
                            f"Access forbidden (403). You may not have permission to view Plant ID {plant_id}."
                        )
                    elif response.status == 404:
                        raise SolArkAPIError(
                            f"Plant ID {plant_id} not found (404). Please verify your Plant ID is correct."
                        )
                    elif response.status == 429:
                        raise SolArkRateLimitError(
                            "Rate limit exceeded (429). Consider increasing the update interval."
                        )
                    elif response.status >= 500:
                        raise SolArkConnectionError(
                            f"Sol-Ark server error ({response.status}). Please try again later."
                        )
                    elif response.status != 200:
                        _LOGGER.warning("Unexpected status %s: %s", response.status, response_text[:200])
                        raise SolArkAPIError(
                            f"Unexpected response status {response.status}"
                        )

                    try:
                        data = await response.json()
                    except aiohttp.ContentTypeError as err:
                        _LOGGER.error("Invalid JSON response: %s", response_text[:500])
                        raise SolArkAPIError(
                            f"Invalid JSON response. The API may have changed."
                        ) from err

                    if not isinstance(data, dict):
                        _LOGGER.error("Response is not a dict: %s", type(data))
                        raise SolArkAPIError(
                            f"Invalid response format: expected dict, got {type(data)}"
                        )

                    _LOGGER.debug("Response data keys: %s", list(data.keys()))

                    # Check for error in response
                    success_flag = data.get("success", data.get("Success"))
                    if success_flag is False:
                        error_msg = (
                            data.get("message")
                            or data.get("Message")
                            or data.get("msg")
                            or data.get("error")
                            or "Unknown error"
                        )
                        _LOGGER.error("API returned success=false: %s", error_msg)
                        
                        # Check if error message indicates auth issue
                        if "token" in error_msg.lower() or "auth" in error_msg.lower():
                            self.token = None
                            raise SolArkAuthError(f"Authentication error: {error_msg}")
                        
                        raise SolArkAPIError(f"API error: {error_msg}")

                    # Extract plant data from various response formats
                    plant_data = None
                    if "data" in data:
                        plant_data = data["data"]
                    elif "Data" in data:
                        plant_data = data["Data"]
                    elif "result" in data:
                        plant_data = data["result"]
                    else:
                        # Maybe the whole response is the plant data
                        plant_data = data

                    if not plant_data:
                        _LOGGER.error("No plant data in response: %s", data)
                        raise SolArkAPIError(
                            f"No plant data returned for Plant ID {plant_id}. Response keys: {list(data.keys())}"
                        )

                    _LOGGER.debug("Plant data retrieved successfully, data keys: %s", list(plant_data.keys()) if isinstance(plant_data, dict) else "not a dict")
                    return plant_data

        except asyncio.TimeoutError as err:
            _LOGGER.error("Plant data request timeout after %s seconds", DEFAULT_TIMEOUT)
            raise SolArkConnectionError(
                f"Request timeout after {DEFAULT_TIMEOUT}s."
            ) from err
        except aiohttp.ClientConnectorError as err:
            _LOGGER.error("Cannot connect to %s: %s", self.base_url, err)
            raise SolArkConnectionError(
                f"Cannot connect to {self.base_url}: {err}"
            ) from err
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error while fetching plant data: %s", err)
            raise SolArkConnectionError(
                f"Network error while fetching plant data: {err}"
            ) from err

    async def close(self) -> None:
        """Close the API client."""
        self.token = None
