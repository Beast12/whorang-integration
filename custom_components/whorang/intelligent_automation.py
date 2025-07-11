"""Intelligent Automation Engine for WhoRang AI Doorbell."""
from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiohttp
from homeassistant.core import HomeAssistant, Event, callback
from homeassistant.helpers import template
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.util import dt as dt_util
from homeassistant.components.camera import async_get_image
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    AI_PROMPT_TEMPLATES,
    NOTIFICATION_TEMPLATES,
    DEFAULT_DISPLAY_DURATION,
    EVENT_DOORBELL_DETECTED,
    EVENT_CAMERA_SNAPSHOT_CAPTURED,
    EVENT_INTELLIGENT_ANALYSIS_COMPLETE,
    EVENT_NOTIFICATION_SENT,
    EVENT_MEDIA_PLAYBACK_COMPLETE,
    EVENT_AUTOMATION_STARTED,
    EVENT_AUTOMATION_STOPPED,
)

_LOGGER = logging.getLogger(__name__)


class IntelligentAutomationEngine:
    """Main engine for intelligent doorbell automation."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator,
        config: Dict[str, Any]
    ) -> None:
        """Initialize the intelligent automation engine."""
        self.hass = hass
        self.coordinator = coordinator
        self.config = config
        self._is_running = False
        self._camera_monitor = None
        self._notification_service = None
        self._media_service = None
        self._weather_service = None
        self._unsubscribe_listeners = []

    async def async_start(self) -> bool:
        """Start the intelligent automation engine."""
        if self._is_running:
            _LOGGER.warning("Intelligent automation is already running")
            return False

        try:
            # Initialize services
            await self._initialize_services()

            # Start camera monitoring if enabled
            if self.config.get("enable_intelligent_automation", False):
                await self._start_camera_monitoring()

            self._is_running = True
            
            # Fire automation started event
            self.hass.bus.async_fire(EVENT_AUTOMATION_STARTED, {
                "timestamp": dt_util.utcnow().isoformat(),
                "config": self._get_sanitized_config()
            })

            _LOGGER.info("Intelligent automation engine started successfully")
            return True

        except Exception as err:
            _LOGGER.error("Failed to start intelligent automation engine: %s", err)
            return False

    async def async_stop(self) -> bool:
        """Stop the intelligent automation engine."""
        if not self._is_running:
            return True

        try:
            # Stop camera monitoring
            await self._stop_camera_monitoring()

            # Unsubscribe from all listeners
            for unsubscribe in self._unsubscribe_listeners:
                unsubscribe()
            self._unsubscribe_listeners.clear()

            self._is_running = False

            # Fire automation stopped event
            self.hass.bus.async_fire(EVENT_AUTOMATION_STOPPED, {
                "timestamp": dt_util.utcnow().isoformat()
            })

            _LOGGER.info("Intelligent automation engine stopped successfully")
            return True

        except Exception as err:
            _LOGGER.error("Failed to stop intelligent automation engine: %s", err)
            return False

    async def _initialize_services(self) -> None:
        """Initialize all automation services."""
        # Initialize camera monitoring service
        self._camera_monitor = CameraMonitoringService(
            self.hass,
            self.config.get("camera_entity"),
            self.config.get("camera_monitor_mode", "state_change")
        )

        # Initialize notification service
        self._notification_service = IntelligentNotificationService(
            self.hass,
            self.config.get("notification_devices", []),
            self.config.get("notification_template", "rich_media")
        )

        # Initialize media service
        self._media_service = MediaIntegrationService(
            self.hass,
            self.config.get("media_players", []),
            self.config.get("display_players", []),
            self.config.get("doorbell_sound_file"),
            self.config.get("tts_service"),
            self.config.get("display_duration", DEFAULT_DISPLAY_DURATION)
        )

        # Initialize weather service
        self._weather_service = WeatherContextService(
            self.hass,
            self.config.get("weather_entity")
        )

    async def _start_camera_monitoring(self) -> None:
        """Start monitoring the configured camera."""
        if not self._camera_monitor:
            return

        # Register callback for camera events
        self._camera_monitor.register_callback(self._handle_camera_event)

        # Start monitoring
        await self._camera_monitor.start_monitoring()

    async def _stop_camera_monitoring(self) -> None:
        """Stop camera monitoring."""
        if self._camera_monitor:
            await self._camera_monitor.stop_monitoring()

    async def _handle_camera_event(self, event_data: Dict[str, Any]) -> None:
        """Handle camera event and trigger full automation pipeline."""
        event_id = str(uuid.uuid4())
        
        try:
            _LOGGER.info("=== INTELLIGENT AUTOMATION PIPELINE STARTED ===")
            _LOGGER.info("Event ID: %s", event_id)

            # Fire doorbell detected event
            self.hass.bus.async_fire(EVENT_DOORBELL_DETECTED, {
                "event_id": event_id,
                "camera_entity": event_data.get("camera_entity"),
                "timestamp": dt_util.utcnow().isoformat()
            })

            # Step 1: Capture camera snapshot
            snapshot_data = await self._capture_camera_snapshot(event_data)
            if not snapshot_data:
                _LOGGER.error("Failed to capture camera snapshot")
                return

            # Fire snapshot captured event
            self.hass.bus.async_fire(EVENT_CAMERA_SNAPSHOT_CAPTURED, {
                "event_id": event_id,
                "snapshot_path": snapshot_data["path"],
                "snapshot_url": snapshot_data["url"],
                "timestamp": dt_util.utcnow().isoformat()
            })

            # Step 2: Get weather context if enabled
            weather_context = {}
            if self.config.get("enable_weather_context", True):
                weather_context = await self._weather_service.get_weather_context()

            # Step 3: Perform AI analysis with custom prompt and weather context
            ai_result = await self._perform_ai_analysis(
                snapshot_data,
                weather_context,
                event_id
            )

            if not ai_result:
                _LOGGER.error("Failed to perform AI analysis")
                return

            # Fire AI analysis complete event
            self.hass.bus.async_fire(EVENT_INTELLIGENT_ANALYSIS_COMPLETE, {
                "event_id": event_id,
                "ai_result": ai_result,
                "weather_context": weather_context,
                "timestamp": dt_util.utcnow().isoformat()
            })

            # Step 4: Execute parallel automation tasks
            tasks = []

            # Send notifications if enabled
            if self.config.get("enable_notifications", True):
                tasks.append(self._send_intelligent_notifications(
                    ai_result, snapshot_data, event_id
                ))

            # Handle media if enabled
            if self.config.get("enable_media", True):
                tasks.append(self._handle_media_sequence(
                    ai_result, snapshot_data, event_id
                ))

            # Send to WhoRang backend
            tasks.append(self._send_to_whorang_backend(
                ai_result, snapshot_data, weather_context, event_id
            ))

            # Execute all tasks in parallel
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

            _LOGGER.info("=== INTELLIGENT AUTOMATION PIPELINE COMPLETED ===")

        except Exception as err:
            _LOGGER.error("Error in intelligent automation pipeline: %s", err, exc_info=True)

    async def _capture_camera_snapshot(self, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Capture snapshot from camera entity."""
        camera_entity = event_data.get("camera_entity") or self.config.get("camera_entity")
        
        if not camera_entity:
            _LOGGER.error("No camera entity configured for snapshot")
            return None

        try:
            # Generate unique filename
            timestamp = int(dt_util.utcnow().timestamp())
            filename = f"whorang_intelligent_snapshot_{timestamp}.jpg"
            file_path = f"/config/www/{filename}"
            
            # Capture snapshot using HA camera service
            await self.hass.services.async_call(
                "camera",
                "snapshot",
                {
                    "entity_id": camera_entity,
                    "filename": file_path
                },
                blocking=True
            )

            # Generate URL for the snapshot
            snapshot_url = f"{self.hass.config.external_url or 'http://homeassistant.local:8123'}/local/{filename}"

            return {
                "path": file_path,
                "url": snapshot_url,
                "filename": filename,
                "camera_entity": camera_entity
            }

        except Exception as err:
            _LOGGER.error("Failed to capture camera snapshot: %s", err)
            return None

    async def _perform_ai_analysis(
        self,
        snapshot_data: Dict[str, Any],
        weather_context: Dict[str, Any],
        event_id: str
    ) -> Optional[Dict[str, Any]]:
        """Perform AI analysis with custom prompt and weather context."""
        try:
            # Get AI prompt configuration
            prompt_template = self.config.get("ai_prompt_template", "professional")
            custom_prompt = self.config.get("custom_ai_prompt", "")

            # Build AI prompt
            if prompt_template == "custom" and custom_prompt:
                prompt_config = {
                    "prompt": custom_prompt,
                    "max_tokens": 150,
                    "temperature": 0.2
                }
            else:
                prompt_config = AI_PROMPT_TEMPLATES.get(prompt_template, AI_PROMPT_TEMPLATES["professional"])

            # Add weather context to prompt if available
            enhanced_prompt = prompt_config["prompt"]
            if weather_context:
                weather_info = f"\n\nCurrent weather: {weather_context.get('condition', 'unknown')}, {weather_context.get('temperature', 'unknown')}°C"
                enhanced_prompt += weather_info

            # Send to WhoRang backend for AI analysis
            analysis_data = {
                "image_url": snapshot_data["url"],
                "custom_prompt": enhanced_prompt,
                "max_tokens": prompt_config.get("max_tokens", 150),
                "temperature": prompt_config.get("temperature", 0.2),
                "weather_context": weather_context,
                "event_id": event_id
            }

            # Use existing coordinator API to trigger analysis
            result = await self.coordinator.api_client.trigger_intelligent_analysis(analysis_data)

            if result and result.get("success"):
                return {
                    "title": result.get("title", "Doorbell"),
                    "description": result.get("description", "Visitor detected"),
                    "confidence": result.get("confidence", 0.8),
                    "faces_detected": result.get("faces_detected", 0),
                    "objects_detected": result.get("objects_detected", []),
                    "processing_time": result.get("processing_time", 0),
                    "ai_provider": result.get("ai_provider", "unknown"),
                    "cost_usd": result.get("cost_usd", 0.0)
                }

            return None

        except Exception as err:
            _LOGGER.error("Failed to perform AI analysis: %s", err)
            return None

    async def _send_intelligent_notifications(
        self,
        ai_result: Dict[str, Any],
        snapshot_data: Dict[str, Any],
        event_id: str
    ) -> None:
        """Send intelligent notifications to configured devices."""
        try:
            result = await self._notification_service.send_notifications(
                ai_result,
                snapshot_data["url"],
                event_id
            )

            # Fire notification sent event
            self.hass.bus.async_fire(EVENT_NOTIFICATION_SENT, {
                "event_id": event_id,
                "notification_result": result,
                "timestamp": dt_util.utcnow().isoformat()
            })

        except Exception as err:
            _LOGGER.error("Failed to send intelligent notifications: %s", err)

    async def _handle_media_sequence(
        self,
        ai_result: Dict[str, Any],
        snapshot_data: Dict[str, Any],
        event_id: str
    ) -> None:
        """Handle media sequence (sounds, TTS, displays)."""
        try:
            result = await self._media_service.play_doorbell_sequence(
                ai_result["description"],
                snapshot_data["url"],
                event_id
            )

            # Fire media playback complete event
            self.hass.bus.async_fire(EVENT_MEDIA_PLAYBACK_COMPLETE, {
                "event_id": event_id,
                "media_result": result,
                "timestamp": dt_util.utcnow().isoformat()
            })

        except Exception as err:
            _LOGGER.error("Failed to handle media sequence: %s", err)

    async def _send_to_whorang_backend(
        self,
        ai_result: Dict[str, Any],
        snapshot_data: Dict[str, Any],
        weather_context: Dict[str, Any],
        event_id: str
    ) -> None:
        """Send event data to WhoRang backend for storage and processing."""
        try:
            # Use existing process_doorbell_event service
            await self.hass.services.async_call(
                DOMAIN,
                "process_doorbell_event",
                {
                    "image_url": snapshot_data["url"],
                    "ai_message": ai_result["description"],
                    "ai_title": ai_result["title"],
                    "location": "front_door",
                    "weather_temp": weather_context.get("temperature", 20),
                    "weather_humidity": weather_context.get("humidity", 50),
                    "weather_condition": weather_context.get("condition", "unknown"),
                    "wind_speed": weather_context.get("wind_speed", 0),
                    "pressure": weather_context.get("pressure", 1013)
                },
                blocking=False
            )

        except Exception as err:
            _LOGGER.error("Failed to send data to WhoRang backend: %s", err)

    def _get_sanitized_config(self) -> Dict[str, Any]:
        """Get sanitized configuration for events (remove sensitive data)."""
        sanitized = self.config.copy()
        # Remove any sensitive information
        sanitized.pop("api_key", None)
        return sanitized

    @property
    def is_running(self) -> bool:
        """Return if the automation engine is running."""
        return self._is_running


