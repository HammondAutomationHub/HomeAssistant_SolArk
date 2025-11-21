# SolArk Cloud – Home Assistant Integration (v4.0.7, energy/flow SOC)

Custom Home Assistant integration for SolArk Cloud using the OAuth2 API at
https://ecsprod-api-new.solarkcloud.com behind https://www.mysolark.com.

Tuned for SolArk 12K, now using the official **energy/flow** endpoint:

`GET /api/v1/plant/energy/{plant_id}/flow?date=YYYY-MM-DD`

This endpoint provides:
- `pvPower`
- `battPower`
- `gridOrMeterPower`
- `loadOrEpsPower`
- `soc` (Battery State of Charge)

## Highlights

- OAuth + legacy login fallback
- Configurable polling interval (seconds) in config flow + options
- Advanced file logging to `custom_components/solark/solark_debug.log`
- Diagnostics support
- High-value sensor set:

  - `sensor.solark_pv_power`
  - `sensor.solark_battery_power`
  - `sensor.solark_grid_power` (net)
  - `sensor.solark_load_power`
  - `sensor.solark_grid_import_power`
  - `sensor.solark_grid_export_power`
  - `sensor.solark_battery_soc`
  - `sensor.solark_energy_today`
  - `sensor.solark_energy_total`

Plant ID is fully variable and comes from the first-time config flow.
