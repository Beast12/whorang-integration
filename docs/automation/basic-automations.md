# Basic Automations Guide

This guide provides essential automation examples for the WhoRang AI Doorbell Integration, perfect for new users getting started.

## Quick Start Automations

### 1. Essential Doorbell Notification

**Purpose**: Get notified whenever someone rings the doorbell with AI analysis.

```yaml
automation:
  - alias: "Doorbell Notification"
    description: "Send notification when doorbell is pressed"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_doorbell
        to: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🔔 Doorbell"
          message: "{{ states('sensor.whorang_latest_visitor') }}"
          data:
            image: "/api/camera_proxy/camera.whorang_latest_image"
            actions:
              - action: "view_visitor"
                title: "View Details"
              - action: "trigger_analysis"
                title: "Re-analyze"
```

**Customization**:
- Replace `your_phone` with your device name
- Add multiple notification services for family members
- Customize message format and actions

### 2. Known Visitor Welcome

**Purpose**: Welcome known visitors with personalized messages.

```yaml
automation:
  - alias: "Welcome Known Visitor"
    description: "Welcome known visitors with TTS announcement"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_known_visitor
        to: "on"
    action:
      - service: tts.google_translate_say
        data:
          entity_id: media_player.living_room_speaker
          message: >
            Welcome home, {{ state_attr('binary_sensor.whorang_known_visitor', 'person_name') }}!
      - service: light.turn_on
        target:
          entity_id: light.porch_light
        data:
          brightness: 255
          color_name: "green"
```

**Customization**:
- Change TTS service and media player
- Add custom actions (lights, locks, etc.)
- Personalize messages per person

### 3. Unknown Visitor Security Alert

**Purpose**: Enhanced security notifications for unknown visitors.

```yaml
automation:
  - alias: "Unknown Visitor Security Alert"
    description: "Security alert for unknown visitors"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_doorbell
        to: "on"
    condition:
      - condition: state
        entity_id: binary_sensor.whorang_known_visitor
        state: "off"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🚨 Unknown Visitor"
          message: "{{ states('sensor.whorang_latest_visitor') }}"
          data:
            image: "/api/camera_proxy/camera.whorang_latest_image"
            actions:
              - action: "trigger_analysis"
                title: "Analyze Visitor"
              - action: "add_known_visitor"
                title: "Add as Known"
            tag: "security_alert"
            group: "doorbell"
      - service: light.turn_on
        target:
          entity_id: light.security_lights
        data:
          brightness: 255
          color_name: "red"
```

### 4. Motion Detection Alert

**Purpose**: Get notified of motion even without doorbell press.

```yaml
automation:
  - alias: "Motion Detection Alert"
    description: "Alert on motion detection"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_motion
        to: "on"
    condition:
      - condition: state
        entity_id: binary_sensor.whorang_doorbell
        state: "off"
        for:
          minutes: 2
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "👁️ Motion Detected"
          message: "Motion detected at front door"
          data:
            image: "/api/camera_proxy/camera.whorang_latest_image"
            tag: "motion_alert"
```

## Time-Based Automations

### 5. Night Mode Security

**Purpose**: Enhanced security during night hours.

```yaml
automation:
  - alias: "Night Mode Doorbell Alert"
    description: "Enhanced security alerts during night hours"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_doorbell
        to: "on"
    condition:
      - condition: time
        after: "22:00:00"
        before: "06:00:00"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🌙 Night Visitor Alert"
          message: "Doorbell activity during night hours: {{ states('sensor.whorang_latest_visitor') }}"
          data:
            image: "/api/camera_proxy/camera.whorang_latest_image"
            tag: "night_alert"
            group: "security"
      - service: light.turn_on
        target:
          entity_id: light.all_security_lights
        data:
          brightness: 255
      - service: camera.record
        target:
          entity_id: camera.whorang_latest_image
        data:
          duration: 30
```

### 6. Away Mode Enhanced Security

**Purpose**: Special handling when nobody is home.

