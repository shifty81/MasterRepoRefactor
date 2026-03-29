"""AtlasAI Phase 33B — Environment Query Pipeline.

Manages EQS queries, generators, tests, and results
for the Environment Query System authoring subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class EQSGeneratorConfig:
    """Configuration for an EQS generator."""

    generator_id: str
    generator_name: str
    generator_type: str = "OnCircle"    # ActorsOfClass/OnCircle/Grid/PathingGrid/Composite/Custom
    radius: float = 500.0
    density: float = 100.0
    max_items: int = 50
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_grid(self) -> bool:
        return self.generator_type == "Grid"


@dataclass
class EQSTestConfig:
    """Configuration for an EQS test."""

    test_id: str
    test_name: str
    test_type: str = "Distance"     # Distance/Dot/Trace/Overlap/Pathfinding/Gameplay/Custom
    weight: float = 1.0
    filter_min: float = 0.0
    filter_max: float = 10000.0
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_filtered(self) -> bool:
        return self.filter_max < 10000.0


@dataclass
class EQSQueryResult:
    """Result produced by running an EQS query."""

    job_id: str
    query_id: str
    items: list = field(default_factory=list)
    best_item_id: str = ""
    score: float = 0.0
    elapsed_ms: float = 0.0

    @property
    def has_results(self) -> bool:
        return bool(self.items)

    @property
    def item_count(self) -> int:
        return len(self.items)


class EnvironmentQueryPipeline:
    """Pipeline for managing and running EQS queries."""

    def __init__(self) -> None:
        self._queries: Dict[str, dict] = {}
        self._generators: Dict[str, List[EQSGeneratorConfig]] = {}
        self._tests: Dict[str, List[EQSTestConfig]] = {}
        self._job_counter: int = 0

    def add_query(self, query_id: str, name: str) -> None:
        """Register a new EQS query."""
        self._queries[query_id] = {"query_id": query_id, "name": name}
        self._generators.setdefault(query_id, [])
        self._tests.setdefault(query_id, [])

    def remove_query(self, query_id: str) -> bool:
        """Remove a query by ID."""
        if query_id in self._queries:
            del self._queries[query_id]
            self._generators.pop(query_id, None)
            self._tests.pop(query_id, None)
            return True
        return False

    def get_query(self, query_id: str) -> Optional[dict]:
        """Retrieve a query by ID."""
        return self._queries.get(query_id)

    def get_all_queries(self) -> List[dict]:
        """Return all registered queries."""
        return list(self._queries.values())

    def add_generator(self, query_id: str, generator: EQSGeneratorConfig) -> bool:
        """Add a generator configuration to a query."""
        if query_id not in self._queries:
            return False
        self._generators.setdefault(query_id, []).append(generator)
        return True

    def add_test(self, query_id: str, test: EQSTestConfig) -> bool:
        """Add a test configuration to a query."""
        if query_id not in self._queries:
            return False
        self._tests.setdefault(query_id, []).append(test)
        return True

    def run(self, query_id: str) -> EQSQueryResult:
        """Run a single query and return results."""
        self._job_counter += 1
        job_id = f"job_{self._job_counter:04d}"
        result = EQSQueryResult(job_id=job_id, query_id=query_id)
        if query_id in self._queries:
            logger.debug("Running EQS query %s (job %s)", query_id, job_id)
        return result

    def run_all(self) -> List[EQSQueryResult]:
        """Run all registered queries and return results."""
        return [self.run(qid) for qid in list(self._queries)]

    def validate(self, query_id: str) -> bool:
        """Validate a query has required configuration."""
        return query_id in self._queries

    def clear(self) -> None:
        """Clear all queries, generators, and tests."""
        self._queries.clear()
        self._generators.clear()
        self._tests.clear()

    @property
    def query_count(self) -> int:
        return len(self._queries)

    @property
    def is_empty(self) -> bool:
        return len(self._queries) == 0
