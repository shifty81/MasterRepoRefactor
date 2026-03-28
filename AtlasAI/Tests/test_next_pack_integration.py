"""Tests for master_repo_next_pack integration.

Validates that all source files, docs, schemas, and ingestion data from
master_repo_next_pack.zip are correctly placed in their canonical locations.
"""

import json
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _p(rel: str) -> Path:
    return REPO_ROOT / rel


def _load_json(rel: str) -> object:
    path = _p(rel)
    assert path.exists(), f"Missing: {rel}"
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Source files present
# ---------------------------------------------------------------------------

class TestNextPackSourceFiles:
    EXPECTED = [
        # BuilderRuntime
        "NovaForge/Runtime/Builder/AssemblyRuntimeComponent.h",
        "NovaForge/Runtime/Builder/AssemblyRuntimeComponent.cpp",
        "NovaForge/Runtime/Builder/SnapGraphRuntime.h",
        "NovaForge/Runtime/Builder/SnapGraphRuntime.cpp",
        # Salvage
        "NovaForge/Runtime/Salvage/SalvageTargetComponent.h",
        "NovaForge/Runtime/Salvage/SalvageTargetComponent.cpp",
        "NovaForge/Runtime/Salvage/RepairableSubsystemComponent.h",
        "NovaForge/Runtime/Salvage/RepairableSubsystemComponent.cpp",
        # SaveLoad
        "NovaForge/Runtime/SaveLoad/SaveCoordinator.h",
        "NovaForge/Runtime/SaveLoad/SaveCoordinator.cpp",
        "NovaForge/Runtime/SaveLoad/DeterministicRestoreService.h",
        "NovaForge/Runtime/SaveLoad/DeterministicRestoreService.cpp",
        # Gameplay bridge
        "NovaForge/Runtime/Gameplay/BuilderSalvageRuntimeBridge.h",
        "NovaForge/Runtime/Gameplay/BuilderSalvageRuntimeBridge.cpp",
        # Debug
        "NovaForge/Runtime/Debug/RuntimeDebugCommandService.h",
        "NovaForge/Runtime/Debug/RuntimeDebugCommandService.cpp",
    ]

    @pytest.mark.parametrize("rel", EXPECTED)
    def test_file_exists(self, rel):
        assert _p(rel).exists(), f"Missing source file: {rel}"

    @pytest.mark.parametrize("rel", [f for f in EXPECTED if f.endswith(".h")])
    def test_header_has_pragma_once(self, rel):
        content = _p(rel).read_text(encoding="utf-8")
        assert "#pragma once" in content, f"{rel} missing #pragma once"

    def test_assembly_component_has_namespace(self):
        h = _p("NovaForge/Runtime/Builder/AssemblyRuntimeComponent.h").read_text()
        assert "namespace Runtime::BuilderRuntime" in h

    def test_salvage_target_has_namespace(self):
        h = _p("NovaForge/Runtime/Salvage/SalvageTargetComponent.h").read_text()
        assert "namespace Runtime::Salvage" in h

    def test_save_coordinator_has_namespace(self):
        h = _p("NovaForge/Runtime/SaveLoad/SaveCoordinator.h").read_text()
        assert "namespace Runtime::SaveLoad" in h

    def test_save_coordinator_has_slot_list(self):
        h = _p("NovaForge/Runtime/SaveLoad/SaveCoordinator.h").read_text()
        assert "ListSlots" in h

    def test_deterministic_restore_exists(self):
        h = _p("NovaForge/Runtime/SaveLoad/DeterministicRestoreService.h").read_text()
        assert "DeterministicRestoreService" in h

    def test_builder_salvage_bridge_has_namespace(self):
        h = _p("NovaForge/Runtime/Gameplay/BuilderSalvageRuntimeBridge.h").read_text()
        assert "namespace Runtime::Gameplay" in h or "namespace Runtime" in h

    def test_debug_command_service_has_namespace(self):
        h = _p("NovaForge/Runtime/Debug/RuntimeDebugCommandService.h").read_text()
        assert "namespace Runtime" in h

    def test_snap_graph_runtime_exists(self):
        h = _p("NovaForge/Runtime/Builder/SnapGraphRuntime.h").read_text()
        assert "SnapGraphRuntime" in h

    def test_repairable_subsystem_component_exists(self):
        h = _p("NovaForge/Runtime/Salvage/RepairableSubsystemComponent.h").read_text()
        assert "RepairableSubsystemComponent" in h


