"""AtlasAI Phase 35B — Matchmaking Pipeline.

Manages matchmaking rule sets, match sessions, and match results
for the online matchmaking and session authoring subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class MatchmakingRuleSet:
    """Rule set definition for matchmaking configuration."""

    ruleset_id: str
    ruleset_name: str
    min_players: int = 2
    max_players: int = 16
    skill_tolerance: float = 100.0
    latency_budget_ms: float = 150.0
    require_same_region: bool = False

    @property
    def is_strict_region(self) -> bool:
        return self.require_same_region

    @property
    def has_skill_matching(self) -> bool:
        return self.skill_tolerance < 500.0


@dataclass
class MatchSession:
    """Definition of a single match session."""

    session_id: str
    session_name: str
    ruleset_id: str = ""
    host_player_id: str = ""
    players: list = field(default_factory=list)
    max_players: int = 16
    session_state: str = "Pending"
    region: str = "us-east"

    @property
    def is_full(self) -> bool:
        return len(self.players) >= self.max_players

    @property
    def is_active(self) -> bool:
        return self.session_state in ("Active", "InProgress")

    @property
    def has_ruleset(self) -> bool:
        return bool(self.ruleset_id)


@dataclass
class MatchResult:
    """Result record for a completed match session."""

    result_id: str
    session_id: str
    winner_team: str = ""
    outcome: str = "Undecided"
    duration_s: float = 0.0
    players_finished: list = field(default_factory=list)
    score_map: dict = field(default_factory=dict)

    @property
    def is_decided(self) -> bool:
        return self.outcome != "Undecided"

    @property
    def has_scores(self) -> bool:
        return bool(self.score_map)


class MatchmakingPipeline:
    """Pipeline for managing matchmaking rule sets, sessions, and results."""

    def __init__(self) -> None:
        self._rulesets: Dict[str, MatchmakingRuleSet] = {}
        self._sessions: Dict[str, MatchSession] = {}
        self._results: Dict[str, MatchResult] = {}

    def add_ruleset(self, r: MatchmakingRuleSet) -> None:
        """Register a matchmaking rule set."""
        self._rulesets[r.ruleset_id] = r

    def remove_ruleset(self, ruleset_id: str) -> bool:
        """Remove a rule set by ID."""
        if ruleset_id in self._rulesets:
            del self._rulesets[ruleset_id]
            return True
        return False

    def get_ruleset(self, ruleset_id: str) -> Optional[MatchmakingRuleSet]:
        """Retrieve a rule set by ID."""
        return self._rulesets.get(ruleset_id)

    def get_all_rulesets(self) -> List[MatchmakingRuleSet]:
        """Return all registered rule sets."""
        return list(self._rulesets.values())

    def create_session(self, s: MatchSession) -> None:
        """Register a match session."""
        self._sessions[s.session_id] = s

    def close_session(self, session_id: str) -> bool:
        """Close and remove a session by ID."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def get_session(self, session_id: str) -> Optional[MatchSession]:
        """Retrieve a session by ID."""
        return self._sessions.get(session_id)

    def get_all_sessions(self) -> List[MatchSession]:
        """Return all registered sessions."""
        return list(self._sessions.values())

    def add_player(self, session_id: str, player_id: str) -> bool:
        """Add a player to a session."""
        session = self._sessions.get(session_id)
        if session is None:
            return False
        if player_id not in session.players:
            session.players.append(player_id)
        return True

    def remove_player(self, session_id: str, player_id: str) -> bool:
        """Remove a player from a session."""
        session = self._sessions.get(session_id)
        if session is None:
            return False
        if player_id in session.players:
            session.players.remove(player_id)
            return True
        return False

    def set_session_state(self, session_id: str, state: str) -> bool:
        """Set the state of a session."""
        session = self._sessions.get(session_id)
        if session is None:
            return False
        session.session_state = state
        return True

    def record_result(self, result: MatchResult) -> None:
        """Record a match result."""
        self._results[result.result_id] = result

    def get_result(self, result_id: str) -> Optional[MatchResult]:
        """Retrieve a result by ID."""
        return self._results.get(result_id)

    def get_results_by_session(self, session_id: str) -> List[MatchResult]:
        """Return all results for a given session."""
        return [r for r in self._results.values() if r.session_id == session_id]

    def validate(self, session: MatchSession) -> bool:
        """Validate a match session has required fields."""
        return bool(session.session_id) and bool(session.session_name)

    def clear(self) -> None:
        """Clear all matchmaking data."""
        self._rulesets.clear()
        self._sessions.clear()
        self._results.clear()

    @property
    def session_count(self) -> int:
        return len(self._sessions)

    @property
    def is_empty(self) -> bool:
        return len(self._sessions) == 0
