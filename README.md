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
- **Note**: Add-ons are not available for Container/Core installations. Use Docker Compose instead.

**Quick Docker Setup:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  whorang:
    image: ghcr.io/beast12/whorang-backend:latest
    ports:
      - "3001:3001"
    volumes:
      - ./whorang-data:/data
    environment:
      - AI_PROVIDER=local
      - LOG_LEVEL=info
    restart: unless-stopped
```

### ⚙️ Manual Installation
For advanced users and custom setups:
- **Repository**: [WhoRang Add-on](https://github.com/Beast12/whorang-addon) (includes manual build instructions)
- **Benefits**: Full control, custom modifications

## 🆕 New to Home Assistant?

If you're new to Home Assistant, here are some key concepts to understand:

### 🏠 What is Home Assistant?
Home Assistant is an open-source home automation platform that allows you to control and monitor smart devices in your home.

### 🔌 What are Integrations?
Integrations connect Home Assistant to external services or devices. WhoRang is an integration that adds AI-powered doorbell monitoring to your Home Assistant.

### 📊 What are Entities?
Entities are the building blocks of Home Assistant - they represent sensors, switches, cameras, etc. WhoRang creates 19+ entities to monitor your doorbell system.

### 🤖 What are Automations?
Automations allow Home Assistant to automatically perform actions based on triggers. For example, send a notification when someone rings your doorbell.

### 📱 What are Dashboards?
Dashboards are customizable interfaces where you can view and control your entities. WhoRang includes a sophisticated face management dashboard.

**Ready to get started?** Follow the steps below!

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

### 🔍 Sensors (14 entities)
| Entity | Description | Example Value |
|--------|-------------|---------------|
| `sensor.whorang_ai_doorbell_latest_visitor` | Latest visitor information | "Person at door with package" |
| `sensor.whorang_ai_doorbell_visitors_today` | Today's visitor count | 5 |
| `sensor.whorang_ai_doorbell_visitor_count_week` | This week's visitor count | 23 |
| `sensor.whorang_ai_doorbell_visitor_count_month` | This month's visitor count | 87 |
| `sensor.whorang_ai_doorbell_system_status` | System health status | "healthy" |
| `sensor.whorang_ai_doorbell_ai_provider` | Current AI provider | "openai" |
| `sensor.whorang_ai_doorbell_ai_cost_today` | Today's AI processing costs | "$0.15" |
| `sensor.whorang_ai_doorbell_ai_cost_this_month` | This month's AI costs | "$4.23" |
| `sensor.whorang_ai_doorbell_ai_response_time` | Latest AI response time | "1200" (ms) |
| `sensor.whorang_ai_doorbell_known_faces` | Number of known faces | 12 |
| `sensor.whorang_ai_doorbell_unknown_faces` | Unknown faces needing labeling | 3 |
| `sensor.whorang_ai_doorbell_latest_face_detection` | Latest face detection results | "2 faces detected" |
| `sensor.whorang_ai_doorbell_face_gallery` | **Face gallery data with images** | Complex object with face data |
| `sensor.whorang_ai_doorbell_known_persons_gallery` | **Known persons with avatars** | Complex object with person data |

### 🚨 Binary Sensors (5 entities)
| Entity | Description | Device Class |
|--------|-------------|--------------|
| `binary_sensor.whorang_ai_doorbell_doorbell` | Recent doorbell activity | - |
| `binary_sensor.whorang_ai_doorbell_motion` | Motion detection | motion |
| `binary_sensor.whorang_ai_doorbell_known_visitor` | Known visitor detected | occupancy |
| `binary_sensor.whorang_ai_doorbell_system_online` | System connectivity | connectivity |
| `binary_sensor.whorang_ai_doorbell_ai_processing` | AI processing status | - |

### 📷 Camera (1 entity)
| Entity | Description |
|--------|-------------|
| `camera.whorang_ai_doorbell_latest_image` | Latest doorbell camera image |

### 🎛️ Controls (5 entities)
| Entity | Description | Options |
|--------|-------------|---------|
| `select.whorang_ai_doorbell_ai_provider` | AI provider selection | openai, local, claude, gemini, google-cloud-vision |
| `select.whorang_ai_doorbell_ai_model` | AI model selection | Provider-specific models (dynamic) |
| `button.whorang_ai_doorbell_trigger_analysis` | Manually trigger AI analysis | - |
| `button.whorang_ai_doorbell_test_webhook` | Test webhook functionality | - |
| `button.whorang_ai_doorbell_refresh_data` | Force data refresh | - |

### 📍 Device Trackers (Dynamic)
Dynamic device trackers are created for each known person:
- `device_tracker.whorang_ai_doorbell_visitors_[person_name]` - Presence tracking for known visitors

### 🎨 Visual Face Management System
The integration includes **3 sophisticated custom cards** for complete face management:

#### **1. Face Manager Card** - `whorang-face-manager-card`
**Full-featured visual face labeling interface**
- **Interactive Selection**: Click faces to select them (blue border indicates selection)
- **Batch Operations**: Label multiple faces as the same person
- **Progress Tracking**: Visual progress of face labeling completion
- **Quality Indicators**: Face detection quality scores and confidence levels
- **Smart Image Loading**: Automatic backend URL detection and fallback
- **Responsive Design**: Adapts to different screen sizes

#### **2. Face Manager Simple Card** - `whorang-face-manager-simple-card`
**Lightweight version for basic face labeling**
- **Simplified Interface**: Clean, minimal design
- **Essential Features**: Face selection and labeling
- **Lower Resource Usage**: Ideal for slower devices
- **Quick Setup**: Minimal configuration required

#### **3. Known Persons Card** - `whorang-known-persons-card`
**Gallery of known persons with avatars and statistics**
- **Person Avatars**: Visual representation of known persons
- **Statistics Display**: Face counts, last seen dates, recognition stats
- **Person Management**: Edit, delete, and manage known persons
- **Face Viewing**: View all faces associated with each person
- **Confidence Indicators**: Recognition confidence levels

See the complete dashboard configuration in [`examples/dashboard.yaml`](examples/dashboard.yaml).

## 🎯 Essential Automations

### Doorbell Notification
```yaml
automation:
  - alias: "Doorbell Pressed"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_ai_doorbell_doorbell
        to: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🔔 Doorbell"
          message: "{{ states('sensor.whorang_ai_doorbell_latest_visitor') }}"
          data:
            image: "/api/camera_proxy/camera.whorang_ai_doorbell_latest_image"
