"""Phase 41B — Tests for ProceduralTerrainPipeline and SkeletalMeshPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    ProceduralTerrainPipeline,
    TerrainGenEntry,
    BiomeLayerEntry,
    ErosionSimEntry,
    SkeletalMeshPipeline,
    BoneEntry,
    WeightPaintEntry,
    MeshLODEntry,
)


# ---------------------------------------------------------------------------
# TerrainGenEntry
# ---------------------------------------------------------------------------

class TestTerrainGenEntry(unittest.TestCase):
    def test_gen_id(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands")
        self.assertEqual(e.gen_id, "gen_001")

    def test_gen_name(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands")
        self.assertEqual(e.gen_name, "Highlands")

    def test_default_mode_noise(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands")
        self.assertEqual(e.mode, "Noise")

    def test_is_noise_true(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands", mode="Noise")
        self.assertTrue(e.is_noise)

    def test_is_noise_false(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands", mode="Heightmap")
        self.assertFalse(e.is_noise)

    def test_is_heightmap_true(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands", mode="Heightmap")
        self.assertTrue(e.is_heightmap)

    def test_is_generated_false(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands")
        self.assertFalse(e.is_generated)

    def test_is_generated_true(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands", generated=True)
        self.assertTrue(e.is_generated)

    def test_is_seamless_false(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands", seamless=False)
        self.assertFalse(e.is_seamless)

    def test_is_seamless_true(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands", seamless=True)
        self.assertTrue(e.is_seamless)

    def test_area(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands", width=512.0, height=256.0)
        self.assertAlmostEqual(e.area, 131072.0)

    def test_aspect_ratio(self):
        e = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands", width=1024.0, height=512.0)
        self.assertAlmostEqual(e.aspect_ratio, 2.0)


# ---------------------------------------------------------------------------
# BiomeLayerEntry
# ---------------------------------------------------------------------------

class TestBiomeLayerEntry(unittest.TestCase):
    def test_biome_layer_id(self):
        b = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001")
        self.assertEqual(b.biome_layer_id, "bio_001")

    def test_default_biome_type(self):
        b = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001")
        self.assertEqual(b.biome_type, "Grassland")

    def test_is_enabled_true(self):
        b = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001", enabled=True)
        self.assertTrue(b.is_enabled)

    def test_is_enabled_false(self):
        b = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001", enabled=False)
        self.assertFalse(b.is_enabled)

    def test_is_base_layer_true(self):
        b = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001", layer="Base")
        self.assertTrue(b.is_base_layer)

    def test_elevation_range(self):
        b = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001", min_elevation=100.0, max_elevation=600.0)
        self.assertAlmostEqual(b.elevation_range, 500.0)

    def test_is_grassland_true(self):
        b = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001", biome_type="Grassland")
        self.assertTrue(b.is_grassland)

    def test_is_desert_false(self):
        b = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001", biome_type="Grassland")
        self.assertFalse(b.is_desert)


# ---------------------------------------------------------------------------
# ErosionSimEntry
# ---------------------------------------------------------------------------

class TestErosionSimEntry(unittest.TestCase):
    def test_erosion_id(self):
        e = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001")
        self.assertEqual(e.erosion_id, "ero_001")

    def test_default_type_hydraulic(self):
        e = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001")
        self.assertEqual(e.erosion_type, "Hydraulic")

    def test_is_hydraulic_true(self):
        e = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001", erosion_type="Hydraulic")
        self.assertTrue(e.is_hydraulic)

    def test_is_thermal_false(self):
        e = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001", erosion_type="Hydraulic")
        self.assertFalse(e.is_thermal)

    def test_is_completed_false(self):
        e = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001")
        self.assertFalse(e.is_completed)

    def test_is_intensive_false(self):
        e = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001", iterations=100)
        self.assertFalse(e.is_intensive)

    def test_is_intensive_true(self):
        e = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001", iterations=600)
        self.assertTrue(e.is_intensive)

    def test_is_high_intensity_true(self):
        e = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001", intensity=0.9)
        self.assertTrue(e.is_high_intensity)


# ---------------------------------------------------------------------------
# ProceduralTerrainPipeline
# ---------------------------------------------------------------------------

class TestProceduralTerrainPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ProceduralTerrainPipeline()
        self.terrain = TerrainGenEntry(gen_id="gen_001", gen_name="Highlands")

    def test_add_terrain(self):
        self.assertTrue(self.pipeline.add_terrain(self.terrain))

    def test_get_terrain(self):
        self.pipeline.add_terrain(self.terrain)
        t = self.pipeline.get_terrain("gen_001")
        self.assertIsNotNone(t)
        self.assertEqual(t.gen_name, "Highlands")

    def test_terrain_count(self):
        self.pipeline.add_terrain(self.terrain)
        self.assertEqual(self.pipeline.terrain_count, 1)

    def test_is_empty_true(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_is_empty_false(self):
        self.pipeline.add_terrain(self.terrain)
        self.assertFalse(self.pipeline.is_empty)

    def test_remove_terrain(self):
        self.pipeline.add_terrain(self.terrain)
        self.assertTrue(self.pipeline.remove_terrain("gen_001"))
        self.assertIsNone(self.pipeline.get_terrain("gen_001"))

    def test_get_all_terrains(self):
        self.pipeline.add_terrain(self.terrain)
        self.assertEqual(len(self.pipeline.get_all_terrains()), 1)

    def test_get_terrains_by_mode(self):
        self.pipeline.add_terrain(self.terrain)
        result = self.pipeline.get_terrains_by_mode("Noise")
        self.assertEqual(len(result), 1)

    def test_add_invalid_terrain(self):
        bad = TerrainGenEntry(gen_id="", gen_name="Bad")
        self.assertFalse(self.pipeline.add_terrain(bad))

    def test_add_biome_layer(self):
        self.pipeline.add_terrain(self.terrain)
        layer = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001")
        self.assertTrue(self.pipeline.add_biome_layer("gen_001", layer))

    def test_get_biome_layers_for_terrain(self):
        self.pipeline.add_terrain(self.terrain)
        layer = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001")
        self.pipeline.add_biome_layer("gen_001", layer)
        layers = self.pipeline.get_biome_layers_for_terrain("gen_001")
        self.assertEqual(len(layers), 1)

    def test_remove_biome_layer(self):
        self.pipeline.add_terrain(self.terrain)
        layer = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001")
        self.pipeline.add_biome_layer("gen_001", layer)
        self.assertTrue(self.pipeline.remove_biome_layer("gen_001", "bio_001"))

    def test_add_erosion_sim(self):
        self.pipeline.add_terrain(self.terrain)
        sim = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001")
        self.assertTrue(self.pipeline.add_erosion_sim("gen_001", sim))

    def test_run_erosion(self):
        self.pipeline.add_terrain(self.terrain)
        sim = ErosionSimEntry(erosion_id="ero_001", gen_id="gen_001")
        self.pipeline.add_erosion_sim("gen_001", sim)
        self.assertTrue(self.pipeline.run_erosion("gen_001", "ero_001"))
        sims = self.pipeline.get_erosion_sims_for_terrain("gen_001")
        self.assertTrue(sims[0].completed)

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.terrain))

    def test_clear(self):
        self.pipeline.add_terrain(self.terrain)
        self.pipeline.clear()
        self.assertEqual(self.pipeline.terrain_count, 0)

    def test_get_generated_terrains(self):
        t2 = TerrainGenEntry(gen_id="gen_002", gen_name="Lowlands", generated=True)
        self.pipeline.add_terrain(self.terrain)
        self.pipeline.add_terrain(t2)
        result = self.pipeline.get_generated_terrains()
        self.assertEqual(len(result), 1)

    def test_get_biome_layers_by_type(self):
        self.pipeline.add_terrain(self.terrain)
        layer = BiomeLayerEntry(biome_layer_id="bio_001", gen_id="gen_001", biome_type="Desert")
        self.pipeline.add_biome_layer("gen_001", layer)
        result = self.pipeline.get_biome_layers_by_type("Desert")
        self.assertEqual(len(result), 1)


# ---------------------------------------------------------------------------
# BoneEntry
# ---------------------------------------------------------------------------

class TestBoneEntry(unittest.TestCase):
    def test_bone_id(self):
        b = BoneEntry(bone_id="bone_001", bone_name="Root")
        self.assertEqual(b.bone_id, "bone_001")

    def test_bone_name(self):
        b = BoneEntry(bone_id="bone_001", bone_name="Root")
        self.assertEqual(b.bone_name, "Root")

    def test_has_parent_false(self):
        b = BoneEntry(bone_id="bone_001", bone_name="Root", is_root=True)
        self.assertFalse(b.has_parent)

    def test_has_parent_true(self):
        b = BoneEntry(bone_id="bone_002", bone_name="Spine", parent_bone_id="bone_001")
        self.assertTrue(b.has_parent)

    def test_is_root_bone_true(self):
        b = BoneEntry(bone_id="bone_001", bone_name="Root", is_root=True)
        self.assertTrue(b.is_root_bone)

    def test_is_at_origin_true(self):
        b = BoneEntry(bone_id="bone_001", bone_name="Root")
        self.assertTrue(b.is_at_origin)

    def test_is_at_origin_false(self):
        b = BoneEntry(bone_id="bone_001", bone_name="Spine", pos_x=1.0)
        self.assertFalse(b.is_at_origin)

    def test_has_rotation_false(self):
        b = BoneEntry(bone_id="bone_001", bone_name="Root")
        self.assertFalse(b.has_rotation)

    def test_has_rotation_true(self):
        b = BoneEntry(bone_id="bone_001", bone_name="Root", rot_x=45.0)
        self.assertTrue(b.has_rotation)


# ---------------------------------------------------------------------------
# WeightPaintEntry
# ---------------------------------------------------------------------------

class TestWeightPaintEntry(unittest.TestCase):
    def test_entry_id(self):
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001")
        self.assertEqual(w.entry_id, "wp_001")

    def test_is_additive_true(self):
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001", mode="Additive")
        self.assertTrue(w.is_additive)

    def test_is_subtractive_false(self):
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001", mode="Additive")
        self.assertFalse(w.is_subtractive)

    def test_is_applied_false(self):
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001")
        self.assertFalse(w.is_applied)

    def test_is_symmetric_true(self):
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001", symmetry=True)
        self.assertTrue(w.is_symmetric)

    def test_is_strong_false(self):
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001", brush_strength=0.5)
        self.assertFalse(w.is_strong)

    def test_is_strong_true(self):
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001", brush_strength=0.9)
        self.assertTrue(w.is_strong)


# ---------------------------------------------------------------------------
# MeshLODEntry
# ---------------------------------------------------------------------------

class TestMeshLODEntry(unittest.TestCase):
    def test_lod_id(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001")
        self.assertEqual(l.lod_id, "lod_001")

    def test_is_base_lod_true(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001", lod_level=0)
        self.assertTrue(l.is_base_lod)

    def test_is_base_lod_false(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001", lod_level=1)
        self.assertFalse(l.is_base_lod)

    def test_is_auto_true(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001", strategy="Auto")
        self.assertTrue(l.is_auto)

    def test_is_generated_false(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001")
        self.assertFalse(l.is_generated)

    def test_has_reduction_false(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001", reduction_percent=0.0)
        self.assertFalse(l.has_reduction)

    def test_has_reduction_true(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001", reduction_percent=50.0)
        self.assertTrue(l.has_reduction)

    def test_is_high_lod_true(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001", lod_level=3)
        self.assertTrue(l.is_high_lod)


# ---------------------------------------------------------------------------
# SkeletalMeshPipeline
# ---------------------------------------------------------------------------

class TestSkeletalMeshPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = SkeletalMeshPipeline()
        self.bone = BoneEntry(bone_id="bone_001", bone_name="Root", is_root=True)

    def test_add_bone(self):
        self.assertTrue(self.pipeline.add_bone(self.bone))

    def test_get_bone(self):
        self.pipeline.add_bone(self.bone)
        b = self.pipeline.get_bone("bone_001")
        self.assertIsNotNone(b)
        self.assertEqual(b.bone_name, "Root")

    def test_bone_count(self):
        self.pipeline.add_bone(self.bone)
        self.assertEqual(self.pipeline.bone_count, 1)

    def test_is_empty_true(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_is_empty_false(self):
        self.pipeline.add_bone(self.bone)
        self.assertFalse(self.pipeline.is_empty)

    def test_remove_bone(self):
        self.pipeline.add_bone(self.bone)
        self.assertTrue(self.pipeline.remove_bone("bone_001"))
        self.assertIsNone(self.pipeline.get_bone("bone_001"))

    def test_rename_bone(self):
        self.pipeline.add_bone(self.bone)
        self.assertTrue(self.pipeline.rename_bone("bone_001", "Pelvis"))
        self.assertEqual(self.pipeline.get_bone("bone_001").bone_name, "Pelvis")

    def test_get_root_bones(self):
        self.pipeline.add_bone(self.bone)
        roots = self.pipeline.get_root_bones()
        self.assertEqual(len(roots), 1)

    def test_get_children(self):
        self.pipeline.add_bone(self.bone)
        child = BoneEntry(bone_id="bone_002", bone_name="Spine", parent_bone_id="bone_001")
        self.pipeline.add_bone(child)
        children = self.pipeline.get_children("bone_001")
        self.assertEqual(len(children), 1)

    def test_add_weight_entry(self):
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001")
        self.assertTrue(self.pipeline.add_weight_entry(w))

    def test_apply_weight(self):
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001")
        self.pipeline.add_weight_entry(w)
        self.assertTrue(self.pipeline.apply_weight("wp_001"))
        entry = self.pipeline.get_weight_entry("wp_001")
        self.assertTrue(entry.applied)

    def test_get_weight_entries_by_bone(self):
        self.pipeline.add_bone(self.bone)
        w = WeightPaintEntry(entry_id="wp_001", bone_id="bone_001", mesh_id="mesh_001")
        self.pipeline.add_weight_entry(w)
        result = self.pipeline.get_weight_entries_by_bone("bone_001")
        self.assertEqual(len(result), 1)

    def test_add_lod(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001")
        self.assertTrue(self.pipeline.add_lod(l))

    def test_generate_lod(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001")
        self.pipeline.add_lod(l)
        self.assertTrue(self.pipeline.generate_lod("lod_001"))
        lod = self.pipeline.get_lod("lod_001")
        self.assertTrue(lod.generated)

    def test_get_lods_by_mesh(self):
        l = MeshLODEntry(lod_id="lod_001", mesh_id="mesh_001")
        self.pipeline.add_lod(l)
        result = self.pipeline.get_lods_by_mesh("mesh_001")
        self.assertEqual(len(result), 1)

    def test_set_edit_mode(self):
        self.assertTrue(self.pipeline.set_edit_mode("Weights"))
        self.assertEqual(self.pipeline.edit_mode, "Weights")

    def test_set_invalid_edit_mode(self):
        self.assertFalse(self.pipeline.set_edit_mode("InvalidMode"))

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.bone))

    def test_clear(self):
        self.pipeline.add_bone(self.bone)
        self.pipeline.clear()
        self.assertEqual(self.pipeline.bone_count, 0)

    def test_get_all_bones(self):
        self.pipeline.add_bone(self.bone)
        bones = self.pipeline.get_all_bones()
        self.assertEqual(len(bones), 1)

    def test_add_invalid_bone(self):
        bad = BoneEntry(bone_id="", bone_name="Bad")
        self.assertFalse(self.pipeline.add_bone(bad))


if __name__ == "__main__":
    unittest.main()