class CameraMonitoringService:
    """Service for monitoring camera entity changes."""

    def __init__(
        self,
        hass: HomeAssistant,
        camera_entity: Optional[str],
        monitor_mode: str = "state_change"
    ) -> None:
        """Initialize camera monitoring service."""
        self.hass = hass
        self.camera_entity = camera_entity
        self.monitor_mode = monitor_mode
        self._callback = None
        self._unsubscribe = None

    def register_callback(self, callback) -> None:
        """Register callback for camera events."""
        self._callback = callback

    async def start_monitoring(self) -> bool:
        """Start monitoring camera entity."""
        if not self.camera_entity:
            _LOGGER.error("No camera entity configured for monitoring")
            return False

        try:
            if self.monitor_mode == "state_change":
                # Monitor camera state changes
                self._unsubscribe = async_track_state_change_event(
                    self.hass,
                    [self.camera_entity],
                    self._handle_camera_state_change
                )
                _LOGGER.info("Started camera state monitoring for %s", self.camera_entity)

            elif self.monitor_mode == "webhook":
                # Webhook monitoring is handled externally
                _LOGGER.info("Camera monitoring set to webhook mode")

            return True

        except Exception as err:
            _LOGGER.error("Failed to start camera monitoring: %s", err)
            return False

    async def stop_monitoring(self) -> None:
        """Stop camera monitoring."""
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None

    @callback
    def _handle_camera_state_change(self, event: Event) -> None:
        """Handle camera state change event."""
        if not self._callback:
            return

        entity_id = event.data.get("entity_id")
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")

        if not new_state or entity_id != self.camera_entity:
            return

        # Trigger callback with camera event data
        event_data = {
            "camera_entity": entity_id,
            "new_state": new_state.state,
            "old_state": old_state.state if old_state else None,
            "attributes": new_state.attributes,
            "timestamp": dt_util.utcnow().isoformat()
        }

        # Schedule callback execution
        self.hass.async_create_task(self._callback(event_data))


