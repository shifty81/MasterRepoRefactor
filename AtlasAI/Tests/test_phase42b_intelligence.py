"""Phase 42B — Tests for DistanceFieldPipeline and AnimationCompressionPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    DistanceFieldPipeline,
    DistanceFieldEntry,
    ShadowConfigEntry,
    FieldBlendOpEntry,
    AnimationCompressionPipeline,
    CompressionSchemeEntry,
    TrackCompressionEntry,
    CompressionPreviewEntry,
)


# ---------------------------------------------------------------------------
# DistanceFieldEntry
# ---------------------------------------------------------------------------

class TestDistanceFieldEntry(unittest.TestCase):
    def test_field_id(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow")
        self.assertEqual(e.field_id, "df_001")

    def test_field_name(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow")
        self.assertEqual(e.field_name, "Player Shadow")

    def test_default_shape_sphere(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow")
        self.assertEqual(e.shape, "Sphere")

    def test_is_sphere_true(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", shape="Sphere")
        self.assertTrue(e.is_sphere)

    def test_is_box_false(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", shape="Sphere")
        self.assertFalse(e.is_box)

    def test_is_box_true(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Box Field", shape="Box")
        self.assertTrue(e.is_box)

    def test_is_enabled_true(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", enabled=True)
        self.assertTrue(e.is_enabled)

    def test_is_enabled_false(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", enabled=False)
        self.assertFalse(e.is_enabled)

    def test_is_high_res_false(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", resolution="Medium")
        self.assertFalse(e.is_high_res)

    def test_is_high_res_true(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", resolution="High")
        self.assertTrue(e.is_high_res)

    def test_has_blend_false(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", blend_radius=0.0)
        self.assertFalse(e.has_blend)

    def test_has_blend_true(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", blend_radius=0.5)
        self.assertTrue(e.has_blend)

    def test_is_at_origin_true(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow")
        self.assertTrue(e.is_at_origin)

    def test_uniform_scale_true(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", scale_x=2.0, scale_y=2.0, scale_z=2.0)
        self.assertTrue(e.uniform_scale)

    def test_uniform_scale_false(self):
        e = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow", scale_x=1.0, scale_y=2.0, scale_z=1.0)
        self.assertFalse(e.uniform_scale)


# ---------------------------------------------------------------------------
# ShadowConfigEntry
# ---------------------------------------------------------------------------

class TestShadowConfigEntry(unittest.TestCase):
    def test_shadow_config_id(self):
        s = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001")
        self.assertEqual(s.shadow_config_id, "sc_001")

    def test_default_type_soft(self):
        s = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001")
        self.assertEqual(s.shadow_type, "Soft")

    def test_is_soft_true(self):
        s = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001", shadow_type="Soft")
        self.assertTrue(s.is_soft)

    def test_is_hard_false(self):
        s = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001", shadow_type="Soft")
        self.assertFalse(s.is_hard)

    def test_is_ray_traced_true(self):
        s = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001", shadow_type="RayTraced")
        self.assertTrue(s.is_ray_traced)

    def test_casts_shadow_true(self):
        s = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001", cast_shadow=True)
        self.assertTrue(s.casts_shadow)

    def test_is_wide_penumbra_false(self):
        s = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001", penumbra_angle=3.0)
        self.assertFalse(s.is_wide_penumbra)

    def test_is_wide_penumbra_true(self):
        s = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001", penumbra_angle=15.0)
        self.assertTrue(s.is_wide_penumbra)


# ---------------------------------------------------------------------------
# FieldBlendOpEntry
# ---------------------------------------------------------------------------

class TestFieldBlendOpEntry(unittest.TestCase):
    def test_blend_op_id(self):
        b = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002")
        self.assertEqual(b.blend_op_id, "bo_001")

    def test_is_union_true(self):
        b = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002", blend_mode="Union")
        self.assertTrue(b.is_union)

    def test_is_intersection_false(self):
        b = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002", blend_mode="Union")
        self.assertFalse(b.is_intersection)

    def test_is_subtraction_true(self):
        b = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002", blend_mode="Subtraction")
        self.assertTrue(b.is_subtraction)

    def test_is_smooth_true(self):
        b = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002", blend_mode="SmoothUnion")
        self.assertTrue(b.is_smooth)

    def test_is_enabled_true(self):
        b = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002", enabled=True)
        self.assertTrue(b.is_enabled)


# ---------------------------------------------------------------------------
# DistanceFieldPipeline
# ---------------------------------------------------------------------------

class TestDistanceFieldPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = DistanceFieldPipeline()
        self.field = DistanceFieldEntry(field_id="df_001", field_name="Player Shadow")

    def test_add_field(self):
        self.assertTrue(self.pipeline.add_field(self.field))

    def test_get_field(self):
        self.pipeline.add_field(self.field)
        f = self.pipeline.get_field("df_001")
        self.assertIsNotNone(f)
        self.assertEqual(f.field_name, "Player Shadow")

    def test_field_count(self):
        self.pipeline.add_field(self.field)
        self.assertEqual(self.pipeline.field_count, 1)

    def test_is_empty_true(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_is_empty_false(self):
        self.pipeline.add_field(self.field)
        self.assertFalse(self.pipeline.is_empty)

    def test_remove_field(self):
        self.pipeline.add_field(self.field)
        self.assertTrue(self.pipeline.remove_field("df_001"))
        self.assertIsNone(self.pipeline.get_field("df_001"))

    def test_get_all_fields(self):
        self.pipeline.add_field(self.field)
        self.assertEqual(len(self.pipeline.get_all_fields()), 1)

    def test_get_fields_by_shape(self):
        self.pipeline.add_field(self.field)
        result = self.pipeline.get_fields_by_shape("Sphere")
        self.assertEqual(len(result), 1)

    def test_get_enabled_fields(self):
        self.pipeline.add_field(self.field)
        disabled = DistanceFieldEntry(field_id="df_002", field_name="Disabled", enabled=False)
        self.pipeline.add_field(disabled)
        result = self.pipeline.get_enabled_fields()
        self.assertEqual(len(result), 1)

    def test_add_shadow_config(self):
        self.pipeline.add_field(self.field)
        sc = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001")
        self.assertTrue(self.pipeline.add_shadow_config("df_001", sc))

    def test_get_shadow_configs_for_field(self):
        self.pipeline.add_field(self.field)
        sc = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001")
        self.pipeline.add_shadow_config("df_001", sc)
        result = self.pipeline.get_shadow_configs_for_field("df_001")
        self.assertEqual(len(result), 1)

    def test_remove_shadow_config(self):
        self.pipeline.add_field(self.field)
        sc = ShadowConfigEntry(shadow_config_id="sc_001", field_id="df_001")
        self.pipeline.add_shadow_config("df_001", sc)
        self.assertTrue(self.pipeline.remove_shadow_config("df_001", "sc_001"))

    def test_add_blend_op(self):
        self.pipeline.add_field(self.field)
        f2 = DistanceFieldEntry(field_id="df_002", field_name="Box Shadow", shape="Box")
        self.pipeline.add_field(f2)
        bo = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002")
        self.assertTrue(self.pipeline.add_blend_op(bo))

    def test_get_blend_ops_by_mode(self):
        bo = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002", blend_mode="Union")
        self.pipeline.add_blend_op(bo)
        result = self.pipeline.get_blend_ops_by_mode("Union")
        self.assertEqual(len(result), 1)

    def test_remove_blend_op(self):
        bo = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002")
        self.pipeline.add_blend_op(bo)
        self.assertTrue(self.pipeline.remove_blend_op("bo_001"))

    def test_add_invalid_field(self):
        bad = DistanceFieldEntry(field_id="", field_name="Bad")
        self.assertFalse(self.pipeline.add_field(bad))

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.field))

    def test_clear(self):
        self.pipeline.add_field(self.field)
        self.pipeline.clear()
        self.assertEqual(self.pipeline.field_count, 0)

    def test_get_blend_op(self):
        bo = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002")
        self.pipeline.add_blend_op(bo)
        result = self.pipeline.get_blend_op("bo_001")
        self.assertIsNotNone(result)

    def test_get_all_blend_ops(self):
        bo = FieldBlendOpEntry(blend_op_id="bo_001", field_a_id="df_001", field_b_id="df_002")
        self.pipeline.add_blend_op(bo)
        self.assertEqual(len(self.pipeline.get_all_blend_ops()), 1)


# ---------------------------------------------------------------------------
# CompressionSchemeEntry
# ---------------------------------------------------------------------------

class TestCompressionSchemeEntry(unittest.TestCase):
    def test_scheme_id(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL")
        self.assertEqual(s.scheme_id, "cs_001")

    def test_scheme_name(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL")
        self.assertEqual(s.scheme_name, "Default ACL")

    def test_default_codec_acl(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL")
        self.assertEqual(s.codec, "ACL")

    def test_is_acl_true(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL", codec="ACL")
        self.assertTrue(s.is_acl)

    def test_is_lossless_false(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL", quality="Medium")
        self.assertFalse(s.is_lossless)

    def test_is_lossless_true(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Lossless", quality="Lossless")
        self.assertTrue(s.is_lossless)

    def test_is_high_quality_false(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL", quality="Medium")
        self.assertFalse(s.is_high_quality)

    def test_is_high_quality_true(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="HQ", quality="High")
        self.assertTrue(s.is_high_quality)

    def test_uses_key_reduction_true(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL", key_reduction="Linear")
        self.assertTrue(s.uses_key_reduction)

    def test_uses_key_reduction_false(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL", key_reduction="None")
        self.assertFalse(s.uses_key_reduction)

    def test_has_tight_tolerance_false(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL", error_threshold=0.01)
        self.assertFalse(s.has_tight_tolerance)

    def test_has_tight_tolerance_true(self):
        s = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Tight", error_threshold=0.0005)
        self.assertTrue(s.has_tight_tolerance)


# ---------------------------------------------------------------------------
# TrackCompressionEntry
# ---------------------------------------------------------------------------

class TestTrackCompressionEntry(unittest.TestCase):
    def test_track_comp_id(self):
        t = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001")
        self.assertEqual(t.track_comp_id, "tc_001")

    def test_is_rotation_true(self):
        t = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001", track_type="Rotation")
        self.assertTrue(t.is_rotation)

    def test_is_translation_false(self):
        t = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001", track_type="Rotation")
        self.assertFalse(t.is_translation)

    def test_is_translation_true(self):
        t = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001", track_type="Translation")
        self.assertTrue(t.is_translation)

    def test_is_scale_true(self):
        t = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001", track_type="Scale")
        self.assertTrue(t.is_scale)

    def test_has_bone_false(self):
        t = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001")
        self.assertFalse(t.has_bone)

    def test_has_bone_true(self):
        t = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001", bone_name="Spine")
        self.assertTrue(t.has_bone)

    def test_is_override_active_false(self):
        t = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001", use_override=False)
        self.assertFalse(t.is_override_active)


# ---------------------------------------------------------------------------
# CompressionPreviewEntry
# ---------------------------------------------------------------------------

class TestCompressionPreviewEntry(unittest.TestCase):
    def test_preview_id(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001")
        self.assertEqual(p.preview_id, "prev_001")

    def test_is_generated_false(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001")
        self.assertFalse(p.is_generated)

    def test_is_generated_true(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001", preview_generated=True)
        self.assertTrue(p.is_generated)

    def test_compression_ratio(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001",
                                     original_size_kb=100.0, compressed_size_kb=40.0)
        self.assertAlmostEqual(p.compression_ratio, 0.4)

    def test_space_saved_kb(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001",
                                     original_size_kb=100.0, compressed_size_kb=60.0)
        self.assertAlmostEqual(p.space_saved_kb, 40.0)

    def test_is_high_error_false(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001", max_error=0.5)
        self.assertFalse(p.is_high_error)

    def test_is_high_error_true(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001", max_error=2.0)
        self.assertTrue(p.is_high_error)

    def test_has_animation_false(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001")
        self.assertFalse(p.has_animation)

    def test_has_animation_true(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001", animation_asset_id="anim_run")
        self.assertTrue(p.has_animation)


# ---------------------------------------------------------------------------
# AnimationCompressionPipeline
# ---------------------------------------------------------------------------

class TestAnimationCompressionPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = AnimationCompressionPipeline()
        self.scheme = CompressionSchemeEntry(scheme_id="cs_001", scheme_name="Default ACL")

    def test_add_scheme(self):
        self.assertTrue(self.pipeline.add_scheme(self.scheme))

    def test_get_scheme(self):
        self.pipeline.add_scheme(self.scheme)
        s = self.pipeline.get_scheme("cs_001")
        self.assertIsNotNone(s)
        self.assertEqual(s.scheme_name, "Default ACL")

    def test_scheme_count(self):
        self.pipeline.add_scheme(self.scheme)
        self.assertEqual(self.pipeline.scheme_count, 1)

    def test_is_empty_true(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_is_empty_false(self):
        self.pipeline.add_scheme(self.scheme)
        self.assertFalse(self.pipeline.is_empty)

    def test_remove_scheme(self):
        self.pipeline.add_scheme(self.scheme)
        self.assertTrue(self.pipeline.remove_scheme("cs_001"))
        self.assertIsNone(self.pipeline.get_scheme("cs_001"))

    def test_get_all_schemes(self):
        self.pipeline.add_scheme(self.scheme)
        self.assertEqual(len(self.pipeline.get_all_schemes()), 1)

    def test_get_schemes_by_codec(self):
        self.pipeline.add_scheme(self.scheme)
        result = self.pipeline.get_schemes_by_codec("ACL")
        self.assertEqual(len(result), 1)

    def test_get_schemes_by_quality(self):
        self.pipeline.add_scheme(self.scheme)
        result = self.pipeline.get_schemes_by_quality("Medium")
        self.assertEqual(len(result), 1)

    def test_add_track_compression(self):
        self.pipeline.add_scheme(self.scheme)
        tc = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001")
        self.assertTrue(self.pipeline.add_track_compression("cs_001", tc))

    def test_get_track_compressions_for_scheme(self):
        self.pipeline.add_scheme(self.scheme)
        tc = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001")
        self.pipeline.add_track_compression("cs_001", tc)
        result = self.pipeline.get_track_compressions_for_scheme("cs_001")
        self.assertEqual(len(result), 1)

    def test_remove_track_compression(self):
        self.pipeline.add_scheme(self.scheme)
        tc = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001")
        self.pipeline.add_track_compression("cs_001", tc)
        self.assertTrue(self.pipeline.remove_track_compression("cs_001", "tc_001"))

    def test_get_track_compressions_by_type(self):
        self.pipeline.add_scheme(self.scheme)
        tc = TrackCompressionEntry(track_comp_id="tc_001", scheme_id="cs_001", track_type="Rotation")
        self.pipeline.add_track_compression("cs_001", tc)
        result = self.pipeline.get_track_compressions_by_type("Rotation")
        self.assertEqual(len(result), 1)

    def test_add_preview(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001")
        self.assertTrue(self.pipeline.add_preview(p))

    def test_generate_preview(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001")
        self.pipeline.add_preview(p)
        self.assertTrue(self.pipeline.generate_preview("prev_001"))
        result = self.pipeline.get_preview("prev_001")
        self.assertTrue(result.preview_generated)

    def test_get_previews_for_scheme(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001")
        self.pipeline.add_preview(p)
        result = self.pipeline.get_previews_for_scheme("cs_001")
        self.assertEqual(len(result), 1)

    def test_get_generated_previews(self):
        p = CompressionPreviewEntry(preview_id="prev_001", scheme_id="cs_001", preview_generated=True)
        self.pipeline.add_preview(p)
        result = self.pipeline.get_generated_previews()
        self.assertEqual(len(result), 1)

    def test_add_invalid_scheme(self):
        bad = CompressionSchemeEntry(scheme_id="", scheme_name="Bad")
        self.assertFalse(self.pipeline.add_scheme(bad))

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.scheme))

    def test_clear(self):
        self.pipeline.add_scheme(self.scheme)
        self.pipeline.clear()
        self.assertEqual(self.pipeline.scheme_count, 0)


if __name__ == "__main__":
    unittest.main()
