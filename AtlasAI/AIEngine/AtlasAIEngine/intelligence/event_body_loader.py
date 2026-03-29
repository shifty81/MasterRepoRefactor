"""AtlasAI Phase 36D — Event Body Loader.

Discovers and manages event body manifests, mirroring the C++
EventBodyRegistry for cross-language event-driven gameplay setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class TriggerConfigManifest:
    """Trigger configuration for an event body manifest."""

    config_id: str = "default"
    trigger_type: str = "OnSignal"      # OnEnter/OnExit/OnOverlap/OnTimer/OnSignal/OnCondition/OnInput/Custom
    priority: str = "Normal"            # Critical/High/Normal/Low/Deferred/Custom
    debounce_ms: float = 0.0
    max_triggers: int = 0
    cooldown_ms: float = 0.0
    persistent: bool = False

    @property
    def is_repeatable(self) -> bool:
        return self.max_triggers != 1

    @property
    def has_cooldown(self) -> bool:
        return self.cooldown_ms > 0


@dataclass
class EventPayloadManifest:
    """Payload record for an event body manifest."""

    payload_id: str
    body_id: str
    event_type: str = "OnSignal"
    data: str = ""
    sender: str = ""
    recipients: list = field(default_factory=list)
    timestamp: float = 0.0
    sequence_id: int = 0

    @property
    def has_recipients(self) -> bool:
        return bool(self.recipients)

    @property
    def is_broadcast(self) -> bool:
        return not self.recipients


@dataclass
class EventBodyManifest:
    """Parsed event body manifest for a single event-driven gameplay entity."""

    body_id: str
    name: str
    scope: str = "Global"               # Global/Local/Team/Channel/Instance/World/Custom
    flags: list = field(default_factory=list)
    channel_id: str = ""
    owner_id: str = ""
    body_state: str = "Idle"            # Idle/Listening/Triggered/Processing/Completed/Failed/Disabled/Custom
    trigger_count: int = 0
    trigger_config: TriggerConfigManifest = field(default_factory=TriggerConfigManifest)
    payloads: list = field(default_factory=list)

    @property
    def is_listening(self) -> bool:
        return self.body_state == "Listening"

    @property
    def is_triggered(self) -> bool:
        return self.body_state == "Triggered"

    @property
    def has_payloads(self) -> bool:
        return bool(self.payloads)


class EventBodyLoader:
    """Loader for event body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[EventBodyManifest] = []

    def load_manifest(self, data: dict) -> EventBodyManifest:
        """Parse a dict into an EventBodyManifest."""
        trigger_data = data.get("trigger_config", {})
        trigger_config = TriggerConfigManifest(
            config_id=trigger_data.get("config_id", "default"),
            trigger_type=trigger_data.get("trigger_type", "OnSignal"),
            priority=trigger_data.get("priority", "Normal"),
            debounce_ms=float(trigger_data.get("debounce_ms", 0.0)),
            max_triggers=int(trigger_data.get("max_triggers", 0)),
            cooldown_ms=float(trigger_data.get("cooldown_ms", 0.0)),
            persistent=bool(trigger_data.get("persistent", False)),
        )
        payloads_data = data.get("payloads", [])
        payloads = []
        for p in payloads_data:
            payloads.append(EventPayloadManifest(
                payload_id=p.get("payload_id", ""),
                body_id=p.get("body_id", ""),
                event_type=p.get("event_type", "OnSignal"),
                data=p.get("data", ""),
                sender=p.get("sender", ""),
                recipients=p.get("recipients", []),
                timestamp=float(p.get("timestamp", 0.0)),
                sequence_id=int(p.get("sequence_id", 0)),
            ))
        manifest = EventBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            scope=data.get("scope", "Global"),
            flags=data.get("flags", []),
            channel_id=data.get("channel_id", ""),
            owner_id=data.get("owner_id", ""),
            body_state=data.get("body_state", "Idle"),
            trigger_count=int(data.get("trigger_count", 0)),
            trigger_config=trigger_config,
            payloads=payloads,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> EventBodyManifest:
        """Load a manifest from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[EventBodyManifest]:
        """Load multiple manifests from a list of dicts."""
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: EventBodyManifest, path) -> None:
        """Serialize and save a manifest to a JSON file."""
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "scope": manifest.scope,
            "flags": manifest.flags,
            "channel_id": manifest.channel_id,
            "owner_id": manifest.owner_id,
            "body_state": manifest.body_state,
            "trigger_count": manifest.trigger_count,
            "trigger_config": {
                "config_id": manifest.trigger_config.config_id,
                "trigger_type": manifest.trigger_config.trigger_type,
                "priority": manifest.trigger_config.priority,
                "debounce_ms": manifest.trigger_config.debounce_ms,
                "max_triggers": manifest.trigger_config.max_triggers,
                "cooldown_ms": manifest.trigger_config.cooldown_ms,
                "persistent": manifest.trigger_config.persistent,
            },
            "payloads": [
                {
                    "payload_id": pl.payload_id,
                    "body_id": pl.body_id,
                    "event_type": pl.event_type,
                    "data": pl.data,
                    "sender": pl.sender,
                    "recipients": pl.recipients,
                    "timestamp": pl.timestamp,
                    "sequence_id": pl.sequence_id,
                }
                for pl in manifest.payloads
            ],
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: EventBodyManifest) -> bool:
        """Validate a manifest has required fields."""
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
