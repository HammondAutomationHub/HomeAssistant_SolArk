# Changelog

## 4.0.3
- Trimmed entity set down to a minimal, high-value group:
  - `pv_power`, `battery_power`
  - `grid_import_power`, `grid_export_power`
  - `battery_soc`
  - `energy_today`, `energy_total`
- All other internal / per-string / grid-meter sensors are no longer exposed as entities.

## 4.0.2
- Added additional sensors:
  - Battery DC voltage (`battery_dc_voltage`)
  - Battery charge current (`battery_current`)
  - Inverter output voltage/current (`inverter_output_voltage`, `inverter_output_current`)
  - Grid meter per-phase powers (`grid_meter_a`, `grid_meter_b`, `grid_meter_c`)
  - Per-string PV powers (`pv_string_1_power` … `pv_string_12_power`)
  - Direct grid import/export power (`grid_import_power`, `grid_export_power`) when available.
- Kept STROG / protocol-2 computed aggregate values:
  - `pv_power`, `load_power`, `grid_power`, `battery_power`, `battery_soc`.

## 4.0.1
- Minor packaging for GitHub/HACS and logging verification.

## 4.0.0
- Initial STROG / protocol-2 support with computed PV/load/grid/battery power and SOC.
