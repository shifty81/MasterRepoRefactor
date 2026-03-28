"""Tests for Phase 16 — Long-Term Vision scaffolding."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestBuildScriptsDir(unittest.TestCase):
    """Scripts/Build/ directory must exist."""

    def test_build_dir_exists(self):
        self.assertTrue(
            (REPO_ROOT / "Scripts/Build").is_dir(),
            "Scripts/Build/ directory is missing",
        )


class TestSmokeTestScriptExists(unittest.TestCase):
    """smoke_test_engine_build.py must exist and contain a main() entry point."""

    SCRIPT = REPO_ROOT / "Scripts/Build/smoke_test_engine_build.py"

    def test_file_exists(self):
        self.assertTrue(self.SCRIPT.exists(), f"Missing: {self.SCRIPT}")

    def test_has_main(self):
        text = self.SCRIPT.read_text(encoding="utf-8")
        self.assertIn("def main(", text, "smoke_test_engine_build.py must define main()")

    def test_has_shebang(self):
        text = self.SCRIPT.read_text(encoding="utf-8")
        self.assertTrue(
            text.startswith("#!/usr/bin/env python3"),
            "Script should start with a python3 shebang",
        )


class TestPhase16DocExists(unittest.TestCase):
    """phase16_long_term_vision.md must exist and cover all four phase sections."""

    DOC = REPO_ROOT / "Docs/Architecture/phase16_long_term_vision.md"

    def test_file_exists(self):
        self.assertTrue(self.DOC.exists(), f"Missing: {self.DOC}")

    def test_has_phase_16a(self):
        self.assertIn("16A", self.DOC.read_text(encoding="utf-8"))

    def test_has_phase_16b(self):
        self.assertIn("16B", self.DOC.read_text(encoding="utf-8"))

    def test_has_phase_16c(self):
        self.assertIn("16C", self.DOC.read_text(encoding="utf-8"))

    def test_has_phase_16d(self):
        self.assertIn("16D", self.DOC.read_text(encoding="utf-8"))


class TestExternalDepsManifestExists(unittest.TestCase):
    """ExternalDepsManifest.h must exist and declare all required constants."""

    HEADER = REPO_ROOT / "Atlas/Engine/Config/ExternalDepsManifest.h"

    def test_file_exists(self):
        self.assertTrue(self.HEADER.exists(), f"Missing: {self.HEADER}")

    def test_has_pragma_once(self):
        self.assertIn("#pragma once", self.HEADER.read_text(encoding="utf-8"))

    def test_has_glm_path(self):
        self.assertIn("GLM_INCLUDE_PATH", self.HEADER.read_text(encoding="utf-8"))

    def test_has_stb_path(self):
        self.assertIn("STB_INCLUDE_PATH", self.HEADER.read_text(encoding="utf-8"))

    def test_has_nlohmann_path(self):
        self.assertIn("NLOHMANN_JSON_INCLUDE_PATH", self.HEADER.read_text(encoding="utf-8"))

    def test_has_tinygltf_path(self):
        self.assertIn("TINYGLTF_INCLUDE_PATH", self.HEADER.read_text(encoding="utf-8"))

    def test_has_tinyobjloader_path(self):
        self.assertIn("TINYOBJLOADER_INCLUDE_PATH", self.HEADER.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
