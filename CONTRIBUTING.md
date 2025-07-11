# Contributing to WhoRang AI Doorbell Integration

Thank you for your interest in contributing to the WhoRang AI Doorbell Integration! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Release Process](#release-process)

## Code of Conduct

This project follows the [Home Assistant Code of Conduct](https://www.home-assistant.io/code_of_conduct/). By participating, you are expected to uphold this code.

## Getting Started

### Types of Contributions

We welcome several types of contributions:

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Implement bug fixes or new features
- **Documentation**: Improve or expand documentation
- **Testing**: Help test new features and bug fixes
- **Translations**: Add or improve translations

### Before Contributing

1. **Search existing issues** to avoid duplicates
2. **Read the documentation** to understand current functionality
3. **Check the roadmap** for planned features
4. **Join discussions** on existing issues or start new ones

## Development Setup

### Prerequisites

- **Home Assistant Development Environment**
- **Python 3.11+**
- **Git**
- **WhoRang Backend** (for testing)

### Local Development Setup

1. **Fork the Repository**:
   ```bash
   git clone https://github.com/your-username/whorang-integration.git
   cd whorang-integration
   ```

2. **Set Up Development Environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

3. **Install in Home Assistant**:
   ```bash
   # Link to your HA custom_components directory
   ln -s $(pwd)/custom_components/whorang /path/to/homeassistant/custom_components/whorang
   ```

4. **Set Up Pre-commit Hooks**:
   ```bash
   pre-commit install
   ```

### Development Dependencies

Create `requirements-dev.txt`:
```
homeassistant>=2023.1.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-homeassistant-custom-component>=0.13.0
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.0.0
pre-commit>=3.0.0
```

## Contributing Guidelines

### Issue Guidelines

#### Bug Reports
- Use the bug report template
- Include detailed reproduction steps
- Provide logs and configuration details
- Test with the latest version

#### Feature Requests
- Use the feature request template
- Explain the use case and problem being solved
- Consider implementation complexity
- Be open to alternative solutions

### Code Contributions

#### Getting Started
1. **Create an issue** first to discuss the change
2. **Fork the repository** and create a feature branch
3. **Make your changes** following coding standards
4. **Test thoroughly** including edge cases
5. **Update documentation** as needed
6. **Submit a pull request**

#### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

## Pull Request Process

### Before Submitting

1. **Ensure all tests pass**:
   ```bash
   pytest tests/
   ```

2. **Run code quality checks**:
   ```bash
   black custom_components/whorang/
   isort custom_components/whorang/
   flake8 custom_components/whorang/
   mypy custom_components/whorang/
   ```

3. **Update documentation** if needed

4. **Update CHANGELOG.md** with your changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in development environment
4. **Documentation review** if applicable
5. **Final approval** and merge

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specific guidelines:

#### Code Formatting
- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Sorted with isort

#### Type Hints
```python
from typing import Any, Dict, Optional

async def example_function(
    param1: str,
    param2: Optional[int] = None
) -> Dict[str, Any]:
    """Example function with proper type hints."""
    return {"result": param1}
```

#### Error Handling
```python
import logging

_LOGGER = logging.getLogger(__name__)

try:
    result = await api_call()
except ApiException as err:
    _LOGGER.error("API call failed: %s", err)
    raise HomeAssistantError(f"Failed to connect: {err}") from err
```

#### Async/Await
```python
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up integration from config entry."""
    coordinator = WhoRangDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    return True
```

### Home Assistant Specific Guidelines

#### Entity Naming
```python
class WhoRangSensor(CoordinatorEntity, SensorEntity):
    """WhoRang sensor entity."""
    
    def __init__(self, coordinator: WhoRangDataUpdateCoordinator, key: str) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{key}"
        self._attr_name = f"WhoRang {key.replace('_', ' ').title()}"
```

#### Configuration Flow
```python
class WhoRangConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow."""
    
    VERSION = 1
    
    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle user step."""
        errors = {}
        
        if user_input is not None:
            try:
                await self._test_connection(user_input)
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input
                )
            except ConnectionError:
                errors["base"] = "cannot_connect"
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=3001): int,
            }),
            errors=errors
        )
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py
├── test_config_flow.py
├── test_coordinator.py
├── test_sensor.py
├── test_binary_sensor.py
└── fixtures/
    ├── __init__.py
    └── api_responses.py
```

### Writing Tests

#### Unit Tests
```python
import pytest
from homeassistant.core import HomeAssistant
from custom_components.whorang.sensor import WhoRangSensor

async def test_sensor_state(hass: HomeAssistant, mock_coordinator):
    """Test sensor state."""
    sensor = WhoRangSensor(mock_coordinator, "visitor_count")
    
    # Test initial state
    assert sensor.state is None
    
    # Update coordinator data
    mock_coordinator.data = {"visitor_count": 5}
    await sensor.async_update()
    
    assert sensor.state == 5
```

#### Integration Tests
```python
async def test_config_flow_success(hass: HomeAssistant, mock_api):
    """Test successful config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data={
            CONF_HOST: "localhost",
            CONF_PORT: 3001,
        }
    )
    
    assert result["type"] == "create_entry"
    assert result["title"] == "localhost"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config_flow.py

# Run with coverage
pytest --cov=custom_components.whorang

# Run with verbose output
pytest -v
```

## Documentation

### Documentation Standards

#### Docstrings
```python
async def async_update_data(self) -> Dict[str, Any]:
    """Fetch data from WhoRang API.
    
    Returns:
        Dict containing the latest data from WhoRang backend.
        
    Raises:
        UpdateFailed: When communication with API fails.
    """
```

#### README Updates
- Keep installation instructions current
- Update feature lists for new functionality
- Include new configuration options
- Add automation examples for new features

#### Code Comments
```python
# Calculate confidence score based on face recognition results
confidence = (face_match_score * 0.7) + (ai_analysis_score * 0.3)

# WebSocket connection requires special handling for SSL contexts
if self._use_ssl:
    ssl_context = self._create_ssl_context()
    websocket = await websockets.connect(ws_url, ssl=ssl_context)
```

### Documentation Types

1. **API Documentation**: Document all public methods and classes
2. **User Documentation**: Installation, configuration, and usage guides
3. **Developer Documentation**: Architecture, contributing guidelines
4. **Automation Examples**: Real-world usage examples

## Release Process

### Version Management

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Update version** in `manifest.json`
2. **Update CHANGELOG.md** with release notes
3. **Run full test suite**
4. **Update documentation** if needed
5. **Create GitHub release** with release notes
6. **Test HACS installation** from release

### Release Notes Format

```markdown
## [1.1.0] - 2025-01-15

### Added
- New AI model selection entity
- Support for Ollama dynamic model discovery
- Enhanced cost tracking features

### Changed
- Improved WebSocket connection handling
- Updated configuration flow validation

### Fixed
- Fixed SSL context creation blocking event loop
- Resolved entity state update delays

### Backend Compatibility
- Requires WhoRang Add-on v1.1.0+
- Backward compatible with v1.0.x backends
```

## Getting Help

### Development Questions
- **GitHub Discussions**: For general development questions
- **Issues**: For specific bugs or feature requests
- **Code Review**: Submit draft PRs for early feedback

### Resources
- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)
- [Home Assistant Architecture](https://developers.home-assistant.io/docs/architecture/)
- [Integration Development](https://developers.home-assistant.io/docs/creating_integration_manifest/)

## Recognition

Contributors will be recognized in:
- **CHANGELOG.md**: Credit for specific contributions
- **README.md**: Major contributors section
- **GitHub**: Contributor statistics and graphs

Thank you for contributing to WhoRang AI Doorbell Integration! 🎉
