# Manual Installation Guide for WhoRang Visual Face Gallery

Since automatic frontend registration is disabled to avoid errors, follow this guide to manually install the custom cards.

## Step 1: Copy Custom Card Files

### Option A: Copy to www/community directory
```bash
# Create directory
mkdir -p /config/www/community/whorang

# Copy custom card files
cp /config/custom_components/whorang/www/whorang-face-manager.js /config/www/community/whorang/
cp /config/custom_components/whorang/www/whorang-face-manager-simple.js /config/www/community/whorang/
```

### Option B: Copy to www directory directly
```bash
# Copy to main www directory
cp /config/custom_components/whorang/www/whorang-face-manager.js /config/www/
cp /config/custom_components/whorang/www/whorang-face-manager-simple.js /config/www/
```

## Step 2: Register Resources in Home Assistant

1. **Go to Settings → Dashboards → Resources**
2. **Click "+ Add Resource"**

### For Option A (community directory):
3. **Add Resource 1 (Main Card):**
   - URL: `/local/community/whorang/whorang-face-manager.js`
   - Type: **JavaScript Module**
4. **Add Resource 2 (Simple Card - Optional):**
   - URL: `/local/community/whorang/whorang-face-manager-simple.js`
   - Type: **JavaScript Module**

### For Option B (www directory):
3. **Add Resource 1 (Main Card):**
   - URL: `/local/whorang-face-manager.js`
   - Type: **JavaScript Module**
4. **Add Resource 2 (Simple Card - Optional):**
   - URL: `/local/whorang-face-manager-simple.js`
   - Type: **JavaScript Module**

5. **Click "Create"** for each resource

**Note**: You can register both cards or just one. The main card uses `whorang-face-manager-card` and the simple card uses `whorang-face-manager-simple-card`.

## Step 3: Create Input Helpers

Go to **Settings → Devices & Services → Helpers** and create:

### Number Helper
- **Name**: Face ID Input
- **Entity ID**: `input_number.face_id_input`
- **Min**: 1
- **Max**: 9999
- **Step**: 1

### Text Helpers
- **Name**: Person Name Input
- **Entity ID**: `input_text.person_name_input`
- **Max length**: 100

- **Name**: Batch Person Name
- **Entity ID**: `input_text.batch_person_name`
- **Max length**: 100

## Step 4: Test Custom Card

Create a test dashboard with this configuration:

```yaml
title: Test Custom Card
views:
  - title: Test
    cards:
      - type: custom:whorang-face-manager-card
        entity: sensor.whorang_ai_doorbell_face_gallery
        title: Face Manager Test
```

## Step 5: Use Full Dashboard

Once the custom card is working, use the complete visual dashboard from `examples/visual_face_dashboard.yaml`.

## Troubleshooting

### If Custom Card Doesn't Load
1. **Check file paths** - Ensure files are copied correctly
2. **Verify URLs** - Make sure resource URLs match file locations
3. **Clear browser cache** - Hard refresh (Ctrl+F5)
4. **Check browser console** - Look for JavaScript errors

### Fallback Option
If custom cards don't work, use the simple dashboard from `examples/simple_face_dashboard.yaml` which uses only standard Home Assistant cards.

## File Locations

The custom card files are located at:
- `/config/custom_components/whorang/www/whorang-face-manager.js`
- `/config/custom_components/whorang/www/whorang-face-manager-simple.js`

Copy these to your `/config/www/` directory and register them as resources.
