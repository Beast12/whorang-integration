# HACS Installation Guide

This guide walks you through installing the WhoRang AI Doorbell Integration via HACS (Home Assistant Community Store).

## Prerequisites

### 1. HACS Installation
HACS must be installed in your Home Assistant instance. If you haven't installed HACS yet:

1. Visit the [HACS Installation Guide](https://hacs.xyz/docs/setup/download)
2. Follow the installation instructions for your Home Assistant setup
3. Restart Home Assistant after HACS installation
4. Complete the HACS onboarding process

### 2. WhoRang Backend Service
**Critical**: This integration requires the WhoRang backend service to be running. Choose your installation method:

#### Option A: Home Assistant Add-on (Recommended)
**Best for**: Home Assistant OS and Supervised installations

1. **Add Repository**:
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click the three dots menu (⋮) → **Repositories**
   - Add: `https://github.com/Beast12/whorang-addon`
   - Click **Add** → **Close**

2. **Install Add-on**:
   - Find "WhoRang AI Doorbell Backend" in the add-on store
   - Click **Install** (this may take several minutes)
   - Configure the add-on options if needed
   - Click **Start**
   - Enable **Start on boot** and **Watchdog**

3. **Verify Installation**:
   - Check the add-on logs for successful startup
   - Note the add-on's IP and port (usually `homeassistant.local:3001`)

#### Option B: Docker Deployment
**Best for**: Home Assistant Container and Core installations

1. **Download Docker Compose**:
   ```bash
   wget https://raw.githubusercontent.com/Beast12/whorang-addon/main/docker-compose.yml
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Start Service**:
   ```bash
   docker-compose up -d
   ```

4. **Verify Installation**:
   ```bash
   docker-compose logs whorang
   ```

#### Option C: Manual Installation
**Best for**: Advanced users and custom setups

See the [WhoRang Add-on repository](https://github.com/Beast12/whorang-addon) for detailed manual installation instructions.

## HACS Installation Steps

### Step 1: Add Custom Repository (If Not in Default Store)

1. **Open HACS**:
   - Go to **HACS** in your Home Assistant sidebar
   - If you don't see HACS, restart Home Assistant

2. **Add Custom Repository**:
   - Click **Integrations**
   - Click the three dots menu (⋮) → **Custom repositories**
   - Add repository URL: `https://github.com/Beast12/whorang-integration`
   - Select category: **Integration**
   - Click **Add**

### Step 2: Install Integration

1. **Search for Integration**:
   - In HACS → **Integrations**
   - Click **Explore & Download Repositories**
   - Search for "WhoRang AI Doorbell"

2. **Download Integration**:
   - Click on "WhoRang AI Doorbell Integration"
   - Review the information and documentation links
   - Click **Download**
   - Select the latest version
   - Click **Download** again

3. **Restart Home Assistant**:
   - Go to **Settings** → **System** → **Restart**
   - Wait for Home Assistant to fully restart

### Step 3: Add Integration

1. **Add Integration**:
   - Go to **Settings** → **Devices & Services**
   - Click **Add Integration** (+ button)
   - Search for "WhoRang AI Doorbell"
   - Click on the integration

2. **Configure Connection**:
   - **Host**: Enter your WhoRang backend host
     - Add-on users: `homeassistant.local` or `localhost`
     - Docker users: Your Docker host IP
     - Manual users: Your backend server IP
   - **Port**: Enter the port (default: `3001`)
   - **Use SSL**: Enable if your backend uses HTTPS
   - **Verify SSL**: Enable for production (disable for self-signed certificates)
   - **API Key**: Leave blank unless you configured authentication

3. **Test Connection**:
   - Click **Submit**
   - The integration will test the connection
   - If successful, you'll see a success message

### Step 4: Configure AI Providers (Optional)

1. **Access Options**:
   - Go to **Settings** → **Devices & Services**
   - Find "WhoRang AI Doorbell" and click **Configure**

2. **Select AI Providers**:
   - Choose "AI Providers" from the menu
   - Configure API keys for desired providers:

#### OpenAI Configuration
- **API Key**: Your OpenAI API key (starts with `sk-`)
- **Models**: GPT-4o, GPT-4o-mini, GPT-4-turbo
- **Cost**: ~$0.01-0.03 per analysis

#### Claude Configuration
- **API Key**: Your Anthropic API key (starts with `sk-ant-`)
- **Models**: Claude-3.5-Sonnet, Claude-3-Haiku
- **Cost**: ~$0.01-0.02 per analysis

#### Gemini Configuration
- **API Key**: Your Google AI API key (starts with `AI`)
- **Models**: Gemini-1.5-Pro, Gemini-1.5-Flash
- **Cost**: ~$0.005-0.015 per analysis

#### Google Cloud Vision
- **API Key**: Your Google Cloud API key
- **Models**: Vision API models
- **Cost**: ~$0.001-0.005 per analysis

#### Local (Ollama)
- **No API Key Required**: Uses local Ollama installation
- **Models**: Any vision-capable model (llava, bakllava, etc.)
- **Cost**: Free (uses local compute)

3. **Validate Configuration**:
   - The integration will test each API key
   - Invalid keys will show error messages
   - Valid keys will be saved securely

## Verification

### Check Entities
After successful installation, verify these entities appear:

#### Sensors
- `sensor.whorang_latest_visitor`
- `sensor.whorang_visitor_count_today`
- `sensor.whorang_visitor_count_week`
- `sensor.whorang_visitor_count_month`
- `sensor.whorang_system_status`
- `sensor.whorang_ai_provider_active`
- `sensor.whorang_ai_cost_today`
- `sensor.whorang_ai_response_time`
- `sensor.whorang_known_faces_count`

#### Binary Sensors
- `binary_sensor.whorang_doorbell`
- `binary_sensor.whorang_motion`
- `binary_sensor.whorang_known_visitor`
- `binary_sensor.whorang_system_online`
- `binary_sensor.whorang_ai_processing`

#### Camera
- `camera.whorang_latest_image`

#### Controls
- `select.whorang_ai_provider`
- `select.whorang_ai_model`
- `button.whorang_trigger_analysis`
- `button.whorang_test_webhook`
- `button.whorang_refresh_data`

### Test Functionality

1. **Check System Status**:
   - `sensor.whorang_system_status` should show "Online"
   - `binary_sensor.whorang_system_online` should be "On"

2. **Test AI Provider**:
   - Use `button.whorang_trigger_analysis` to test AI analysis
   - Check `sensor.whorang_ai_response_time` for response

3. **Verify WebSocket**:
   - Real-time updates should work without manual refresh
   - Check integration logs for WebSocket connection status

## Troubleshooting

### Common Installation Issues

#### Integration Not Found in HACS
- Ensure you added the custom repository correctly
- Check the repository URL is exact: `https://github.com/Beast12/whorang-integration`
- Refresh HACS and try searching again

#### Connection Failed During Setup
- Verify WhoRang backend is running and accessible
- Check host and port configuration
- Test connectivity: `curl http://your-host:3001/api/health`
- Review backend logs for errors

#### Entities Not Appearing
- Restart Home Assistant after installation
- Check **Settings** → **Devices & Services** → **Entities** for disabled entities
- Review integration logs in **Settings** → **System** → **Logs**

#### WebSocket Connection Issues
- Disable WebSocket in integration options as temporary workaround
- Check firewall settings for WebSocket connections
- Verify backend WebSocket endpoint is accessible

### Getting Help

If you encounter issues:

1. **Check Logs**:
   - **Settings** → **System** → **Logs**
   - Look for `whorang` related errors

2. **Review Documentation**:
   - [Configuration Guide](../configuration/initial-setup.md)
   - [Troubleshooting Guide](../troubleshooting/common-issues.md)

3. **Community Support**:
   - [GitHub Issues](https://github.com/Beast12/whorang-integration/issues)
   - [Home Assistant Community](https://community.home-assistant.io/)

## Next Steps

After successful installation:

1. **[Configure Integration](../configuration/initial-setup.md)** - Detailed configuration options
2. **[Set Up Automations](../automation/basic-automations.md)** - Essential automation examples
3. **[Create Dashboard](../usage/dashboard-examples.md)** - Dashboard configuration examples
4. **[Explore Services](../usage/services-reference.md)** - Available services and API

## Updates

### Automatic Updates via HACS
- HACS will notify you of new versions
- Click **Update** when available
- Restart Home Assistant after updates

### Manual Updates
- Download new version from HACS
- Restart Home Assistant
- Check changelog for breaking changes

### Backend Updates
- Add-on users: Update via Add-on Store
- Docker users: Pull new image and restart
- Manual users: Follow update instructions in add-on repository

---

**Need Help?** Check our [troubleshooting guide](../troubleshooting/common-issues.md) or [open an issue](https://github.com/Beast12/whorang-integration/issues).
