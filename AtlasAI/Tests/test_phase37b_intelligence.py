"""Phase 37B — Tests for ChaosDestructionPipeline and HairGroomPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    ChaosDestructionPipeline,
    GeometryCollectionEntry,
    GeometryFragmentDef,
    DestructionEventDef,
    HairGroomPipeline,
    GroomAssetEntry,
    GroomStrandDef,
    GroomLODEntry,
)


# ---------------------------------------------------------------------------
# GeometryFragmentDef
# ---------------------------------------------------------------------------

class TestGeometryFragmentDef(unittest.TestCase):
    def test_fragment_id(self):
        f = GeometryFragmentDef(fragment_id="frag_001", collection_id="col_001")
        self.assertEqual(f.fragment_id, "frag_001")

    def test_default_volume(self):
        f = GeometryFragmentDef(fragment_id="frag_001", collection_id="col_001")
        self.assertEqual(f.volume, 0.0)

    def test_has_mass_false(self):
        f = GeometryFragmentDef(fragment_id="frag_001", collection_id="col_001")
        self.assertFalse(f.has_mass)

    def test_has_mass_true(self):
        f = GeometryFragmentDef(fragment_id="frag_001", collection_id="col_001", mass=10.0)
        self.assertTrue(f.has_mass)

    def test_is_large_false(self):
        f = GeometryFragmentDef(fragment_id="frag_001", collection_id="col_001", volume=500.0)
        self.assertFalse(f.is_large)

    def test_is_large_true(self):
        f = GeometryFragmentDef(fragment_id="frag_001", collection_id="col_001", volume=2000.0)
        self.assertTrue(f.is_large)


# ---------------------------------------------------------------------------
# DestructionEventDef
# ---------------------------------------------------------------------------

class TestDestructionEventDef(unittest.TestCase):
    def test_event_id(self):
        e = DestructionEventDef(event_id="evt_001", collection_id="col_001")
        self.assertEqual(e.event_id, "evt_001")

    def test_default_damage_amount(self):
        e = DestructionEventDef(event_id="evt_001", collection_id="col_001")
        self.assertEqual(e.damage_amount, 0.0)

    def test_is_lethal_false(self):
        e = DestructionEventDef(event_id="evt_001", collection_id="col_001", damage_amount=50.0)
        self.assertFalse(e.is_lethal)

    def test_is_lethal_true(self):
        e = DestructionEventDef(event_id="evt_001", collection_id="col_001", damage_amount=200.0)
        self.assertTrue(e.is_lethal)

    def test_has_impact_false(self):
        e = DestructionEventDef(event_id="evt_001", collection_id="col_001")
        self.assertFalse(e.has_impact)

    def test_has_impact_true(self):
        e = DestructionEventDef(event_id="evt_001", collection_id="col_001", impact_velocity=5.0)
        self.assertTrue(e.has_impact)


# ---------------------------------------------------------------------------
# GeometryCollectionEntry
# ---------------------------------------------------------------------------

class TestGeometryCollectionEntry(unittest.TestCase):
    def test_collection_id(self):
        c = GeometryCollectionEntry(collection_id="col_001", collection_name="Rock Pillar")
        self.assertEqual(c.collection_id, "col_001")

    def test_is_empty_true(self):
        c = GeometryCollectionEntry(collection_id="col_001", collection_name="Rock Pillar")
        self.assertTrue(c.is_empty)

    def test_is_empty_false(self):
        c = GeometryCollectionEntry(collection_id="col_001", collection_name="Rock Pillar",
                                    fragments=["frag_001"])
        self.assertFalse(c.is_empty)

    def test_fragment_count(self):
        c = GeometryCollectionEntry(collection_id="col_001", collection_name="Rock Pillar",
                                    fragments=["frag_001", "frag_002"])
        self.assertEqual(c.fragment_count, 2)

    def test_has_events_false(self):
        c = GeometryCollectionEntry(collection_id="col_001", collection_name="Rock Pillar")
        self.assertFalse(c.has_events)

    def test_has_events_true(self):
        c = GeometryCollectionEntry(collection_id="col_001", collection_name="Rock Pillar",
                                    events=["evt_001"])
        self.assertTrue(c.has_events)


# ---------------------------------------------------------------------------
# ChaosDestructionPipeline
# ---------------------------------------------------------------------------

class TestChaosDestructionPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ChaosDestructionPipeline()
        self.col = GeometryCollectionEntry(collection_id="col_001", collection_name="Rock Pillar")

    def test_add_collection(self):
        self.pipeline.add_collection(self.col)
        self.assertIsNotNone(self.pipeline.get_collection("col_001"))

    def test_remove_collection(self):
        self.pipeline.add_collection(self.col)
        result = self.pipeline.remove_collection("col_001")
        self.assertTrue(result)
        self.assertIsNone(self.pipeline.get_collection("col_001"))

    def test_get_all_collections(self):
        self.pipeline.add_collection(self.col)
        all_cols = self.pipeline.get_all_collections()
        self.assertEqual(len(all_cols), 1)

    def test_add_fragment(self):
        self.pipeline.add_collection(self.col)
        frag = GeometryFragmentDef(fragment_id="frag_001", collection_id="col_001")
        result = self.pipeline.add_fragment("col_001", frag)
        self.assertTrue(result)

    def test_remove_fragment(self):
        self.pipeline.add_collection(self.col)
        frag = GeometryFragmentDef(fragment_id="frag_001", collection_id="col_001")
        self.pipeline.add_fragment("col_001", frag)
        result = self.pipeline.remove_fragment("col_001", "frag_001")
        self.assertTrue(result)

    def test_get_fragments_for_collection(self):
        self.pipeline.add_collection(self.col)
        frag = GeometryFragmentDef(fragment_id="frag_001", collection_id="col_001")
        self.pipeline.add_fragment("col_001", frag)
        frags = self.pipeline.get_fragments_for_collection("col_001")
        self.assertEqual(len(frags), 1)

    def test_add_event(self):
        self.pipeline.add_collection(self.col)
        evt = DestructionEventDef(event_id="evt_001", collection_id="col_001")
        result = self.pipeline.add_event("col_001", evt)
        self.assertTrue(result)

    def test_remove_event(self):
        self.pipeline.add_collection(self.col)
        evt = DestructionEventDef(event_id="evt_001", collection_id="col_001")
        self.pipeline.add_event("col_001", evt)
        result = self.pipeline.remove_event("col_001", "evt_001")
        self.assertTrue(result)

    def test_get_events_for_collection(self):
        self.pipeline.add_collection(self.col)
        evt = DestructionEventDef(event_id="evt_001", collection_id="col_001")
        self.pipeline.add_event("col_001", evt)
        events = self.pipeline.get_events_for_collection("col_001")
        self.assertEqual(len(events), 1)

    def test_get_lethal_events(self):
        self.pipeline.add_collection(self.col)
        lethal = DestructionEventDef(event_id="evt_001", collection_id="col_001", damage_amount=500.0)
        normal = DestructionEventDef(event_id="evt_002", collection_id="col_001", damage_amount=10.0)
        self.pipeline.add_event("col_001", lethal)
        self.pipeline.add_event("col_001", normal)
        lethal_events = self.pipeline.get_lethal_events()
        self.assertEqual(len(lethal_events), 1)
        self.assertEqual(lethal_events[0].event_id, "evt_001")

    def test_set_enabled(self):
        self.pipeline.add_collection(self.col)
        result = self.pipeline.set_enabled("col_001", False)
        self.assertTrue(result)
        self.assertFalse(self.pipeline.get_collection("col_001").enabled)

    def test_get_enabled_collections(self):
        self.pipeline.add_collection(self.col)
        col2 = GeometryCollectionEntry(collection_id="col_002", collection_name="Wall", enabled=False)
        self.pipeline.add_collection(col2)
        enabled = self.pipeline.get_enabled_collections()
        self.assertEqual(len(enabled), 1)

    def test_get_disabled_collections(self):
        self.pipeline.add_collection(self.col)
        col2 = GeometryCollectionEntry(collection_id="col_002", collection_name="Wall", enabled=False)
        self.pipeline.add_collection(col2)
        disabled = self.pipeline.get_disabled_collections()
        self.assertEqual(len(disabled), 1)

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.col))

    def test_collection_count(self):
        self.pipeline.add_collection(self.col)
        self.assertEqual(self.pipeline.collection_count, 1)

    def test_is_empty(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_clear(self):
        self.pipeline.add_collection(self.col)
        self.pipeline.clear()
        self.assertTrue(self.pipeline.is_empty)


# ---------------------------------------------------------------------------
# GroomStrandDef
# ---------------------------------------------------------------------------

class TestGroomStrandDef(unittest.TestCase):
    def test_strand_id(self):
        s = GroomStrandDef(strand_id="strand_001", groom_id="groom_001")
        self.assertEqual(s.strand_id, "strand_001")

    def test_default_width(self):
        s = GroomStrandDef(strand_id="strand_001", groom_id="groom_001")
        self.assertEqual(s.width, 0.5)

    def test_is_guide_true(self):
        s = GroomStrandDef(strand_id="strand_001", groom_id="groom_001", strand_type="Guide")
        self.assertTrue(s.is_guide)

    def test_is_guide_false(self):
        s = GroomStrandDef(strand_id="strand_001", groom_id="groom_001", strand_type="Render")
        self.assertFalse(s.is_guide)

    def test_is_long_false(self):
        s = GroomStrandDef(strand_id="strand_001", groom_id="groom_001", length=10.0)
        self.assertFalse(s.is_long)

    def test_is_long_true(self):
        s = GroomStrandDef(strand_id="strand_001", groom_id="groom_001", length=30.0)
        self.assertTrue(s.is_long)


# ---------------------------------------------------------------------------
# GroomLODEntry
# ---------------------------------------------------------------------------

class TestGroomLODEntry(unittest.TestCase):
    def test_lod_id(self):
        lod = GroomLODEntry(lod_id="lod_001", groom_id="groom_001")
        self.assertEqual(lod.lod_id, "lod_001")

    def test_default_lod_level(self):
        lod = GroomLODEntry(lod_id="lod_001", groom_id="groom_001")
        self.assertEqual(lod.lod_level, 0)

    def test_is_highest_lod_true(self):
        lod = GroomLODEntry(lod_id="lod_001", groom_id="groom_001", lod_level=0)
        self.assertTrue(lod.is_highest_lod)

    def test_is_highest_lod_false(self):
        lod = GroomLODEntry(lod_id="lod_001", groom_id="groom_001", lod_level=2)
        self.assertFalse(lod.is_highest_lod)

    def test_is_culled_false(self):
        lod = GroomLODEntry(lod_id="lod_001", groom_id="groom_001", strand_ratio=1.0)
        self.assertFalse(lod.is_culled)

    def test_is_culled_true(self):
        lod = GroomLODEntry(lod_id="lod_001", groom_id="groom_001", strand_ratio=0.0)
        self.assertTrue(lod.is_culled)


# ---------------------------------------------------------------------------
# GroomAssetEntry
# ---------------------------------------------------------------------------

class TestGroomAssetEntry(unittest.TestCase):
    def test_groom_id(self):
        g = GroomAssetEntry(groom_id="groom_001", groom_name="HeroHair")
        self.assertEqual(g.groom_id, "groom_001")

    def test_is_empty_true(self):
        g = GroomAssetEntry(groom_id="groom_001", groom_name="HeroHair")
        self.assertTrue(g.is_empty)

    def test_is_empty_false(self):
        g = GroomAssetEntry(groom_id="groom_001", groom_name="HeroHair", strands=["s1"])
        self.assertFalse(g.is_empty)

    def test_has_lods_false(self):
        g = GroomAssetEntry(groom_id="groom_001", groom_name="HeroHair")
        self.assertFalse(g.has_lods)

    def test_has_lods_true(self):
        g = GroomAssetEntry(groom_id="groom_001", groom_name="HeroHair", lods=["lod_001"])
        self.assertTrue(g.has_lods)

    def test_is_simulated_false(self):
        g = GroomAssetEntry(groom_id="groom_001", groom_name="HeroHair", sim_mode="Disabled")
        self.assertFalse(g.is_simulated)

    def test_is_simulated_true(self):
        g = GroomAssetEntry(groom_id="groom_001", groom_name="HeroHair", sim_mode="GPU")
        self.assertTrue(g.is_simulated)


# ---------------------------------------------------------------------------
# HairGroomPipeline
# ---------------------------------------------------------------------------

class TestHairGroomPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = HairGroomPipeline()
        self.groom = GroomAssetEntry(groom_id="groom_001", groom_name="HeroHair")

    def test_add_groom(self):
        self.pipeline.add_groom(self.groom)
        self.assertIsNotNone(self.pipeline.get_groom("groom_001"))

    def test_remove_groom(self):
        self.pipeline.add_groom(self.groom)
        result = self.pipeline.remove_groom("groom_001")
        self.assertTrue(result)
        self.assertIsNone(self.pipeline.get_groom("groom_001"))

    def test_get_all_grooms(self):
        self.pipeline.add_groom(self.groom)
        all_grooms = self.pipeline.get_all_grooms()
        self.assertEqual(len(all_grooms), 1)

    def test_add_strand(self):
        self.pipeline.add_groom(self.groom)
        strand = GroomStrandDef(strand_id="strand_001", groom_id="groom_001")
        result = self.pipeline.add_strand("groom_001", strand)
        self.assertTrue(result)

    def test_remove_strand(self):
        self.pipeline.add_groom(self.groom)
        strand = GroomStrandDef(strand_id="strand_001", groom_id="groom_001")
        self.pipeline.add_strand("groom_001", strand)
        result = self.pipeline.remove_strand("groom_001", "strand_001")
        self.assertTrue(result)

    def test_get_strands_for_groom(self):
        self.pipeline.add_groom(self.groom)
        strand = GroomStrandDef(strand_id="strand_001", groom_id="groom_001")
        self.pipeline.add_strand("groom_001", strand)
        strands = self.pipeline.get_strands_for_groom("groom_001")
        self.assertEqual(len(strands), 1)

    def test_add_lod(self):
        self.pipeline.add_groom(self.groom)
        lod = GroomLODEntry(lod_id="lod_001", groom_id="groom_001")
        result = self.pipeline.add_lod("groom_001", lod)
        self.assertTrue(result)

    def test_remove_lod(self):
        self.pipeline.add_groom(self.groom)
        lod = GroomLODEntry(lod_id="lod_001", groom_id="groom_001")
        self.pipeline.add_lod("groom_001", lod)
        result = self.pipeline.remove_lod("groom_001", "lod_001")
        self.assertTrue(result)

    def test_get_lods_for_groom(self):
        self.pipeline.add_groom(self.groom)
        lod = GroomLODEntry(lod_id="lod_001", groom_id="groom_001")
        self.pipeline.add_lod("groom_001", lod)
        lods = self.pipeline.get_lods_for_groom("groom_001")
        self.assertEqual(len(lods), 1)

    def test_get_simulated_grooms(self):
        self.pipeline.add_groom(self.groom)
        sim_groom = GroomAssetEntry(groom_id="groom_002", groom_name="NPC Hair", sim_mode="GPU")
        self.pipeline.add_groom(sim_groom)
        simulated = self.pipeline.get_simulated_grooms()
        self.assertEqual(len(simulated), 1)
        self.assertEqual(simulated[0].groom_id, "groom_002")

    def test_get_guide_strands(self):
        self.pipeline.add_groom(self.groom)
        guide = GroomStrandDef(strand_id="s1", groom_id="groom_001", strand_type="Guide")
        render = GroomStrandDef(strand_id="s2", groom_id="groom_001", strand_type="Render")
        self.pipeline.add_strand("groom_001", guide)
        self.pipeline.add_strand("groom_001", render)
        guides = self.pipeline.get_guide_strands("groom_001")
        self.assertEqual(len(guides), 1)

    def test_set_enabled(self):
        self.pipeline.add_groom(self.groom)
        result = self.pipeline.set_enabled("groom_001", False)
        self.assertTrue(result)
        self.assertFalse(self.pipeline.get_groom("groom_001").enabled)

    def test_get_enabled_grooms(self):
        self.pipeline.add_groom(self.groom)
        g2 = GroomAssetEntry(groom_id="groom_002", groom_name="NPC Hair", enabled=False)
        self.pipeline.add_groom(g2)
        enabled = self.pipeline.get_enabled_grooms()
        self.assertEqual(len(enabled), 1)

    def test_get_disabled_grooms(self):
        self.pipeline.add_groom(self.groom)
        g2 = GroomAssetEntry(groom_id="groom_002", groom_name="NPC Hair", enabled=False)
        self.pipeline.add_groom(g2)
        disabled = self.pipeline.get_disabled_grooms()
        self.assertEqual(len(disabled), 1)

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.groom))

    def test_groom_count(self):
        self.pipeline.add_groom(self.groom)
        self.assertEqual(self.pipeline.groom_count, 1)

    def test_is_empty(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_clear(self):
        self.pipeline.add_groom(self.groom)
        self.pipeline.clear()
        self.assertTrue(self.pipeline.is_empty)


if __name__ == "__main__":
    unittest.main()
