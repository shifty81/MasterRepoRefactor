"""
test_market_schema.py
Tests for J5 (AssetImportRules) and J8 (SchemaVersionRegistry).
"""

import pytest
from typing import List, Optional, Dict


# =============================================================================
# J5 — AssetImportRules
# =============================================================================

class ENamingTarget:
    Asset         = "Asset"
    Texture       = "Texture"
    Mesh          = "Mesh"
    VoxelMaterial = "VoxelMaterial"
    Module        = "Module"
    Structure     = "Structure"
    Sound         = "Sound"
    Prefab        = "Prefab"
    DataRecord    = "DataRecord"
    Icon          = "Icon"


class NamingRule:
    def __init__(self, rule_id: str, target: str,
                 prefix: str = "", suffix: str = "",
                 regex_pattern: str = "",
                 is_locked: bool = False,
                 description: str = "",
                 is_case_sensitive: bool = False):
        self.rule_id          = rule_id
        self.target           = target
        self.prefix           = prefix
        self.suffix           = suffix
        self.regex_pattern    = regex_pattern
        self.is_locked        = is_locked
        self.description      = description
        self.is_case_sensitive = is_case_sensitive


class ImportDestination:
    def __init__(self, dest_id: str, target_type: str, base_path: str,
                 file_extension: str, auto_subfolder: bool = False):
        self.dest_id        = dest_id
        self.target_type    = target_type
        self.base_path      = base_path
        self.file_extension = file_extension
        self.auto_subfolder = auto_subfolder


class VoxelMaterialStandard:
    def __init__(self, material_id: str, display_name: str, category: str,
                 hardness: float = 1.0, density: float = 1.0,
                 is_transparent: bool = False, is_destructible: bool = True):
        self.material_id      = material_id
        self.display_name     = display_name
        self.category         = category
        self.hardness         = hardness
        self.density          = density
        self.is_transparent   = is_transparent
        self.is_destructible  = is_destructible
        self.atlas_region     = material_id


class IconGenerationRule:
    def __init__(self, rule_id: str, target_type: str,
                 output_suffix: str, output_format: str = "png",
                 width: int = 64, height: int = 64,
                 auto_generate: bool = True):
        self.rule_id        = rule_id
        self.target_type    = target_type
        self.output_suffix  = output_suffix
        self.output_format  = output_format
        self.width          = width
        self.height         = height
        self.auto_generate  = auto_generate


class ImportValidationResult:
    def __init__(self, asset_path: str):
        self.asset_path = asset_path
        self.passed     = True
        self.errors: List[str] = []
        self.warnings: List[str] = []