# ---------------------------------------------------------------------------
# Documentation files present
# ---------------------------------------------------------------------------

class TestNextPackDocs:
    def test_builder_salvage_spec(self):
        p = _p("Docs/Runtime/EXPANDED_BUILDER_SALVAGE_SPEC.md")
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert "AssemblyRuntimeComponent" in content
        assert "salvage" in content.lower()

    def test_saveload_contracts(self):
        p = _p("Docs/Runtime/EXPANDED_SAVELOAD_CONTRACTS.md")
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert "save" in content.lower() or "SaveCoordinator" in content

    def test_command_gateway_doc(self):
        p = _p("Docs/AtlasSuite/EXPANDED_ARBITER_COMMAND_GATEWAY.md")
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert "gateway" in content.lower() or "command" in content.lower()


# ---------------------------------------------------------------------------
# Schema file present and valid JSON
# ---------------------------------------------------------------------------

class TestNextPackSchema:
    def test_command_gateway_schema_present(self):
        assert _p("Shared/ToolProtocol/schemas/command_gateway_schema.json").exists()

    def test_command_gateway_schema_valid_json(self):
        data = _load_json("Shared/ToolProtocol/schemas/command_gateway_schema.json")
        assert data is not None


# ---------------------------------------------------------------------------
# Ingestion data merged and valid
# ---------------------------------------------------------------------------

class TestNextPackIngestion:
    def test_knowledge_chunks_valid_json(self):
        chunks = _load_json("AtlasAI/Ingestion/knowledge_chunks.json")
        assert isinstance(chunks, list)
        assert len(chunks) >= 8, "Should have at least 8 chunks (5 original + 3 new)"

    def test_new_chunk_ids_present(self):
        chunks = _load_json("AtlasAI/Ingestion/knowledge_chunks.json")
        ids = {c["id"] for c in chunks}
        assert "builder-salvage-overview" in ids
        assert "save-seed-delta-rule" in ids
        assert "gateway-command-envelope" in ids

    def test_original_chunk_ids_preserved(self):
        chunks = _load_json("AtlasAI/Ingestion/knowledge_chunks.json")
        ids = {c["id"] for c in chunks}
        assert "runtime-gameplay-overview" in ids
        assert "rig-controller-contract" in ids

    def test_all_chunks_have_required_fields(self):
        chunks = _load_json("AtlasAI/Ingestion/knowledge_chunks.json")
        for chunk in chunks:
            assert "id" in chunk, f"Chunk missing id: {chunk}"
            assert "title" in chunk, f"Chunk missing title: {chunk}"
            assert "summary" in chunk, f"Chunk missing summary: {chunk}"
            assert "keywords" in chunk, f"Chunk missing keywords: {chunk}"

    def test_no_trailing_commas_in_chunks_json(self):
        """Knowledge chunks JSON must be standard-compliant (no trailing commas)."""
        raw = _p("AtlasAI/Ingestion/knowledge_chunks.json").read_text(encoding="utf-8")
        # If json.loads succeeds, it's standards-compliant
        parsed = json.loads(raw)
        assert isinstance(parsed, list)


# ---------------------------------------------------------------------------
# Root is clean (no zip files or extracted dirs at root)
# ---------------------------------------------------------------------------

class TestRootClean:
    def test_free_lowpoly_zip_not_at_root(self):
        assert not _p("free-low-poly-male-base.zip").exists()

    def test_next_pack_zip_not_at_root(self):
        assert not _p("master_repo_next_pack.zip").exists()

    def test_mega_archive_dir_not_at_root(self):
        assert not _p("MasterRepo_MegaArchive").exists()

    def test_zips_archived(self):
        assert _p("Docs/Archive/ZipFiles/free-low-poly-male-base.zip").exists()
        assert _p("Docs/Archive/ZipFiles/master_repo_next_pack.zip").exists()

    def test_mega_archive_extracted_archived(self):
        assert _p("Docs/Archive/MasterRepo_MegaArchive_Extracted").is_dir()

    def test_gitignore_has_mesh_exclusions(self):
        gi = _p(".gitignore").read_text(encoding="utf-8")
        assert ".glb" in gi
        assert ".fbx" in gi
        assert "ASSET_MANIFEST.json" in gi

    def test_gitignore_has_main_zip_entry(self):
        gi = _p(".gitignore").read_text(encoding="utf-8")
        assert "MasterRepoRefactor-main.zip" in gi
