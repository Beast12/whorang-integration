# WhoRang Custom Cards Configuration Guide

This guide covers the configuration options for the WhoRang custom cards, including the new production-ready image URL detection system.

## Overview

WhoRang provides two custom cards for face management:
- **whorang-face-manager-card**: Full-featured visual face manager
- **whorang-face-manager-simple-card**: Simplified face manager

Both cards now include robust, production-ready image URL detection that works across all Home Assistant installation types.

## Basic Configuration

### Main Face Manager Card

```yaml
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
title: "Face Recognition Manager"
columns: 4
show_progress: true
show_controls: true
```

### Simple Face Manager Card

```yaml
type: custom:whorang-face-manager-simple-card
entity: sensor.whorang_ai_doorbell_face_gallery
title: "Face Recognition Manager"
```

## Advanced Configuration Options

### Custom WhoRang Server URL

For non-standard installations, you can specify the WhoRang backend URL:

```yaml
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "http://custom-host:3001"
```

### Multiple Fallback URLs

For complex network setups, you can provide multiple fallback URLs:

```yaml
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "http://primary-host:3001"
fallback_urls:
  - "http://backup-host:3001"
  - "https://secure-host:3001"
  - "http://192.168.1.100:3001"
```

## Automatic URL Detection

The cards automatically detect the correct WhoRang backend URL using the following priority order:

### 1. User Configuration (Highest Priority)
- `whorang_url` from card configuration
- `fallback_urls` array from card configuration

### 2. Integration-Provided URLs
- `backend_url` from entity attributes
- `whorang_server_url` from entity attributes

### 3. Smart Detection
- Same host as Home Assistant with port 3001
- Protocol adaptation (HTTPS → HTTP fallback)

### 4. Common Configurations
- `http://homeassistant.local:3001` (Add-on users)
- `http://localhost:3001` (Local installations)
- `http://127.0.0.1:3001` (Fallback)

## Installation Type Support

### Home Assistant OS + Add-on
```yaml
# Usually works automatically, but can be configured:
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "http://homeassistant.local:3001"
```

### Home Assistant Supervised + Add-on
```yaml
# Auto-detects using current hostname:
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
# No additional configuration needed
```

### Home Assistant Container + Docker
```yaml
# Configure based on your Docker setup:
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "http://docker-host:3001"
```

### Home Assistant Core + Docker
```yaml
# Configure for your specific setup:
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "http://localhost:3001"
fallback_urls:
  - "http://127.0.0.1:3001"
  - "http://your-server-ip:3001"
```

## Configuration Parameters

### Main Card Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `entity` | string | Required | WhoRang face gallery sensor entity |
| `title` | string | "Face Manager" | Card title |
| `columns` | number | 4 | Number of columns in face grid |
| `show_progress` | boolean | true | Show labeling progress bar |
| `show_controls` | boolean | true | Show face management controls |
| `whorang_url` | string | Auto-detected | Custom WhoRang backend URL |
| `fallback_urls` | array | [] | Additional fallback URLs |

### Simple Card Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `entity` | string | Required | WhoRang face gallery sensor entity |
| `title` | string | "Face Recognition Manager" | Card title |
| `whorang_url` | string | Auto-detected | Custom WhoRang backend URL |
| `fallback_urls` | array | [] | Additional fallback URLs |

## Troubleshooting

### Images Not Loading

If face images are not loading, try these steps:

1. **Check Network Connectivity**
   ```yaml
   # Test with explicit URL
   type: custom:whorang-face-manager-card
   entity: sensor.whorang_ai_doorbell_face_gallery
   whorang_url: "http://your-ha-ip:3001"
   ```

2. **Enable Browser Developer Tools**
   - Open browser developer tools (F12)
   - Check Console tab for error messages
   - Check Network tab for failed requests

3. **Test Multiple URLs**
   ```yaml
   type: custom:whorang-face-manager-card
   entity: sensor.whorang_ai_doorbell_face_gallery
   fallback_urls:
     - "http://homeassistant.local:3001"
     - "http://localhost:3001"
     - "http://127.0.0.1:3001"
     - "http://your-server-ip:3001"
   ```

### Common Network Configurations

#### Docker Compose Setup
```yaml
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "http://host.docker.internal:3001"
```

#### Reverse Proxy Setup
```yaml
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "https://your-domain.com/whorang"
```

#### Custom Port Setup
```yaml
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "http://homeassistant.local:8080"
```

## Error Messages

### "Image Error"
- The image URL was found but failed to load
- Check network connectivity to WhoRang backend
- Verify WhoRang backend is running and accessible

### "No Image"
- No working image URL could be found
- Configure `whorang_url` manually
- Check WhoRang backend API endpoints

### "Load Error"
- JavaScript error occurred during image loading
- Check browser console for detailed error messages
- Verify card configuration syntax

## Performance Optimization

### Image Loading Performance
- Cards test URLs with 2-second timeout
- Working URLs are cached for future use
- Multiple URLs tested in parallel for efficiency

### Network Efficiency
- Failed URLs are not retried within the same session
- Successful base URLs are reused for all faces
- Images load lazily as cards are rendered

## Security Considerations

### HTTPS/HTTP Mixed Content
If Home Assistant runs on HTTPS but WhoRang on HTTP:

```yaml
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "https://your-domain.com:3001"  # Use HTTPS
```

### Network Isolation
Cards only attempt connections to:
- User-configured URLs
- Same-host URLs (different ports)
- Common local network addresses

### CORS Configuration
Ensure WhoRang backend allows requests from Home Assistant:
- Add Home Assistant URL to CORS origins
- Configure proper CORS headers in WhoRang

## Migration from Previous Versions

### From Hardcoded URLs
Previous versions used hardcoded `127.0.0.1:3001`. New version:
- Automatically detects correct URL
- No configuration changes required for most users
- Provides fallback to previous behavior

### Configuration Updates
```yaml
# Old configuration (still works)
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery

# New configuration (recommended for custom setups)
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
whorang_url: "http://your-custom-host:3001"
```

## Support and Debugging

### Enable Debug Logging
Check browser console for detailed logging:
- Image URL detection attempts
- Network request results
- Error messages and stack traces

### Common Issues and Solutions

1. **Mixed Content Errors**: Use HTTPS for WhoRang backend
2. **CORS Errors**: Configure WhoRang CORS settings
3. **Network Timeouts**: Check firewall and network connectivity
4. **Port Conflicts**: Verify WhoRang is running on expected port

### Getting Help
- Check browser developer tools console
- Verify WhoRang backend is accessible
- Test URLs manually in browser
- Report issues with network configuration details

This production-ready image loading system ensures the WhoRang custom cards work reliably across all Home Assistant installation types and network configurations.