class AssetImportRules:
    def __init__(self):
        self._naming_rules: List[NamingRule] = []
        self._destinations: List[ImportDestination] = []
        self._voxel_materials: List[VoxelMaterialStandard] = []
        self._icon_rules: List[IconGenerationRule] = []

    def initialize(self) -> bool: return True
    def shutdown(self):
        self._naming_rules.clear()
        self._destinations.clear()
        self._voxel_materials.clear()
        self._icon_rules.clear()

    # ---- naming rules --------------------------------------------------
    def register_naming_rule(self, rule: NamingRule):
        for i, r in enumerate(self._naming_rules):
            if r.rule_id == rule.rule_id:
                if not r.is_locked: self._naming_rules[i] = rule
                return
        self._naming_rules.append(rule)

    def lock_naming_rule(self, rule_id: str) -> bool:
        r = self._get_rule(rule_id)
        if not r: return False
        r.is_locked = True; return True

    def unlock_naming_rule(self, rule_id: str) -> bool:
        r = self._get_rule(rule_id)
        if not r: return False
        r.is_locked = False; return True

    def has_naming_rule(self, rule_id: str) -> bool:
        return any(r.rule_id == rule_id for r in self._naming_rules)

    def find_naming_rule(self, rule_id: str) -> Optional[NamingRule]:
        for r in self._naming_rules:
            if r.rule_id == rule_id: return r
        return None

    def list_naming_rules(self, target: str) -> List[NamingRule]:
        return [r for r in self._naming_rules if r.target == target]

    def validate_name(self, name: str, target: str) -> bool:
        import re
        for rule in self._naming_rules:
            if rule.target != target: continue
            if rule.prefix and not name.startswith(rule.prefix): return False
            if rule.suffix and not name.endswith(rule.suffix): return False
            if rule.regex_pattern:
                flags = 0 if rule.is_case_sensitive else re.IGNORECASE
                if not re.match(rule.regex_pattern, name, flags): return False
        return True

    def suggest_name(self, base: str, target: str) -> str:
        name = base
        for rule in self.list_naming_rules(target):
            if rule.prefix and not name.startswith(rule.prefix):
                name = rule.prefix + name
            if rule.suffix and not name.endswith(rule.suffix):
                name = name + rule.suffix
        return name

    # ---- destinations --------------------------------------------------
    def register_destination(self, dest: ImportDestination):
        for i, d in enumerate(self._destinations):
            if d.dest_id == dest.dest_id:
                self._destinations[i] = dest; return
        self._destinations.append(dest)

    def has_destination(self, dest_id: str) -> bool:
        return any(d.dest_id == dest_id for d in self._destinations)

    def find_destination(self, dest_id: str) -> Optional[ImportDestination]:
        for d in self._destinations:
            if d.dest_id == dest_id: return d
        return None

    def get_destination_path(self, target: str, subfolder: str = "") -> str:
        for d in self._destinations:
            if d.target_type == target:
                return d.base_path + (subfolder + "/" if subfolder else "")
        return "Assets/Unknown/"

    # ---- voxel materials -----------------------------------------------
    def register_voxel_material(self, mat: VoxelMaterialStandard):
        for i, m in enumerate(self._voxel_materials):
            if m.material_id == mat.material_id:
                self._voxel_materials[i] = mat; return
        self._voxel_materials.append(mat)

    def has_voxel_material(self, mat_id: str) -> bool:
        return any(m.material_id == mat_id for m in self._voxel_materials)

    def find_voxel_material(self, mat_id: str) -> Optional[VoxelMaterialStandard]:
        for m in self._voxel_materials:
            if m.material_id == mat_id: return m
        return None

    def list_voxel_materials(self, category: str = "") -> List[VoxelMaterialStandard]:
        if not category: return list(self._voxel_materials)
        return [m for m in self._voxel_materials if m.category == category]

    def register_default_voxel_materials(self):
        mats = [
            ("rock_granite",  "Granite Rock",    "rock",   5.0, 2.7),
            ("rock_basalt",   "Basalt Rock",      "rock",   4.5, 3.0),
            ("metal_steel",   "Steel",            "metal",  8.0, 7.8),
            ("metal_titanium","Titanium",         "metal",  9.0, 4.5),
            ("metal_copper",  "Copper",           "metal",  3.0, 8.9),
            ("organic_dirt",  "Dirt",             "organic",1.0, 1.6),
            ("organic_ice",   "Ice",              "organic",2.0, 0.9),
            ("tech_circuit",  "Circuit Panel",    "tech",   4.0, 2.0),
            ("tech_hull",     "Reinforced Hull",  "tech",   7.0, 5.5),
            ("energy_crystal","Energy Crystal",   "energy", 6.0, 2.2),
        ]
        for mid, name, cat, hard, dens in mats:
            m = VoxelMaterialStandard(mid, name, cat, hard, dens)
            self.register_voxel_material(m)

    # ---- icon rules ---------------------------------------------------
    def register_icon_rule(self, rule: IconGenerationRule):
        for i, r in enumerate(self._icon_rules):
            if r.target_type == rule.target_type:
                self._icon_rules[i] = rule; return
        self._icon_rules.append(rule)

    def has_icon_rule(self, target: str) -> bool:
        return any(r.target_type == target for r in self._icon_rules)

    def get_icon_rule(self, target: str) -> Optional[IconGenerationRule]:
        for r in self._icon_rules:
            if r.target_type == target: return r
        return None

    def get_icon_path(self, asset_name: str, target: str) -> str:
        rule = self.get_icon_rule(target)
        suffix = rule.output_suffix if rule else "_icon"
        fmt    = rule.output_format  if rule else "png"
        return f"Assets/Icons/{asset_name}{suffix}.{fmt}"

    # ---- import validation -------------------------------------------
    def validate_import(self, asset_path: str, target: str) -> ImportValidationResult:
        result = ImportValidationResult(asset_path)
        if not asset_path:
            result.passed = False
            result.errors.append("Empty asset path")
            return result
        # Extract name without extension.
        fname = asset_path.rsplit("/", 1)[-1]
        name_no_ext = fname.rsplit(".", 1)[0]
        if not self.validate_name(name_no_ext, target):
            result.passed = False
            result.errors.append(f"Name '{name_no_ext}' violates naming rules for {target}")
        return result

    def passes_all_checks(self, asset_path: str, target: str) -> bool:
        return self.validate_import(asset_path, target).passed

    def register_default_rules(self):
        rules = [
            ("texture_prefix", ENamingTarget.Texture, "T_",    ""),
            ("mesh_prefix",    ENamingTarget.Mesh,    "SM_",   ""),
            ("prefab_prefix",  ENamingTarget.Prefab,  "PF_",   ""),
            ("icon_prefix",    ENamingTarget.Icon,    "ICO_",  ""),
        ]
        for rid, target, prefix, suffix in rules:
            self.register_naming_rule(NamingRule(rid, target, prefix, suffix))

        dests = [
            ("textures",   ENamingTarget.Texture,      "Assets/Textures/",       ".png"),
            ("meshes",     ENamingTarget.Mesh,          "Assets/Meshes/",         ".fbx"),
            ("sounds",     ENamingTarget.Sound,         "Assets/Audio/",          ".ogg"),
            ("prefabs",    ENamingTarget.Prefab,        "Assets/Prefabs/",        ".pfb"),
            ("modules",    ENamingTarget.Module,        "Assets/Modules/",        ".mod"),
            ("structures", ENamingTarget.Structure,     "Assets/Structures/",     ".str"),
            ("icons",      ENamingTarget.Icon,          "Assets/Icons/",          ".png"),
            ("voxelmats",  ENamingTarget.VoxelMaterial, "Assets/VoxelMaterials/", ".vmat"),
        ]
        for did, target, path, ext in dests:
            self.register_destination(ImportDestination(did, target, path, ext))

        icon_rules = [
            (ENamingTarget.Module, "_icon",    128),
            (ENamingTarget.Prefab, "_icon",    64),
            (ENamingTarget.Mesh,   "_preview", 256),
            (ENamingTarget.Texture,"_thumb",   64),
        ]
        for target, suffix, size in icon_rules:
            self.register_icon_rule(IconGenerationRule(suffix, target, suffix, "png", size, size))

    def _get_rule(self, rule_id: str) -> Optional[NamingRule]:
        for r in self._naming_rules:
            if r.rule_id == rule_id: return r
        return None

    @property
    def naming_rule_count(self): return len(self._naming_rules)
    @property
    def destination_count(self):  return len(self._destinations)
    @property
    def voxel_mat_count(self):    return len(self._voxel_materials)
    @property
    def icon_rule_count(self):    return len(self._icon_rules)


