"""Phase 42C — Tests for cygnus_solar_system.json and SolarSystemAssembler.h."""
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
# cygnus_solar_system.json
# ---------------------------------------------------------------------------

class TestCygnusSolarSystemJson(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS / "cygnus_solar_system.json").exists())

    def test_has_id(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("id", data)
        self.assertIn("cygnus", data["id"])

    def test_has_name(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("name", data)
        self.assertIn("Cygnus", data["name"])

    def test_has_star(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("star", data)

    def test_star_type_g3v(self):
        data = _load_json("cygnus_solar_system")
        self.assertEqual(data["star"]["type"], "G3V")

    def test_has_celestials(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("celestials", data)

    def test_total_celestials_8(self):
        data = _load_json("cygnus_solar_system")
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_count_8(self):
        data = _load_json("cygnus_solar_system")
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_habitable_planet(self):
        data = _load_json("cygnus_solar_system")
        habitable = [c for c in data["celestials"] if c.get("habitable", False)]
        self.assertGreaterEqual(len(habitable), 1)

    def test_has_gas_giant(self):
        data = _load_json("cygnus_solar_system")
        gas_giants = [c for c in data["celestials"] if c.get("type") == "GasGiant"]
        self.assertEqual(len(gas_giants), 1)

    def test_has_station(self):
        data = _load_json("cygnus_solar_system")
        stations = [c for c in data["celestials"] if c.get("type") == "Station"]
        self.assertEqual(len(stations), 1)

    def test_has_anomaly(self):
        data = _load_json("cygnus_solar_system")
        anomalies = [c for c in data["celestials"] if c.get("type") == "Anomaly"]
        self.assertEqual(len(anomalies), 1)

    def test_has_moon(self):
        data = _load_json("cygnus_solar_system")
        moons = [c for c in data["celestials"] if c.get("type") == "Moon"]
        self.assertGreaterEqual(len(moons), 1)

    def test_has_npc_factions(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("npc_factions", data)
        self.assertGreaterEqual(len(data["npc_factions"]), 1)

    def test_has_pcg_config(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("pcg_config", data)

    def test_pcg_config_seed(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("seed", data["pcg_config"])

    def test_has_version(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("version", data)

    def test_habitable_has_atmosphere(self):
        data = _load_json("cygnus_solar_system")
        habitable = [c for c in data["celestials"] if c.get("habitable", False)]
        for h in habitable:
            self.assertIn("atmosphere", h)

    def test_star_has_luminosity(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("luminosity", data["star"])

    def test_star_has_temperature(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("temperature", data["star"])

    def test_has_hazards(self):
        data = _load_json("cygnus_solar_system")
        self.assertIn("hazards", data)


# ---------------------------------------------------------------------------
# SolarSystemAssembler.h
# ---------------------------------------------------------------------------

class TestSolarSystemAssemblerHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemAssembler.h").exists())


class TestSolarSystemAssemblerNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("SolarSystemAssembler"))


class TestSolarSystemAssemblerEnums(unittest.TestCase):
    def test_assembly_state_enum(self):
        self.assertIn("AssemblyState", _read_header("SolarSystemAssembler"))

    def test_lod_stage_enum(self):
        self.assertIn("LODStage", _read_header("SolarSystemAssembler"))

    def test_streaming_priority_enum(self):
        self.assertIn("StreamingPriority", _read_header("SolarSystemAssembler"))

    def test_assembly_pass_enum(self):
        self.assertIn("AssemblyPass", _read_header("SolarSystemAssembler"))

    def test_pending_state_value(self):
        self.assertIn("Pending", _read_header("SolarSystemAssembler"))

    def test_complete_state_value(self):
        self.assertIn("Complete", _read_header("SolarSystemAssembler"))

    def test_stale_state_value(self):
        self.assertIn("Stale", _read_header("SolarSystemAssembler"))

    def test_full_lod_value(self):
        self.assertIn("Full", _read_header("SolarSystemAssembler"))

    def test_impostor_lod_value(self):
        self.assertIn("Impostor", _read_header("SolarSystemAssembler"))

    def test_critical_priority_value(self):
        self.assertIn("Critical", _read_header("SolarSystemAssembler"))


class TestSolarSystemAssemblerStructs(unittest.TestCase):
    def test_assembly_manifest_def_struct(self):
        self.assertIn("AssemblyManifestDef", _read_header("SolarSystemAssembler"))

    def test_lod_stage_def_struct(self):
        self.assertIn("LODStageDef", _read_header("SolarSystemAssembler"))

    def test_streaming_chunk_def_struct(self):
        self.assertIn("StreamingChunkDef", _read_header("SolarSystemAssembler"))

    def test_celestial_count_in_manifest(self):
        self.assertIn("celestialCount", _read_header("SolarSystemAssembler"))

    def test_screen_size_threshold_in_lod(self):
        self.assertIn("screenSizeThreshold", _read_header("SolarSystemAssembler"))

    def test_load_radius_in_chunk(self):
        self.assertIn("loadRadiusLY", _read_header("SolarSystemAssembler"))


class TestSolarSystemAssemblerMethods(unittest.TestCase):
    def test_create_manifest(self):
        self.assertIn("CreateManifest", _read_header("SolarSystemAssembler"))

    def test_delete_manifest(self):
        self.assertIn("DeleteManifest", _read_header("SolarSystemAssembler"))

    def test_build_manifest(self):
        self.assertIn("BuildManifest", _read_header("SolarSystemAssembler"))

    def test_invalidate_manifest(self):
        self.assertIn("InvalidateManifest", _read_header("SolarSystemAssembler"))

    def test_get_manifests_by_state(self):
        self.assertIn("GetManifestsByState", _read_header("SolarSystemAssembler"))

    def test_get_stale_manifests(self):
        self.assertIn("GetStaleManifests", _read_header("SolarSystemAssembler"))

    def test_add_lod_stage(self):
        self.assertIn("AddLODStage", _read_header("SolarSystemAssembler"))

    def test_get_lod_stages_by_level(self):
        self.assertIn("GetLODStagesByLevel", _read_header("SolarSystemAssembler"))

    def test_add_chunk(self):
        self.assertIn("AddChunk", _read_header("SolarSystemAssembler"))

    def test_load_chunk(self):
        self.assertIn("LoadChunk", _read_header("SolarSystemAssembler"))

    def test_unload_chunk(self):
        self.assertIn("UnloadChunk", _read_header("SolarSystemAssembler"))

    def test_pin_chunk(self):
        self.assertIn("PinChunk", _read_header("SolarSystemAssembler"))

    def test_get_pinned_chunks(self):
        self.assertIn("GetPinnedChunks", _read_header("SolarSystemAssembler"))

    def test_reset(self):
        self.assertIn("Reset", _read_header("SolarSystemAssembler"))


if __name__ == "__main__":
    unittest.main()
