"""AtlasAI Phase 28B — VFX Graph Compiler.

Manages visual effects graph assets composed of emitter nodes and link edges,
compiling them into serialisable asset payloads for use in the game VFX runtime.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class VFXEmitterNode:
    """A single emitter node in a VFX graph."""

    node_id: str
    name: str
    emitter_type: str = "Point"   # Point, Sphere, Box, Cone, Mesh, Trail
    spawn_rate: float = 10.0
    lifetime: float = 2.0
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)
    enabled: bool = True

    @property
    def is_emitter(self) -> bool:
        return self.emitter_type in ("Point", "Sphere", "Box", "Cone", "Mesh", "Trail")

    @property
    def is_active(self) -> bool:
        return self.enabled


@dataclass
class VFXLinkEdge:
    """A directed data edge between two VFX graph nodes."""

    edge_id: str
    source_id: str
    target_id: str
    data_type: str = "Float"   # Float, Vector2, Vector3, Color, Texture, Boolean
    enabled: bool = True

    @property
    def is_connected(self) -> bool:
        return bool(self.source_id) and bool(self.target_id)


@dataclass
class VFXGraphAsset:
    """A compiled VFX graph asset with nodes and edges."""

    asset_id: str
    name: str
    nodes: list[VFXEmitterNode] = field(default_factory=list)
    edges: list[VFXLinkEdge] = field(default_factory=list)
    compiled: bool = False
    compile_time_ms: float = 0.0
    asset_path: str = ""
    description: str = ""

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def is_valid(self) -> bool:
        node_ids = {n.node_id for n in self.nodes}
        for edge in self.edges:
            if edge.source_id not in node_ids or edge.target_id not in node_ids:
                return False
        return True

    @property
    def is_compiled(self) -> bool:
        return self.compiled


class VFXGraphCompiler:
    """Manages and compiles VFX graph assets from emitter nodes and link edges."""

    def __init__(self) -> None:
        self._assets: dict[str, VFXGraphAsset] = {}
        self._next_asset: int = 0
        self._next_node: int = 0
        self._next_edge: int = 0

    # ------------------------------------------------------------------
    # Asset management
    # ------------------------------------------------------------------

    def create_asset(self, name: str, description: str = "") -> VFXGraphAsset:
        asset_id = f"asset_{self._next_asset:04d}"
        self._next_asset += 1
        asset = VFXGraphAsset(asset_id=asset_id, name=name, description=description)
        self._assets[asset_id] = asset
        logger.debug("Created VFX graph asset %s: %s", asset_id, name)
        return asset

    def remove_asset(self, asset_id: str) -> bool:
        if asset_id not in self._assets:
            return False
        del self._assets[asset_id]
        return True

    def get_asset(self, asset_id: str) -> Optional[VFXGraphAsset]:
        return self._assets.get(asset_id)

    def list_assets(self) -> list[str]:
        return list(self._assets.keys())

    # ------------------------------------------------------------------
    # Node management
    # ------------------------------------------------------------------

    def add_node(
        self,
        asset_id: str,
        name: str,
        emitter_type: str = "Point",
        spawn_rate: float = 10.0,
        lifetime: float = 2.0,
        position: tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> Optional[VFXEmitterNode]:
        asset = self._assets.get(asset_id)
        if asset is None:
            return None
        node_id = f"node_{self._next_node:04d}"
        self._next_node += 1
        node = VFXEmitterNode(
            node_id=node_id,
            name=name,
            emitter_type=emitter_type,
            spawn_rate=spawn_rate,
            lifetime=lifetime,
            position=position,
        )
        asset.nodes.append(node)
        asset.compiled = False
        return node

    def remove_node(self, asset_id: str, node_id: str) -> bool:
        asset = self._assets.get(asset_id)
        if asset is None:
            return False
        before = len(asset.nodes)
        asset.nodes = [n for n in asset.nodes if n.node_id != node_id]
        # Remove edges referencing this node
        asset.edges = [
            e for e in asset.edges
            if e.source_id != node_id and e.target_id != node_id
        ]
        asset.compiled = False
        return len(asset.nodes) < before

    # ------------------------------------------------------------------
    # Edge management
    # ------------------------------------------------------------------

    def add_edge(
        self,
        asset_id: str,
        source_id: str,
        target_id: str,
        data_type: str = "Float",
    ) -> Optional[VFXLinkEdge]:
        asset = self._assets.get(asset_id)
        if asset is None:
            return None
        edge_id = f"edge_{self._next_edge:04d}"
        self._next_edge += 1
        edge = VFXLinkEdge(
            edge_id=edge_id,
            source_id=source_id,
            target_id=target_id,
            data_type=data_type,
        )
        asset.edges.append(edge)
        asset.compiled = False
        return edge

    def remove_edge(self, asset_id: str, edge_id: str) -> bool:
        asset = self._assets.get(asset_id)
        if asset is None:
            return False
        before = len(asset.edges)
        asset.edges = [e for e in asset.edges if e.edge_id != edge_id]
        asset.compiled = False
        return len(asset.edges) < before

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_graph(self, asset_id: str) -> list[str]:
        """Return a list of validation error messages (empty = valid)."""
        asset = self._assets.get(asset_id)
        if asset is None:
            return [f"Asset {asset_id} not found"]
        errors: list[str] = []
        node_ids = {n.node_id for n in asset.nodes}
        for edge in asset.edges:
            if edge.source_id not in node_ids:
                errors.append(f"Edge {edge.edge_id}: source {edge.source_id!r} not found")
            if edge.target_id not in node_ids:
                errors.append(f"Edge {edge.edge_id}: target {edge.target_id!r} not found")
        return errors

    # ------------------------------------------------------------------
    # Compilation
    # ------------------------------------------------------------------

    def compile(self, asset_id: str) -> bool:
        """Simulate compilation of the VFX graph asset."""
        start = time.time()
        asset = self._assets.get(asset_id)
        if asset is None:
            return False
        errors = self.validate_graph(asset_id)
        if errors:
            logger.warning("VFX graph %s has %d validation errors", asset_id, len(errors))
            return False
        asset.compiled = True
        asset.compile_time_ms = (time.time() - start) * 1000
        logger.debug("Compiled VFX graph asset %s in %.2f ms", asset_id, asset.compile_time_ms)
        return True

    def compile_all(self) -> int:
        compiled = 0
        for asset_id in list(self._assets):
            if self.compile(asset_id):
                compiled += 1
        return compiled

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def get_compiled_count(self) -> int:
        return sum(1 for a in self._assets.values() if a.compiled)

    def get_total_node_count(self) -> int:
        return sum(len(a.nodes) for a in self._assets.values())

    def get_total_edge_count(self) -> int:
        return sum(len(a.edges) for a in self._assets.values())

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_manifest(self, output_path: str) -> bool:
        data = {
            "asset_count": len(self._assets),
            "assets": [
                {
                    "asset_id": a.asset_id,
                    "name": a.name,
                    "compiled": a.compiled,
                    "node_count": a.node_count,
                    "edge_count": a.edge_count,
                }
                for a in self._assets.values()
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save VFX manifest: %s", exc)
            return False

    def clear(self) -> None:
        self._assets.clear()
        self._next_asset = 0
        self._next_node = 0
        self._next_edge = 0
