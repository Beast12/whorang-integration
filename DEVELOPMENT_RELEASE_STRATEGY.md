# WhoRang Development Release Strategy

## 🎯 Development Release: v1.1.0-dev

**Purpose**: Continuous development release for the Intelligent Notification System  
**Strategy**: Keep updating the same `v1.1.0-dev` tag for ongoing development  
**Benefit**: Users can reinstall the same version without changing release numbers  

## 📋 Release Structure

### Stable Releases
- **v1.0.0** - Current stable release (production)
- **v1.1.0** - Future stable release (when development is complete)

### Development Releases
- **v1.1.0-dev** - Active development release (continuously updated)

## 🚀 Development Workflow

### 1. Create Initial Development Release
```bash
# Tag the current state as v1.1.0-dev
git add .
git commit -m "feat: Intelligent Notification System v1.1.0-dev

- Added IntelligentAutomationEngine for zero-config automation
- Added 7 new intelligent automation services
- Added AI prompt templates (professional, friendly, sarcastic, detailed, custom)
- Added notification templates (rich_media, simple, custom)
- Added media integration (sound + TTS + display)
- Added weather context integration
- Added HA 2025+ compatibility features

BREAKING: This is a development release for testing new features"

git tag -a v1.1.0-dev -m "Development release: Intelligent Notification System

Features:
- Zero-configuration intelligent automation
- Template-based AI prompts and notifications
- Media integration with parallel execution
- Weather context integration
- HA 2025+ compatibility

This is a development release for testing purposes."

git push origin main
git push origin v1.1.0-dev
```

### 2. Continuous Development Updates
```bash
# For each development iteration:
git add .
git commit -m "feat: [description of changes]"

# Update the same development tag (force push)
git tag -f v1.1.0-dev -m "Updated development release: [description]"
git push origin main
git push -f origin v1.1.0-dev
```

### 3. User Installation
Users can install the development version with:
```yaml
# In HACS or manual installation
Repository: https://github.com/Beast12/whorang-integration
Version: v1.1.0-dev
```

Users can **reinstall the same version** to get updates without changing version numbers.

## 📦 Release Management

### Development Phase (Current)
- **Version**: `1.1.0-dev`
- **Tag**: `v1.1.0-dev` (continuously updated)
- **Purpose**: Active development and testing
- **Update Strategy**: Force push to same tag

### Stable Release (Future)
- **Version**: `1.1.0`
- **Tag**: `v1.1.0` (final release)
- **Purpose**: Production deployment
- **Update Strategy**: New tag, no force push

## 🔄 Development Cycle

### Phase 1: Feature Development ✅
- [x] Intelligent Automation Engine
- [x] AI Prompt Templates
- [x] Notification Templates
- [x] Media Integration
- [x] Weather Context
- [x] Service Implementation

### Phase 2: Testing & Refinement (Current)
- [ ] User testing and feedback
- [ ] Bug fixes and improvements
- [ ] Performance optimization
- [ ] Documentation updates

### Phase 3: Stable Release (Future)
- [ ] Final testing
- [ ] Create v1.1.0 stable release
- [ ] Update documentation
- [ ] Announce stable release

## 🛠️ Commands for Development

### Create Development Release
```bash
# Initial development release
git tag -a v1.1.0-dev -m "Development release: Intelligent Notification System"
git push origin v1.1.0-dev
```

### Update Development Release
```bash
# Update existing development release
git tag -f v1.1.0-dev -m "Updated: [description of changes]"
git push -f origin v1.1.0-dev
```

### Create Stable Release (When Ready)
```bash
# Final stable release
git tag -a v1.1.0 -m "Stable release: Intelligent Notification System"
git push origin v1.1.0
```

## 📋 Version Management

### manifest.json
```json
{
  "version": "1.1.0-dev"
}
```

### const.py
```python
SW_VERSION: Final = "1.1.0-dev"
```

## 🎯 Benefits of This Strategy

### For Development
- ✅ **Continuous Updates**: Same tag, continuous development
- ✅ **No Version Confusion**: Users always know it's development
- ✅ **Easy Testing**: Users can reinstall same version for updates
- ✅ **Clear Separation**: Dev vs stable releases clearly marked

### For Users
- ✅ **Easy Installation**: Install `v1.1.0-dev` once
- ✅ **Easy Updates**: Reinstall same version to get updates
- ✅ **Clear Expectations**: `-dev` suffix indicates development status
- ✅ **Stable Fallback**: Can always return to `v1.0.0` stable

## 🚨 Important Notes

### Development Release Warnings
- **Development Status**: This is a development release for testing
- **Potential Issues**: May contain bugs or incomplete features
- **Breaking Changes**: Features may change during development
- **Backup Recommended**: Always backup before installing development releases

### Force Push Considerations
- **Development Only**: Only force push development tags, never stable releases
- **Communication**: Inform users when significant updates are pushed
- **Documentation**: Keep changelog updated for development changes

## 📝 Changelog for v1.1.0-dev

### Added ✅
- **IntelligentAutomationEngine**: Master orchestrator for automation
- **CameraMonitoringService**: Automatic camera state monitoring
- **IntelligentNotificationService**: Template-based notifications
- **MediaIntegrationService**: Sound + TTS + display coordination
- **WeatherContextService**: Automatic weather context integration
- **AI Prompt Templates**: 5 built-in templates (professional, friendly, sarcastic, detailed, custom)
- **Notification Templates**: 3 built-in templates (rich_media, simple, custom)
- **7 New Services**: Complete intelligent automation service suite
- **HA 2025+ Features**: Service responses, target selectors, modern schemas

### Enhanced ✅
- **Zero Configuration**: Users configure camera entity, WhoRang handles the rest
- **Parallel Execution**: All automation actions run concurrently
- **Error Handling**: Comprehensive error recovery and logging
- **Event System**: Rich event system for automation integration
- **Template Engine**: Jinja2 template support for notifications and prompts

### Technical ✅
- **700+ Lines**: New intelligent automation engine
- **30+ Constants**: New configuration options and templates
- **300+ Lines**: Service implementation with HA 2025+ compatibility
- **Backward Compatible**: All existing features preserved and enhanced

This development release transforms WhoRang from a monitoring system into a complete intelligent automation platform.