```

### Known Visitor Welcome
```yaml
automation:
  - alias: "Welcome Known Visitor"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_ai_doorbell_known_visitor
        to: "on"
    action:
      - service: tts.google_translate_say
        data:
          entity_id: media_player.living_room_speaker
          message: >
            Welcome home, {{ state_attr('binary_sensor.whorang_ai_doorbell_known_visitor', 'person_name') }}!
```

### Security Alert for Unknown Visitors
```yaml
automation:
  - alias: "Unknown Visitor Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_ai_doorbell_doorbell
        to: "on"
    condition:
      - condition: state
        entity_id: binary_sensor.whorang_ai_doorbell_known_visitor
        state: "off"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🚨 Unknown Visitor"
          message: "{{ states('sensor.whorang_ai_doorbell_latest_visitor') }}"
          data:
            image: "/api/camera_proxy/camera.whorang_ai_doorbell_latest_image"
            actions:
              - action: "trigger_analysis"
                title: "Analyze Visitor"
```

### Unknown Face Detection Alert
```yaml
automation:
  - alias: "Unknown Face Detected"
    trigger:
      - platform: state
        entity_id: sensor.whorang_ai_doorbell_face_gallery
        attribute: total_unknown
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.attributes.total_unknown | int > trigger.from_state.attributes.total_unknown | int }}"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🔍 New Unknown Face"
          message: "{{ state_attr('sensor.whorang_ai_doorbell_face_gallery', 'total_unknown') }} faces need labeling"
          data:
            actions:
              - action: "open_face_manager"
                title: "Label Faces"
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

## 👤 Face Management Services

### `whorang.label_face`
Assign a name to an unknown face for recognition.
```yaml
service: whorang.label_face
data:
  face_id: 8
  person_name: "John Doe"
```

### `whorang.create_person_from_face`
Create a new person and assign the face to them.
```yaml
service: whorang.create_person_from_face
data:
  face_id: 8
  person_name: "Jane Smith"
  description: "Family member"  # Optional
```

### `whorang.get_unknown_faces`
Retrieve and update the list of unknown faces requiring labeling.
```yaml
service: whorang.get_unknown_faces
data:
  limit: 50                    # Optional, default 50
  quality_threshold: 0.6       # Optional, minimum quality score
```

