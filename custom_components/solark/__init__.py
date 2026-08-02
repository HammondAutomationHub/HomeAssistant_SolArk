"""SolArk integration entry point."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import SolArkCloudAPI, SolArkCloudAPIError
from .const import (
    DOMAIN,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_PLANT_ID,
    CONF_BASE_URL,
    CONF_API_URL,
    CONF_AUTO_DISCOVER_API,
    CONF_SCAN_INTERVAL,
    DEFAULT_BASE_URL,
    DEFAULT_API_URL,
    DEFAULT_AUTO_DISCOVER_API,
    DEFAULT_SCAN_INTERVAL,
    PLATFORMS,
    normalize_solark_urls,
)
from .discovery import discover_api_url

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up from YAML (not used)."""
    return True


async def _resolve_urls(hass: HomeAssistant, entry: ConfigEntry) -> tuple[str, str, bool]:
    """Normalize hosts and optionally rediscover the API base URL."""
    base_url = entry.data.get(CONF_BASE_URL, DEFAULT_BASE_URL)
    api_url = entry.data.get(CONF_API_URL, DEFAULT_API_URL)
    auto_discover = entry.options.get(
        CONF_AUTO_DISCOVER_API,
        entry.data.get(CONF_AUTO_DISCOVER_API, DEFAULT_AUTO_DISCOVER_API),
    )
    base_url, api_url = normalize_solark_urls(base_url, api_url)

    if auto_discover:
        session = async_get_clientsession(hass)
        discovered = await discover_api_url(session, base_url)
        if discovered:
            api_url = discovered
        else:
            _LOGGER.warning(
                "SolArk API auto-discovery failed; using %s",
                api_url,
            )

    return base_url, api_url, bool(auto_discover)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SolArk from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    plant_id = entry.data[CONF_PLANT_ID]
    base_url, api_url, auto_discover = await _resolve_urls(hass, entry)

    # Persist resolved hosts / discovery flag so the UI and diagnostics stay current.
    new_data = {
        **entry.data,
        CONF_BASE_URL: base_url,
        CONF_API_URL: api_url,
        CONF_AUTO_DISCOVER_API: auto_discover,
    }
    if dict(entry.data) != new_data:
        _LOGGER.info(
            "Updating SolArk URLs for entry %s to base_url=%s api_url=%s auto_discover=%s",
            entry.entry_id,
            base_url,
            api_url,
            auto_discover,
        )
        hass.config_entries.async_update_entry(entry, data=new_data)

    scan_interval = int(
        entry.options.get(
            CONF_SCAN_INTERVAL,
            entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
    )

    _LOGGER.debug(
        "Setting up SolArk entry %s with scan_interval=%s seconds base_url=%s api_url=%s",
        entry.entry_id,
        scan_interval,
        base_url,
        api_url,
    )

    session = async_get_clientsession(hass)
    api = SolArkCloudAPI(
        username=username,
        password=password,
        plant_id=plant_id,
        base_url=base_url,
        api_url=api_url,
        session=session,
    )

    async def async_update_data() -> dict[str, Any]:
        """Fetch and parse data from SolArk."""
        try:
            raw = await api.get_plant_data()
            parsed = api.parse_plant_data(raw)
            return parsed
        except SolArkCloudAPIError as err:
            raise UpdateFailed(str(err)) from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"SolArk {plant_id}",
        update_method=async_update_data,
        update_interval=timedelta(seconds=scan_interval),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
