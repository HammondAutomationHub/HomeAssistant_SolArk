"""SolArk sensors (high-value set using energy/flow)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN


@dataclass
class SolArkSensorDescription(SensorEntityDescription):
    key: str


SENSOR_DESCRIPTIONS: list[SolArkSensorDescription] = [
    # Real-time powers from energy/flow:
    SolArkSensorDescription(
        key="pv_power",
        name="PV Power",
        native_unit_of_measurement="W",
        device_class=SensorDeviceClass.POWER,
    ),
    SolArkSensorDescription(
        key="battery_power",
        name="Battery Power",
        native_unit_of_measurement="W",
        device_class=SensorDeviceClass.POWER,
    ),
    SolArkSensorDescription(
        key="grid_power",
        name="Grid Power (Net)",
        native_unit_of_measurement="W",
        device_class=SensorDeviceClass.POWER,
    ),
    SolArkSensorDescription(
        key="load_power",
        name="Load Power",
        native_unit_of_measurement="W",
        device_class=SensorDeviceClass.POWER,
    ),
    # Grid import/export derived from meterA/B/C:
    SolArkSensorDescription(
        key="grid_import_power",
        name="Grid Import Power",
        native_unit_of_measurement="W",
        device_class=SensorDeviceClass.POWER,
    ),
    SolArkSensorDescription(
        key="grid_export_power",
        name="Grid Export Power",
        native_unit_of_measurement="W",
        device_class=SensorDeviceClass.POWER,
    ),
    # Battery SOC:
    SolArkSensorDescription(
        key="battery_soc",
        name="Battery SOC",
        native_unit_of_measurement="%",
    ),
    # Energy:
    SolArkSensorDescription(
        key="energy_today",
        name="Energy Today",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
    ),
    SolArkSensorDescription(
        key="energy_total",
        name="Energy Total",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SolArk sensors from config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: DataUpdateCoordinator = data["coordinator"]

    entities: list[SolArkSensor] = [
        SolArkSensor(coordinator, entry, desc) for desc in SENSOR_DESCRIPTIONS
    ]
    async_add_entities(entities)


class SolArkSensor(CoordinatorEntity, SensorEntity):
    """Representation of a SolArk sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        description: SolArkSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "SolArk Plant",
            "manufacturer": "SolArk",
        }

    @property
    def native_value(self) -> Any:
        data = self.coordinator.data or {}
        return data.get(self.entity_description.key)
