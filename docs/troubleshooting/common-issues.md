# Common Issues and Troubleshooting

This guide covers the most common issues users encounter with the WhoRang AI Doorbell Integration and their solutions.

## Installation Issues

### Integration Not Found in HACS

**Symptoms**:
- Cannot find "WhoRang AI Doorbell" in HACS
- Search returns no results

**Solutions**:

1. **Add Custom Repository**:
   ```
   Repository: https://github.com/Beast12/whorang-integration
   Category: Integration
   ```

2. **Verify HACS Installation**:
   - Ensure HACS is properly installed and configured
   - Restart Home Assistant if HACS was recently installed

3. **Check Repository URL**:
   - Ensure exact URL: `https://github.com/Beast12/whorang-integration`
   - No trailing slashes or extra characters

4. **Refresh HACS**:
   - Go to HACS → Integrations → Three dots menu → Reload

### Integration Installation Fails

**Symptoms**:
- Download fails with error messages
- Integration files not created

**Solutions**:

1. **Check Internet Connection**:
   - Verify Home Assistant can access GitHub
   - Test: `curl https://github.com/Beast12/whorang-integration`

2. **Clear HACS Cache**:
   - Restart Home Assistant
   - Try installation again

3. **Manual Installation**:
   ```bash
   cd /config/custom_components
   git clone https://github.com/Beast12/whorang-integration.git whorang
   ```

4. **Check Disk Space**:
   - Ensure sufficient storage available
   - Clean up old backups if needed

## Connection Issues

### Cannot Connect to WhoRang Backend

**Symptoms**:
- "Connection failed" during setup
- Integration shows as unavailable
- Entities show "Unknown" or "Unavailable"

**Diagnostic Steps**:

1. **Test Backend Connectivity**:
   ```bash
   # Test basic connectivity
   curl http://your-host:3001/api/health
   
   # Expected response: {"status": "ok"}
   ```

2. **Check Backend Status**:
   - **Add-on users**: Check add-on logs and status
   - **Docker users**: `docker-compose logs whorang`
   - **Manual users**: Check service status

**Solutions**:

1. **Verify Host Configuration**:
   - **Add-on users**: Use `homeassistant.local` or `localhost`
   - **Docker users**: Use Docker host IP
   - **Remote users**: Use server IP or domain

2. **Check Port Configuration**:
   - Default port: `3001`
   - Verify port is not blocked by firewall
   - Test: `telnet your-host 3001`

3. **SSL Configuration Issues**:
   - If using SSL, ensure certificates are valid
   - For self-signed certificates, disable "Verify SSL"
   - Check SSL certificate expiration

4. **Network Troubleshooting**:
   ```bash
   # Test network connectivity
   ping your-host
   
   # Test port connectivity
   nc -zv your-host 3001
   
   # Check DNS resolution
   nslookup your-host
   ```

### WebSocket Connection Issues

**Symptoms**:
- Entities don't update in real-time
- Manual refresh required for updates
- WebSocket errors in logs

**Solutions**:

1. **Disable WebSocket Temporarily**:
   - Go to integration options
   - Disable "Enable WebSocket"
   - Test if basic functionality works

2. **Check Firewall Settings**:
   - Ensure WebSocket port is open
   - Check for proxy/firewall blocking WebSocket upgrades

3. **Network Configuration**:
   - Some networks block WebSocket connections
   - Try different network or VPN

4. **Backend WebSocket Support**:
   - Verify backend supports WebSocket connections
   - Check backend logs for WebSocket errors

## Authentication Issues

### API Key Validation Failed

**Symptoms**:
- "Invalid API key" errors
- Authentication failures during setup

**Solutions**:

1. **Verify API Key Format**:
   - **OpenAI**: Starts with `sk-`
   - **Claude**: Starts with `sk-ant-`
   - **Gemini**: Starts with `AI`
   - **Google Cloud**: Various formats

2. **Test API Key Directly**:
   ```bash
   # Test OpenAI API key
   curl -H "Authorization: Bearer sk-your-key" \
        https://api.openai.com/v1/models
   
   # Test Claude API key
   curl -H "x-api-key: sk-ant-your-key" \
        https://api.anthropic.com/v1/messages
   ```