class IntelligentNotificationService:
    """Service for sending intelligent notifications."""

    def __init__(
        self,
        hass: HomeAssistant,
        notification_devices: List[str],
        template_name: str = "rich_media"
    ) -> None:
        """Initialize notification service."""
        self.hass = hass
        self.notification_devices = notification_devices
        self.template_name = template_name
        self.template_engine = template.Template("", hass)

    async def send_notifications(
        self,
        ai_result: Dict[str, Any],
        snapshot_url: str,
        event_id: str
    ) -> Dict[str, Any]:
        """Send notifications to all configured devices."""
        if not self.notification_devices:
            return {"success": False, "error": "No notification devices configured"}

        template_config = NOTIFICATION_TEMPLATES.get(
            self.template_name,
            NOTIFICATION_TEMPLATES["rich_media"]
        )

        # Prepare template variables
        template_vars = {
            "ai_title": ai_result.get("title", "Doorbell"),
            "ai_description": ai_result.get("description", "Visitor detected"),
            "snapshot_url": snapshot_url,
            "event_id": event_id,
            "timestamp": dt_util.utcnow()
        }

        results = []
        
        for device in self.notification_devices:
            try:
                # Render notification content
                title = self._render_template(template_config["title"], template_vars)
                message = self._render_template(template_config["message"], template_vars)
                
                # Prepare notification data
                notification_data = template_config.get("data", {}).copy()
                
                # Render template values in data
                for key, value in notification_data.items():
                    if isinstance(value, str) and "{{" in value:
                        notification_data[key] = self._render_template(value, template_vars)
                    elif key == "actions" and isinstance(value, list):
                        # Handle action buttons
                        for action in value:
                            if "uri" in action and isinstance(action["uri"], str) and "{{" in action["uri"]:
                                action["uri"] = self._render_template(action["uri"], template_vars)

                # Send notification
                service_name = device.replace("notify.", "")
                await self.hass.services.async_call(
                    "notify",
                    service_name,
                    {
                        "title": title,
                        "message": message,
                        "data": notification_data
                    },
                    blocking=False
                )

                results.append({"device": device, "success": True})

            except Exception as err:
                _LOGGER.error("Failed to send notification to %s: %s", device, err)
                results.append({"device": device, "success": False, "error": str(err)})

        success_count = len([r for r in results if r["success"]])
        
        return {
            "success": success_count > 0,
            "total_devices": len(self.notification_devices),
            "successful_devices": success_count,
            "results": results
        }

    def _render_template(self, template_str: str, variables: Dict[str, Any]) -> str:
        """Render a template string with variables."""
        try:
            template_obj = template.Template(template_str, self.hass)
            return template_obj.async_render(variables)
        except Exception as err:
            _LOGGER.error("Failed to render template '%s': %s", template_str, err)
            return template_str


