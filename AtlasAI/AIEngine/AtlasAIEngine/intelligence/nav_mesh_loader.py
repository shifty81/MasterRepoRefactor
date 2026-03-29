"""AtlasAI Phase 25D — NavMesh Loader.

Discovers and manages navigation mesh manifests, mirroring the C++
NavMeshRegistry for cross-language AI pathfinding coordination at runtime.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class NavMeshAABB:
    """Axis-aligned bounding box for a navigation mesh."""

    min_x: float = 0.0
    min_y: float = 0.0
    min_z: float = 0.0
    max_x: float = 100.0
    max_y: float = 100.0
    max_z: float = 100.0

    def contains_point(self, px: float, py: float, pz: float) -> bool:
        return (self.min_x <= px <= self.max_x
                and self.min_y <= py <= self.max_y
                and self.min_z <= pz <= self.max_z)

    def intersects(self, other: "NavMeshAABB") -> bool:
        return (self.min_x <= other.max_x and self.max_x >= other.min_x
                and self.min_y <= other.max_y and self.max_y >= other.min_y
                and self.min_z <= other.max_z and self.max_z >= other.min_z)

    @property
    def volume(self) -> float:
        return (max(0.0, self.max_x - self.min_x)
                * max(0.0, self.max_y - self.min_y)
                * max(0.0, self.max_z - self.min_z))


@dataclass
class NavMeshNode:
    """A node (waypoint/polygon centre) within a navigation mesh."""

    node_id: str
    mesh_id: str
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    traversal_cost: float = 1.0
    flags: int = 0
    area_id: int = 0

    @property
    def position(self) -> tuple[float, float, float]:
        return (self.pos_x, self.pos_y, self.pos_z)


@dataclass
class NavMeshEdge:
    """A directed edge connecting two NavMesh nodes."""

    edge_id: str
    from_node_id: str
    to_node_id: str
    mesh_id: str
    cost: float = 1.0
    bidirectional: bool = True
    enabled: bool = True
    portal_width: float = 1.0


@dataclass
class NavMeshManifest:
    """Parsed navigation mesh manifest."""

    mesh_id: str
    name: str
    mesh_type: str = "Ground"
    bounds: NavMeshAABB = field(default_factory=NavMeshAABB)
    asset_path: str = ""
    manifest_path: str = ""
    neighbour_ids: list[str] = field(default_factory=list)
    agent_types: list[str] = field(default_factory=list)
    nodes: list[NavMeshNode] = field(default_factory=list)
    edges: list[NavMeshEdge] = field(default_factory=list)
    always_loaded: bool = False
    priority: int = 0
    parent_mesh_id: str = ""

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def neighbour_count(self) -> int:
        return len(self.neighbour_ids)

    def supports_agent(self, agent_type: str) -> bool:
        return agent_type in self.agent_types


class NavMeshLoader:
    """Discovers and manages navigation mesh manifests for the AI subsystem."""

    def __init__(self) -> None:
        self._manifests: dict[str, NavMeshManifest] = {}
        self._loaded: set[str] = set()
        self._next_node: int = 0
        self._next_edge: int = 0

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        mesh_id: str,
        name: str,
        mesh_type: str = "Ground",
        always_loaded: bool = False,
        priority: int = 0,
    ) -> NavMeshManifest:
        manifest = NavMeshManifest(
            mesh_id=mesh_id,
            name=name,
            mesh_type=mesh_type,
            always_loaded=always_loaded,
            priority=priority,
        )
        self._manifests[mesh_id] = manifest
        logger.debug("Registered nav mesh %s", mesh_id)
        return manifest

    def register_from_dict(self, data: dict) -> Optional[NavMeshManifest]:
        try:
            mesh_id = data["mesh_id"]
            name = data["name"]
            manifest = self.register(
                mesh_id=mesh_id,
                name=name,
                mesh_type=data.get("mesh_type", "Ground"),
                always_loaded=data.get("always_loaded", False),
                priority=data.get("priority", 0),
            )
            if "bounds" in data:
                b = data["bounds"]
                manifest.bounds = NavMeshAABB(
                    min_x=b.get("min_x", 0.0),
                    min_y=b.get("min_y", 0.0),
                    min_z=b.get("min_z", 0.0),
                    max_x=b.get("max_x", 100.0),
                    max_y=b.get("max_y", 100.0),
                    max_z=b.get("max_z", 100.0),
                )
            manifest.neighbour_ids = data.get("neighbour_ids", [])
            manifest.agent_types = data.get("agent_types", [])
            manifest.asset_path = data.get("asset_path", "")
            manifest.parent_mesh_id = data.get("parent_mesh_id", "")
            return manifest
        except (KeyError, TypeError) as exc:
            logger.error("register_from_dict failed: %s", exc)
            return None

    def unregister(self, mesh_id: str) -> bool:
        if mesh_id not in self._manifests:
            return False
        del self._manifests[mesh_id]
        self._loaded.discard(mesh_id)
        return True

    def get_manifest(self, mesh_id: str) -> Optional[NavMeshManifest]:
        return self._manifests.get(mesh_id)

    def get_registered_count(self) -> int:
        return len(self._manifests)

    def get_all_mesh_ids(self) -> list[str]:
        return list(self._manifests.keys())

    # ------------------------------------------------------------------
    # Load / unload
    # ------------------------------------------------------------------

    def load_mesh(self, mesh_id: str) -> bool:
        if mesh_id not in self._manifests:
            logger.warning("Cannot load unknown mesh %s", mesh_id)
            return False
        self._loaded.add(mesh_id)
        logger.debug("Loaded nav mesh %s", mesh_id)
        return True

    def unload_mesh(self, mesh_id: str) -> bool:
        if mesh_id not in self._loaded:
            return False
        self._loaded.discard(mesh_id)
        return True

    def is_loaded(self, mesh_id: str) -> bool:
        return mesh_id in self._loaded

    def get_loaded_count(self) -> int:
        return len(self._loaded)

    def get_loaded_ids(self) -> list[str]:
        return list(self._loaded)

    def load_always_loaded(self) -> int:
        loaded = 0
        for mesh_id, manifest in self._manifests.items():
            if manifest.always_loaded and mesh_id not in self._loaded:
                self._loaded.add(mesh_id)
                loaded += 1
        return loaded

    # ------------------------------------------------------------------
    # Node / edge management
    # ------------------------------------------------------------------

    def add_node(
        self,
        mesh_id: str,
        pos_x: float = 0.0,
        pos_y: float = 0.0,
        pos_z: float = 0.0,
        traversal_cost: float = 1.0,
        area_id: int = 0,
    ) -> Optional[NavMeshNode]:
        manifest = self._manifests.get(mesh_id)
        if manifest is None:
            return None
        node_id = f"node_{self._next_node:05d}"
        self._next_node += 1
        node = NavMeshNode(
            node_id=node_id,
            mesh_id=mesh_id,
            pos_x=pos_x,
            pos_y=pos_y,
            pos_z=pos_z,
            traversal_cost=traversal_cost,
            area_id=area_id,
        )
        manifest.nodes.append(node)
        return node

    def add_edge(
        self,
        mesh_id: str,
        from_node_id: str,
        to_node_id: str,
        cost: float = 1.0,
        bidirectional: bool = True,
    ) -> Optional[NavMeshEdge]:
        manifest = self._manifests.get(mesh_id)
        if manifest is None:
            return None
        edge_id = f"edge_{self._next_edge:05d}"
        self._next_edge += 1
        edge = NavMeshEdge(
            edge_id=edge_id,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            mesh_id=mesh_id,
            cost=max(0.0, cost),
            bidirectional=bidirectional,
        )
        manifest.edges.append(edge)
        return edge

    # ------------------------------------------------------------------
    # Neighbours and agents
    # ------------------------------------------------------------------

    def add_neighbour(self, mesh_id: str, neighbour_id: str) -> bool:
        manifest = self._manifests.get(mesh_id)
        if manifest is None:
            return False
        if neighbour_id not in manifest.neighbour_ids:
            manifest.neighbour_ids.append(neighbour_id)
        return True

    def add_agent_type(self, mesh_id: str, agent_type: str) -> bool:
        manifest = self._manifests.get(mesh_id)
        if manifest is None:
            return False
        if agent_type not in manifest.agent_types:
            manifest.agent_types.append(agent_type)
        return True

    def get_neighbours(self, mesh_id: str) -> list[str]:
        manifest = self._manifests.get(mesh_id)
        return list(manifest.neighbour_ids) if manifest else []

    # ------------------------------------------------------------------
    # Spatial queries
    # ------------------------------------------------------------------

    def query_point(self, px: float, py: float, pz: float) -> list[str]:
        return [
            mid
            for mid, m in self._manifests.items()
            if m.bounds.contains_point(px, py, pz)
        ]

    def query_path(
        self, start_mesh_id: str, end_mesh_id: str
    ) -> list[str]:
        if start_mesh_id == end_mesh_id:
            return [start_mesh_id]
        start = self._manifests.get(start_mesh_id)
        if start is None:
            return []
        if end_mesh_id in start.neighbour_ids:
            return [start_mesh_id, end_mesh_id]
        return [start_mesh_id, end_mesh_id]

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_registry(self, output_path: str) -> bool:
        data = []
        for m in self._manifests.values():
            data.append({
                "mesh_id": m.mesh_id,
                "name": m.name,
                "mesh_type": m.mesh_type,
                "always_loaded": m.always_loaded,
                "priority": m.priority,
                "neighbour_ids": m.neighbour_ids,
                "agent_types": m.agent_types,
                "asset_path": m.asset_path,
                "node_count": m.node_count,
                "edge_count": m.edge_count,
            })
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save nav mesh registry: %s", exc)
            return False

    def load_registry(self, input_path: str) -> int:
        try:
            data = json.loads(Path(input_path).read_text())
            loaded = 0
            for entry in data:
                if self.register_from_dict(entry) is not None:
                    loaded += 1
            return loaded
        except (OSError, json.JSONDecodeError) as exc:
            logger.error("Failed to load nav mesh registry: %s", exc)
            return 0

    def clear(self) -> None:
        self._manifests.clear()
        self._loaded.clear()
        self._next_node = 0
        self._next_edge = 0
