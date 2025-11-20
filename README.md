# Sol-Ark Cloud Integration for Home Assistant

A custom Home Assistant integration that connects to Sol-Ark Cloud (MySolArk portal) to retrieve live solar inverter and battery data.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Method 1: HACS (Recommended)](#method-1-hacs-recommended)
  - [Method 2: Manual Installation](#method-2-manual-installation)
- [Configuration](#configuration)
  - [Finding Your Plant ID](#finding-your-plant-id-do-this-first)
  - [Adding the Integration](#adding-the-integration-in-home-assistant)
  - [Viewing Your Integration](#viewing-your-new-integration)
  - [Updating Configuration](#updating-configuration)
  - [Multiple Systems](#using-multiple-sol-ark-systems)
- [Available Sensors](#available-sensors)
- [Using Your Sensors](#using-your-sensors-in-home-assistant)
  - [Viewing Sensor Data](#viewing-sensor-data)
  - [Customizing Names](#customizing-sensor-names)
  - [Adding to Dashboard](#adding-to-dashboard)
- [Usage Examples](#usage-examples)
  - [Energy Dashboard](#integrating-with-home-assistant-energy-dashboard)
  - [Dashboard Cards](#dashboard-cards)
  - [Automations](#automations)
- [Troubleshooting](#troubleshooting)
- [API Information](#api-information)
- [Credits](#credits)
- [Support](#support)
- [License](#license)
- [Disclaimer](#disclaimer)
- [Development](#development)

## Features

- 🔐 **Secure Authentication** with MySolArk credentials
- 🔄 **Flexible Auth Modes**: Auto, Strict, and Legacy authentication support
- 📊 **Comprehensive Sensors**:
  - PV Power (W)
  - Load Power (W)
  - Grid Import Power (W)
  - Grid Export Power (W)
  - Battery Power (W) - positive for discharge, negative for charging
  - Battery State of Charge (%)
  - Energy Today (kWh)
  - Last Error (diagnostics)
- ⚙️ **Full UI Configuration** - No YAML editing required
- 🔧 **Options Flow** - Easily update settings without recreating the integration
- 📡 **Configurable Update Interval** - Balance between data freshness and API load
- 🌐 **Multiple Base URL Support** - Works with api.solarkcloud.com and www.mysolark.com

## Installation

### Prerequisites

Before installing, ensure you have:
- ✅ Home Assistant Core 2023.1.0 or newer
- ✅ Active MySolArk account with access to your plant data
- ✅ Your Sol-Ark Plant ID (see "Finding Your Plant ID" below)

### Method 1: HACS (Recommended)

**HACS** (Home Assistant Community Store) makes installation and updates easy:

1. **Open HACS**
   - In Home Assistant, click on "HACS" in the sidebar
   - If you don't have HACS, install it first: https://hacs.xyz/docs/setup/download

2. **Add Custom Repository**
   - Click the three-dot menu (⋮) in the top right corner
   - Select "Custom repositories"
   - In the "Repository" field, enter: `https://github.com/HammondAutomationHub/HomeAssistant_SolArk`
   - In the "Category" dropdown, select: **Integration**
   - Click "Add"

3. **Install the Integration**
   - Go to the "Integrations" tab in HACS
   - Click "+ Explore & Download Repositories"
   - Search for "Sol-Ark Cloud"
   - Click on "Sol-Ark Cloud"
   - Click "Download" button
   - Select the latest version
   - Click "Download" again to confirm

4. **Restart Home Assistant**
   - Go to **Settings** → **System** → **Restart**
   - Or use **Developer Tools** → **YAML** → **Restart** → **Restart Home Assistant**
   - Wait for Home Assistant to fully restart (typically 30-60 seconds)

5. **Verify Installation**
   - The integration files are now in your system
   - Ready to configure (see Configuration section below)

### Method 2: Manual Installation

If you prefer manual installation or don't use HACS:

1. **Download the Integration**
   - Go to: https://github.com/HammondAutomationHub/HomeAssistant_SolArk
   - Click the green "Code" button
   - Select "Download ZIP"
   - Extract the ZIP file

2. **Locate Your Config Directory**
   - Find your Home Assistant configuration directory
   - Common locations:
     - Docker: `/config`
     - Home Assistant OS: `/config`
     - Manual install: `~/.homeassistant`
   - This is where your `configuration.yaml` file lives

3. **Create Custom Components Folder** (if needed)
   - In your config directory, look for `custom_components` folder
   - If it doesn't exist, create it
   - Final structure: `<config>/custom_components/`

4. **Copy Integration Files**
   - From the downloaded ZIP, copy the `custom_components/solark_cloud` folder
   - Paste into your `<config>/custom_components/` directory
   - Verify structure: `<config>/custom_components/solark_cloud/`
   - Should contain files like: `__init__.py`, `manifest.json`, `config_flow.py`, etc.

5. **Restart Home Assistant**
   - Go to **Settings** → **System** → **Restart**
   - Wait for restart to complete

6. **Verify Installation**
   - Check **Settings** → **System** → **Logs** for any errors
   - Integration should be ready to add

## Configuration

All configuration is done through the Home Assistant UI - **no YAML editing required!**

### Finding Your Plant ID (Do This First!)

Before adding the integration, you need your Plant ID:

1. **Log into MySolArk Portal**
   - Go to: https://www.mysolark.com
   - Enter your MySolArk credentials
   - Click "Sign In"

2. **Navigate to Your Plant**
   - You should see your plant/system dashboard
   - If you have multiple plants, select the one you want to monitor

3. **Get Plant ID from URL**
   - Look at your browser's address bar
   - The URL will look like: `https://www.mysolark.com/plant/detail/12345`
   - The number at the end is your **Plant ID** (in this example: `12345`)
   - **Write this number down** - you'll need it in the next step

### Adding the Integration in Home Assistant

After installation and restart, add the integration:

1. **Navigate to Integrations**
   - Click on **Settings** in the sidebar (gear icon)
   - Click **Devices & Services**
   - You'll see a list of all your integrations

2. **Add New Integration**
   - Click the **+ Add Integration** button (bottom right corner)
   - A dialog will appear

3. **Search for Sol-Ark**
   - In the search box, type: `Sol-Ark Cloud` or just `Sol-Ark`
   - Click on **Sol-Ark Cloud** when it appears
   - The configuration form will open

4. **Fill in Required Information**

   The form has several fields. Here's what to enter:

   **Required Fields:**

   - **Email Address**
     - Enter your MySolArk account email
     - This is the email you use to log into https://www.mysolark.com
     - Example: `john@example.com`

   - **Password**
     - Enter your MySolArk account password
     - This is stored securely and encrypted by Home Assistant
     - The field will show dots (••••) for security

   - **Plant ID**
     - Enter the number you found in your MySolArk URL
     - Just the number, no letters or special characters
     - Example: `12345`

   **Optional Fields (Usually Leave as Default):**

   - **Base URL**
     - Default: `https://api.solarkcloud.com`
     - Alternative: `https://www.mysolark.com`
     - Only change if you have connection issues

   - **Authentication Mode**
     - Default: `Auto` (recommended)
     - Options: `Auto`, `Strict`, `Legacy`
     - Auto tries all methods automatically

   - **Update Interval**
     - Default: `120` seconds (2 minutes)
     - Range: 30 to 3600 seconds
     - Lower = more frequent updates (but more API calls)
     - Higher = less frequent updates (but lighter on API)

5. **Submit Configuration**
   - Click the **Submit** button at the bottom
   - Home Assistant will test the connection
   - This may take 5-10 seconds

6. **Success!**
   - If successful, you'll see "Success!" message
   - The integration appears in your Devices & Services list
   - Sensors are automatically created

7. **If Connection Fails**
   - Double-check your email and password
   - Verify your Plant ID is correct
   - Try changing Base URL to `https://www.mysolark.com`
   - Try changing Auth Mode to `Legacy`
   - Check Settings → System → Logs for detailed errors

### Viewing Your New Integration

After successful setup:

1. **Find Integration in List**
   - Go to **Settings** → **Devices & Services**
   - Scroll to find **Sol-Ark Cloud**
   - You'll see it with your plant ID

2. **Click on the Integration**
   - Shows device information
   - Lists all 8 sensors
   - Shows last update time

3. **View Device**
   - Click on the device name (e.g., "Sol-Ark Plant 12345")
   - See all sensors and their current values
   - Access sensor history and graphs

### Updating Configuration

Change settings without removing the integration:

1. **Navigate to Integration**
   - **Settings** → **Devices & Services**
   - Find **Sol-Ark Cloud** integration

2. **Open Configuration**
   - Click the three-dot menu (⋮) on the integration card
   - Select **Configure**
   - Or click **Configure** button if visible

3. **Update Settings**
   - You can change:
     - Base URL
     - Authentication Mode
     - Update Interval
   - You **cannot** change:
     - Username
     - Password  
     - Plant ID
   - (To change these, you must remove and re-add the integration)

4. **Save Changes**
   - Click **Submit**
   - Changes take effect immediately
   - No restart required

### Using Multiple Sol-Ark Systems

If you have multiple Sol-Ark installations:

1. Add the integration multiple times (one for each plant)
2. Use different Plant IDs for each
3. Each creates separate sensors with unique IDs
4. Sensors are grouped by plant in Devices & Services

## Available Sensors

After configuration, the following sensors will be created:

| Sensor | Description | Unit | Device Class |
|--------|-------------|------|--------------|
| `sensor.sol_ark_pv_power` | Solar panel power production | W | Power |
| `sensor.sol_ark_load_power` | Current load consumption | W | Power |
| `sensor.sol_ark_grid_import_power` | Power imported from grid | W | Power |
| `sensor.sol_ark_grid_export_power` | Power exported to grid | W | Power |
| `sensor.sol_ark_battery_power` | Battery charge/discharge | W | Power |
| `sensor.sol_ark_battery_state_of_charge` | Battery level | % | Battery |
| `sensor.sol_ark_energy_today` | Total energy produced today | kWh | Energy |
| `sensor.sol_ark_last_error` | Last system error | - | - |

### Battery Power Sensor

The battery power sensor shows:
- **Positive values**: Battery is discharging (providing power)
- **Negative values**: Battery is charging (consuming power)
- **Zero**: Battery is idle

Additional attribute `status` shows: `charging`, `discharging`, or `idle`

## Using Your Sensors in Home Assistant

### Viewing Sensor Data

**Method 1: Developer Tools (Quick Check)**

1. Go to **Developer Tools** (in sidebar)
2. Click **States** tab
3. In the filter box, type: `sol_ark`
4. See all 8 sensors with current values
5. Click any sensor to see detailed information

**Method 2: Device Page (Organized View)**

1. **Settings** → **Devices & Services**
2. Find and click **Sol-Ark Cloud** integration
3. Click on your device (e.g., "Sol-Ark Plant 12345")
4. See all sensors organized together
5. Click any sensor for history graph

**Method 3: Dashboard Cards (Visual Display)**

See "Usage Examples" section below for creating dashboard cards

### Understanding Sensor Names

After adding the integration, your sensors are named:

| Entity ID | Friendly Name | Shows |
|-----------|---------------|-------|
| `sensor.sol_ark_pv_power` | Sol-Ark PV Power | Current solar production |
| `sensor.sol_ark_load_power` | Sol-Ark Load Power | Current home consumption |
| `sensor.sol_ark_grid_import_power` | Sol-Ark Grid Import Power | Power from utility |
| `sensor.sol_ark_grid_export_power` | Sol-Ark Grid Export Power | Power to utility |
| `sensor.sol_ark_battery_power` | Sol-Ark Battery Power | Battery charge/discharge |
| `sensor.sol_ark_battery_state_of_charge` | Sol-Ark Battery State of Charge | Battery percentage |
| `sensor.sol_ark_energy_today` | Sol-Ark Energy Today | Daily production total |
| `sensor.sol_ark_last_error` | Sol-Ark Last Error | System diagnostics |

### Customizing Sensor Names

To change how sensors appear in Home Assistant:

1. **Settings** → **Devices & Services**
2. Click **Entities** tab
3. Search for `sol_ark`
4. Click on a sensor
5. Click **Settings** (gear icon)
6. Update:
   - **Name**: Change display name
   - **Entity ID**: Change technical ID (use caution)
   - **Icon**: Change icon
   - **Area**: Assign to room/area
7. Click **Update**

### Adding to Dashboard

**Quick Add - Entities Card**

1. Open your dashboard (Overview)
2. Click **Edit Dashboard** (top right, three dots)
3. Click **Add Card**
4. Select **Entities**
5. Click **+ Add Entity**
6. Search and select `sol_ark` sensors
7. Arrange in desired order
8. Click **Save**

**Example Entities Card Configuration:**

```yaml
type: entities
title: Solar System Status
entities:
  - entity: sensor.sol_ark_pv_power
    name: Solar Production
  - entity: sensor.sol_ark_battery_state_of_charge
    name: Battery Level
  - entity: sensor.sol_ark_battery_power
    name: Battery Flow
  - entity: sensor.sol_ark_load_power
    name: Home Usage
  - entity: sensor.sol_ark_grid_import_power
    name: From Grid
  - entity: sensor.sol_ark_energy_today
    name: Today's Production
```

**Create Gauge Cards for Visual Display**

1. **Edit Dashboard**
2. **Add Card** → **Gauge**
3. Select `sensor.sol_ark_battery_state_of_charge`
4. Configure:
   - Name: "Battery Level"
   - Min: 0
   - Max: 100
   - Severity colors (optional):
     - Green: 50-100
     - Yellow: 20-50
     - Red: 0-20
5. **Save**

**Create Power Flow Card (Advanced)**

For a visual power flow diagram:

1. Install "Power Flow Card Plus" from HACS (if available)
2. Or use built-in Energy Dashboard (Settings → Energy)
3. Configure with your Sol-Ark sensors

## Usage Examples

### Integrating with Home Assistant Energy Dashboard

The Energy Dashboard provides comprehensive energy monitoring. Here's how to add your Sol-Ark sensors:

**1. Open Energy Dashboard Configuration**
   - **Settings** → **Dashboards** → **Energy**
   - Or sidebar: **Energy** → Click **Configure** (if first time)

**2. Configure Solar Panels**
   - Click **Add Solar Production**
   - **Solar production**: Select `sensor.sol_ark_pv_power`
   - Click **Save**
   - Energy Dashboard will now track your solar production

**3. Configure Battery Storage (Recommended)**
   - In Energy Dashboard configuration
   - Find **Battery Systems** section
   - Click **Add Battery System**
   - **Energy going in to the battery**: `sensor.sol_ark_battery_power` (when negative)
   - **Energy coming out of the battery**: `sensor.sol_ark_battery_power` (when positive)
   - Click **Save**
   - Note: The battery power sensor handles both directions automatically

**4. Configure Grid (If Applicable)**
   - **Grid Consumption**: Click **Add Grid Consumption**
   - Select: `sensor.sol_ark_grid_import_power`
   - **Return to Grid**: Click **Add Grid Return**  
   - Select: `sensor.sol_ark_grid_export_power`
   - Click **Save** for each

**5. View Energy Dashboard**
   - Click **Energy** in sidebar
   - See visual energy flow
   - View daily, weekly, monthly statistics
   - Track energy costs (if configured)

### Dashboard Cards

**Create Simple Status Card**

```yaml
type: entities
title: Sol-Ark Status
entities:
  - sensor.sol_ark_pv_power
  - sensor.sol_ark_battery_state_of_charge
  - sensor.sol_ark_load_power
show_header_toggle: false
```

**Create Detailed Monitoring Card**

```yaml
type: vertical-stack
cards:
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.sol_ark_battery_state_of_charge
        name: Battery Level
        min: 0
        max: 100
        severity:
          green: 50
          yellow: 20
          red: 0
      - type: sensor
        entity: sensor.sol_ark_pv_power
        name: Solar Production
        graph: line
  - type: entities
    title: Power Flow
    entities:
      - entity: sensor.sol_ark_pv_power
        name: Solar → System
      - entity: sensor.sol_ark_battery_power
        name: Battery Flow
      - entity: sensor.sol_ark_load_power
        name: Home Usage
      - entity: sensor.sol_ark_grid_import_power
        name: From Grid
      - entity: sensor.sol_ark_grid_export_power
        name: To Grid
  - type: sensor
    entity: sensor.sol_ark_energy_today
    name: Today's Energy
    graph: line
```

### Automations

Create automations based on your solar system status.

**Example 1: Low Battery Alert**

Get notified when battery drops below 20%:

Via UI:
1. **Settings** → **Automations & Scenes**
2. Click **Create Automation** → **Create new automation**
3. Click **Add Trigger** → **Numeric State**
   - Entity: `sensor.sol_ark_battery_state_of_charge`
   - Below: `20`
4. Click **Add Action** → **Send notification**
   - Service: `notify.mobile_app_your_phone` (select your device)
   - Message: `Battery low at {{ states('sensor.sol_ark_battery_state_of_charge') }}%`
5. **Save** with name: "Low Battery Alert"

Via YAML:
```yaml
alias: Low Battery Alert
trigger:
  - platform: numeric_state
    entity_id: sensor.sol_ark_battery_state_of_charge
    below: 20
action:
  - service: notify.mobile_app
    data:
      title: "Battery Low"
      message: "Sol-Ark battery is at {{ states('sensor.sol_ark_battery_state_of_charge') }}%"
```

**Example 2: Daily Energy Report**

Get production summary at end of day:

Via UI:
1. **Settings** → **Automations & Scenes**
2. **Create Automation** → **Create new automation**
3. **Add Trigger** → **Time**
   - At: `23:59:00`
4. **Add Action** → **Send notification**
   - Message: `Today's solar production: {{ states('sensor.sol_ark_energy_today') }} kWh`
5. **Save**

Via YAML:
```yaml
alias: Daily Energy Report
trigger:
  - platform: time
    at: "23:59:00"
action:
  - service: notify.mobile_app
    data:
      title: "Daily Energy Summary"
      message: "Today's production: {{ states('sensor.sol_ark_energy_today') }} kWh"
```

**Example 3: High Production Alert**

Notify when solar exceeds threshold (good for tracking):

Via UI:
1. **Add Trigger** → **Numeric State**
   - Entity: `sensor.sol_ark_pv_power`
   - Above: `5000` (5kW - adjust for your system)
   - For: `00:10:00` (10 minutes)
2. **Add Action** → **Send notification**
   - Message: `High solar production: {{ states('sensor.sol_ark_pv_power') }}W`

Via YAML:
```yaml
alias: High Production Alert
trigger:
  - platform: numeric_state
    entity_id: sensor.sol_ark_pv_power
    above: 5000
    for:
      hours: 0
      minutes: 10
action:
  - service: notify.mobile_app
    data:
      message: "High solar production: {{ states('sensor.sol_ark_pv_power') }}W 🌞"
```

**Example 4: Battery Full Notification**

Know when battery is fully charged:

Via YAML:
```yaml
alias: Battery Full
trigger:
  - platform: numeric_state
    entity_id: sensor.sol_ark_battery_state_of_charge
    above: 95
condition:
  - condition: numeric_state
    entity_id: sensor.sol_ark_battery_power
    below: 100  # Charging with less than 100W (nearly complete)
action:
  - service: notify.mobile_app
    data:
      title: "Battery Fully Charged"
      message: "Sol-Ark battery is at {{ states('sensor.sol_ark_battery_state_of_charge') }}%"
```

**Example 5: Grid Export Tracking**

Track when you're sending power to grid:

Via YAML:
```yaml
alias: Exporting to Grid
trigger:
  - platform: numeric_state
    entity_id: sensor.sol_ark_grid_export_power
    above: 500
    for:
      minutes: 5
action:
  - service: notify.mobile_app
    data:
      message: "Currently exporting {{ states('sensor.sol_ark_grid_export_power') }}W to grid"
```

**Example 6: System Error Alert**

Get notified of system errors:

Via YAML:
```yaml
alias: Sol-Ark System Error
trigger:
  - platform: state
    entity_id: sensor.sol_ark_last_error
condition:
  - condition: template
    value_template: "{{ states('sensor.sol_ark_last_error') != 'None' }}"
action:
  - service: notify.mobile_app
    data:
      title: "Sol-Ark System Error"
      message: "Error detected: {{ states('sensor.sol_ark_last_error') }}"
      data:
        priority: high
```

## Troubleshooting

### Common Installation Issues

**Issue: "Integration not found" after installation**

**Solution**:
1. Verify files are in correct location: `<config>/custom_components/solark_cloud/`
2. Check that folder contains: `__init__.py`, `manifest.json`, etc.
3. Restart Home Assistant completely
4. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
5. Check Settings → System → Logs for errors

**Issue: "Cannot connect" error during setup**

**Solution**:
1. Verify MySolArk credentials are correct
   - Test login at https://www.mysolark.com
2. Double-check Plant ID matches exactly
3. Try alternative Base URL: `https://www.mysolark.com`
4. Try different Authentication Mode: `Legacy`
5. Check your internet connection
6. Verify firewall allows Home Assistant to access Sol-Ark API

**Issue: Sensors not updating**

**Solution**:
1. Check Update Interval setting (minimum is 30 seconds)
2. Verify Sol-Ark system is online in MySolArk portal
3. Check Settings → System → Logs for API errors
4. Try increasing scan interval to reduce load
5. Verify your MySolArk account hasn't been locked

### Viewing Debug Logs

If you need detailed troubleshooting information:

1. **Enable Debug Logging**
   
   Add to `configuration.yaml`:
   ```yaml
   logger:
     default: warning
     logs:
       custom_components.solark_cloud: debug
   ```

2. **Restart Home Assistant**

3. **View Logs**
   - Settings → System → Logs
   - Look for entries starting with "custom_components.solark_cloud"
   - Copy relevant errors when reporting issues

4. **Disable Debug Logging**
   - Remove the logger configuration above
   - Restart Home Assistant

### Configuration Issues

**Issue: Can't change username/password/plant ID**

This is by design. To change these:
1. Settings → Devices & Services
2. Find Sol-Ark Cloud integration
3. Click three-dot menu → Delete
4. Re-add integration with new credentials

**Issue: "Already configured" error**

**Solution**:
- You can only add each Plant ID once
- To re-configure, first delete the existing integration
- Make sure you're using the correct Plant ID for a different system

### Authentication Issues

**Issue: Authentication fails randomly**

**Solution**:
1. Increase Update Interval to 180-300 seconds
2. Switch Auth Mode to "Legacy"
3. Check if Sol-Ark is performing maintenance
4. Verify account isn't rate-limited

### Sensor Data Issues

**Issue: Sensors show "Unknown" or "Unavailable"**

**Solution**:
1. Check if integration is online (Settings → Devices & Services)
2. Verify last update time on device page
3. Check if Sol-Ark system is online
4. Restart the integration (disable/enable)
5. Check logs for API errors

**Issue: Wrong sensor values**

**Solution**:
1. Compare with MySolArk portal values
2. Check units match (W vs kW)
3. For battery power: negative = charging, positive = discharging
4. Report issue on GitHub if values don't match portal

### Getting Additional Help

If troubleshooting doesn't resolve your issue:

1. **Check GitHub Issues**: https://github.com/HammondAutomationHub/HomeAssistant_SolArk/issues
   - Search for similar problems
   - See if solution already exists

2. **Create New Issue**:
   - Include Home Assistant version
   - Include integration version
   - Include relevant log excerpts
   - Describe steps to reproduce
   - Note what you've already tried

3. **Community Support**:
   - Home Assistant Community Forum
   - Reddit: r/homeassistant
   - Discuss only after checking documentation

## Troubleshooting

### Cannot Connect Error

1. **Verify credentials**: Ensure email and password are correct
2. **Check Plant ID**: Confirm it matches your MySolArk portal
3. **Try different Base URL**: Switch between api.solarkcloud.com and www.mysolark.com
4. **Change Auth Mode**: If Auto doesn't work, try Strict or Legacy manually

### Sensors Not Updating

1. Check your **Update Interval** setting
2. Verify your Sol-Ark system is online in MySolArk portal
3. Check Home Assistant logs for API errors
4. Try increasing the scan interval to reduce API load

### Authentication Fails Periodically

1. Increase the **Update Interval** to reduce API requests
2. Switch to **Legacy** auth mode for more stable connections
3. Verify your MySolArk account is active

### Viewing Logs

Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.solark_cloud: debug
```

## API Information

This integration uses the Sol-Ark Cloud API to retrieve data:

- **Endpoints**: 
  - `POST /rest/account/login` - Authentication
  - `POST /rest/plant/getPlantData` - Retrieve plant data
- **Authentication**: Token-based (JWT)
- **Rate Limiting**: Recommended minimum 30-second intervals

## Credits

- Based on the work of Sol-Ark community projects
- Developed with assistance from AI tools
- Maintained by [@HammondAutomationHub](https://github.com/HammondAutomationHub)
- Original concept based on Sol-Ark community projects

## Support

- **Issues**: [GitHub Issues](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/discussions)

## License

MIT License - See LICENSE file for details

## Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by Sol-Ark. Use at your own risk. The integration communicates with Sol-Ark's cloud services, which are subject to change without notice.

## Development

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Testing

This integration can be tested in a Home Assistant development environment:

```bash
# Install development dependencies
pip install -r requirements_dev.txt

# Run tests
pytest tests/
```

### Code Quality

- Uses `ruff` for linting
- Type hints with `mypy`
- Black for code formatting

## Changelog

### Version 1.0.0
- Initial release
- Full UI configuration support
- Multiple authentication modes
- Comprehensive sensor coverage
- Options flow for easy updates
