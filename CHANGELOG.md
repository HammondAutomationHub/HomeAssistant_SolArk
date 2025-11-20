# Changelog

## 4.0.1
- Minor release packaging for GitHub/HACS.
- Confirmed advanced file logging to `custom_components/solark/solark_debug.log`.
- Ensured STROG / protocol-2 computed power sensors are wired:
  - `pv_power`, `load_power`, `grid_power`, `battery_power`, `battery_soc`.
- Polling interval exposed both in initial config and options flow.

## 4.0.0
- Added computed power values for STROG / protocol-2 inverters:
  - PV Power = Σ(voltN × currentN) for MPPT strings.
  - Load Power = inverterOutputVoltage × curCurrent × pf.
  - Grid Power = meterA + meterB + meterC.
  - Battery Power = curVolt × chargeCurrent.
  - Battery SOC from curCap / batteryCap.
- Added energy today/total and detailed battery & limit parameters.
- Implemented OAuth login with legacy fallback.
- Added diagnostics and file-based debug logging.
