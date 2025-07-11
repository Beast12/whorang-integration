# Initial Setup Configuration Guide

This guide covers the complete configuration process for the WhoRang AI Doorbell Integration after installation.

## Overview

The WhoRang integration uses a two-step configuration process:
1. **Initial Setup**: Connect to your WhoRang backend service
2. **Options Configuration**: Configure AI providers, update intervals, and advanced settings

## Initial Setup Flow

### Step 1: Add Integration

1. **Navigate to Integrations**:
   - Go to **Settings** → **Devices & Services**
   - Click **Add Integration** (+ button)
   - Search for "WhoRang AI Doorbell"

2. **Start Configuration**:
   - Click on "WhoRang AI Doorbell Integration"
   - The setup wizard will begin

### Step 2: Backend Connection Configuration

#### Connection Settings

**Host Configuration**:
- **Host**: The IP address or hostname of your WhoRang backend
  - Add-on users: `homeassistant.local`, `localhost`, or `127.0.0.1`
  - Docker users: Your Docker host IP (e.g., `192.168.1.100`)
  - Remote users: Your server's IP or domain name
  - Examples: `192.168.1.50`, `whorang.local`, `doorbell.example.com`

**Port Configuration**:
- **Port**: The port your WhoRang backend is running on
  - Default: `3001`
  - Add-on users: Usually `3001`
  - Custom installations: Check your configuration

**SSL Configuration**:
- **Use SSL**: Enable if your backend uses HTTPS
  - Add-on with SSL: Enable
  - Local installations: Usually disabled
  - Remote installations: Recommended to enable

- **Verify SSL**: Enable for production environments
  - Production: Always enable
  - Development/Self-signed certificates: Disable
  - Let's Encrypt certificates: Enable

**Authentication**:
- **API Key**: Optional authentication key
  - Leave blank if no authentication configured
  - Enter your API key if backend requires authentication
  - Format: Usually alphanumeric string

#### Connection Examples

**Home Assistant Add-on (Default)**:
```
Host: homeassistant.local
Port: 3001
Use SSL: false
Verify SSL: false
API Key: (leave blank)
```

**Docker on Same Host**:
```
Host: localhost
Port: 3001
Use SSL: false
Verify SSL: false
API Key: (leave blank)
```

**Docker on Different Host**:
```
Host: 192.168.1.100
Port: 3001
Use SSL: false
Verify SSL: false
API Key: (leave blank)
```

**Remote Server with SSL**:
```
Host: doorbell.example.com
Port: 443
Use SSL: true
Verify SSL: true
API Key: your-api-key-here
```

### Step 3: Connection Testing

The integration will automatically test the connection:

1. **HTTP Connectivity**: Tests basic HTTP connection
2. **API Endpoint**: Verifies WhoRang API is responding
3. **WebSocket**: Tests real-time connection capability
4. **Authentication**: Validates API key if provided

**Success Indicators**:
- ✅ "Connection successful" message
- ✅ Integration appears in Devices & Services
- ✅ Entities are created and populated

**Failure Indicators**:
- ❌ "Connection failed" error message
- ❌ Timeout errors
- ❌ Authentication errors

### Step 4: AI Provider Configuration (Optional)

After successful connection, you can configure AI providers:

1. **Access Options**:
   - Go to **Settings** → **Devices & Services**
   - Find "WhoRang AI Doorbell" and click **Configure**
   - Select "AI Providers" from the menu

2. **Provider Configuration**:
   - Configure API keys for desired external providers
   - Configure Ollama host/port for local AI processing
   - Local (Ollama) provider is always available

## Options Configuration

### Accessing Options

1. **Navigate to Integration**:
   - **Settings** → **Devices & Services**
   - Find "WhoRang AI Doorbell"
   - Click **Configure**

2. **Configuration Menu**:
   - **AI Providers**: Configure API keys and provider settings
   - **Update Settings**: Adjust polling intervals and WebSocket settings
   - **Advanced Options**: Additional configuration options

### AI Provider Configuration

#### OpenAI Configuration