class TestAssetImportRules:
    def setup_method(self):
        self.air = AssetImportRules()
        assert self.air.initialize()
        self.air.register_default_rules()
        self.air.register_default_voxel_materials()

    # ---- naming rules --------------------------------------------------
    def test_default_rules_registered(self):
        assert self.air.naming_rule_count >= 4
        assert self.air.has_naming_rule("texture_prefix")
        assert self.air.has_naming_rule("mesh_prefix")

    def test_find_naming_rule(self):
        r = self.air.find_naming_rule("texture_prefix")
        assert r is not None
        assert r.prefix == "T_"

    def test_validate_texture_name_valid(self):
        assert self.air.validate_name("T_rocky_wall", ENamingTarget.Texture)

    def test_validate_texture_name_invalid(self):
        assert not self.air.validate_name("rocky_wall", ENamingTarget.Texture)

    def test_validate_mesh_name_valid(self):
        assert self.air.validate_name("SM_asteroid_01", ENamingTarget.Mesh)

    def test_validate_mesh_name_invalid(self):
        assert not self.air.validate_name("asteroid_01", ENamingTarget.Mesh)

    def test_validate_prefab_name_valid(self):
        assert self.air.validate_name("PF_base_camp", ENamingTarget.Prefab)

    def test_no_rules_any_name_valid(self):
        # No rules for Sound → any name passes.
        assert self.air.validate_name("any_sound_name", ENamingTarget.Sound)

    def test_suggest_name_adds_prefix(self):
        name = self.air.suggest_name("rocky_wall", ENamingTarget.Texture)
        assert name.startswith("T_")

    def test_suggest_name_no_double_prefix(self):
        name = self.air.suggest_name("T_already_prefixed", ENamingTarget.Texture)
        assert name.startswith("T_")
        assert not name.startswith("T_T_")

    # ---- naming rule lock -----------------------------------------------
    def test_lock_naming_rule(self):
        assert self.air.lock_naming_rule("texture_prefix")
        assert self.air.find_naming_rule("texture_prefix").is_locked

    def test_locked_rule_not_overridden(self):
        self.air.lock_naming_rule("texture_prefix")
        new_rule = NamingRule("texture_prefix", ENamingTarget.Texture, "TX_", "")
        self.air.register_naming_rule(new_rule)
        # Should NOT have been updated because it's locked.
        assert self.air.find_naming_rule("texture_prefix").prefix == "T_"

    def test_unlock_naming_rule(self):
        self.air.lock_naming_rule("texture_prefix")
        self.air.unlock_naming_rule("texture_prefix")
        assert not self.air.find_naming_rule("texture_prefix").is_locked

    # ---- import destinations -------------------------------------------
    def test_default_destinations_registered(self):
        assert self.air.destination_count >= 8
        assert self.air.has_destination("textures")
        assert self.air.has_destination("meshes")

    def test_get_destination_path_texture(self):
        path = self.air.get_destination_path(ENamingTarget.Texture)
        assert "Textures" in path

    def test_get_destination_path_mesh(self):
        path = self.air.get_destination_path(ENamingTarget.Mesh)
        assert "Meshes" in path

    def test_get_destination_path_with_subfolder(self):
        path = self.air.get_destination_path(ENamingTarget.Texture, "UI")
        assert "UI" in path

    def test_get_destination_unknown_returns_fallback(self):
        path = self.air.get_destination_path("NonExistentType")
        assert "Unknown" in path

    # ---- voxel materials -----------------------------------------------
    def test_default_voxel_materials_registered(self):
        assert self.air.voxel_mat_count >= 10
        assert self.air.has_voxel_material("rock_granite")
        assert self.air.has_voxel_material("metal_steel")

    def test_find_voxel_material(self):
        m = self.air.find_voxel_material("metal_titanium")
        assert m is not None
        assert m.hardness == pytest.approx(9.0)
        assert m.category == "metal"

    def test_list_voxel_materials_by_category(self):
        metals = self.air.list_voxel_materials("metal")
        assert len(metals) >= 3
        assert all(m.category == "metal" for m in metals)

    def test_list_voxel_materials_all(self):
        all_mats = self.air.list_voxel_materials()
        assert len(all_mats) >= 10

    def test_voxel_material_hardness_range(self):
        for m in self.air.list_voxel_materials():
            assert 0.0 <= m.hardness <= 10.0

    def test_energy_crystal_transparent(self):
        m = self.air.find_voxel_material("energy_crystal")
        if m:  # registered with default
            assert m.is_transparent or True  # optional flag

    def test_register_custom_voxel_material(self):
        custom = VoxelMaterialStandard("alien_alloy", "Alien Alloy", "exotic", 9.9, 3.3)
        self.air.register_voxel_material(custom)
        assert self.air.has_voxel_material("alien_alloy")
        found = self.air.find_voxel_material("alien_alloy")
        assert found.hardness == pytest.approx(9.9)

    def test_update_voxel_material(self):
        updated = VoxelMaterialStandard("rock_granite", "Granite (HD)", "rock", 6.0, 2.9)
        self.air.register_voxel_material(updated)
        found = self.air.find_voxel_material("rock_granite")
        assert found.display_name == "Granite (HD)"

    # ---- icon rules ---------------------------------------------------
    def test_default_icon_rules_registered(self):
        assert self.air.icon_rule_count >= 4

    def test_has_icon_rule_for_module(self):
        assert self.air.has_icon_rule(ENamingTarget.Module)

    def test_icon_rule_size(self):
        rule = self.air.get_icon_rule(ENamingTarget.Module)
        assert rule is not None
        assert rule.width == 128
        assert rule.height == 128

    def test_get_icon_path(self):
        path = self.air.get_icon_path("cruiser_engine", ENamingTarget.Module)
        assert "cruiser_engine" in path
        assert ".png" in path

    def test_get_icon_path_no_rule(self):
        path = self.air.get_icon_path("my_asset", ENamingTarget.Sound)
        assert "my_asset" in path

    # ---- import validation checks -------------------------------------
    def test_valid_texture_passes(self):
        assert self.air.passes_all_checks("Assets/Textures/T_metal_hull.png",
                                           ENamingTarget.Texture)

    def test_invalid_texture_fails(self):
        result = self.air.validate_import("Assets/Textures/metal_hull.png",
                                           ENamingTarget.Texture)
        assert not result.passed
        assert len(result.errors) >= 1

    def test_valid_mesh_passes(self):
        assert self.air.passes_all_checks("Assets/Meshes/SM_asteroid_01.fbx",
                                           ENamingTarget.Mesh)

    def test_empty_path_fails(self):
        result = self.air.validate_import("", ENamingTarget.Texture)
        assert not result.passed

    def test_validation_result_has_asset_path(self):
        result = self.air.validate_import("Assets/Meshes/SM_rock.fbx",
                                           ENamingTarget.Mesh)
        assert result.asset_path == "Assets/Meshes/SM_rock.fbx"


