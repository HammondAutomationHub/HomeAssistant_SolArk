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
    CONF_SCAN_INTERVAL,
    DEFAULT_BASE_URL,
    DEFAULT_API_URL,
    DEFAULT_SCAN_INTERVAL,
    PLATFORMS,
    normalize_solark_urls,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up from YAML (not used)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SolArk from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    plant_id = entry.data[CONF_PLANT_ID]
    base_url = entry.data.get(CONF_BASE_URL, DEFAULT_BASE_URL)
    api_url = entry.data.get(CONF_API_URL, DEFAULT_API_URL)
    base_url, api_url = normalize_solark_urls(base_url, api_url)

    # Persist migrated hosts so existing installs keep working after Sol-Ark
    # moved off mysolark.com / ecsprod-api-new.solarkcloud.com.
    if (
        entry.data.get(CONF_BASE_URL) != base_url
        or entry.data.get(CONF_API_URL) != api_url
    ):
        _LOGGER.warning(
            "Updating SolArk URLs for entry %s to base_url=%s api_url=%s",
            entry.entry_id,
            base_url,
            api_url,
        )
        hass.config_entries.async_update_entry(
            entry,
            data={
                **entry.data,
                CONF_BASE_URL: base_url,
                CONF_API_URL: api_url,
            },
        )

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

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
