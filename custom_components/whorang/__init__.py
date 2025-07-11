"""The WhoRang AI Doorbell integration."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.components.http import StaticPathConfig

from .api_client import WhoRangAPIClient, WhoRangConnectionError
from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_UPDATE_INTERVAL,
    CONF_ENABLE_WEBSOCKET,
    CONF_ENABLE_COST_TRACKING,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_OLLAMA_HOST,
    DEFAULT_OLLAMA_PORT,
    SERVICE_TRIGGER_ANALYSIS,
    SERVICE_ADD_KNOWN_VISITOR,
    SERVICE_REMOVE_KNOWN_VISITOR,
    SERVICE_SET_AI_PROVIDER,
    SERVICE_SET_AI_MODEL,
    SERVICE_GET_AVAILABLE_MODELS,
    SERVICE_REFRESH_OLLAMA_MODELS,
    SERVICE_TEST_OLLAMA_CONNECTION,
    SERVICE_EXPORT_DATA,
    SERVICE_TEST_WEBHOOK,
    SERVICE_PROCESS_DOORBELL_EVENT,
    SERVICE_LABEL_FACE,
    SERVICE_BATCH_LABEL_FACES,
    SERVICE_CREATE_PERSON_FROM_FACE,
    SERVICE_GET_UNKNOWN_FACES,
    SERVICE_DELETE_FACE,
    SERVICE_GET_FACE_SIMILARITIES,
    # Intelligent Automation Services
    SERVICE_SETUP_CAMERA_AUTOMATION,
    SERVICE_START_INTELLIGENT_MONITORING,
    SERVICE_STOP_INTELLIGENT_MONITORING,
    SERVICE_INTELLIGENT_NOTIFY,
    SERVICE_PLAY_DOORBELL_SEQUENCE,
    SERVICE_CONFIGURE_AI_PROMPT,
    SERVICE_TEST_NOTIFICATION_TEMPLATE,
    EVENT_FACE_LABELED,
    EVENT_PERSON_CREATED,
    EVENT_UNKNOWN_FACE_DETECTED,
)
from .coordinator import WhoRangDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CAMERA,
    Platform.DEVICE_TRACKER,
    Platform.BUTTON,
    Platform.SELECT,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WhoRang AI Doorbell from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    api_key = entry.data.get(CONF_API_KEY)
    
    # Get options with defaults
    update_interval = entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    enable_websocket = entry.options.get(CONF_ENABLE_WEBSOCKET, True)
    enable_cost_tracking = entry.options.get(CONF_ENABLE_COST_TRACKING, True)
    
    # Get Ollama configuration
    ollama_config = entry.data.get("ollama_config", {
        "host": DEFAULT_OLLAMA_HOST,
        "port": DEFAULT_OLLAMA_PORT,
        "enabled": False
    })

    # Create API client with Ollama configuration
    api_client = WhoRangAPIClient(
        host=host,
        port=port,
        api_key=api_key,
        ollama_config=ollama_config
    )

    # Test connection
    try:
        if not await api_client.validate_connection():
            raise ConfigEntryNotReady("Unable to connect to WhoRang system")
    except WhoRangConnectionError as err:
        raise ConfigEntryNotReady(f"Error connecting to WhoRang: {err}") from err

    # Create coordinator
    coordinator = WhoRangDataUpdateCoordinator(
        hass,
        api_client,
        update_interval=update_interval,
        enable_websocket=enable_websocket,
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Set up coordinator
    await coordinator.async_setup()

    # Update Ollama configuration in backend if enabled
    if ollama_config.get("enabled", False):
        try:
            await api_client.set_ollama_config(
                ollama_config.get("host", DEFAULT_OLLAMA_HOST),
                ollama_config.get("port", DEFAULT_OLLAMA_PORT)
            )
            _LOGGER.info("Updated Ollama configuration in WhoRang backend: %s:%s", 
                        ollama_config.get("host"), ollama_config.get("port"))
        except Exception as err:
            _LOGGER.warning("Failed to update Ollama configuration in backend: %s", err)

    # Store coordinator in hass data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register frontend resources for custom cards
    await _async_register_frontend_resources(hass)

    # Register services
    await _async_register_services(hass)

    # Set up options update listener
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def _async_register_frontend_resources(hass: HomeAssistant) -> None:
    """Register frontend resources for custom cards."""
    # Temporarily disabled to avoid registration issues
    # Custom cards can be manually registered via Dashboard Resources
    _LOGGER.info("Frontend resource registration disabled - use manual registration")
    _LOGGER.info("Custom cards available at:")
    _LOGGER.info("- /local/community/whorang/whorang-face-manager.js")
    _LOGGER.info("- /local/community/whorang/whorang-face-manager-simple.js")
    _LOGGER.info("- /local/community/whorang/whorang-known-persons-card.js")
    _LOGGER.info("Manual registration: Settings → Dashboards → Resources")


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Get coordinator
        coordinator: WhoRangDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
        
        # Shutdown coordinator
        await coordinator.async_shutdown()
        
        # Remove from hass data
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def _async_register_services(hass: HomeAssistant) -> None:
    """Register integration services."""
    
    async def trigger_analysis_service(call) -> None:
        """Handle trigger analysis service call."""
        visitor_id = call.data.get("visitor_id")
        
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            success = await coordinator.async_trigger_analysis(visitor_id)
            if success:
                _LOGGER.info("Triggered AI analysis for visitor: %s", visitor_id or "latest")
            else:
                _LOGGER.error("Failed to trigger AI analysis for visitor: %s", visitor_id or "latest")

    async def add_known_visitor_service(call) -> None:
        """Handle add known visitor service call."""
        name = call.data.get("name")
        notes = call.data.get("notes")
        
        if not name:
            _LOGGER.error("Name is required for adding known visitor")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            success = await coordinator.async_add_known_person(name, notes)
            if success:
                _LOGGER.info("Added known visitor: %s", name)
            else:
                _LOGGER.error("Failed to add known visitor: %s", name)

    async def remove_known_visitor_service(call) -> None:
        """Handle remove known visitor service call."""
        person_id = call.data.get("person_id")
        
        if not person_id:
            _LOGGER.error("Person ID is required for removing known visitor")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            success = await coordinator.async_remove_known_person(person_id)
            if success:
                _LOGGER.info("Removed known visitor: %s", person_id)
            else:
                _LOGGER.error("Failed to remove known visitor: %s", person_id)

    async def set_ai_provider_service(call) -> None:
        """Handle set AI provider service call."""
        provider = call.data.get("provider")
        
        if not provider:
            _LOGGER.error("Provider is required for setting AI provider")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            success = await coordinator.async_set_ai_provider(provider)
            if success:
                _LOGGER.info("Set AI provider to: %s", provider)
            else:
                _LOGGER.error("Failed to set AI provider to: %s", provider)

    async def export_data_service(call) -> None:
        """Handle export data service call."""
        start_date = call.data.get("start_date")
        end_date = call.data.get("end_date")
        format_type = call.data.get("format", "json")
        
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            result = await coordinator.async_export_data(start_date, end_date, format_type)
            if result:
                _LOGGER.info("Exported visitor data in %s format", format_type)
            else:
                _LOGGER.error("Failed to export visitor data")

    async def test_webhook_service(call) -> None:
        """Handle test webhook service call."""
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            success = await coordinator.async_test_webhook()
            if success:
                _LOGGER.info("Webhook test successful")
            else:
                _LOGGER.error("Webhook test failed")

    async def set_ai_model_service(call) -> None:
        """Handle set AI model service call."""
        model = call.data.get("model")
        
        if not model:
            _LOGGER.error("Model is required for setting AI model")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            success = await coordinator.api_client.set_ai_model(model)
            if success:
                _LOGGER.info("Set AI model to: %s", model)
                await coordinator.async_request_refresh()
            else:
                _LOGGER.error("Failed to set AI model to: %s", model)

    async def get_available_models_service(call) -> None:
        """Handle get available models service call."""
        provider = call.data.get("provider")
        
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                if provider:
                    models = await coordinator.api_client.get_provider_models(provider)
                    _LOGGER.info("Available models for %s: %s", provider, models)
                else:
                    models = await coordinator.api_client.get_available_models()
                    _LOGGER.info("Available models: %s", models)
            except Exception as err:
                _LOGGER.error("Failed to get available models: %s", err)

    async def refresh_ollama_models_service(call) -> None:
        """Handle refresh Ollama models service call."""
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                # Force refresh of Ollama models
                ollama_models = await coordinator.api_client.get_ollama_models()
                _LOGGER.info("Refreshed Ollama models: found %d models", len(ollama_models))
                
                # Trigger coordinator refresh to update entities
                await coordinator.async_request_refresh()
            except Exception as err:
                _LOGGER.error("Failed to refresh Ollama models: %s", err)

    async def test_ollama_connection_service(call) -> None:
        """Handle test Ollama connection service call."""
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                status = await coordinator.api_client.get_ollama_status()
                if status.get("status") == "connected":
                    _LOGGER.info("Ollama connection test successful: %s", status.get("message", "Connected"))
                else:
                    _LOGGER.warning("Ollama connection test failed: %s", status.get("message", "Disconnected"))
            except Exception as err:
                _LOGGER.error("Failed to test Ollama connection: %s", err)

    async def process_doorbell_event_service(call) -> None:
        """Handle process doorbell event service call."""
        _LOGGER.info("=== DOORBELL EVENT SERVICE CALLED ===")
        _LOGGER.info("Service call data: %s", call.data)
        
        # Extract and validate service call data
        image_url = call.data.get("image_url")
        ai_message = call.data.get("ai_message", "")
        ai_title = call.data.get("ai_title", "")
        location = call.data.get("location", "front_door")
        weather_temp = call.data.get("weather_temp", 20)
        weather_humidity = call.data.get("weather_humidity", 50)
        weather_condition = call.data.get("weather_condition", "unknown")
        wind_speed = call.data.get("wind_speed", 0)
        pressure = call.data.get("pressure", 1013)
        
        if not image_url:
            _LOGGER.error("Image URL is required for processing doorbell event")
            return
            
        # Get coordinators from hass data
        coordinators_data = hass.data.get(DOMAIN, {})
        if not coordinators_data:
            _LOGGER.error("No WhoRang coordinators found in hass data")
            return
        
        coordinators = [
            coordinator for coordinator in coordinators_data.values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        if not coordinators:
            _LOGGER.error("No WhoRangDataUpdateCoordinator instances found")
            return
        
        # Process the doorbell event for each coordinator
        for coordinator in coordinators:
            try:
                _LOGGER.info("Processing doorbell event through coordinator")
                
                # Create comprehensive event data
                event_data = {
                    "image_url": image_url,
                    "ai_message": ai_message,
                    "ai_title": ai_title,
                    "location": location,
                    "weather_temp": weather_temp,
                    "weather_humidity": weather_humidity,
                    "weather_condition": weather_condition,
                    "wind_speed": wind_speed,
                    "pressure": pressure,
                    "timestamp": datetime.now().isoformat(),
                    "source": "service_call"
                }
                
                # Process through coordinator
                success = await coordinator.async_process_doorbell_event(event_data)
                
                if success:
                    _LOGGER.info("Successfully processed doorbell event with image: %s", image_url)
                    
                    # Force immediate coordinator refresh to update all entities
                    _LOGGER.info("Triggering coordinator refresh to update entities")
                    await coordinator.async_request_refresh()
                    
                    # Fire Home Assistant event for automations
                    hass.bus.async_fire("whorang_doorbell_event", {
                        "image_url": image_url,
                        "ai_message": ai_message,
                        "ai_title": ai_title,
                        "weather_data": {
                            "temperature": weather_temp,
                            "humidity": weather_humidity,
                            "condition": weather_condition,
                            "wind_speed": wind_speed,
                            "pressure": pressure
                        },
                        "timestamp": event_data["timestamp"],
                        "source": "service_call"
                    })
                    
                else:
                    _LOGGER.error("Failed to process doorbell event with image: %s", image_url)
                    
            except Exception as err:
                _LOGGER.error("Error processing doorbell event: %s", err, exc_info=True)
        
        _LOGGER.info("=== DOORBELL EVENT SERVICE COMPLETED ===")

    # Face Management Services

    async def label_face_service(call) -> None:
        """Handle label face service call."""
        face_id = call.data.get("face_id")
        person_name = call.data.get("person_name")
        
        if not face_id or not person_name:
            _LOGGER.error("Face ID and person name are required for labeling face")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                success = await coordinator.api_client.label_face_with_name(face_id, person_name)
                if success:
                    _LOGGER.info("Successfully labeled face %s as %s", face_id, person_name)
                    await coordinator.async_request_refresh()
                    
                    # Fire event for automations
                    hass.bus.async_fire(EVENT_FACE_LABELED, {
                        "face_id": face_id,
                        "person_name": person_name,
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    _LOGGER.error("Failed to label face %s as %s", face_id, person_name)
                    
            except Exception as err:
                _LOGGER.error("Error labeling face %s: %s", face_id, err)

    async def batch_label_faces_service(call) -> None:
        """Handle batch label faces service call."""
        face_ids = call.data.get("face_ids", [])
        person_name = call.data.get("person_name")
        create_person = call.data.get("create_person", True)
        
        if not face_ids or not person_name:
            _LOGGER.error("Face IDs list and person name are required for batch labeling faces")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                result = await coordinator.api_client.batch_label_faces(face_ids, person_name, create_person)
                labeled_count = result.get("labeled_count", 0)
                
                if labeled_count > 0:
                    _LOGGER.info("Successfully batch labeled %d faces as %s", labeled_count, person_name)
                    await coordinator.async_request_refresh()
                    
                    # Fire event for automations
                    hass.bus.async_fire(EVENT_FACE_LABELED, {
                        "face_ids": face_ids,
                        "person_name": person_name,
                        "labeled_count": labeled_count,
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    _LOGGER.error("Failed to batch label faces as %s", person_name)
                    
            except Exception as err:
                _LOGGER.error("Error batch labeling faces: %s", err)

    async def create_person_from_face_service(call) -> None:
        """Handle create person from face service call."""
        face_id = call.data.get("face_id")
        person_name = call.data.get("person_name")
        description = call.data.get("description", "")
        
        if not face_id or not person_name:
            _LOGGER.error("Face ID and person name are required for creating person from face")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                success = await coordinator.api_client.create_person_from_face(face_id, person_name, description)
                if success:
                    _LOGGER.info("Successfully created person %s from face %s", person_name, face_id)
                    await coordinator.async_request_refresh()
                    
                    # Fire events for automations
                    hass.bus.async_fire(EVENT_PERSON_CREATED, {
                        "person_name": person_name,
                        "description": description,
                        "face_id": face_id,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    hass.bus.async_fire(EVENT_FACE_LABELED, {
                        "face_id": face_id,
                        "person_name": person_name,
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    _LOGGER.error("Failed to create person %s from face %s", person_name, face_id)
                    
            except Exception as err:
                _LOGGER.error("Error creating person from face %s: %s", face_id, err)

    async def get_unknown_faces_service(call) -> None:
        """Handle get unknown faces service call."""
        limit = call.data.get("limit", 50)
        quality_threshold = call.data.get("quality_threshold", 0.0)
        
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                unknown_faces = await coordinator.api_client.get_unassigned_faces(
                    limit=limit, 
                    quality_threshold=quality_threshold
                )
                
                _LOGGER.info("Retrieved %d unknown faces requiring labeling", len(unknown_faces))
                
                # Update coordinator data with unknown faces
                if coordinator.data is None:
                    coordinator.data = {}
                coordinator.data["unknown_faces"] = unknown_faces
                coordinator.async_set_updated_data(coordinator.data)
                
                # Fire event for automations
                if unknown_faces:
                    hass.bus.async_fire(EVENT_UNKNOWN_FACE_DETECTED, {
                        "unknown_faces_count": len(unknown_faces),
                        "faces": unknown_faces,
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except Exception as err:
                _LOGGER.error("Error getting unknown faces: %s", err)

    async def delete_face_service(call) -> None:
        """Handle delete face service call."""
        face_id = call.data.get("face_id")
        
        if not face_id:
            _LOGGER.error("Face ID is required for deleting face")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                success = await coordinator.api_client.delete_face(face_id)
                if success:
                    _LOGGER.info("Successfully deleted face %s", face_id)
                    await coordinator.async_request_refresh()
                else:
                    _LOGGER.error("Failed to delete face %s", face_id)
                    
            except Exception as err:
                _LOGGER.error("Error deleting face %s: %s", face_id, err)

    async def get_face_similarities_service(call) -> None:
        """Handle get face similarities service call."""
        face_id = call.data.get("face_id")
        threshold = call.data.get("threshold", 0.6)
        limit = call.data.get("limit", 10)
        
        if not face_id:
            _LOGGER.error("Face ID is required for getting face similarities")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                similarities = await coordinator.api_client.get_face_similarities(
                    face_id, threshold=threshold, limit=limit
                )
                
                _LOGGER.info("Found %d similar faces for face %s", len(similarities), face_id)
                
                # Update coordinator data with similarities
                if coordinator.data is None:
                    coordinator.data = {}
                coordinator.data["face_similarities"] = {
                    "target_face_id": face_id,
                    "similarities": similarities,
                    "threshold": threshold,
                    "timestamp": datetime.now().isoformat()
                }
                coordinator.async_set_updated_data(coordinator.data)
                    
            except Exception as err:
                _LOGGER.error("Error getting face similarities for %s: %s", face_id, err)

    # Person Management Services

    async def update_person_service(call) -> None:
        """Handle update person service call."""
        person_id = call.data.get("person_id")
        name = call.data.get("name")
        description = call.data.get("description")
        
        if not person_id:
            _LOGGER.error("Person ID is required for updating person")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                success = await coordinator.api_client.update_person(person_id, {
                    "name": name,
                    "description": description
                })
                if success:
                    _LOGGER.info("Successfully updated person %s", person_id)
                    await coordinator.async_request_refresh()
                else:
                    _LOGGER.error("Failed to update person %s", person_id)
                    
            except Exception as err:
                _LOGGER.error("Error updating person %s: %s", person_id, err)

    async def get_person_details_service(call) -> None:
        """Handle get person details service call."""
        person_id = call.data.get("person_id")
        
        if not person_id:
            _LOGGER.error("Person ID is required for getting person details")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                person_details = await coordinator.api_client.get_person_details(person_id)
                if person_details:
                    _LOGGER.info("Retrieved details for person %s: %s", person_id, person_details.get("name", "Unknown"))
                    
                    # Update coordinator data with person details
                    if coordinator.data is None:
                        coordinator.data = {}
                    coordinator.data["person_details"] = {
                        "person_id": person_id,
                        "details": person_details,
                        "timestamp": datetime.now().isoformat()
                    }
                    coordinator.async_set_updated_data(coordinator.data)
                else:
                    _LOGGER.error("Failed to get details for person %s", person_id)
                    
            except Exception as err:
                _LOGGER.error("Error getting person details for %s: %s", person_id, err)

    async def merge_persons_service(call) -> None:
        """Handle merge persons service call."""
        source_person_id = call.data.get("source_person_id")
        target_person_id = call.data.get("target_person_id")
        
        if not source_person_id or not target_person_id:
            _LOGGER.error("Both source and target person IDs are required for merging persons")
            return
            
        if source_person_id == target_person_id:
            _LOGGER.error("Source and target person IDs cannot be the same")
            return
            
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        for coordinator in coordinators:
            try:
                success = await coordinator.api_client.merge_persons(source_person_id, target_person_id)
                if success:
                    _LOGGER.info("Successfully merged person %s into person %s", source_person_id, target_person_id)
                    await coordinator.async_request_refresh()
                else:
                    _LOGGER.error("Failed to merge person %s into person %s", source_person_id, target_person_id)
                    
            except Exception as err:
                _LOGGER.error("Error merging persons %s -> %s: %s", source_person_id, target_person_id, err)

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_TRIGGER_ANALYSIS,
        trigger_analysis_service,
        schema=vol.Schema({
            vol.Optional("visitor_id"): str,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_KNOWN_VISITOR,
        add_known_visitor_service,
        schema=vol.Schema({
            vol.Required("name"): str,
            vol.Optional("notes"): str,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_REMOVE_KNOWN_VISITOR,
        remove_known_visitor_service,
        schema=vol.Schema({
            vol.Required("person_id"): int,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_AI_PROVIDER,
        set_ai_provider_service,
        schema=vol.Schema({
            vol.Required("provider"): vol.In(["openai", "local", "claude", "gemini", "google-cloud-vision"]),
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_EXPORT_DATA,
        export_data_service,
        schema=vol.Schema({
            vol.Optional("start_date"): str,
            vol.Optional("end_date"): str,
            vol.Optional("format", default="json"): vol.In(["json", "csv"]),
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_TEST_WEBHOOK,
        test_webhook_service,
        schema=vol.Schema({}),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_AI_MODEL,
        set_ai_model_service,
        schema=vol.Schema({
            vol.Required("model"): str,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_AVAILABLE_MODELS,
        get_available_models_service,
        schema=vol.Schema({
            vol.Optional("provider"): vol.In(["local", "openai", "claude", "gemini", "google-cloud-vision"]),
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH_OLLAMA_MODELS,
        refresh_ollama_models_service,
        schema=vol.Schema({}),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_TEST_OLLAMA_CONNECTION,
        test_ollama_connection_service,
        schema=vol.Schema({}),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_PROCESS_DOORBELL_EVENT,
        process_doorbell_event_service,
        schema=vol.Schema({
            vol.Required("image_url"): str,
            vol.Optional("ai_message"): str,
            vol.Optional("ai_title"): str,
            vol.Optional("location", default="front_door"): str,
            vol.Optional("weather_temp"): vol.Any(vol.Coerce(float), str),  # Allow templates
            vol.Optional("weather_humidity"): vol.Any(vol.Coerce(int), str),  # Allow templates
            vol.Optional("weather_condition"): str,
            vol.Optional("wind_speed"): vol.Any(vol.Coerce(float), str),  # Allow templates
            vol.Optional("pressure"): vol.Any(vol.Coerce(float), str),  # Allow templates
        }),
    )

    # Register face management services
    hass.services.async_register(
        DOMAIN,
        SERVICE_LABEL_FACE,
        label_face_service,
        schema=vol.Schema({
            vol.Required("face_id"): int,
            vol.Required("person_name"): str,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_BATCH_LABEL_FACES,
        batch_label_faces_service,
        schema=vol.Schema({
            vol.Required("face_ids"): [int],
            vol.Required("person_name"): str,
            vol.Optional("create_person", default=True): bool,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CREATE_PERSON_FROM_FACE,
        create_person_from_face_service,
        schema=vol.Schema({
            vol.Required("face_id"): int,
            vol.Required("person_name"): str,
            vol.Optional("description"): str,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_UNKNOWN_FACES,
        get_unknown_faces_service,
        schema=vol.Schema({
            vol.Optional("limit", default=50): vol.All(int, vol.Range(min=1, max=200)),
            vol.Optional("quality_threshold", default=0.0): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=1.0)),
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_DELETE_FACE,
        delete_face_service,
        schema=vol.Schema({
            vol.Required("face_id"): int,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_FACE_SIMILARITIES,
        get_face_similarities_service,
        schema=vol.Schema({
            vol.Required("face_id"): int,
            vol.Optional("threshold", default=0.6): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=1.0)),
            vol.Optional("limit", default=10): vol.All(int, vol.Range(min=1, max=50)),
        }),
    )

    # Register person management services
    hass.services.async_register(
        DOMAIN,
        "update_person",
        update_person_service,
        schema=vol.Schema({
            vol.Required("person_id"): int,
            vol.Optional("name"): str,
            vol.Optional("description"): str,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        "get_person_details",
        get_person_details_service,
        schema=vol.Schema({
            vol.Required("person_id"): int,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        "merge_persons",
        merge_persons_service,
        schema=vol.Schema({
            vol.Required("source_person_id"): int,
            vol.Required("target_person_id"): int,
        }),
    )

    # Intelligent Automation Services (HA 2025+ Compatible)

    async def setup_camera_automation_service(call) -> Dict[str, Any]:
        """Handle setup camera automation service call."""
        from .intelligent_automation import IntelligentAutomationEngine
        
        camera_entity = call.data.get("camera_entity")
        monitor_mode = call.data.get("monitor_mode", "state_change")
        ai_prompt_template = call.data.get("ai_prompt_template", "professional")
        custom_ai_prompt = call.data.get("custom_ai_prompt", "")
        enable_notifications = call.data.get("enable_notifications", True)
        enable_media = call.data.get("enable_media", True)
        enable_weather_context = call.data.get("enable_weather_context", True)
        
        if not camera_entity:
            _LOGGER.error("Camera entity is required for setting up automation")
            return {"success": False, "error": "Camera entity is required"}
        
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        results = []
        for coordinator in coordinators:
            try:
                # Create automation configuration
                automation_config = {
                    "enable_intelligent_automation": True,
                    "camera_entity": camera_entity,
                    "camera_monitor_mode": monitor_mode,
                    "ai_prompt_template": ai_prompt_template,
                    "custom_ai_prompt": custom_ai_prompt,
                    "enable_notifications": enable_notifications,
                    "enable_media": enable_media,
                    "enable_weather_context": enable_weather_context,
                    "notification_devices": [],  # Will be configured separately
                    "media_players": [],  # Will be configured separately
                    "display_players": [],  # Will be configured separately
                }
                
                # Store automation engine in coordinator
                if not hasattr(coordinator, 'automation_engine'):
                    coordinator.automation_engine = IntelligentAutomationEngine(
                        hass, coordinator, automation_config
                    )
                else:
                    # Update existing configuration
                    coordinator.automation_engine.config.update(automation_config)
                
                _LOGGER.info("Successfully configured camera automation for %s", camera_entity)
                results.append({
                    "coordinator": str(coordinator),
                    "success": True,
                    "camera_entity": camera_entity
                })
                
            except Exception as err:
                _LOGGER.error("Failed to setup camera automation: %s", err)
                results.append({
                    "coordinator": str(coordinator),
                    "success": False,
                    "error": str(err)
                })
        
        return {
            "success": any(r["success"] for r in results),
            "results": results,
            "camera_entity": camera_entity
        }

    async def start_intelligent_monitoring_service(call) -> Dict[str, Any]:
        """Handle start intelligent monitoring service call."""
        camera_entity = call.data.get("camera_entity")
        
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        results = []
        for coordinator in coordinators:
            try:
                if hasattr(coordinator, 'automation_engine'):
                    # Update camera entity if provided
                    if camera_entity:
                        coordinator.automation_engine.config["camera_entity"] = camera_entity
                    
                    success = await coordinator.automation_engine.async_start()
                    if success:
                        _LOGGER.info("Successfully started intelligent monitoring")
                        results.append({"coordinator": str(coordinator), "success": True})
                    else:
                        _LOGGER.error("Failed to start intelligent monitoring")
                        results.append({"coordinator": str(coordinator), "success": False, "error": "Failed to start"})
                else:
                    _LOGGER.error("No automation engine configured. Run setup_camera_automation first.")
                    results.append({"coordinator": str(coordinator), "success": False, "error": "No automation engine"})
                    
            except Exception as err:
                _LOGGER.error("Error starting intelligent monitoring: %s", err)
                results.append({"coordinator": str(coordinator), "success": False, "error": str(err)})
        
        return {
            "success": any(r["success"] for r in results),
            "results": results
        }

    async def stop_intelligent_monitoring_service(call) -> Dict[str, Any]:
        """Handle stop intelligent monitoring service call."""
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        results = []
        for coordinator in coordinators:
            try:
                if hasattr(coordinator, 'automation_engine'):
                    success = await coordinator.automation_engine.async_stop()
                    if success:
                        _LOGGER.info("Successfully stopped intelligent monitoring")
                        results.append({"coordinator": str(coordinator), "success": True})
                    else:
                        _LOGGER.error("Failed to stop intelligent monitoring")
                        results.append({"coordinator": str(coordinator), "success": False, "error": "Failed to stop"})
                else:
                    _LOGGER.warning("No automation engine to stop")
                    results.append({"coordinator": str(coordinator), "success": True, "message": "No engine to stop"})
                    
            except Exception as err:
                _LOGGER.error("Error stopping intelligent monitoring: %s", err)
                results.append({"coordinator": str(coordinator), "success": False, "error": str(err)})
        
        return {
            "success": any(r["success"] for r in results),
            "results": results
        }

    async def intelligent_notify_service(call) -> Dict[str, Any]:
        """Handle intelligent notification service call."""
        from .intelligent_automation import IntelligentNotificationService
        
        template = call.data.get("template", "rich_media")
        devices = call.data.get("devices", [])
        ai_result = call.data.get("ai_result", {})
        snapshot_url = call.data.get("snapshot_url")
        event_id = call.data.get("event_id", "manual")
        
        if not devices or not snapshot_url:
            _LOGGER.error("Devices and snapshot URL are required for intelligent notifications")
            return {"success": False, "error": "Missing required parameters"}
        
        try:
            # Extract device entity IDs from target selector
            device_list = []
            if isinstance(devices, dict) and "entity_id" in devices:
                if isinstance(devices["entity_id"], list):
                    device_list = devices["entity_id"]
                else:
                    device_list = [devices["entity_id"]]
            elif isinstance(devices, list):
                device_list = devices
            
            # Create notification service
            notification_service = IntelligentNotificationService(
                hass, device_list, template
            )
            
            # Send notifications
            result = await notification_service.send_notifications(
                ai_result, snapshot_url, event_id
            )
            
            _LOGGER.info("Intelligent notification result: %s", result)
            return result
            
        except Exception as err:
            _LOGGER.error("Error sending intelligent notifications: %s", err)
            return {"success": False, "error": str(err)}

    async def play_doorbell_sequence_service(call) -> Dict[str, Any]:
        """Handle play doorbell sequence service call."""
        from .intelligent_automation import MediaIntegrationService
        
        sequence_type = call.data.get("sequence_type", "full")
        ai_message = call.data.get("ai_message", "")
        snapshot_url = call.data.get("snapshot_url", "")
        target_players = call.data.get("target_players", [])
        display_players = call.data.get("display_players", [])
        doorbell_sound_file = call.data.get("doorbell_sound_file", "/local/sounds/doorbell.mp3")
        tts_service = call.data.get("tts_service")
        display_duration = call.data.get("display_duration", 15)
        
        try:
            # Extract player entity IDs from target selectors
            media_player_list = []
            display_player_list = []
            
            if isinstance(target_players, dict) and "entity_id" in target_players:
                if isinstance(target_players["entity_id"], list):
                    media_player_list = target_players["entity_id"]
                else:
                    media_player_list = [target_players["entity_id"]]
            elif isinstance(target_players, list):
                media_player_list = target_players
            
            if isinstance(display_players, dict) and "entity_id" in display_players:
                if isinstance(display_players["entity_id"], list):
                    display_player_list = display_players["entity_id"]
                else:
                    display_player_list = [display_players["entity_id"]]
            elif isinstance(display_players, list):
                display_player_list = display_players
            
            # Create media service
            media_service = MediaIntegrationService(
                hass,
                media_player_list,
                display_player_list,
                doorbell_sound_file,
                tts_service,
                display_duration
            )
            
            # Play sequence based on type
            if sequence_type == "full":
                result = await media_service.play_doorbell_sequence(
                    ai_message, snapshot_url, "manual"
                )
            elif sequence_type == "sound_only":
                await media_service._play_doorbell_sound()
                result = {"success": True, "actions": ["doorbell_sound"]}
            elif sequence_type == "tts_only":
                await media_service._play_tts_announcement(ai_message)
                result = {"success": True, "actions": ["tts_announcement"]}
            elif sequence_type == "display_only":
                await media_service._display_snapshot(snapshot_url)
                result = {"success": True, "actions": ["snapshot_display"]}
            else:
                result = {"success": False, "error": "Invalid sequence type"}
            
            _LOGGER.info("Doorbell sequence result: %s", result)
            return result
            
        except Exception as err:
            _LOGGER.error("Error playing doorbell sequence: %s", err)
            return {"success": False, "error": str(err)}

    async def configure_ai_prompt_service(call) -> Dict[str, Any]:
        """Handle configure AI prompt service call."""
        template = call.data.get("template")
        custom_prompt = call.data.get("custom_prompt", "")
        max_tokens = call.data.get("max_tokens", 150)
        temperature = call.data.get("temperature", 0.2)
        enable_weather_context = call.data.get("enable_weather_context", True)
        
        if not template:
            _LOGGER.error("Template is required for configuring AI prompt")
            return {"success": False, "error": "Template is required"}
        
        # Get all coordinators
        coordinators = [
            coordinator for coordinator in hass.data[DOMAIN].values()
            if isinstance(coordinator, WhoRangDataUpdateCoordinator)
        ]
        
        results = []
        for coordinator in coordinators:
            try:
                if hasattr(coordinator, 'automation_engine'):
                    # Update AI prompt configuration
                    coordinator.automation_engine.config.update({
                        "ai_prompt_template": template,
                        "custom_ai_prompt": custom_prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "enable_weather_context": enable_weather_context
                    })
                    
                    _LOGGER.info("Successfully configured AI prompt template: %s", template)
                    results.append({
                        "coordinator": str(coordinator),
                        "success": True,
                        "template": template
                    })
                else:
                    _LOGGER.error("No automation engine configured. Run setup_camera_automation first.")
                    results.append({
                        "coordinator": str(coordinator),
                        "success": False,
                        "error": "No automation engine"
                    })
                    
            except Exception as err:
                _LOGGER.error("Error configuring AI prompt: %s", err)
                results.append({
                    "coordinator": str(coordinator),
                    "success": False,
                    "error": str(err)
                })
        
        return {
            "success": any(r["success"] for r in results),
            "results": results,
            "template": template
        }

    async def test_notification_template_service(call) -> Dict[str, Any]:
        """Handle test notification template service call."""
        from .intelligent_automation import IntelligentNotificationService
        
        template = call.data.get("template")
        devices = call.data.get("devices", [])
        test_message = call.data.get("test_message", "This is a test notification from WhoRang intelligent automation")
        test_title = call.data.get("test_title", "WhoRang Test")
        test_image_url = call.data.get("test_image_url", "")
        
        if not template or not devices:
            _LOGGER.error("Template and devices are required for testing notifications")
            return {"success": False, "error": "Missing required parameters"}
        
        try:
            # Extract device entity IDs from target selector
            device_list = []
            if isinstance(devices, dict) and "entity_id" in devices:
                if isinstance(devices["entity_id"], list):
                    device_list = devices["entity_id"]
                else:
                    device_list = [devices["entity_id"]]
            elif isinstance(devices, list):
                device_list = devices
            
            # Create test AI result
            test_ai_result = {
                "title": test_title,
                "description": test_message,
                "confidence": 0.9,
                "faces_detected": 1,
                "objects_detected": ["person"],
                "processing_time": 1.5,
                "ai_provider": "test",
                "cost_usd": 0.0
            }
            
            # Create notification service
            notification_service = IntelligentNotificationService(
                hass, device_list, template
            )
            
            # Send test notifications
            result = await notification_service.send_notifications(
                test_ai_result,
                test_image_url or "http://homeassistant.local:8123/local/test_image.jpg",
                "test"
            )
            
            _LOGGER.info("Test notification result: %s", result)
            return result
            
        except Exception as err:
            _LOGGER.error("Error testing notification template: %s", err)
            return {"success": False, "error": str(err)}

    # Register intelligent automation services with HA 2025+ features
    hass.services.async_register(
        DOMAIN,
        SERVICE_SETUP_CAMERA_AUTOMATION,
        setup_camera_automation_service,
        schema=vol.Schema({
            vol.Required("camera_entity"): str,
            vol.Optional("monitor_mode", default="state_change"): vol.In(["state_change", "webhook", "manual"]),
            vol.Optional("ai_prompt_template", default="professional"): vol.In(["professional", "friendly", "sarcastic", "detailed", "custom"]),
            vol.Optional("custom_ai_prompt"): str,
            vol.Optional("enable_notifications", default=True): bool,
            vol.Optional("enable_media", default=True): bool,
            vol.Optional("enable_weather_context", default=True): bool,
        }),
        supports_response=True,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_START_INTELLIGENT_MONITORING,
        start_intelligent_monitoring_service,
        schema=vol.Schema({
            vol.Optional("camera_entity"): str,
        }),
        supports_response=True,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_STOP_INTELLIGENT_MONITORING,
        stop_intelligent_monitoring_service,
        schema=vol.Schema({}),
        supports_response=True,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_INTELLIGENT_NOTIFY,
        intelligent_notify_service,
        schema=vol.Schema({
            vol.Optional("template", default="rich_media"): vol.In(["rich_media", "simple", "custom"]),
            vol.Required("devices"): vol.Any(dict, list),  # Target selector or list
            vol.Required("ai_result"): dict,
            vol.Required("snapshot_url"): str,
            vol.Optional("event_id"): str,
        }),
        supports_response=True,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_PLAY_DOORBELL_SEQUENCE,
        play_doorbell_sequence_service,
        schema=vol.Schema({
            vol.Optional("sequence_type", default="full"): vol.In(["full", "sound_only", "tts_only", "display_only"]),
            vol.Optional("ai_message"): str,
            vol.Optional("snapshot_url"): str,
            vol.Optional("target_players"): vol.Any(dict, list),  # Target selector or list
            vol.Optional("display_players"): vol.Any(dict, list),  # Target selector or list
            vol.Optional("doorbell_sound_file", default="/local/sounds/doorbell.mp3"): str,
            vol.Optional("tts_service"): str,
            vol.Optional("display_duration", default=15): vol.All(int, vol.Range(min=5, max=300)),
        }),
        supports_response=True,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CONFIGURE_AI_PROMPT,
        configure_ai_prompt_service,
        schema=vol.Schema({
            vol.Required("template"): vol.In(["professional", "friendly", "sarcastic", "detailed", "custom"]),
            vol.Optional("custom_prompt"): str,
            vol.Optional("max_tokens", default=150): vol.All(int, vol.Range(min=50, max=500)),
            vol.Optional("temperature", default=0.2): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=1.0)),
            vol.Optional("enable_weather_context", default=True): bool,
        }),
        supports_response=True,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_TEST_NOTIFICATION_TEMPLATE,
        test_notification_template_service,
        schema=vol.Schema({
            vol.Required("template"): vol.In(["rich_media", "simple", "custom"]),
            vol.Required("devices"): vol.Any(dict, list),  # Target selector or list
            vol.Optional("test_message", default="This is a test notification from WhoRang intelligent automation"): str,
            vol.Optional("test_title", default="WhoRang Test"): str,
            vol.Optional("test_image_url"): str,
        }),
        supports_response=True,
    )
