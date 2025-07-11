# WhoRang Face Labeling Usage Guide

## Overview
This guide explains how to view detected faces and label unknown faces using the WhoRang Home Assistant integration.

## Quick Start

### 1. Setup Required Helper Entities
First, add the helper entities to your `configuration.yaml`:

```yaml
# Copy contents from face_labeling_helpers.yaml
input_number:
  face_id_input:
    name: Face ID for Labeling
    min: 1
    max: 10000
    step: 1
    mode: box
    icon: mdi:identifier

input_text:
  person_name_input:
    name: Person Name for Labeling
    max: 100
    icon: mdi:account
    
  quick_person_name:
    name: Quick Person Name
    max: 100
    icon: mdi:account-start
```

### 2. Add Dashboard
Copy the contents of `face_labeling_dashboard.yaml` to create a new dashboard in Home Assistant.

### 3. Restart Home Assistant
Restart Home Assistant to load the new helper entities.

## How to View Unknown Faces

### Method 1: Using the Dashboard

1. **Open the Face Labeling Dashboard**
2. **Click "Refresh Unknown Faces"** - This populates the sensor with face data
3. **View Face Details** - The dashboard will show:
   - Face ID numbers
   - Quality scores
   - Detection timestamps
   - Links to view face images
   - Context information

### Method 2: Using Developer Tools

1. Go to **Developer Tools** → **States**
2. Find `sensor.whorang_unknown_faces`
3. Click on the sensor to view attributes
4. Look for the `face_details` attribute which contains:
   ```json
   {
     "face_id": 8,
     "quality_score": 0.85,
     "face_image_url": "http://your-whorang:3001/uploads/faces/face_8.jpg",
     "original_image_url": "http://your-whorang:3001/uploads/events/event_123.jpg",
     "created_at": "2025-01-08T16:30:00Z"
   }
   ```

### Method 3: Using Services

Call the service to refresh face data:
```yaml
service: whorang.get_unknown_faces
data:
  limit: 50
  quality_threshold: 0.6
```

## How to Label Faces

### Method 1: Quick Labeling (Recommended)

1. **Refresh Unknown Faces** first
2. **View the "Next Face to Label"** section on the dashboard
3. **Enter the person's name** in the "Quick Person Name" field
4. **Click "Label Face [ID]"** button

### Method 2: Manual Labeling

1. **Note the Face ID** from the face details
2. **Enter Face ID** in the "Face ID" field
3. **Enter Person Name** in the "Person Name" field
4. **Click "Label Face"** or **"Create New Person"**

### Method 3: Using Services Directly

```yaml
# Label existing person
service: whorang.label_face
data:
  face_id: 8
  person_name: "John Doe"

# Create new person
service: whorang.create_person_from_face
data:
  face_id: 8
  person_name: "Jane Smith"
  description: "Family member"
```

## Viewing Face Images

### Direct Image URLs
The sensor provides direct URLs to face images:

- **Face Crop**: `face_image_url` - Shows just the detected face
- **Original Image**: `original_image_url` - Shows the full doorbell image
- **Thumbnail**: `thumbnail_url` - Small version of the face crop

### Accessing Images
1. **From Dashboard**: Click the "View Face Crop" or "View Full Image" links
2. **Direct URL**: Copy the URL from sensor attributes and paste in browser
3. **Example URL**: `http://192.168.1.100:3001/uploads/faces/face_8.jpg`

## Understanding Face Data

### Face Quality Scores
- **0.8 - 1.0**: High quality (excellent for labeling)
- **0.6 - 0.8**: Medium quality (good for labeling)
- **0.0 - 0.6**: Low quality (may be difficult to recognize)

### Face Information Available
Each detected face includes:
- **Face ID**: Unique identifier for labeling
- **Quality Score**: How clear/recognizable the face is
- **Confidence**: Detection confidence level
- **Timestamps**: When the face was detected
- **Context**: AI description of the scene
- **Image URLs**: Direct links to face images

