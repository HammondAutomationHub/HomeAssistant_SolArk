# Changelog

## 4.0.7
- Added support for the official power flow endpoint:
  `/api/v1/plant/energy/{plant_id}/flow?date=YYYY-MM-DD`
  using the configured Plant ID (from the config flow).
- Reads:
  - `pvPower`, `battPower`, `gridOrMeterPower`, `loadOrEpsPower`, `soc`
- Exposes new/updated sensors:
  - `pv_power`, `battery_power`, `grid_power`, `load_power`,
    `battery_soc`, `grid_import_power`, `grid_export_power`,
    `energy_today`, `energy_total`.
- Keeps advanced logging and diagnostics.

## 4.0.6
- Derived SOC from curCap / batteryCap when flow endpoint was not yet known.