### `whorang.batch_label_faces`
Label multiple faces as the same person (used by visual interface).
```yaml
service: whorang.batch_label_faces
data:
  face_ids: [8, 12, 15]
  person_name: "John Doe"
  create_person: true          # Optional, create person if doesn't exist
```

### `whorang.delete_face`
Delete a detected face from the system.
```yaml
service: whorang.delete_face
data:
  face_id: 8
```

### `whorang.get_face_similarities`
Find similar faces to help with labeling decisions.
```yaml
service: whorang.get_face_similarities
data:
  face_id: 8
  threshold: 0.6               # Optional, similarity threshold
  limit: 10                    # Optional, max results
```

## 🔧 Advanced Services

### `whorang.process_doorbell_event`
Process a complete doorbell event with image and context data.
```yaml
service: whorang.process_doorbell_event
data:
  image_url: "http://192.168.1.100:8123/local/doorbell_snapshot.jpg"
  ai_message: "A person is standing at the front door"  # Optional
  ai_title: "Visitor Detected"                          # Optional
  location: "front_door"                                # Optional
  weather_temp: "{{ state_attr('weather.home', 'temperature') }}"     # Optional
  weather_humidity: "{{ state_attr('weather.home', 'humidity') }}"    # Optional
  weather_condition: "{{ states('weather.home') }}"                   # Optional
```

### `whorang.get_available_models`
Get list of available models for current or specified provider.
```yaml
service: whorang.get_available_models
data:
  provider: "openai"           # Optional, uses current if not specified
```

### `whorang.refresh_ollama_models`
Refresh the list of available Ollama models from the local instance.
```yaml
service: whorang.refresh_ollama_models
```

### `whorang.test_ollama_connection`
Test connection to the Ollama service and get status information.
```yaml
service: whorang.test_ollama_connection
```

### `whorang.test_webhook`
Test webhook functionality by sending a test event.
```yaml
service: whorang.test_webhook
```

## 📱 Complete Dashboard Setup

### Quick Setup
1. Copy the contents of [`examples/dashboard.yaml`](examples/dashboard.yaml)
2. Go to **Settings** → **Dashboards** → **Add Dashboard**
3. Choose **"Take control"** and paste the YAML
4. Update the `whorang_url` to match your backend URL

### Dashboard Features
- **Visual Face Manager**: Interactive face labeling interface
- **System Status**: Real-time system health monitoring  
- **Quick Actions**: One-click operations for common tasks
- **Usage Guide**: Built-in help and instructions
- **Manual Controls**: Fallback controls for advanced users

### Required Custom Cards
The dashboard uses the `whorang-face-manager-card` which is included with the integration.
If you see "Custom element doesn't exist", restart Home Assistant.

### Simple Dashboard Example

```yaml
type: vertical-stack
cards:
  - type: picture-entity
    entity: camera.whorang_ai_doorbell_latest_image
    name: Latest Visitor
    show_state: false
    
  - type: glance
    title: Visitor Statistics
    entities:
      - entity: sensor.whorang_ai_doorbell_visitors_today
        name: Today
      - entity: sensor.whorang_ai_doorbell_visitor_count_week
        name: Week
      - entity: sensor.whorang_ai_doorbell_visitor_count_month
        name: Month
      - entity: sensor.whorang_ai_doorbell_known_faces
        name: Known Faces
        
  - type: entities
    title: System Status
    entities:
      - entity: sensor.whorang_ai_doorbell_system_status
        name: Status
      - entity: binary_sensor.whorang_ai_doorbell_system_online
        name: Online
      - entity: sensor.whorang_ai_doorbell_ai_provider
        name: AI Provider
      - entity: sensor.whorang_ai_doorbell_ai_cost_today
        name: AI Cost Today
        
  - type: entities
    title: Controls
    entities:
      - entity: select.whorang_ai_doorbell_ai_provider
        name: AI Provider
      - entity: select.whorang_ai_doorbell_ai_model
        name: AI Model
      - entity: button.whorang_ai_doorbell_trigger_analysis
        name: Trigger Analysis
      - entity: button.whorang_ai_doorbell_refresh_data
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
- **[Face Management Guide](docs/usage/face-management-guide.md)** - Comprehensive face recognition guide
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
