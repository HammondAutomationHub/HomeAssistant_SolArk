# Sol-Ark Cloud Integration - Configuration Guide

This guide explains all configuration options and how to optimize your Sol-Ark Cloud integration.

## Table of Contents

1. [Initial Configuration](#initial-configuration)
2. [Configuration Parameters](#configuration-parameters)
3. [Advanced Settings](#advanced-settings)
4. [Optimization Tips](#optimization-tips)
5. [Common Scenarios](#common-scenarios)

## Initial Configuration

When you first add the Sol-Ark Cloud integration, you'll be presented with a configuration form. Here's what each field means:

### Required Fields

#### Email Address
- **What it is**: Your MySolArk account email
- **Format**: Standard email (e.g., `user@example.com`)
- **Important**: Must match exactly with your MySolArk login
- **Case sensitive**: No
- **Example**: `john.smith@email.com`

#### Password
- **What it is**: Your MySolArk account password
- **Security**: Stored encrypted in Home Assistant
- **Special characters**: Supported
- **Important**: Use your actual MySolArk password, not an app-specific password

#### Plant ID
- **What it is**: Unique identifier for your Sol-Ark installation
- **Format**: Numeric (e.g., `12345`, `67890`)
- **How to find it**: 
  1. Log into https://www.mysolark.com
  2. Go to your plant dashboard
  3. Look at the URL: `https://www.mysolark.com/plant/detail/YOUR_PLANT_ID`
  4. The number at the end is your Plant ID
- **Example**: If URL is `.../plant/detail/98765`, use `98765`

### Optional Fields (Advanced)

#### Base URL
- **Default**: `https://api.solarkcloud.com`
- **Options**:
  - `https://api.solarkcloud.com` (Primary API endpoint)
  - `https://www.mysolark.com` (Alternative endpoint)
- **When to change**: 
  - If you get connection errors with the default
  - If Sol-Ark support tells you to use a specific endpoint
  - If one endpoint is faster for your location
- **Recommendation**: Start with default, only change if needed

#### Authentication Mode
- **Default**: `Auto`
- **Options**:
  - `Auto` - Tries all methods automatically (recommended)
  - `Strict` - Uses full authentication headers
  - `Legacy` - Uses minimal headers for older systems
  
**Detailed explanation**:

- **Auto Mode**: 
  - Tries Strict first, falls back to Legacy if needed
  - Best for most users
  - Handles API changes automatically

- **Strict Mode**:
  - Uses Origin and Referer headers
  - Most secure method
  - Required by some API versions
  - Use if: You know your API requires these headers

- **Legacy Mode**:
  - Minimal headers
  - Works with older Sol-Ark systems
  - More compatible but less secure
  - Use if: Auto mode fails or you have an older system

#### Update Interval
- **Default**: `120` seconds (2 minutes)
- **Range**: 30 - 3600 seconds (30 seconds to 1 hour)
- **Unit**: Seconds
- **What it does**: How often to fetch new data from Sol-Ark Cloud

**Choosing the right interval**:

| Interval | Use Case | Pros | Cons |
|----------|----------|------|------|
| 30-60s | Real-time monitoring | Fresh data, immediate updates | Higher API load, potential rate limiting |
| 120-180s | Normal use (recommended) | Good balance | Slight delay in updates |
| 300-600s | Low priority, stable systems | Lower API load, battery friendly | Less frequent updates |
| 900-3600s | Archival/historical only | Minimal API impact | Very stale data |

## Advanced Settings

### Updating Configuration After Installation

You can change most settings without removing the integration:

1. Go to **Settings** → **Devices & Services**
2. Find **Sol-Ark Cloud** integration
3. Click **Configure** (or the three-dot menu → Configure)
4. Update settings:
   - Base URL
   - Authentication Mode
   - Update Interval
5. Click **Submit**
6. Changes take effect immediately (next update cycle)

**Note**: You cannot change Username, Password, or Plant ID through the options flow. To change these, you must remove and re-add the integration.

### Multiple Sol-Ark Systems

If you have multiple Sol-Ark installations, you can add multiple instances:

1. Add the integration once for each plant
2. Use different Plant IDs for each
3. Each will create separate sensors with unique IDs
4. Sensors will be grouped by plant in Devices & Services

## Optimization Tips

### For Best Performance

1. **Start Conservative**: Use 120-second interval initially
2. **Monitor Logs**: Check for any errors or warnings
3. **Adjust as Needed**: Decrease interval if you need more frequent updates
4. **Watch API**: If you see rate limiting, increase the interval

### For Battery-Powered Monitoring Systems

If monitoring via battery-powered tablet or device:

1. Use 300-600 second intervals
2. This reduces wake-ups and extends battery life
3. Still provides good visibility into daily patterns

### For High-Frequency Trading/Automation

If you need real-time data for automation:

1. Use 30-60 second intervals
2. Monitor for any API rate limiting
3. Consider caching sensor values for automations
4. Add retry logic to your automations

### Network Optimization

**Slow Connection**:
- Increase interval to 180-300 seconds
- Use Legacy auth mode (fewer headers = smaller packets)
- Consider Base URL closest to your location

**Unreliable Connection**:
- Use Auto auth mode (handles fallback)
- Increase interval to reduce retry frequency
- Enable debug logging to track connection issues

## Common Scenarios

### Scenario 1: Standard Home User

**Goal**: Monitor solar production and battery level

**Recommended Settings**:
- Base URL: `https://api.solarkcloud.com`
- Auth Mode: `Auto`
- Update Interval: `120` seconds

**Why**: Good balance of data freshness and system load

### Scenario 2: Power User / Automation Heavy

**Goal**: Real-time monitoring with automations

**Recommended Settings**:
- Base URL: `https://api.solarkcloud.com`
- Auth Mode: `Auto`
- Update Interval: `60` seconds

**Why**: Provides near real-time data for responsive automations

### Scenario 3: Remote Monitoring / Slow Internet

**Goal**: Monitor from remote location with limited bandwidth

**Recommended Settings**:
- Base URL: `https://www.mysolark.com` (try both to see which is faster)
- Auth Mode: `Legacy`
- Update Interval: `300` seconds

**Why**: Reduces data transfer and handles intermittent connections

### Scenario 4: Energy Dashboard Only

**Goal**: Just want energy statistics, don't need real-time

**Recommended Settings**:
- Base URL: `https://api.solarkcloud.com`
- Auth Mode: `Auto`
- Update Interval: `600` seconds (10 minutes)

**Why**: Sufficient for daily energy tracking, minimal API load

### Scenario 5: Testing / Development

**Goal**: Developing automations or testing

**Recommended Settings**:
- Base URL: `https://api.solarkcloud.com`
- Auth Mode: `Auto`
- Update Interval: `30` seconds
- Enable debug logging

**Why**: Fast feedback loop for testing, detailed logs for debugging

## Troubleshooting Configuration Issues

### Problem: Authentication Fails

**Check**:
1. Email and password are exactly correct
2. MySolArk account is active
3. Try switching auth mode to Legacy
4. Try alternative Base URL

### Problem: Sensors Update Slowly

**Check**:
1. Your configured Update Interval
2. Network latency to Sol-Ark servers
3. Consider decreasing interval

### Problem: Frequent Connection Errors

**Check**:
1. Increase Update Interval to reduce request frequency
2. Switch to Legacy auth mode
3. Try alternative Base URL
4. Check Sol-Ark service status

### Problem: Incorrect Data

**Check**:
1. Verify Plant ID is correct
2. Check MySolArk portal shows same data
3. Wait for next update cycle
4. Check sensor attributes for error messages

## Configuration Best Practices

1. **Start with defaults**: Only change if you have specific needs
2. **Make one change at a time**: Easier to identify what works
3. **Document your settings**: Note what works for your setup
4. **Monitor after changes**: Check logs after changing settings
5. **Be patient**: Allow a few update cycles after changes

## Getting Help

If you're still having configuration issues:

1. Enable debug logging
2. Check Home Assistant logs
3. Note your configuration settings
4. Post in GitHub Issues with:
   - Your configuration (hide credentials!)
   - Log excerpts
   - What you've tried

## Configuration File Reference

For reference, your configuration is stored in:
```
<config>/.storage/core.config_entries
```

**Do not edit this file directly** - always use the UI or Home Assistant services to modify configuration.

## Summary

- **Most users**: Use all defaults except credentials and Plant ID
- **Power users**: Decrease interval to 60s
- **Remote/Slow**: Increase interval to 300s, use Legacy mode
- **Having issues**: Try alternate Base URL and Legacy auth mode
- **Multiple plants**: Add integration multiple times with different Plant IDs

Happy monitoring!
