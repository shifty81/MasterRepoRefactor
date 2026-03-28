"""Tests for AtlasAI core/live_ingestion.py — NovaForgeLiveIngestion."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "AIEngine" / "AtlasAIEngine"))

from core.live_ingestion import (
    EconomySnapshot,
    FactionSnapshot,
    IngestionConfig,
    IngestionSnapshot,
    NovaForgeLiveIngestion,
    PlayerSystemsSnapshot,
    WorldStateSnapshot,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_stub_raw(sequence: int = 1) -> dict:
    now = "2026-03-28T12:00:00Z"
    return {
        "sequenceId": sequence,
        "capturedAt": now,
        "economy": {
            "capturedAt": now, "activeMarkets": 10,
            "openOrderCount": 200, "globalPriceIndex": 1.05,
            "topResourceId": "iron_ore", "topResourcePrice": 30.0,
        },
        "factions": {
            "capturedAt": now, "factionCount": 5,
            "hostilePairCount": 1, "activeConflicts": 1,
            "dominantFactionId": "pirates",
        },
        "world": {
            "capturedAt": now, "loadedSectorCount": 3,
            "totalEntityCount": 400, "activePlayerCount": 20,
            "simulationRunning": True, "activeSectorId": "alpha-1",
        },
        "players": {
            "capturedAt": now, "onlinePlayerCount": 20,
            "inCombatCount": 2, "dockedCount": 8, "inSpaceCount": 10,
        },
    }


# ---------------------------------------------------------------------------
# Snapshot data-class tests
# ---------------------------------------------------------------------------

class TestSnapshotDataClasses(unittest.TestCase):
    def test_economy_snapshot_defaults(self):
        s = EconomySnapshot()
        self.assertEqual(s.active_markets, 0)
        self.assertEqual(s.global_price_index, 1.0)

    def test_economy_snapshot_to_dict(self):
        s = EconomySnapshot(captured_at="now", active_markets=5, top_resource_id="gold")
        d = s.to_dict()
        self.assertEqual(d["active_markets"], 5)
        self.assertEqual(d["top_resource_id"], "gold")

    def test_faction_snapshot_defaults(self):
        s = FactionSnapshot()
        self.assertEqual(s.faction_count, 0)
        self.assertEqual(s.dominant_faction_id, "")

    def test_faction_snapshot_to_dict(self):
        s = FactionSnapshot(faction_count=3, dominant_faction_id="navy")
        d = s.to_dict()
        self.assertEqual(d["faction_count"], 3)
        self.assertEqual(d["dominant_faction"], "navy")

    def test_world_state_snapshot_to_dict(self):
        s = WorldStateSnapshot(loaded_sector_count=4, simulation_running=True)
        d = s.to_dict()
        self.assertEqual(d["loaded_sector_count"], 4)
        self.assertTrue(d["simulation_running"])

    def test_player_systems_snapshot_to_dict(self):
        s = PlayerSystemsSnapshot(online_player_count=10, in_combat_count=2)
        d = s.to_dict()
        self.assertEqual(d["online_player_count"], 10)

    def test_ingestion_snapshot_to_dict_has_all_keys(self):
        snap = IngestionSnapshot(sequence_id=1, captured_at="now")
        d = snap.to_dict()
        for key in ("sequence_id", "captured_at", "economy", "factions", "world", "players"):
            self.assertIn(key, d)


# ---------------------------------------------------------------------------
# NovaForgeLiveIngestion — construction
# ---------------------------------------------------------------------------

class TestLiveIngestionConstruction(unittest.TestCase):
    def test_default_config(self):
        ing = NovaForgeLiveIngestion()
        self.assertIsNotNone(ing.config)
        self.assertTrue(ing.config.include_economy)

    def test_custom_config(self):
        cfg = IngestionConfig(include_economy=False, poll_interval_seconds=2.0)
        ing = NovaForgeLiveIngestion(config=cfg)
        self.assertFalse(ing.config.include_economy)
        self.assertEqual(ing.config.poll_interval_seconds, 2.0)

    def test_initial_state(self):
        ing = NovaForgeLiveIngestion()
        self.assertFalse(ing.is_running)
        self.assertEqual(ing.sequence, 0)
        self.assertEqual(ing.consecutive_failures, 0)
        self.assertIsNone(ing.get_last_snapshot())


# ---------------------------------------------------------------------------
# NovaForgeLiveIngestion — stub mode (no network)
# ---------------------------------------------------------------------------

class TestLiveIngestionStubMode(unittest.TestCase):
    def setUp(self) -> None:
        self.ing = NovaForgeLiveIngestion()

    def test_poll_once_stub_returns_snapshot(self):
        snap = self.ing.poll_once()
        self.assertIsNotNone(snap)

    def test_poll_once_increments_sequence(self):
        self.ing.poll_once()
        self.assertEqual(self.ing.sequence, 1)
        self.ing.poll_once()
        self.assertEqual(self.ing.sequence, 2)

    def test_poll_once_resets_failure_count(self):
        self.ing.poll_once()
        self.assertEqual(self.ing.consecutive_failures, 0)

    def test_last_snapshot_set_after_poll(self):
        self.ing.poll_once()
        self.assertIsNotNone(self.ing.get_last_snapshot())

    def test_last_economy_populated(self):
        self.ing.poll_once()
        eco = self.ing.get_last_economy()
        self.assertIsNotNone(eco)
        assert eco is not None
        self.assertGreater(eco.active_markets, 0)

    def test_last_factions_populated(self):
        self.ing.poll_once()
        fac = self.ing.get_last_factions()
        self.assertIsNotNone(fac)
        assert fac is not None
        self.assertGreater(fac.faction_count, 0)

    def test_last_world_populated(self):
        self.ing.poll_once()
        wld = self.ing.get_last_world()
        self.assertIsNotNone(wld)

    def test_last_players_populated(self):
        self.ing.poll_once()
        plr = self.ing.get_last_players()
        self.assertIsNotNone(plr)


# ---------------------------------------------------------------------------
# NovaForgeLiveIngestion — custom fetcher
# ---------------------------------------------------------------------------

class TestLiveIngestionCustomFetcher(unittest.TestCase):
    def test_fetcher_is_called(self):
        calls = []
        def fetcher():
            calls.append(1)
            return _make_stub_raw()

        ing = NovaForgeLiveIngestion()
        ing.attach_fetcher(fetcher)
        ing.poll_once()
        self.assertEqual(len(calls), 1)

    def test_fetcher_data_is_parsed(self):
        ing = NovaForgeLiveIngestion()
        ing.attach_fetcher(lambda: _make_stub_raw())
        snap = ing.poll_once()
        self.assertIsNotNone(snap)
        assert snap is not None
        self.assertEqual(snap.economy.active_markets, 10)
        self.assertEqual(snap.factions.dominant_faction_id, "pirates")
        self.assertTrue(snap.world.simulation_running)
        self.assertEqual(snap.world.active_sector_id, "alpha-1")
        self.assertEqual(snap.players.in_combat_count, 2)

    def test_fetcher_returning_none_counts_failure(self):
        ing = NovaForgeLiveIngestion()
        ing.attach_fetcher(lambda: None)
        result = ing.poll_once()
        self.assertIsNone(result)
        self.assertEqual(ing.consecutive_failures, 1)

    def test_fetcher_exception_counts_failure(self):
        ing = NovaForgeLiveIngestion()
        def bad_fetcher():
            raise RuntimeError("network error")
        ing.attach_fetcher(bad_fetcher)
        result = ing.poll_once()
        self.assertIsNone(result)
        self.assertEqual(ing.consecutive_failures, 1)

    def test_success_resets_failure_count(self):
        call_count = [0]
        def intermittent():
            call_count[0] += 1
            if call_count[0] < 3:
                return None
            return _make_stub_raw()

        ing = NovaForgeLiveIngestion()
        ing.attach_fetcher(intermittent)
        ing.poll_once()  # fails
        ing.poll_once()  # fails
        ing.poll_once()  # succeeds
        self.assertEqual(ing.consecutive_failures, 0)


# ---------------------------------------------------------------------------
# NovaForgeLiveIngestion — inject_stub_snapshot
# ---------------------------------------------------------------------------

class TestLiveIngestionInjectStub(unittest.TestCase):
    def test_inject_sets_last_snapshot(self):
        ing = NovaForgeLiveIngestion()
        snap = IngestionSnapshot(sequence_id=99, captured_at="2026-01-01")
        ing.inject_stub_snapshot(snap)
        self.assertIsNotNone(ing.get_last_snapshot())

    def test_inject_increments_sequence(self):
        ing = NovaForgeLiveIngestion()
        snap = IngestionSnapshot()
        ing.inject_stub_snapshot(snap)
        self.assertEqual(ing.sequence, 1)

    def test_inject_sets_captured_at_if_empty(self):
        ing = NovaForgeLiveIngestion()
        snap = IngestionSnapshot()
        ing.inject_stub_snapshot(snap)
        last = ing.get_last_snapshot()
        assert last is not None
        self.assertNotEqual(last.captured_at, "")


# ---------------------------------------------------------------------------
# NovaForgeLiveIngestion — listeners
# ---------------------------------------------------------------------------

class TestLiveIngestionListeners(unittest.TestCase):
    def test_listener_called_on_poll(self):
        received = []
        ing = NovaForgeLiveIngestion()
        ing.add_listener(received.append)
        ing.poll_once()
        self.assertEqual(len(received), 1)

    def test_listener_receives_snapshot(self):
        received = []
        ing = NovaForgeLiveIngestion()
        ing.add_listener(received.append)
        ing.poll_once()
        self.assertIsInstance(received[0], IngestionSnapshot)

    def test_multiple_listeners(self):
        a, b = [], []
        ing = NovaForgeLiveIngestion()
        ing.add_listener(a.append)
        ing.add_listener(b.append)
        ing.poll_once()
        self.assertEqual(len(a), 1)
        self.assertEqual(len(b), 1)

    def test_remove_listener(self):
        received = []
        ing = NovaForgeLiveIngestion()
        ing.add_listener(received.append)
        ing.remove_listener(received.append)
        ing.poll_once()
        self.assertEqual(len(received), 0)

    def test_clear_listeners(self):
        received = []
        ing = NovaForgeLiveIngestion()
        ing.add_listener(received.append)
        ing.clear_listeners()
        ing.poll_once()
        self.assertEqual(len(received), 0)

    def test_listener_exception_does_not_stop_ingestion(self):
        def bad_listener(_snap):
            raise RuntimeError("boom")

        ing = NovaForgeLiveIngestion()
        ing.add_listener(bad_listener)
        # Should not raise
        snap = ing.poll_once()
        self.assertIsNotNone(snap)

    def test_listener_called_on_inject(self):
        received = []
        ing = NovaForgeLiveIngestion()
        ing.add_listener(received.append)
        ing.inject_stub_snapshot(IngestionSnapshot())
        self.assertEqual(len(received), 1)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

class TestLiveIngestionParsing(unittest.TestCase):
    def setUp(self) -> None:
        self.ing = NovaForgeLiveIngestion()

    def test_parse_partial_raw_missing_factions(self):
        raw = _make_stub_raw()
        del raw["factions"]
        snap = self.ing._parse_snapshot(raw)
        # Factions should default to empty snapshot, not crash
        self.assertEqual(snap.factions.faction_count, 0)

    def test_parse_empty_subsections(self):
        raw = {"sequenceId": 1, "capturedAt": "now",
               "economy": {}, "factions": {}, "world": {}, "players": {}}
        snap = self.ing._parse_snapshot(raw)
        self.assertEqual(snap.economy.active_markets, 0)
        self.assertEqual(snap.world.simulation_running, False)

    def test_parse_captured_at_propagated(self):
        raw = _make_stub_raw()
        snap = self.ing._parse_snapshot(raw)
        self.assertEqual(snap.captured_at, "2026-03-28T12:00:00Z")


if __name__ == "__main__":
    unittest.main()
