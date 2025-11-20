"""API client for Sol-Ark Cloud."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import aiohttp
import asyncio

_LOGGER = logging.getLogger(__name__)

# ---- Advanced file logging in solark directory ----
LOG_FILE = Path(__file__).parent / "solark_debug.log"

# Avoid adding multiple handlers on reloads
if not any(
    isinstance(h, logging.FileHandler) and getattr(h, "_solark_file_handler", False)
    for h in _LOGGER.handlers
):
    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler._solark_file_handler = True  # type: ignore[attr-defined]
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s"
        )
        file_handler.setFormatter(formatter)
        _LOGGER.addHandler(file_handler)
        # Ensure debug logs are emitted
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("SolArk file logger initialized at %s", LOG_FILE)
    except Exception as e:  # noqa: BLE001
        # Fallback to normal HA logging only
        _LOGGER.error("Failed to initialize SolArk file logger: %s", e)


class SolArkCloudAPIError(Exception):
    """Exception for Sol-Ark Cloud API errors."""


class SolArkCloudAPI:
    """Sol-Ark Cloud API client."""

    def __init__(
        self,
        username: str,
        password: str,
        plant_id: str,
        base_url: str,
        api_url: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self.username = username
        self.password = password
        self.plant_id = plant_id

        self.base_url = base_url.rstrip("/")
        self.api_url = api_url.rstrip("/")

        self._session = session

        self._token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

        _LOGGER.debug(
            "SolArkCloudAPI initialized for plant_id=%s, base_url=%s, api_url=%s",
            self.plant_id,
            self.base_url,
            self.api_url,
        )

    # ----------------- helpers -----------------

    def _get_headers(self, strict: bool = True) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if strict:
            headers.update(
                {
                    "Origin": self.base_url,
                    "Referer": f"{self.base_url}/",
                }
            )
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    async def _ensure_token(self) -> None:
        if self._token and self._token_expiry and datetime.utcnow() < self._token_expiry:
            return
        _LOGGER.debug("Token missing or expired, logging in again")
        await self.login()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        auth_required: bool = True,
    ) -> Dict[str, Any]:
        """Low-level request helper."""
        if auth_required:
            await self._ensure_token()

        url = f"{self.api_url}{endpoint}"
        headers = self._get_headers(strict=True)

        json_body = None
        params = None
        if method.upper() in ("GET", "DELETE"):
            params = data
        else:
            json_body = data

        _LOGGER.debug(
            "Requesting %s %s with params=%s json=%s",
            method,
            url,
            params,
            json_body,
        )

        try:
            async with self._session.request(
                method,
                url,
                headers=headers,
                json=json_body,
                params=params,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                text = await resp.text()
                _LOGGER.debug(
                    "Response %s %s -> HTTP %s, body: %s",
                    method,
                    url,
                    resp.status,
                    text[:1000],
                )
                try:
                    resp.raise_for_status()
                except aiohttp.ClientResponseError as e:
                    raise SolArkCloudAPIError(
                        f"HTTP {resp.status} for {endpoint}: {text[:500]}"
                    ) from e

                try:
                    result = await resp.json()
                except Exception as e:  # noqa: BLE001
                    raise SolArkCloudAPIError(
                        f"Invalid JSON response from {endpoint}: {text[:200]}"
                    ) from e

        except asyncio.TimeoutError as e:  # noqa: BLE001
            raise SolArkCloudAPIError(f"Timeout for {endpoint}") from e
        except aiohttp.ClientError as e:  # noqa: BLE001
            raise SolArkCloudAPIError(f"Client error for {endpoint}: {e}") from e

        if isinstance(result, dict):
            code = result.get("code")
            if code not in (0, "0", None):
                msg = result.get("msg", "Unknown error")
                raise SolArkCloudAPIError(
                    f"API error for {endpoint}: {msg} (code={code})"
                )

        return result

    # ----------------- auth -----------------

    async def _oauth_login(self) -> None:
        """Login using new OAuth2 /oauth/token endpoint."""
        url = f"{self.api_url}/oauth/token"
        headers = self._get_headers(strict=True)
        headers["Content-Type"] = "application/json;charset=UTF-8"

        payload = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
            "client_id": "csp-web",
        }

        _LOGGER.debug("Attempting OAuth login at %s", url)

        try:
            async with self._session.post(
                url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                text = await resp.text()
                _LOGGER.debug(
                    "OAuth login response HTTP %s, body: %s",
                    resp.status,
                    text[:1000],
                )
                try:
                    resp.raise_for_status()
                except aiohttp.ClientResponseError as e:
                    raise SolArkCloudAPIError(
                        f"OAuth login HTTP {resp.status}: {text[:500]}"
                    ) from e

                try:
                    result = await resp.json()
                except Exception as e:  # noqa: BLE001
                    raise SolArkCloudAPIError(
                        f"OAuth login invalid JSON: {text[:200]}"
                    ) from e

        except asyncio.TimeoutError as e:  # noqa: BLE001
            raise SolArkCloudAPIError("OAuth login timeout") from e
        except aiohttp.ClientError as e:  # noqa: BLE001
            raise SolArkCloudAPIError(f"OAuth login client error: {e}") from e

        if not isinstance(result, dict):
            raise SolArkCloudAPIError("OAuth login response not JSON object")

        code = result.get("code")
        if code not in (0, "0"):
            raise SolArkCloudAPIError(
                f"OAuth login failed: {result.get('msg', 'Unknown error')} (code={code})"
            )

        data = result.get("data") or {}
        token = data.get("access_token") or data.get("token")
        if not token:
            raise SolArkCloudAPIError("OAuth login succeeded but no access_token")

        self._token = token
        self._refresh_token = data.get("refresh_token")
        expires_in = int(data.get("expires_in", 3600))
        self._token_expiry = datetime.utcnow() + timedelta(seconds=expires_in - 60)

        _LOGGER.debug(
            "OAuth login successful, token expires in %s seconds (at %s)",
            expires_in,
            self._token_expiry,
        )

    async def _legacy_login(self) -> None:
        """Optional fallback to old API host."""
        url = "https://api.solarkcloud.com/rest/account/login"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {"username": self.username, "password": self.password}

        _LOGGER.debug("Attempting legacy login at %s", url)

        try:
            async with self._session.post(
                url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                text = await resp.text()
                _LOGGER.debug(
                    "Legacy login response HTTP %s, body: %s",
                    resp.status,
                    text[:1000],
                )
                try:
                    resp.raise_for_status()
                except aiohttp.ClientResponseError as e:
                    raise SolArkCloudAPIError(
                        f"Legacy login HTTP {resp.status}: {text[:500]}"
                    ) from e

                try:
                    result = await resp.json()
                except Exception as e:  # noqa: BLE001
                    raise SolArkCloudAPIError(
                        f"Legacy login invalid JSON: {text[:200]}"
                    ) from e

        except asyncio.TimeoutError as e:  # noqa: BLE001
            raise SolArkCloudAPIError("Legacy login timeout") from e
        except aiohttp.ClientError as e:  # noqa: BLE001
            raise SolArkCloudAPIError(f"Legacy login client error: {e}") from e

        if not isinstance(result, dict):
            raise SolArkCloudAPIError("Legacy login response not JSON object")

        token = (
            result.get("token")
            or result.get("access_token")
            or (result.get("data") or {}).get("token")
            or (result.get("data") or {}).get("access_token")
        )
        if not token:
            raise SolArkCloudAPIError("Legacy login succeeded but no token")

        self._token = token
        self._token_expiry = datetime.utcnow() + timedelta(minutes=30)

        _LOGGER.debug("Legacy login successful, temporary token set")

    async def login(self) -> bool:
        """Try OAuth login, then legacy login."""
        errors: list[str] = []

        try:
            await self._oauth_login()
            return True
        except SolArkCloudAPIError as e:
            _LOGGER.debug("OAuth login failed: %s", e)
            errors.append(f"oauth: {e}")

        try:
            await self._legacy_login()
            return True
        except SolArkCloudAPIError as e:
            _LOGGER.debug("Legacy login failed: %s", e)
            errors.append(f"legacy: {e}")

        raise SolArkCloudAPIError("All login methods failed: " + " | ".join(errors))

    # ----------------- plant data -----------------

    async def get_plant_data(self) -> Dict[str, Any]:
        """Fetch live plant data (via inverter SN)."""
        await self._ensure_token()
        _LOGGER.debug("Getting plant data for plant_id=%s", self.plant_id)

        # 1) Get inverters for the plant
        inv_params = {
            "page": 1,
            "limit": 10,
            "stationId": self.plant_id,
            "status": -1,
            "sn": "",
            "type": -2,
        }
        _LOGGER.debug("Requesting inverter list with params=%s", inv_params)
        inv_resp = await self._request(
            "GET",
            f"/api/v1/plant/{self.plant_id}/inverters",
            inv_params,
        )
        _LOGGER.debug("Raw inverter response: %s", inv_resp)

        inv_data = inv_resp.get("data") or {}
        inverters = (
            inv_data.get("infos")
            or inv_data.get("list")
            or inv_data.get("records")
            or []
        )
        _LOGGER.debug("Parsed inverters list length: %s", len(inverters))

        if not inverters:
            _LOGGER.warning("No inverters found for plant %s", self.plant_id)
            return inv_data

        first = inverters[0]
        _LOGGER.debug("First inverter entry: %s", first)
        sn = first.get("sn") or first.get("deviceSn")
        if not sn:
            _LOGGER.warning("First inverter for plant %s has no SN", self.plant_id)
            return inv_data

        # 2) Live data for that inverter
        _LOGGER.debug("Requesting live data for inverter SN=%s", sn)
        live_resp = await self._request(
            "GET",
            f"/api/v1/dy/store/{sn}/read",
            {"sn": sn},
        )
        _LOGGER.debug("Raw live response: %s", live_resp)

        live_data = live_resp.get("data") or live_resp
        if isinstance(live_data, dict):
            _LOGGER.debug(
                "Live data keys for SN=%s: %s", sn, list(live_data.keys())
            )
        else:
            _LOGGER.debug("Live data for SN=%s is not a dict: %r", sn, live_data)

        return live_data

    async def test_connection(self) -> bool:
        try:
            await self.login()
            await self.get_plant_data()
            return True
        except SolArkCloudAPIError as e:
            _LOGGER.error("SolArk test_connection failed: %s", e)
            return False

    def parse_plant_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Map API fields to sensor values."""
        if not isinstance(data, dict):
            _LOGGER.warning("parse_plant_data got non-dict: %r", data)
            return {}

        _LOGGER.debug("parse_plant_data received keys: %s", list(data.keys()))

        sensors: Dict[str, Any] = {}
        try:
            sensors["pv_power"] = float(data.get("pvPower", 0))
            sensors["load_power"] = float(data.get("loadPower", 0))
            sensors["grid_import_power"] = float(data.get("gridImportPower", 0))
            sensors["grid_export_power"] = float(data.get("gridExportPower", 0))
            sensors["battery_power"] = float(data.get("battPower", 0))
            sensors["battery_soc"] = float(data.get("battSoc", 0))
            sensors["energy_today"] = float(data.get("energyToday", 0))
            sensors["last_error"] = data.get("lastError", "None")
        except (TypeError, ValueError) as e:  # noqa: BLE001
            _LOGGER.warning("Error parsing plant data: %s", e)

        _LOGGER.debug("Parsed sensors dict: %s", sensors)
        return sensors
