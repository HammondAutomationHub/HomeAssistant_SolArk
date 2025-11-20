# Sol-Ark Cloud Integration - Project Structure

## Directory Layout

```
solark_cloud_integration/
├── custom_components/
│   └── solark_cloud/              # Main integration package
│       ├── __init__.py            # Integration initialization and setup
│       ├── api.py                 # Sol-Ark Cloud API client
│       ├── config_flow.py         # UI configuration flow
│       ├── const.py               # Constants and configuration
│       ├── manifest.json          # Integration metadata
│       ├── sensor.py              # Sensor platform implementation
│       ├── strings.json           # UI strings (legacy)
│       └── translations/          # Localization files
│           └── en.json            # English translations
│
├── .gitignore                     # Git ignore rules
├── CONFIGURATION.md               # Detailed configuration guide
├── INSTALLATION.md                # Step-by-step installation guide
├── LICENSE                        # MIT License
├── README.md                      # Main documentation
├── hacs.json                      # HACS integration manifest
└── package.sh                     # Build/packaging script
```

## File Descriptions

### Core Integration Files

#### `__init__.py`
- Entry point for the integration
- Handles setup and teardown
- Creates DataUpdateCoordinator for periodic updates
- Manages integration lifecycle
- Sets up platforms (sensors)

**Key Functions**:
- `async_setup_entry()` - Initialize integration
- `async_unload_entry()` - Clean up integration
- `async_reload_entry()` - Reload when options change

#### `api.py`
- Sol-Ark Cloud API client implementation
- Handles authentication and token management
- Makes HTTP requests to Sol-Ark endpoints
- Parses API responses into sensor data
- Implements retry logic and error handling

**Key Classes**:
- `SolArkCloudAPI` - Main API client
- `SolArkCloudAPIError` - Custom exception

**Key Methods**:
- `login()` - Authenticate with Sol-Ark
- `get_plant_data()` - Fetch plant information
- `parse_plant_data()` - Convert API data to sensor values
- `test_connection()` - Verify connectivity

#### `config_flow.py`
- UI configuration flow implementation
- Handles initial setup wizard
- Implements options flow for updating settings
- Validates user input
- Creates config entries

**Key Classes**:
- `SolArkCloudConfigFlow` - Main configuration flow
- `SolArkCloudOptionsFlow` - Options update flow

**Key Methods**:
- `async_step_user()` - Initial setup
- `async_step_init()` - Options update
- `validate_input()` - Credential validation

#### `const.py`
- Centralized constants and defaults
- Configuration key definitions
- Sensor type definitions with metadata
- API endpoint paths
- Default values and limits

**Key Constants**:
- `DOMAIN` - Integration domain name
- `SENSOR_TYPES` - All sensor definitions
- `DEFAULT_*` - Default configuration values
- `*_OPTIONS` - Dropdown menu options

#### `sensor.py`
- Sensor platform implementation
- Creates and manages sensor entities
- Updates sensor states from coordinator
- Provides device information
- Handles state attributes

**Key Classes**:
- `SolArkCloudSensor` - Individual sensor entity

**Key Methods**:
- `async_setup_entry()` - Create sensor entities
- `native_value` - Current sensor value
- `extra_state_attributes` - Additional attributes

#### `manifest.json`
- Integration metadata for Home Assistant
- Declares dependencies and requirements
- Specifies integration type and capabilities
- Version information
- Links to documentation and issues

#### `strings.json` & `translations/en.json`
- UI text strings for configuration flow
- Error messages
- Field labels and descriptions
- Help text
- Localization support

### Documentation Files

#### `README.md`
- Main documentation
- Feature overview
- Installation instructions
- Configuration guide
- Usage examples
- Troubleshooting
- API information

#### `INSTALLATION.md`
- Detailed step-by-step installation
- Prerequisites
- HACS and manual installation
- Finding Plant ID
- Configuration walkthrough
- Troubleshooting common installation issues

#### `CONFIGURATION.md`
- Comprehensive configuration guide
- Explanation of all parameters
- Optimization tips
- Common scenarios
- Best practices
- Advanced settings

### Support Files

#### `hacs.json`
- HACS (Home Assistant Community Store) manifest
- Enables HACS installation
- Specifies integration metadata
- Minimum Home Assistant version

#### `.gitignore`
- Git ignore patterns
- Excludes Python cache files
- Excludes IDE files
- Excludes sensitive data

#### `LICENSE`
- MIT License
- Usage terms and conditions
- Copyright information

#### `package.sh`
- Build and packaging script
- Creates distribution zip files
- Generates HACS-compatible package
- Automates release process

## Integration Flow

### Installation Flow

```
User adds integration
    ↓
config_flow.py: async_step_user()
    ↓
Collect credentials (email, password, plant_id)
    ↓
validate_input() - Test connection
    ↓
Create config entry
    ↓
__init__.py: async_setup_entry()
    ↓
Initialize API client
    ↓
Create DataUpdateCoordinator
    ↓
Fetch initial data
    ↓
sensor.py: async_setup_entry()
    ↓
Create sensor entities
    ↓
Integration ready!
```

