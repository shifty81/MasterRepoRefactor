"""AtlasAI Phase 35D — Game Body Loader.

Discovers and manages game body manifests, mirroring the C++
GameBodyRegistry for cross-language gameplay and session setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class SpawnConfigManifest:
    """Spawn configuration for a game body manifest."""

    config_id: str = "default"
    policy: str = "Immediate"       # Immediate/Deferred/Pooled/Streamed/Custom
    spawn_radius: float = 500.0
    max_instances: int = 100
    respawn_delay: float = 5.0
    pool_size: int = 10
    persistent: bool = False

    @property
    def is_pooled(self) -> bool:
        return self.policy == "Pooled"

    @property
    def is_persistent(self) -> bool:
        return self.persistent


@dataclass
class GameEventManifest:
    """Event record for a game body manifest."""

    event_id: str
    body_id: str
    event_type: str = "Spawn"       # Spawn/Despawn/Interact/Damage/Death/Respawn/StateChange/Custom
    timestamp: float = 0.0
    actor_id: str = ""
    payload: str = ""

    @property
    def is_spawn(self) -> bool:
        return self.event_type == "Spawn"

    @property
    def is_death(self) -> bool:
        return self.event_type == "Death"


@dataclass
class GameBodyManifest:
    """Parsed game body manifest for a single gameplay entity."""

    body_id: str
    name: str
    role: str = "NPC"               # None_/Player/NPC/Vehicle/Projectile/Interactable/Environment/Custom
    flags: list = field(default_factory=list)
    team_id: str = ""
    owner_id: str = ""
    body_state: str = "Inactive"    # Inactive/Initializing/Active/Paused/Terminating/Terminated/Error
    health: float = 100.0
    max_health: float = 100.0
    spawn_config: SpawnConfigManifest = field(default_factory=SpawnConfigManifest)
    events: list = field(default_factory=list)

    @property
    def is_alive(self) -> bool:
        return self.body_state == "Active" and self.health > 0

    @property
    def is_player(self) -> bool:
        return self.role == "Player"

    @property
    def has_events(self) -> bool:
        return bool(self.events)


class GameBodyLoader:
    """Loader for game body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[GameBodyManifest] = []

    def load_manifest(self, data: dict) -> GameBodyManifest:
        """Parse a dict into a GameBodyManifest."""
        config_data = data.get("spawn_config", {})
        config = SpawnConfigManifest(
            config_id=config_data.get("config_id", "default"),
            policy=config_data.get("policy", "Immediate"),
            spawn_radius=float(config_data.get("spawn_radius", 500.0)),
            max_instances=int(config_data.get("max_instances", 100)),
            respawn_delay=float(config_data.get("respawn_delay", 5.0)),
            pool_size=int(config_data.get("pool_size", 10)),
            persistent=bool(config_data.get("persistent", False)),
        )
        events_data = data.get("events", [])
        events = []
        for e in events_data:
            events.append(GameEventManifest(
                event_id=e.get("event_id", ""),
                body_id=e.get("body_id", ""),
                event_type=e.get("event_type", "Spawn"),
                timestamp=float(e.get("timestamp", 0.0)),
                actor_id=e.get("actor_id", ""),
                payload=e.get("payload", ""),
            ))
        manifest = GameBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            role=data.get("role", "NPC"),
            flags=data.get("flags", []),
            team_id=data.get("team_id", ""),
            owner_id=data.get("owner_id", ""),
            body_state=data.get("body_state", "Inactive"),
            health=float(data.get("health", 100.0)),
            max_health=float(data.get("max_health", 100.0)),
            spawn_config=config,
            events=events,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> GameBodyManifest:
        """Load a manifest from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[GameBodyManifest]:
        """Load multiple manifests from a list of dicts."""
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: GameBodyManifest, path) -> None:
        """Serialize and save a manifest to a JSON file."""
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "role": manifest.role,
            "flags": manifest.flags,
            "team_id": manifest.team_id,
            "owner_id": manifest.owner_id,
            "body_state": manifest.body_state,
            "health": manifest.health,
            "max_health": manifest.max_health,
            "spawn_config": {
                "config_id": manifest.spawn_config.config_id,
                "policy": manifest.spawn_config.policy,
                "spawn_radius": manifest.spawn_config.spawn_radius,
                "max_instances": manifest.spawn_config.max_instances,
                "respawn_delay": manifest.spawn_config.respawn_delay,
                "pool_size": manifest.spawn_config.pool_size,
                "persistent": manifest.spawn_config.persistent,
            },
            "events": [
                {
                    "event_id": ev.event_id,
                    "body_id": ev.body_id,
                    "event_type": ev.event_type,
                    "timestamp": ev.timestamp,
                    "actor_id": ev.actor_id,
                    "payload": ev.payload,
                }
                for ev in manifest.events
            ],
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: GameBodyManifest) -> bool:
        """Validate a manifest has required fields."""
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
