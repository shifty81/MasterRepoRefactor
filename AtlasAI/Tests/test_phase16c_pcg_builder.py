"""Phase 16C — PCG & Builder Tooling tests."""
from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestBuilderToolActionIdHeader(unittest.TestCase):
    def setUp(self):
        self.header = REPO_ROOT / "Atlas" / "Editor" / "PCG" / "BuilderToolActionId.h"
        self.content = self.header.read_text()

    def test_file_exists(self):
        self.assertTrue(self.header.exists())

    def test_pragma_once(self):
        self.assertIn("#pragma once", self.content)

    def test_enum_class_defined(self):
        self.assertIn("BuilderToolActionIdV2", self.content)

    def test_preview_mesh_value(self):
        self.assertIn("PreviewMesh", self.content)

    def test_validate_entity_value(self):
        self.assertIn("ValidateEntity", self.content)

    def test_run_diagnostics_value(self):
        self.assertIn("RunDiagnostics", self.content)

    def test_export_pcg_seed_value(self):
        self.assertIn("ExportPCGSeed", self.content)

    def test_namespace(self):
        self.assertIn("Atlas::Editor", self.content)


class TestPreviewMeshGeneratorHeader(unittest.TestCase):
    def setUp(self):
        self.header = REPO_ROOT / "Atlas" / "Engine" / "PCG" / "PreviewMeshGenerator.h"
        self.content = self.header.read_text()

    def test_file_exists(self):
        self.assertTrue(self.header.exists())

    def test_pragma_once(self):
        self.assertIn("#pragma once", self.content)

    def test_generate_method(self):
        self.assertIn("Generate", self.content)

    def test_set_resolution_method(self):
        self.assertIn("SetResolution", self.content)

    def test_lod_member(self):
        self.assertIn("m_lod", self.content)

    def test_namespace(self):
        self.assertIn("Atlas::Engine", self.content)


class TestBuilderEntityValidatorHeader(unittest.TestCase):
    def setUp(self):
        self.header = (
            REPO_ROOT / "Atlas" / "Editor" / "Validation" / "BuilderEntityValidator.h"
        )
        self.content = self.header.read_text()

    def test_file_exists(self):
        self.assertTrue(self.header.exists())

    def test_pragma_once(self):
        self.assertIn("#pragma once", self.content)

    def test_validate_method(self):
        self.assertIn("Validate", self.content)

    def test_set_schema_method(self):
        self.assertIn("SetSchema", self.content)

    def test_schema_path_member(self):
        self.assertIn("m_schemaPath", self.content)

    def test_namespace(self):
        self.assertIn("Atlas::Editor", self.content)


class TestDiagnosticsPanelHeader(unittest.TestCase):
    def setUp(self):
        self.header = REPO_ROOT / "Atlas" / "Editor" / "Panels" / "DiagnosticsPanel.h"
        self.content = self.header.read_text()

    def test_file_exists(self):
        self.assertTrue(self.header.exists())

    def test_pragma_once(self):
        self.assertIn("#pragma once", self.content)

    def test_add_entry_method(self):
        self.assertIn("AddEntry", self.content)

    def test_set_severity_filter_method(self):
        self.assertIn("SetSeverityFilter", self.content)

    def test_clear_method(self):
        self.assertIn("Clear", self.content)

    def test_severity_filter_member(self):
        self.assertIn("m_severityFilter", self.content)

    def test_namespace(self):
        self.assertIn("Atlas::Editor", self.content)


class TestDirectoryStructure(unittest.TestCase):
    def test_editor_pcg_directory_exists(self):
        self.assertTrue((REPO_ROOT / "Atlas" / "Editor" / "PCG").is_dir())

    def test_engine_pcg_directory_exists(self):
        self.assertTrue((REPO_ROOT / "Atlas" / "Engine" / "PCG").is_dir())

    def test_editor_validation_directory_exists(self):
        self.assertTrue((REPO_ROOT / "Atlas" / "Editor" / "Validation").is_dir())


if __name__ == "__main__":
    unittest.main()
