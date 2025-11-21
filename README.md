# SolArk Cloud Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/HammondAutomationHub/HomeAssistant_SolArk.svg)](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/releases)
[![GitHub issues](https://img.shields.io/github/issues/HammondAutomationHub/HomeAssistant_SolArk.svg)](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/issues)

A Home Assistant custom integration for Sol-Ark inverter systems (12K and other models) that connects to the SolArk Cloud API to retrieve real-time solar system data. This integration provides the same monitoring capabilities you see in the Sol-Ark mobile app and website, bringing that data directly into your Home Assistant instance.

## Features

- **Real-time Monitoring**: Access live data from your Sol-Ark inverter system
- **Cloud-based**: No physical connections required - connects via the official Sol-Ark Cloud API
- **Comprehensive Sensors**: Monitor all critical aspects of your solar system
- **Energy Flow Visualization**: Track power flows between PV, battery, grid, and loads
- **Energy Statistics**: Daily and lifetime energy production tracking
- **Pre-built Dashboards**: Includes beautiful Lovelace dashboard examples
- **Configurable Update Interval**: Customize polling frequency to suit your needs
- **Home Assistant Integration**: Fully integrated with Home Assistant's entity system

## Monitored Data

The integration creates the following sensors:

### Power Sensors
- **PV Power** - Real-time solar panel power generation (W)
- **Battery Power** - Battery charge/discharge power (W, positive = discharging, negative = charging)
- **Grid Power (Net)** - Net grid power (W, positive = importing, negative = exporting)
- **Load Power** - Total home load consumption (W)
- **Grid Import Power** - Power being imported from grid (W)
- **Grid Export Power** - Power being exported to grid (W)

### Battery Sensors
- **Battery SOC** - Battery state of charge (%)

### Energy Sensors
- **Energy Today** - Total energy produced today (kWh)
- **Energy Total** - Lifetime energy production (kWh)

## Requirements

- Home Assistant 2023.5.0 or newer
- A Sol-Ark inverter system (12K, 15K, 8K, 5K models supported)
- An active Sol-Ark Cloud account
- Your Plant ID from the Sol-Ark portal

## Installation

### HACS Installation (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed
2. In HACS, go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/HammondAutomationHub/HomeAssistant_SolArk` as an Integration
6. Click "Download" on the SolArk Cloud integration
7. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/releases)
2. Extract the contents
3. Copy the `custom_components/solark` folder to your Home Assistant's `custom_components` directory
4. If `custom_components` doesn't exist, create it in the same directory as your `configuration.yaml`
5. Restart Home Assistant

## Configuration

### Finding Your Plant ID

1. Log in to your Sol-Ark Cloud account at [mysolark.com](https://www.mysolark.com)
2. Navigate to your plant/system
3. Look in the URL bar - your Plant ID is the numeric value after `/plant/` in the URL
   - Example: `https://www.mysolark.com/plant/12345` → Plant ID is `12345`

### Setting Up the Integration

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for "SolArk Cloud"
4. Enter your credentials:
   - **Username**: Your Sol-Ark Cloud username/email
   - **Password**: Your Sol-Ark Cloud password
   - **Plant ID**: Your Plant ID (see above)
   - **Base URL**: (Optional) Default is `https://www.mysolark.com`
   - **API URL**: (Optional) Default is `https://ecsprod-api-new.solarkcloud.com`
   - **Scan Interval**: (Optional) Update frequency in seconds (default: 30)
5. Click **SUBMIT**

The integration will validate your credentials and connect to your system. Once connected, all sensors will be created automatically.

### Post-Installation Configuration

After installation, you can adjust settings:

1. Go to **Settings** → **Devices & Services**
2. Find "SolArk Cloud" and click **CONFIGURE**
3. Adjust the **Scan Interval** to change update frequency (minimum 10 seconds recommended)

## Dashboard Examples

The integration includes two pre-built dashboard configurations located in the `dashboards/` directory:

### Power Flow Dashboard (`solark_flow.yaml`)

A comprehensive dashboard featuring:
- Real-time power flow indicators with dynamic colors
- Battery state of charge with visual indicators
- Grid import/export status
- 24-hour historical charts for PV, Load, Battery, and Grid
- Energy production statistics

**Required Custom Cards:**
- [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom)
- [ApexCharts Card](https://github.com/RomRider/apexcharts-card)

To use this dashboard:
1. Install the required custom cards via HACS
2. Copy the contents of `dashboards/solark_flow.yaml`
3. In Home Assistant, go to **Settings** → **Dashboards**
4. Create a new dashboard or edit an existing one
5. Add a new view and paste the YAML configuration

### Basic Dashboard (`solark_dashboard.yaml`)

A simpler dashboard with essential monitoring cards.

## Usage Examples

### Automations

Monitor battery level and send notifications:

```yaml
automation:
  - alias: "Low Battery Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.solark_battery_soc
        below: 20
    action:
      - service: notify.mobile_app
        data:
          message: "Battery level is below 20%: {{ states('sensor.solark_battery_soc') }}%"
```

Track excess solar production:

```yaml
automation:
  - alias: "Excess Solar Notification"
    trigger:
      - platform: numeric_state
        entity_id: sensor.solark_grid_export_power
        above: 2000
        for: "00:05:00"
    action:
      - service: notify.mobile_app
        data:
          message: "Exporting {{ states('sensor.solark_grid_export_power') }}W to grid"
```

### Templates

Calculate self-consumption percentage:

```yaml
sensor:
  - platform: template
    sensors:
      solar_self_consumption:
        friendly_name: "Solar Self-Consumption"
        unit_of_measurement: "%"
        value_template: >
          {% set pv = states('sensor.solark_pv_power') | float(0) %}
          {% set export = states('sensor.solark_grid_export_power') | float(0) %}
          {% if pv > 0 %}
            {{ ((pv - export) / pv * 100) | round(1) }}
          {% else %}
            0
          {% endif %}
```

## Troubleshooting

### Integration Won't Connect

1. **Verify Credentials**: Ensure your username and password are correct
2. **Check Plant ID**: Confirm your Plant ID is accurate from the Sol-Ark portal
3. **Review Logs**: Check Home Assistant logs for detailed error messages
   - Go to **Settings** → **System** → **Logs**
   - Look for entries containing `custom_components.solark`

### Sensors Show "Unknown" or "Unavailable"

1. **Check Integration Status**: Verify the integration is loaded in Devices & Services
2. **Increase Scan Interval**: Try increasing the scan interval to 60 seconds to avoid rate limiting
3. **Check API Status**: Verify the Sol-Ark Cloud service is operational
4. **Review Debug Logs**: Check `custom_components/solark/solark_debug.log` for detailed API communication

### Debug Logging

The integration writes detailed debug information to `solark_debug.log` in the integration directory. This file includes:
- API request/response details
- Authentication status
- Data parsing information
- Error messages

Enable debug logging in Home Assistant:

```yaml
logger:
  default: info
  logs:
    custom_components.solark: debug
```

### Common Issues

**Q: Why are my power values different from the Sol-Ark app?**
A: The integration uses the same API endpoints as the mobile app. Minor differences may occur due to timing, but values should be very close. Ensure your scan interval isn't too short.

**Q: Can I control my inverter settings through this integration?**
A: No, this integration is read-only. It monitors your system but does not send control commands to the inverter.

**Q: How often does the data update?**
A: By default, data updates every 30 seconds. You can adjust this in the integration configuration. Be mindful not to set it too low to avoid potential API rate limiting.

## Technical Details

### API Endpoints Used

The integration interacts with the Sol-Ark Cloud API using two main endpoints:

1. **Energy Flow Endpoint** (`/api/v1/plant/energy/{plant_id}/flow`)
   - Provides: PV Power, Battery Power, Grid Power, Load Power, Battery SOC
   - Updated: Per scan interval

2. **Inverter Live Data Endpoint** (`/api/v1/dy/store/{sn}/read`)
   - Provides: Energy Today, Energy Total, detailed inverter metrics
   - Updated: Per scan interval

### Authentication

The integration uses OAuth 2.0 authentication with automatic token refresh. Tokens are managed internally and refreshed automatically when expired.

### Data Update Coordinator

The integration uses Home Assistant's `DataUpdateCoordinator` for efficient polling and data management. All sensors share a single coordinator to minimize API calls.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Clone the repository
2. Create a symbolic link from your Home Assistant's `custom_components` directory to the `custom_components/solark` folder in the repository
3. Restart Home Assistant
4. Enable debug logging (see above)

## Support

- **Issues**: [GitHub Issues](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/discussions)

## License

This project is provided as-is with no warranty. Use at your own risk.

## Acknowledgments

- Thanks to the Home Assistant community for their support and tools
- Sol-Ark for providing cloud API access
- All contributors who have helped improve this integration

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

---

**Note**: This integration is not officially affiliated with or endorsed by Sol-Ark. It is a community-developed tool for Home Assistant users.
