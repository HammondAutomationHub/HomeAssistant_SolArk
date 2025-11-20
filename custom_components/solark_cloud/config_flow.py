"""Config flow for Sol-Ark Cloud integration with improved error handling."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_AUTH_MODE,
    CONF_BASE_URL,
    CONF_EMAIL,
    CONF_PLANT_ID,
    DEFAULT_AUTH_MODE,
    DEFAULT_BASE_URL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .solark_api import SolArkAPI, SolArkAPIError, SolArkAuthError, SolArkConnectionError

_LOGGER = logging.getLogger(__name__)

AUTH_MODE_AUTO = "Auto"
AUTH_MODE_STRICT = "Strict"
AUTH_MODE_LEGACY = "Legacy"


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    api = SolArkAPI(
        session=session,
        email=data[CONF_EMAIL],
        password=data[CONF_PASSWORD],
        base_url=data.get(CONF_BASE_URL, DEFAULT_BASE_URL),
        auth_mode=data.get(CONF_AUTH_MODE, DEFAULT_AUTH_MODE),
    )

    # First, try to authenticate - this is the critical step that catches wrong credentials
    try:
        _LOGGER.debug("Starting authentication for user: %s", data[CONF_EMAIL])
        auth_success = await api.authenticate()
        if not auth_success:
            raise SolArkAuthError("Authentication failed - invalid credentials")
        _LOGGER.debug("Authentication successful")
    except SolArkAuthError as err:
        _LOGGER.error("Authentication error: %s", err)
        raise InvalidAuth(str(err)) from err
    except SolArkConnectionError as err:
        _LOGGER.error("Connection error: %s", err)
        raise CannotConnect(str(err)) from err
    except Exception as err:
        _LOGGER.exception("Unexpected error during authentication: %s", err)
        raise UnknownError(str(err)) from err

    # Now try to get plant data - this validates the Plant ID
    try:
        _LOGGER.debug("Fetching plant data for Plant ID: %s", data[CONF_PLANT_ID])
        plant_data = await api.get_plant_data(data[CONF_PLANT_ID])
        if not plant_data:
            raise SolArkAPIError(f"Unable to retrieve data for Plant ID: {data[CONF_PLANT_ID]}")
        _LOGGER.debug("Plant data retrieved successfully")

        return {
            "title": f"Sol-Ark Plant {data[CONF_PLANT_ID]}",
            "plant_name": plant_data.get("plantName", f"Plant {data[CONF_PLANT_ID]}"),
        }

    except SolArkAuthError as err:
        # Token issue after initial auth
        _LOGGER.error("Authentication error during plant data fetch: %s", err)
        raise InvalidAuth(str(err)) from err
    except SolArkConnectionError as err:
        _LOGGER.error("Connection error during plant data fetch: %s", err)
        raise CannotConnect(str(err)) from err
    except SolArkAPIError as err:
        _LOGGER.error("API error during plant data fetch: %s", err)
        raise InvalidPlantID(str(err)) from err
    except Exception as err:
        _LOGGER.exception("Unexpected error during plant data fetch: %s", err)
        raise UnknownError(str(err)) from err


class SolArkCloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sol-Ark Cloud."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(str(user_input[CONF_PLANT_ID]))
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, user_input)
            except InvalidAuth as err:
                errors["base"] = "invalid_auth"
                description_placeholders["error"] = str(err)
                _LOGGER.warning("Invalid authentication: %s", err)
            except CannotConnect as err:
                errors["base"] = "cannot_connect"
                description_placeholders["error"] = str(err)
                _LOGGER.warning("Cannot connect to Sol-Ark Cloud: %s", err)
            except InvalidPlantID as err:
                errors["base"] = "invalid_plant_id"
                description_placeholders["error"] = str(err)
                _LOGGER.warning("Invalid Plant ID: %s", err)
            except UnknownError as err:
                errors["base"] = "unknown"
                description_placeholders["error"] = str(err)
                _LOGGER.error("Unknown error occurred: %s", err)
            else:
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_PLANT_ID): str,
                    vol.Optional(
                        CONF_BASE_URL, default=DEFAULT_BASE_URL
                    ): vol.In(
                        [
                            "https://api.solarkcloud.com",
                            "https://www.mysolark.com",
                        ]
                    ),
                    vol.Optional(
                        CONF_AUTH_MODE, default=DEFAULT_AUTH_MODE
                    ): vol.In(
                        [AUTH_MODE_AUTO, AUTH_MODE_STRICT, AUTH_MODE_LEGACY]
                    ),
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=30, max=3600)),
                }
            ),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> SolArkCloudOptionsFlowHandler:
        """Get the options flow for this handler."""
        return SolArkCloudOptionsFlowHandler(config_entry)


class SolArkCloudOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Sol-Ark Cloud."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                test_data = {
                    CONF_EMAIL: self.config_entry.data[CONF_EMAIL],
                    CONF_PASSWORD: self.config_entry.data[CONF_PASSWORD],
                    CONF_PLANT_ID: self.config_entry.data[CONF_PLANT_ID],
                    CONF_BASE_URL: user_input.get(
                        CONF_BASE_URL, DEFAULT_BASE_URL
                    ),
                    CONF_AUTH_MODE: user_input.get(
                        CONF_AUTH_MODE, DEFAULT_AUTH_MODE
                    ),
                }
                await validate_input(self.hass, test_data)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception as err:
                _LOGGER.exception("Unexpected error in options flow: %s", err)
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_BASE_URL,
                        default=self.config_entry.options.get(
                            CONF_BASE_URL,
                            self.config_entry.data.get(
                                CONF_BASE_URL, DEFAULT_BASE_URL
                            ),
                        ),
                    ): vol.In(
                        [
                            "https://api.solarkcloud.com",
                            "https://www.mysolark.com",
                        ]
                    ),
                    vol.Optional(
                        CONF_AUTH_MODE,
                        default=self.config_entry.options.get(
                            CONF_AUTH_MODE,
                            self.config_entry.data.get(
                                CONF_AUTH_MODE, DEFAULT_AUTH_MODE
                            ),
                        ),
                    ): vol.In(
                        [AUTH_MODE_AUTO, AUTH_MODE_STRICT, AUTH_MODE_LEGACY]
                    ),
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL,
                            self.config_entry.data.get(
                                CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                            ),
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=30, max=3600)),
                }
            ),
            errors=errors,
        )


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""


class InvalidPlantID(Exception):
    """Error to indicate the Plant ID is invalid or inaccessible."""


class UnknownError(Exception):
    """Error to indicate an unknown error occurred."""