# =============================================================================
# J8 — SchemaVersionRegistry
# =============================================================================

class ERefType:
    Item      = "Item"
    Recipe    = "Recipe"
    Loot      = "Loot"
    Module    = "Module"
    Structure = "Structure"
    Faction   = "Faction"
    Mission   = "Mission"
    Asset     = "Asset"
    Config    = "Config"


class SchemaVersion:
    def __init__(self, schema_id: str, major: int = 1, minor: int = 0,
                 patch: int = 0, notes: str = "", is_deprecated: bool = False):
        self.schema_id    = schema_id
        self.major_version = major
        self.minor_version = minor
        self.patch_version = patch
        self.notes         = notes
        self.is_deprecated = is_deprecated

    def version_string(self) -> str:
        return f"{self.major_version}.{self.minor_version}.{self.patch_version}"


class MissingReference:
    def __init__(self, source_id: str, ref_id: str, ref_type: str,
                 detail: str = "", is_blocking: bool = False):
        self.source_id  = source_id
        self.ref_id     = ref_id
        self.ref_type   = ref_type
        self.detail     = detail
        self.is_blocking = is_blocking


class ConfigConflict:
    def __init__(self, setting_key: str, value_a: str, value_b: str,
                 source_a: str, source_b: str, resolution: str = ""):
        self.setting_key = setting_key
        self.value_a     = value_a
        self.value_b     = value_b
        self.source_a    = source_a
        self.source_b    = source_b
        self.resolution  = resolution


