"""API client for Sol-Ark Cloud (SolArk 12K + HTML SOC)."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
import logging
from pathlib import Path
from typing import Any, Dict, Optional
import re

import aiohttp

_LOGGER = logging.getLogger(__name__)

# Log to custom_components/solark/solark_debug.log
LOG_FILE = Path(__file__).parent / "solark_debug.log"

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
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("SolArk file logger initialized at %s", LOG_FILE)
    except Exception as e:  # noqa: BLE001
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

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

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

    # -------------------------------------------------------------------------
    # Auth
    # -------------------------------------------------------------------------

    async def _oauth_login(self) -> None:
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

    # -------------------------------------------------------------------------
    # HTML SOC scraping
    # -------------------------------------------------------------------------

    async def _fetch_soc_from_html(self) -> Optional[float]:
        """Fetch Battery SOC from the mys
        olark overview HTML page.

        Uses the URL style:
          https://www.mysolark.com/plants/overview/{plant_id}/2

        and looks for:
          <div class="soc">72.0%</div>
        """
        await self._ensure_token()

        url = f"{self.base_url}/plants/overview/{self.plant_id}/2"
        headers = self._get_headers(strict=True)
        headers[
            "Accept"
        ] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

        _LOGGER.debug("Fetching SOC from HTML overview page: %s", url)

        try:
            async with self._session.get(
                url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                text = await resp.text()
                _LOGGER.debug(
                    "HTML overview response HTTP %s, length=%s",
                    resp.status,
                    len(text),
                )
                if resp.status != 200:
                    _LOGGER.warning(
                        "HTML SOC fetch got HTTP %s, ignoring", resp.status
                    )
                    return None
        except asyncio.TimeoutError as e:  # noqa: BLE001
            _LOGGER.warning("HTML SOC fetch timeout: %s", e)
            return None
        except aiohttp.ClientError as e:  # noqa: BLE001
            _LOGGER.warning("HTML SOC fetch client error: %s", e)
            return None

        # Regex: <div class="soc">72.0%</div>
        m = re.search(
            r'class="soc"[^>]*>([0-9]+(?:\.[0-9]+)?)\s*%',
            text,
        )
        if not m:
            _LOGGER.warning("Could not find SOC div in HTML overview page")
            return None

        try:
            soc_value = float(m.group(1))
        except ValueError:
            _LOGGER.warning(
                "Failed to parse SOC percentage from HTML: %r", m.group(1)
            )
            return None

        _LOGGER.debug("Parsed SOC from HTML as %s%%", soc_value)
        return soc_value

    # -------------------------------------------------------------------------
    # Plant data
    # -------------------------------------------------------------------------

    async def get_plant_data(self) -> Dict[str, Any]:
        """Fetch live plant data and HTML SOC for SolArk 12K."""
        await self._ensure_token()
        _LOGGER.debug("Getting plant data for plant_id=%s", self.plant_id)

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

        _LOGGER.debug("Requesting live data for inverter SN=%s", sn)
        live_resp = await self._request(
            "GET",
            f"/api/v1/dy/store/{sn}/read",
            {"sn": sn},
        )
        _LOGGER.debug("Raw live response: %s", live_resp)

        live_data = live_resp.get("data") or live_resp
        if not isinstance(live_data, dict):
            _LOGGER.debug("Live data for SN=%s is not a dict: %r", sn, live_data)
            return {}

        _LOGGER.debug(
            "Live data keys for SN=%s: %s", sn, list(live_data.keys())
        )

        # Merge energy from inverter summary if present
        try:
            etoday = first.get("etoday")
            etotal = first.get("etotal")
            if etoday is not None:
                live_data.setdefault("energyToday", etoday)
            if etotal is not None:
                live_data.setdefault("energyTotal", etotal)
        except Exception as e:  # noqa: BLE001
            _LOGGER.debug(
                "Unable to merge inverter energy stats into live data: %s", e
            )

        # Fetch SOC from HTML and inject as battSoc
        try:
            soc_html = await self._fetch_soc_from_html()
            if soc_html is not None:
                live_data["battSoc"] = soc_html
                _LOGGER.debug(
                    "Injected battSoc from HTML into live_data: %s", soc_html
                )
        except Exception as e:  # noqa: BLE001
            _LOGGER.warning("HTML SOC fetch/inject failed: %s", e)

        return live_data

    async def test_connection(self) -> bool:
        try:
            await self.login()
            await self.get_plant_data()
            return True
        except SolArkCloudAPIError as e:
            _LOGGER.error("SolArk test_connection failed: %s", e)
            return False

    # -------------------------------------------------------------------------
    # Parsing helpers
    # -------------------------------------------------------------------------

    def _safe_float(self, value: Any) -> float:
        try:
            if value is None:
                return 0.0
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def parse_plant_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Map API + HTML fields to sensor values (SolArk 12K)."""
        if not isinstance(data, dict):
            _LOGGER.warning("parse_plant_data got non-dict: %r", data)
            return {}

        _LOGGER.debug("parse_plant_data received keys: %s", list(data.keys()))

        sensors: Dict[str, Any] = {}

        # --- Energy today / total ---
        if "energyToday" in data or "etoday" in data:
            sensors["energy_today"] = self._safe_float(
                data.get("energyToday", data.get("etoday"))
            )
        if "energyTotal" in data or "etotal" in data:
            sensors["energy_total"] = self._safe_float(
                data.get("energyTotal", data.get("etotal"))
            )

        # --- Battery SOC ---
        # Prefer battSoc, which we injected from HTML.
        if "battSoc" in data:
            sensors["battery_soc"] = self._safe_float(data.get("battSoc"))

        # Fallback: SOC from curCap / batteryCap if battSoc missing
        if "battery_soc" not in sensors:
            cur_cap = self._safe_float(data.get("curCap"))
            batt_cap = self._safe_float(data.get("batteryCap"))
            if batt_cap > 0:
                sensors["battery_soc"] = (cur_cap / batt_cap) * 100.0

        # --- PV power ---
        if "pvPower" in data:
            sensors["pv_power"] = self._safe_float(data.get("pvPower"))

        # Fallback: sum MPPT strings voltN * currentN
        pv_sum = 0.0
        for i in range(1, 13):
            v_raw = data.get(f"volt{i}")
            c_raw = data.get(f"current{i}")
            if v_raw is None and c_raw is None:
                continue
            v = self._safe_float(v_raw)
            c = self._safe_float(c_raw)
            pv_sum += v * c

        if "pv_power" not in sensors and pv_sum != 0.0:
            sensors["pv_power"] = pv_sum

        # --- Battery power ---
        if "battPower" in data:
            sensors["battery_power"] = self._safe_float(data.get("battPower"))

        if "battery_power" not in sensors:
            cur_volt = self._safe_float(data.get("curVolt"))
            charge_current = self._safe_float(data.get("chargeCurrent"))
            if cur_volt != 0.0 or charge_current != 0.0:
                sensors["battery_power"] = cur_volt * charge_current

        # --- Grid import/export from meterA/B/C ---
        meter_a = self._safe_float(data.get("meterA"))
        meter_b = self._safe_float(data.get("meterB"))
        meter_c = self._safe_float(data.get("meterC"))
        grid_net = meter_a + meter_b + meter_c

        if grid_net != 0.0:
            if grid_net > 0:
                sensors["grid_import_power"] = grid_net
                sensors["grid_export_power"] = 0.0
            else:
                sensors["grid_import_power"] = 0.0
                sensors["grid_export_power"] = abs(grid_net)
        else:
            if "gridImportPower" in data:
                sensors["grid_import_power"] = self._safe_float(
                    data.get("gridImportPower")
                )
            if "gridExportPower" in data:
                sensors["grid_export_power"] = self._safe_float(
                    data.get("gridExportPower")
                )

        # Ensure all minimal sensors exist
        sensors.setdefault("pv_power", 0.0)
        sensors.setdefault("battery_power", 0.0)
        sensors.setdefault("grid_import_power", 0.0)
        sensors.setdefault("grid_export_power", 0.0)
        sensors.setdefault("battery_soc", 0.0)
        sensors.setdefault("energy_today", 0.0)
        sensors.setdefault("energy_total", 0.0)

        _LOGGER.debug("Parsed sensors dict: %s", sensors)
        return sensors
