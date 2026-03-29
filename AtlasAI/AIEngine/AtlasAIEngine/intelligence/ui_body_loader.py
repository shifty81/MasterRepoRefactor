"""AtlasAI Phase 33D — UI Body Loader.

Discovers and manages UI body manifests, mirroring the C++
UIBodyRegistry for cross-language widget and interface setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class UIStyleManifest:
    """Style configuration for a UI body manifest."""

    style_id: str
    font_family: str = "Arial"
    font_size: int = 14
    fg_r: float = 1.0
    fg_g: float = 1.0
    fg_b: float = 1.0
    fg_a: float = 1.0
    bg_r: float = 0.0
    bg_g: float = 0.0
    bg_b: float = 0.0
    bg_a: float = 0.8
    border_width: float = 1.0
    border_radius: float = 4.0
    padding: float = 8.0

    @property
    def has_border(self) -> bool:
        return self.border_width > 0

    @property
    def is_transparent(self) -> bool:
        return self.bg_a < 1.0


@dataclass
class UILayoutManifest:
    """Layout configuration for a UI body manifest."""

    layout_id: str
    anchor: str = "Center"
    pos_x: float = 0.0
    pos_y: float = 0.0
    width: float = 100.0
    height: float = 50.0
    z_order: int = 0
    scale_mode: str = "Constant"

    @property
    def is_centered(self) -> bool:
        return self.anchor == "Center"

    @property
    def has_z_order(self) -> bool:
        return self.z_order != 0


@dataclass
class UIBodyManifest:
    """Parsed UI body manifest for a single widget in a scene."""

    body_id: str
    name: str
    ui_type: str = "Widget"         # Widget/Panel/Button/Label/Image/Slider/InputField/Dropdown/List/Canvas
    tooltip: str = ""
    visible: bool = True
    enabled: bool = True
    interactive: bool = True
    body_state: str = "Hidden"
    update_mode: str = "Always"
    style: UIStyleManifest = field(default_factory=lambda: UIStyleManifest(style_id="default"))
    layout: UILayoutManifest = field(default_factory=lambda: UILayoutManifest(layout_id="default"))

    @property
    def is_visible(self) -> bool:
        return self.visible

    @property
    def is_interactive(self) -> bool:
        return self.interactive and self.enabled

    @property
    def is_active(self) -> bool:
        return self.body_state == "Active"


class UIBodyLoader:
    """Loader for UI body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[UIBodyManifest] = []

    def load_manifest(self, data: dict) -> UIBodyManifest:
        """Parse a dict into a UIBodyManifest."""
        style_data = data.get("style", {})
        style = UIStyleManifest(
            style_id=style_data.get("style_id", "default"),
            font_family=style_data.get("font_family", "Arial"),
            font_size=int(style_data.get("font_size", 14)),
            fg_r=float(style_data.get("fg_r", 1.0)),
            fg_g=float(style_data.get("fg_g", 1.0)),
            fg_b=float(style_data.get("fg_b", 1.0)),
            fg_a=float(style_data.get("fg_a", 1.0)),
            bg_r=float(style_data.get("bg_r", 0.0)),
            bg_g=float(style_data.get("bg_g", 0.0)),
            bg_b=float(style_data.get("bg_b", 0.0)),
            bg_a=float(style_data.get("bg_a", 0.8)),
            border_width=float(style_data.get("border_width", 1.0)),
            border_radius=float(style_data.get("border_radius", 4.0)),
            padding=float(style_data.get("padding", 8.0)),
        )
        layout_data = data.get("layout", {})
        layout = UILayoutManifest(
            layout_id=layout_data.get("layout_id", "default"),
            anchor=layout_data.get("anchor", "Center"),
            pos_x=float(layout_data.get("pos_x", 0.0)),
            pos_y=float(layout_data.get("pos_y", 0.0)),
            width=float(layout_data.get("width", 100.0)),
            height=float(layout_data.get("height", 50.0)),
            z_order=int(layout_data.get("z_order", 0)),
            scale_mode=layout_data.get("scale_mode", "Constant"),
        )
        manifest = UIBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            ui_type=data.get("ui_type", "Widget"),
            tooltip=data.get("tooltip", ""),
            visible=bool(data.get("visible", True)),
            enabled=bool(data.get("enabled", True)),
            interactive=bool(data.get("interactive", True)),
            body_state=data.get("body_state", "Hidden"),
            update_mode=data.get("update_mode", "Always"),
            style=style,
            layout=layout,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> UIBodyManifest:
        """Load a manifest from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[UIBodyManifest]:
        """Load multiple manifests from a list of dicts."""
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: UIBodyManifest, path) -> None:
        """Serialize and save a manifest to a JSON file."""
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "ui_type": manifest.ui_type,
            "tooltip": manifest.tooltip,
            "visible": manifest.visible,
            "enabled": manifest.enabled,
            "interactive": manifest.interactive,
            "body_state": manifest.body_state,
            "update_mode": manifest.update_mode,
            "style": {
                "style_id": manifest.style.style_id,
                "font_family": manifest.style.font_family,
                "font_size": manifest.style.font_size,
                "fg_r": manifest.style.fg_r,
                "fg_g": manifest.style.fg_g,
                "fg_b": manifest.style.fg_b,
                "fg_a": manifest.style.fg_a,
                "bg_r": manifest.style.bg_r,
                "bg_g": manifest.style.bg_g,
                "bg_b": manifest.style.bg_b,
                "bg_a": manifest.style.bg_a,
                "border_width": manifest.style.border_width,
                "border_radius": manifest.style.border_radius,
                "padding": manifest.style.padding,
            },
            "layout": {
                "layout_id": manifest.layout.layout_id,
                "anchor": manifest.layout.anchor,
                "pos_x": manifest.layout.pos_x,
                "pos_y": manifest.layout.pos_y,
                "width": manifest.layout.width,
                "height": manifest.layout.height,
                "z_order": manifest.layout.z_order,
                "scale_mode": manifest.layout.scale_mode,
            },
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: UIBodyManifest) -> bool:
        """Validate a manifest has required fields."""
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
