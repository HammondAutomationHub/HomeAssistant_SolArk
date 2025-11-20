# Sol-Ark Cloud Integration - Quick Installation Guide

## Prerequisites

- Home Assistant Core 2023.1.0 or newer
- Active MySolArk account with access to your plant data
- Your Sol-Ark Plant ID

## Installation Steps

### Step 1: Install the Integration

#### Option A: HACS (Easiest)

1. Open HACS in your Home Assistant
2. Go to **Integrations**
3. Click the **⋮** menu (three dots) in the top right
4. Select **Custom repositories**
5. Add repository: `https://github.com/HammondAutomationHub/HomeAssistant_SolArk`
6. Category: **Integration**
7. Click **Add**
8. Search for "Sol-Ark Cloud" in HACS
9. Click **Download**
10. **Restart Home Assistant**

#### Option B: Manual Installation

1. Download the latest release from GitHub
2. Extract the `custom_components/solark_cloud` folder
3. Copy to: `<config_directory>/custom_components/solark_cloud/`
4. Your folder structure should be:
   ```
   config/
   └── custom_components/
       └── solark_cloud/
           ├── __init__.py
           ├── api.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── sensor.py
           ├── strings.json
           └── translations/
               └── en.json
   ```
5. **Restart Home Assistant**

### Step 2: Get Your Plant ID

Before configuring the integration, you need your Plant ID:

1. Go to [MySolArk](https://www.mysolark.com)
2. Log in with your credentials
3. Navigate to your plant/system dashboard
4. Look at the browser URL bar
5. The Plant ID is the number in the URL:
   - URL: `https://www.mysolark.com/plant/detail/12345`
   - Plant ID: `12345`
6. **Write down this number**

### Step 3: Add the Integration

1. In Home Assistant, go to **Settings** (gear icon)
2. Click **Devices & Services**
3. Click the **+ Add Integration** button (bottom right)
4. Search for "Sol-Ark Cloud"
5. Click on it to start configuration

### Step 4: Configure the Integration

Fill in the configuration form:

#### Required Information

1. **Email Address**: Your MySolArk account email
   - Example: `john@example.com`

2. **Password**: Your MySolArk account password
   - This is stored securely and encrypted

3. **Plant ID**: The number you found in Step 2
   - Example: `12345`

#### Optional Settings (Use Defaults First)

4. **Base URL**: Leave as `https://api.solarkcloud.com`
   - Only change if you have connection issues

5. **Authentication Mode**: Leave as `Auto`
   - This tries all auth methods automatically

6. **Update Interval**: Leave as `120` seconds
   - Minimum is 30 seconds
   - Lower = more frequent updates but more API load

### Step 5: Submit and Verify

1. Click **Submit**
2. Integration will test the connection
3. If successful, you'll see "Success!" message
4. Your Sol-Ark device will appear in Devices & Services

### Step 6: Check Your Sensors

1. Go to **Developer Tools** → **States**
2. Search for "sol_ark"
3. You should see 8 sensors:
   - `sensor.sol_ark_pv_power`
   - `sensor.sol_ark_load_power`
   - `sensor.sol_ark_grid_import_power`
   - `sensor.sol_ark_grid_export_power`
   - `sensor.sol_ark_battery_power`
   - `sensor.sol_ark_battery_state_of_charge`
   - `sensor.sol_ark_energy_today`
   - `sensor.sol_ark_last_error`

## Troubleshooting Installation

### "Cannot Connect" Error

**Problem**: Integration can't reach Sol-Ark Cloud

**Solutions**:
1. Verify your email and password are correct
2. Make sure Plant ID is exactly as shown in MySolArk URL
3. Try switching Base URL to `https://www.mysolark.com`
4. Check your internet connection
5. Verify your MySolArk account is active

### "Already Configured" Error

**Problem**: This plant is already set up

**Solutions**:
1. Go to Settings → Devices & Services
2. Find existing Sol-Ark Cloud integration
3. Either use the existing one or remove it first
4. Try adding again

### Sensors Not Appearing

**Problem**: Integration added but no sensors

**Solutions**:
1. Go to Settings → Devices & Services
2. Find Sol-Ark Cloud integration
3. Click on it
4. You should see all 8 sensors listed
5. If not, try removing and re-adding the integration
6. Check Home Assistant logs for errors

### Authentication Keeps Failing

**Problem**: Can connect initially but fails later

**Solutions**:
1. Increase Update Interval to 180 or 300 seconds
2. Change Auth Mode to "Legacy"
3. Verify your MySolArk account hasn't been locked
4. Check if Sol-Ark is performing maintenance

## Post-Installation Configuration

### Add to Energy Dashboard

1. Go to Settings → Dashboards → Energy
2. Click on Solar Panels section
3. Add `sensor.sol_ark_pv_power`
4. Configure other energy sources as needed

### Create Dashboard Card

1. Go to Overview (main dashboard)
2. Click Edit Dashboard
3. Add Card → Entities
4. Select Sol-Ark sensors you want to display

### Enable Debug Logging (For Issues)

Add to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.solark_cloud: debug
```

Restart Home Assistant and check logs:
- Settings → System → Logs

## Need More Help?

- **Documentation**: See full README.md
- **Issues**: [GitHub Issues](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/issues)
- **Community**: [Home Assistant Community Forum](https://community.home-assistant.io/)

## Next Steps

After successful installation:

1. ✅ Add sensors to your dashboard
2. ✅ Configure Energy Dashboard
3. ✅ Create automations based on battery level
4. ✅ Set up notifications for system status
5. ✅ Monitor daily energy production

Enjoy your Sol-Ark Cloud integration!
