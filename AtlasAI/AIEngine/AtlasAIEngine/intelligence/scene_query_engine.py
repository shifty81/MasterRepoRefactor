"""AtlasAI Phase 19B — Scene Query Engine.

Provides a flexible query API for filtering and inspecting scene graph entities
by type, property, tag, or spatial criteria.  Results are returned as
lightweight SceneEntityRecord objects and can be exported to JSON for
AI-driven decision making.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


@dataclass
class SceneEntityRecord:
    """Lightweight snapshot of a scene entity returned by a query."""

    entity_id: str
    entity_type: str
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    tags: list[str] = field(default_factory=list)
    properties: dict[str, Any] = field(default_factory=dict)


class SceneQueryEngine:
    """Filter and inspect scene entities using composable predicates.

    Entities are registered at load / spawn time.  Queries are expressed as
    Python callables (or the built-in helpers) and executed against the
    in-memory registry.

    Example::

        engine = SceneQueryEngine()
        engine.register("ent_01", "Planet", 0.0, 0.0, 1.0, tags=["habitable"])
        engine.register("ent_02", "Station", 0.0, 0.0, 1.2, tags=["dev"])
        planets = engine.query_by_type("Planet")
        tagged  = engine.query_by_tag("habitable")
    """

    def __init__(self) -> None:
        self._entities: dict[str, SceneEntityRecord] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        entity_id: str,
        entity_type: str,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        tags: Optional[list[str]] = None,
        properties: Optional[dict[str, Any]] = None,
    ) -> SceneEntityRecord:
        """Register or update a scene entity."""
        record = SceneEntityRecord(
            entity_id=entity_id,
            entity_type=entity_type,
            x=x,
            y=y,
            z=z,
            tags=list(tags or []),
            properties=dict(properties or {}),
        )
        self._entities[entity_id] = record
        logger.debug("Registered scene entity %s (%s)", entity_id, entity_type)
        return record

    def unregister(self, entity_id: str) -> bool:
        """Remove an entity from the registry.  Returns True if it existed."""
        if entity_id in self._entities:
            del self._entities[entity_id]
            return True
        return False

    def get_entity(self, entity_id: str) -> Optional[SceneEntityRecord]:
        """Return the record for *entity_id*, or None."""
        return self._entities.get(entity_id)

    def get_entity_count(self) -> int:
        """Return the total number of registered entities."""
        return len(self._entities)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def query(self, predicate: Callable[[SceneEntityRecord], bool]) -> list[SceneEntityRecord]:
        """Return all entities for which *predicate* returns True."""
        return [e for e in self._entities.values() if predicate(e)]

    def query_by_type(self, entity_type: str) -> list[SceneEntityRecord]:
        """Return all entities of the given type."""
        return self.query(lambda e: e.entity_type == entity_type)

    def query_by_tag(self, tag: str) -> list[SceneEntityRecord]:
        """Return all entities that carry *tag*."""
        return self.query(lambda e: tag in e.tags)

    def query_by_property(self, key: str, value: Any) -> list[SceneEntityRecord]:
        """Return all entities where properties[key] == value."""
        return self.query(lambda e: e.properties.get(key) == value)

    def query_within_radius(
        self, cx: float, cz: float, radius: float
    ) -> list[SceneEntityRecord]:
        """Return all entities whose XZ distance from (cx, cz) ≤ radius."""
        r2 = radius * radius

        def _within(e: SceneEntityRecord) -> bool:
            dx = e.x - cx
            dz = e.z - cz
            return (dx * dx + dz * dz) <= r2

        return self.query(_within)

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_results(self, results: list[SceneEntityRecord], path: str) -> bool:
        """Serialise *results* to a JSON file at *path*.  Returns True on success."""
        try:
            data = [
                {
                    "entity_id": r.entity_id,
                    "entity_type": r.entity_type,
                    "x": r.x,
                    "y": r.y,
                    "z": r.z,
                    "tags": r.tags,
                    "properties": r.properties,
                }
                for r in results
            ]
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("Failed to export query results: %s", exc)
            return False

    def clear(self) -> None:
        """Remove all registered entities."""
        self._entities.clear()