### Update Flow

```
Coordinator timer triggers
    ↓
__init__.py: async_update_data()
    ↓
api.py: get_plant_data()
    ↓
Authenticate if needed
    ↓
Fetch plant data from API
    ↓
api.py: parse_plant_data()
    ↓
Convert to sensor values
    ↓
Update coordinator data
    ↓
sensor.py: native_value updates
    ↓
Sensors show new values
```

### Options Flow

```
User clicks Configure
    ↓
config_flow.py: async_step_init()
    ↓
Show current settings
    ↓
User updates values
    ↓
Validate if needed
    ↓
Update config entry
    ↓
__init__.py: async_reload_entry()
    ↓
Unload integration
    ↓
Reload with new settings
```

## Key Design Decisions

### 1. DataUpdateCoordinator
- Centralized data fetching
- Automatic retry on failure
- Efficient updates across all sensors
- Built-in error handling

### 2. Config Flow
- Full UI configuration (no YAML)
- Input validation before saving
- Options flow for easy updates
- Prevents duplicate entries

### 3. API Client
- Async/await for non-blocking operations
- Session management with context manager
- Automatic token refresh
- Multiple auth mode support
- Graceful error handling

### 4. Sensor Platform
- Inherits from CoordinatorEntity
- Automatic updates when coordinator refreshes
- Proper device class and state class
- Rich state attributes
- Grouped by device

### 5. Error Handling
- Custom exception types
- Meaningful error messages
- Graceful degradation
- Detailed logging

## Extension Points

### Adding New Sensors

1. Add sensor definition to `const.py`:
```python
SENSOR_TYPES = {
    "new_sensor": {
        "name": "New Sensor",
        "unit": "unit",
        "icon": "mdi:icon",
        "device_class": "class",
        "state_class": "measurement"
    }
}
```

2. Update `api.py` parse_plant_data():
```python
sensors["new_sensor"] = float(data.get("apiField", 0))
```

3. Sensors automatically created in `sensor.py`

### Adding New Configuration Options

1. Add constant to `const.py`:
```python
CONF_NEW_OPTION = "new_option"
DEFAULT_NEW_OPTION = "default_value"
```

2. Add to config flow schema in `config_flow.py`
3. Add translation strings to `translations/en.json`
4. Use in API client or coordinator

### Supporting Additional Languages

1. Create new translation file: `translations/xx.json`
2. Copy structure from `en.json`
3. Translate all strings
4. File automatically detected by Home Assistant

## Development Workflow

### Testing Locally

1. Copy `custom_components/solark_cloud` to HA config
2. Restart Home Assistant
3. Check logs for errors
4. Test configuration flow
5. Verify sensors update

### Making Changes

1. Edit relevant files
2. Restart Home Assistant to reload
3. Test changes
4. Check logs for issues
5. Update version in `manifest.json`

### Creating Release

1. Update version in `manifest.json`
2. Update `CHANGELOG.md` (if created)
3. Run `./package.sh` to create distribution files
4. Create GitHub release with zip files
5. Tag with version number

## Dependencies

### Python Built-in
- `logging` - Logging functionality
- `datetime` - Time handling
- `typing` - Type hints
- `asyncio` - Async support

### Home Assistant
- `homeassistant.core` - Core functionality
- `homeassistant.config_entries` - Config flow
- `homeassistant.helpers` - Helper utilities
- `homeassistant.components.sensor` - Sensor platform

### External (None Required)
- Uses built-in `aiohttp` from Home Assistant
- No additional pip packages needed
- All dependencies bundled with HA

## Security Considerations

1. **Credentials**: Stored encrypted by Home Assistant
2. **API Token**: Kept in memory, never persisted
3. **HTTPS**: All API communication encrypted
4. **Input Validation**: All user input validated
5. **Error Messages**: Don't expose sensitive data

## Performance Characteristics

- **Memory**: ~5MB per integration instance
- **CPU**: Negligible except during updates
- **Network**: ~1KB per update
- **Update Time**: 1-3 seconds per cycle
- **Startup Time**: 3-5 seconds

## Maintenance

### Regular Updates
- Monitor Home Assistant API changes
- Update dependencies if needed
- Test with new HA versions
- Address user-reported issues

### Common Maintenance Tasks
- Update API endpoints if Sol-Ark changes
- Add new sensor types as API expands
- Improve error handling
- Optimize update intervals
- Add new configuration options

## Support and Community

- **Issues**: GitHub Issues tracker
- **Discussions**: GitHub Discussions
- **Pull Requests**: Welcome with tests
- **Documentation**: Keep README updated

---

This structure follows Home Assistant best practices and provides a solid foundation for a production-quality custom integration.
