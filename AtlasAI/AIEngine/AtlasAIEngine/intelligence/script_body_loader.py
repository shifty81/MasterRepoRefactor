"""AtlasAI Phase 37D — Script Body Loader.

Discovers and manages script body manifests, mirroring the C++
ScriptBodyRegistry for cross-language script execution setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ScriptConfigManifest:
    """Script configuration for a script body manifest."""

    config_id: str = "default"
    script_path: str = ""
    language: str = "Lua"               # Lua/Python/Blueprint/JavaScript/AngelScript/Custom
    execution_mode: str = "Immediate"   # Immediate/Deferred/Scheduled/EventDriven/Custom
    timeout_ms: float = 5000.0
    max_retries: int = 0
    sandboxed: bool = True

    @property
    def is_scheduled(self) -> bool:
        return self.execution_mode == "Scheduled"

    @property
    def has_script(self) -> bool:
        return bool(self.script_path)

    @property
    def is_safe(self) -> bool:
        return self.sandboxed


@dataclass
class ScriptBindingManifest:
    """Binding record for a script body manifest."""

    binding_id: str
    body_id: str
    target_id: str = ""
    event: str = ""
    handler_name: str = ""
    active: bool = True

    @property
    def has_target(self) -> bool:
        return bool(self.target_id)

    @property
    def has_handler(self) -> bool:
        return bool(self.handler_name)

    @property
    def is_active(self) -> bool:
        return self.active


@dataclass
class ScriptBodyManifest:
    """Parsed script body manifest for a single scripted entity."""

    body_id: str
    name: str
    scope: str = "Global"               # Global/Local/Team/Scene/Actor/Component/Custom
    body_state: str = "Idle"            # Idle/Running/Paused/Completed/Failed/Disabled/Custom
    language: str = "Lua"
    trigger_count: int = 0
    last_error: str = ""
    script_config: ScriptConfigManifest = field(default_factory=ScriptConfigManifest)
    bindings: list = field(default_factory=list)

    @property
    def is_running(self) -> bool:
        return self.body_state == "Running"

    @property
    def is_failed(self) -> bool:
        return self.body_state == "Failed"

    @property
    def has_bindings(self) -> bool:
        return bool(self.bindings)

    @property
    def has_error(self) -> bool:
        return bool(self.last_error)


class ScriptBodyLoader:
    """Loader for script body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[ScriptBodyManifest] = []

    def load_manifest(self, data: dict) -> ScriptBodyManifest:
        """Parse a dict into a ScriptBodyManifest."""
        config_data = data.get("script_config", {})
        script_config = ScriptConfigManifest(
            config_id=config_data.get("config_id", "default"),
            script_path=config_data.get("script_path", ""),
            language=config_data.get("language", "Lua"),
            execution_mode=config_data.get("execution_mode", "Immediate"),
            timeout_ms=float(config_data.get("timeout_ms", 5000.0)),
            max_retries=int(config_data.get("max_retries", 0)),
            sandboxed=bool(config_data.get("sandboxed", True)),
        )
        bindings_data = data.get("bindings", [])
        bindings = []
        for b in bindings_data:
            bindings.append(ScriptBindingManifest(
                binding_id=b.get("binding_id", ""),
                body_id=b.get("body_id", ""),
                target_id=b.get("target_id", ""),
                event=b.get("event", ""),
                handler_name=b.get("handler_name", ""),
                active=bool(b.get("active", True)),
            ))
        manifest = ScriptBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            scope=data.get("scope", "Global"),
            body_state=data.get("body_state", "Idle"),
            language=data.get("language", "Lua"),
            trigger_count=int(data.get("trigger_count", 0)),
            last_error=data.get("last_error", ""),
            script_config=script_config,
            bindings=bindings,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> ScriptBodyManifest:
        """Load a manifest from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[ScriptBodyManifest]:
        """Load multiple manifests from a list of dicts."""
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: ScriptBodyManifest, path) -> None:
        """Serialize and save a manifest to a JSON file."""
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "scope": manifest.scope,
            "body_state": manifest.body_state,
            "language": manifest.language,
            "trigger_count": manifest.trigger_count,
            "last_error": manifest.last_error,
            "script_config": {
                "config_id": manifest.script_config.config_id,
                "script_path": manifest.script_config.script_path,
                "language": manifest.script_config.language,
                "execution_mode": manifest.script_config.execution_mode,
                "timeout_ms": manifest.script_config.timeout_ms,
                "max_retries": manifest.script_config.max_retries,
                "sandboxed": manifest.script_config.sandboxed,
            },
            "bindings": [
                {
                    "binding_id": b.binding_id,
                    "body_id": b.body_id,
                    "target_id": b.target_id,
                    "event": b.event,
                    "handler_name": b.handler_name,
                    "active": b.active,
                }
                for b in manifest.bindings
            ],
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: ScriptBodyManifest) -> bool:
        """Validate a manifest has required fields."""
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
