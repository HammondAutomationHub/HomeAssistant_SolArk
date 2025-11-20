# Sol-Ark Cloud Integration for Home Assistant

A custom Home Assistant integration that connects to Sol-Ark Cloud (MySolArk portal) to retrieve live solar inverter and battery data with enhanced error handling and user-friendly feedback.

## ✨ Features

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
- ✅ **Enhanced Error Handling** - Clear, actionable error messages with troubleshooting guidance

## 📋 Requirements

- ✅ Home Assistant Core 2023.1.0 or newer
- ✅ Active MySolArk account with access to your plant data
- ✅ Your Sol-Ark Plant ID

## 🚀 Installation

### Via HACS (Recommended)

1. **Open HACS**
   - In Home Assistant, click on "HACS" in the sidebar
   - If you don't have HACS, [install it first](https://hacs.xyz/docs/setup/download)

2. **Add Custom Repository**
   - Click the three-dot menu (⋮) in the top right corner
   - Select "Custom repositories"
   - Repository: `https://github.com/HammondAutomationHub/HomeAssistant_SolArk`
   - Category: Integration
   - Click "Add"

3. **Install the Integration**
   - Go to the "Integrations" tab in HACS
   - Click "+ Explore & Download Repositories"
   - Search for "Sol-Ark Cloud"
   - Click "Download"
   - Select the latest version
   - Click "Download" to confirm

4. **Restart Home Assistant**
   - Go to Settings → System → Restart
   - Wait for restart to complete (30-60 seconds)

### Manual Installation

1. Download the integration from GitHub
2. Copy the `custom_components/solark_cloud` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## ⚙️ Configuration

### Finding Your Plant ID

1. Log into [MySolArk Portal](https://www.mysolark.com)
2. Navigate to your plant dashboard
3. Look at the URL: `https://www.mysolark.com/plant/detail/12345`
4. The Plant ID is the number at the end (e.g., `12345`)

### Adding the Integration

1. **Navigate to Integrations**
   - Settings → Devices & Services
   - Click "+ Add Integration"

2. **Search for Sol-Ark**
   - Type "Sol-Ark Cloud" in the search box
   - Click on the integration

3. **Fill in Configuration**
   - **Email**: Your MySolArk account email
   - **Password**: Your MySolArk account password
   - **Plant ID**: The number from your MySolArk URL
   - **Base URL** (optional): Default is `https://api.solarkcloud.com`
   - **Auth Mode** (optional): Default is "Auto" (recommended)
   - **Update Interval** (optional): Default is 120 seconds

4. **Submit**
   - The integration will test the connection
   - If successful, sensors will be created automatically

## 🔧 Updating Settings

Change settings without removing the integration:

1. Settings → Devices & Services
2. Find Sol-Ark Cloud integration
3. Click the three-dot menu (⋮) → Configure
4. Update:
   - Base URL
   - Authentication Mode
   - Update Interval

*Note: To change email, password, or Plant ID, you must remove and re-add the integration.*

## 📊 Available Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| `sensor.sol_ark_pv_power` | W | Solar panel power production |
| `sensor.sol_ark_load_power` | W | Current load consumption |
| `sensor.sol_ark_grid_import_power` | W | Power imported from grid |
| `sensor.sol_ark_grid_export_power` | W | Power exported to grid |
| `sensor.sol_ark_battery_power` | W | Battery charge/discharge (negative = charging) |
| `sensor.sol_ark_battery_state_of_charge` | % | Battery level |
| `sensor.sol_ark_energy_today` | kWh | Total energy produced today |
| `sensor.sol_ark_last_error` | - | Last system error (diagnostics) |

## 🔍 Troubleshooting

### Common Error Messages

#### "Cannot Connect to Sol-Ark Cloud"
**Solutions:**
- Check your internet connection
- Try alternative Base URL: `https://www.mysolark.com`
- Verify firewall allows HTTPS connections
- Check if Sol-Ark servers are accessible

#### "Authentication Failed"
**Solutions:**
- Verify email and password at [www.mysolark.com](https://www.mysolark.com)
- Check for typos in credentials
- Wait 15-30 minutes if account was locked
- Try changing Auth Mode to "Legacy"

#### "Invalid Plant ID"
**Solutions:**
- Verify Plant ID from MySolArk URL
- Ensure you have permission to view this plant
- Check that plant is active in your account

#### "Rate Limit Exceeded"
**Solutions:**
- Increase Update Interval to 180-300 seconds
- Check for duplicate integrations
- Wait 5-15 minutes before retrying

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.solark_cloud: debug
```

Then restart Home Assistant and check: Settings → System → Logs

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/discussions)
- **Community**: [Home Assistant Community Forum](https://community.home-assistant.io)

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by Sol-Ark. Use at your own risk.

## 🙏 Credits

- Developed with assistance from AI tools
- Maintained by [@HammondAutomationHub](https://github.com/HammondAutomationHub)
- Based on Sol-Ark community projects

## 📝 Changelog

### Version 2.0.0
- Enhanced error handling with specific exception classes
- User-friendly error messages with troubleshooting guidance
- Improved authentication with systematic mode fallback
- Better API response parsing for multiple formats
- Timeout protection on all API calls
- Comprehensive debug logging
- Options flow validation
- Support for rate limit detection

### Version 1.0.0
- Initial release
