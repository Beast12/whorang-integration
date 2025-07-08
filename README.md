# WhoRang AI Doorbell Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

_Transform your Home Assistant into an intelligent doorbell monitoring system with AI-powered visitor analysis, face recognition, and real-time notifications._

## 🚨 Important: Backend Required

**This integration requires the WhoRang backend service to be running.** Choose your installation method:

### 🏠 Home Assistant Add-on (Recommended)
For Home Assistant OS and Supervised installations:
- **Repository**: [WhoRang Add-on](https://github.com/Beast12/whorang-addon)
- **Installation**: Add-on Store → Add Repository → Install WhoRang
- **Benefits**: Automatic updates, integrated management, web UI

### 🐳 Docker Deployment
For Home Assistant Container and Core installations:
- **Repository**: [WhoRang Add-on](https://github.com/Beast12/whorang-addon) (includes Docker instructions)
- **Benefits**: Standalone deployment, custom configurations

### ⚙️ Manual Installation
For advanced users and custom setups:
- **Repository**: [WhoRang Add-on](https://github.com/Beast12/whorang-addon) (includes manual build instructions)
- **Benefits**: Full control, custom modifications

## 🚀 Quick Start

### Step 1: Install Backend
Choose and install the backend service using one of the methods above.

### Step 2: Install Integration

#### Via HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click "Explore & Download Repositories"
4. Search for "WhoRang AI Doorbell"
5. Click "Download"
6. Restart Home Assistant

#### Manual Installation
1. Download the latest release from [releases page][releases]
2. Extract to `custom_components/whorang/` in your HA config directory
3. Restart Home Assistant

### Step 3: Configure Integration
1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "WhoRang AI Doorbell"
3. Enter your WhoRang system details:
   - **Host**: IP address or hostname (e.g., `192.168.1.100` or `homeassistant.local`)
   - **Port**: Port number (default: `3001`)
   - **Use SSL**: Enable if using HTTPS
   - **API Key**: Optional authentication (if configured in backend)

### Step 4: Configure AI Providers (Optional)
1. Go to **Settings** → **Devices & Services** → **WhoRang AI Doorbell** → **Configure**
2. Select "AI Providers" from the menu
3. Enter API keys for desired providers:
   - **OpenAI**: For GPT-4 Vision analysis
   - **Claude**: For Anthropic Claude analysis
   - **Gemini**: For Google Gemini analysis
   - **Google Cloud Vision**: For Google Cloud analysis
   - **Local (Ollama)**: No API key required

## 📊 What You Get

### Sensors (9 entities)
| Entity | Description | Example Value |
|--------|-------------|---------------|
| `sensor.whorang_latest_visitor` | Latest visitor information | "Person at door with package" |
| `sensor.whorang_visitor_count_today` | Today's visitor count | 5 |
| `sensor.whorang_visitor_count_week` | This week's visitor count | 23 |
| `sensor.whorang_visitor_count_month` | This month's visitor count | 87 |
| `sensor.whorang_system_status` | System health status | "Online" |
| `sensor.whorang_ai_provider_active` | Current AI provider | "openai" |
| `sensor.whorang_ai_cost_today` | Today's AI processing costs | "$0.15" |
| `sensor.whorang_ai_response_time` | Latest AI response time | "1.2s" |
| `sensor.whorang_known_faces_count` | Number of known faces | 12 |

### Binary Sensors (5 entities)
| Entity | Description | Device Class |
|--------|-------------|--------------|
| `binary_sensor.whorang_doorbell` | Recent doorbell activity | - |
| `binary_sensor.whorang_motion` | Motion detection | motion |
| `binary_sensor.whorang_known_visitor` | Known visitor detected | occupancy |
| `binary_sensor.whorang_system_online` | System connectivity | connectivity |
| `binary_sensor.whorang_ai_processing` | AI processing status | - |

### Camera (1 entity)
| Entity | Description |
|--------|-------------|
| `camera.whorang_latest_image` | Latest doorbell camera image |

### Controls (5 entities)
| Entity | Description | Options |
|--------|-------------|---------|
| `select.whorang_ai_provider` | AI provider selection | openai, local, claude, gemini, google-cloud-vision |
| `select.whorang_ai_model` | AI model selection | Provider-specific models |
| `button.whorang_trigger_analysis` | Manually trigger AI analysis | - |
| `button.whorang_test_webhook` | Test webhook functionality | - |
| `button.whorang_refresh_data` | Force data refresh | - |

### Device Trackers (Dynamic)
Dynamic device trackers are created for each known person:
- `device_tracker.whorang_visitors_[person_name]` - Presence tracking for known visitors

## 🎯 Essential Automations

### Doorbell Notification
```yaml
automation:
  - alias: "Doorbell Pressed"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_doorbell
        to: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🔔 Doorbell"
          message: "{{ states('sensor.whorang_latest_visitor') }}"
          data:
            image: "/api/camera_proxy/camera.whorang_latest_image"
```

### Known Visitor Welcome
```yaml
automation:
  - alias: "Welcome Known Visitor"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_known_visitor
        to: "on"
    action:
      - service: tts.google_translate_say
        data:
          entity_id: media_player.living_room_speaker
          message: >
            Welcome home, {{ state_attr('binary_sensor.whorang_known_visitor', 'person_name') }}!
```

### Security Alert for Unknown Visitors
```yaml
automation:
  - alias: "Unknown Visitor Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_doorbell
        to: "on"
    condition:
      - condition: state
        entity_id: binary_sensor.whorang_known_visitor
        state: "off"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🚨 Unknown Visitor"
          message: "{{ states('sensor.whorang_latest_visitor') }}"
          data:
            image: "/api/camera_proxy/camera.whorang_latest_image"
            actions:
              - action: "trigger_analysis"
                title: "Analyze Visitor"
```

## 🛠️ Services

### `whorang.trigger_analysis`
Manually trigger AI analysis for a visitor.
```yaml
service: whorang.trigger_analysis
data:
  visitor_id: "optional-visitor-id"  # Uses latest if not specified
```

### `whorang.set_ai_provider`
Change the active AI provider.
```yaml
service: whorang.set_ai_provider
data:
  provider: "openai"  # openai, local, claude, gemini, google-cloud-vision
  api_key: "sk-..."   # Optional, uses stored key if available
```

### `whorang.set_ai_model`
Change the active AI model for the current provider.
```yaml
service: whorang.set_ai_model
data:
  model: "gpt-4o"  # Provider-specific model name
```

### `whorang.add_known_visitor`
Add a new known person for face recognition.
```yaml
service: whorang.add_known_visitor
data:
  name: "John Doe"
  notes: "Neighbor from next door"  # Optional
```

### `whorang.remove_known_visitor`
Remove a known person from face recognition.
```yaml
service: whorang.remove_known_visitor
data:
  person_id: 1
```

### `whorang.export_data`
Export visitor data in specified format.
```yaml
service: whorang.export_data
data:
  start_date: "2024-01-01T00:00:00Z"  # Optional
  end_date: "2024-12-31T23:59:59Z"    # Optional
  format: "json"                       # json or csv
```

## 📱 Dashboard Example

```yaml
type: vertical-stack
cards:
  - type: picture-entity
    entity: camera.whorang_latest_image
    name: Latest Visitor
    show_state: false
    
  - type: glance
    title: Visitor Statistics
    entities:
      - entity: sensor.whorang_visitor_count_today
        name: Today
      - entity: sensor.whorang_visitor_count_week
        name: Week
      - entity: sensor.whorang_visitor_count_month
        name: Month
      - entity: sensor.whorang_known_faces_count
        name: Known Faces
        
  - type: entities
    title: System Status
    entities:
      - entity: sensor.whorang_system_status
        name: Status
      - entity: binary_sensor.whorang_system_online
        name: Online
      - entity: sensor.whorang_ai_provider_active
        name: AI Provider
      - entity: sensor.whorang_ai_cost_today
        name: AI Cost Today
        
  - type: entities
    title: Controls
    entities:
      - entity: select.whorang_ai_provider
        name: AI Provider
      - entity: select.whorang_ai_model
        name: AI Model
      - entity: button.whorang_trigger_analysis
        name: Trigger Analysis
      - entity: button.whorang_refresh_data
        name: Refresh Data
```

## 🔧 Configuration Options

After initial setup, you can configure additional options through the integration's options menu:

- **Update Interval**: How often to poll for updates (10-300 seconds)
- **Enable WebSocket**: Use WebSocket for real-time updates (recommended)
- **Enable Cost Tracking**: Track AI processing costs and usage
- **AI Provider Settings**: Configure API keys and provider preferences

## 📚 Documentation

- **[Installation Guide](docs/installation/hacs-installation.md)** - Detailed installation instructions
- **[Configuration Guide](docs/configuration/initial-setup.md)** - Complete configuration reference
- **[Automation Examples](docs/automation/basic-automations.md)** - 15+ ready-to-use automations
- **[Troubleshooting](docs/troubleshooting/common-issues.md)** - Common issues and solutions
- **[API Reference](docs/usage/services-reference.md)** - Complete service documentation

## 🆘 Troubleshooting

### Common Issues

#### Cannot connect to WhoRang system
1. Verify the host and port are correct
2. Ensure WhoRang backend is running and accessible
3. Check firewall settings
4. Try using IP address instead of hostname

#### WebSocket connection fails
1. Disable WebSocket in integration options
2. Check network connectivity
3. Verify WhoRang WebSocket endpoint is accessible

#### Entities not updating
1. Check system status sensor
2. Verify WebSocket connection
3. Try refreshing data manually using the refresh button

#### AI provider not working
1. Verify API key is correctly configured
2. Check AI provider status in WhoRang web interface
3. Ensure sufficient API credits/quota

For more detailed troubleshooting, see our [comprehensive troubleshooting guide](docs/troubleshooting/common-issues.md).

## 🤝 Support & Community

- **Issues**: [GitHub Issues](https://github.com/Beast12/whorang-integration/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Beast12/whorang-integration/discussions)
- **Community**: [Home Assistant Community](https://community.home-assistant.io/)
- **Documentation**: [Complete Documentation](docs/)

## 🔄 Version Compatibility

| Integration Version | Add-on Version | Notes |
|-------------------|----------------|-------|
| 1.0.x | 1.0.x | Initial HACS release |
| 1.1.x | 1.0.x | Enhanced AI models support |
| 1.1.x | 1.1.x | Recommended pairing |

Always check the [releases page][releases] for the latest compatibility information.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Contributing

Contributions are welcome! Please see the [Contributing Guide](CONTRIBUTING.md) for details.

---

[releases-shield]: https://img.shields.io/github/release/Beast12/whorang-integration.svg?style=for-the-badge
[releases]: https://github.com/Beast12/whorang-integration/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/Beast12/whorang-integration.svg?style=for-the-badge
[commits]: https://github.com/Beast12/whorang-integration/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/Beast12/whorang-integration.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40Beast12-blue.svg?style=for-the-badge
[user_profile]: https://github.com/Beast12
