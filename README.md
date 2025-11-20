# SolArk Cloud – Home Assistant Integration

Custom Home Assistant integration for SolArk Cloud using the new OAuth2 API
behind https://www.mysolark.com.

## Features

- Logs into SolArk Cloud via OAuth2 (`ecsprod-api-new.solarkcloud.com/oauth/token`)
- Automatically keeps the access token fresh
- Fetches live data for a configured plant (by plant ID)
- Exposes key sensors in Home Assistant:
  - PV Power
  - Load Power
  - Grid Import Power
  - Grid Export Power
  - Battery Power
  - Battery SOC
  - Energy Today
  - Last Error
- Advanced file logging to `custom_components/solark/solark_debug.log`
- Configurable polling interval (seconds), via config flow & options
- Diagnostics support available from the Home Assistant UI

## Installation via HACS

1. In Home Assistant, open **HACS → Integrations**.
2. Click the three dots → **Custom repositories**.
3. Add:

   ```text
   https://github.com/HammondAutomationHub/HomeAssistant_SolArk
   ```

   Category: **Integration**.

4. Install **SolArk Cloud** from HACS.
5. Restart Home Assistant.

Then go to **Settings → Devices & Services → Add Integration** and search for
**SolArk Cloud**. Enter your SolArk username, password, plant ID, and (optionally)
polling interval in seconds.

After installation, you can change the polling interval in the integration's
**Options** dialog.
