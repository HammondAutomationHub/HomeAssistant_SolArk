# SolArk Cloud – Home Assistant Integration (v4, STROG/protocol-2 aware)

Custom Home Assistant integration for SolArk Cloud using the new OAuth2 API
behind https://www.mysolark.com.

## Highlights

- OAuth login to SolArk Cloud; legacy login fallback
- Polling interval configurable in config flow and options
- Advanced file logging to `custom_components/solark/solark_debug.log`
- Diagnostics support in HA (Download diagnostics)
- Computed real-time values for STROG / protocol-2 devices:
  - PV Power
  - Load Power
  - Grid Power
  - Battery Power
  - Battery SOC
- Energy today/total and detailed battery & limit parameters exposed as sensors.

Install via HACS as a custom repository, restart HA, then add the **SolArk Cloud**
integration from Settings → Devices & Services.
