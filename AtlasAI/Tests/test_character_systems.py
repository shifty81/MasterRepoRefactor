"""Tests for NovaForge Character System — data definitions and source structure."""

import json
import sys
import unittest
from pathlib import Path

# Repo root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestCharacterDataDefinitions(unittest.TestCase):
    """Validate JSON data definition files for the character system."""

    def _load_json(self, relative_path: str) -> dict:
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing file: {relative_path}")
        return json.loads(full.read_text(encoding="utf-8"))

    # --- Phase 1 data files ---

    def test_default_character_has_id(self):
        data = self._load_json("NovaForge/Data/Definitions/Characters/default_character.character.json")
        self.assertIn("id", data)
        self.assertIsInstance(data["id"], str)

    def test_default_character_has_movement_modes(self):
        data = self._load_json("NovaForge/Data/Definitions/Characters/default_character.character.json")
        self.assertIn("movement_modes", data)
        self.assertIsInstance(data["movement_modes"], list)
        self.assertGreater(len(data["movement_modes"]), 0)

    def test_default_equipment_has_equipment_list(self):
        data = self._load_json("NovaForge/Data/Definitions/Equipment/default_equipment.equipment.json")
        self.assertIn("equipment", data)
        self.assertIsInstance(data["equipment"], list)
        self.assertGreater(len(data["equipment"]), 0)

    def test_default_equipment_items_have_id(self):
        data = self._load_json("NovaForge/Data/Definitions/Equipment/default_equipment.equipment.json")
        for item in data["equipment"]:
            self.assertIn("id", item)

    def test_default_animation_has_states_list(self):
        data = self._load_json("NovaForge/Data/Definitions/Animation/default_animation_states.animation.json")
        self.assertIn("states", data)
        self.assertIsInstance(data["states"], list)
        self.assertGreater(len(data["states"]), 0)

    # --- Phase 2 data files ---

    def test_character_state_defaults_has_id(self):
        data = self._load_json("NovaForge/Data/Definitions/Characters/character_state_defaults.character.json")
        self.assertIn("id", data)

    def test_character_state_defaults_has_sockets(self):
        data = self._load_json("NovaForge/Data/Definitions/Characters/character_state_defaults.character.json")
        self.assertIn("sockets", data)
        self.assertIsInstance(data["sockets"], list)

    def test_character_layers_has_layers(self):
        data = self._load_json("NovaForge/Data/Definitions/Animation/character_layers.animation.json")
        self.assertIn("layers", data)
        self.assertIsInstance(data["layers"], list)

    def test_ik_defaults_has_targets(self):
        data = self._load_json("NovaForge/Data/Definitions/IK/ik_defaults.ik.json")
        self.assertIn("targets", data)
        self.assertIsInstance(data["targets"], list)

    def test_ik_defaults_targets_have_type(self):
        data = self._load_json("NovaForge/Data/Definitions/IK/ik_defaults.ik.json")
        for target in data["targets"]:
            self.assertIn("type", target)

    def test_mining_tool_contract_has_tool_id(self):
        data = self._load_json("NovaForge/Data/Definitions/Tools/mining_tool_contract.tool.json")
        self.assertIn("tool_id", data)

    def test_mining_tool_contract_has_use_animation(self):
        data = self._load_json("NovaForge/Data/Definitions/Tools/mining_tool_contract.tool.json")
        self.assertIn("use_animation", data)


class TestCharacterSourceFilesExist(unittest.TestCase):
    """Verify the expected character source files are present in the repo."""

    def _check(self, relative_path: str):
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing source file: {relative_path}")

    def test_character_types_header(self):
        self._check("NovaForge/Gameplay/Characters/CharacterTypes.h")

    def test_character_system_header(self):
        self._check("NovaForge/Gameplay/Characters/CharacterSystem.h")

    def test_character_system_source(self):
        self._check("NovaForge/Gameplay/Characters/CharacterSystem.cpp")

    def test_character_controller_shell_header(self):
        self._check("NovaForge/Gameplay/Characters/CharacterControllerShell.h")

    def test_animation_controller_header(self):
        self._check("NovaForge/Gameplay/Characters/Animation/AnimationController.h")

    def test_animation_controller_source(self):
        self._check("NovaForge/Gameplay/Characters/Animation/AnimationController.cpp")

    def test_equipment_system_source(self):
        self._check("NovaForge/Gameplay/Characters/Equipment/EquipmentSystem.cpp")

    def test_mech_possession_system_source(self):
        self._check("NovaForge/Gameplay/Characters/Mech/MechPossessionSystem.cpp")

    def test_character_state_authority_header(self):
        self._check("NovaForge/Gameplay/Characters/Core/CharacterStateAuthority.h")

    def test_character_state_authority_source(self):
        self._check("NovaForge/Gameplay/Characters/Core/CharacterStateAuthority.cpp")

    def test_character_transition_rules_source(self):
        self._check("NovaForge/Gameplay/Characters/Core/CharacterTransitionRules.cpp")

    def test_animation_layer_system_source(self):
        self._check("NovaForge/Gameplay/Characters/Animation/AnimationLayerSystem.cpp")

    def test_ik_system_source(self):
        self._check("NovaForge/Gameplay/Characters/IK/IKSystem.cpp")

    def test_fps_presentation_system_source(self):
        self._check("NovaForge/Gameplay/Characters/FPS/FPSPresentationSystem.cpp")

    def test_character_editor_system_source(self):
        self._check("NovaForge/Gameplay/Characters/Editor/CharacterEditorSystem.cpp")

    def test_tool_interaction_shell_source(self):
        self._check("NovaForge/Gameplay/Characters/Tools/ToolInteractionShell.cpp")


class TestCharacterDocsExist(unittest.TestCase):
    """Verify character documentation files are present."""

    def test_character_system_roadmap(self):
        path = REPO_ROOT / "NovaForge/Docs/Characters/Character_System_Roadmap.md"
        self.assertTrue(path.exists(), "Missing Character_System_Roadmap.md")

    def test_character_phase2_roadmap(self):
        path = REPO_ROOT / "NovaForge/Docs/Characters/Character_Phase2_Roadmap.md"
        self.assertTrue(path.exists(), "Missing Character_Phase2_Roadmap.md")

    def test_character_standards(self):
        path = REPO_ROOT / "NovaForge/Docs/Characters/Character_Standards.md"
        self.assertTrue(path.exists(), "Missing Character_Standards.md")


if __name__ == "__main__":
    unittest.main()
