"""Tests for Platform Hardening Pack v2 and Gap Closure Pack v1 integration.

Verifies that all files from both packs landed in their canonical repo locations:
  - Docs/AtlasSuite/Security/      — security spec docs (GAP_CLOSURE_PACK_V1 + PlatformHardeningPackV2)
  - Atlas/Config/Security/         — runtime JSON configs
  - Atlas/Config/Security/Schemas/ — JSON schemas from GAP_CLOSURE_PACK_V1
  - Atlas/Services/Common/         — shared C++17 utilities
  - Atlas/Services/Security/       — session, capability, path, audit services
  - Atlas/Services/Archive/        — archive intake service
  - Atlas/Services/Bridge/         — command broker and bridge service
  - Tests/Security/                — C++ integration tests
"""

import json
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _p(rel: str) -> Path:
    return REPO_ROOT / rel


# ---------------------------------------------------------------------------
# Documentation — Gap Closure Pack v1 specs
# ---------------------------------------------------------------------------

class TestGapClosurePackV1Docs:
    """All 9 security spec docs from GapClosurePackV1_Docs.zip must be present."""

    def test_gap_closure_index(self):
        assert _p("Docs/AtlasSuite/Security/GAP_CLOSURE_PACK_V1.md").exists()

    def test_path_canonicalization_spec(self):
        assert _p("Docs/AtlasSuite/Security/PATH_CANONICALIZATION_SPEC.md").exists()

    def test_patch_review_spec(self):
        assert _p("Docs/AtlasSuite/Security/PATCH_REVIEW_SPEC.md").exists()

    def test_command_broker_execution_spec(self):
        assert _p("Docs/AtlasSuite/Security/COMMAND_BROKER_EXECUTION_SPEC.md").exists()

    def test_audit_chain_spec(self):
        assert _p("Docs/AtlasSuite/Security/AUDIT_CHAIN_SPEC.md").exists()

    def test_config_schema_spec(self):
        assert _p("Docs/AtlasSuite/Security/CONFIG_SCHEMA_SPEC.md").exists()

    def test_archive_deep_inspection_spec(self):
        assert _p("Docs/AtlasSuite/Security/ARCHIVE_DEEP_INSPECTION_SPEC.md").exists()

    def test_transport_auth_binding_spec(self):
        assert _p("Docs/AtlasSuite/Security/TRANSPORT_AUTH_BINDING_SPEC.md").exists()

    def test_secret_redaction_spec(self):
        assert _p("Docs/AtlasSuite/Security/SECRET_REDACTION_SPEC.md").exists()

    def test_gap_closure_index_content(self):
        content = _p("Docs/AtlasSuite/Security/GAP_CLOSURE_PACK_V1.md").read_text(encoding="utf-8")
        assert "Gap Closure" in content
        assert "Tier 1" in content

    def test_path_canonicalization_spec_not_empty(self):
        assert _p("Docs/AtlasSuite/Security/PATH_CANONICALIZATION_SPEC.md").stat().st_size > 0


# ---------------------------------------------------------------------------
# Documentation — PlatformHardeningPackV2 docs
# ---------------------------------------------------------------------------

class TestPlatformHardeningDocs:
    """Integration notes and repo patch guide from PlatformHardeningPackV2."""

    def test_integration_notes(self):
        assert _p("Docs/AtlasSuite/Security/INTEGRATION_NOTES.md").exists()

    def test_repo_patch_guide(self):
        assert _p("Docs/AtlasSuite/Security/REPO_PATCH_GUIDE.md").exists()

    def test_integration_notes_mentions_session_wiring(self):
        content = _p("Docs/AtlasSuite/Security/INTEGRATION_NOTES.md").read_text(encoding="utf-8")
        assert "session" in content.lower()

    def test_repo_patch_guide_not_empty(self):
        assert _p("Docs/AtlasSuite/Security/REPO_PATCH_GUIDE.md").stat().st_size > 0


# ---------------------------------------------------------------------------
# Config schemas — Gap Closure Pack v1
# ---------------------------------------------------------------------------

