"""AtlasAI Phase 22B — Asset Dependency Graph.

Builds and queries a directed dependency graph of content assets so that
the AI pipeline can compute asset impact, suggest safe deletion candidates,
and order rebuild jobs correctly.
"""
from __future__ import annotations

import json
import logging
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class AssetNode:
    """A single asset node in the dependency graph."""

    asset_id: str
    asset_type: str
    path: str
    tags: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class AssetDependencyGraph:
    """Directed asset dependency graph supporting forward and reverse traversal.

    Edges represent *asset_id → depends_on → dep_id* relationships.  Both
    forward traversal (what does X depend on?) and reverse traversal (what
    depends on X?) are supported in O(V + E).

    Example::

        graph = AssetDependencyGraph()
        graph.add_node("mesh_01", "StaticMesh", "/content/mesh_01.fbx")
        graph.add_node("mat_01", "Material", "/content/mat_01.mat")
        graph.add_dependency("mesh_01", "mat_01")

        deps = graph.get_dependencies("mesh_01")   # ["mat_01"]
        refs = graph.get_dependents("mat_01")       # ["mesh_01"]
    """

    def __init__(self) -> None:
        self._nodes: dict[str, AssetNode] = {}
        self._forward: dict[str, list[str]] = {}   # asset → its deps
        self._reverse: dict[str, list[str]] = {}   # dep → assets that use it

    # ------------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------------

    def add_node(self, asset_id: str, asset_type: str,
                 path: str = "", tags: Optional[list[str]] = None,
                 metadata: Optional[dict] = None) -> AssetNode:
        node = AssetNode(
            asset_id=asset_id,
            asset_type=asset_type,
            path=path,
            tags=list(tags or []),
            metadata=dict(metadata or {}),
        )
        self._nodes[asset_id] = node
        self._forward.setdefault(asset_id, [])
        self._reverse.setdefault(asset_id, [])
        return node

    def remove_node(self, asset_id: str) -> bool:
        if asset_id not in self._nodes:
            return False
        # Remove edges referencing this node
        for dep in list(self._forward.get(asset_id, [])):
            self._reverse[dep] = [x for x in self._reverse.get(dep, [])
                                   if x != asset_id]
        for src in list(self._reverse.get(asset_id, [])):
            self._forward[src] = [x for x in self._forward.get(src, [])
                                   if x != asset_id]
        del self._nodes[asset_id]
        self._forward.pop(asset_id, None)
        self._reverse.pop(asset_id, None)
        return True

    def has_node(self, asset_id: str) -> bool:
        return asset_id in self._nodes

    def get_node(self, asset_id: str) -> Optional[AssetNode]:
        return self._nodes.get(asset_id)

    def get_node_count(self) -> int:
        return len(self._nodes)

    def get_all_node_ids(self) -> list[str]:
        return list(self._nodes.keys())

    def get_nodes_by_type(self, asset_type: str) -> list[AssetNode]:
        return [n for n in self._nodes.values() if n.asset_type == asset_type]

    # ------------------------------------------------------------------
    # Edges
    # ------------------------------------------------------------------

    def add_dependency(self, asset_id: str, dep_id: str) -> bool:
        """Record that *asset_id* depends on *dep_id*."""
        if asset_id not in self._nodes or dep_id not in self._nodes:
            logger.warning("AssetDependencyGraph: cannot add edge %s→%s "
                           "(node missing)", asset_id, dep_id)
            return False
        if dep_id not in self._forward[asset_id]:
            self._forward[asset_id].append(dep_id)
        if asset_id not in self._reverse[dep_id]:
            self._reverse[dep_id].append(asset_id)
        return True

    def remove_dependency(self, asset_id: str, dep_id: str) -> bool:
        try:
            self._forward[asset_id].remove(dep_id)
            self._reverse[dep_id].remove(asset_id)
            return True
        except (KeyError, ValueError):
            return False

    def has_dependency(self, asset_id: str, dep_id: str) -> bool:
        return dep_id in self._forward.get(asset_id, [])

    def get_edge_count(self) -> int:
        return sum(len(v) for v in self._forward.values())

    # ------------------------------------------------------------------
    # Traversal
    # ------------------------------------------------------------------

    def get_dependencies(self, asset_id: str,
                          transitive: bool = False) -> list[str]:
        """Return direct (or transitive) dependencies of *asset_id*."""
        if not transitive:
            return list(self._forward.get(asset_id, []))
        return self._bfs(asset_id, self._forward)

    def get_dependents(self, asset_id: str,
                        transitive: bool = False) -> list[str]:
        """Return assets that directly (or transitively) depend on *asset_id*."""
        if not transitive:
            return list(self._reverse.get(asset_id, []))
        return self._bfs(asset_id, self._reverse)

    @staticmethod
    def _bfs(start: str, graph: dict[str, list[str]]) -> list[str]:
        visited: list[str] = []
        queue = deque(graph.get(start, []))
        seen = {start}
        while queue:
            node = queue.popleft()
            if node in seen:
                continue
            seen.add(node)
            visited.append(node)
            for n in graph.get(node, []):
                if n not in seen:
                    queue.append(n)
        return visited

    def get_roots(self) -> list[str]:
        """Assets that nothing depends on (i.e. entry points)."""
        return [nid for nid in self._nodes
                if not self._reverse.get(nid)]

    def get_leaves(self) -> list[str]:
        """Assets that have no dependencies themselves."""
        return [nid for nid in self._nodes
                if not self._forward.get(nid)]

    def detect_cycles(self) -> list[list[str]]:
        """Return list of cycles (each cycle as list of node IDs).  Empty = no cycles."""
        visited: set[str] = set()
        rec_stack: set[str] = set()
        cycles: list[list[str]] = []

        def _dfs(node: str, path: list[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            for dep in self._forward.get(node, []):
                if dep not in visited:
                    _dfs(dep, path)
                elif dep in rec_stack:
                    idx = path.index(dep)
                    cycles.append(list(path[idx:]))
            path.pop()
            rec_stack.discard(node)

        for nid in self._nodes:
            if nid not in visited:
                _dfs(nid, [])
        return cycles

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str) -> bool:
        try:
            data = {
                "nodes": [
                    {"asset_id": n.asset_id, "asset_type": n.asset_type,
                     "path": n.path, "tags": n.tags, "metadata": n.metadata}
                    for n in self._nodes.values()
                ],
                "edges": [
                    {"from": aid, "to": dep}
                    for aid, deps in self._forward.items()
                    for dep in deps
                ],
            }
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("AssetDependencyGraph.save failed: %s", exc)
            return False

    def load(self, path: str) -> bool:
        try:
            data = json.loads(Path(path).read_text())
            self.clear()
            for n in data.get("nodes", []):
                self.add_node(n["asset_id"], n["asset_type"],
                              n.get("path", ""), n.get("tags", []),
                              n.get("metadata", {}))
            for e in data.get("edges", []):
                self.add_dependency(e["from"], e["to"])
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("AssetDependencyGraph.load failed: %s", exc)
            return False

    def clear(self) -> None:
        self._nodes.clear()
        self._forward.clear()
        self._reverse.clear()
