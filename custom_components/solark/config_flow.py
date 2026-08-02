"""Config flow for SolArk."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

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
    normalize_solark_urls,
)
from .discovery import discover_api_url

_LOGGER = logging.getLogger(__name__)


async def _resolve_for_flow(
    hass, data: dict[str, Any]
) -> tuple[str, str, bool]:
    """Normalize URLs and optionally discover the API endpoint."""
    base_url, api_url = normalize_solark_urls(
        data.get(CONF_BASE_URL, DEFAULT_BASE_URL),
        data.get(CONF_API_URL, DEFAULT_API_URL),
    )
    auto_discover = data.get(CONF_AUTO_DISCOVER_API, DEFAULT_AUTO_DISCOVER_API)
    if auto_discover:
        session = async_get_clientsession(hass)
        discovered = await discover_api_url(session, base_url)
        if discovered:
            api_url = discovered
    return base_url, api_url, bool(auto_discover)


async def _test_connection(
    hass, data: dict[str, Any]
) -> tuple[bool, str | None, dict[str, Any] | None]:
    base_url, api_url, auto_discover = await _resolve_for_flow(hass, data)
    session = async_get_clientsession(hass)
    api = SolArkCloudAPI(
        username=data[CONF_USERNAME],
        password=data[CONF_PASSWORD],
        plant_id=data[CONF_PLANT_ID],
        base_url=base_url,
        api_url=api_url,
        session=session,
    )

    try:
        ok = await api.test_connection()
        if ok:
            return True, None, {
                CONF_BASE_URL: base_url,
                CONF_API_URL: api_url,
                CONF_AUTO_DISCOVER_API: auto_discover,
            }
        return False, "cannot_connect", None
    except SolArkCloudAPIError as e:  # noqa: BLE001
        _LOGGER.error("SolArk test_connection failed: %s", e)
        return False, "auth_failed", None
    except Exception as e:  # noqa: BLE001
        _LOGGER.exception("Unexpected exception testing SolArk connection: %s", e)
        return False, "unknown", None


class SolArkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SolArk."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            ok, reason, resolved = await _test_connection(self.hass, user_input)
            if ok and resolved:
                unique_id = f"{user_input[CONF_USERNAME]}_{user_input[CONF_PLANT_ID]}"
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"SolArk {user_input[CONF_PLANT_ID]}",
                    data={
                        CONF_USERNAME: user_input[CONF_USERNAME],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                        CONF_PLANT_ID: user_input[CONF_PLANT_ID],
                        CONF_BASE_URL: resolved[CONF_BASE_URL],
                        CONF_API_URL: resolved[CONF_API_URL],
                        CONF_AUTO_DISCOVER_API: resolved[CONF_AUTO_DISCOVER_API],
                        CONF_SCAN_INTERVAL: int(
                            user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                        ),
                    },
                )

            errors["base"] = reason or "unknown"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_PLANT_ID): str,
                vol.Optional(
                    CONF_AUTO_DISCOVER_API, default=DEFAULT_AUTO_DISCOVER_API
                ): bool,
                vol.Optional(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
                vol.Optional(CONF_API_URL, default=DEFAULT_API_URL): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        return SolArkOptionsFlowHandler(config_entry)


class SolArkOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle SolArk options (post-install settings)."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            base_url, api_url, auto_discover = await _resolve_for_flow(
                self.hass,
                {
                    CONF_BASE_URL: user_input.get(
                        CONF_BASE_URL,
                        self.config_entry.data.get(CONF_BASE_URL, DEFAULT_BASE_URL),
                    ),
                    CONF_API_URL: user_input.get(
                        CONF_API_URL,
                        self.config_entry.data.get(CONF_API_URL, DEFAULT_API_URL),
                    ),
                    CONF_AUTO_DISCOVER_API: user_input.get(
                        CONF_AUTO_DISCOVER_API,
                        self.config_entry.data.get(
                            CONF_AUTO_DISCOVER_API, DEFAULT_AUTO_DISCOVER_API
                        ),
                    ),
                },
            )
            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data={
                    **self.config_entry.data,
                    CONF_BASE_URL: base_url,
                    CONF_API_URL: api_url,
                    CONF_AUTO_DISCOVER_API: auto_discover,
                },
            )
            return self.async_create_entry(
                title="",
                data={
                    CONF_SCAN_INTERVAL: int(
                        user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                    ),
                    CONF_AUTO_DISCOVER_API: auto_discover,
                },
            )

        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        current_auto = self.config_entry.options.get(
            CONF_AUTO_DISCOVER_API,
            self.config_entry.data.get(
                CONF_AUTO_DISCOVER_API, DEFAULT_AUTO_DISCOVER_API
            ),
        )

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_AUTO_DISCOVER_API,
                    default=current_auto,
                ): bool,
                vol.Optional(
                    CONF_BASE_URL,
                    default=self.config_entry.data.get(
                        CONF_BASE_URL, DEFAULT_BASE_URL
                    ),
                ): str,
                vol.Optional(
                    CONF_API_URL,
                    default=self.config_entry.data.get(CONF_API_URL, DEFAULT_API_URL),
                ): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=current_interval,
                ): int,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )
