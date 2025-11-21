# SolArk Cloud – Home Assistant Integration (v4.0.3, minimal sensor set)

Custom Home Assistant integration for SolArk Cloud using the OAuth2 API at
https://ecsprod-api-new.solarkcloud.com behind https://www.mysolark.com.

## Highlights

- OAuth login with legacy fallback for older endpoints.
- Polling interval configurable in config flow and options.
- Advanced file logging to `custom_components/solark/solark_debug.log`.
- Diagnostics support from the Home Assistant UI.
- Minimal, high-value sensors only:
  - PV Power
  - Battery Power
  - Grid Import Power
  - Grid Export Power
  - Battery State of Charge (SOC)
  - Energy Today
  - Energy Total

Install via HACS as a custom repository, restart HA, then add the **SolArk Cloud**
integration from Settings → Devices & Services.
