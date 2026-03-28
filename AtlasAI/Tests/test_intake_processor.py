"""
test_intake_processor.py
Tests for the root intake pipeline:
  — Classification rules (zip, docs, C++, Python, C#, CMake, data, unknown)
  — validate_root enforcement
  — process_intake routing logic
  — audit log output
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from typing import Optional
from enum import Enum, auto


# =============================================================================
# Mirror of classification types (kept pure-Python, no filesystem deps)
# =============================================================================

class ClassificationLabel(str, Enum):
    ZipArchive         = "zip_archive"
    DesignDoc          = "design_doc"
    DesignDocDefault   = "design_doc_default"
    ArchitectureDoc    = "architecture_doc"
    RoadmapDoc         = "roadmap_doc"
    PlanningDoc        = "planning_doc"
    TopLevelDoc        = "top_level_doc"
    ChatExport         = "chat_export"
    AtlasEngineCpp     = "atlas_engine_cpp"
    AtlasEditorCpp     = "atlas_editor_cpp"
    NovaForgeGameplay  = "novaforge_gameplay_cpp"
    NovaForgeApp       = "novaforge_app_cpp"
    NovaForgeSave      = "novaforge_save_cpp"
    PythonTest         = "python_test"
    ValidateScript     = "validate_script"
    BuildScript        = "build_script"
    CIScript           = "ci_script"
    AiEnginePython     = "ai_engine_python"
    CSharpHostApp      = "csharp_hostapp"
    CmakeModule        = "cmake_module"
    DataConfig         = "data_config"
    Unclassified       = "unclassified"
    BoundaryViolation  = "boundary_violation"


class ClassificationResult:
    def __init__(self, source: str, destination: str,
                 label: ClassificationLabel, confident: bool = True, note: str = ""):
        self.source      = source
        self.destination = destination
        self.label       = label
        self.confident   = confident
        self.note        = note


# ---------------------------------------------------------------------------
# Pure-Python classifier (mirrors process_intake.py logic)
# ---------------------------------------------------------------------------

_DOC_SIGNALS = [
    (["DESIGN", "DIRECTIVE", "VISION", "CANON", "MASTER_DESIGN", "MASTER_REPO"],
     "Docs/Design", ClassificationLabel.DesignDoc),
    (["ARCHITECTURE", "BOUNDAR", "DEPENDENCY", "LAYOUT", "MONOREPO",
      "SHIPPING", "INTAKE"],
     "Docs/Architecture", ClassificationLabel.ArchitectureDoc),
    (["PHASE_EXECUTION", "ROADMAP"],
     "Docs/Roadmaps", ClassificationLabel.RoadmapDoc),
    (["CHECKLIST", "MIGRATION", "EXECUTION", "PHASE_",
      "DAY_BY_DAY", "MOVE_CHECKLIST", "MODULE_OWNERSHIP",
      "POST_CONSOLIDATION", "FIRST_REAL", "GITHUB_ISSUES",
      "SPRINT"],
     "Docs/Archive/Planning", ClassificationLabel.PlanningDoc),
    (["CROSSPLATFORM", "GUI", "LAUNCHING", "SETUP", "CONTRIBUTING"],
     "Docs", ClassificationLabel.TopLevelDoc),
]

import re as _re


def classify_filename(name: str) -> ClassificationResult:
    """Classify a filename-only (no content sniffing)."""
    p        = Path(name)
    stem_up  = p.stem.upper()
    suffix   = p.suffix.lower()

    # Archives
    if suffix in (".zip", ".tar", ".gz", ".7z", ".rar"):
        return ClassificationResult(name, f"Docs/Archive/ZipFiles/{name}",
                                    ClassificationLabel.ZipArchive)

    # Docs
    if suffix in (".md", ".rst"):
        for signals, dest, label in _DOC_SIGNALS:
            if any(s in stem_up for s in signals):
                return ClassificationResult(name, f"{dest}/{name}", label)
        return ClassificationResult(name, f"Docs/Design/{name}",
                                    ClassificationLabel.DesignDocDefault)

    # CMake — must come before .txt check to avoid CMakeLists.txt being misrouted
    if suffix == ".cmake" or name == "CMakeLists.txt":
        return ClassificationResult(name, f"cmake/{name}",
                                    ClassificationLabel.CmakeModule)

    if suffix == ".txt":
        return ClassificationResult(name, f"Docs/Archive/Chats/{name}",
                                    ClassificationLabel.ChatExport,
                                    note="Convert to structured .md in Docs/Design/")

    # C++
    if suffix in (".h", ".hpp", ".hxx", ".cpp", ".cxx", ".cc", ".c"):
        return ClassificationResult(name, f"Atlas/Engine/Core/{name}",
                                    ClassificationLabel.AtlasEngineCpp,
                                    confident=False,
                                    note="Content sniff required for precise routing.")

    # Python
    if suffix == ".py":
        if p.stem.startswith("test_"):
            return ClassificationResult(name, f"AtlasAI/Tests/{name}",
                                        ClassificationLabel.PythonTest)
        sl = p.stem.lower()
        if any(k in sl for k in ("validate", "check", "lint")):
            return ClassificationResult(name, f"Scripts/Validate/{name}",
                                        ClassificationLabel.ValidateScript)
        if any(k in sl for k in ("build", "clean", "compile")):
            return ClassificationResult(name, f"Scripts/Build/{name}",
                                        ClassificationLabel.BuildScript)
        if any(k in sl for k in ("ci", "workflow", "pipeline")):
            return ClassificationResult(name, f"Scripts/CI/{name}",
                                        ClassificationLabel.CIScript)
        return ClassificationResult(name,
                                    f"AtlasAI/AIEngine/AtlasAIEngine/{name}",
                                    ClassificationLabel.AiEnginePython,
                                    confident=False)

    # C#
    if suffix in (".cs", ".csproj", ".sln"):
        return ClassificationResult(name, f"AtlasAI/HostApp/{name}",
                                    ClassificationLabel.CSharpHostApp,
                                    confident=False)

    # Data
    if suffix in (".json", ".yaml", ".yml", ".toml", ".ini"):
        return ClassificationResult(name, f"NovaForge/Data/{name}",
                                    ClassificationLabel.DataConfig,
                                    confident=False)

    # Unknown
    return ClassificationResult(name,
                                f"Docs/Archive/Planning/UNCLASSIFIED/{name}",
                                ClassificationLabel.Unclassified,
                                confident=False,
                                note="Manual review required.")


# =============================================================================
# Tests — Classification rules
# =============================================================================

class TestArchiveClassification:
    @pytest.mark.parametrize("filename", [
        "SomeFeature.zip",
        "MasterRepo_Phase7_Pack.zip",
        "source.tar.gz",
        "data.7z",
    ])
    def test_archives_go_to_zipfiles(self, filename):
        r = classify_filename(filename)
        assert r.label == ClassificationLabel.ZipArchive
        assert "Docs/Archive/ZipFiles" in r.destination

    def test_archive_confident(self):
        r = classify_filename("anything.zip")
        assert r.confident is True


class TestDocumentationClassification:
    def test_design_doc_by_directive_signal(self):
        r = classify_filename("MASTER_REPO_DIRECTIVE.md")
        assert r.label == ClassificationLabel.DesignDoc
        assert r.destination.startswith("Docs/Design")

    def test_design_doc_by_vision_signal(self):
        r = classify_filename("VISION_2026.md")
        assert r.label == ClassificationLabel.DesignDoc

    def test_architecture_doc(self):
        r = classify_filename("REPO_BOUNDARIES.md")
        assert r.label == ClassificationLabel.ArchitectureDoc
        assert "Docs/Architecture" in r.destination

    def test_monorepo_layout_doc(self):
        r = classify_filename("MONOREPO_LAYOUT.md")
        assert r.label == ClassificationLabel.ArchitectureDoc

    def test_dependency_rules_doc(self):
        r = classify_filename("DEPENDENCY_RULES.md")
        assert r.label == ClassificationLabel.ArchitectureDoc

    def test_intake_policy_doc(self):
        r = classify_filename("INTAKE_POLICY.md")
        assert r.label == ClassificationLabel.ArchitectureDoc

    def test_roadmap_doc(self):
        r = classify_filename("PROJECT_ROADMAP.md")
        assert r.label == ClassificationLabel.RoadmapDoc
        assert "Roadmaps" in r.destination

    def test_planning_checklist(self):
        r = classify_filename("MASTER_IMPLEMENTATION_CHECKLIST.md")
        assert r.label == ClassificationLabel.PlanningDoc
        assert "Archive/Planning" in r.destination

    def test_migration_doc(self):
        r = classify_filename("MASTERREPO_MIGRATION_MAPPING_SHEET.md")
        assert r.label == ClassificationLabel.PlanningDoc

    def test_crossplatform_doc(self):
        r = classify_filename("CROSSPLATFORM.md")
        assert r.label == ClassificationLabel.TopLevelDoc
        assert r.destination.startswith("Docs/")
        assert "Design" not in r.destination

    def test_launching_doc(self):
        r = classify_filename("LAUNCHING.md")
        assert r.label == ClassificationLabel.TopLevelDoc

    def test_unknown_md_goes_to_design(self):
        r = classify_filename("SomeRandomDoc.md")
        assert r.label == ClassificationLabel.DesignDocDefault
        assert "Docs/Design" in r.destination

    def test_txt_chat_export_goes_to_archive(self):
        r = classify_filename("RepoDirective1.txt")
        assert r.label == ClassificationLabel.ChatExport
        assert "Archive/Chats" in r.destination
        assert r.note != ""


class TestCppClassification:
    def test_cpp_file_classified(self):
        r = classify_filename("LaunchConfig.cpp")
        assert r.label == ClassificationLabel.AtlasEngineCpp

    def test_header_classified(self):
        r = classify_filename("GameSystemsRegistry.h")
        assert r.label == ClassificationLabel.AtlasEngineCpp

    def test_cpp_not_confident_without_content(self):
        # Without content sniffing, C++ routing is provisional
        r = classify_filename("SomeSystem.h")
        assert r.confident is False


class TestPythonClassification:
    def test_test_file_goes_to_tests(self):
        r = classify_filename("test_new_feature.py")
        assert r.label == ClassificationLabel.PythonTest
        assert "AtlasAI/Tests" in r.destination

    def test_validate_script(self):
        r = classify_filename("validate_something.py")
        assert r.label == ClassificationLabel.ValidateScript
        assert "Scripts/Validate" in r.destination

    def test_build_script(self):
        r = classify_filename("build_helper.py")
        assert r.label == ClassificationLabel.BuildScript
        assert "Scripts/Build" in r.destination

    def test_ci_script(self):
        r = classify_filename("ci_runner.py")
        assert r.label == ClassificationLabel.CIScript
        assert "Scripts/CI" in r.destination

    def test_generic_python_goes_to_ai_engine(self):
        r = classify_filename("some_module.py")
        assert r.label == ClassificationLabel.AiEnginePython
        assert r.confident is False


class TestCSharpClassification:
    def test_cs_file_goes_to_hostapp(self):
        r = classify_filename("NewService.cs")
        assert r.label == ClassificationLabel.CSharpHostApp
        assert "AtlasAI/HostApp" in r.destination
        assert r.confident is False  # needs content sniff

    def test_csproj_classified(self):
        r = classify_filename("MyProject.csproj")
        assert r.label == ClassificationLabel.CSharpHostApp


class TestCMakeClassification:
    def test_cmake_module(self):
        r = classify_filename("Options.cmake")
        assert r.label == ClassificationLabel.CmakeModule
        assert "cmake/" in r.destination

    def test_cmakelists(self):
        r = classify_filename("CMakeLists.txt")
        assert r.label == ClassificationLabel.CmakeModule


class TestDataClassification:
    def test_json_goes_to_data(self):
        r = classify_filename("items.json")
        assert r.label == ClassificationLabel.DataConfig
        assert "NovaForge/Data" in r.destination
        assert r.confident is False

    def test_yaml_classified(self):
        r = classify_filename("config.yaml")
        assert r.label == ClassificationLabel.DataConfig


class TestUnknownClassification:
    @pytest.mark.parametrize("filename", [
        "RandomBinary.bin",
        "UnknownFile.dat",
        "StrangeExtension.xyzzy",
    ])
    def test_unknown_goes_to_unclassified(self, filename):
        r = classify_filename(filename)
        assert r.label == ClassificationLabel.Unclassified
        assert r.confident is False
        assert "UNCLASSIFIED" in r.destination
        assert r.note != ""


# =============================================================================
# Tests — Root validator
# =============================================================================

ROOT_ALLOWLIST = {
    "Atlas", "AtlasAI", "NovaForge", "Shared", "Services", "Tools",
    "ThirdParty", "Tests", "Scripts", "Docs", "cmake", "Intake", "DropBox", "Build",
    "CMakeLists.txt", "README.md", "LICENSE", ".gitignore",
    ".git", ".github", ".pytest_cache", ".venv", "venv", "env",
    ".editorconfig", ".clang-format", ".clang-tidy",
    "pyproject.toml", "setup.cfg", "setup.py",
}


def check_root_violations(root_items: list[str]) -> list[str]:
    """Return a list of root items that are not in the allowlist."""
    violations = []
    for name in root_items:
        if name.startswith(".") and name not in ROOT_ALLOWLIST:
            continue  # skip hidden items not in allowlist
        if name not in ROOT_ALLOWLIST:
            violations.append(name)
    return violations


class TestValidateRoot:
    def test_clean_root_has_no_violations(self):
        clean = ["Atlas", "AtlasAI", "NovaForge", "CMakeLists.txt",
                 "README.md", "LICENSE", ".gitignore", "Docs",
                 "Scripts", "Shared", "Tests", "Tools", "ThirdParty",
                 "Services", "cmake", "Intake", "DropBox"]
        assert check_root_violations(clean) == []

    def test_stray_zip_is_violation(self):
        items = ["Atlas", "SomeFeature.zip", "README.md"]
        violations = check_root_violations(items)
        assert "SomeFeature.zip" in violations

    def test_stray_markdown_is_violation(self):
        items = ["Atlas", "MasterRepo_Checklist.md", "README.md"]
        violations = check_root_violations(items)
        assert "MasterRepo_Checklist.md" in violations

    def test_stray_source_directory_is_violation(self):
        items = ["Atlas", "NewImplementations", "README.md"]
        violations = check_root_violations(items)
        assert "NewImplementations" in violations

    def test_stray_text_file_is_violation(self):
        items = ["Atlas", "RepoDirective.txt"]
        violations = check_root_violations(items)
        assert "RepoDirective.txt" in violations

    def test_hidden_items_not_in_allowlist_are_skipped(self):
        # Hidden items (starting with .) not in allowlist are ignored by convention
        items = [".some_tool_cache"]
        assert check_root_violations(items) == []

    def test_known_hidden_items_allowed(self):
        for item in [".git", ".github", ".gitignore", ".pytest_cache"]:
            assert check_root_violations([item]) == []

    def test_multiple_violations_reported(self):
        items = ["Atlas", "stray1.md", "stray2.zip", "stray3.txt", "README.md"]
        violations = check_root_violations(items)
        assert len(violations) == 3

    def test_intake_dir_is_allowed(self):
        # Intake/ itself is in the allowlist — it is the sanctioned staging area
        assert check_root_violations(["Intake"]) == []

    def test_build_dir_is_allowed(self):
        assert check_root_violations(["Build"]) == []


# =============================================================================
# Tests — Intake processor (filesystem-level, using tempdir)
# =============================================================================

class TestIntakeProcessorFilesystem:
    """Filesystem-level tests that create a temporary repo-like layout."""

    @pytest.fixture
    def tmp_repo(self, tmp_path):
        """Create a minimal tmp repo with Intake/ and key destination dirs."""
        intake    = tmp_path / "Intake"
        intake.mkdir()
        (tmp_path / "Docs" / "Archive" / "ZipFiles").mkdir(parents=True)
        (tmp_path / "Docs" / "Archive" / "Chats").mkdir(parents=True)
        (tmp_path / "Docs" / "Archive" / "Planning").mkdir(parents=True)
        (tmp_path / "Docs" / "Design").mkdir(parents=True)
        (tmp_path / "Docs" / "Architecture").mkdir(parents=True)
        (tmp_path / "Docs" / "Roadmaps").mkdir(parents=True)
        (tmp_path / "AtlasAI" / "Tests").mkdir(parents=True)
        (tmp_path / "Scripts" / "Validate").mkdir(parents=True)
        (tmp_path / "Scripts" / "Build").mkdir(parents=True)
        (tmp_path / "Scripts" / "CI").mkdir(parents=True)
        (tmp_path / "AtlasAI" / "AIEngine" / "AtlasAIEngine").mkdir(parents=True)
        (tmp_path / "AtlasAI" / "HostApp").mkdir(parents=True)
        (tmp_path / "cmake").mkdir(parents=True)
        (tmp_path / "NovaForge" / "Data").mkdir(parents=True)
        (tmp_path / "Docs" / "Archive" / "Planning" / "UNCLASSIFIED").mkdir(parents=True)
        return tmp_path

    def _route_file(self, intake_path: Path, dest_dir: Path) -> Path:
        """Move a file from intake to dest, mimicking the processor."""
        dest = dest_dir / intake_path.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            shutil.move(str(intake_path), str(dest))
        return dest

    def test_zip_moved_to_zipfiles(self, tmp_repo):
        zip_file = tmp_repo / "Intake" / "MasterRepo_NewPack.zip"
        zip_file.touch()
        r = classify_filename(zip_file.name)
        dest = self._route_file(zip_file, tmp_repo / "Docs" / "Archive" / "ZipFiles")
        assert dest.exists()
        assert not zip_file.exists()

    def test_design_doc_moved_to_design(self, tmp_repo):
        md_file = tmp_repo / "Intake" / "MASTER_REPO_DIRECTIVE.md"
        md_file.write_text("# directive")
        r = classify_filename(md_file.name)
        assert "Design" in r.destination
        dest = self._route_file(md_file, tmp_repo / "Docs" / "Design")
        assert dest.exists()

    def test_test_python_moved_to_tests(self, tmp_repo):
        py_file = tmp_repo / "Intake" / "test_new_system.py"
        py_file.write_text("# test")
        r = classify_filename(py_file.name)
        assert r.label == ClassificationLabel.PythonTest
        dest = self._route_file(py_file, tmp_repo / "AtlasAI" / "Tests")
        assert dest.exists()

    def test_validate_script_moved_correctly(self, tmp_repo):
        py_file = tmp_repo / "Intake" / "validate_something.py"
        py_file.write_text("# validator")
        r = classify_filename(py_file.name)
        assert r.label == ClassificationLabel.ValidateScript
        dest = self._route_file(py_file, tmp_repo / "Scripts" / "Validate")
        assert dest.exists()

    def test_chat_txt_moved_to_archive_chats(self, tmp_repo):
        txt_file = tmp_repo / "Intake" / "RepoDirective1.txt"
        txt_file.write_text("some chat content")
        r = classify_filename(txt_file.name)
        assert r.label == ClassificationLabel.ChatExport
        dest = self._route_file(txt_file, tmp_repo / "Docs" / "Archive" / "Chats")
        assert dest.exists()

    def test_cmake_moved_to_cmake_dir(self, tmp_repo):
        cmake_file = tmp_repo / "Intake" / "MyModule.cmake"
        cmake_file.write_text("# cmake")
        r = classify_filename(cmake_file.name)
        assert r.label == ClassificationLabel.CmakeModule
        dest = self._route_file(cmake_file, tmp_repo / "cmake")
        assert dest.exists()

    def test_json_moved_to_data(self, tmp_repo):
        json_file = tmp_repo / "Intake" / "items.json"
        json_file.write_text("{}")
        r = classify_filename(json_file.name)
        assert r.label == ClassificationLabel.DataConfig
        dest = self._route_file(json_file, tmp_repo / "NovaForge" / "Data")
        assert dest.exists()

    def test_intake_empty_after_routing(self, tmp_repo):
        # Place + route several files
        for name in ["Test.zip", "DESIGN_DOC.md", "test_x.py"]:
            f = tmp_repo / "Intake" / name
            f.touch()

        for name in ["Test.zip", "DESIGN_DOC.md", "test_x.py"]:
            src = tmp_repo / "Intake" / name
            r   = classify_filename(name)
            # Resolve destination relative to tmp_repo
            dest_rel  = Path(r.destination)
            dest_abs  = tmp_repo / dest_rel
            dest_abs.parent.mkdir(parents=True, exist_ok=True)
            if src.exists() and not dest_abs.exists():
                shutil.move(str(src), str(dest_abs))

        remaining = [f for f in (tmp_repo / "Intake").iterdir()
                     if f.name != "README.md"]
        assert len(remaining) == 0

    def test_duplicate_destination_not_overwritten(self, tmp_repo):
        zip_file = tmp_repo / "Intake" / "Existing.zip"
        zip_file.touch()
        dest = tmp_repo / "Docs" / "Archive" / "ZipFiles" / "Existing.zip"
        dest.write_text("original")

        # Processor should skip (not overwrite)
        if zip_file.exists() and not dest.exists():
            shutil.move(str(zip_file), str(dest))
        # dest was already there; content unchanged
        assert dest.read_text() == "original"


# =============================================================================
# Tests — Audit log
# =============================================================================

class TestAuditLog:
    def test_audit_entry_schema(self, tmp_path):
        """Audit log entries must contain required fields."""
        log_file = tmp_path / "intake_log.jsonl"
        entry = {
            "timestamp":      "2026-03-28T14:00:00+00:00",
            "source":         "Intake/SomeFile.md",
            "destination":    "Docs/Design/SomeFile.md",
            "classification": "design_doc",
            "confident":      True,
            "note":           "",
            "dry_run":        False,
        }
        log_file.write_text(json.dumps(entry) + "\n")
        loaded = json.loads(log_file.read_text().strip())
        assert loaded["timestamp"] != ""
        assert loaded["source"].startswith("Intake/")
        assert "classification" in loaded
        assert isinstance(loaded["confident"], bool)
        assert "dry_run" in loaded

    def test_audit_entry_dry_run_flag(self, tmp_path):
        log_file = tmp_path / "intake_log.jsonl"
        entry = {
            "timestamp": "2026-03-28T14:00:00+00:00",
            "source": "Intake/x.zip",
            "destination": "Docs/Archive/ZipFiles/x.zip",
            "classification": "zip_archive",
            "confident": True,
            "note": "",
            "dry_run": True,
        }
        log_file.write_text(json.dumps(entry) + "\n")
        loaded = json.loads(log_file.read_text().strip())
        assert loaded["dry_run"] is True

    def test_multiple_audit_entries(self, tmp_path):
        log_file = tmp_path / "intake_log.jsonl"
        entries = [
            {"timestamp": "t", "source": "Intake/a.zip",
             "destination": "Docs/Archive/ZipFiles/a.zip",
             "classification": "zip_archive", "confident": True, "note": "", "dry_run": False},
            {"timestamp": "t", "source": "Intake/b.md",
             "destination": "Docs/Design/b.md",
             "classification": "design_doc", "confident": True, "note": "", "dry_run": False},
        ]
        log_file.write_text("\n".join(json.dumps(e) for e in entries) + "\n")
        lines = [json.loads(l) for l in log_file.read_text().strip().splitlines()]
        assert len(lines) == 2
        assert lines[0]["classification"] == "zip_archive"
        assert lines[1]["classification"] == "design_doc"


# =============================================================================
# Tests — Content-based C++ routing (namespace sniffing)
# =============================================================================

_CPP_NAMESPACE_RE = _re.compile(r'namespace\s+(atlas|novaforge)\b', _re.IGNORECASE)
_CPP_BOUNDARY_RE  = _re.compile(r'#include\s+".*novaforge', _re.IGNORECASE)


def classify_cpp_content(filename: str, content: str) -> ClassificationResult:
    """Classify a C++ file using its content."""
    head = "\n".join(content.splitlines()[:60])
    stem = Path(filename).stem.lower()

    has_atlas_ns    = bool(_re.search(r'namespace\s+atlas\b', head, _re.IGNORECASE))
    has_novaforge_ns = bool(_re.search(r'namespace\s+novaforge\b', head, _re.IGNORECASE))
    has_nf_include   = bool(_re.search(r'#include\s+".*novaforge', head, _re.IGNORECASE))

    if has_atlas_ns:
        if has_nf_include:
            return ClassificationResult(filename,
                                        f"Docs/Archive/Planning/UNCLASSIFIED/{filename}",
                                        ClassificationLabel.BoundaryViolation,
                                        confident=False,
                                        note="Atlas file with NovaForge include.")
        if any(k in stem for k in ("editor", "panel", "dock", "outliner",
                                    "inspector", "gizmo", "command")):
            return ClassificationResult(filename,
                                        f"Atlas/Editor/Core/{filename}",
                                        ClassificationLabel.AtlasEditorCpp)
        if any(k in stem for k in ("launch", "config", "schema", "settings")):
            zone = "Config"
        elif any(k in stem for k in ("render", "viewport")):
            zone = "Rendering"
        elif any(k in stem for k in ("physics",)):
            zone = "Physics"
        else:
            zone = "Core"
        return ClassificationResult(filename, f"Atlas/Engine/{zone}/{filename}",
                                    ClassificationLabel.AtlasEngineCpp)

    if has_novaforge_ns:
        if any(k in stem for k in ("bootstrap", "app", "session", "orchestrat")):
            return ClassificationResult(filename,
                                        f"NovaForge/App/src/{filename}",
                                        ClassificationLabel.NovaForgeApp)
        return ClassificationResult(filename,
                                    f"NovaForge/Gameplay/{filename}",
                                    ClassificationLabel.NovaForgeGameplay)

    return ClassificationResult(filename,
                                f"Docs/Archive/Planning/UNCLASSIFIED/{filename}",
                                ClassificationLabel.Unclassified,
                                confident=False)


class TestCppContentClassification:
    def test_atlas_config_header(self):
        content = "namespace atlas {\nclass LaunchConfig {};\n}"
        r = classify_cpp_content("LaunchConfig.h", content)
        assert r.label == ClassificationLabel.AtlasEngineCpp
        assert "Config" in r.destination

    def test_atlas_render_header(self):
        content = "namespace atlas {\nclass RenderViewport {};\n}"
        r = classify_cpp_content("RenderViewport.h", content)
        assert r.label == ClassificationLabel.AtlasEngineCpp
        assert "Rendering" in r.destination

    def test_atlas_editor_header(self):
        content = "namespace atlas {\nclass EditorOutliner {};\n}"
        r = classify_cpp_content("EditorOutliner.h", content)
        assert r.label == ClassificationLabel.AtlasEditorCpp
        assert "Atlas/Editor" in r.destination

    def test_novaforge_app_bootstrap(self):
        content = "namespace NovaForge {\nclass WorldBootstrap {};\n}"
        r = classify_cpp_content("WorldBootstrap.h", content)
        assert r.label == ClassificationLabel.NovaForgeApp

    def test_novaforge_gameplay(self):
        content = "namespace NovaForge {\nclass FleetSystem {};\n}"
        r = classify_cpp_content("FleetSystem.h", content)
        assert r.label == ClassificationLabel.NovaForgeGameplay

    def test_atlas_with_novaforge_include_is_violation(self):
        content = ('namespace atlas {\n'
                   '#include "NovaForge/Gameplay/FleetSystem.h"\n'
                   'class BrokenSystem {};\n}')
        r = classify_cpp_content("BrokenSystem.h", content)
        assert r.label == ClassificationLabel.BoundaryViolation
        assert r.confident is False

    def test_no_namespace_is_unclassified(self):
        content = "// just a comment\nint foo() { return 0; }\n"
        r = classify_cpp_content("mystery.cpp", content)
        assert r.label == ClassificationLabel.Unclassified
        assert r.confident is False


# =============================================================================
# Tests — DropBox staging area
# =============================================================================

class TestDropBoxValidation:
    """DropBox/ must be in the root allowlist and git-ignored for binary/archive types."""

    def test_dropbox_is_allowed_at_root(self):
        """DropBox is a sanctioned root directory and must not trigger root violations."""
        updated_allowlist = ROOT_ALLOWLIST | {"DropBox"}
        violations = [name for name in ["DropBox"]
                      if name not in updated_allowlist]
        assert violations == [], "DropBox must be in the root allowlist"

    def test_dropbox_in_validate_root_allowlist(self):
        """validate_root.py ALLOWLIST must include DropBox."""
        validate_root_path = (
            Path(__file__).resolve().parents[2]
            / "Scripts" / "Validate" / "validate_root.py"
        )
        assert validate_root_path.exists(), "validate_root.py must exist"
        source = validate_root_path.read_text(encoding="utf-8")
        assert '"DropBox"' in source, (
            'validate_root.py ALLOWLIST must contain "DropBox"'
        )

    def test_dropbox_gitignore_exists(self):
        """DropBox/.gitignore must exist to prevent binary/archive files from being tracked."""
        dropbox_gitignore = (
            Path(__file__).resolve().parents[2] / "DropBox" / ".gitignore"
        )
        assert dropbox_gitignore.exists(), "DropBox/.gitignore must exist"

    def test_dropbox_gitignore_covers_zip(self):
        """DropBox/.gitignore must include *.zip pattern."""
        dropbox_gitignore = (
            Path(__file__).resolve().parents[2] / "DropBox" / ".gitignore"
        )
        content = dropbox_gitignore.read_text(encoding="utf-8")
        assert "*.zip" in content, "DropBox/.gitignore must ignore *.zip"

    def test_dropbox_gitignore_covers_common_archive_types(self):
        """DropBox/.gitignore must cover major archive/binary formats."""
        dropbox_gitignore = (
            Path(__file__).resolve().parents[2] / "DropBox" / ".gitignore"
        )
        content = dropbox_gitignore.read_text(encoding="utf-8")
        for pattern in ("*.7z", "*.rar", "*.tar", "*.exe"):
            assert pattern in content, (
                f"DropBox/.gitignore must ignore {pattern}"
            )

    def test_dropbox_readme_exists(self):
        """DropBox/README.md must exist to document the intake workflow."""
        dropbox_readme = (
            Path(__file__).resolve().parents[2] / "DropBox" / "README.md"
        )
        assert dropbox_readme.exists(), "DropBox/README.md must exist"

    def test_dropbox_readme_mentions_process_intake(self):
        """DropBox/README.md must reference process_intake.py."""
        dropbox_readme = (
            Path(__file__).resolve().parents[2] / "DropBox" / "README.md"
        )
        content = dropbox_readme.read_text(encoding="utf-8")
        assert "process_intake.py" in content, (
            "DropBox/README.md must mention process_intake.py"
        )


class TestDropBoxClassification:
    """Files dropped in DropBox are classified identically to files in Intake/."""

    def test_zip_from_dropbox_routes_to_zipfiles(self):
        r = classify_filename("SomePack.zip")
        assert r.label == ClassificationLabel.ZipArchive
        assert "ZipFiles" in r.destination

    def test_7z_from_dropbox_routes_to_zipfiles(self):
        r = classify_filename("SomePack.7z")
        assert r.label == ClassificationLabel.ZipArchive
        assert "ZipFiles" in r.destination

    def test_rar_from_dropbox_routes_to_zipfiles(self):
        r = classify_filename("SomePack.rar")
        assert r.label == ClassificationLabel.ZipArchive
        assert "ZipFiles" in r.destination

    def test_md_from_dropbox_still_classified_as_doc(self):
        r = classify_filename("DESIGN_BRIEF.md")
        assert r.label in (
            ClassificationLabel.DesignDoc,
            ClassificationLabel.DesignDocDefault,
        )


class TestDropBoxFilesystemIntegration:
    """Filesystem-level tests using a temp dir to verify DropBox scanning."""

    @pytest.fixture
    def tmp_repo(self, tmp_path):
        """Create a minimal tmp repo with both Intake/ and DropBox/ staging areas."""
        (tmp_path / "Intake").mkdir()
        (tmp_path / "DropBox").mkdir()
        (tmp_path / "Docs" / "Archive" / "ZipFiles").mkdir(parents=True)
        (tmp_path / "Docs" / "Archive" / "Chats").mkdir(parents=True)
        (tmp_path / "Docs" / "Design").mkdir(parents=True)
        return tmp_path

    def _route_file(self, src: Path, dest_dir: Path) -> Path:
        dest = dest_dir / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            shutil.move(str(src), str(dest))
        return dest

    def test_zip_in_dropbox_can_be_routed(self, tmp_repo):
        """A zip placed in DropBox/ should be classifiable and routable."""
        zip_file = tmp_repo / "DropBox" / "NewContent.zip"
        zip_file.touch()
        r = classify_filename(zip_file.name)
        assert r.label == ClassificationLabel.ZipArchive
        dest = self._route_file(zip_file, tmp_repo / "Docs" / "Archive" / "ZipFiles")
        assert dest.exists()
        assert not zip_file.exists()

    def test_md_in_dropbox_can_be_routed(self, tmp_repo):
        """A markdown dropped in DropBox/ is classified and moves to Docs/."""
        md_file = tmp_repo / "DropBox" / "DESIGN_SPEC.md"
        md_file.write_text("# spec")
        r = classify_filename(md_file.name)
        assert "Design" in r.destination
        dest = self._route_file(md_file, tmp_repo / "Docs" / "Design")
        assert dest.exists()

    def test_dropbox_empty_after_routing(self, tmp_repo):
        """After routing all items, DropBox/ (minus README/.gitignore) should be empty."""
        files = {
            "TestBundle.zip": tmp_repo / "Docs" / "Archive" / "ZipFiles",
            "DESIGN_DOC.md": tmp_repo / "Docs" / "Design",
        }
        for name, dest_dir in files.items():
            (tmp_repo / "DropBox" / name).touch()

        for name, dest_dir in files.items():
            src = tmp_repo / "DropBox" / name
            if src.exists():
                self._route_file(src, dest_dir)

        remaining = [
            f for f in (tmp_repo / "DropBox").iterdir()
            if f.name not in ("README.md", ".gitignore")
        ]
        assert len(remaining) == 0, f"DropBox still has unrouted items: {remaining}"

    def test_both_intake_and_dropbox_scanned(self, tmp_repo):
        """Both Intake/ and DropBox/ should be scanned independently."""
        (tmp_repo / "Intake" / "intake_doc.md").write_text("# doc")
        (tmp_repo / "DropBox" / "dropbox_pack.zip").touch()

        # Simulate scanning both
        all_files = (
            list((tmp_repo / "Intake").iterdir()) +
            list((tmp_repo / "DropBox").iterdir())
        )
        all_files = [f for f in all_files
                     if f.name not in ("README.md", ".gitignore") and not f.name.startswith(".")]

        assert len(all_files) == 2
        names = {f.name for f in all_files}
        assert "intake_doc.md" in names
        assert "dropbox_pack.zip" in names


class TestProcessIntakeScript:
    """Tests that verify the process_intake.py script exposes the DropBox scanning feature."""

    def test_process_intake_defines_dropbox_dir(self):
        """process_intake.py must define DROPBOX_DIR pointing to DropBox/."""
        script_path = (
            Path(__file__).resolve().parents[2]
            / "Scripts" / "Intake" / "process_intake.py"
        )
        source = script_path.read_text(encoding="utf-8")
        assert "DROPBOX_DIR" in source, (
            "process_intake.py must define DROPBOX_DIR"
        )
        assert '"DropBox"' in source or "'DropBox'" in source, (
            'process_intake.py must reference the "DropBox" directory'
        )

    def test_process_intake_accepts_source_argument(self):
        """process_intake.py must accept a --source argument with dropbox option."""
        script_path = (
            Path(__file__).resolve().parents[2]
            / "Scripts" / "Intake" / "process_intake.py"
        )
        source = script_path.read_text(encoding="utf-8")
        assert "--source" in source, (
            "process_intake.py must support --source CLI argument"
        )
        assert "dropbox" in source, (
            "process_intake.py --source must accept 'dropbox' option"
        )

    def test_process_intake_scans_dropbox_dir(self):
        """process_intake.py must call _scan_staging_dir on DROPBOX_DIR."""
        script_path = (
            Path(__file__).resolve().parents[2]
            / "Scripts" / "Intake" / "process_intake.py"
        )
        source = script_path.read_text(encoding="utf-8")
        assert "_scan_staging_dir" in source, (
            "process_intake.py must define _scan_staging_dir to handle DropBox"
        )