```yaml
automation:
  - alias: "Away Mode Doorbell Alert"
    description: "Enhanced alerts when away from home"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_doorbell
        to: "on"
    condition:
      - condition: state
        entity_id: group.family
        state: "not_home"
    action:
      - service: notify.family_group
        data:
          title: "🏠 Visitor While Away"
          message: "{{ states('sensor.whorang_latest_visitor') }}"
          data:
            image: "/api/camera_proxy/camera.whorang_latest_image"
            actions:
              - action: "view_live_feed"
                title: "View Live"
              - action: "trigger_analysis"
                title: "Re-analyze"
            tag: "away_alert"
            group: "security"
      - service: script.security_recording
```

## AI and Cost Management

### 7. AI Cost Monitoring

**Purpose**: Monitor and alert on AI usage costs.

```yaml
automation:
  - alias: "AI Cost Alert"
    description: "Alert when daily AI costs exceed threshold"
    trigger:
      - platform: numeric_state
        entity_id: sensor.whorang_ai_cost_today
        above: 1.00  # $1.00 threshold
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "💰 AI Cost Alert"
          message: "Daily AI costs have exceeded $1.00. Current: ${{ states('sensor.whorang_ai_cost_today') }}"
      - service: select.select_option
        target:
          entity_id: select.whorang_ai_provider
        data:
          option: "local"  # Switch to free local provider
```

### 8. Automatic AI Provider Switching

**Purpose**: Switch to cost-effective providers during high usage.

```yaml
automation:
  - alias: "Smart AI Provider Management"
    description: "Switch to cost-effective providers based on usage"
    trigger:
      - platform: numeric_state
        entity_id: sensor.whorang_visitor_count_today
        above: 10
    condition:
      - condition: state
        entity_id: select.whorang_ai_provider
        state: "openai"
    action:
      - service: select.select_option
        target:
          entity_id: select.whorang_ai_provider
        data:
          option: "local"
      - service: notify.mobile_app_your_phone
        data:
          title: "🤖 AI Provider Switched"
          message: "Switched to local AI provider due to high usage today"
```

## System Health Monitoring

### 9. System Offline Alert

**Purpose**: Get notified when the WhoRang system goes offline.

```yaml
automation:
  - alias: "WhoRang System Offline Alert"
    description: "Alert when WhoRang system goes offline"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_system_online
        to: "off"
        for:
          minutes: 5
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "⚠️ WhoRang System Offline"
          message: "WhoRang doorbell system is not responding"
          data:
            tag: "system_alert"
            group: "maintenance"
      - service: persistent_notification.create
        data:
          title: "WhoRang System Issue"
          message: "The WhoRang doorbell system appears to be offline. Check the backend service."
          notification_id: "whorang_offline"
```

### 10. System Recovery Notification

**Purpose**: Confirm when the system comes back online.

```yaml
automation:
  - alias: "WhoRang System Recovery"
    description: "Notify when system comes back online"
    trigger:
      - platform: state
        entity_id: binary_sensor.whorang_system_online
        to: "on"
    condition:
      - condition: state
        entity_id: binary_sensor.whorang_system_online
        state: "off"
        for:
          minutes: 5
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "✅ WhoRang System Online"
          message: "WhoRang doorbell system is back online"
          data:
            tag: "system_recovery"
      - service: persistent_notification.dismiss
        data:
          notification_id: "whorang_offline"
```

## Advanced Automations

### 11. Package Delivery Detection

**Purpose**: Detect and log package deliveries.

```yaml
automation:
  - alias: "Package Delivery Detection"
    description: "Detect package deliveries using AI analysis"
    trigger:
      - platform: state
        entity_id: sensor.whorang_latest_visitor
    condition:
      - condition: template
        value_template: >
          {{ 'package' in states('sensor.whorang_latest_visitor') | lower or
             'delivery' in states('sensor.whorang_latest_visitor') | lower or
             'ups' in states('sensor.whorang_latest_visitor') | lower or
             'fedex' in states('sensor.whorang_latest_visitor') | lower or
             'amazon' in states('sensor.whorang_latest_visitor') | lower }}
    action:
      - service: notify.family_group
        data:
          title: "📦 Package Delivery"
          message: "Package delivery detected: {{ states('sensor.whorang_latest_visitor') }}"
          data:
            image: "/api/camera_proxy/camera.whorang_latest_image"
            tag: "package_delivery"
      - service: logbook.log
        data:
          name: "Package Delivery"
          message: "{{ states('sensor.whorang_latest_visitor') }}"
          entity_id: sensor.whorang_latest_visitor
```

