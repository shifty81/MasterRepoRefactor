"""Tests for Atlas Editor Commands and Validation systems."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestCommandSourceFilesExist(unittest.TestCase):
    """Verify command system source files are present."""

    def _check(self, relative_path: str):
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing source file: {relative_path}")

    # CommandTypes
    def test_command_types_header(self):
        self._check("Atlas/Editor/Commands/CommandTypes.h")

    # CommandStack
    def test_command_stack_header(self):
        self._check("Atlas/Editor/Commands/CommandStack.h")

    def test_command_stack_source(self):
        self._check("Atlas/Editor/Commands/CommandStack.cpp")

    # TransformCommand
    def test_transform_command_header(self):
        self._check("Atlas/Editor/Commands/TransformCommand.h")

    def test_transform_command_source(self):
        self._check("Atlas/Editor/Commands/TransformCommand.cpp")

    # PropertyEditCommand
    def test_property_edit_command_header(self):
        self._check("Atlas/Editor/Commands/PropertyEditCommand.h")

    def test_property_edit_command_source(self):
        self._check("Atlas/Editor/Commands/PropertyEditCommand.cpp")

    # VoxelEditCommand
    def test_voxel_edit_command_header(self):
        self._check("Atlas/Editor/Commands/VoxelEditCommand.h")

    def test_voxel_edit_command_source(self):
        self._check("Atlas/Editor/Commands/VoxelEditCommand.cpp")


class TestCommandHeaderContent(unittest.TestCase):
    """Verify command headers contain expected declarations."""

    def _read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def test_command_types_defines_icommand(self):
        content = self._read("Atlas/Editor/Commands/CommandTypes.h")
        self.assertIn("ICommand", content)

    def test_command_types_defines_execute(self):
        content = self._read("Atlas/Editor/Commands/CommandTypes.h")
        self.assertIn("Execute", content)

    def test_command_types_defines_undo(self):
        content = self._read("Atlas/Editor/Commands/CommandTypes.h")
        self.assertIn("Undo", content)

    def test_command_types_defines_get_description(self):
        content = self._read("Atlas/Editor/Commands/CommandTypes.h")
        self.assertIn("GetDescription", content)

    def test_command_stack_has_submit(self):
        content = self._read("Atlas/Editor/Commands/CommandStack.h")
        self.assertIn("Submit", content)

    def test_command_stack_has_undo_redo(self):
        content = self._read("Atlas/Editor/Commands/CommandStack.h")
        self.assertIn("Undo", content)
        self.assertIn("Redo", content)

    def test_transform_command_has_snapshot(self):
        content = self._read("Atlas/Editor/Commands/TransformCommand.h")
        self.assertIn("TransformSnapshot", content)

    def test_voxel_edit_command_has_voxel_coord(self):
        content = self._read("Atlas/Editor/Commands/VoxelEditCommand.h")
        self.assertIn("VoxelCoord", content)

    def test_voxel_edit_command_has_op_enum(self):
        content = self._read("Atlas/Editor/Commands/VoxelEditCommand.h")
        self.assertIn("EVoxelEditOp", content)

    def test_property_edit_command_has_property_path(self):
        content = self._read("Atlas/Editor/Commands/PropertyEditCommand.h")
        self.assertIn("propertyPath", content)


class TestValidationSourceFilesExist(unittest.TestCase):
    """Verify validation toolkit source files are present."""

    def _check(self, relative_path: str):
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing source file: {relative_path}")

    def test_validation_types_header(self):
        self._check("Atlas/Editor/Validation/ValidationTypes.h")

    def test_validation_system_header(self):
        self._check("Atlas/Editor/Validation/ValidationSystem.h")

    def test_validation_system_source(self):
        self._check("Atlas/Editor/Validation/ValidationSystem.cpp")


class TestValidationHeaderContent(unittest.TestCase):
    """Verify validation headers contain expected declarations."""

    def _read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def test_validation_types_has_severity_enum(self):
        content = self._read("Atlas/Editor/Validation/ValidationTypes.h")
        self.assertIn("EValidationSeverity", content)

    def test_validation_types_has_validation_issue(self):
        content = self._read("Atlas/Editor/Validation/ValidationTypes.h")
        self.assertIn("ValidationIssue", content)

    def test_validation_types_has_validation_report(self):
        content = self._read("Atlas/Editor/Validation/ValidationTypes.h")
        self.assertIn("ValidationReport", content)

    def test_validation_types_has_has_errors(self):
        content = self._read("Atlas/Editor/Validation/ValidationTypes.h")
        self.assertIn("HasErrors", content)

    def test_validation_system_has_run_all(self):
        content = self._read("Atlas/Editor/Validation/ValidationSystem.h")
        self.assertIn("RunAll", content)

    def test_validation_system_has_validate_item_references(self):
        content = self._read("Atlas/Editor/Validation/ValidationSystem.h")
        self.assertIn("ValidateItemReferences", content)

    def test_validation_system_has_validate_module_references(self):
        content = self._read("Atlas/Editor/Validation/ValidationSystem.h")
        self.assertIn("ValidateModuleReferences", content)

    def test_validation_system_has_validate_loot_references(self):
        content = self._read("Atlas/Editor/Validation/ValidationSystem.h")
        self.assertIn("ValidateLootReferences", content)


class TestEditorCMakeListsUpdated(unittest.TestCase):
    """Verify Atlas/Editor/CMakeLists.txt includes new command and validation sources."""

    def _cmake(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/CMakeLists.txt").read_text(encoding="utf-8")

    def test_cmake_includes_command_stack(self):
        self.assertIn("CommandStack.cpp", self._cmake())

    def test_cmake_includes_transform_command(self):
        self.assertIn("TransformCommand.cpp", self._cmake())

    def test_cmake_includes_property_edit_command(self):
        self.assertIn("PropertyEditCommand.cpp", self._cmake())

    def test_cmake_includes_voxel_edit_command(self):
        self.assertIn("VoxelEditCommand.cpp", self._cmake())

    def test_cmake_includes_validation_system(self):
        self.assertIn("ValidationSystem.cpp", self._cmake())

    def test_cmake_includes_commands_dir(self):
        self.assertIn("Commands", self._cmake())

    def test_cmake_includes_validation_dir(self):
        self.assertIn("Validation", self._cmake())


if __name__ == "__main__":
    unittest.main()
