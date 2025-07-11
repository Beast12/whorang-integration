# Dashboard Examples

This document provides example dashboard configurations for the WhoRang AI Doorbell Integration to help you create effective monitoring and control interfaces.

## Basic Dashboard Card

### Simple Entity Card
```yaml
type: entities
title: WhoRang Doorbell
entities:
  - sensor.whorang_latest_visitor
  - binary_sensor.whorang_doorbell
  - binary_sensor.whorang_known_visitor
  - camera.whorang_latest_image
```

### Picture Entity Card
```yaml
type: picture-entity
entity: camera.whorang_latest_image
name: Latest Visitor
show_state: false
show_name: true
tap_action:
  action: more-info
```

## Advanced Dashboard Layouts

### Grid Layout with Multiple Cards
```yaml
type: grid
columns: 2
square: false
cards:
  - type: picture-entity
    entity: camera.whorang_latest_image
    name: Latest Visitor Image
    show_state: false
    
  - type: entities
    title: Visitor Information
    entities:
      - sensor.whorang_latest_visitor
      - sensor.whorang_visitor_count_today
      - sensor.whorang_visitor_count_week
      - binary_sensor.whorang_known_visitor
```

### Comprehensive Monitoring Dashboard
```yaml
type: vertical-stack
cards:
  - type: horizontal-stack
    cards:
      - type: entity
        entity: sensor.whorang_visitor_count_today
        name: Today
        icon: mdi:account-group
        
      - type: entity
        entity: sensor.whorang_visitor_count_week
        name: This Week
        icon: mdi:calendar-week
        
      - type: entity
        entity: sensor.whorang_visitor_count_month
        name: This Month
        icon: mdi:calendar-month

  - type: picture-entity
    entity: camera.whorang_latest_image
    name: Latest Visitor
    show_state: false
    
  - type: entities
    title: System Status
    entities:
      - binary_sensor.whorang_system_online
      - sensor.whorang_system_status
      - binary_sensor.whorang_ai_processing
      - sensor.whorang_ai_response_time
```

## Control Dashboard

### AI Provider Management
```yaml
type: entities
title: AI Configuration
entities:
  - select.whorang_ai_provider
  - select.whorang_ai_model
  - sensor.whorang_ai_cost_today
  - sensor.whorang_ai_cost_month
```

### Manual Controls
```yaml
type: entities
title: Manual Controls
entities:
  - button.whorang_trigger_analysis
  - button.whorang_refresh_data
  - button.whorang_test_connection
```

## Conditional Cards

### Show Card Only When Visitor Detected
```yaml
type: conditional
conditions:
  - entity: binary_sensor.whorang_doorbell
    state: "on"
card:
  type: entities
  title: Active Visitor
  entities:
    - sensor.whorang_latest_visitor
    - camera.whorang_latest_image
    - binary_sensor.whorang_known_visitor
```

### Unknown Visitor Alert
```yaml
type: conditional
conditions:
  - entity: binary_sensor.whorang_doorbell
    state: "on"
  - entity: binary_sensor.whorang_known_visitor
    state: "off"
card:
  type: markdown
  content: |
    ## ⚠️ Unknown Visitor Detected
    
    **Analysis**: {{ states('sensor.whorang_latest_visitor') }}
    
    **Time**: {{ state_attr('sensor.whorang_latest_visitor', 'timestamp') }}
```

## Statistics Dashboard

### Visitor Analytics
```yaml
type: vertical-stack
cards:
  - type: statistics-graph
    title: Daily Visitors
    entities:
      - sensor.whorang_visitor_count_today
    period: day
    stat_types:
      - mean
      - max
    
  - type: history-graph
    title: Visitor Activity
    entities:
      - sensor.whorang_visitor_count_today
      - binary_sensor.whorang_doorbell
    hours_to_show: 24
```

### AI Cost Tracking
```yaml
type: entities
title: AI Usage & Costs
entities:
  - type: section
    label: Today's Usage
  - sensor.whorang_ai_cost_today
  - sensor.whorang_ai_response_time
  - type: section
    label: Monthly Summary
  - sensor.whorang_ai_cost_month
  - type: section
    label: Provider Settings
  - select.whorang_ai_provider
  - select.whorang_ai_model
```

## Mobile-Optimized Layout

### Compact Mobile Dashboard
```yaml
type: vertical-stack
cards:
  - type: picture-entity
    entity: camera.whorang_latest_image
    name: Latest Visitor
    show_state: false
    aspect_ratio: "16:9"
    
  - type: glance
    entities:
      - entity: sensor.whorang_visitor_count_today
        name: Today
      - entity: binary_sensor.whorang_known_visitor
        name: Known
      - entity: binary_sensor.whorang_system_online
        name: Online
        
  - type: entities
    entities:
      - sensor.whorang_latest_visitor
      - button.whorang_trigger_analysis
```

## Custom Button Card Examples

### Quick Action Buttons
```yaml
type: horizontal-stack
cards:
  - type: button
    entity: button.whorang_trigger_analysis
    name: Analyze Now
    icon: mdi:brain
    tap_action:
      action: call-service
      service: button.press
      target:
        entity_id: button.whorang_trigger_analysis
        
  - type: button
    entity: button.whorang_refresh_data
    name: Refresh
    icon: mdi:refresh
    tap_action:
      action: call-service
      service: button.press
      target:
        entity_id: button.whorang_refresh_data
```

## Automation Integration Cards

### Automation Status
```yaml
type: entities
title: WhoRang Automations
entities:
  - automation.doorbell_notification
  - automation.unknown_visitor_alert
  - automation.known_visitor_welcome
  - automation.daily_visitor_summary
```

## Troubleshooting Dashboard

### System Health Monitoring
```yaml
type: entities
title: System Health
entities:
  - binary_sensor.whorang_system_online
  - sensor.whorang_system_status
  - sensor.whorang_ai_response_time
  - binary_sensor.whorang_ai_processing
  - type: section
    label: Connection Test
  - button.whorang_test_connection
  - type: section
    label: Data Management
  - button.whorang_refresh_data
```

## Tips for Dashboard Design

### Performance Optimization
- Use conditional cards to reduce unnecessary updates
- Limit history graphs to reasonable time periods
- Use glance cards for quick status overview

### User Experience
- Group related entities together
- Use clear, descriptive names
- Include relevant icons for visual clarity
- Consider mobile layout for responsive design

### Accessibility
- Ensure sufficient color contrast
- Use descriptive entity names
- Include status indicators for system health

## Next Steps

- **[Basic Automations](../automation/basic-automations.md)** - Set up essential automations
- **[Configuration Guide](../configuration/initial-setup.md)** - Advanced configuration options
- **[Troubleshooting](../troubleshooting/common-issues.md)** - Solve common issues

---

**Need Help?** Check our [troubleshooting guide](../troubleshooting/common-issues.md) or [open an issue](https://github.com/Beast12/whorang-integration/issues).
