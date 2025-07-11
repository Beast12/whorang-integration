# Changelog

All notable changes to the WhoRang AI Doorbell Integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-08

### Added
- Initial HACS-compliant release
- Complete Home Assistant integration with 19+ entities
- Multi-provider AI support (OpenAI, Claude, Gemini, Google Cloud Vision, Ollama)
- Real-time WebSocket integration for instant updates
- Comprehensive API key management system
- Dynamic AI model selection for all providers
- Face recognition with known visitor tracking
- Visitor statistics and analytics
- AI cost tracking and usage monitoring
- Device tracker entities for known persons
- 6 custom services for automation and management
- 4 event types for advanced automation triggers
- Complete configuration flow with validation
- Options flow for ongoing management
- Extensive documentation and automation examples

### Features
- **Sensors (9)**: Latest visitor, counts, system status, AI metrics
- **Binary Sensors (5)**: Doorbell, motion, known visitor, connectivity
- **Camera (1)**: Latest doorbell image with auto-updates
- **Controls (5)**: AI provider/model selection, manual triggers
- **Device Trackers**: Dynamic presence tracking for known visitors
- **Services (6)**: Complete API for automation and management
- **Events (4)**: Rich automation triggers

### Technical Details
- **Minimum HA Version**: 2023.1.0
- **IoT Class**: Local Push (WebSocket + API)
- **Configuration**: UI-based config flow with validation
- **Dependencies**: aiohttp>=3.8.0, websockets>=11.0
- **Quality Scale**: Silver (HACS compliant)

### Backend Compatibility
- **Requires**: WhoRang Add-on v1.0.0+
- **Repository**: [WhoRang Add-on](https://github.com/Beast12/whorang-addon)
- **Installation**: Home Assistant Add-on Store or Docker deployment

### Documentation
- Complete installation guides for all HA installation types
- Comprehensive configuration reference
- 15+ automation examples for common use cases
- Troubleshooting guides for common issues
- API reference for all services and entities

### Security
- Encrypted API key storage in Home Assistant configuration
- Secure transmission of credentials to backend
- Real-time validation with provider-specific testing
- No sensitive data exposed in logs or debug output

### Performance
- WebSocket-based real-time updates (no polling delays)
- Efficient SSL context management
- Smart caching and data coordination
- Graceful error handling and automatic recovery

---

## Version Compatibility Matrix

| Integration Version | Add-on Version | Release Date | Notes |
|-------------------|----------------|--------------|-------|
| 1.0.0 | 1.0.0 | 2025-01-08 | Initial HACS release |

## Migration Notes

### From Legacy Repository
If you were using the integration from the legacy `who-rang` repository:

1. **Backup Configuration**: Export your current settings and known faces
2. **Remove Legacy Integration**: Delete from custom_components
3. **Install via HACS**: Follow the new installation process
4. **Restore Configuration**: Re-configure using the new setup flow
5. **Verify Functionality**: Test all entities and automations

### Breaking Changes
- Repository URL changed from `Beast12/who-rang` to `Beast12/whorang-integration`
- Backend now distributed separately via `Beast12/whorang-addon`
- Configuration flow enhanced with additional validation steps

## Support

- **Issues**: [GitHub Issues](https://github.com/Beast12/whorang-integration/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Beast12/whorang-integration/discussions)
- **Documentation**: [Complete Documentation](https://github.com/Beast12/whorang-integration/blob/main/README.md)
- **Community**: [Home Assistant Community](https://community.home-assistant.io/)

## Contributing

Contributions are welcome! Please see the [Contributing Guide](CONTRIBUTING.md) for details on:
- Code style and standards
- Testing requirements
- Documentation updates
- Release process
