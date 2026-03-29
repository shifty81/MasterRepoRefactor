"""Phase 43B — Tests for SubsurfaceScatterPipeline and VectorFieldPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    SubsurfaceScatterPipeline,
    SSSProfileEntry,
    TransmissionEntry,
    SSSKernelEntry,
    VectorFieldPipeline,
    VectorFieldEntry,
    FlowVisualizationEntry,
    ParticleCouplingEntry,
)


# ---------------------------------------------------------------------------
# SSSProfileEntry
# ---------------------------------------------------------------------------

class TestSSSProfileEntry(unittest.TestCase):
    def test_profile_id(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin")
        self.assertEqual(p.profile_id, "sss_001")

    def test_profile_name(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin")
        self.assertEqual(p.profile_name, "Skin")

    def test_default_model_burley(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin")
        self.assertEqual(p.scatter_model, "Burley")

    def test_is_burley_true(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin", scatter_model="Burley")
        self.assertTrue(p.is_burley)

    def test_is_separable_false(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin", scatter_model="Burley")
        self.assertFalse(p.is_separable)

    def test_is_separable_true(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin", scatter_model="Separable")
        self.assertTrue(p.is_separable)

    def test_is_enabled_true(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin", enabled=True)
        self.assertTrue(p.is_enabled)

    def test_is_enabled_false(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin", enabled=False)
        self.assertFalse(p.is_enabled)

    def test_is_high_quality_false(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin", quality="Medium")
        self.assertFalse(p.is_high_quality)

    def test_is_high_quality_true(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin", quality="Ultra")
        self.assertTrue(p.is_high_quality)

    def test_is_opaque_true(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin", opacity=1.0)
        self.assertTrue(p.is_opaque)

    def test_is_opaque_false(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin", opacity=0.5)
        self.assertFalse(p.is_opaque)

    def test_has_rgb_radii_true(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin",
                             scatter_radius_r=1.0, scatter_radius_g=0.7, scatter_radius_b=0.5)
        self.assertTrue(p.has_rgb_radii)

    def test_max_scatter_radius(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin",
                             scatter_radius_r=1.0, scatter_radius_g=0.7, scatter_radius_b=0.5)
        self.assertAlmostEqual(p.max_scatter_radius, 1.0)

    def test_is_chromatic_true(self):
        p = SSSProfileEntry(profile_id="sss_001", profile_name="Skin",
                             scatter_radius_r=1.0, scatter_radius_g=0.7, scatter_radius_b=0.5)
        self.assertTrue(p.is_chromatic)


# ---------------------------------------------------------------------------
# TransmissionEntry
# ---------------------------------------------------------------------------

class TestTransmissionEntry(unittest.TestCase):
    def test_transmission_id(self):
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001")
        self.assertEqual(t.transmission_id, "t_001")

    def test_default_mode_thick(self):
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001")
        self.assertEqual(t.mode, "Thick")

    def test_is_thick_true(self):
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001", mode="Thick")
        self.assertTrue(t.is_thick)

    def test_is_thin_false(self):
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001", mode="Thick")
        self.assertFalse(t.is_thin)

    def test_is_thin_true(self):
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001", mode="Thin")
        self.assertTrue(t.is_thin)

    def test_is_wrap_true(self):
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001", mode="Wrap")
        self.assertTrue(t.is_wrap)

    def test_casts_shadow_true(self):
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001", shadow_cast=True)
        self.assertTrue(t.casts_shadow)

    def test_is_translucent_true(self):
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001",
                               transmittance_r=0.2, transmittance_g=0.1, transmittance_b=0.05)
        self.assertTrue(t.is_translucent)


# ---------------------------------------------------------------------------
# SSSKernelEntry
# ---------------------------------------------------------------------------

class TestSSSKernelEntry(unittest.TestCase):
    def test_kernel_id(self):
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001")
        self.assertEqual(k.kernel_id, "k_001")

    def test_default_channel_all(self):
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001")
        self.assertEqual(k.channel, "All")

    def test_is_all_channels_true(self):
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001", channel="All")
        self.assertTrue(k.is_all_channels)

    def test_is_high_sample_false(self):
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001", sample_count=32)
        self.assertFalse(k.is_high_sample)

    def test_is_high_sample_true(self):
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001", sample_count=64)
        self.assertTrue(k.is_high_sample)

    def test_is_low_sample_false(self):
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001", sample_count=32)
        self.assertFalse(k.is_low_sample)

    def test_is_low_sample_true(self):
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001", sample_count=8)
        self.assertTrue(k.is_low_sample)

    def test_uses_follow_surface_true(self):
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001", use_follow_surface=True)
        self.assertTrue(k.uses_follow_surface)


# ---------------------------------------------------------------------------
# SubsurfaceScatterPipeline
# ---------------------------------------------------------------------------

class TestSubsurfaceScatterPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = SubsurfaceScatterPipeline()
        self.profile = SSSProfileEntry(profile_id="sss_001", profile_name="Skin")

    def test_add_profile(self):
        self.assertTrue(self.pipeline.add_profile(self.profile))

    def test_get_profile(self):
        self.pipeline.add_profile(self.profile)
        p = self.pipeline.get_profile("sss_001")
        self.assertIsNotNone(p)
        self.assertEqual(p.profile_name, "Skin")

    def test_profile_count(self):
        self.pipeline.add_profile(self.profile)
        self.assertEqual(self.pipeline.profile_count, 1)

    def test_is_empty_true(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_is_empty_false(self):
        self.pipeline.add_profile(self.profile)
        self.assertFalse(self.pipeline.is_empty)

    def test_remove_profile(self):
        self.pipeline.add_profile(self.profile)
        self.assertTrue(self.pipeline.remove_profile("sss_001"))
        self.assertIsNone(self.pipeline.get_profile("sss_001"))

    def test_get_all_profiles(self):
        self.pipeline.add_profile(self.profile)
        self.assertEqual(len(self.pipeline.get_all_profiles()), 1)

    def test_get_profiles_by_model(self):
        self.pipeline.add_profile(self.profile)
        result = self.pipeline.get_profiles_by_model("Burley")
        self.assertEqual(len(result), 1)

    def test_get_enabled_profiles(self):
        self.pipeline.add_profile(self.profile)
        disabled = SSSProfileEntry(profile_id="sss_002", profile_name="Disabled", enabled=False)
        self.pipeline.add_profile(disabled)
        result = self.pipeline.get_enabled_profiles()
        self.assertEqual(len(result), 1)

    def test_add_transmission(self):
        self.pipeline.add_profile(self.profile)
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001")
        self.assertTrue(self.pipeline.add_transmission("sss_001", t))

    def test_get_transmissions_for_profile(self):
        self.pipeline.add_profile(self.profile)
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001")
        self.pipeline.add_transmission("sss_001", t)
        result = self.pipeline.get_transmissions_for_profile("sss_001")
        self.assertEqual(len(result), 1)

    def test_remove_transmission(self):
        self.pipeline.add_profile(self.profile)
        t = TransmissionEntry(transmission_id="t_001", profile_id="sss_001")
        self.pipeline.add_transmission("sss_001", t)
        self.assertTrue(self.pipeline.remove_transmission("sss_001", "t_001"))

    def test_add_kernel(self):
        self.pipeline.add_profile(self.profile)
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001")
        self.assertTrue(self.pipeline.add_kernel("sss_001", k))

    def test_get_kernels_for_profile(self):
        self.pipeline.add_profile(self.profile)
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001")
        self.pipeline.add_kernel("sss_001", k)
        result = self.pipeline.get_kernels_for_profile("sss_001")
        self.assertEqual(len(result), 1)

    def test_remove_kernel(self):
        self.pipeline.add_profile(self.profile)
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001")
        self.pipeline.add_kernel("sss_001", k)
        self.assertTrue(self.pipeline.remove_kernel("sss_001", "k_001"))

    def test_get_kernels_by_channel(self):
        self.pipeline.add_profile(self.profile)
        k = SSSKernelEntry(kernel_id="k_001", profile_id="sss_001", channel="All")
        self.pipeline.add_kernel("sss_001", k)
        result = self.pipeline.get_kernels_by_channel("All")
        self.assertEqual(len(result), 1)

    def test_add_invalid_profile(self):
        bad = SSSProfileEntry(profile_id="", profile_name="Bad")
        self.assertFalse(self.pipeline.add_profile(bad))

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.profile))

    def test_clear(self):
        self.pipeline.add_profile(self.profile)
        self.pipeline.clear()
        self.assertEqual(self.pipeline.profile_count, 0)


# ---------------------------------------------------------------------------
# VectorFieldEntry
# ---------------------------------------------------------------------------

class TestVectorFieldEntry(unittest.TestCase):
    def test_field_id(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind")
        self.assertEqual(f.field_id, "vf_001")

    def test_field_name(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind")
        self.assertEqual(f.field_name, "Wind")

    def test_default_type_uniform(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind")
        self.assertEqual(f.field_type, "Uniform")

    def test_is_uniform_true(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind", field_type="Uniform")
        self.assertTrue(f.is_uniform)

    def test_is_vortex_false(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind", field_type="Uniform")
        self.assertFalse(f.is_vortex)

    def test_is_vortex_true(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Tornado", field_type="Vortex")
        self.assertTrue(f.is_vortex)

    def test_is_turbulent_true(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Turb", field_type="Turbulent")
        self.assertTrue(f.is_turbulent)

    def test_is_wind_true(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind", field_type="Wind")
        self.assertTrue(f.is_wind)

    def test_is_3d_true(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind", dimension="ThreeD")
        self.assertTrue(f.is_3d)

    def test_is_2d_true(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind", dimension="TwoD")
        self.assertTrue(f.is_2d)

    def test_voxel_count_3d(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind",
                              resolution_x=4, resolution_y=4, resolution_z=4, dimension="ThreeD")
        self.assertEqual(f.voxel_count, 64)

    def test_voxel_count_2d(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind",
                              resolution_x=4, resolution_y=4, resolution_z=4, dimension="TwoD")
        self.assertEqual(f.voxel_count, 16)

    def test_is_high_res_false(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind", resolution_x=32, resolution_y=32)
        self.assertFalse(f.is_high_res)

    def test_is_high_res_true(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind", resolution_x=64, resolution_y=64)
        self.assertTrue(f.is_high_res)

    def test_is_float32_true(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind", data_type="Float32")
        self.assertTrue(f.is_float32)

    def test_volume(self):
        f = VectorFieldEntry(field_id="vf_001", field_name="Wind",
                              bounds_x=10.0, bounds_y=10.0, bounds_z=10.0)
        self.assertAlmostEqual(f.volume, 1000.0)


# ---------------------------------------------------------------------------
# FlowVisualizationEntry
# ---------------------------------------------------------------------------

class TestFlowVisualizationEntry(unittest.TestCase):
    def test_vis_id(self):
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001")
        self.assertEqual(v.vis_id, "vis_001")

    def test_is_enabled_true(self):
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001", enabled=True)
        self.assertTrue(v.is_enabled)

    def test_shows_arrows_true(self):
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001", show_arrows=True)
        self.assertTrue(v.shows_arrows)

    def test_uses_heat_map_false(self):
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001", use_heat_map=False)
        self.assertFalse(v.uses_heat_map)

    def test_is_dense_false(self):
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001", streamline_count=64)
        self.assertFalse(v.is_dense)

    def test_is_dense_true(self):
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001", streamline_count=128)
        self.assertTrue(v.is_dense)

    def test_is_fine_step_false(self):
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001", step_size=0.5)
        self.assertFalse(v.is_fine_step)

    def test_is_fine_step_true(self):
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001", step_size=0.05)
        self.assertTrue(v.is_fine_step)


# ---------------------------------------------------------------------------
# ParticleCouplingEntry
# ---------------------------------------------------------------------------

class TestParticleCouplingEntry(unittest.TestCase):
    def test_coupling_id(self):
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001")
        self.assertEqual(c.coupling_id, "pc_001")

    def test_is_one_way_true(self):
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001", coupling_type="OneWay")
        self.assertTrue(c.is_one_way)

    def test_is_two_way_false(self):
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001", coupling_type="OneWay")
        self.assertFalse(c.is_two_way)

    def test_is_two_way_true(self):
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001", coupling_type="TwoWay")
        self.assertTrue(c.is_two_way)

    def test_is_disabled_coupling_true(self):
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001", coupling_type="None")
        self.assertTrue(c.is_disabled_coupling)

    def test_has_particle_system_false(self):
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001")
        self.assertFalse(c.has_particle_system)

    def test_has_particle_system_true(self):
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001", particle_system_id="ps_001")
        self.assertTrue(c.has_particle_system)

    def test_is_strong_false(self):
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001", strength_scale=1.0)
        self.assertFalse(c.is_strong)

    def test_is_high_drag_false(self):
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001", drag_coefficient=0.1)
        self.assertFalse(c.is_high_drag)


# ---------------------------------------------------------------------------
# VectorFieldPipeline
# ---------------------------------------------------------------------------

class TestVectorFieldPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = VectorFieldPipeline()
        self.field = VectorFieldEntry(field_id="vf_001", field_name="Wind")

    def test_add_field(self):
        self.assertTrue(self.pipeline.add_field(self.field))

    def test_get_field(self):
        self.pipeline.add_field(self.field)
        f = self.pipeline.get_field("vf_001")
        self.assertIsNotNone(f)
        self.assertEqual(f.field_name, "Wind")

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
        self.assertTrue(self.pipeline.remove_field("vf_001"))
        self.assertIsNone(self.pipeline.get_field("vf_001"))

    def test_get_all_fields(self):
        self.pipeline.add_field(self.field)
        self.assertEqual(len(self.pipeline.get_all_fields()), 1)

    def test_get_fields_by_type(self):
        self.pipeline.add_field(self.field)
        result = self.pipeline.get_fields_by_type("Uniform")
        self.assertEqual(len(result), 1)

    def test_get_fields_by_dimension(self):
        self.pipeline.add_field(self.field)
        result = self.pipeline.get_fields_by_dimension("ThreeD")
        self.assertEqual(len(result), 1)

    def test_get_enabled_fields(self):
        self.pipeline.add_field(self.field)
        disabled = VectorFieldEntry(field_id="vf_002", field_name="Disabled", enabled=False)
        self.pipeline.add_field(disabled)
        result = self.pipeline.get_enabled_fields()
        self.assertEqual(len(result), 1)

    def test_add_visualization(self):
        self.pipeline.add_field(self.field)
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001")
        self.assertTrue(self.pipeline.add_visualization("vf_001", v))

    def test_get_visualizations_for_field(self):
        self.pipeline.add_field(self.field)
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001")
        self.pipeline.add_visualization("vf_001", v)
        result = self.pipeline.get_visualizations_for_field("vf_001")
        self.assertEqual(len(result), 1)

    def test_remove_visualization(self):
        self.pipeline.add_field(self.field)
        v = FlowVisualizationEntry(vis_id="vis_001", field_id="vf_001")
        self.pipeline.add_visualization("vf_001", v)
        self.assertTrue(self.pipeline.remove_visualization("vf_001", "vis_001"))

    def test_add_coupling(self):
        self.pipeline.add_field(self.field)
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001")
        self.assertTrue(self.pipeline.add_coupling("vf_001", c))

    def test_get_couplings_for_field(self):
        self.pipeline.add_field(self.field)
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001")
        self.pipeline.add_coupling("vf_001", c)
        result = self.pipeline.get_couplings_for_field("vf_001")
        self.assertEqual(len(result), 1)

    def test_remove_coupling(self):
        self.pipeline.add_field(self.field)
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001")
        self.pipeline.add_coupling("vf_001", c)
        self.assertTrue(self.pipeline.remove_coupling("vf_001", "pc_001"))

    def test_get_couplings_by_type(self):
        self.pipeline.add_field(self.field)
        c = ParticleCouplingEntry(coupling_id="pc_001", field_id="vf_001", coupling_type="OneWay")
        self.pipeline.add_coupling("vf_001", c)
        result = self.pipeline.get_couplings_by_type("OneWay")
        self.assertEqual(len(result), 1)

    def test_add_invalid_field(self):
        bad = VectorFieldEntry(field_id="", field_name="Bad")
        self.assertFalse(self.pipeline.add_field(bad))

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.field))

    def test_clear(self):
        self.pipeline.add_field(self.field)
        self.pipeline.clear()
        self.assertEqual(self.pipeline.field_count, 0)


if __name__ == "__main__":
    unittest.main()