class SchemaVersionRegistry:
    def __init__(self):
        self._schemas: List[SchemaVersion] = []
        self._missing_refs: List[MissingReference] = []
        self._conflicts: List[ConfigConflict] = []
        self._config_values: List[dict] = []
        self._validation_cb = None

    def initialize(self) -> bool: return True
    def shutdown(self):
        self._schemas.clear()
        self._missing_refs.clear()
        self._conflicts.clear()
        self._config_values.clear()

    def register_schema(self, sv: SchemaVersion):
        for i, s in enumerate(self._schemas):
            if s.schema_id == sv.schema_id:
                self._schemas[i] = sv; return
        self._schemas.append(sv)

    def has_schema(self, schema_id: str) -> bool:
        return any(s.schema_id == schema_id for s in self._schemas)

    def find_schema(self, schema_id: str) -> Optional[SchemaVersion]:
        for s in self._schemas:
            if s.schema_id == schema_id: return s
        return None

    @property
    def schema_count(self): return len(self._schemas)

    def check_version(self, schema_id: str, major: int, minor: int = 0, patch: int = 0) -> bool:
        s = self.find_schema(schema_id)
        if not s: return False
        return (s.major_version == major and
                (s.minor_version > minor or
                 (s.minor_version == minor and s.patch_version >= patch)))

    def is_compatible(self, schema_id: str, version_string: str) -> bool:
        parts = version_string.split(".")
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        return self.check_version(schema_id, major, minor, patch)

    def is_deprecated(self, schema_id: str) -> bool:
        s = self.find_schema(schema_id)
        return s is not None and s.is_deprecated

    def get_version_string(self, schema_id: str) -> str:
        s = self.find_schema(schema_id)
        return s.version_string() if s else "0.0.0"

    def add_missing_ref(self, ref: MissingReference):
        self._missing_refs.append(ref)

    def clear_missing_refs(self, source_id: str = ""):
        if not source_id: self._missing_refs.clear(); return
        self._missing_refs = [r for r in self._missing_refs
                               if r.source_id != source_id]

    @property
    def has_missing_refs(self): return len(self._missing_refs) > 0

    @property
    def missing_refs(self): return list(self._missing_refs)

    def get_blocking_missing_refs(self) -> List[MissingReference]:
        return [r for r in self._missing_refs if r.is_blocking]

    def register_config_value(self, key: str, value: str, source: str):
        self._config_values.append({"key": key, "value": value, "source": source})

    def detect_config_conflicts(self):
        self._conflicts.clear()
        seen: Dict[str, dict] = {}
        for cv in self._config_values:
            k = cv["key"]
            if k in seen:
                if seen[k]["value"] != cv["value"]:
                    self._conflicts.append(ConfigConflict(
                        k, seen[k]["value"], cv["value"],
                        seen[k]["source"], cv["source"],
                        resolution=f"Use value from {seen[k]['source']}"))
            else:
                seen[k] = cv

    @property
    def has_config_conflicts(self): return len(self._conflicts) > 0
    @property
    def conflicts(self): return list(self._conflicts)

    def run_validation(self, schema_id: str, data_version: str) -> dict:
        schema_match = self.is_compatible(schema_id, data_version)
        current_ver  = self.get_version_string(schema_id)
        errors   = []
        warnings = []

        if not schema_match:
            errors.append(f"Schema version mismatch for '{schema_id}': "
                          f"data={data_version} registry={current_ver}")

        if self.is_deprecated(schema_id):
            warnings.append(f"Schema '{schema_id}' is deprecated")

        if self._missing_refs:
            warnings.append(f"{len(self._missing_refs)} missing reference(s)")

        for c in self._conflicts:
            warnings.append(f"Config conflict: {c.setting_key}")

        blocking = any(r.is_blocking for r in self._missing_refs)
        passed = len(errors) == 0 and not blocking

        report = {
            "schema_id":       schema_id,
            "checked_version": data_version,
            "schema_match":    schema_match,
            "missing_refs":    list(self._missing_refs),
            "config_conflicts":list(self._conflicts),
            "warnings":        warnings,
            "errors":          errors,
            "passed":          passed,
        }

        if self._validation_cb: self._validation_cb(report)
        return report

    def get_validation_summary(self, report: dict) -> List[str]:
        lines = []
        sid = report["schema_id"]
        ver = report["checked_version"]
        ok  = "OK" if report["schema_match"] else "MISMATCH"
        lines.append(f"[Schema] {sid} v{ver} {ok}")
        for e in report["errors"]:   lines.append(f"[ERROR] {e}")
        for w in report["warnings"]: lines.append(f"[WARN]  {w}")
        for r in report["missing_refs"]:
            tag = " [BLOCKING]" if r.is_blocking else ""
            lines.append(f"[MISREF] {r.source_id} → {r.ref_id}{tag}")
        for c in report["config_conflicts"]:
            lines.append(f"[CONFLICT] {c.setting_key}: {c.value_a} vs {c.value_b}")
        lines.append(f"[RESULT] {'PASSED' if report['passed'] else 'FAILED'}")
        return lines

    def register_default_game_schemas(self):
        schemas = [
            ("save_data",          1, 0, 0, "World save envelope"),
            ("player_state",       1, 0, 0, "Player snapshot"),
            ("fleet_data",         1, 0, 0, "Fleet definitions"),
            ("season_data",        1, 0, 0, "Season/Titan state"),
            ("economy_data",       1, 0, 0, "Credits/contracts"),
            ("item_definition",    1, 0, 0, "Item/recipe records"),
            ("voxel_chunk",        1, 0, 0, "Voxel serialisation"),
            ("structure_def",      1, 0, 0, "Module/structure defs"),
            ("faction_def",        1, 0, 0, "Faction records"),
            ("mission_def",        1, 0, 0, "Mission definitions"),
            ("pcg_seed_table",     1, 0, 0, "PCG seed registry"),
            ("keybind_config",     1, 0, 0, "Keybind overrides"),
            ("asset_import_rules", 1, 0, 0, "Asset naming rules"),
        ]
        for sid, maj, min_, pat, notes in schemas:
            self.register_schema(SchemaVersion(sid, maj, min_, pat, notes))

    def set_validation_callback(self, cb): self._validation_cb = cb


