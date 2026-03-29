"""Phase 20B — Tests for AgentActionLog and ContentHashRegistry."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    AgentActionLog,
    ActionEntry,
    ContentHashRegistry,
    ContentHashEntry,
)

TMP_DIR = Path("/tmp/test_phase20b")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# ActionEntry dataclass
# ---------------------------------------------------------------------------

class TestActionEntryDataclass(unittest.TestCase):
    def test_action_id_field(self):
        e = ActionEntry("action_00001", "CodeSuggest", "2026-01-01T00:00:00+00:00")
        self.assertEqual(e.action_id, "action_00001")

    def test_action_type_field(self):
        e = ActionEntry("a", "Approve", "ts")
        self.assertEqual(e.action_type, "Approve")

    def test_timestamp_field(self):
        e = ActionEntry("a", "T", "2026-01-01T00:00:00+00:00")
        self.assertEqual(e.timestamp, "2026-01-01T00:00:00+00:00")

    def test_payload_default_empty(self):
        e = ActionEntry("a", "T", "ts")
        self.assertIsInstance(e.payload, dict)
        self.assertEqual(len(e.payload), 0)

    def test_result_default_none(self):
        e = ActionEntry("a", "T", "ts")
        self.assertIsNone(e.result)

    def test_success_default_true(self):
        e = ActionEntry("a", "T", "ts")
        self.assertTrue(e.success)


# ---------------------------------------------------------------------------
# AgentActionLog — basic recording
# ---------------------------------------------------------------------------

class TestAgentActionLogRecording(unittest.TestCase):
    def setUp(self):
        self.log = AgentActionLog(agent_id="test_agent")

    def test_agent_id_set(self):
        self.assertEqual(self.log.agent_id, "test_agent")

    def test_record_returns_string(self):
        aid = self.log.record("CodeSuggest")
        self.assertIsInstance(aid, str)

    def test_record_increments_count(self):
        self.log.record("A")
        self.log.record("B")
        self.assertEqual(self.log.get_entry_count(), 2)

    def test_record_with_payload(self):
        aid = self.log.record("CodeSuggest", payload={"file": "foo.cpp"})
        entry = self.log.get_entry(aid)
        self.assertEqual(entry.payload["file"], "foo.cpp")

    def test_get_entry_returns_action_entry(self):
        aid = self.log.record("Test")
        entry = self.log.get_entry(aid)
        self.assertIsInstance(entry, ActionEntry)

    def test_get_entry_missing_returns_none(self):
        self.assertIsNone(self.log.get_entry("nonexistent"))

    def test_set_result_returns_true(self):
        aid = self.log.record("Test")
        self.assertTrue(self.log.set_result(aid, "done", success=True))

    def test_set_result_updates_entry(self):
        aid = self.log.record("Test")
        self.log.set_result(aid, "applied", success=True)
        entry = self.log.get_entry(aid)
        self.assertEqual(entry.result, "applied")
        self.assertTrue(entry.success)

    def test_set_result_failure(self):
        aid = self.log.record("Test")
        self.log.set_result(aid, "rejected", success=False)
        entry = self.log.get_entry(aid)
        self.assertFalse(entry.success)

    def test_set_result_missing_returns_false(self):
        self.assertFalse(self.log.set_result("ghost", "x"))

    def test_clear_resets_count(self):
        self.log.record("A")
        self.log.clear()
        self.assertEqual(self.log.get_entry_count(), 0)


# ---------------------------------------------------------------------------
# AgentActionLog — query
# ---------------------------------------------------------------------------

class TestAgentActionLogQuery(unittest.TestCase):
    def setUp(self):
        self.log = AgentActionLog()
        self.log.record("CodeSuggest", payload={"file": "a.cpp"})
        self.log.record("CodeSuggest", payload={"file": "b.cpp"})
        aid = self.log.record("Approve")
        self.log.set_result(aid, "ok", success=True)
        fail_id = self.log.record("Reject")
        self.log.set_result(fail_id, "rejected", success=False)

    def test_get_by_type_code_suggest(self):
        results = self.log.get_by_type("CodeSuggest")
        self.assertEqual(len(results), 2)

    def test_get_by_type_approve(self):
        results = self.log.get_by_type("Approve")
        self.assertEqual(len(results), 1)

    def test_get_by_type_missing_returns_empty(self):
        self.assertEqual(self.log.get_by_type("Unknown"), [])

    def test_get_failures(self):
        failures = self.log.get_failures()
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0].action_type, "Reject")

    def test_total_count(self):
        self.assertEqual(self.log.get_entry_count(), 4)


# ---------------------------------------------------------------------------
# AgentActionLog — replay
# ---------------------------------------------------------------------------

class TestAgentActionLogReplay(unittest.TestCase):
    def setUp(self):
        self.log = AgentActionLog()
        self.log.record("A")
        self.log.record("B")
        self.log.record("C")

    def test_replay_returns_list(self):
        self.assertIsInstance(self.log.replay(), list)

    def test_replay_count(self):
        self.assertEqual(len(self.log.replay()), 3)

    def test_replay_order(self):
        entries = self.log.replay()
        types = [e.action_type for e in entries]
        self.assertEqual(types, ["A", "B", "C"])

    def test_replay_with_handler(self):
        seen = []
        self.log.replay(handler=lambda e: seen.append(e.action_type))
        self.assertEqual(seen, ["A", "B", "C"])


# ---------------------------------------------------------------------------
# AgentActionLog — persistence
# ---------------------------------------------------------------------------

class TestAgentActionLogPersistence(unittest.TestCase):
    def setUp(self):
        self.log = AgentActionLog(agent_id="persist_agent")
        aid = self.log.record("TestAction", payload={"k": "v"})
        self.log.set_result(aid, "done", success=True)

    def test_save_returns_true(self):
        path = str(TMP_DIR / "agent_log_save.json")
        self.assertTrue(self.log.save(path))

    def test_save_creates_file(self):
        path = str(TMP_DIR / "agent_log_create.json")
        self.log.save(path)
        self.assertTrue(Path(path).exists())

    def test_save_valid_json(self):
        path = str(TMP_DIR / "agent_log_json.json")
        self.log.save(path)
        data = json.loads(Path(path).read_text())
        self.assertEqual(data["agent_id"], "persist_agent")

    def test_load_returns_count(self):
        path = str(TMP_DIR / "agent_log_load.json")
        self.log.save(path)
        log2 = AgentActionLog()
        count = log2.load(path)
        self.assertEqual(count, 1)

    def test_load_restores_entries(self):
        path = str(TMP_DIR / "agent_log_restore.json")
        self.log.save(path)
        log2 = AgentActionLog()
        log2.load(path)
        self.assertEqual(log2.get_entry_count(), 1)

    def test_load_restores_agent_id(self):
        path = str(TMP_DIR / "agent_log_agent_id.json")
        self.log.save(path)
        log2 = AgentActionLog()
        log2.load(path)
        self.assertEqual(log2.agent_id, "persist_agent")

    def test_load_missing_returns_zero(self):
        log2 = AgentActionLog()
        self.assertEqual(log2.load("/nonexistent/log.json"), 0)


# ---------------------------------------------------------------------------
# ContentHashEntry dataclass
# ---------------------------------------------------------------------------

class TestContentHashEntryDataclass(unittest.TestCase):
    def test_path_field(self):
        e = ContentHashEntry("file.json", "abc123", 100)
        self.assertEqual(e.path, "file.json")

    def test_sha256_field(self):
        e = ContentHashEntry("file.json", "abc123", 100)
        self.assertEqual(e.sha256, "abc123")

    def test_size_bytes_field(self):
        e = ContentHashEntry("file.json", "abc123", 256)
        self.assertEqual(e.size_bytes, 256)

    def test_dirty_default_false(self):
        e = ContentHashEntry("file.json", "abc123", 0)
        self.assertFalse(e.dirty)


# ---------------------------------------------------------------------------
# ContentHashRegistry — hash helpers
# ---------------------------------------------------------------------------

class TestContentHashRegistryHashHelpers(unittest.TestCase):
    def test_hash_string_returns_64_chars(self):
        digest = ContentHashRegistry.hash_string("hello")
        self.assertEqual(len(digest), 64)

    def test_hash_string_deterministic(self):
        d1 = ContentHashRegistry.hash_string("same")
        d2 = ContentHashRegistry.hash_string("same")
        self.assertEqual(d1, d2)

    def test_hash_string_different_inputs(self):
        d1 = ContentHashRegistry.hash_string("abc")
        d2 = ContentHashRegistry.hash_string("xyz")
        self.assertNotEqual(d1, d2)

    def test_hash_file_real_file(self):
        path = TMP_DIR / "hash_test.txt"
        path.write_text("content for hashing")
        digest = ContentHashRegistry.hash_file(str(path))
        self.assertIsNotNone(digest)
        self.assertEqual(len(digest), 64)

    def test_hash_file_missing_returns_none(self):
        self.assertIsNone(ContentHashRegistry.hash_file("/nonexistent/file.txt"))


# ---------------------------------------------------------------------------
# ContentHashRegistry — registration
# ---------------------------------------------------------------------------

class TestContentHashRegistryRegistration(unittest.TestCase):
    def setUp(self):
        self.reg = ContentHashRegistry()

    def test_register_string_returns_entry(self):
        entry = self.reg.register_string("key1", "data")
        self.assertIsInstance(entry, ContentHashEntry)

    def test_register_string_increments_count(self):
        self.reg.register_string("k1", "data1")
        self.reg.register_string("k2", "data2")
        self.assertEqual(self.reg.get_entry_count(), 2)

    def test_get_entry_returns_entry(self):
        self.reg.register_string("k1", "data")
        entry = self.reg.get_entry("k1")
        self.assertIsNotNone(entry)

    def test_get_entry_missing_returns_none(self):
        self.assertIsNone(self.reg.get_entry("ghost"))

    def test_unregister_returns_true(self):
        self.reg.register_string("k1", "data")
        self.assertTrue(self.reg.unregister("k1"))

    def test_unregister_removes_entry(self):
        self.reg.register_string("k1", "data")
        self.reg.unregister("k1")
        self.assertEqual(self.reg.get_entry_count(), 0)

    def test_unregister_missing_returns_false(self):
        self.assertFalse(self.reg.unregister("ghost"))

    def test_register_file_real_file(self):
        path = TMP_DIR / "reg_test.json"
        path.write_text('{"id": "test"}')
        entry = self.reg.register_file(str(path))
        self.assertIsNotNone(entry)
        self.assertEqual(entry.path, str(path))

    def test_clear_removes_all(self):
        self.reg.register_string("k1", "data")
        self.reg.clear()
        self.assertEqual(self.reg.get_entry_count(), 0)


# ---------------------------------------------------------------------------
# ContentHashRegistry — change detection
# ---------------------------------------------------------------------------

class TestContentHashRegistryChangeDetection(unittest.TestCase):
    def setUp(self):
        self.reg = ContentHashRegistry()

    def test_check_string_no_change(self):
        self.reg.register_string("k1", "same")
        changed = self.reg.check_string("k1", "same")
        self.assertFalse(changed)

    def test_check_string_changed(self):
        self.reg.register_string("k1", "original")
        changed = self.reg.check_string("k1", "modified")
        self.assertTrue(changed)

    def test_check_string_marks_dirty(self):
        self.reg.register_string("k1", "original")
        self.reg.check_string("k1", "modified")
        entry = self.reg.get_entry("k1")
        self.assertTrue(entry.dirty)

    def test_get_dirty_returns_changed(self):
        self.reg.register_string("k1", "orig")
        self.reg.check_string("k1", "new")
        dirty = self.reg.get_dirty()
        self.assertEqual(len(dirty), 1)

    def test_clear_dirty_resets_flags(self):
        self.reg.register_string("k1", "orig")
        self.reg.check_string("k1", "new")
        count = self.reg.clear_dirty()
        self.assertEqual(count, 1)
        self.assertEqual(len(self.reg.get_dirty()), 0)

    def test_check_string_missing_key_returns_false(self):
        self.assertFalse(self.reg.check_string("ghost", "data"))


# ---------------------------------------------------------------------------
# ContentHashRegistry — persistence
# ---------------------------------------------------------------------------

class TestContentHashRegistryPersistence(unittest.TestCase):
    def setUp(self):
        self.reg = ContentHashRegistry()
        self.reg.register_string("k1", "data1")
        self.reg.register_string("k2", "data2")

    def test_save_returns_true(self):
        path = str(TMP_DIR / "hash_reg_save.json")
        self.assertTrue(self.reg.save(path))

    def test_save_creates_file(self):
        path = str(TMP_DIR / "hash_reg_create.json")
        self.reg.save(path)
        self.assertTrue(Path(path).exists())

    def test_load_returns_count(self):
        path = str(TMP_DIR / "hash_reg_load.json")
        self.reg.save(path)
        reg2 = ContentHashRegistry()
        count = reg2.load(path)
        self.assertEqual(count, 2)

    def test_load_restores_entries(self):
        path = str(TMP_DIR / "hash_reg_restore.json")
        self.reg.save(path)
        reg2 = ContentHashRegistry()
        reg2.load(path)
        self.assertEqual(reg2.get_entry_count(), 2)

    def test_load_missing_returns_zero(self):
        reg2 = ContentHashRegistry()
        self.assertEqual(reg2.load("/nonexistent/hashes.json"), 0)


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_agent_action_log_exported(self):
        from AtlasAIEngine.intelligence import AgentActionLog as AAL
        self.assertIsNotNone(AAL)

    def test_action_entry_exported(self):
        from AtlasAIEngine.intelligence import ActionEntry as AE
        self.assertIsNotNone(AE)

    def test_content_hash_registry_exported(self):
        from AtlasAIEngine.intelligence import ContentHashRegistry as CHR
        self.assertIsNotNone(CHR)

    def test_content_hash_entry_exported(self):
        from AtlasAIEngine.intelligence import ContentHashEntry as CHE
        self.assertIsNotNone(CHE)


if __name__ == "__main__":
    unittest.main()