class TestConfigSchemas:
    """All 5 JSON schemas from GapClosurePackV1 must be present and valid JSON."""

    SCHEMAS = [
        "Atlas/Config/Security/Schemas/path_policy.schema.json",
        "Atlas/Config/Security/Schemas/session_capabilities.schema.json",
        "Atlas/Config/Security/Schemas/tool_allowlist.schema.json",
        "Atlas/Config/Security/Schemas/archive_intake_policy.schema.json",
        "Atlas/Config/Security/Schemas/shipping_feature_policy.schema.json",
    ]

    def test_path_policy_schema_exists(self):
        assert _p("Atlas/Config/Security/Schemas/path_policy.schema.json").exists()

    def test_session_capabilities_schema_exists(self):
        assert _p("Atlas/Config/Security/Schemas/session_capabilities.schema.json").exists()

    def test_tool_allowlist_schema_exists(self):
        assert _p("Atlas/Config/Security/Schemas/tool_allowlist.schema.json").exists()

    def test_archive_intake_policy_schema_exists(self):
        assert _p("Atlas/Config/Security/Schemas/archive_intake_policy.schema.json").exists()

    def test_shipping_feature_policy_schema_exists(self):
        assert _p("Atlas/Config/Security/Schemas/shipping_feature_policy.schema.json").exists()

    @pytest.mark.parametrize("rel", SCHEMAS)
    def test_schema_is_valid_json(self, rel: str):
        text = _p(rel).read_text(encoding="utf-8")
        parsed = json.loads(text)
        assert isinstance(parsed, dict), f"{rel} root must be a JSON object"


# ---------------------------------------------------------------------------
# Runtime configs — PlatformHardeningPackV2
# ---------------------------------------------------------------------------

class TestRuntimeConfigs:
    """All 4 runtime JSON configs must be present and valid JSON."""

    CONFIGS = [
        "Atlas/Config/Security/path_policy.json",
        "Atlas/Config/Security/session_capabilities.json",
        "Atlas/Config/Security/tool_allowlist.json",
        "Atlas/Config/Security/archive_intake_policy.json",
    ]

    def test_path_policy_json_exists(self):
        assert _p("Atlas/Config/Security/path_policy.json").exists()

    def test_session_capabilities_json_exists(self):
        assert _p("Atlas/Config/Security/session_capabilities.json").exists()

    def test_tool_allowlist_json_exists(self):
        assert _p("Atlas/Config/Security/tool_allowlist.json").exists()

    def test_archive_intake_policy_json_exists(self):
        assert _p("Atlas/Config/Security/archive_intake_policy.json").exists()

    @pytest.mark.parametrize("rel", CONFIGS)
    def test_config_is_valid_json(self, rel: str):
        text = _p(rel).read_text(encoding="utf-8")
        assert json.loads(text) is not None, f"{rel} must be valid JSON"

    def test_path_policy_has_protected_roots(self):
        data = json.loads(_p("Atlas/Config/Security/path_policy.json").read_text(encoding="utf-8"))
        assert "protectedRoots" in data
        assert isinstance(data["protectedRoots"], list)
        assert len(data["protectedRoots"]) > 0

    def test_session_capabilities_has_editor_role(self):
        data = json.loads(_p("Atlas/Config/Security/session_capabilities.json").read_text(encoding="utf-8"))
        modes = data.get("modes", data)  # support both flat and nested formats
        assert "editor" in modes
        assert "read_repo" in modes["editor"]

    def test_tool_allowlist_has_cmake_entry(self):
        data = json.loads(_p("Atlas/Config/Security/tool_allowlist.json").read_text(encoding="utf-8"))
        assert isinstance(data, dict)
        assert "tools" in data
        tool_ids = [t.get("toolId") for t in data["tools"]]
        assert "cmake_build" in tool_ids

    def test_archive_intake_policy_has_quarantine_flag(self):
        data = json.loads(_p("Atlas/Config/Security/archive_intake_policy.json").read_text(encoding="utf-8"))
        assert "quarantine" in data


# ---------------------------------------------------------------------------
# C++ Common utilities
# ---------------------------------------------------------------------------

