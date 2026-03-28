"""Tests for AtlasAI core/legacy_adapter.py — MasterRepoLegacyAdapter."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

# Make core importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "AIEngine" / "AtlasAIEngine"))

from core.legacy_adapter import (
    LEGACY_ACTION_MAP,
    LEGACY_DEFAULT_ROOTS,
    LegacyManifest,
    MasterRepoLegacyAdapter,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MINIMAL_MANIFEST: dict = {
    "project": {
        "id": "masterrepo-legacy",
        "displayName": "MasterRepo (Legacy)",
        "version": "0.2.0",
        "description": "Test manifest",
        "repoRoot": "../../",
    },
    "capabilities": {"supportsAISession": True},
    "buildTargets": [
        {"name": "AtlasEditor", "displayName": "Atlas Editor",
         "configuration": "Debug", "platform": "Win64"},
    ],
    "bridge": {"host": "localhost", "restPort": 57100, "timeoutSeconds": 30},
    "legacyLayout": {
        "enabled": True,
        "sourceRoot": "src",
        "testsRoot": "tests",
        "docsRoot": "docs",
        "legacyNamingPrefix": "Arbiter",
    },
    "repoPaths": {
        "sourceRoot": "Atlas", "gameRoot": "NovaForge",
        "toolingRoot": "AtlasAI", "sharedRoot": "Shared",
        "docsRoot": "Docs", "dataRoot": "NovaForge/Data",
        "contentRoot": "NovaForge/Content", "scriptsRoot": "Scripts",
        "testsRoot": "Tests",
    },
    "safetySettings": {
        "requireDryRunByDefault": True,
        "requireSessionTokenForWrites": True,
        "allowedToolActions": [
            "ValidateData", "RunPCGPreview", "OpenScene",
            "FocusEntity", "RegenerateSchemas",
        ],
        "writeableRoots": ["NovaForge/Data"],
    },
}


def _write_manifest(root: Path, data: dict | None = None) -> Path:
    """Write manifest JSON to root/Shared/ProjectManifests/masterrepo.legacy.project.json."""
    manifest_dir = root / "Shared" / "ProjectManifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "masterrepo.legacy.project.json"
    manifest_path.write_text(json.dumps(data or MINIMAL_MANIFEST), encoding="utf-8")
    return manifest_path


# ---------------------------------------------------------------------------
# LegacyManifest tests
# ---------------------------------------------------------------------------

class TestLegacyManifestDefaults(unittest.TestCase):
    """Empty dict → sensible defaults."""

    def setUp(self) -> None:
        self.manifest = LegacyManifest({})

    def test_project_id_default(self):
        self.assertEqual(self.manifest.project_id, "masterrepo-legacy")

    def test_display_name_default(self):
        self.assertIn("Legacy", self.manifest.display_name)

    def test_version_default(self):
        self.assertEqual(self.manifest.version, "0.1.0")

    def test_legacy_enabled_default(self):
        self.assertFalse(self.manifest.legacy_enabled)

    def test_naming_prefix_default(self):
        self.assertEqual(self.manifest.legacy_naming_prefix, "Arbiter")

    def test_bridge_host_default(self):
        self.assertEqual(self.manifest.bridge_host, "localhost")

    def test_rest_port_default(self):
        self.assertEqual(self.manifest.rest_port, 57100)

    def test_require_dry_run_default(self):
        self.assertTrue(self.manifest.require_dry_run)


class TestLegacyManifestFromData(unittest.TestCase):
    """Loaded from MINIMAL_MANIFEST."""

    def setUp(self) -> None:
        self.manifest = LegacyManifest(MINIMAL_MANIFEST)

    def test_project_id_loaded(self):
        self.assertEqual(self.manifest.project_id, "masterrepo-legacy")

    def test_version_loaded(self):
        self.assertEqual(self.manifest.version, "0.2.0")

    def test_legacy_enabled_true(self):
        self.assertTrue(self.manifest.legacy_enabled)

    def test_legacy_source_root(self):
        self.assertEqual(self.manifest.legacy_source_root, "src")

    def test_legacy_tests_root(self):
        self.assertEqual(self.manifest.legacy_tests_root, "tests")

    def test_legacy_docs_root(self):
        self.assertEqual(self.manifest.legacy_docs_root, "docs")

    def test_allowed_tool_actions(self):
        actions = self.manifest.allowed_tool_actions
        self.assertIn("ValidateData", actions)
        self.assertIn("OpenScene", actions)

    def test_to_dict_has_project_id(self):
        d = self.manifest.to_dict()
        self.assertEqual(d["project_id"], "masterrepo-legacy")

    def test_to_dict_has_legacy_enabled(self):
        d = self.manifest.to_dict()
        self.assertTrue(d["legacy_enabled"])


# ---------------------------------------------------------------------------
# MasterRepoLegacyAdapter tests
# ---------------------------------------------------------------------------

class TestLegacyAdapterManifestLoading(unittest.TestCase):
    def test_loads_manifest_from_repo_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_manifest(root)
            adapter = MasterRepoLegacyAdapter(root)
            self.assertEqual(adapter.manifest.version, "0.2.0")

    def test_missing_manifest_uses_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            # No manifest written → adapter should still construct with defaults
            adapter = MasterRepoLegacyAdapter(tmp)
            self.assertIsNotNone(adapter.manifest)
            self.assertEqual(adapter.manifest.project_id, "masterrepo-legacy")

    def test_invalid_json_uses_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_dir = root / "Shared" / "ProjectManifests"
            manifest_dir.mkdir(parents=True, exist_ok=True)
            (manifest_dir / "masterrepo.legacy.project.json").write_text(
                "NOT JSON", encoding="utf-8"
            )
            adapter = MasterRepoLegacyAdapter(root)
            self.assertIsNotNone(adapter.manifest)


class TestLegacyAdapterLayoutDetection(unittest.TestCase):
    def test_is_legacy_when_manifest_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_manifest(root)
            adapter = MasterRepoLegacyAdapter(root)
            self.assertTrue(adapter.is_legacy_layout())

    def test_is_legacy_when_src_dir_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # No manifest, but src/ dir exists
            (root / "src").mkdir()
            adapter = MasterRepoLegacyAdapter(root)
            self.assertTrue(adapter.is_legacy_layout())

    def test_not_legacy_when_neither(self):
        with tempfile.TemporaryDirectory() as tmp:
            # No manifest, no src/ dir
            data = {**MINIMAL_MANIFEST}
            data["legacyLayout"] = {**MINIMAL_MANIFEST["legacyLayout"], "enabled": False}
            root = Path(tmp)
            _write_manifest(root, data)
            adapter = MasterRepoLegacyAdapter(root)
            # enabled=False and no src/ dir
            self.assertFalse(adapter.is_legacy_layout())


class TestLegacyAdapterProjectInfo(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        root = Path(self.tmp)
        _write_manifest(root)
        self.adapter = MasterRepoLegacyAdapter(root)

    def test_get_project_info_has_id(self):
        info = self.adapter.get_project_info()
        self.assertEqual(info["id"], "masterrepo-legacy")

    def test_get_project_info_has_display_name(self):
        info = self.adapter.get_project_info()
        self.assertIn("displayName", info)

    def test_get_project_info_is_legacy_true(self):
        info = self.adapter.get_project_info()
        self.assertTrue(info["isLegacy"])

    def test_get_project_info_has_naming_prefix(self):
        info = self.adapter.get_project_info()
        self.assertEqual(info["namingPrefix"], "Arbiter")


class TestLegacyAdapterActionTranslation(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        root = Path(self.tmp)
        _write_manifest(root)
        self.adapter = MasterRepoLegacyAdapter(root)

    def test_translate_exact_legacy_name(self):
        self.assertEqual(
            self.adapter.translate_action("Arbiter.ValidateData"), "ValidateData"
        )

    def test_translate_all_legacy_map_entries(self):
        for legacy, modern in LEGACY_ACTION_MAP.items():
            self.assertEqual(self.adapter.translate_action(legacy), modern)

    def test_translate_dynamic_prefix(self):
        self.assertEqual(
            self.adapter.translate_action("Arbiter.SomeNewAction"), "SomeNewAction"
        )

    def test_no_translation_needed(self):
        self.assertEqual(
            self.adapter.translate_action("ValidateData"), "ValidateData"
        )

    def test_is_action_allowed_modern_name(self):
        self.assertTrue(self.adapter.is_action_allowed("ValidateData"))

    def test_is_action_allowed_legacy_name(self):
        self.assertTrue(self.adapter.is_action_allowed("Arbiter.ValidateData"))

    def test_is_action_not_allowed(self):
        self.assertFalse(self.adapter.is_action_allowed("DeleteEverything"))

    def test_requires_dry_run_true(self):
        self.assertTrue(self.adapter.requires_dry_run())


class TestLegacyAdapterSearchRoots(unittest.TestCase):
    def test_fallback_to_defaults_when_no_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_manifest(root)
            adapter = MasterRepoLegacyAdapter(root)
            roots = adapter.get_search_roots()
            self.assertIsInstance(roots, list)
            # Falls back to defaults since no dirs exist
            self.assertEqual(roots, LEGACY_DEFAULT_ROOTS)

    def test_returns_existing_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_manifest(root)
            (root / "src").mkdir()
            (root / "docs").mkdir()
            adapter = MasterRepoLegacyAdapter(root)
            roots = adapter.get_search_roots()
            paths = [r["path"] for r in roots]
            self.assertIn("src", paths)
            self.assertIn("docs", paths)

    def test_root_entries_have_required_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_manifest(root)
            (root / "src").mkdir()
            adapter = MasterRepoLegacyAdapter(root)
            for r in adapter.get_search_roots():
                self.assertIn("label", r)
                self.assertIn("path",  r)
                self.assertIn("kind",  r)


if __name__ == "__main__":
    unittest.main()
