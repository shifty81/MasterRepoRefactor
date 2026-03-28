"""live_ingestion.py — MasterRepo NovaForge live data ingestion pipeline for AtlasAI.

Polls the NovaForge bridge service and maintains an in-process cache of the
latest game-state snapshots (economy, factions, world state, player systems).
AtlasAI tools and agents query this module to reason about live project state.

Responsibilities:
- Fetch IngestionSnapshots from the NovaForge bridge endpoint.
- Cache the latest snapshot per subsystem.
- Provide a delta-tracking mechanism so consumers only see changes.
- Support a synchronous stub mode (no network) for testing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional
from core.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Snapshot data classes
# ---------------------------------------------------------------------------

@dataclass
class EconomySnapshot:
    captured_at:         str   = ""
    active_markets:      int   = 0
    open_order_count:    int   = 0
    global_price_index:  float = 1.0
    top_resource_id:     str   = ""
    top_resource_price:  float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "captured_at":        self.captured_at,
            "active_markets":     self.active_markets,
            "open_order_count":   self.open_order_count,
            "global_price_index": self.global_price_index,
            "top_resource_id":    self.top_resource_id,
            "top_resource_price": self.top_resource_price,
        }


@dataclass
class FactionSnapshot:
    captured_at:         str  = ""
    faction_count:       int  = 0
    hostile_pair_count:  int  = 0
    active_conflicts:    int  = 0
    dominant_faction_id: str  = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "captured_at":        self.captured_at,
            "faction_count":      self.faction_count,
            "hostile_pair_count": self.hostile_pair_count,
            "active_conflicts":   self.active_conflicts,
            "dominant_faction":   self.dominant_faction_id,
        }


@dataclass
class WorldStateSnapshot:
    captured_at:          str  = ""
    loaded_sector_count:  int  = 0
    total_entity_count:   int  = 0
    active_player_count:  int  = 0
    simulation_running:   bool = False
    active_sector_id:     str  = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "captured_at":         self.captured_at,
            "loaded_sector_count": self.loaded_sector_count,
            "total_entity_count":  self.total_entity_count,
            "active_player_count": self.active_player_count,
            "simulation_running":  self.simulation_running,
            "active_sector_id":    self.active_sector_id,
        }


@dataclass
class PlayerSystemsSnapshot:
    captured_at:         str = ""
    online_player_count: int = 0
    in_combat_count:     int = 0
    docked_count:        int = 0
    in_space_count:      int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "captured_at":          self.captured_at,
            "online_player_count":  self.online_player_count,
            "in_combat_count":      self.in_combat_count,
            "docked_count":         self.docked_count,
            "in_space_count":       self.in_space_count,
        }


@dataclass
class IngestionSnapshot:
    sequence_id: int                      = 0
    captured_at: str                      = ""
    economy:     EconomySnapshot          = field(default_factory=EconomySnapshot)
    factions:    FactionSnapshot          = field(default_factory=FactionSnapshot)
    world:       WorldStateSnapshot       = field(default_factory=WorldStateSnapshot)
    players:     PlayerSystemsSnapshot    = field(default_factory=PlayerSystemsSnapshot)

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence_id": self.sequence_id,
            "captured_at": self.captured_at,
            "economy":     self.economy.to_dict(),
            "factions":    self.factions.to_dict(),
            "world":       self.world.to_dict(),
            "players":     self.players.to_dict(),
        }


# ---------------------------------------------------------------------------
# Ingestion configuration
# ---------------------------------------------------------------------------

@dataclass
class IngestionConfig:
    include_economy:          bool = True
    include_factions:         bool = True
    include_world_state:      bool = True
    include_player_systems:   bool = True
    poll_interval_seconds:    float = 5.0
    max_consecutive_failures: int = 5


# ---------------------------------------------------------------------------
# Snapshot listener type
# ---------------------------------------------------------------------------

SnapshotListener = Callable[[IngestionSnapshot], None]


# ---------------------------------------------------------------------------
# NovaForgeLiveIngestion
# ---------------------------------------------------------------------------

class NovaForgeLiveIngestion:
    """
    Manages a live ingestion stream from the NovaForge bridge into AtlasAI.

    In production, call ``attach_fetcher()`` with a function that performs
    the actual HTTP call to the bridge.  In tests or stub mode, call
    ``inject_stub_snapshot()`` to push data directly.

    Usage::

        ingestion = NovaForgeLiveIngestion(config=IngestionConfig())
        ingestion.attach_fetcher(my_http_fetcher)
        snapshot = ingestion.poll_once()
        ingestion.add_listener(lambda s: print(s.sequence_id))
    """

    def __init__(self, config: Optional[IngestionConfig] = None) -> None:
        self._config      = config or IngestionConfig()
        self._last: Optional[IngestionSnapshot] = None
        self._sequence:   int   = 0
        self._failures:   int   = 0
        self._running:    bool  = False
        self._listeners:  list[SnapshotListener] = []
        self._fetcher:    Optional[Callable[[], Optional[dict[str, Any]]]] = None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @property
    def config(self) -> IngestionConfig:
        return self._config

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def consecutive_failures(self) -> int:
        return self._failures

    @property
    def sequence(self) -> int:
        return self._sequence

    # ------------------------------------------------------------------
    # Fetcher / stub injection
    # ------------------------------------------------------------------

    def attach_fetcher(
        self, fetcher: Callable[[], Optional[dict[str, Any]]]
    ) -> None:
        """
        Attach a callable that fetches a raw snapshot dict from the bridge.
        The callable should return None on failure.
        """
        self._fetcher = fetcher

    def inject_stub_snapshot(self, snapshot: IngestionSnapshot) -> None:
        """Push a snapshot directly (used in tests and stub mode)."""
        self._sequence    += 1
        snapshot.sequence_id = self._sequence
        if not snapshot.captured_at:
            snapshot.captured_at = datetime.now(timezone.utc).isoformat()
        self._last     = snapshot
        self._failures = 0
        self._notify(snapshot)

    # ------------------------------------------------------------------
    # Polling
    # ------------------------------------------------------------------

    def poll_once(self) -> Optional[IngestionSnapshot]:
        """
        Execute a single poll.  Uses the attached fetcher if present,
        otherwise builds a stub snapshot.
        Returns the snapshot on success, None on failure.
        """
        raw = self._fetch_raw()
        if raw is None:
            self._failures += 1
            logger.warning(
                "Live ingestion poll failed (consecutive=%d)", self._failures
            )
            return None

        snapshot = self._parse_snapshot(raw)
        self._sequence    += 1
        snapshot.sequence_id = self._sequence
        self._last         = snapshot
        self._failures     = 0
        self._notify(snapshot)
        logger.debug("Ingestion snapshot #%d captured", self._sequence)
        return snapshot

    def _fetch_raw(self) -> Optional[dict[str, Any]]:
        if self._fetcher is not None:
            try:
                return self._fetcher()
            except Exception as exc:
                logger.error("Fetcher raised: %s", exc)
                return None
        # Stub mode: synthesise data
        return self._build_stub_raw()

    def _build_stub_raw(self) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        return {
            "sequenceId": self._sequence + 1,
            "capturedAt": now,
            "economy": {
                "capturedAt": now, "activeMarkets": 12,
                "openOrderCount": 340, "globalPriceIndex": 1.02,
                "topResourceId": "titanium_ore", "topResourcePrice": 42.5,
            },
            "factions": {
                "capturedAt": now, "factionCount": 8,
                "hostilePairCount": 2, "activeConflicts": 1,
                "dominantFactionId": "imperial_navy",
            },
            "world": {
                "capturedAt": now, "loadedSectorCount": 4,
                "totalEntityCount": 512, "activePlayerCount": 24,
                "simulationRunning": True, "activeSectorId": "sector-alpha-7",
            },
            "players": {
                "capturedAt": now, "onlinePlayerCount": 24,
                "inCombatCount": 3, "dockedCount": 11, "inSpaceCount": 10,
            },
        }

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_snapshot(raw: dict[str, Any]) -> IngestionSnapshot:
        snap = IngestionSnapshot()
        snap.captured_at = str(raw.get("capturedAt", ""))

        eco = raw.get("economy") or {}
        snap.economy = EconomySnapshot(
            captured_at        = str(eco.get("capturedAt", "")),
            active_markets     = int(eco.get("activeMarkets", 0)),
            open_order_count   = int(eco.get("openOrderCount", 0)),
            global_price_index = float(eco.get("globalPriceIndex", 1.0)),
            top_resource_id    = str(eco.get("topResourceId", "")),
            top_resource_price = float(eco.get("topResourcePrice", 0.0)),
        )

        fac = raw.get("factions") or {}
        snap.factions = FactionSnapshot(
            captured_at         = str(fac.get("capturedAt", "")),
            faction_count       = int(fac.get("factionCount", 0)),
            hostile_pair_count  = int(fac.get("hostilePairCount", 0)),
            active_conflicts    = int(fac.get("activeConflicts", 0)),
            dominant_faction_id = str(fac.get("dominantFactionId", "")),
        )

        wld = raw.get("world") or {}
        snap.world = WorldStateSnapshot(
            captured_at          = str(wld.get("capturedAt", "")),
            loaded_sector_count  = int(wld.get("loadedSectorCount", 0)),
            total_entity_count   = int(wld.get("totalEntityCount", 0)),
            active_player_count  = int(wld.get("activePlayerCount", 0)),
            simulation_running   = bool(wld.get("simulationRunning", False)),
            active_sector_id     = str(wld.get("activeSectorId", "")),
        )

        plr = raw.get("players") or {}
        snap.players = PlayerSystemsSnapshot(
            captured_at          = str(plr.get("capturedAt", "")),
            online_player_count  = int(plr.get("onlinePlayerCount", 0)),
            in_combat_count      = int(plr.get("inCombatCount", 0)),
            docked_count         = int(plr.get("dockedCount", 0)),
            in_space_count       = int(plr.get("inSpaceCount", 0)),
        )

        return snap

    # ------------------------------------------------------------------
    # Last-known state
    # ------------------------------------------------------------------

    def get_last_snapshot(self) -> Optional[IngestionSnapshot]:
        return self._last

    def get_last_economy(self) -> Optional[EconomySnapshot]:
        return self._last.economy if self._last else None

    def get_last_factions(self) -> Optional[FactionSnapshot]:
        return self._last.factions if self._last else None

    def get_last_world(self) -> Optional[WorldStateSnapshot]:
        return self._last.world if self._last else None

    def get_last_players(self) -> Optional[PlayerSystemsSnapshot]:
        return self._last.players if self._last else None

    # ------------------------------------------------------------------
    # Listeners
    # ------------------------------------------------------------------

    def add_listener(self, listener: SnapshotListener) -> None:
        """Register a callback invoked on every successful snapshot."""
        self._listeners.append(listener)

    def remove_listener(self, listener: SnapshotListener) -> None:
        self._listeners = [l for l in self._listeners if l != listener]

    def clear_listeners(self) -> None:
        self._listeners.clear()

    def _notify(self, snapshot: IngestionSnapshot) -> None:
        for listener in self._listeners:
            try:
                listener(snapshot)
            except Exception as exc:
                logger.error("Ingestion listener raised: %s", exc)
