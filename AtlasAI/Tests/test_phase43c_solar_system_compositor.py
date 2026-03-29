"""Phase 43C — Tests for orion_solar_system.json and SolarSystemCompositor.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


def _load_json(name: str) -> dict:
    return json.loads((SOLAR_SYSTEMS / f"{name}.json").read_text())


# ---------------------------------------------------------------------------
# orion_solar_system.json
# ---------------------------------------------------------------------------

class TestOrionSolarSystemJson(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS / "orion_solar_system.json").exists())

    def test_has_id(self):
        data = _load_json("orion_solar_system")
        self.assertIn("id", data)
        self.assertIn("orion", data["id"])

    def test_has_name(self):
        data = _load_json("orion_solar_system")
        self.assertIn("name", data)
        self.assertIn("Orion", data["name"])

    def test_has_star(self):
        data = _load_json("orion_solar_system")
        self.assertIn("star", data)

    def test_star_type_k2v(self):
        data = _load_json("orion_solar_system")
        self.assertEqual(data["star"]["type"], "K2V")

    def test_has_celestials(self):
        data = _load_json("orion_solar_system")
        self.assertIn("celestials", data)

    def test_total_celestials_8(self):
        data = _load_json("orion_solar_system")
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_count_8(self):
        data = _load_json("orion_solar_system")
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_habitable_planet(self):
        data = _load_json("orion_solar_system")
        habitable = [c for c in data["celestials"] if c.get("habitable", False)]
        self.assertGreaterEqual(len(habitable), 1)

    def test_has_gas_giant(self):
        data = _load_json("orion_solar_system")
        gas_giants = [c for c in data["celestials"] if c.get("type") == "GasGiant"]
        self.assertEqual(len(gas_giants), 1)

    def test_has_station(self):
        data = _load_json("orion_solar_system")
        stations = [c for c in data["celestials"] if c.get("type") == "Station"]
        self.assertEqual(len(stations), 1)

    def test_has_moons(self):
        data = _load_json("orion_solar_system")
        moons = [c for c in data["celestials"] if c.get("type") == "Moon"]
        self.assertGreaterEqual(len(moons), 1)

    def test_has_asteroid_belt(self):
        data = _load_json("orion_solar_system")
        belts = [c for c in data["celestials"] if c.get("type") == "AsteroidBelt"]
        self.assertEqual(len(belts), 1)

    def test_has_npc_factions(self):
        data = _load_json("orion_solar_system")
        self.assertIn("npc_factions", data)
        self.assertGreaterEqual(len(data["npc_factions"]), 1)

    def test_has_pcg_config(self):
        data = _load_json("orion_solar_system")
        self.assertIn("pcg_config", data)

    def test_pcg_config_seed(self):
        data = _load_json("orion_solar_system")
        self.assertIn("seed", data["pcg_config"])

    def test_has_version(self):
        data = _load_json("orion_solar_system")
        self.assertIn("version", data)

    def test_habitable_has_atmosphere(self):
        data = _load_json("orion_solar_system")
        habitable = [c for c in data["celestials"] if c.get("habitable", False)]
        for h in habitable:
            self.assertIn("atmosphere", h)

    def test_star_has_luminosity(self):
        data = _load_json("orion_solar_system")
        self.assertIn("luminosity", data["star"])

    def test_star_has_temperature(self):
        data = _load_json("orion_solar_system")
        self.assertIn("temperature", data["star"])

    def test_has_hazards(self):
        data = _load_json("orion_solar_system")
        self.assertIn("hazards", data)


# ---------------------------------------------------------------------------
# SolarSystemCompositor.h
# ---------------------------------------------------------------------------

class TestSolarSystemCompositorHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemCompositor.h").exists())


class TestSolarSystemCompositorNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("SolarSystemCompositor"))


class TestSolarSystemCompositorEnums(unittest.TestCase):
    def test_composite_mode_enum(self):
        self.assertIn("CompositeMode", _read_header("SolarSystemCompositor"))

    def test_render_pass_type_enum(self):
        self.assertIn("RenderPassType", _read_header("SolarSystemCompositor"))

    def test_layer_blend_op_enum(self):
        self.assertIn("LayerBlendOp", _read_header("SolarSystemCompositor"))

    def test_compositor_state_enum(self):
        self.assertIn("CompositorState", _read_header("SolarSystemCompositor"))

    def test_opaque_mode_value(self):
        self.assertIn("Opaque", _read_header("SolarSystemCompositor"))

    def test_translucent_mode_value(self):
        self.assertIn("Translucent", _read_header("SolarSystemCompositor"))

    def test_additive_mode_value(self):
        self.assertIn("Additive", _read_header("SolarSystemCompositor"))

    def test_depth_pass_type(self):
        self.assertIn("Depth", _read_header("SolarSystemCompositor"))

    def test_shadow_pass_type(self):
        self.assertIn("Shadow", _read_header("SolarSystemCompositor"))

    def test_compositing_state(self):
        self.assertIn("Compositing", _read_header("SolarSystemCompositor"))


class TestSolarSystemCompositorStructs(unittest.TestCase):
    def test_composite_layer_def_struct(self):
        self.assertIn("CompositeLayerDef", _read_header("SolarSystemCompositor"))

    def test_render_pass_def_struct(self):
        self.assertIn("RenderPassDef", _read_header("SolarSystemCompositor"))

    def test_post_process_stack_def_struct(self):
        self.assertIn("PostProcessStackDef", _read_header("SolarSystemCompositor"))

    def test_cast_shadows_in_layer(self):
        self.assertIn("castShadows", _read_header("SolarSystemCompositor"))

    def test_async_execution_in_pass(self):
        self.assertIn("asyncExecution", _read_header("SolarSystemCompositor"))

    def test_blend_weight_in_stack(self):
        self.assertIn("blendWeight", _read_header("SolarSystemCompositor"))


class TestSolarSystemCompositorMethods(unittest.TestCase):
    def test_add_layer(self):
        self.assertIn("AddLayer", _read_header("SolarSystemCompositor"))

    def test_remove_layer(self):
        self.assertIn("RemoveLayer", _read_header("SolarSystemCompositor"))

    def test_enable_layer(self):
        self.assertIn("EnableLayer", _read_header("SolarSystemCompositor"))

    def test_set_layer_mode(self):
        self.assertIn("SetLayerMode", _read_header("SolarSystemCompositor"))

    def test_get_layers_by_mode(self):
        self.assertIn("GetLayersByMode", _read_header("SolarSystemCompositor"))

    def test_get_layers_sorted_by_order(self):
        self.assertIn("GetLayersSortedByOrder", _read_header("SolarSystemCompositor"))

    def test_add_render_pass(self):
        self.assertIn("AddRenderPass", _read_header("SolarSystemCompositor"))

    def test_get_passes_by_type(self):
        self.assertIn("GetPassesByType", _read_header("SolarSystemCompositor"))

    def test_get_async_passes(self):
        self.assertIn("GetAsyncPasses", _read_header("SolarSystemCompositor"))

    def test_add_post_process_stack(self):
        self.assertIn("AddPostProcessStack", _read_header("SolarSystemCompositor"))

    def test_add_effect_to_stack(self):
        self.assertIn("AddEffectToStack", _read_header("SolarSystemCompositor"))

    def test_composite(self):
        self.assertIn("Composite", _read_header("SolarSystemCompositor"))

    def test_is_compositing(self):
        self.assertIn("IsCompositing", _read_header("SolarSystemCompositor"))

    def test_get_state(self):
        self.assertIn("GetState", _read_header("SolarSystemCompositor"))

    def test_reset(self):
        self.assertIn("Reset", _read_header("SolarSystemCompositor"))


if __name__ == "__main__":
    unittest.main()
