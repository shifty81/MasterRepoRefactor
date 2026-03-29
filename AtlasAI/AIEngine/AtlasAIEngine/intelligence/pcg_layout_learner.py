"""AtlasAI Phase 18C — Dev AI Phase 4: PCG Layout Learner.

Ingests approved placement layouts and updates the PCG baseline parameters
so future procedural generation reflects developer-approved patterns.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class LayoutSample:
    """A single approved layout sample ingested from an export file."""
    layout_id: str
    entity_type_counts: dict = field(default_factory=dict)
    average_spacing: float = 0.0
    placement_count: int = 0


class PCGLayoutLearner:
    """Learns PCG baseline parameters from approved placement layouts.

    Workflow:
        1. PlacementPCGBridge exports approved layouts to JSON
        2. PCGLayoutLearner.ingest() reads those files
        3. PCGLayoutLearner.compute_baseline() derives density/spacing params
        4. Params can be exported back to solar_system_pcg_config.json

    Example::

        learner = PCGLayoutLearner()
        learner.ingest("/path/to/layout_001.json")
        baseline = learner.compute_baseline()
        learner.export_baseline("/path/to/solar_system_pcg_config.json")
    """

    def __init__(self) -> None:
        self._samples: list[LayoutSample] = []
        self._entity_counts: dict[str, list[int]] = defaultdict(list)

    def ingest(self, layout_path: str) -> bool:
        """Load and register a layout JSON file. Returns True on success."""
        path = Path(layout_path)
        if not path.exists():
            logger.warning("PCGLayoutLearner: file not found: %s", path)
            return False
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("PCGLayoutLearner: failed to parse %s: %s", path, exc)
            return False

        placements = data.get("placements", [])
        type_counts: dict[str, int] = defaultdict(int)
        for p in placements:
            type_counts[p.get("entity_type", "Unknown")] += 1

        sample = LayoutSample(
            layout_id=data.get("layout_id", path.stem),
            entity_type_counts=dict(type_counts),
            placement_count=len(placements),
        )
        self._samples.append(sample)
        for etype, count in type_counts.items():
            self._entity_counts[etype].append(count)
        logger.info("PCGLayoutLearner: ingested layout '%s' (%d placements)",
                    sample.layout_id, sample.placement_count)
        return True

    def compute_baseline(self) -> dict:
        """Derive average density parameters from all ingested layouts."""
        if not self._samples:
            return {}
        baseline: dict = {}
        for etype, counts in self._entity_counts.items():
            avg = sum(counts) / len(counts)
            baseline[f"{etype.lower()}_density"] = round(avg / 10.0, 3)
        baseline["sample_count"] = len(self._samples)
        logger.info("PCGLayoutLearner: computed baseline from %d samples", len(self._samples))
        return baseline

    def export_baseline(self, config_path: str) -> bool:
        """Merge computed baseline into an existing PCG config JSON file."""
        baseline = self.compute_baseline()
        if not baseline:
            logger.warning("PCGLayoutLearner: no samples to export")
            return False
        path = Path(config_path)
        existing: dict = {}
        if path.exists():
            try:
                existing = json.loads(path.read_text())
            except (json.JSONDecodeError, OSError):
                pass
        existing.update(baseline)
        existing["learned"] = True
        path.write_text(json.dumps(existing, indent=2))
        logger.info("PCGLayoutLearner: exported baseline → %s", path)
        return True

    def get_sample_count(self) -> int:
        """Return the number of ingested layout samples."""
        return len(self._samples)

    def get_entity_types(self) -> list[str]:
        """Return all entity types seen across ingested layouts."""
        return list(self._entity_counts.keys())

    def clear(self) -> None:
        """Clear all ingested samples."""
        self._samples.clear()
        self._entity_counts.clear()
