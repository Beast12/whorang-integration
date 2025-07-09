# Visual Face Gallery Setup Guide

This guide explains how to set up and use the custom visual face gallery component for WhoRang AI Doorbell integration.

## Overview

The Visual Face Gallery provides a Google Nest-style interface for managing face recognition within Home Assistant. It features:

- **Visual face thumbnails** in a responsive grid
- **Click/tap selection** with visual feedback
- **Batch labeling** of multiple faces
- **Progress tracking** with real-time updates
- **Mobile-friendly** touch interface
- **Quality indicators** for face detection confidence

## Prerequisites

### Required Components

1. **WhoRang AI Doorbell Integration** - Must be installed and configured
2. **Working Face Detection** - WhoRang addon must be detecting faces
3. **Input Helpers** - Required for fallback manual controls

### Optional Dependencies

- **Mushroom Cards** (via HACS) - For enhanced status cards
- **Auto-entities** (via HACS) - For dynamic entity lists

## Installation Steps

### 1. Verify Integration Setup

Ensure your WhoRang integration is working:

```yaml
# Check these entities exist:
- sensor.whorang_ai_doorbell_face_gallery
- binary_sensor.whorang_ai_doorbell_system_online
- sensor.whorang_ai_doorbell_ai_provider
```

### 2. Create Input Helpers

Go to **Settings → Devices & Services → Helpers** and create:

#### Number Helper
- **Name**: Face ID Input
- **Entity ID**: `input_number.face_id_input`
- **Min**: 1
- **Max**: 9999
- **Step**: 1

#### Text Helpers
- **Name**: Person Name Input
- **Entity ID**: `input_text.person_name_input`
- **Max length**: 100

- **Name**: Batch Person Name
- **Entity ID**: `input_text.batch_person_name`
- **Max length**: 100

### 3. Install Custom Card

The custom face manager card is automatically registered when the WhoRang integration loads. No additional installation is required.

### 4. Add Dashboard

1. Go to **Settings → Dashboards**
2. Click **+ Add Dashboard**
3. Choose **New dashboard from scratch**
4. Name it "WhoRang Face Recognition"
5. Click the **⋮** menu → **Raw configuration editor**
6. Copy and paste the contents of `visual_face_dashboard.yaml`
7. Click **Save**

## Usage Guide

### Visual Interface

#### Selecting Faces
- **Single click/tap** a face to select it
- **Selected faces** show a blue border and checkmark
- **Click "Select All"** to select all unknown faces
- **Click "Clear All"** to deselect all faces

#### Labeling Faces
1. **Select one or more faces** by clicking them
2. **Enter a person's name** in the text field
3. **Click "Label Selected"** to assign faces to that person
4. **Wait for confirmation** message and auto-refresh

#### Progress Tracking
- **Progress bar** shows overall labeling completion
- **Statistics** display unknown vs. known face counts
- **Quality badges** show detection confidence (0-100%)

### Features

#### Batch Operations
- **Select multiple faces** of the same person
- **Label them together** for consistent recognition
- **Automatic person creation** if name doesn't exist

#### Quality Indicators
- **Green (80-100%)**: High quality, reliable for recognition
- **Yellow (60-79%)**: Medium quality, acceptable
- **Red (0-59%)**: Low quality, may need manual verification

#### Auto-refresh
- **Gallery updates** automatically after labeling
- **Progress tracking** updates in real-time
- **Manual refresh** button available if needed

### Mobile Experience

The interface is optimized for mobile devices:

- **Touch-friendly** face selection
- **Responsive grid** adapts to screen size
- **Large touch targets** for easy interaction
- **Swipe-friendly** scrolling

## Troubleshooting

### Common Issues

#### Faces Not Loading
**Problem**: Face thumbnails show "Loading..." or "Image Error"

**Solutions**:
1. Check WhoRang system is online
2. Verify face detection is working
3. Check network connectivity to WhoRang
4. Refresh the page/dashboard

#### Labeling Fails
**Problem**: "Failed to label faces" error message