3. **Check API Key Permissions**:
   - Ensure API key has necessary permissions
   - Verify quota and billing status
   - Check rate limits

4. **API Key Expiration**:
   - Verify API key hasn't expired
   - Regenerate if necessary

## Entity Issues

### Entities Not Appearing

**Symptoms**:
- Integration installed but no entities visible
- Missing sensors, cameras, or controls

**Solutions**:

1. **Check Entity Registry**:
   - Go to **Settings** → **Devices & Services** → **Entities**
   - Search for "whorang"
   - Enable any disabled entities

2. **Restart Home Assistant**:
   - Full restart required after installation
   - Wait for complete startup

3. **Check Integration Status**:
   - Verify integration shows as "Loaded" in Devices & Services
   - Look for error messages or warnings

4. **Review Integration Logs**:
   ```
   Settings → System → Logs
   Filter: "whorang"
   ```

### Entities Show "Unknown" or "Unavailable"

**Symptoms**:
- Entities exist but show no data
- States remain "Unknown" or "Unavailable"

**Solutions**:

1. **Check Backend Connection**:
   - Verify `binary_sensor.whorang_system_online` is "On"
   - Test backend connectivity

2. **Force Data Refresh**:
   - Use `button.whorang_refresh_data`
   - Wait for update cycle

3. **Check Backend Data**:
   - Verify backend has data to provide
   - Check backend API endpoints directly

4. **Review Entity Configuration**:
   - Some entities may require specific backend features
   - Check entity attributes for error messages

### Camera Entity Issues

**Symptoms**:
- Camera shows "Unknown" or no image
- Image not updating

**Solutions**:

1. **Check Image Availability**:
   - Verify backend has recent images
   - Test image URL directly in browser

2. **Image Format Issues**:
   - Ensure images are in supported format (JPEG, PNG)
   - Check image size and resolution

3. **Network Issues**:
   - Large images may timeout on slow connections
   - Check network bandwidth

4. **Backend Image Service**:
   - Verify backend image serving is working
   - Check backend logs for image-related errors

## AI Provider Issues

### AI Analysis Not Working

**Symptoms**:
- AI analysis fails or returns errors
- No response from AI providers

**Solutions**:

1. **Check AI Provider Configuration**:
   - Verify API keys are correctly configured
   - Test API key validity

2. **Provider-Specific Issues**:

   **OpenAI**:
   - Check quota and billing status
   - Verify model availability in your region
   - Test with different models

   **Claude**:
   - Ensure API access is enabled
   - Check rate limits and quotas

   **Gemini**:
   - Verify Google AI Studio access
   - Check API key permissions

   **Local (Ollama)**:
   - Ensure Ollama is running
   - Verify vision-capable model is installed
   - Test: `ollama list` and `ollama run llava`

3. **Network Connectivity**:
   - Test internet connectivity for cloud providers
   - Check for proxy or firewall blocking

4. **Rate Limiting**:
   - Reduce analysis frequency
   - Implement delays between requests

### High AI Costs

**Symptoms**:
- Unexpected high costs
- Rapid quota consumption

**Solutions**:

1. **Enable Cost Tracking**:
   - Monitor `sensor.whorang_ai_cost_today`
   - Set up cost alerts

2. **Optimize Provider Selection**:
   - Use local Ollama for cost-free analysis
   - Switch to more cost-effective models
   - Implement smart provider switching

3. **Reduce Analysis Frequency**:
   - Adjust trigger conditions
   - Implement cooldown periods

4. **Monitor Usage Patterns**:
   - Review automation triggers
   - Identify high-usage scenarios

## Performance Issues

### Slow Response Times

**Symptoms**:
- Long delays in entity updates
- Slow AI analysis responses

**Solutions**:

1. **Check Network Performance**:
   - Test network speed and latency
   - Monitor backend response times

2. **Backend Performance**:
   - Check backend resource usage (CPU, memory)
   - Monitor backend logs for performance issues

3. **AI Provider Performance**:
   - Try different AI models
   - Switch to faster providers
   - Use local Ollama for faster responses

4. **Optimize Configuration**:
   - Adjust polling intervals
   - Reduce unnecessary API calls

### High Resource Usage

**Symptoms**:
- High CPU or memory usage
- System slowdowns

**Solutions**:

1. **Monitor Resource Usage**:
   - Check Home Assistant system resources
   - Monitor backend resource consumption