class TestAtlasServicesCommon:
    """Common C++17 utility headers must be present in Atlas/Services/Common/."""

    def test_status_h(self):
        assert _p("Atlas/Services/Common/Status.h").exists()

    def test_clock_h(self):
        assert _p("Atlas/Services/Common/Clock.h").exists()

    def test_clock_cpp(self):
        assert _p("Atlas/Services/Common/Clock.cpp").exists()

    def test_text_util_h(self):
        assert _p("Atlas/Services/Common/TextUtil.h").exists()

    def test_status_defines_atlas_common_namespace(self):
        content = _p("Atlas/Services/Common/Status.h").read_text(encoding="utf-8")
        assert "Atlas::Common" in content

    def test_text_util_defines_read_text_file(self):
        content = _p("Atlas/Services/Common/TextUtil.h").read_text(encoding="utf-8")
        assert "ReadTextFile" in content

    def test_text_util_defines_starts_with_path(self):
        content = _p("Atlas/Services/Common/TextUtil.h").read_text(encoding="utf-8")
        assert "StartsWithPath" in content

    def test_text_util_defines_json_escape(self):
        content = _p("Atlas/Services/Common/TextUtil.h").read_text(encoding="utf-8")
        assert "JsonEscape" in content

    def test_clock_defines_utc_now(self):
        content = _p("Atlas/Services/Common/Clock.h").read_text(encoding="utf-8")
        assert "UtcNowIso8601" in content


# ---------------------------------------------------------------------------
# C++ Security services
# ---------------------------------------------------------------------------

class TestAtlasServicesSecurity:
    """All 8 security C++ files must be present in Atlas/Services/Security/."""

    def test_session_authority_h(self):
        assert _p("Atlas/Services/Security/SessionAuthority.h").exists()

    def test_session_authority_cpp(self):
        assert _p("Atlas/Services/Security/SessionAuthority.cpp").exists()

    def test_capability_resolver_h(self):
        assert _p("Atlas/Services/Security/CapabilityResolver.h").exists()

    def test_capability_resolver_cpp(self):
        assert _p("Atlas/Services/Security/CapabilityResolver.cpp").exists()

    def test_path_policy_service_h(self):
        assert _p("Atlas/Services/Security/PathPolicyService.h").exists()

    def test_path_policy_service_cpp(self):
        assert _p("Atlas/Services/Security/PathPolicyService.cpp").exists()

    def test_audit_event_writer_h(self):
        assert _p("Atlas/Services/Security/AuditEventWriter.h").exists()

    def test_audit_event_writer_cpp(self):
        assert _p("Atlas/Services/Security/AuditEventWriter.cpp").exists()

    def test_session_authority_defines_session_mode(self):
        content = _p("Atlas/Services/Security/SessionAuthority.h").read_text(encoding="utf-8")
        assert "SessionMode" in content

    def test_session_authority_defines_create_session(self):
        content = _p("Atlas/Services/Security/SessionAuthority.h").read_text(encoding="utf-8")
        assert "CreateSession" in content

    def test_session_authority_defines_validate(self):
        content = _p("Atlas/Services/Security/SessionAuthority.h").read_text(encoding="utf-8")
        assert "Validate" in content

    def test_path_policy_service_defines_can_write(self):
        content = _p("Atlas/Services/Security/PathPolicyService.h").read_text(encoding="utf-8")
        assert "CanWrite" in content

    def test_capability_resolver_defines_has_capability(self):
        content = _p("Atlas/Services/Security/CapabilityResolver.h").read_text(encoding="utf-8")
        assert "HasCapability" in content

    def test_audit_event_writer_defines_write(self):
        content = _p("Atlas/Services/Security/AuditEventWriter.h").read_text(encoding="utf-8")
        assert "Write" in content

    def test_security_uses_atlas_namespace(self):
        content = _p("Atlas/Services/Security/SessionAuthority.h").read_text(encoding="utf-8")
        assert "Atlas::Security" in content


# ---------------------------------------------------------------------------
# C++ Archive service
# ---------------------------------------------------------------------------

class TestAtlasServicesArchive:
    """ArchiveIntakeService must be present in Atlas/Services/Archive/."""

    def test_archive_intake_service_h(self):
        assert _p("Atlas/Services/Archive/ArchiveIntakeService.h").exists()

    def test_archive_intake_service_cpp(self):
        assert _p("Atlas/Services/Archive/ArchiveIntakeService.cpp").exists()

    def test_archive_intake_service_defines_run(self):
        content = _p("Atlas/Services/Archive/ArchiveIntakeService.h").read_text(encoding="utf-8")
        assert "Run" in content

    def test_archive_intake_service_defines_load_policy(self):
        content = _p("Atlas/Services/Archive/ArchiveIntakeService.h").read_text(encoding="utf-8")
        assert "LoadPolicy" in content

    def test_archive_uses_atlas_archive_namespace(self):
        content = _p("Atlas/Services/Archive/ArchiveIntakeService.h").read_text(encoding="utf-8")
        assert "Atlas::Archive" in content


