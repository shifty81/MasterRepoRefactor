"""Phase 26D — Tests for PhysicsBodyRegistry.h and PhysicsBodyLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    PhysicsBodyLoader,
    PhysicsBodyManifest,
    PhysicsMaterialDef,
    ColliderDef,
)

TMP_DIR = Path("/tmp/test_phase26d")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# PhysicsBodyRegistry.h
# ---------------------------------------------------------------------------

def _read_registry() -> str:
    return (SCENE_DIR / "PhysicsBodyRegistry.h").read_text()


class TestPhysicsBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "PhysicsBodyRegistry.h").exists())


class TestPhysicsBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("PhysicsBodyRegistry", _read_registry())

    def test_body_state_enum(self):
        self.assertIn("BodyState", _read_registry())

    def test_body_type_enum(self):
        self.assertIn("BodyType", _read_registry())

    def test_collider_shape_enum(self):
        self.assertIn("ColliderShape", _read_registry())

    def test_physics_layer_enum(self):
        self.assertIn("PhysicsLayer", _read_registry())

    def test_physics_material_def_struct(self):
        self.assertIn("PhysicsMaterialDef", _read_registry())

    def test_collider_def_struct(self):
        self.assertIn("ColliderDef", _read_registry())

    def test_body_record_struct(self):
        self.assertIn("BodyRecord", _read_registry())

    def test_constraint_manifest_struct(self):
        self.assertIn("ConstraintManifest", _read_registry())


class TestPhysicsBodyRegistryAPI(unittest.TestCase):
    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_body_type(self):
        self.assertIn("SetBodyType", _read_registry())

    def test_set_body_layer(self):
        self.assertIn("SetBodyLayer", _read_registry())

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_registry())

    def test_get_bodies_by_scene(self):
        self.assertIn("GetBodiesByScene", _read_registry())

    def test_add_collider(self):
        self.assertIn("AddCollider", _read_registry())

    def test_remove_collider(self):
        self.assertIn("RemoveCollider", _read_registry())

    def test_register_material(self):
        self.assertIn("RegisterMaterial", _read_registry())

    def test_register_constraint(self):
        self.assertIn("RegisterConstraint", _read_registry())

    def test_activate_body(self):
        self.assertIn("ActivateBody", _read_registry())

    def test_deactivate_body(self):
        self.assertIn("DeactivateBody", _read_registry())

    def test_activate_all_in_scene(self):
        self.assertIn("ActivateAllInScene", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear", _read_registry())


# ---------------------------------------------------------------------------
# ColliderDef dataclass
# ---------------------------------------------------------------------------

class TestColliderDefDataclass(unittest.TestCase):
    def test_collider_id_field(self):
        c = ColliderDef(collider_id="c001")
        self.assertEqual(c.collider_id, "c001")

    def test_default_shape(self):
        c = ColliderDef(collider_id="c001")
        self.assertEqual(c.shape, "Box")

    def test_default_extent(self):
        c = ColliderDef(collider_id="c001")
        self.assertAlmostEqual(c.extent_x, 0.5)

    def test_offset_property(self):
        c = ColliderDef(collider_id="c001",
                         offset_x=1.0, offset_y=2.0, offset_z=3.0)
        self.assertEqual(c.offset, (1.0, 2.0, 3.0))

    def test_default_is_trigger_false(self):
        c = ColliderDef(collider_id="c001")
        self.assertFalse(c.is_trigger)

    def test_default_enabled_true(self):
        c = ColliderDef(collider_id="c001")
        self.assertTrue(c.enabled)


# ---------------------------------------------------------------------------
# PhysicsMaterialDef dataclass
# ---------------------------------------------------------------------------

class TestPhysicsMaterialDefDataclass(unittest.TestCase):
    def test_material_id_field(self):
        m = PhysicsMaterialDef(material_id="m001", name="Rock")
        self.assertEqual(m.material_id, "m001")

    def test_name_field(self):
        m = PhysicsMaterialDef(material_id="m001", name="Rock")
        self.assertEqual(m.name, "Rock")

    def test_default_static_friction(self):
        m = PhysicsMaterialDef(material_id="m001", name="Rock")
        self.assertAlmostEqual(m.static_friction, 0.6)

    def test_friction_ratio_realistic(self):
        m = PhysicsMaterialDef(material_id="m001", name="Rock",
                                 static_friction=0.6, dynamic_friction=0.4)
        self.assertLessEqual(m.friction_ratio, 1.0)

    def test_friction_ratio_zero_static(self):
        m = PhysicsMaterialDef(material_id="m001", name="Ice",
                                 static_friction=0.0, dynamic_friction=0.0)
        self.assertAlmostEqual(m.friction_ratio, 0.0)


# ---------------------------------------------------------------------------
# PhysicsBodyManifest dataclass
# ---------------------------------------------------------------------------

class TestPhysicsBodyManifestDataclass(unittest.TestCase):
    def test_body_id_field(self):
        m = PhysicsBodyManifest("b001", "Crate")
        self.assertEqual(m.body_id, "b001")

    def test_name_field(self):
        m = PhysicsBodyManifest("b001", "Crate")
        self.assertEqual(m.name, "Crate")

    def test_default_body_type(self):
        m = PhysicsBodyManifest("b001", "Crate")
        self.assertEqual(m.body_type, "Dynamic")

    def test_collider_count_empty(self):
        m = PhysicsBodyManifest("b001", "Crate")
        self.assertEqual(m.collider_count, 0)

    def test_position_property(self):
        m = PhysicsBodyManifest("b001", "Crate",
                                  pos_x=1.0, pos_y=2.0, pos_z=3.0)
        self.assertEqual(m.position, (1.0, 2.0, 3.0))

    def test_is_dynamic_true(self):
        m = PhysicsBodyManifest("b001", "Crate", body_type="Dynamic")
        self.assertTrue(m.is_dynamic)

    def test_is_dynamic_false_for_static(self):
        m = PhysicsBodyManifest("b001", "Wall", body_type="Static")
        self.assertFalse(m.is_dynamic)

    def test_is_active_false_by_default(self):
        m = PhysicsBodyManifest("b001", "Crate")
        self.assertFalse(m.is_active)

    def test_get_collider_none(self):
        m = PhysicsBodyManifest("b001", "Crate")
        self.assertIsNone(m.get_collider("no_such"))


# ---------------------------------------------------------------------------
# PhysicsBodyLoader — registration
# ---------------------------------------------------------------------------

class TestPhysicsBodyLoaderRegistration(unittest.TestCase):
    def setUp(self):
        self.loader = PhysicsBodyLoader()

    def test_register_returns_manifest(self):
        m = self.loader.register("b001", "Crate")
        self.assertIsInstance(m, PhysicsBodyManifest)

    def test_register_name(self):
        m = self.loader.register("b001", "Crate")
        self.assertEqual(m.name, "Crate")

    def test_registered_count(self):
        self.loader.register("b001", "Crate")
        self.loader.register("b002", "Barrel")
        self.assertEqual(self.loader.get_registered_count(), 2)

    def test_get_manifest_by_id(self):
        self.loader.register("b001", "Crate")
        m = self.loader.get_manifest("b001")
        self.assertIsNotNone(m)
        self.assertEqual(m.name, "Crate")

    def test_get_manifest_missing_returns_none(self):
        self.assertIsNone(self.loader.get_manifest("ghost"))

    def test_get_all_body_ids(self):
        self.loader.register("b001", "Crate")
        self.assertIn("b001", self.loader.get_all_body_ids())

    def test_unregister(self):
        self.loader.register("b001", "Crate")
        self.assertTrue(self.loader.unregister("b001"))
        self.assertEqual(self.loader.get_registered_count(), 0)

    def test_unregister_missing_returns_false(self):
        self.assertFalse(self.loader.unregister("ghost"))

    def test_get_bodies_by_scene(self):
        self.loader.register("b001", "Crate", scene_id="scene_A")
        self.loader.register("b002", "Wall", scene_id="scene_B")
        ids = self.loader.get_bodies_by_scene("scene_A")
        self.assertIn("b001", ids)
        self.assertEqual(len(ids), 1)

    def test_get_bodies_by_type(self):
        self.loader.register("b001", "Crate", body_type="Dynamic")
        self.loader.register("b002", "Wall", body_type="Static")
        ids = self.loader.get_bodies_by_type("Static")
        self.assertIn("b002", ids)
        self.assertEqual(len(ids), 1)

    def test_register_from_dict(self):
        data = {"body_id": "b001", "name": "Crate", "body_type": "Dynamic"}
        m = self.loader.register_from_dict(data)
        self.assertIsNotNone(m)
        self.assertEqual(m.body_id, "b001")

    def test_register_from_dict_with_colliders(self):
        data = {
            "body_id": "b001",
            "name": "Crate",
            "colliders": [
                {"collider_id": "c001", "shape": "Box"}
            ],
        }
        m = self.loader.register_from_dict(data)
        self.assertIsNotNone(m)
        self.assertEqual(m.collider_count, 1)

    def test_register_from_dict_missing_key_returns_none(self):
        self.assertIsNone(self.loader.register_from_dict({"name": "oops"}))

    def test_clear(self):
        self.loader.register("b001", "Crate")
        self.loader.clear()
        self.assertEqual(self.loader.get_registered_count(), 0)


# ---------------------------------------------------------------------------
# PhysicsBodyLoader — activation
# ---------------------------------------------------------------------------

class TestPhysicsBodyLoaderActivation(unittest.TestCase):
    def setUp(self):
        self.loader = PhysicsBodyLoader()
        self.loader.register("b001", "Crate", scene_id="s1", always_active=False)
        self.loader.register("b002", "Platform", scene_id="s1", always_active=True)
        self.loader.register("b003", "Wall", scene_id="s2")

    def test_activate(self):
        self.assertTrue(self.loader.activate("b001"))
        self.assertTrue(self.loader.is_active("b001"))

    def test_activate_unknown_returns_false(self):
        self.assertFalse(self.loader.activate("ghost"))

    def test_deactivate(self):
        self.loader.activate("b001")
        self.assertTrue(self.loader.deactivate("b001"))
        self.assertFalse(self.loader.is_active("b001"))

    def test_deactivate_not_active_returns_false(self):
        self.assertFalse(self.loader.deactivate("b001"))

    def test_get_active_count(self):
        self.loader.activate("b001")
        self.assertEqual(self.loader.get_active_count(), 1)

    def test_get_active_ids(self):
        self.loader.activate("b001")
        self.assertIn("b001", self.loader.get_active_ids())

    def test_activate_all_in_scene(self):
        count = self.loader.activate_all_in_scene("s1")
        self.assertEqual(count, 2)

    def test_deactivate_all_in_scene(self):
        self.loader.activate_all_in_scene("s1")
        deactivated = self.loader.deactivate_all_in_scene("s1")
        self.assertEqual(deactivated, 2)
        self.assertFalse(self.loader.is_active("b001"))

    def test_activate_always_active(self):
        count = self.loader.activate_always_active()
        self.assertEqual(count, 1)
        self.assertTrue(self.loader.is_active("b002"))

    def test_body_state_after_activate(self):
        self.loader.activate("b001")
        m = self.loader.get_manifest("b001")
        self.assertEqual(m.body_state, "Active")


# ---------------------------------------------------------------------------
# PhysicsBodyLoader — colliders
# ---------------------------------------------------------------------------

class TestPhysicsBodyLoaderColliders(unittest.TestCase):
    def setUp(self):
        self.loader = PhysicsBodyLoader()
        self.loader.register("b001", "Crate")

    def test_add_collider_returns_collider(self):
        c = self.loader.add_collider("b001", shape="Box")
        self.assertIsInstance(c, ColliderDef)

    def test_collider_shape_set(self):
        c = self.loader.add_collider("b001", shape="Sphere")
        self.assertEqual(c.shape, "Sphere")

    def test_get_collider_count(self):
        self.loader.add_collider("b001")
        self.loader.add_collider("b001")
        self.assertEqual(self.loader.get_collider_count("b001"), 2)

    def test_remove_collider(self):
        c = self.loader.add_collider("b001")
        self.assertTrue(self.loader.remove_collider("b001", c.collider_id))
        self.assertEqual(self.loader.get_collider_count("b001"), 0)

    def test_add_collider_unknown_body_returns_none(self):
        result = self.loader.add_collider("ghost")
        self.assertIsNone(result)

    def test_collider_accessible_via_manifest(self):
        c = self.loader.add_collider("b001")
        m = self.loader.get_manifest("b001")
        found = m.get_collider(c.collider_id)
        self.assertIsNotNone(found)


# ---------------------------------------------------------------------------
# PhysicsBodyLoader — materials
# ---------------------------------------------------------------------------

class TestPhysicsBodyLoaderMaterials(unittest.TestCase):
    def setUp(self):
        self.loader = PhysicsBodyLoader()

    def test_register_material_returns_material(self):
        m = self.loader.register_material("Rock")
        self.assertIsInstance(m, PhysicsMaterialDef)

    def test_material_name(self):
        m = self.loader.register_material("Rock")
        self.assertEqual(m.name, "Rock")

    def test_material_id_unique(self):
        m1 = self.loader.register_material("Rock")
        m2 = self.loader.register_material("Ice")
        self.assertNotEqual(m1.material_id, m2.material_id)

    def test_get_material_count(self):
        self.loader.register_material("Rock")
        self.loader.register_material("Ice")
        self.assertEqual(self.loader.get_material_count(), 2)

    def test_get_material_by_id(self):
        m = self.loader.register_material("Rock")
        fetched = self.loader.get_material(m.material_id)
        self.assertIsNotNone(fetched)

    def test_get_all_material_ids(self):
        m = self.loader.register_material("Rock")
        self.assertIn(m.material_id, self.loader.get_all_material_ids())

    def test_unregister_material(self):
        m = self.loader.register_material("Rock")
        self.assertTrue(self.loader.unregister_material(m.material_id))
        self.assertEqual(self.loader.get_material_count(), 0)


# ---------------------------------------------------------------------------
# PhysicsBodyLoader — persistence
# ---------------------------------------------------------------------------

class TestPhysicsBodyLoaderPersistence(unittest.TestCase):
    def setUp(self):
        self.loader = PhysicsBodyLoader()
        self.loader.register("b001", "Crate", scene_id="scene_01", body_type="Dynamic")
        self.loader.add_collider("b001", shape="Box")
        self.loader.register_material("Rock", static_friction=0.7)

    def test_save_registry(self):
        out = str(TMP_DIR / "physics_registry.json")
        self.assertTrue(self.loader.save_registry(out))
        self.assertTrue(Path(out).exists())

    def test_save_registry_content(self):
        out = str(TMP_DIR / "physics_registry2.json")
        self.loader.save_registry(out)
        data = json.loads(Path(out).read_text())
        self.assertIn("bodies", data)
        self.assertIn("materials", data)
        self.assertEqual(data["bodies"][0]["body_id"], "b001")

    def test_load_registry(self):
        out = str(TMP_DIR / "physics_registry3.json")
        self.loader.save_registry(out)
        loader2 = PhysicsBodyLoader()
        count = loader2.load_registry(out)
        self.assertEqual(count, 1)
        self.assertIsNotNone(loader2.get_manifest("b001"))

    def test_load_registry_missing_file_returns_zero(self):
        loader2 = PhysicsBodyLoader()
        count = loader2.load_registry("/tmp/no_such_physics_file.json")
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
