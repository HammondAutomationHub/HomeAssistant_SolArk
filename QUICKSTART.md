# Sol-Ark Cloud Integration - Quick Start

Get up and running in 5 minutes!

## What You Need

- [ ] Home Assistant installed and running
- [ ] MySolArk account (email & password)
- [ ] Your Sol-Ark Plant ID

## Step 1: Get Your Plant ID (2 minutes)

1. Open https://www.mysolark.com in your browser
2. Log in with your MySolArk credentials
3. Look at the URL in the address bar
4. Copy the number at the end - that's your Plant ID!

Example: `https://www.mysolark.com/plant/detail/12345` → Your Plant ID is **12345**

## Step 2: Install Integration (2 minutes)

### Via HACS (Easiest)

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click ⋮ menu → Custom repositories
4. Add: `https://github.com/HammondAutomationHub/HomeAssistant_SolArk`
5. Category: Integration
6. Search "Sol-Ark Cloud" and download
7. Restart Home Assistant

### Manual Install

1. Download this repository
2. Copy `custom_components/solark_cloud` to `<config>/custom_components/`
3. Restart Home Assistant

## Step 3: Add Integration (1 minute)

1. Settings → Devices & Services
2. Click + Add Integration
3. Search "Sol-Ark Cloud"
4. Enter your info:
   - **Email**: Your MySolArk email
   - **Password**: Your MySolArk password
   - **Plant ID**: The number from Step 1
5. Leave other settings as default
6. Click Submit

**That's it!** You should see "Success!" if everything worked.

## Step 4: Check Your Sensors

Go to Developer Tools → States and search for "sol_ark"

You should see 8 new sensors:
- ✅ PV Power
- ✅ Load Power
- ✅ Grid Import Power
- ✅ Grid Export Power
- ✅ Battery Power
- ✅ Battery State of Charge
- ✅ Energy Today
- ✅ Last Error

## Quick Dashboard Setup

Add a simple card to see your solar data:

1. Go to your Overview dashboard
2. Click Edit Dashboard
3. Add Card → Entities Card
4. Select these sensors:
   - `sensor.sol_ark_pv_power`
   - `sensor.sol_ark_battery_state_of_charge`
   - `sensor.sol_ark_load_power`
5. Save!

## Quick Automation Example

Get notified when battery is low:

```yaml
alias: Battery Low Alert
trigger:
  - platform: numeric_state
    entity_id: sensor.sol_ark_battery_state_of_charge
    below: 20
action:
  - service: notify.mobile_app
    data:
      message: "Battery at {{ states('sensor.sol_ark_battery_state_of_charge') }}%"
```

## Troubleshooting

### Can't connect?

1. Double-check your email and password
2. Verify Plant ID is correct
3. Try again - sometimes first attempt fails

### Still not working?

1. Try these settings:
   - Base URL: `https://www.mysolark.com`
   - Auth Mode: `Legacy`
2. Check Settings → System → Logs for errors

## Next Steps

- 📊 Add to Energy Dashboard (Settings → Energy)
- 🤖 Create automations based on battery level
- 📱 Set up mobile notifications
- 📈 Build custom dashboard cards

## Need More Help?

- **Full Docs**: See README.md
- **Detailed Install**: See INSTALLATION.md
- **Configuration**: See CONFIGURATION.md
- **Issues**: https://github.com/HammondAutomationHub/HomeAssistant_SolArk/issues

---

**Time to complete**: ~5 minutes  
**Difficulty**: Easy  
**Next**: Customize your dashboard and create automations!