class MediaIntegrationService:
    """Service for media integration (sounds, TTS, displays)."""

    def __init__(
        self,
        hass: HomeAssistant,
        media_players: List[str],
        display_players: List[str],
        doorbell_sound_file: Optional[str],
        tts_service: Optional[str],
        display_duration: int = 15
    ) -> None:
        """Initialize media integration service."""
        self.hass = hass
        self.media_players = media_players
        self.display_players = display_players
        self.doorbell_sound_file = doorbell_sound_file
        self.tts_service = tts_service
        self.display_duration = display_duration

    async def play_doorbell_sequence(
        self,
        ai_message: str,
        snapshot_url: str,
        event_id: str
    ) -> Dict[str, Any]:
        """Play complete doorbell sequence."""
        tasks = []
        results = {"actions": []}

        # Play doorbell sound
        if self.doorbell_sound_file and self.media_players:
            tasks.append(self._play_doorbell_sound())
            results["actions"].append("doorbell_sound")

        # TTS announcement
        if ai_message and self.tts_service and self.media_players:
            tasks.append(self._play_tts_announcement(ai_message))
            results["actions"].append("tts_announcement")

        # Display snapshot
        if snapshot_url and self.display_players:
            tasks.append(self._display_snapshot(snapshot_url))
            results["actions"].append("snapshot_display")

        # Execute all tasks concurrently
        if tasks:
            task_results = await asyncio.gather(*tasks, return_exceptions=True)
            results["success"] = all(not isinstance(r, Exception) for r in task_results)
            results["errors"] = [str(r) for r in task_results if isinstance(r, Exception)]
        else:
            results["success"] = True
            results["message"] = "No media actions configured"

        return results

    async def _play_doorbell_sound(self) -> None:
        """Play doorbell sound on configured media players."""
        for player in self.media_players:
            try:
                await self.hass.services.async_call(
                    "media_player",
                    "play_media",
                    {
                        "entity_id": player,
                        "media_content_type": "music",
                        "media_content_id": self.doorbell_sound_file
                    },
                    blocking=False
                )
            except Exception as err:
                _LOGGER.error("Failed to play doorbell sound on %s: %s", player, err)

    async def _play_tts_announcement(self, message: str) -> None:
        """Play TTS announcement on configured media players."""
        if not self.tts_service:
            return

        for player in self.media_players:
            try:
                await self.hass.services.async_call(
                    "tts",
                    "speak",
                    {
                        "entity_id": self.tts_service,
                        "media_player_entity_id": player,
                        "message": message,
                        "cache": True
                    },
                    blocking=False
                )
            except Exception as err:
                _LOGGER.error("Failed to play TTS on %s: %s", player, err)

    async def _display_snapshot(self, snapshot_url: str) -> None:
        """Display snapshot on configured display players."""
        for player in self.display_players:
            try:
                # Display image
                await self.hass.services.async_call(
                    "media_player",
                    "play_media",
                    {
                        "entity_id": player,
                        "media_content_type": "image/jpeg",
                        "media_content_id": snapshot_url
                    },
                    blocking=False
                )

                # Schedule stop after duration
                if self.display_duration > 0:
                    async def stop_display():
                        await asyncio.sleep(self.display_duration)
                        try:
                            await self.hass.services.async_call(
                                "media_player",
                                "media_stop",
                                {"entity_id": player},
                                blocking=False
                            )
                        except Exception as err:
                            _LOGGER.error("Failed to stop display on %s: %s", player, err)

                    self.hass.async_create_task(stop_display())

            except Exception as err:
                _LOGGER.error("Failed to display snapshot on %s: %s", player, err)


class WeatherContextService:
    """Service for gathering weather context."""

    def __init__(self, hass: HomeAssistant, weather_entity: Optional[str] = None) -> None:
        """Initialize weather context service."""
        self.hass = hass
        self.weather_entity = weather_entity

    async def get_weather_context(self) -> Dict[str, Any]:
        """Get current weather context."""
        try:
            # Auto-discover weather entity if not configured
            if not self.weather_entity:
                weather_entities = [
                    entity_id for entity_id in self.hass.states.async_entity_ids("weather")
                ]
                if weather_entities:
                    self.weather_entity = weather_entities[0]

            if not self.weather_entity:
                return {}

            weather_state = self.hass.states.get(self.weather_entity)
            if not weather_state:
                return {}

            return {
                "temperature": weather_state.attributes.get("temperature", 20),
                "humidity": weather_state.attributes.get("humidity", 50),
                "condition": weather_state.state,
                "wind_speed": weather_state.attributes.get("wind_speed", 0),
                "pressure": weather_state.attributes.get("pressure", 1013),
                "entity_id": self.weather_entity
            }

        except Exception as err:
            _LOGGER.error("Failed to get weather context: %s", err)
            return {}
