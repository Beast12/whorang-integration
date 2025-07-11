# Custom Card Troubleshooting Guide

This guide helps troubleshoot issues with the WhoRang Face Manager custom card.

## Common Issues

### 1. "Custom element not found: whorang-face-manager-card"

This error means the custom card JavaScript file isn't being loaded by Home Assistant.

#### Solutions:

**A. Restart Home Assistant**
1. Go to **Settings → System → Restart**
2. Wait for Home Assistant to fully restart
3. Clear your browser cache (Ctrl+F5 or Cmd+Shift+R)
4. Try the dashboard again

**B. Check File Location**
Ensure the file exists at:
```
custom_components/whorang/www/whorang-face-manager.js
```

**C. Check Home Assistant Logs**
1. Go to **Settings → System → Logs**
2. Look for messages like:
   - `Registering frontend resources from: /path/to/custom_components/whorang/www`
   - `Successfully registered WhoRang Face Manager custom card`
   - Any error messages related to frontend registration

**D. Manual Resource Registration**
If automatic registration fails, add manually:

1. Go to **Settings → Dashboards → Resources**
2. Click **+ Add Resource**
3. URL: `/whorang-face-manager/whorang-face-manager.js`
4. Resource type: **JavaScript Module**
5. Click **Create**
6. Refresh your dashboard

### 2. JavaScript Console Errors

**Check Browser Console:**
1. Press **F12** to open developer tools
2. Go to **Console** tab
3. Look for errors related to `whorang-face-manager`

**Common Console Errors:**

```javascript
// Network error - file not found
GET /whorang-face-manager/whorang-face-manager.js net::ERR_FILE_NOT_FOUND

// Solution: Check file exists and restart HA
```

```javascript
// Module loading error
Failed to resolve module specifier "lit"

// Solution: The card uses standard web components, no external dependencies needed
```

### 3. Integration Not Loading

**Check Integration Status:**
1. Go to **Settings → Devices & Services**
2. Find **WhoRang AI Doorbell**
3. Ensure it shows as **Configured** (not **Failed**)

**If Integration Failed:**
1. Remove and re-add the integration
2. Check WhoRang addon is running
3. Verify network connectivity

### 4. Face Gallery Entity Missing

**Check Required Entity:**
The custom card requires: `sensor.whorang_ai_doorbell_face_gallery`

**If Entity Missing:**
1. Check WhoRang addon has face detection enabled
2. Trigger face detection: Service `whorang.get_unknown_faces`
3. Check addon logs for face processing errors

## Debugging Steps

### Step 1: Verify File Structure
```
custom_components/
└── whorang/
    ├── __init__.py
    ├── const.py
    ├── api_client.py
    ├── coordinator.py
    ├── sensor.py
    └── www/
        └── whorang-face-manager.js  ← This file must exist
```

### Step 2: Check Frontend Registration
Look in Home Assistant logs for:
```
[custom_components.whorang] Registering frontend resources from: /path/to/www
[custom_components.whorang] Successfully registered WhoRang Face Manager custom card at /whorang-face-manager/whorang-face-manager.js
```

### Step 3: Test Static File Access
Try accessing directly in browser:
```
http://your-ha-ip:8123/whorang-face-manager/whorang-face-manager.js
```

Should return JavaScript code, not 404 error.

### Step 4: Check Entity Data
Go to **Developer Tools → States** and check:
```yaml
sensor.whorang_ai_doorbell_face_gallery:
  state: "X unknown, Y known"
  attributes:
    unknown_faces: [...]
    gallery_ready: true
```

## Fallback Solutions

### Use Simple Dashboard
If custom card won't load, use the simple dashboard:
- File: `examples/simple_face_dashboard.yaml`
- Uses only standard Home Assistant cards
- Provides all face labeling functionality
- No custom components required

### Manual Face Labeling
Even without dashboards, you can use services directly:

```yaml
# Label single face
service: whorang.label_face
data:
  face_id: 123
  person_name: "John Doe"

# Batch label faces
service: whorang.batch_label_faces
data:
  face_ids: [123, 124, 125]
  person_name: "John Doe"
  create_person: true
```

## Advanced Debugging

### Enable Debug Logging
Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.whorang: debug
```

### Check Network Tab
1. Open browser developer tools
2. Go to **Network** tab
3. Reload dashboard
4. Look for failed requests to `/whorang-face-manager/`

### Inspect Element
1. Right-click on the error card
2. Select **Inspect Element**
3. Look for `<whorang-face-manager-card>` element
4. Check if it's being created but not rendering

## Getting Help

### Information to Provide
When reporting issues, include:

1. **Home Assistant Version**
2. **Browser and Version**
3. **Console Errors** (F12 → Console)
4. **Home Assistant Logs** (Settings → System → Logs)
5. **Entity State** (Developer Tools → States → sensor.whorang_ai_doorbell_face_gallery)
6. **File Verification** (confirm whorang-face-manager.js exists)

### Log Commands
```bash
# Check if file exists
ls -la custom_components/whorang/www/

# Check file permissions
ls -la custom_components/whorang/www/whorang-face-manager.js

# Check Home Assistant can read file
cat custom_components/whorang/www/whorang-face-manager.js | head -5
```

## Success Indicators

### When Working Correctly:
1. **No console errors** in browser developer tools
2. **Card loads** without "Custom element not found" error
3. **Face thumbnails display** in a grid layout
4. **Click selection works** (blue borders on faces)
5. **Labeling functions** update the gallery

### Expected Browser Console:
```javascript
WHORANG-FACE-MANAGER-CARD v1.0.0
```

This troubleshooting guide should help resolve most issues with the custom face manager card. If problems persist, use the simple dashboard as a reliable fallback.
