# Face Management Guide

This comprehensive guide covers the face recognition and management features of the WhoRang AI Doorbell Integration.

## 🎯 Overview

WhoRang includes sophisticated face recognition capabilities that allow you to:
- **Automatically detect faces** in doorbell images
- **Label unknown faces** with names
- **Recognize known visitors** automatically
- **Manage person profiles** with avatars
- **Track visitor patterns** and statistics

## 🎨 Visual Face Management System

### What are the Visual Face Management Cards?

The WhoRang integration includes **3 sophisticated custom cards** for complete face management:

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

### Setting Up the Visual Face Manager

1. **Copy Dashboard Configuration**:
   - Use the complete dashboard from [`examples/dashboard.yaml`](../../examples/dashboard.yaml)
   - Or add the face manager card to your existing dashboard

2. **Card Configuration Examples**:

   **Full-Featured Face Manager Card:**
   ```yaml
   type: custom:whorang-face-manager-card
   entity: sensor.whorang_ai_doorbell_face_gallery
   whorang_url: http://localhost:3001  # Update to your backend URL
   title: Face Recognition Manager
   columns: 4
   show_progress: true
   show_controls: true
   ```

   **Simple Face Manager Card:**
   ```yaml
   type: custom:whorang-face-manager-simple-card
   entity: sensor.whorang_ai_doorbell_face_gallery
   whorang_url: http://localhost:3001  # Update to your backend URL
   title: Simple Face Manager
   ```

   **Known Persons Gallery Card:**
   ```yaml
   type: custom:whorang-known-persons-card
   entity: sensor.whorang_ai_doorbell_known_persons_gallery
   whorang_url: http://localhost:3001  # Update to your backend URL
   title: Known Persons
   columns: 3
   show_stats: true
   show_last_seen: true
   show_face_count: true
   ```

3. **Configure Backend URL**:
   - Update `whorang_url` to match your WhoRang backend
   - Add-on users: `http://homeassistant.local:3001`
   - Docker users: `http://your-docker-host:3001`

### Using the Visual Interface

#### Step 1: Load Unknown Faces
1. **Trigger Face Detection**: Use the "Get Unknown Faces" button or service
2. **Wait for Loading**: The gallery will populate with detected faces
3. **Review Quality**: Higher quality faces (80%+) are more reliable

#### Step 2: Label Faces
1. **Click to Select**: Click on face thumbnails to select them (blue border)
2. **Enter Name**: Type the person's name in the text field
3. **Label Selected**: Click "Label Selected" to assign the name
4. **Batch Labeling**: Select multiple faces of the same person and label together

#### Step 3: Manage Persons
1. **View Known Persons**: See all labeled persons with their face counts
2. **Edit Persons**: Modify names or add notes
3. **Delete Persons**: Remove persons if needed
4. **Track Statistics**: Monitor recognition accuracy and patterns

## 📊 Face Recognition Entities

### Face Gallery Sensor
**Entity**: `sensor.whorang_ai_doorbell_face_gallery`

This sensor provides comprehensive face data:

```yaml
# Example attributes
unknown_faces:
  - id: 8
    image_url: "http://backend:3001/uploads/faces/face_8.jpg"
    thumbnail_url: "http://backend:3001/uploads/faces/thumb_8.jpg"
    quality_score: 0.85
    confidence: 0.92
    detection_date: "2025-01-11T08:00:00Z"
    description: "Person with brown hair"
    selectable: true

known_persons:
  - id: 1
    name: "John Doe"
    face_count: 5
    last_seen: "2025-01-11T07:30:00Z"
    avatar_url: "http://backend:3001/uploads/avatars/person_1.jpg"
    recognition_count: 12

total_unknown: 3
total_known_persons: 5
labeling_progress: 75
gallery_ready: true
```

### Known Persons Gallery Sensor
**Entity**: `sensor.whorang_ai_doorbell_known_persons_gallery`

Provides detailed information about known persons:

```yaml
# Example attributes
persons:
  - id: 1
    name: "John Doe"
    face_count: 5
    last_seen: "2025-01-11T07:30:00Z"
    avatar_url: "http://backend:3001/uploads/avatars/person_1.jpg"
    avg_confidence: 0.88
    recognition_count: 12
    notes: "Family member"

total_known_persons: 5
total_labeled_faces: 25
avg_faces_per_person: 5.0
gallery_ready: true
```

### Unknown Faces Sensor
**Entity**: `sensor.whorang_ai_doorbell_unknown_faces`

Tracks faces that need labeling:

