# WhoRang AI Doorbell Integration

Transform your doorbell into an intelligent visitor identification system with advanced face recognition, multi-provider AI analysis, and comprehensive visitor insights.

## ✨ Features

- 🧠 **Multi-Provider AI Intelligence** - OpenAI, Claude, Gemini, Google Cloud Vision, Ollama
- 👤 **Advanced Face Recognition** - Identify and track recurring visitors automatically  
- 📱 **Real-time Updates** - WebSocket-powered live notifications
- 📊 **Comprehensive Analytics** - Track AI usage, costs, and visitor patterns
- 🔒 **Privacy-First Design** - Self-hosted solution that keeps your data secure
- ⚡ **19+ Entities** - Complete integration across sensors, cameras, controls

## 🏠 Entities Provided

### Sensors (9)
- Latest Visitor information
- Daily/Weekly/Monthly visitor counts  
- AI cost tracking and usage statistics
- System status and health monitoring

### Binary Sensors (5)
- Doorbell ring detection
- Motion detection
- Known visitor presence
- System connectivity status

### Controls (5)
- AI Provider selection (OpenAI, Claude, Gemini, etc.)
- Manual analysis triggers
- Data refresh controls
- System testing functions

### Camera (1)
- Latest doorbell image with auto-updates

## ⚠️ Prerequisites

**This integration requires the WhoRang backend service to be running.**

### Installation Options:

1. **Home Assistant Add-on** (Recommended for HAOS/Supervised)
   - Install the [WhoRang Add-on](https://github.com/Beast12/whorang-addon)
   - Provides complete backend service with web UI

2. **Docker Deployment** (For Container/Core installations)
   - Use provided Docker Compose configuration
   - Standalone container deployment

3. **Manual Installation** (Advanced users)
   - Build and run WhoRang backend manually
   - Custom deployment configurations

## 🚀 Quick Start

1. **Install Backend Service** (choose one option above)
2. **Install this Integration** via HACS
3. **Configure Integration** in Home Assistant UI
4. **Add Entities** to your dashboard
5. **Set up Automations** for notifications

## 📖 Documentation

- [Complete Installation Guide](https://github.com/Beast12/whorang-integration/blob/main/docs/installation/hacs-installation.md)
- [Configuration Options](https://github.com/Beast12/whorang-integration/blob/main/docs/configuration/initial-setup.md)
- [Automation Examples](https://github.com/Beast12/whorang-integration/blob/main/docs/automation/basic-automations.md)
- [Troubleshooting](https://github.com/Beast12/whorang-integration/blob/main/docs/troubleshooting/common-issues.md)

## 🔧 Technical Details

- **Minimum HA Version**: 2023.1.0
- **IoT Class**: Local Push (WebSocket + API)
- **Configuration**: UI-based config flow
- **Dependencies**: aiohttp, websockets
- **Platforms**: All major HA installation types

## 💡 Automation Examples

```yaml
# Notify on unknown visitor
automation:
  - alias: "Unknown Visitor Alert"
    trigger:
      platform: state
      entity_id: binary_sensor.whorang_doorbell
      to: "on"
    condition:
      condition: template
      value_template: "{{ state_attr('sensor.whorang_latest_visitor', 'face_recognized') == false }}"
    action:
      service: notify.mobile_app
      data:
        title: "Unknown Visitor at Door"
        message: "{{ state_attr('sensor.whorang_latest_visitor', 'ai_analysis') }}"
        data:
          image: "{{ state_attr('sensor.whorang_latest_visitor', 'image_url') }}"
```

## 🆘 Support

- [GitHub Issues](https://github.com/Beast12/whorang-integration/issues)
- [Home Assistant Community](https://community.home-assistant.io/)
- [Documentation](https://github.com/Beast12/whorang-integration/blob/main/README.md)

Made with ❤️ for the Home Assistant community
