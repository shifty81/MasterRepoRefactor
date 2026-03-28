"""Tests for the atlas_suite_persistence_pack integration.

Checks that all persistence runtime files, UI panels, docs, and data configs
landed in their canonical repo locations.
"""

import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _p(rel: str) -> Path:
    return REPO_ROOT / rel


# ---------------------------------------------------------------------------
# NovaForge Runtime — Persistence core
# ---------------------------------------------------------------------------

class TestPersistenceRuntimeCore:
    def test_save_manifest(self):
        assert _p("NovaForge/Runtime/Persistence/SaveManifest.cs").exists()

    def test_contributor_snapshot_ref(self):
        assert _p("NovaForge/Runtime/Persistence/ContributorSnapshotRef.cs").exists()

    def test_ipersistence_contributor(self):
        assert _p("NovaForge/Runtime/Persistence/IPersistenceContributor.cs").exists()

    def test_persistence_validation_result(self):
        assert _p("NovaForge/Runtime/Persistence/PersistenceValidationResult.cs").exists()

    def test_persistence_registry(self):
        assert _p("NovaForge/Runtime/Persistence/PersistenceRegistry.cs").exists()

    def test_json_snapshot_serializer(self):
        assert _p("NovaForge/Runtime/Persistence/JsonSnapshotSerializer.cs").exists()

    def test_save_slot_service(self):
        assert _p("NovaForge/Runtime/Persistence/SaveSlotService.cs").exists()

    def test_persistence_coordinator(self):
        assert _p("NovaForge/Runtime/Persistence/PersistenceCoordinator.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Persistence snapshots
# ---------------------------------------------------------------------------

class TestPersistenceSnapshots:
    def test_rig_snapshot(self):
        assert _p("NovaForge/Runtime/Persistence/Snapshots/RigPersistenceSnapshot.cs").exists()

    def test_vehicle_snapshot(self):
        assert _p("NovaForge/Runtime/Persistence/Snapshots/VehiclePersistenceSnapshot.cs").exists()

    def test_builder_salvage_snapshot(self):
        assert _p("NovaForge/Runtime/Persistence/Snapshots/BuilderSalvagePersistenceSnapshot.cs").exists()

    def test_mission_snapshot(self):
        assert _p("NovaForge/Runtime/Persistence/Snapshots/MissionPersistenceSnapshot.cs").exists()

    def test_economy_snapshot(self):
        assert _p("NovaForge/Runtime/Persistence/Snapshots/EconomyPersistenceSnapshot.cs").exists()

    def test_faction_snapshot(self):
        assert _p("NovaForge/Runtime/Persistence/Snapshots/FactionPersistenceSnapshot.cs").exists()

    def test_combat_hazard_snapshot(self):
        assert _p("NovaForge/Runtime/Persistence/Snapshots/CombatHazardPersistenceSnapshot.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Persistence contributors
# ---------------------------------------------------------------------------

class TestPersistenceContributors:
    def test_rig_contributor(self):
        assert _p("NovaForge/Runtime/Persistence/Contributors/RigPersistenceContributor.cs").exists()

    def test_vehicle_contributor(self):
        assert _p("NovaForge/Runtime/Persistence/Contributors/VehiclePersistenceContributor.cs").exists()

    def test_builder_salvage_contributor(self):
        assert _p("NovaForge/Runtime/Persistence/Contributors/BuilderSalvagePersistenceContributor.cs").exists()

    def test_mission_contributor(self):
        assert _p("NovaForge/Runtime/Persistence/Contributors/MissionPersistenceContributor.cs").exists()

    def test_economy_contributor(self):
        assert _p("NovaForge/Runtime/Persistence/Contributors/EconomyPersistenceContributor.cs").exists()

    def test_faction_contributor(self):
        assert _p("NovaForge/Runtime/Persistence/Contributors/FactionPersistenceContributor.cs").exists()

    def test_combat_hazard_contributor(self):
        assert _p("NovaForge/Runtime/Persistence/Contributors/CombatHazardPersistenceContributor.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — DevWorld persistence service
# ---------------------------------------------------------------------------

class TestPersistenceDevWorldService:
    def test_persistence_smoke_test_service(self):
        assert _p("NovaForge/Runtime/DevWorld/Services/PersistenceSmokeTestService.cs").exists()


# ---------------------------------------------------------------------------
# Atlas UI — Persistence panels and playtest command
# ---------------------------------------------------------------------------

class TestPersistenceUI:
    def test_persistence_playtest_command(self):
        assert _p("Atlas/UI/AtlasSuite/PlaytestHost/PersistencePlaytestCommand.cs").exists()

    def test_persistence_debug_panel_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/PersistenceDebug/PersistenceDebugPanel.xaml").exists()

    def test_persistence_debug_panel_cs(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/PersistenceDebug/PersistenceDebugPanel.xaml.cs").exists()


# ---------------------------------------------------------------------------
# Docs — Persistence pack docs
# ---------------------------------------------------------------------------

class TestPersistenceDocs:
    def test_scaffold_doc(self):
        assert _p("Docs/AtlasSuite/SAVELOAD_PERSISTENCE_INTEGRATION_SCAFFOLD.md").exists()

    def test_smoke_test_doc(self):
        assert _p("Docs/AtlasSuite/SAVELOAD_PERSISTENCE_SMOKE_TEST.md").exists()

    def test_pack_index(self):
        assert _p("Docs/AtlasSuite/PERSISTENCE_PACK_INDEX.md").exists()


# ---------------------------------------------------------------------------
# Content — Persistence config and data
# ---------------------------------------------------------------------------

class TestPersistenceContent:
    def test_dev_persistence_profile(self):
        assert _p("NovaForge/Content/Config/dev_persistence_profile.json").exists()

    def test_devworld_save_manifest_template(self):
        assert _p("NovaForge/Content/Data/SaveLoad/devworld_save_manifest_template.json").exists()


# ---------------------------------------------------------------------------
# Root validation
# ---------------------------------------------------------------------------

class TestRootClean:
    """Root must contain only allowlisted items after intake."""

    _ALLOWLIST = {
        "Atlas", "AtlasAI", "NovaForge", "Shared", "Services", "Tools",
        "ThirdParty", "Tests", "Scripts", "Docs", "cmake",
        "Intake", "Build",
        "CMakeLists.txt", "README.md", "LICENSE", ".gitignore",
        ".git", ".github", ".pytest_cache", ".venv", "venv", "env",
        ".editorconfig", ".clang-format", ".clang-tidy",
        "pyproject.toml", "setup.cfg", "setup.py",
    }

    def test_no_root_violations(self):
        violations = []
        for item in sorted(REPO_ROOT.iterdir()):
            name = item.name
            if name.startswith(".") and name not in self._ALLOWLIST:
                continue
            if name not in self._ALLOWLIST:
                violations.append(name)
        assert violations == [], f"Root-level violations found: {violations}"