### 12. Visitor Statistics Summary

**Purpose**: Daily summary of visitor activity.

```yaml
automation:
  - alias: "Daily Visitor Summary"
    description: "Send daily summary of visitor activity"
    trigger:
      - platform: time
        at: "20:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.whorang_visitor_count_today
        above: 0
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "📊 Daily Visitor Summary"
          message: >
            Today's Activity:
            • Total Visitors: {{ states('sensor.whorang_visitor_count_today') }}
            • Known Visitors: {{ state_attr('sensor.whorang_visitor_count_today', 'known_count') | default(0) }}
            • AI Cost: ${{ states('sensor.whorang_ai_cost_today') }}
            • System Status: {{ states('sensor.whorang_system_status') }}
```

## Notification Action Handlers

### 13. Notification Action Responses

**Purpose**: Handle actions from notification buttons.

```yaml
automation:
  - alias: "Handle Doorbell Notification Actions"
    description: "Handle actions from doorbell notifications"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "trigger_analysis"
    action:
      - service: button.press
        target:
          entity_id: button.whorang_trigger_analysis

  - alias: "Handle View Visitor Action"
    description: "Handle view visitor action from notifications"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "view_visitor"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "Latest Visitor Details"
          message: >
            Visitor: {{ states('sensor.whorang_latest_visitor') }}
            Time: {{ state_attr('sensor.whorang_latest_visitor', 'timestamp') }}
            Known: {{ state_attr('sensor.whorang_latest_visitor', 'face_recognized') }}
            Confidence: {{ state_attr('sensor.whorang_latest_visitor', 'confidence') }}%
```

## Customization Tips

### Personalizing Notifications

**Device Names**: Replace `mobile_app_your_phone` with your actual device:
- Find your device: **Settings** → **Devices & Services** → **Mobile App**
- Common formats: `mobile_app_johns_iphone`, `mobile_app_pixel_7`

**Notification Services**: Use appropriate notification services:
- Single device: `notify.mobile_app_device_name`
- Multiple devices: `notify.family_group`
- All devices: `notify.notify`

**Message Customization**: Enhance messages with entity attributes:
```yaml
message: >
  {{ states('sensor.whorang_latest_visitor') }}
  Time: {{ state_attr('sensor.whorang_latest_visitor', 'timestamp') }}
  Confidence: {{ state_attr('sensor.whorang_latest_visitor', 'confidence') }}%
```

### Conditional Logic

**Time-based conditions**:
```yaml
condition:
  - condition: time
    after: "08:00:00"
    before: "22:00:00"
    weekday:
      - mon
      - tue
      - wed
      - thu
      - fri
```

**State-based conditions**:
```yaml
condition:
  - condition: state
    entity_id: input_boolean.vacation_mode
    state: "off"
  - condition: numeric_state
    entity_id: sensor.whorang_visitor_count_today
    below: 10
```

## Testing Your Automations

### Manual Testing

1. **Test Triggers**:
   - Use `button.whorang_trigger_analysis` to simulate doorbell
   - Manually toggle binary sensors in Developer Tools

2. **Check Conditions**:
   - Use Template Editor to test condition logic
   - Verify entity states and attributes

3. **Validate Actions**:
   - Test notification services separately
   - Check service call responses

### Automation Debugging

1. **Enable Automation Tracing**:
   - **Settings** → **Automations & Scenes** → Select automation → **Traces**

2. **Check Logs**:
   - **Settings** → **System** → **Logs**
   - Filter for automation-related errors

3. **Use Automation Editor**:
   - Visual editor helps identify syntax issues
   - Test mode allows safe testing

## Next Steps

After setting up basic automations:

1. **[Advanced Automations](advanced-automations.md)** - Complex automation patterns
2. **[Dashboard Examples](../usage/dashboard-examples.md)** - Create monitoring dashboards
3. **[Services Reference](../usage/services-reference.md)** - Explore all available services
4. **[Troubleshooting](../troubleshooting/common-issues.md)** - Solve common automation issues

---

**Need Help?** Check our [troubleshooting guide](../troubleshooting/common-issues.md) or [open an issue](https://github.com/Beast12/whorang-integration/issues).