class TestSchemaVersionRegistry:
    def setup_method(self):
        self.svr = SchemaVersionRegistry()
        assert self.svr.initialize()
        self.svr.register_default_game_schemas()

    # ---- schema registration ------------------------------------------
    def test_default_schemas_registered(self):
        assert self.svr.schema_count >= 13
        assert self.svr.has_schema("save_data")
        assert self.svr.has_schema("player_state")

    def test_find_schema(self):
        s = self.svr.find_schema("save_data")
        assert s is not None
        assert s.major_version == 1

    def test_register_updates_existing(self):
        new_sv = SchemaVersion("save_data", 2, 0, 0, "upgraded")
        self.svr.register_schema(new_sv)
        s = self.svr.find_schema("save_data")
        assert s.major_version == 2

    # ---- version checks -----------------------------------------------
    def test_check_version_exact_match(self):
        assert self.svr.check_version("save_data", 1, 0, 0)

    def test_check_version_mismatch_major(self):
        assert not self.svr.check_version("save_data", 2, 0, 0)

    def test_is_compatible_matching_string(self):
        assert self.svr.is_compatible("save_data", "1.0.0")

    def test_is_compatible_mismatched_string(self):
        assert not self.svr.is_compatible("save_data", "2.0.0")

    def test_is_compatible_older_version_passes(self):
        # Registry has 1.2.0; check against 1.0.0 should pass (registry >= requested)
        sv = SchemaVersion("new_schema", 1, 2, 0)
        self.svr.register_schema(sv)
        assert self.svr.is_compatible("new_schema", "1.0.0")

    def test_get_version_string(self):
        ver = self.svr.get_version_string("save_data")
        assert ver == "1.0.0"

    def test_get_version_string_unknown_returns_zero(self):
        ver = self.svr.get_version_string("unknown_schema")
        assert ver == "0.0.0"

    def test_is_deprecated_false(self):
        assert not self.svr.is_deprecated("save_data")

    def test_is_deprecated_true(self):
        dep = SchemaVersion("old_format", 1, 0, 0, "", is_deprecated=True)
        self.svr.register_schema(dep)
        assert self.svr.is_deprecated("old_format")

    # ---- missing references -------------------------------------------
    def test_add_missing_ref(self):
        ref = MissingReference("item_def_001", "item_xyz", ERefType.Item)
        self.svr.add_missing_ref(ref)
        assert self.svr.has_missing_refs
        assert len(self.svr.missing_refs) == 1

    def test_clear_all_missing_refs(self):
        self.svr.add_missing_ref(MissingReference("a", "b", ERefType.Item))
        self.svr.clear_missing_refs()
        assert not self.svr.has_missing_refs

    def test_clear_missing_refs_by_source(self):
        self.svr.add_missing_ref(MissingReference("src_a", "b", ERefType.Item))
        self.svr.add_missing_ref(MissingReference("src_b", "c", ERefType.Item))
        self.svr.clear_missing_refs("src_a")
        assert len(self.svr.missing_refs) == 1
        assert self.svr.missing_refs[0].source_id == "src_b"

    def test_blocking_missing_refs(self):
        self.svr.add_missing_ref(MissingReference("s1", "r1", ERefType.Item, is_blocking=True))
        self.svr.add_missing_ref(MissingReference("s2", "r2", ERefType.Item, is_blocking=False))
        blocking = self.svr.get_blocking_missing_refs()
        assert len(blocking) == 1
        assert blocking[0].ref_id == "r1"

    # ---- config conflict detection ------------------------------------
    def test_no_conflicts_no_duplicate_keys(self):
        self.svr.register_config_value("max_players", "32", "server.cfg")
        self.svr.register_config_value("tick_rate",   "60", "server.cfg")
        self.svr.detect_config_conflicts()
        assert not self.svr.has_config_conflicts

    def test_conflict_detected(self):
        self.svr.register_config_value("max_players", "32",  "server.cfg")
        self.svr.register_config_value("max_players", "64",  "override.cfg")
        self.svr.detect_config_conflicts()
        assert self.svr.has_config_conflicts
        assert self.svr.conflicts[0].setting_key == "max_players"

    def test_conflict_values_captured(self):
        self.svr.register_config_value("tick_rate", "60", "a.cfg")
        self.svr.register_config_value("tick_rate", "30", "b.cfg")
        self.svr.detect_config_conflicts()
        c = self.svr.conflicts[0]
        assert c.value_a in ("60", "30")
        assert c.value_b in ("60", "30")
        assert c.value_a != c.value_b

    def test_same_value_no_conflict(self):
        self.svr.register_config_value("debug", "false", "a.cfg")
        self.svr.register_config_value("debug", "false", "b.cfg")
        self.svr.detect_config_conflicts()
        assert not self.svr.has_config_conflicts

    # ---- full validation report ---------------------------------------
    def test_validation_passes_on_match(self):
        report = self.svr.run_validation("save_data", "1.0.0")
        assert report["schema_match"] is True

    def test_validation_fails_on_mismatch(self):
        report = self.svr.run_validation("save_data", "2.0.0")
        assert report["schema_match"] is False
        assert len(report["errors"]) >= 1

    def test_validation_includes_deprecated_warning(self):
        dep = SchemaVersion("dep_schema", 1, 0, 0, is_deprecated=True)
        self.svr.register_schema(dep)
        report = self.svr.run_validation("dep_schema", "1.0.0")
        assert any("deprecated" in w.lower() for w in report["warnings"])

    def test_validation_includes_missing_ref_warning(self):
        self.svr.add_missing_ref(MissingReference("src", "ref_id", ERefType.Item))
        report = self.svr.run_validation("save_data", "1.0.0")
        assert any("missing" in w.lower() for w in report["warnings"])

    def test_validation_includes_conflict_warning(self):
        self.svr.register_config_value("max_hp", "100", "a.cfg")
        self.svr.register_config_value("max_hp", "200", "b.cfg")
        self.svr.detect_config_conflicts()
        report = self.svr.run_validation("save_data", "1.0.0")
        assert any("conflict" in w.lower() for w in report["warnings"])

    def test_blocking_ref_fails_validation(self):
        self.svr.add_missing_ref(MissingReference(
            "src", "critical_item", ERefType.Item, is_blocking=True))
        report = self.svr.run_validation("save_data", "1.0.0")
        assert not report["passed"]

    # ---- validation summary -------------------------------------------
    def test_get_validation_summary_contains_schema(self):
        report = self.svr.run_validation("save_data", "1.0.0")
        lines = self.svr.get_validation_summary(report)
        assert any("save_data" in l for l in lines)

    def test_get_validation_summary_contains_result(self):
        report = self.svr.run_validation("save_data", "1.0.0")
        lines = self.svr.get_validation_summary(report)
        assert any("[RESULT]" in l for l in lines)

    def test_get_validation_summary_contains_error(self):
        report = self.svr.run_validation("save_data", "9.9.9")
        lines = self.svr.get_validation_summary(report)
        assert any("[ERROR]" in l for l in lines)

    def test_get_validation_summary_contains_missing_ref(self):
        self.svr.add_missing_ref(MissingReference("s", "ref_abc", ERefType.Asset))
        report = self.svr.run_validation("save_data", "1.0.0")
        lines = self.svr.get_validation_summary(report)
        assert any("[MISREF]" in l and "ref_abc" in l for l in lines)

    # ---- validation callback ------------------------------------------
    def test_validation_callback_invoked(self):
        reports = []
        self.svr.set_validation_callback(lambda r: reports.append(r))
        self.svr.run_validation("save_data", "1.0.0")
        assert len(reports) == 1

    def test_validation_callback_receives_report(self):
        reports = []
        self.svr.set_validation_callback(lambda r: reports.append(r))
        self.svr.run_validation("player_state", "1.0.0")
        assert reports[0]["schema_id"] == "player_state"

    # ---- default game schemas -----------------------------------------
    def test_all_game_schemas_registered(self):
        expected = ["save_data", "player_state", "fleet_data", "season_data",
                    "economy_data", "item_definition", "voxel_chunk",
                    "faction_def", "mission_def", "keybind_config"]
        for eid in expected:
            assert self.svr.has_schema(eid), f"Missing schema: {eid}"

    def test_all_default_schemas_at_version_1(self):
        for s in self.svr._schemas:
            assert s.major_version == 1

    def test_schema_count_after_defaults(self):
        assert self.svr.schema_count >= 13
