"""AtlasAI Phase 35B — Conversation Graph Pipeline.

Manages conversation graph nodes, edges, and graph entries
for the dialogue and conversation authoring subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ConversationNodeDef:
    """Definition of a single conversation graph node."""

    node_id: str
    node_name: str
    node_type: str = "Dialogue"   # Dialogue/Choice/Condition/Action/Jump/Entry/Exit/Custom
    speaker_id: str = ""
    text: str = ""
    conditions: list = field(default_factory=list)
    actions: list = field(default_factory=list)

    @property
    def is_dialogue(self) -> bool:
        return self.node_type == "Dialogue"

    @property
    def has_conditions(self) -> bool:
        return bool(self.conditions)

    @property
    def has_actions(self) -> bool:
        return bool(self.actions)


@dataclass
class ConversationEdgeDef:
    """Definition of a directed edge between two conversation nodes."""

    edge_id: str
    from_node_id: str
    to_node_id: str
    edge_label: str = ""
    condition: str = ""

    @property
    def has_condition(self) -> bool:
        return bool(self.condition)


@dataclass
class ConversationGraphEntry:
    """Entry representing a full conversation graph."""

    graph_id: str
    graph_name: str
    nodes: list = field(default_factory=list)
    edges: list = field(default_factory=list)
    entry_node_id: str = ""
    owner_npc_id: str = ""

    @property
    def is_empty(self) -> bool:
        return not self.nodes

    @property
    def has_entry(self) -> bool:
        return bool(self.entry_node_id)

    @property
    def has_edges(self) -> bool:
        return bool(self.edges)


class ConversationGraphPipeline:
    """Pipeline for managing conversation graphs, nodes, and edges."""

    def __init__(self) -> None:
        self._graphs: Dict[str, ConversationGraphEntry] = {}
        self._nodes: Dict[str, Dict[str, ConversationNodeDef]] = {}
        self._edges: Dict[str, Dict[str, ConversationEdgeDef]] = {}

    def add_graph(self, g: ConversationGraphEntry) -> None:
        """Register a conversation graph."""
        self._graphs[g.graph_id] = g
        self._nodes.setdefault(g.graph_id, {})
        self._edges.setdefault(g.graph_id, {})

    def remove_graph(self, graph_id: str) -> bool:
        """Remove a graph by ID."""
        if graph_id in self._graphs:
            del self._graphs[graph_id]
            self._nodes.pop(graph_id, None)
            self._edges.pop(graph_id, None)
            return True
        return False

    def get_graph(self, graph_id: str) -> Optional[ConversationGraphEntry]:
        """Retrieve a graph by ID."""
        return self._graphs.get(graph_id)

    def get_all_graphs(self) -> List[ConversationGraphEntry]:
        """Return all registered graphs."""
        return list(self._graphs.values())

    def add_node(self, graph_id: str, node: ConversationNodeDef) -> bool:
        """Add a node to a graph."""
        if graph_id not in self._graphs:
            return False
        self._nodes.setdefault(graph_id, {})[node.node_id] = node
        graph = self._graphs[graph_id]
        if node.node_id not in graph.nodes:
            graph.nodes.append(node.node_id)
        return True

    def remove_node(self, graph_id: str, node_id: str) -> bool:
        """Remove a node from a graph."""
        nodes = self._nodes.get(graph_id, {})
        if node_id in nodes:
            del nodes[node_id]
            graph = self._graphs.get(graph_id)
            if graph and node_id in graph.nodes:
                graph.nodes.remove(node_id)
            return True
        return False

    def add_edge(self, graph_id: str, edge: ConversationEdgeDef) -> bool:
        """Add an edge to a graph."""
        if graph_id not in self._graphs:
            return False
        self._edges.setdefault(graph_id, {})[edge.edge_id] = edge
        graph = self._graphs[graph_id]
        if edge.edge_id not in graph.edges:
            graph.edges.append(edge.edge_id)
        return True

    def remove_edge(self, graph_id: str, edge_id: str) -> bool:
        """Remove an edge from a graph."""
        edges = self._edges.get(graph_id, {})
        if edge_id in edges:
            del edges[edge_id]
            graph = self._graphs.get(graph_id)
            if graph and edge_id in graph.edges:
                graph.edges.remove(edge_id)
            return True
        return False

    def set_entry_node(self, graph_id: str, node_id: str) -> bool:
        """Set the entry node for a graph."""
        graph = self._graphs.get(graph_id)
        if graph is None:
            return False
        graph.entry_node_id = node_id
        return True

    def get_nodes_by_type(self, graph_id: str, node_type: str) -> List[ConversationNodeDef]:
        """Return all nodes in a graph of a given type."""
        nodes = self._nodes.get(graph_id, {})
        return [n for n in nodes.values() if n.node_type == node_type]

    def get_edges_for_node(self, graph_id: str, node_id: str) -> List[ConversationEdgeDef]:
        """Return all outgoing edges from a node in a graph."""
        edges = self._edges.get(graph_id, {})
        return [e for e in edges.values() if e.from_node_id == node_id]

    def validate(self, graph: ConversationGraphEntry) -> bool:
        """Validate a graph has required fields."""
        return bool(graph.graph_id) and bool(graph.graph_name)

    def clear(self) -> None:
        """Clear all conversation graph data."""
        self._graphs.clear()
        self._nodes.clear()
        self._edges.clear()

    @property
    def graph_count(self) -> int:
        return len(self._graphs)

    @property
    def is_empty(self) -> bool:
        return len(self._graphs) == 0