## Troubleshooting

### No Faces Showing
1. **Check if faces are detected**: Look at `sensor.whorang_latest_face_detection`
2. **Refresh unknown faces**: Click "Refresh Unknown Faces" button
3. **Check quality threshold**: Lower the quality threshold in the service call
4. **Verify backend connection**: Check `sensor.whorang_system_status`

### Can't See Face Images
1. **Check URLs**: Ensure the URLs in sensor attributes are accessible
2. **Network access**: Make sure you can reach the WhoRang backend from your browser
3. **Backend status**: Verify the WhoRang backend is running and accessible

### Face Labeling Not Working
1. **Check service calls**: Use Developer Tools → Services to test manually
2. **Verify Face ID**: Ensure you're using a valid Face ID from the sensor
3. **Check logs**: Look at Home Assistant logs for error messages
4. **Backend logs**: Check WhoRang backend logs for API errors

## Advanced Usage

### Automation Examples

**Auto-refresh when faces detected:**
```yaml
automation:
  - alias: "Auto Refresh Unknown Faces"
    trigger:
      platform: state
      entity_id: sensor.whorang_latest_face_detection
      to: "1 face detected"
    action:
      service: whorang.get_unknown_faces
      data:
        limit: 50
        quality_threshold: 0.6
```

**Notification when unknown faces found:**
```yaml
automation:
  - alias: "Unknown Face Alert"
    trigger:
      platform: state
      entity_id: sensor.whorang_unknown_faces
    condition:
      condition: template
      value_template: "{{ trigger.to_state.state | int > 0 }}"
    action:
      service: notify.mobile_app_your_phone
      data:
        title: "Unknown Face Detected"
        message: "{{ states('sensor.whorang_unknown_faces') }} faces need labeling"
```

### Bulk Labeling Workflow

1. **Get all unknown faces**: Call `whorang.get_unknown_faces`
2. **Review face details**: Check quality scores and images
3. **Find similar faces**: Use `whorang.get_face_similarities` for each face
4. **Label in batches**: Group similar faces and label together

### Quality-Based Labeling

Focus on high-quality faces first:
```yaml
service: whorang.get_unknown_faces
data:
  limit: 20
  quality_threshold: 0.8  # Only high-quality faces
```

## Best Practices

### For Better Recognition
1. **Label high-quality faces first** (score > 0.8)
2. **Use consistent naming** (e.g., "John Doe" not "john" or "John")
3. **Label multiple angles** of the same person when available
4. **Review similar faces** before labeling to avoid duplicates

### For Efficient Workflow
1. **Set up automations** to auto-refresh face data
2. **Use mobile notifications** to alert when faces need labeling
3. **Create common name shortcuts** using input_select helper
4. **Regular maintenance** - label faces promptly for better accuracy

### Privacy Considerations
1. **Face data storage** - Understand that face crops are stored locally
2. **Access control** - Secure your Home Assistant instance
3. **Data retention** - Consider periodic cleanup of old face data
4. **Consent** - Ensure appropriate consent for face recognition use

## API Reference

### Services Available
- `whorang.get_unknown_faces` - Refresh unknown faces data
- `whorang.label_face` - Label face with existing person
- `whorang.create_person_from_face` - Create new person from face
- `whorang.delete_face` - Remove face from system
- `whorang.get_face_similarities` - Find similar faces

### Sensor Entities
- `sensor.whorang_unknown_faces` - Count and details of unknown faces
- `sensor.whorang_latest_face_detection` - Latest face detection results
- `sensor.whorang_known_faces` - Count of known faces/persons

### Key Attributes
- `face_details` - Complete face information array
- `face_ids` - Quick list of available face IDs
- `next_face_to_label` - Recommended next face for labeling
- `face_image_url` - Direct URL to face crop image

This comprehensive system provides everything needed to effectively manage face recognition and labeling within Home Assistant!
