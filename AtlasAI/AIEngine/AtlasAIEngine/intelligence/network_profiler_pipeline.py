"""AtlasAI Phase 38B — Network Profiler Pipeline.

Manages network profiling sessions, samples, and anomaly records
for the NetworkProfilerTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class NetworkSampleEntry:
    """A single network metric sample."""
    sample_id: str
    session_id: str
    metric_type: str = "Bandwidth"
    value: float = 0.0
    timestamp: float = 0.0

    @property
    def is_latency(self) -> bool:
        return self.metric_type == "Latency"

    @property
    def is_high_value(self) -> bool:
        return self.value > 1000.0

    @property
    def has_timestamp(self) -> bool:
        return self.timestamp > 0.0


@dataclass
class NetworkAnomalyEntry:
    """A detected network anomaly."""
    anomaly_id: str
    session_id: str
    metric_type: str = "Latency"
    threshold: float = 0.0
    actual_value: float = 0.0
    acknowledged: bool = False

    @property
    def is_critical(self) -> bool:
        return self.actual_value > self.threshold * 2

    @property
    def is_acknowledged(self) -> bool:
        return self.acknowledged

    @property
    def severity_ratio(self) -> float:
        if self.threshold > 0:
            return self.actual_value / self.threshold
        return 0.0


@dataclass
class ProfilerSessionEntry:
    """A profiling session containing samples and anomalies."""
    session_id: str
    session_name: str
    state: str = "Idle"
    filter: str = "AllTraffic"
    samples: list = field(default_factory=list)
    anomalies: list = field(default_factory=list)
    enabled: bool = True

    @property
    def is_recording(self) -> bool:
        return self.state == "Recording"

    @property
    def is_completed(self) -> bool:
        return self.state == "Completed"

    @property
    def has_anomalies(self) -> bool:
        return bool(self.anomalies)

    @property
    def sample_count(self) -> int:
        return len(self.samples)

    @property
    def is_enabled(self) -> bool:
        return self.enabled


class NetworkProfilerPipeline:
    """Pipeline for managing network profiling sessions, samples, and anomalies."""

    def __init__(self) -> None:
        self._sessions: Dict[str, ProfilerSessionEntry] = {}

    # Session CRUD
    def add_session(self, entry: ProfilerSessionEntry) -> bool:
        if not entry.session_id:
            return False
        self._sessions[entry.session_id] = entry
        return True

    def get_session(self, session_id: str) -> Optional[ProfilerSessionEntry]:
        return self._sessions.get(session_id)

    def remove_session(self, session_id: str) -> bool:
        if session_id not in self._sessions:
            return False
        del self._sessions[session_id]
        return True

    def get_all_sessions(self) -> List[ProfilerSessionEntry]:
        return list(self._sessions.values())

    # Sample management
    def add_sample(self, session_id: str, sample: NetworkSampleEntry) -> bool:
        session = self._sessions.get(session_id)
        if session is None:
            return False
        session.samples.append(sample)
        return True

    def remove_sample(self, session_id: str, sample_id: str) -> bool:
        session = self._sessions.get(session_id)
        if session is None:
            return False
        before = len(session.samples)
        session.samples = [s for s in session.samples if s.sample_id != sample_id]
        return len(session.samples) < before

    def get_samples_for_session(self, session_id: str) -> list:
        session = self._sessions.get(session_id)
        if session is None:
            return []
        return list(session.samples)

    # Anomaly management
    def add_anomaly(self, session_id: str, anomaly: NetworkAnomalyEntry) -> bool:
        session = self._sessions.get(session_id)
        if session is None:
            return False
        session.anomalies.append(anomaly)
        return True

    def remove_anomaly(self, session_id: str, anomaly_id: str) -> bool:
        session = self._sessions.get(session_id)
        if session is None:
            return False
        before = len(session.anomalies)
        session.anomalies = [a for a in session.anomalies if a.anomaly_id != anomaly_id]
        return len(session.anomalies) < before

    def get_anomalies_for_session(self, session_id: str) -> list:
        session = self._sessions.get(session_id)
        if session is None:
            return []
        return list(session.anomalies)

    def get_unacknowledged_anomalies(self) -> list:
        result = []
        for session in self._sessions.values():
            result.extend(a for a in session.anomalies if not a.acknowledged)
        return result

    def get_recording_sessions(self) -> List[ProfilerSessionEntry]:
        return [s for s in self._sessions.values() if s.state == "Recording"]

    # State management
    def set_state(self, session_id: str, state: str) -> bool:
        session = self._sessions.get(session_id)
        if session is None:
            return False
        session.state = state
        return True

    def get_enabled_sessions(self) -> List[ProfilerSessionEntry]:
        return [s for s in self._sessions.values() if s.enabled]

    def get_disabled_sessions(self) -> List[ProfilerSessionEntry]:
        return [s for s in self._sessions.values() if not s.enabled]

    # Validation
    def validate(self, entry: ProfilerSessionEntry) -> bool:
        return bool(entry.session_id) and bool(entry.session_name)

    # Properties
    @property
    def session_count(self) -> int:
        return len(self._sessions)

    @property
    def is_empty(self) -> bool:
        return len(self._sessions) == 0

    def clear(self) -> None:
        self._sessions.clear()