2. **Optimize Settings**:
   - Increase polling intervals
   - Disable unnecessary features
   - Reduce WebSocket connections

3. **Backend Optimization**:
   - Ensure adequate hardware resources
   - Optimize backend configuration

## Automation Issues

### Automations Not Triggering

**Symptoms**:
- Automations don't run when expected
- No notifications or actions

**Solutions**:

1. **Check Automation Status**:
   - Verify automations are enabled
   - Check automation traces

2. **Verify Trigger Conditions**:
   - Test entity states manually
   - Use Developer Tools to simulate triggers

3. **Review Conditions**:
   - Check all conditions are met
   - Use Template Editor to test conditions

4. **Check Action Configuration**:
   - Verify service calls are correct
   - Test actions manually

### Notification Issues

**Symptoms**:
- No notifications received
- Notifications missing images or actions

**Solutions**:

1. **Check Notification Service**:
   - Verify mobile app is configured
   - Test notification service manually

2. **Device Configuration**:
   - Ensure device name is correct
   - Check mobile app permissions

3. **Image Issues**:
   - Verify camera entity is working
   - Check image URL accessibility

4. **Action Button Issues**:
   - Verify action handlers are configured
   - Check event listeners

## Diagnostic Tools

### Integration Logs

**Access Logs**:
```
Settings → System → Logs
Filter: "whorang"
```

**Common Log Messages**:
- Connection errors
- Authentication failures
- API response issues
- WebSocket problems

### Developer Tools

**Useful Tools**:
1. **States**: Check entity states and attributes
2. **Services**: Test service calls manually
3. **Templates**: Test template logic
4. **Events**: Monitor integration events

### Backend Diagnostics

**Health Check**:
```bash
curl http://your-host:3001/api/health
```

**API Endpoints**:
```bash
# Check providers
curl http://your-host:3001/api/openai/providers

# Check system status
curl http://your-host:3001/api/stats
```

## Getting Help

### Before Requesting Help

1. **Check Logs**:
   - Review integration logs
   - Check backend logs
   - Note any error messages

2. **Gather Information**:
   - Home Assistant version
   - Integration version
   - Backend version and type
   - Network configuration

3. **Test Basic Functionality**:
   - Verify backend connectivity
   - Test simple operations

### Support Channels

1. **GitHub Issues**:
   - [Integration Issues](https://github.com/Beast12/whorang-integration/issues)
   - [Add-on Issues](https://github.com/Beast12/whorang-addon/issues)

2. **Community Support**:
   - [Home Assistant Community](https://community.home-assistant.io/)
   - Search for existing solutions

3. **Documentation**:
   - [Installation Guide](../installation/hacs-installation.md)
   - [Configuration Guide](../configuration/initial-setup.md)
   - [Automation Examples](../automation/basic-automations.md)

### Issue Reporting Template

When reporting issues, include:

```
**Environment**:
- Home Assistant version: 
- Integration version: 
- Backend type: (Add-on/Docker/Manual)
- Backend version: 

**Issue Description**:
- What you expected to happen
- What actually happened
- Steps to reproduce

**Logs**:
- Integration logs (Settings → System → Logs)
- Backend logs (if accessible)
- Any error messages

**Configuration**:
- Connection settings (host, port, SSL)
- AI providers configured
- Relevant automation configuration
```

## Prevention Tips

### Regular Maintenance

1. **Keep Updated**:
   - Update integration via HACS
   - Update backend regularly
   - Monitor for security updates

2. **Monitor Health**:
   - Set up system health automations
   - Monitor resource usage
   - Check logs regularly

3. **Backup Configuration**:
   - Regular Home Assistant backups
   - Export automation configurations
   - Document custom settings

### Best Practices

1. **Gradual Deployment**:
   - Test with simple automations first
   - Add complexity gradually
   - Monitor performance impact

2. **Resource Management**:
   - Monitor AI costs and usage
   - Optimize polling intervals
   - Use appropriate AI models

3. **Security**:
   - Secure API keys properly
   - Use SSL for remote connections
   - Regular security reviews

---

**Still Need Help?** If this guide doesn't solve your issue, please [open an issue](https://github.com/Beast12/whorang-integration/issues) with detailed information about your problem.
