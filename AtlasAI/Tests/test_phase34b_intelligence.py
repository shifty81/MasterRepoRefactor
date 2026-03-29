"""Phase 34B — Tests for WorldPartitionPipeline and DataLayerPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    WorldPartitionPipeline,
    WorldPartitionEntry,
    StreamingCellDef,
    HLODLayerConfig,
    DataLayerPipeline,
    DataLayerSpec,
    DataLayerActorAssignment,
    DataLayerState,
)


# ---------------------------------------------------------------------------
# StreamingCellDef
# ---------------------------------------------------------------------------

class TestStreamingCellDef(unittest.TestCase):
    def test_cell_id(self):
        c = StreamingCellDef(cell_id="cell_001", grid_id="grid_001")
        self.assertEqual(c.cell_id, "cell_001")

    def test_grid_id(self):
        c = StreamingCellDef(cell_id="cell_001", grid_id="grid_001")
        self.assertEqual(c.grid_id, "grid_001")

    def test_default_cell_state(self):
        c = StreamingCellDef(cell_id="cell_001", grid_id="grid_001")
        self.assertEqual(c.cell_state, "Unloaded")

    def test_is_loaded_false(self):
        c = StreamingCellDef(cell_id="cell_001", grid_id="grid_001")
        self.assertFalse(c.is_loaded)

    def test_has_data_layers_false(self):
        c = StreamingCellDef(cell_id="cell_001", grid_id="grid_001")
        self.assertFalse(c.has_data_layers)


# ---------------------------------------------------------------------------
# HLODLayerConfig
# ---------------------------------------------------------------------------

class TestHLODLayerConfig(unittest.TestCase):
    def test_hlod_id(self):
        h = HLODLayerConfig(hlod_id="hlod_001", layer_name="HLOD Layer 0")
        self.assertEqual(h.hlod_id, "hlod_001")

    def test_layer_name(self):
        h = HLODLayerConfig(hlod_id="hlod_001", layer_name="HLOD Layer 0")
        self.assertEqual(h.layer_name, "HLOD Layer 0")

    def test_default_hlod_type(self):
        h = HLODLayerConfig(hlod_id="hlod_001", layer_name="HLOD Layer 0")
        self.assertEqual(h.hlod_type, "MeshMerge")

    def test_is_enabled_true(self):
        h = HLODLayerConfig(hlod_id="hlod_001", layer_name="HLOD Layer 0")
        self.assertTrue(h.is_enabled)

    def test_is_approximation_false(self):
        h = HLODLayerConfig(hlod_id="hlod_001", layer_name="HLOD Layer 0", hlod_type="MeshMerge")
        self.assertFalse(h.is_approximation)


# ---------------------------------------------------------------------------
# WorldPartitionEntry
# ---------------------------------------------------------------------------

class TestWorldPartitionEntry(unittest.TestCase):
    def test_entry_id(self):
        e = WorldPartitionEntry(entry_id="wp_001", world_name="OpenWorld")
        self.assertEqual(e.entry_id, "wp_001")

    def test_world_name(self):
        e = WorldPartitionEntry(entry_id="wp_001", world_name="OpenWorld")
        self.assertEqual(e.world_name, "OpenWorld")

    def test_default_cell_size(self):
        e = WorldPartitionEntry(entry_id="wp_001", world_name="OpenWorld")
        self.assertAlmostEqual(e.cell_size, 12800.0)

    def test_default_loading_radius(self):
        e = WorldPartitionEntry(entry_id="wp_001", world_name="OpenWorld")
        self.assertAlmostEqual(e.loading_radius, 25600.0)

    def test_is_streaming_enabled_true(self):
        e = WorldPartitionEntry(entry_id="wp_001", world_name="OpenWorld")
        self.assertTrue(e.is_streaming_enabled)

    def test_has_cells_false(self):
        e = WorldPartitionEntry(entry_id="wp_001", world_name="OpenWorld")
        self.assertFalse(e.has_cells)

    def test_has_hlod_false(self):
        e = WorldPartitionEntry(entry_id="wp_001", world_name="OpenWorld")
        self.assertFalse(e.has_hlod)


# ---------------------------------------------------------------------------
# WorldPartitionPipeline
# ---------------------------------------------------------------------------

class TestWorldPartitionPipeline(unittest.TestCase):
    def _pipeline(self):
        return WorldPartitionPipeline()

    def _entry(self, eid="wp_001"):
        return WorldPartitionEntry(entry_id=eid, world_name="OpenWorld")

    def _cell(self, cid="cell_001", gid="grid_001"):
        return StreamingCellDef(cell_id=cid, grid_id=gid)

    def test_add_world(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry())
        self.assertEqual(pipe.world_count, 1)

    def test_remove_world(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry())
        self.assertTrue(pipe.remove_world("wp_001"))
        self.assertEqual(pipe.world_count, 0)

    def test_get_world(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry())
        self.assertIsNotNone(pipe.get_world("wp_001"))

    def test_get_all_worlds(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry("wp_001"))
        pipe.add_world(self._entry("wp_002"))
        self.assertEqual(len(pipe.get_all_worlds()), 2)

    def test_add_cell(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry())
        self.assertTrue(pipe.add_cell("wp_001", self._cell()))

    def test_add_hlod_layer(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry())
        hlod = HLODLayerConfig(hlod_id="hlod_001", layer_name="HLOD Layer 0")
        self.assertTrue(pipe.add_hlod_layer("wp_001", hlod))

    def test_load_cell(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry())
        pipe.add_cell("wp_001", self._cell())
        self.assertTrue(pipe.load_cell("wp_001", "cell_001"))
        cell = pipe._cells["wp_001"]["cell_001"]
        self.assertTrue(cell.is_loaded)

    def test_unload_cell(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry())
        pipe.add_cell("wp_001", self._cell())
        pipe.load_cell("wp_001", "cell_001")
        self.assertTrue(pipe.unload_cell("wp_001", "cell_001"))
        cell = pipe._cells["wp_001"]["cell_001"]
        self.assertFalse(cell.is_loaded)

    def test_get_loaded_cells(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry())
        pipe.add_cell("wp_001", self._cell("cell_001"))
        pipe.add_cell("wp_001", StreamingCellDef(cell_id="cell_002", grid_id="grid_001"))
        pipe.load_cell("wp_001", "cell_001")
        loaded = pipe.get_loaded_cells("wp_001")
        self.assertEqual(len(loaded), 1)

    def test_validate(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.validate(self._entry()))

    def test_world_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.world_count, 0)
        pipe.add_world(self._entry())
        self.assertEqual(pipe.world_count, 1)

    def test_is_empty_true(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.add_world(self._entry())
        pipe.clear()
        self.assertTrue(pipe.is_empty)


# ---------------------------------------------------------------------------
# DataLayerSpec
# ---------------------------------------------------------------------------

class TestDataLayerSpec(unittest.TestCase):
    def test_layer_id(self):
        s = DataLayerSpec(layer_id="dl_001", layer_name="Gameplay Layer")
        self.assertEqual(s.layer_id, "dl_001")

    def test_layer_name(self):
        s = DataLayerSpec(layer_id="dl_001", layer_name="Gameplay Layer")
        self.assertEqual(s.layer_name, "Gameplay Layer")

    def test_default_layer_type(self):
        s = DataLayerSpec(layer_id="dl_001", layer_name="Gameplay Layer")
        self.assertEqual(s.layer_type, "Runtime")

    def test_default_runtime_init(self):
        s = DataLayerSpec(layer_id="dl_001", layer_name="Gameplay Layer")
        self.assertEqual(s.runtime_init, "Deactivated")

    def test_is_runtime_true(self):
        s = DataLayerSpec(layer_id="dl_001", layer_name="Gameplay Layer", layer_type="Runtime")
        self.assertTrue(s.is_runtime)

    def test_is_editor_only_false(self):
        s = DataLayerSpec(layer_id="dl_001", layer_name="Gameplay Layer", layer_type="Runtime")
        self.assertFalse(s.is_editor_only)

    def test_has_parent_false(self):
        s = DataLayerSpec(layer_id="dl_001", layer_name="Gameplay Layer")
        self.assertFalse(s.has_parent)


# ---------------------------------------------------------------------------
# DataLayerActorAssignment
# ---------------------------------------------------------------------------

class TestDataLayerActorAssignment(unittest.TestCase):
    def test_assignment_id(self):
        a = DataLayerActorAssignment(assignment_id="asgn_001", actor_id="actor_001", layer_id="dl_001")
        self.assertEqual(a.assignment_id, "asgn_001")

    def test_actor_id(self):
        a = DataLayerActorAssignment(assignment_id="asgn_001", actor_id="actor_001", layer_id="dl_001")
        self.assertEqual(a.actor_id, "actor_001")

    def test_layer_id(self):
        a = DataLayerActorAssignment(assignment_id="asgn_001", actor_id="actor_001", layer_id="dl_001")
        self.assertEqual(a.layer_id, "dl_001")

    def test_is_inherited_false(self):
        a = DataLayerActorAssignment(assignment_id="asgn_001", actor_id="actor_001", layer_id="dl_001")
        self.assertFalse(a.is_inherited)


# ---------------------------------------------------------------------------
# DataLayerState dataclass
# ---------------------------------------------------------------------------

class TestDataLayerStateDataclass(unittest.TestCase):
    def test_state_id(self):
        s = DataLayerState(state_id="st_001", layer_id="dl_001")
        self.assertEqual(s.state_id, "st_001")

    def test_layer_id_field(self):
        s = DataLayerState(state_id="st_001", layer_id="dl_001")
        self.assertEqual(s.layer_id, "dl_001")

    def test_default_current_state(self):
        s = DataLayerState(state_id="st_001", layer_id="dl_001")
        self.assertEqual(s.current_state, "Unloaded")

    def test_is_active_false(self):
        s = DataLayerState(state_id="st_001", layer_id="dl_001")
        self.assertFalse(s.is_active)

    def test_is_loaded_false(self):
        s = DataLayerState(state_id="st_001", layer_id="dl_001")
        self.assertFalse(s.is_loaded)

    def test_has_pending_false(self):
        s = DataLayerState(state_id="st_001", layer_id="dl_001")
        self.assertFalse(s.has_pending)


# ---------------------------------------------------------------------------
# DataLayerPipeline
# ---------------------------------------------------------------------------

class TestDataLayerPipeline(unittest.TestCase):
    def _pipeline(self):
        return DataLayerPipeline()

    def _spec(self, lid="dl_001"):
        return DataLayerSpec(layer_id=lid, layer_name="Gameplay Layer")

    def test_add_layer(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec())
        self.assertEqual(pipe.layer_count, 1)

    def test_remove_layer(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec())
        self.assertTrue(pipe.remove_layer("dl_001"))
        self.assertEqual(pipe.layer_count, 0)

    def test_get_layer(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec())
        self.assertIsNotNone(pipe.get_layer("dl_001"))

    def test_get_all_layers(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec("dl_001"))
        pipe.add_layer(self._spec("dl_002"))
        self.assertEqual(len(pipe.get_all_layers()), 2)

    def test_assign_actor(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec())
        asgn = DataLayerActorAssignment(assignment_id="asgn_001", actor_id="actor_001", layer_id="dl_001")
        self.assertTrue(pipe.assign_actor(asgn))

    def test_unassign_actor(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec())
        asgn = DataLayerActorAssignment(assignment_id="asgn_001", actor_id="actor_001", layer_id="dl_001")
        pipe.assign_actor(asgn)
        self.assertTrue(pipe.unassign_actor("asgn_001"))

    def test_set_layer_state(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec())
        state = pipe.set_layer_state("dl_001", "Activated")
        self.assertIsInstance(state, DataLayerState)
        self.assertEqual(state.current_state, "Activated")

    def test_get_state(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec())
        pipe.set_layer_state("dl_001", "Loaded")
        state = pipe.get_state("dl_001")
        self.assertIsNotNone(state)

    def test_get_layers_by_type(self):
        pipe = self._pipeline()
        pipe.add_layer(DataLayerSpec(layer_id="dl_001", layer_name="Runtime Layer", layer_type="Runtime"))
        pipe.add_layer(DataLayerSpec(layer_id="dl_002", layer_name="Editor Layer", layer_type="Editor"))
        runtime = pipe.get_layers_by_type("Runtime")
        self.assertEqual(len(runtime), 1)

    def test_get_actors_by_layer(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec())
        asgn = DataLayerActorAssignment(assignment_id="asgn_001", actor_id="actor_001", layer_id="dl_001")
        pipe.assign_actor(asgn)
        actors = pipe.get_actors_by_layer("dl_001")
        self.assertIn("actor_001", actors)

    def test_get_child_layers(self):
        pipe = self._pipeline()
        pipe.add_layer(DataLayerSpec(layer_id="parent_001", layer_name="Parent Layer"))
        pipe.add_layer(DataLayerSpec(layer_id="child_001", layer_name="Child Layer", parent_id="parent_001"))
        children = pipe.get_child_layers("parent_001")
        self.assertEqual(len(children), 1)

    def test_validate(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.validate(self._spec()))

    def test_layer_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.layer_count, 0)
        pipe.add_layer(self._spec())
        self.assertEqual(pipe.layer_count, 1)

    def test_is_empty_true(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.add_layer(self._spec())
        pipe.clear()
        self.assertTrue(pipe.is_empty)


if __name__ == "__main__":
    unittest.main()
