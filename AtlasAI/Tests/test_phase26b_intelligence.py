"""Phase 26B — Tests for PhysicsSimulationCache and BehaviorTreeCompiler."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    PhysicsSimulationCache,
    PhysicsSimulationEntry,
    PhysicsFrameData,
    CachePolicy,
    BehaviorTreeCompiler,
    BTSourceTree,
    BTNodeDef,
    BTCompileResult,
    BTBytecodeInstruction,
)

TMP_DIR = Path("/tmp/test_phase26b")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# PhysicsFrameData dataclass
# ---------------------------------------------------------------------------

class TestPhysicsFrameDataDataclass(unittest.TestCase):
    def test_frame_index_field(self):
        f = PhysicsFrameData(frame_index=5, simulation_id="sim_0001")
        self.assertEqual(f.frame_index, 5)

    def test_simulation_id_field(self):
        f = PhysicsFrameData(frame_index=0, simulation_id="sim_0001")
        self.assertEqual(f.simulation_id, "sim_0001")

    def test_default_kinetic_energy(self):
        f = PhysicsFrameData(frame_index=0, simulation_id="s")
        self.assertAlmostEqual(f.kinetic_energy, 0.0)

    def test_total_energy(self):
        f = PhysicsFrameData(frame_index=0, simulation_id="s",
                              kinetic_energy=10.0, potential_energy=5.0)
        self.assertAlmostEqual(f.total_energy, 15.0)


# ---------------------------------------------------------------------------
# PhysicsSimulationEntry dataclass
# ---------------------------------------------------------------------------

class TestPhysicsSimulationEntryDataclass(unittest.TestCase):
    def test_simulation_id_field(self):
        import time
        e = PhysicsSimulationEntry("s001", "test_sim", created_at=time.time())
        self.assertEqual(e.simulation_id, "s001")

    def test_name_field(self):
        import time
        e = PhysicsSimulationEntry("s001", "test_sim", created_at=time.time())
        self.assertEqual(e.name, "test_sim")

    def test_stored_frame_count_empty(self):
        import time
        e = PhysicsSimulationEntry("s001", "test_sim", created_at=time.time())
        self.assertEqual(e.stored_frame_count, 0)

    def test_is_complete_no_frames(self):
        import time
        e = PhysicsSimulationEntry("s001", "test_sim",
                                    frame_count=0, created_at=time.time())
        self.assertFalse(e.is_complete)

    def test_cache_size_kb(self):
        import time
        e = PhysicsSimulationEntry("s001", "test_sim",
                                    cache_size_bytes=2048, created_at=time.time())
        self.assertAlmostEqual(e.cache_size_kb, 2.0)


# ---------------------------------------------------------------------------
# CachePolicy dataclass
# ---------------------------------------------------------------------------

class TestCachePolicyDataclass(unittest.TestCase):
    def test_policy_id_field(self):
        p = CachePolicy(policy_id="strict")
        self.assertEqual(p.policy_id, "strict")

    def test_default_max_entries(self):
        p = CachePolicy(policy_id="default")
        self.assertEqual(p.max_entries, 100)

    def test_default_eviction_strategy(self):
        p = CachePolicy(policy_id="default")
        self.assertEqual(p.eviction_strategy, "LRU")


# ---------------------------------------------------------------------------
# PhysicsSimulationCache — entry management
# ---------------------------------------------------------------------------

class TestPhysicsSimulationCacheEntries(unittest.TestCase):
    def setUp(self):
        self.cache = PhysicsSimulationCache()

    def test_create_entry_returns_entry(self):
        e = self.cache.create_entry("cloth_sim", scene_id="scene_01")
        self.assertIsInstance(e, PhysicsSimulationEntry)

    def test_entry_name(self):
        e = self.cache.create_entry("cloth_sim")
        self.assertEqual(e.name, "cloth_sim")

    def test_simulation_id_unique(self):
        e1 = self.cache.create_entry("a")
        e2 = self.cache.create_entry("b")
        self.assertNotEqual(e1.simulation_id, e2.simulation_id)

    def test_get_entry_count(self):
        self.cache.create_entry("a")
        self.cache.create_entry("b")
        self.assertEqual(self.cache.get_entry_count(), 2)

    def test_get_entry_by_id(self):
        e = self.cache.create_entry("cloth")
        fetched = self.cache.get_entry(e.simulation_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "cloth")

    def test_get_entry_missing_returns_none(self):
        result = self.cache.get_entry("ghost")
        self.assertIsNone(result)

    def test_has_entry_true(self):
        e = self.cache.create_entry("cloth")
        self.assertTrue(self.cache.has_entry(e.simulation_id))

    def test_has_entry_false(self):
        self.assertFalse(self.cache.has_entry("ghost"))

    def test_remove_entry(self):
        e = self.cache.create_entry("cloth")
        self.assertTrue(self.cache.remove_entry(e.simulation_id))
        self.assertEqual(self.cache.get_entry_count(), 0)

    def test_remove_entry_missing_false(self):
        self.assertFalse(self.cache.remove_entry("ghost"))

    def test_get_all_simulation_ids(self):
        e = self.cache.create_entry("cloth")
        self.assertIn(e.simulation_id, self.cache.get_all_simulation_ids())

    def test_get_entries_for_scene(self):
        e = self.cache.create_entry("cloth", scene_id="scene_A")
        self.cache.create_entry("rigid", scene_id="scene_B")
        ids = self.cache.get_entries_for_scene("scene_A")
        self.assertIn(e.simulation_id, ids)
        self.assertEqual(len(ids), 1)

    def test_clear(self):
        self.cache.create_entry("cloth")
        self.cache.clear()
        self.assertEqual(self.cache.get_entry_count(), 0)


# ---------------------------------------------------------------------------
# PhysicsSimulationCache — frame storage
# ---------------------------------------------------------------------------

class TestPhysicsSimulationCacheFrames(unittest.TestCase):
    def setUp(self):
        self.cache = PhysicsSimulationCache()
        self.entry = self.cache.create_entry("rigid_sim", frame_count=100,
                                               frame_rate=60.0, body_count=5)

    def test_store_frame_returns_frame(self):
        f = self.cache.store_frame(self.entry.simulation_id, 0,
                                    kinetic_energy=10.0, potential_energy=5.0)
        self.assertIsInstance(f, PhysicsFrameData)

    def test_frame_index_set(self):
        f = self.cache.store_frame(self.entry.simulation_id, 42)
        self.assertEqual(f.frame_index, 42)

    def test_frame_kinetic_energy(self):
        f = self.cache.store_frame(self.entry.simulation_id, 0,
                                    kinetic_energy=20.0)
        self.assertAlmostEqual(f.kinetic_energy, 20.0)

    def test_frame_count_increases(self):
        self.cache.store_frame(self.entry.simulation_id, 0)
        self.cache.store_frame(self.entry.simulation_id, 1)
        self.assertEqual(
            self.cache.get_frame_count(self.entry.simulation_id), 2
        )

    def test_get_frame_by_index(self):
        self.cache.store_frame(self.entry.simulation_id, 5, kinetic_energy=3.0)
        f = self.cache.get_frame(self.entry.simulation_id, 5)
        self.assertIsNotNone(f)
        self.assertAlmostEqual(f.kinetic_energy, 3.0)

    def test_get_frame_missing_returns_none(self):
        self.assertIsNone(
            self.cache.get_frame(self.entry.simulation_id, 999)
        )

    def test_store_frame_unknown_sim_returns_none(self):
        result = self.cache.store_frame("ghost", 0)
        self.assertIsNone(result)

    def test_clear_frames(self):
        self.cache.store_frame(self.entry.simulation_id, 0)
        self.assertTrue(self.cache.clear_frames(self.entry.simulation_id))
        self.assertEqual(
            self.cache.get_frame_count(self.entry.simulation_id), 0
        )

    def test_is_complete_after_enough_frames(self):
        for i in range(100):
            self.cache.store_frame(self.entry.simulation_id, i)
        self.assertTrue(self.entry.is_complete)


# ---------------------------------------------------------------------------
# PhysicsSimulationCache — statistics and eviction
# ---------------------------------------------------------------------------

class TestPhysicsSimulationCacheStats(unittest.TestCase):
    def setUp(self):
        self.cache = PhysicsSimulationCache()

    def test_hit_count_increments(self):
        e = self.cache.create_entry("a")
        self.cache.get_entry(e.simulation_id)
        self.assertEqual(self.cache.get_hit_count(), 1)

    def test_miss_count_increments(self):
        self.cache.get_entry("ghost")
        self.assertEqual(self.cache.get_miss_count(), 1)

    def test_hit_rate_zero_no_requests(self):
        self.assertAlmostEqual(self.cache.get_hit_rate(), 0.0)

    def test_hit_rate_calculation(self):
        e = self.cache.create_entry("a")
        self.cache.get_entry(e.simulation_id)
        self.cache.get_entry("ghost")
        self.assertAlmostEqual(self.cache.get_hit_rate(), 0.5)

    def test_reset_stats(self):
        e = self.cache.create_entry("a")
        self.cache.get_entry(e.simulation_id)
        self.cache.reset_stats()
        self.assertEqual(self.cache.get_hit_count(), 0)

    def test_evict_oldest(self):
        self.cache.create_entry("a")
        self.cache.create_entry("b")
        evicted = self.cache.evict_oldest(1)
        self.assertEqual(evicted, 1)
        self.assertEqual(self.cache.get_entry_count(), 1)

    def test_evict_by_scene(self):
        self.cache.create_entry("a", scene_id="scene_X")
        self.cache.create_entry("b", scene_id="scene_X")
        self.cache.create_entry("c", scene_id="scene_Y")
        evicted = self.cache.evict_by_scene("scene_X")
        self.assertEqual(evicted, 2)
        self.assertEqual(self.cache.get_entry_count(), 1)

    def test_set_policy(self):
        p = CachePolicy(policy_id="custom", max_entries=5)
        self.cache.set_policy(p)
        self.assertEqual(self.cache.get_policy().max_entries, 5)

    def test_save_index(self):
        self.cache.create_entry("cloth")
        out = str(TMP_DIR / "cache_index.json")
        self.assertTrue(self.cache.save_index(out))
        self.assertTrue(Path(out).exists())

    def test_total_cache_size_bytes(self):
        self.cache.create_entry("cloth")
        self.assertGreaterEqual(self.cache.get_total_cache_size_bytes(), 0)


# ---------------------------------------------------------------------------
# BTNodeDef dataclass
# ---------------------------------------------------------------------------

class TestBTNodeDefDataclass(unittest.TestCase):
    def test_node_id_field(self):
        n = BTNodeDef(node_id="n001", node_type="Action")
        self.assertEqual(n.node_id, "n001")

    def test_node_type_field(self):
        n = BTNodeDef(node_id="n001", node_type="Sequence")
        self.assertEqual(n.node_type, "Sequence")

    def test_child_count_empty(self):
        n = BTNodeDef(node_id="n001", node_type="Sequence")
        self.assertEqual(n.child_count, 0)

    def test_is_composite_sequence(self):
        n = BTNodeDef(node_id="n001", node_type="Sequence")
        self.assertTrue(n.is_composite)

    def test_is_composite_action_false(self):
        n = BTNodeDef(node_id="n001", node_type="Action")
        self.assertFalse(n.is_composite)

    def test_is_leaf_action(self):
        n = BTNodeDef(node_id="n001", node_type="Action")
        self.assertTrue(n.is_leaf)

    def test_is_leaf_sequence_false(self):
        n = BTNodeDef(node_id="n001", node_type="Sequence")
        self.assertFalse(n.is_leaf)


# ---------------------------------------------------------------------------
# BTCompileResult dataclass
# ---------------------------------------------------------------------------

class TestBTCompileResultDataclass(unittest.TestCase):
    def test_tree_id_field(self):
        r = BTCompileResult(tree_id="t001", tree_name="Guard")
        self.assertEqual(r.tree_id, "t001")

    def test_default_success_false(self):
        r = BTCompileResult(tree_id="t001", tree_name="Guard")
        self.assertFalse(r.success)

    def test_has_warnings_false(self):
        r = BTCompileResult(tree_id="t001", tree_name="Guard")
        self.assertFalse(r.has_warnings)

    def test_bytecode_size_bytes(self):
        r = BTCompileResult(tree_id="t001", tree_name="Guard",
                             instruction_count=10)
        self.assertEqual(r.bytecode_size_bytes, 640)


# ---------------------------------------------------------------------------
# BehaviorTreeCompiler — source tree management
# ---------------------------------------------------------------------------

class TestBehaviorTreeCompilerTrees(unittest.TestCase):
    def setUp(self):
        self.compiler = BehaviorTreeCompiler()

    def test_create_source_tree(self):
        t = self.compiler.create_source_tree("Guard")
        self.assertIsInstance(t, BTSourceTree)

    def test_tree_name(self):
        t = self.compiler.create_source_tree("Guard")
        self.assertEqual(t.name, "Guard")

    def test_tree_id_unique(self):
        t1 = self.compiler.create_source_tree("A")
        t2 = self.compiler.create_source_tree("B")
        self.assertNotEqual(t1.tree_id, t2.tree_id)

    def test_get_source_tree_count(self):
        self.compiler.create_source_tree("A")
        self.compiler.create_source_tree("B")
        self.assertEqual(self.compiler.get_source_tree_count(), 2)

    def test_get_all_tree_ids(self):
        t = self.compiler.create_source_tree("A")
        self.assertIn(t.tree_id, self.compiler.get_all_tree_ids())

    def test_get_source_tree_by_id(self):
        t = self.compiler.create_source_tree("Guard")
        fetched = self.compiler.get_source_tree(t.tree_id)
        self.assertIsNotNone(fetched)

    def test_remove_source_tree(self):
        t = self.compiler.create_source_tree("Guard")
        self.assertTrue(self.compiler.remove_source_tree(t.tree_id))
        self.assertEqual(self.compiler.get_source_tree_count(), 0)

    def test_remove_source_tree_missing(self):
        self.assertFalse(self.compiler.remove_source_tree("ghost"))

    def test_clear(self):
        self.compiler.create_source_tree("A")
        self.compiler.clear()
        self.assertEqual(self.compiler.get_source_tree_count(), 0)


# ---------------------------------------------------------------------------
# BehaviorTreeCompiler — node management
# ---------------------------------------------------------------------------

class TestBehaviorTreeCompilerNodes(unittest.TestCase):
    def setUp(self):
        self.compiler = BehaviorTreeCompiler()
        self.tree = self.compiler.create_source_tree("Guard")

    def test_add_node_returns_node(self):
        n = self.compiler.add_node(self.tree.tree_id, "Sequence")
        self.assertIsInstance(n, BTNodeDef)

    def test_node_type_set(self):
        n = self.compiler.add_node(self.tree.tree_id, "Action",
                                    action_id="AttackAction")
        self.assertEqual(n.node_type, "Action")

    def test_node_action_id(self):
        n = self.compiler.add_node(self.tree.tree_id, "Action",
                                    action_id="AttackAction")
        self.assertEqual(n.action_id, "AttackAction")

    def test_get_node_count(self):
        self.compiler.add_node(self.tree.tree_id, "Sequence")
        self.compiler.add_node(self.tree.tree_id, "Action")
        self.assertEqual(self.compiler.get_node_count(self.tree.tree_id), 2)

    def test_first_node_becomes_root(self):
        n = self.compiler.add_node(self.tree.tree_id, "Sequence")
        t = self.compiler.get_source_tree(self.tree.tree_id)
        self.assertEqual(t.root_node_id, n.node_id)

    def test_add_child(self):
        seq = self.compiler.add_node(self.tree.tree_id, "Sequence")
        act = self.compiler.add_node(self.tree.tree_id, "Action")
        result = self.compiler.add_child(self.tree.tree_id, seq.node_id, act.node_id)
        self.assertTrue(result)
        self.assertIn(act.node_id, seq.children)

    def test_set_root(self):
        self.compiler.add_node(self.tree.tree_id, "Sequence")
        sel = self.compiler.add_node(self.tree.tree_id, "Selector")
        self.assertTrue(self.compiler.set_root(self.tree.tree_id, sel.node_id))
        t = self.compiler.get_source_tree(self.tree.tree_id)
        self.assertEqual(t.root_node_id, sel.node_id)

    def test_add_blackboard_key(self):
        self.assertTrue(
            self.compiler.add_blackboard_key(self.tree.tree_id, "EnemySeen")
        )
        t = self.compiler.get_source_tree(self.tree.tree_id)
        self.assertIn("EnemySeen", t.blackboard_keys)

    def test_add_node_unknown_tree_returns_none(self):
        result = self.compiler.add_node("ghost", "Action")
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# BehaviorTreeCompiler — validation
# ---------------------------------------------------------------------------

class TestBehaviorTreeCompilerValidation(unittest.TestCase):
    def setUp(self):
        self.compiler = BehaviorTreeCompiler()
        self.tree = self.compiler.create_source_tree("Patrol")

    def test_validate_empty_tree_has_errors(self):
        errors = self.compiler.validate(self.tree.tree_id)
        self.assertGreater(len(errors), 0)

    def test_validate_with_root_action_no_errors(self):
        n = self.compiler.add_node(self.tree.tree_id, "Action",
                                    action_id="PatrolAction")
        self.compiler.set_root(self.tree.tree_id, n.node_id)
        errors = self.compiler.validate(self.tree.tree_id)
        self.assertEqual(errors, [])

    def test_validate_action_without_id_has_error(self):
        n = self.compiler.add_node(self.tree.tree_id, "Action")
        n.action_id = ""
        errors = self.compiler.validate(self.tree.tree_id)
        self.assertGreater(len(errors), 0)

    def test_validate_unknown_tree_returns_error(self):
        errors = self.compiler.validate("ghost")
        self.assertGreater(len(errors), 0)


# ---------------------------------------------------------------------------
# BehaviorTreeCompiler — compilation
# ---------------------------------------------------------------------------

class TestBehaviorTreeCompilerCompile(unittest.TestCase):
    def setUp(self):
        self.compiler = BehaviorTreeCompiler()
        self.tree = self.compiler.create_source_tree("Attack")
        seq = self.compiler.add_node(self.tree.tree_id, "Sequence")
        act = self.compiler.add_node(self.tree.tree_id, "Action",
                                      action_id="AttackAction")
        self.compiler.add_child(self.tree.tree_id, seq.node_id, act.node_id)
        self.compiler.set_root(self.tree.tree_id, seq.node_id)

    def test_compile_returns_result(self):
        r = self.compiler.compile(self.tree.tree_id)
        self.assertIsInstance(r, BTCompileResult)

    def test_compile_success(self):
        r = self.compiler.compile(self.tree.tree_id)
        self.assertTrue(r.success)

    def test_compile_has_instructions(self):
        r = self.compiler.compile(self.tree.tree_id)
        self.assertGreater(r.instruction_count, 0)

    def test_compile_instructions_are_list(self):
        r = self.compiler.compile(self.tree.tree_id)
        self.assertIsInstance(r.instructions, list)

    def test_compile_last_instruction_is_return(self):
        r = self.compiler.compile(self.tree.tree_id)
        self.assertEqual(r.instructions[-1].opcode, "Return")

    def test_get_result_after_compile(self):
        self.compiler.compile(self.tree.tree_id)
        r = self.compiler.get_result(self.tree.tree_id)
        self.assertIsNotNone(r)

    def test_compile_all_returns_list(self):
        self.compiler.create_source_tree("Empty")
        results = self.compiler.compile_all()
        self.assertEqual(len(results), 2)

    def test_compile_unknown_tree_fails(self):
        r = self.compiler.compile("ghost")
        self.assertFalse(r.success)

    def test_save_bytecode(self):
        self.compiler.compile(self.tree.tree_id)
        out = str(TMP_DIR / "bt_bytecode.json")
        self.assertTrue(self.compiler.save_bytecode(self.tree.tree_id, out))
        self.assertTrue(Path(out).exists())

    def test_save_bytecode_content(self):
        self.compiler.compile(self.tree.tree_id)
        out = str(TMP_DIR / "bt_bytecode2.json")
        self.compiler.save_bytecode(self.tree.tree_id, out)
        data = json.loads(Path(out).read_text())
        self.assertIn("instructions", data)
        self.assertIn("instruction_count", data)

    def test_save_bytecode_failed_compile_returns_false(self):
        empty = self.compiler.create_source_tree("Empty")
        self.compiler.compile(empty.tree_id)
        out = str(TMP_DIR / "bt_failed.json")
        # Failed compile has no saved bytecode
        result = self.compiler.get_result(empty.tree_id)
        if result and not result.success:
            self.assertFalse(
                self.compiler.save_bytecode(empty.tree_id, out)
            )

    def test_load_source_from_dict(self):
        data = {
            "name": "Loaded",
            "root_node_id": "n001",
            "nodes": [
                {"node_id": "n001", "node_type": "Action",
                 "action_id": "Idle"}
            ],
        }
        t = self.compiler.load_source_from_dict(data)
        self.assertIsNotNone(t)
        self.assertEqual(t.name, "Loaded")


# ---------------------------------------------------------------------------
# BTBytecodeInstruction dataclass
# ---------------------------------------------------------------------------

class TestBTBytecodeInstructionDataclass(unittest.TestCase):
    def test_opcode_field(self):
        ins = BTBytecodeInstruction(opcode="RunAction")
        self.assertEqual(ins.opcode, "RunAction")

    def test_default_jump_target(self):
        ins = BTBytecodeInstruction(opcode="Return")
        self.assertEqual(ins.jump_target, -1)

    def test_str_representation(self):
        ins = BTBytecodeInstruction(opcode="RunAction", operand_a="attack")
        s = str(ins)
        self.assertIn("RunAction", s)


if __name__ == "__main__":
    unittest.main()
