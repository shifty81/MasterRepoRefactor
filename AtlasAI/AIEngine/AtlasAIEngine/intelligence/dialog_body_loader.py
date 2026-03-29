"""AtlasAI Phase 38D — Dialog Body Loader.

Discovers and manages dialog body manifests, mirroring the C++
DialogBodyRegistry for cross-language NPC conversation management.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class DialogLineManifest:
    """A single dialog line in a dialog body manifest."""
    line_id: str
    body_id: str
    speaker_id: str = ""
    text: str = ""
    voice_asset_id: str = ""
    duration: float = 0.0
    auto_advance: bool = True
    response_ids: list = field(default_factory=list)

    @property
    def has_voice(self) -> bool:
        return bool(self.voice_asset_id)

    @property
    def has_responses(self) -> bool:
        return bool(self.response_ids)

    @property
    def is_timed(self) -> bool:
        return self.duration > 0.0


@dataclass
class DialogResponseManifest:
    """A response option for a dialog line."""
    response_id: str
    line_id: str
    response_text: str = ""
    next_line_id: str = ""
    condition_expr: str = ""
    is_default: bool = False

    @property
    def has_condition(self) -> bool:
        return bool(self.condition_expr)

    @property
    def has_next(self) -> bool:
        return bool(self.next_line_id)


@dataclass
class DialogBodyManifest:
    """Parsed dialog body manifest for a single NPC conversation entity."""
    body_id: str
    name: str
    scope: str = "NPC"
    body_state: str = "Idle"
    flow_type: str = "Linear"
    trigger_type: str = "OnInteract"
    start_line_id: str = ""
    play_count: int = 0
    lines: list = field(default_factory=list)
    responses: list = field(default_factory=list)

    @property
    def is_active(self) -> bool:
        return self.body_state == "Active"

    @property
    def is_completed(self) -> bool:
        return self.body_state == "Completed"

    @property
    def is_branching(self) -> bool:
        return self.flow_type == "Branching"

    @property
    def has_lines(self) -> bool:
        return bool(self.lines)

    @property
    def has_responses(self) -> bool:
        return bool(self.responses)

    @property
    def has_start(self) -> bool:
        return bool(self.start_line_id)


class DialogBodyLoader:
    """Loader for dialog body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[DialogBodyManifest] = []

    def load_manifest(self, data: dict) -> DialogBodyManifest:
        """Parse a dict into a DialogBodyManifest."""
        lines_data = data.get("lines", [])
        lines = []
        for l in lines_data:
            lines.append(DialogLineManifest(
                line_id=l.get("line_id", ""),
                body_id=l.get("body_id", ""),
                speaker_id=l.get("speaker_id", ""),
                text=l.get("text", ""),
                voice_asset_id=l.get("voice_asset_id", ""),
                duration=float(l.get("duration", 0.0)),
                auto_advance=bool(l.get("auto_advance", True)),
                response_ids=l.get("response_ids", []),
            ))
        responses_data = data.get("responses", [])
        responses = []
        for r in responses_data:
            responses.append(DialogResponseManifest(
                response_id=r.get("response_id", ""),
                line_id=r.get("line_id", ""),
                response_text=r.get("response_text", ""),
                next_line_id=r.get("next_line_id", ""),
                condition_expr=r.get("condition_expr", ""),
                is_default=bool(r.get("is_default", False)),
            ))
        manifest = DialogBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            scope=data.get("scope", "NPC"),
            body_state=data.get("body_state", "Idle"),
            flow_type=data.get("flow_type", "Linear"),
            trigger_type=data.get("trigger_type", "OnInteract"),
            start_line_id=data.get("start_line_id", ""),
            play_count=int(data.get("play_count", 0)),
            lines=lines,
            responses=responses,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> DialogBodyManifest:
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[DialogBodyManifest]:
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: DialogBodyManifest, path) -> None:
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "scope": manifest.scope,
            "body_state": manifest.body_state,
            "flow_type": manifest.flow_type,
            "trigger_type": manifest.trigger_type,
            "start_line_id": manifest.start_line_id,
            "play_count": manifest.play_count,
            "lines": [
                {
                    "line_id": l.line_id,
                    "body_id": l.body_id,
                    "speaker_id": l.speaker_id,
                    "text": l.text,
                    "voice_asset_id": l.voice_asset_id,
                    "duration": l.duration,
                    "auto_advance": l.auto_advance,
                    "response_ids": l.response_ids,
                }
                for l in manifest.lines
            ],
            "responses": [
                {
                    "response_id": r.response_id,
                    "line_id": r.line_id,
                    "response_text": r.response_text,
                    "next_line_id": r.next_line_id,
                    "condition_expr": r.condition_expr,
                    "is_default": r.is_default,
                }
                for r in manifest.responses
            ],
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: DialogBodyManifest) -> bool:
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
