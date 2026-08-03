# SolArk Cloud Integration - Quick Start Guide

## What You'll Get

After installation, you'll have 9 sensors monitoring your Sol-Ark system:

- `sensor.solark_pv_power` - Solar power generation
- `sensor.solark_battery_power` - Battery charge/discharge
- `sensor.solark_battery_soc` - Battery percentage
- `sensor.solark_grid_power` - Grid import/export (net)
- `sensor.solark_load_power` - Home consumption
- `sensor.solark_grid_import_power` - Power from grid
- `sensor.solark_grid_export_power` - Power to grid
- `sensor.solark_energy_today` - Today's production
- `sensor.solark_energy_total` - Lifetime production

## Installation (5 Steps)

### Step 1: Install via HACS

1. Open Home Assistant
2. Go to **HACS** â†’ **Integrations**
3. Click **â‹®** â†’ **Custom repositories**
4. Add: `https://github.com/HammondAutomationHub/HomeAssistant_SolArk`
5. Category: **Integration**
6. Click **Download** on "SolArk Cloud"
7. **Restart Home Assistant**

### Step 2: Get Your Plant ID

1. Go to [solarkcloud.com](https://www.solarkcloud.com)
2. Log in with your Sol-Ark account
3. Click on your system/plant
4. Look at the URL: `https://www.solarkcloud.com/plants/overview/12345/...`
5. Your Plant ID is the number: `12345`

### Step 3: Add Integration

1. Go to **Settings** â†’ **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search: **SolArk Cloud**
4. Enter:
   - Username: (your Sol-Ark email)
   - Password: (your Sol-Ark password)
   - Plant ID: (from Step 2)
   - Scan Interval: `30` (leave default)
5. Click **SUBMIT**

### Step 4: Verify Sensors Work

1. Go to **Developer Tools** â†’ **States**
2. Search for: `solark`
3. You should see 9 sensors with live data
4. If they show "unavailable", wait 30 seconds for first update

### Step 5: Add Dashboard (Optional)

**Easy Way:**
1. Download `dashboards/solark_flow.yaml` from the GitHub repo
2. Copy all the contents
3. Go to **Settings** â†’ **Dashboards** â†’ **+ ADD DASHBOARD**
4. Name it "SolArk"
5. After creation, click **â‹®** â†’ **Edit Dashboard**
6. Click **â‹®** â†’ **Raw configuration editor**
7. Delete everything and paste the copied YAML
8. Click **SAVE**

**Required:** Install these custom cards first via HACS:
- Mushroom Cards
- ApexCharts Card

Then restart HA and refresh your browser (Ctrl+Shift+R).

## Troubleshooting

### "Authentication Failed"
- Double-check your username and password
- Try logging into solarkcloud.com with same credentials
- Make sure your Plant ID is correct

### "No sensors appearing"
- Restart Home Assistant completely
- Wait 30-60 seconds after restart
- Check **Settings** â†’ **System** â†’ **Logs** for errors

### "Dashboard is blank"
- Make sure you installed Mushroom Cards from HACS
- Make sure you installed ApexCharts Card from HACS
- Restart HA after installing custom cards
- Clear browser cache (Ctrl+Shift+R)

### "Sensors show 'unavailable'"
- Check if solarkcloud.com is working
- Increase Scan Interval to 60 seconds
- Check logs for API errors
- Try removing and re-adding the integration

## Quick Dashboard Test

If the full dashboard doesn't work, test with this simple one:

1. Create new dashboard
2. Add an **Entities Card**
3. Add these entities:
   - sensor.solark_pv_power
   - sensor.solark_battery_soc
   - sensor.solark_load_power

If this works, the issue is with the custom cards, not the integration.

## Getting Help

- **GitHub Issues:** Report bugs at [GitHub Issues](https://github.com/HammondAutomationHub/HomeAssistant_SolArk/issues)
- **Logs:** Check **Settings → System → Logs** (credentials are redacted)
- **Community:** Ask at [Home Assistant Forums](https://community.home-assistant.io/)

## Next Steps

Once working, you can:
- Create automations based on battery level
- Get notifications when exporting to grid
- Track energy production over time
- Build custom dashboards with your data
- Compare solar production vs consumption

Enjoy your Sol-Ark monitoring! ðŸŒžðŸ”‹