```yaml
# Example attributes
unknown_faces:
  - face_id: 8
    quality_score: 0.85
    face_image_url: "http://backend:3001/uploads/faces/face_8.jpg"
    thumbnail_url: "http://backend:3001/uploads/faces/thumb_8.jpg"
    created_at: "2025-01-11T08:00:00Z"

face_ids: [8, 12, 15]
requires_labeling: true
next_face_to_label:
  face_id: 8
  quality_score: 0.85
```

## 🛠️ Face Management Services

### Basic Face Labeling

#### Label a Single Face
```yaml
service: whorang.label_face
data:
  face_id: 8
  person_name: "John Doe"
```

#### Create New Person from Face
```yaml
service: whorang.create_person_from_face
data:
  face_id: 8
  person_name: "Jane Smith"
  description: "Neighbor from next door"
```

### Batch Operations

#### Label Multiple Faces
```yaml
service: whorang.batch_label_faces
data:
  face_ids: [8, 12, 15]
  person_name: "John Doe"
  create_person: true
```

#### Get Unknown Faces
```yaml
service: whorang.get_unknown_faces
data:
  limit: 50
  quality_threshold: 0.6
```

### Advanced Operations

#### Find Similar Faces
```yaml
service: whorang.get_face_similarities
data:
  face_id: 8
  threshold: 0.7
  limit: 10
```

#### Delete Unwanted Face
```yaml
service: whorang.delete_face
data:
  face_id: 8
```

## 🤖 Automations for Face Management

### Unknown Face Alert
```yaml
automation:
  - alias: "New Unknown Face Detected"
    trigger:
      - platform: state
        entity_id: sensor.whorang_ai_doorbell_face_gallery
        attribute: total_unknown
    condition:
      - condition: template
        value_template: >
          {{ trigger.to_state.attributes.total_unknown | int > 
             trigger.from_state.attributes.total_unknown | int }}
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🔍 New Unknown Face"
          message: >
            {{ state_attr('sensor.whorang_ai_doorbell_face_gallery', 'total_unknown') }} 
            faces need labeling
          data:
            actions:
              - action: "open_face_manager"
                title: "Label Faces"
```

### Known Person Recognition
```yaml
automation:
  - alias: "Known Person Detected"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_ai_doorbell_known_visitor
        to: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "👋 Known Visitor"
          message: >
            {{ state_attr('binary_sensor.whorang_ai_doorbell_known_visitor', 'person_name') }} 
            is at the door
          data:
            image: "/api/camera_proxy/camera.whorang_ai_doorbell_latest_image"
```

### Daily Face Summary
```yaml
automation:
  - alias: "Daily Face Recognition Summary"
    trigger:
      - platform: time
        at: "20:00:00"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "📊 Daily Face Recognition Summary"
          message: >
            Today: {{ states('sensor.whorang_ai_doorbell_visitors_today') }} visitors, 
            {{ state_attr('sensor.whorang_ai_doorbell_face_gallery', 'total_unknown') }} 
            faces need labeling
```

## 📱 Dashboard Integration

### Face Management Dashboard Section
```yaml
- type: grid
  cards:
    - type: heading
      heading: Face Recognition Manager
    - type: custom:whorang-face-manager-card
      entity: sensor.whorang_ai_doorbell_face_gallery
      whorang_url: http://localhost:3001
      title: Face Recognition Manager
      columns: 4
      show_progress: true
      show_controls: true

- type: grid
  cards:
    - type: heading
      heading: Face Statistics
    - type: entities
      title: Face Recognition Stats
      entities:
        - entity: sensor.whorang_ai_doorbell_known_faces
          name: Known Faces
        - entity: sensor.whorang_ai_doorbell_unknown_faces
          name: Unknown Faces
        - entity: sensor.whorang_ai_doorbell_face_gallery
          name: Labeling Progress
          attribute: labeling_progress
          unit: "%"
```

### Quick Actions Section
```yaml
- type: grid
  cards:
    - type: heading
      heading: Quick Actions
    - type: entities
      title: Face Management Actions
      entities:
        - type: button
          name: Get Unknown Faces
          icon: mdi:face-recognition
          tap_action:
            action: call-service
            service: whorang.get_unknown_faces
            service_data:
              limit: 50
              quality_threshold: 0.3
        - type: button
          name: Refresh Gallery
          icon: mdi:refresh
          tap_action:
            action: call-service
            service: homeassistant.update_entity
            service_data:
              entity_id: sensor.whorang_ai_doorbell_face_gallery
```

## 🔧 Manual Face Labeling

