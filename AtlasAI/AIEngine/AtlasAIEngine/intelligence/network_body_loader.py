"""AtlasAI Phase 34D — Network Body Loader.

Discovers and manages network body manifests, mirroring the C++
NetworkBodyRegistry for cross-language replication and session setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ReplicationConfigManifest:
    """Replication configuration for a network body manifest."""

    config_id: str = "default"
    mode: str = "RepGraph"          # None_/RepGraph/Actor/Component/Subobject/Custom
    channel: str = "Reliable"       # Reliable/Unreliable/Voice/DataStream/FileTransfer/Custom
    sync_frequency: str = "Medium"  # Never/Low/Medium/High/VeryHigh/Custom
    relevancy_radius: float = 10000.0
    dormancy: bool = True
    priority_multiplier: float = 1.0

    @property
    def is_reliable(self) -> bool:
        return self.channel == "Reliable"

    @property
    def has_relevancy(self) -> bool:
        return self.relevancy_radius < 100000.0


@dataclass
class NetworkPropertyManifest:
    """Property definition for network replication."""

    prop_id: str
    prop_name: str
    prop_type: str = "Float"
    replication_mode: str = "Actor"
    sync_frequency: str = "Medium"
    condition: str = "Always"
    is_owner_only: bool = False

    @property
    def is_always_replicated(self) -> bool:
        return self.condition == "Always"


@dataclass
class NetworkBodyManifest:
    """Parsed network body manifest for a single replicated entity."""

    body_id: str
    name: str
    role: str = "SimulatedProxy"    # None_/Authority/AutonomousProxy/SimulatedProxy/Replay/Custom
    net_id: str = ""
    owner_actor_id: str = ""
    body_state: str = "Offline"     # Offline/Connecting/Connected/Synchronizing/Ready/Error/Disconnecting
    latency_ms: float = 0.0
    replication_config: ReplicationConfigManifest = field(
        default_factory=ReplicationConfigManifest
    )
    properties: list = field(default_factory=list)

    @property
    def is_connected(self) -> bool:
        return self.body_state in ("Connected", "Ready", "Synchronizing")

    @property
    def is_authority(self) -> bool:
        return self.role == "Authority"

    @property
    def has_properties(self) -> bool:
        return bool(self.properties)


class NetworkBodyLoader:
    """Loader for network body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[NetworkBodyManifest] = []

    def load_manifest(self, data: dict) -> NetworkBodyManifest:
        """Parse a dict into a NetworkBodyManifest."""
        config_data = data.get("replication_config", {})
        config = ReplicationConfigManifest(
            config_id=config_data.get("config_id", "default"),
            mode=config_data.get("mode", "RepGraph"),
            channel=config_data.get("channel", "Reliable"),
            sync_frequency=config_data.get("sync_frequency", "Medium"),
            relevancy_radius=float(config_data.get("relevancy_radius", 10000.0)),
            dormancy=bool(config_data.get("dormancy", True)),
            priority_multiplier=float(config_data.get("priority_multiplier", 1.0)),
        )
        props_data = data.get("properties", [])
        properties = []
        for p in props_data:
            properties.append(NetworkPropertyManifest(
                prop_id=p.get("prop_id", ""),
                prop_name=p.get("prop_name", ""),
                prop_type=p.get("prop_type", "Float"),
                replication_mode=p.get("replication_mode", "Actor"),
                sync_frequency=p.get("sync_frequency", "Medium"),
                condition=p.get("condition", "Always"),
                is_owner_only=bool(p.get("is_owner_only", False)),
            ))
        manifest = NetworkBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            role=data.get("role", "SimulatedProxy"),
            net_id=data.get("net_id", ""),
            owner_actor_id=data.get("owner_actor_id", ""),
            body_state=data.get("body_state", "Offline"),
            latency_ms=float(data.get("latency_ms", 0.0)),
            replication_config=config,
            properties=properties,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> NetworkBodyManifest:
        """Load a manifest from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[NetworkBodyManifest]:
        """Load multiple manifests from a list of dicts."""
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: NetworkBodyManifest, path) -> None:
        """Serialize and save a manifest to a JSON file."""
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "role": manifest.role,
            "net_id": manifest.net_id,
            "owner_actor_id": manifest.owner_actor_id,
            "body_state": manifest.body_state,
            "latency_ms": manifest.latency_ms,
            "replication_config": {
                "config_id": manifest.replication_config.config_id,
                "mode": manifest.replication_config.mode,
                "channel": manifest.replication_config.channel,
                "sync_frequency": manifest.replication_config.sync_frequency,
                "relevancy_radius": manifest.replication_config.relevancy_radius,
                "dormancy": manifest.replication_config.dormancy,
                "priority_multiplier": manifest.replication_config.priority_multiplier,
            },
            "properties": [
                {
                    "prop_id": prop.prop_id,
                    "prop_name": prop.prop_name,
                    "prop_type": prop.prop_type,
                    "replication_mode": prop.replication_mode,
                    "sync_frequency": prop.sync_frequency,
                    "condition": prop.condition,
                    "is_owner_only": prop.is_owner_only,
                }
                for prop in manifest.properties
            ],
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: NetworkBodyManifest) -> bool:
        """Validate a manifest has required fields."""
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