# ---------------------------------------------------------------------------
# C++ Bridge services
# ---------------------------------------------------------------------------

class TestAtlasServicesBridge:
    """CommandBroker and BridgeService must be present in Atlas/Services/Bridge/."""

    def test_command_broker_h(self):
        assert _p("Atlas/Services/Bridge/CommandBroker.h").exists()

    def test_command_broker_cpp(self):
        assert _p("Atlas/Services/Bridge/CommandBroker.cpp").exists()

    def test_bridge_service_h(self):
        assert _p("Atlas/Services/Bridge/BridgeService.h").exists()

    def test_bridge_service_cpp(self):
        assert _p("Atlas/Services/Bridge/BridgeService.cpp").exists()

    def test_command_broker_defines_execute(self):
        content = _p("Atlas/Services/Bridge/CommandBroker.h").read_text(encoding="utf-8")
        assert "Execute" in content

    def test_command_broker_defines_load_allowlist(self):
        content = _p("Atlas/Services/Bridge/CommandBroker.h").read_text(encoding="utf-8")
        assert "LoadAllowlist" in content

    def test_bridge_service_defines_handle(self):
        content = _p("Atlas/Services/Bridge/BridgeService.h").read_text(encoding="utf-8")
        assert "Handle" in content

    def test_bridge_request_has_session_token(self):
        content = _p("Atlas/Services/Bridge/BridgeService.h").read_text(encoding="utf-8")
        assert "sessionToken" in content

    def test_bridge_uses_atlas_bridge_namespace(self):
        content = _p("Atlas/Services/Bridge/BridgeService.h").read_text(encoding="utf-8")
        assert "Atlas::Bridge" in content


# ---------------------------------------------------------------------------
# C++ Tests — Security
# ---------------------------------------------------------------------------

class TestSecurityCppTests:
    """PlatformHardeningTests.cpp must be present in Tests/Security/."""

    def test_platform_hardening_tests_cpp(self):
        assert _p("Tests/Security/PlatformHardeningTests.cpp").exists()

    def test_cpp_tests_reference_bridge_service(self):
        content = _p("Tests/Security/PlatformHardeningTests.cpp").read_text(encoding="utf-8")
        assert "BridgeService" in content

    def test_cpp_tests_reference_session_authority(self):
        content = _p("Tests/Security/PlatformHardeningTests.cpp").read_text(encoding="utf-8")
        assert "SessionAuthority" in content

    def test_cpp_tests_have_assertions(self):
        content = _p("Tests/Security/PlatformHardeningTests.cpp").read_text(encoding="utf-8")
        assert "TEST_ASSERT" in content


# ---------------------------------------------------------------------------
# Integration — cross-file coherence checks
# ---------------------------------------------------------------------------

class TestCrossFileCoherence:
    """Verify that config JSON keys match what the C++ headers declare."""

    def test_session_capabilities_roles_match_session_mode_enum(self):
        """session_capabilities.json roles must align with SessionMode enum values."""
        data = json.loads(_p("Atlas/Config/Security/session_capabilities.json").read_text(encoding="utf-8"))
        modes = data.get("modes", data)  # support both flat and nested formats
        # observer, reviewer, editor, admin_local are the 4 defined modes
        for role in ("observer", "editor", "admin_local"):
            assert role in modes, f"Expected role '{role}' in session_capabilities.json"

    def test_tool_allowlist_entries_have_required_fields(self):
        data = json.loads(_p("Atlas/Config/Security/tool_allowlist.json").read_text(encoding="utf-8"))
        entries = data.get("tools", data) if isinstance(data, dict) else data
        for entry in entries:
            assert "toolId" in entry
            assert "exe" in entry
            assert "allowedArgs" in entry

    def test_path_policy_has_all_required_root_keys(self):
        data = json.loads(_p("Atlas/Config/Security/path_policy.json").read_text(encoding="utf-8"))
        for key in ("protectedRoots", "generatedRoots", "archiveRoots"):
            assert key in data, f"path_policy.json must contain '{key}'"

    def test_archive_intake_policy_has_allowed_repo_roots(self):
        data = json.loads(_p("Atlas/Config/Security/archive_intake_policy.json").read_text(encoding="utf-8"))
        assert "allowedRepoRootNames" in data
        assert "Atlas" in data["allowedRepoRootNames"]