### Using Input Helpers
For manual face labeling without the visual interface:

1. **Create Input Helpers**:
   ```yaml
   input_number:
     face_id_input:
       name: Face ID
       min: 1
       max: 10000
       mode: box

   input_text:
     person_name_input:
       name: Person Name
       max: 100
   ```

2. **Manual Labeling Button**:
   ```yaml
   - type: button
     name: Label Face
     icon: mdi:tag
     tap_action:
       action: call-service
       service: whorang.label_face
       service_data:
         face_id: "{{ states('input_number.face_id_input') | int }}"
         person_name: "{{ states('input_text.person_name_input') }}"
   ```

## 🎯 Best Practices

### Face Quality Guidelines
- **High Quality (80%+)**: Excellent for recognition, use for training
- **Medium Quality (60-80%)**: Good for recognition, acceptable for training
- **Low Quality (<60%)**: May cause false matches, consider deleting

### Labeling Strategy
1. **Start with High Quality**: Label highest quality faces first
2. **Group Similar Faces**: Use batch labeling for multiple faces of same person
3. **Regular Maintenance**: Review and clean up low-quality faces
4. **Consistent Naming**: Use consistent naming conventions

### Privacy Considerations
- **Local Processing**: All face data stays on your system
- **Secure Storage**: Face images stored securely on your backend
- **Access Control**: Limit access to face management interface
- **Data Retention**: Regularly review and clean up old face data

## 🔍 Troubleshooting

### Common Issues

#### Faces Not Appearing
1. **Check Backend Connection**: Verify WhoRang backend is running
2. **Trigger Face Detection**: Use "Get Unknown Faces" service
3. **Check Image URLs**: Verify backend URL in card configuration
4. **Review Logs**: Check Home Assistant logs for errors

#### Poor Recognition Accuracy
1. **Improve Face Quality**: Use higher quality face images for training
2. **Add More Samples**: Label multiple faces of the same person
3. **Clean Up Data**: Remove low-quality or incorrect labels
4. **Adjust Thresholds**: Modify confidence thresholds in backend

#### Visual Interface Not Working
1. **Restart Home Assistant**: Reload custom cards
2. **Check Card Configuration**: Verify whorang_url is correct
3. **Browser Cache**: Clear browser cache and refresh
4. **Check Console**: Look for JavaScript errors in browser console

### Performance Optimization

#### Large Face Databases
- **Pagination**: Use limit parameter in get_unknown_faces
- **Quality Filtering**: Set higher quality thresholds
- **Regular Cleanup**: Remove old or unnecessary faces
- **Batch Processing**: Use batch operations for efficiency

#### Network Performance
- **Local Backend**: Keep backend on same network as Home Assistant
- **Image Optimization**: Backend automatically optimizes thumbnails
- **Caching**: Browser caches face images for better performance

## 📈 Advanced Features

### Face Similarity Analysis
Use face similarities to help with labeling decisions:

```yaml
service: whorang.get_face_similarities
data:
  face_id: 8
  threshold: 0.7
  limit: 5
```

This returns faces that look similar, helping you identify if they're the same person.

### Automated Labeling Workflows
Create automations that suggest labels based on similarity:

```yaml
automation:
  - alias: "Suggest Face Labels"
    trigger:
      - platform: state
        entity_id: sensor.whorang_ai_doorbell_unknown_faces
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.state | int > 0 }}"
    action:
      - service: whorang.get_face_similarities
        data:
          face_id: "{{ state_attr('sensor.whorang_ai_doorbell_unknown_faces', 'next_face_to_label').face_id }}"
          threshold: 0.8
```

### Integration with Other Systems
- **Security Systems**: Trigger alerts for unknown faces
- **Access Control**: Grant access based on face recognition
- **Visitor Logs**: Maintain detailed visitor records
- **Analytics**: Track visitor patterns and statistics

## 🎓 Learning and Improvement

### Recognition Accuracy
The system learns and improves over time:
- **More Samples**: Each labeled face improves recognition
- **Quality Matters**: Higher quality faces provide better training
- **Consistent Lighting**: Faces in similar lighting conditions work better
- **Multiple Angles**: Label faces from different angles for better coverage

### Monitoring Performance
Track recognition performance:
- **Recognition Rate**: Percentage of known visitors correctly identified
- **False Positives**: Unknown visitors incorrectly identified as known
- **False Negatives**: Known visitors not recognized
- **Quality Trends**: Average face quality over time

This comprehensive face management system provides powerful tools for building and maintaining an accurate face recognition database for your doorbell system.