**API Key Setup**:
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-`)
4. Enter in WhoRang configuration

**Available Models**:
- **GPT-4o**: Latest multimodal model (recommended)
- **GPT-4o-mini**: Faster, cost-effective option
- **GPT-4-turbo**: Previous generation model

**Cost Estimation**:
- GPT-4o: ~$0.01-0.03 per analysis
- GPT-4o-mini: ~$0.005-0.015 per analysis

**Configuration Example**:
```
API Key: sk-proj-abc123...
Model: gpt-4o
```

#### Claude Configuration

**API Key Setup**:
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Copy the key (starts with `sk-ant-`)
4. Enter in WhoRang configuration

**Available Models**:
- **Claude-3.5-Sonnet**: Best performance (recommended)
- **Claude-3-Haiku**: Faster, cost-effective option

**Cost Estimation**:
- Claude-3.5-Sonnet: ~$0.01-0.02 per analysis
- Claude-3-Haiku: ~$0.005-0.01 per analysis

#### Gemini Configuration

**API Key Setup**:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create an API key
3. Copy the key (starts with `AI`)
4. Enter in WhoRang configuration

**Available Models**:
- **Gemini-1.5-Pro**: Best performance
- **Gemini-1.5-Flash**: Faster option

**Cost Estimation**:
- Gemini-1.5-Pro: ~$0.005-0.015 per analysis
- Gemini-1.5-Flash: ~$0.001-0.005 per analysis

#### Google Cloud Vision

**API Key Setup**:
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Vision API
3. Create service account and API key
4. Enter in WhoRang configuration

**Cost Estimation**:
- ~$0.001-0.005 per analysis

#### Local (Ollama) Configuration

**No API Key Required**: Uses local Ollama installation

**Host/Port Configuration**:
- **Ollama Host**: IP address or hostname of Ollama service
  - Local installation: `localhost` or `127.0.0.1`
  - Remote installation: `192.168.1.200` or `ollama.local`
  - Default: `localhost`
- **Ollama Port**: Port number for Ollama service
  - Default: `11434`
  - Custom installations: Check your Ollama configuration

**Configuration Examples**:

**Local Ollama (Default)**:
```
Ollama Host: localhost
Ollama Port: 11434
```

**Remote Ollama Server**:
```
Ollama Host: 192.168.1.200
Ollama Port: 11434
```

**Custom Port Installation**:
```
Ollama Host: localhost
Ollama Port: 8080
```

**Requirements**:
- Ollama installed and running on specified host/port
- Vision-capable model installed (e.g., `llava`, `bakllava`, `llava-phi3`)
- Network connectivity to Ollama service

**Benefits**:
- No API costs
- Complete privacy
- No internet dependency
- Custom model support

**Connection Testing**:
The integration will test the Ollama connection during configuration and show:
- ✅ "Connected to Ollama at host:port" for successful connections
- ❌ "Failed to connect to Ollama service" for connection issues

### Update Settings Configuration

#### Polling Interval
- **Range**: 10-300 seconds
- **Default**: 30 seconds
- **Recommendation**: 30-60 seconds for most users
- **Lower values**: More responsive but higher resource usage
- **Higher values**: Less responsive but lower resource usage

#### WebSocket Settings
- **Enable WebSocket**: Recommended for real-time updates
- **Benefits**: Instant notifications, no polling delays
- **Disable if**: Network issues or firewall restrictions

#### Cost Tracking
- **Enable Cost Tracking**: Monitor AI usage and costs
- **Benefits**: Budget management, usage analytics
- **Privacy**: All tracking is local, no data sent externally

### Advanced Options

#### SSL Configuration
- **Custom SSL Context**: For advanced SSL setups
- **Certificate Validation**: Custom certificate handling
- **Timeout Settings**: Connection and request timeouts

#### Logging Configuration
- **Debug Logging**: Enable for troubleshooting
- **Log Level**: Control verbosity of logs
- **Sensitive Data**: Option to exclude sensitive data from logs

## Validation and Testing

### Connection Validation

After configuration, verify the connection:

1. **Check System Status**:
   - `sensor.whorang_system_status` should show "Online"
   - `binary_sensor.whorang_system_online` should be "On"

2. **Test Entities**:
   - All entities should appear in **Settings** → **Devices & Services** → **Entities**
   - Entities should have current values (not "Unknown" or "Unavailable")

3. **Test WebSocket**:
   - Real-time updates should work without manual refresh
   - Check logs for WebSocket connection messages

### AI Provider Validation

Test each configured AI provider:

1. **Manual Analysis**:
   - Use `button.whorang_trigger_analysis`
   - Check `sensor.whorang_ai_response_time` for response
   - Verify `sensor.whorang_latest_visitor` updates

2. **Provider Switching**:
   - Use `select.whorang_ai_provider` to switch providers
   - Verify each provider works correctly
   - Check cost tracking if enabled

3. **Model Selection**:
   - Use `select.whorang_ai_model` to test different models
   - Verify model switching works for each provider

## Troubleshooting Configuration Issues

### Connection Issues

**"Connection failed" Error**:
1. Verify backend is running and accessible
2. Check host and port configuration
3. Test connectivity: `curl http://your-host:3001/api/health`
4. Review firewall settings

**SSL/TLS Errors**:
1. Verify SSL settings match backend configuration
2. For self-signed certificates, disable "Verify SSL"
3. Check certificate validity and expiration

**Authentication Errors**:
1. Verify API key is correct
2. Check backend authentication configuration
3. Ensure API key has necessary permissions

### AI Provider Issues

**API Key Validation Failed**:
1. Verify API key format and validity
2. Check API key permissions and quotas
3. Test API key directly with provider's API
4. Ensure sufficient credits/quota available

**Model Not Available**:
1. Verify model name is correct
2. Check if model is available in your region
3. Ensure API key has access to the model
4. Try alternative models for the provider

**High Costs**:
1. Monitor usage with cost tracking
2. Consider using more cost-effective models
3. Adjust analysis frequency
4. Use local Ollama for cost-free analysis

### Performance Issues

**Slow Response Times**:
1. Check network connectivity to backend
2. Monitor backend resource usage
3. Consider using faster AI models
4. Adjust timeout settings

**High Resource Usage**:
1. Increase polling intervals
2. Disable unnecessary features
3. Monitor backend performance
4. Consider hardware upgrades

## Best Practices

### Security
- Use SSL for remote connections
- Secure API keys properly
- Regular security updates
- Monitor access logs

### Performance
- Optimize polling intervals
- Use appropriate AI models for your needs
- Monitor resource usage
- Regular maintenance

### Cost Management
- Enable cost tracking
- Use local Ollama when possible
- Choose cost-effective models
- Monitor usage patterns

### Reliability
- Enable WebSocket for real-time updates
- Configure proper timeouts
- Monitor system health
- Regular backups

## Next Steps

After successful configuration:

1. **[Set Up Automations](../automation/basic-automations.md)** - Create essential automations
2. **[Create Dashboard](../usage/dashboard-examples.md)** - Build monitoring dashboards
3. **[Explore Services](../usage/services-reference.md)** - Learn about available services
4. **[Advanced Configuration](advanced-options.md)** - Explore advanced features

---

**Need Help?** Check our [troubleshooting guide](../troubleshooting/common-issues.md) or [open an issue](https://github.com/Beast12/whorang-integration/issues).