**Solutions**:
1. Verify person name is valid (no special characters)
2. Check WhoRang system is responding
3. Try labeling fewer faces at once
4. Use manual controls as fallback

#### Custom Card Not Found
**Problem**: "Custom element doesn't exist: whorang-face-manager-card"

**Solutions**:
1. Restart Home Assistant
2. Clear browser cache
3. Check integration is properly installed
4. Verify no JavaScript errors in browser console

#### No Faces Displayed
**Problem**: "All faces have been labeled!" when faces should exist

**Solutions**:
1. Trigger face detection: `whorang.get_unknown_faces`
2. Check face detection is enabled in WhoRang
3. Verify images are being processed
4. Check entity state in Developer Tools

### Manual Fallback

If the visual interface isn't working, use the manual controls:

1. **Find face ID** from entity attributes or WhoRang logs
2. **Enter face ID** in the number input
3. **Enter person name** in the text input
4. **Click "Label Face"** button

### Debug Information

#### Check Entity States
Go to **Developer Tools → States** and check:

```yaml
sensor.whorang_ai_doorbell_face_gallery:
  state: "3 unknown, 8 known"
  attributes:
    unknown_faces: [...]
    known_persons: [...]
    total_unknown: 3
    total_known: 8
    labeling_progress: 72.7
    gallery_ready: true
```

#### Check Services
Go to **Developer Tools → Services** and verify these exist:

- `whorang.label_face`
- `whorang.batch_label_faces`
- `whorang.get_unknown_faces`
- `whorang.delete_face`

#### Browser Console
Press **F12** and check for JavaScript errors:

```javascript
// Should see this on successful load:
WHORANG-FACE-MANAGER-CARD v1.0.0
```

## Advanced Configuration

### Custom Card Options

```yaml
type: custom:whorang-face-manager-card
entity: sensor.whorang_ai_doorbell_face_gallery
title: "My Face Manager"          # Custom title
columns: 6                        # Faces per row (default: 4)
show_progress: true               # Show progress bar (default: true)
show_controls: true               # Show labeling controls (default: true)
```

### Responsive Columns
The grid automatically adjusts:
- **Desktop**: 4 columns (or custom setting)
- **Tablet**: 3 columns
- **Mobile**: 2 columns

### Custom Styling
The card uses CSS custom properties for theming:

```css
--primary-color: #03a9f4          # Selection color
--card-background-color: #fff     # Card background
--primary-text-color: #212121     # Text color
--secondary-text-color: #757575   # Secondary text
```

## Integration with Automations

### Face Labeled Event
```yaml
trigger:
  - platform: event
    event_type: whorang_face_labeled
    event_data:
      person_name: "John Doe"
action:
  - service: notify.mobile_app
    data:
      message: "Face labeled as {{ trigger.event.data.person_name }}"
```

### Unknown Face Detected
```yaml
trigger:
  - platform: event
    event_type: whorang_unknown_face_detected
condition:
  - condition: numeric_state
    entity_id: sensor.whorang_ai_doorbell_face_gallery
    attribute: total_unknown
    above: 5
action:
  - service: notify.mobile_app
    data:
      message: "{{ trigger.event.data.unknown_faces_count }} unknown faces need labeling"
```

## Performance Considerations

### Image Loading
- **Thumbnails** are served at 150px for faster loading
- **Full images** available on demand
- **Caching** enabled for 24 hours

### Network Usage
- **Efficient loading** with progressive image display
- **Minimal API calls** with smart refresh logic
- **Mobile optimized** for slower connections

### Browser Compatibility
- **Modern browsers** required (Chrome 80+, Firefox 75+, Safari 13+)
- **JavaScript enabled** required
- **Local storage** used for temporary state

## Support

### Getting Help
1. **Check logs** in Home Assistant for error messages
2. **Verify setup** using this guide
3. **Test manually** using fallback controls
4. **Report issues** with detailed error information

### Useful Log Commands
```yaml
# Enable debug logging
logger:
  default: info
  logs:
    custom_components.whorang: debug
```

This visual face gallery transforms the WhoRang face recognition system into an intuitive, Google Nest-style interface that makes face management accessible and efficient for all users.
