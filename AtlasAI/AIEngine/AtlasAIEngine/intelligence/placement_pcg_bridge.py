"""AtlasAI Phase 18C — Dev AI Phase 4: Placement + PCG Bridge.

Connects free-move object placement in the editor to the PCG learner,
so that agent-approved layouts are fed back into the generative baseline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class PlacementRecord:
    """A single approved entity placement."""
    entity_id: str
    entity_type: str
    x: float
    y: float
    z: float
    rotation_y: float = 0.0
    pcg_seed: Optional[int] = None
    approved: bool = False


class PlacementPCGBridge:
    """Routes editor placement events to the PCG learner baseline.

    Workflow:
        1. Developer places entity in scene → record created (approved=False)
        2. AI agent or developer calls approve_placement()
        3. On approval, placement is fed to PCGLayoutLearner as training data

    Example::

        bridge = PlacementPCGBridge("/repo/NovaForge/Content")
        pid = bridge.record_placement("ent_01", "Station", 0.0, 0.0, 1200.0)
        bridge.approve_placement(pid)
        bridge.export_approved_layout("layout_001.json")
    """

    def __init__(self, content_root: str) -> None:
        self.content_root = Path(content_root)
        self._placements: dict[str, PlacementRecord] = {}
        self._next_id = 0

    def record_placement(self, entity_id: str, entity_type: str,
                          x: float, y: float, z: float,
                          rotation_y: float = 0.0,
                          pcg_seed: Optional[int] = None) -> str:
        """Record a new placement. Returns a placement record ID."""
        pid = f"placement_{self._next_id:04d}"
        self._next_id += 1
        self._placements[pid] = PlacementRecord(
            entity_id=entity_id,
            entity_type=entity_type,
            x=x, y=y, z=z,
            rotation_y=rotation_y,
            pcg_seed=pcg_seed,
        )
        logger.debug("PlacementPCGBridge: recorded %s → %s", pid, entity_type)
        return pid

    def approve_placement(self, placement_id: str) -> bool:
        """Approve a placement record for PCG baseline integration."""
        record = self._placements.get(placement_id)
        if record is None:
            return False
        record.approved = True
        logger.info("PlacementPCGBridge: approved %s (%s)", placement_id, record.entity_type)
        return True

    def reject_placement(self, placement_id: str) -> bool:
        """Reject and remove a placement record."""
        if placement_id not in self._placements:
            return False
        del self._placements[placement_id]
        logger.info("PlacementPCGBridge: rejected %s", placement_id)
        return True

    def get_approved_placements(self) -> list[PlacementRecord]:
        """Return all approved placement records."""
        return [p for p in self._placements.values() if p.approved]

    def get_pending_placements(self) -> list[PlacementRecord]:
        """Return all unapproved (pending) placement records."""
        return [p for p in self._placements.values() if not p.approved]

    def export_approved_layout(self, output_filename: str) -> Path:
        """Serialize approved placements to a JSON layout file.

        Returns the absolute path to the written file.
        """
        import json
        approved = self.get_approved_placements()
        layout = {
            "layout_id": output_filename.replace(".json", ""),
            "placements": [
                {
                    "entity_id": p.entity_id,
                    "entity_type": p.entity_type,
                    "position": {"x": p.x, "y": p.y, "z": p.z},
                    "rotation_y": p.rotation_y,
                    "pcg_seed": p.pcg_seed,
                }
                for p in approved
            ],
        }
        out_path = self.content_root / output_filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(layout, indent=2))
        logger.info("PlacementPCGBridge: exported %d placements → %s",
                    len(approved), out_path)
        return out_path

    def clear(self) -> None:
        """Remove all placement records."""
        self._placements.clear()
        logger.debug("PlacementPCGBridge: cleared all records")

    def get_stats(self) -> dict:
        """Return stats about current placement records."""
        total = len(self._placements)
        approved = sum(1 for p in self._placements.values() if p.approved)
        return {"total": total, "approved": approved, "pending": total - approved}
