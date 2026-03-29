#include "archive/ArchiveIntakeService.h"
#include "bridge/BridgeService.h"
#include "security/AuditEventWriter.h"
#include "security/CapabilityResolver.h"
#include "security/PathPolicyService.h"
#include "security/SessionAuthority.h"

#include <filesystem>
#include <fstream>
#include <iostream>

namespace fs = std::filesystem;

static int g_failures = 0;

#define TEST_ASSERT(expr) do { if (!(expr)) { ++g_failures; std::cerr << "Assertion failed: " #expr << " at line " << __LINE__ << "\n"; } } while (0)

int main() {
    const fs::path root = fs::temp_directory_path() / "platform_hardening_pack_tests";
    std::error_code ec;
    fs::remove_all(root, ec);
    fs::create_directories(root / "config");
    fs::create_directories(root / "AuditLogs");
    fs::create_directories(root / "Archive");
    fs::create_directories(root / "Atlas");
    fs::create_directories(root / "Generated");

    {
        std::ofstream(root / "config/path_policy.json") << "{\"protectedRoots\":[\"/Atlas\"],\"generatedRoots\":[\"/Generated\"],\"archiveRoots\":[\"/Archive\"],\"sandboxRoots\":[\"/Local\"],\"externalSyncRoots\":[\"/ExternalSync\"]}";
        std::ofstream(root / "config/session_capabilities.json") << "{\"observer\":[\"read_repo\"],\"editor\":[\"read_repo\",\"write_generated\",\"archive_intake\",\"run_build\"],\"admin_local\":[\"*\"]}";
        std::ofstream(root / "config/tool_allowlist.json") << "[{\"toolId\":\"cmake_build\",\"exe\":\"cmake.exe\",\"allowedArgs\":[\"--build\",\"--preset\",\"--config\"],\"networkAccess\":false}]";
        std::ofstream(root / "config/archive_intake_policy.json") << "{\"autoExtractZips\":true,\"quarantine\":true,\"generateReports\":true,\"allowedRepoRootNames\":[\"Atlas\",\"Archive\"]}";
    }

    Atlas::Security::SessionAuthority sessionAuthority;
    Atlas::Security::CapabilityResolver capabilityResolver;
    Atlas::Security::PathPolicyService pathPolicyService;
    Atlas::Security::AuditEventWriter auditWriter(root / "AuditLogs");
    Atlas::Archive::ArchiveIntakeService archiveIntakeService;
    Atlas::Bridge::CommandBroker commandBroker;

    TEST_ASSERT(capabilityResolver.LoadFromFile((root / "config/session_capabilities.json").string()));
    TEST_ASSERT(pathPolicyService.LoadFromFile(root / "config/path_policy.json"));
    TEST_ASSERT(archiveIntakeService.LoadPolicy(root / "config/archive_intake_policy.json"));
    TEST_ASSERT(commandBroker.LoadAllowlist(root / "config/tool_allowlist.json"));

    TEST_ASSERT(!pathPolicyService.CanWrite("/Atlas/Core/file.cpp", false));
    TEST_ASSERT(pathPolicyService.CanWrite("/Generated/Autogen/file.cpp", false));

    const std::string token = sessionAuthority.CreateSession(Atlas::Security::SessionMode::Editor,
                                                             {"write_generated", "archive_intake", "run_build"},
                                                             "local-machine", "tester", std::chrono::minutes(10), true);

    Atlas::Bridge::BridgeService bridge(sessionAuthority, capabilityResolver, pathPolicyService,
                                        auditWriter, archiveIntakeService, commandBroker);

    auto denied = bridge.Handle({token, "corr-1", "write_generated", "write_file", "/Atlas/Core/file.cpp", true, false, std::nullopt, false, {}, {}});
    TEST_ASSERT(!denied.status.ok);

    auto allowed = bridge.Handle({token, "corr-2", "write_generated", "write_file", "/Generated/out.cpp", true, false, std::nullopt, false, {}, {}});
    TEST_ASSERT(allowed.status.ok);

    Atlas::Bridge::CommandRequest cmd;
    cmd.toolId = "cmake_build";
    cmd.args = {"--build", "--config"};
    cmd.dryRun = true;
    auto cmdResp = bridge.Handle({token, "corr-3", "run_build", "run_command", "/Generated/out.cpp", true, false, cmd, false, {}, {}});
    TEST_ASSERT(cmdResp.status.ok);
    TEST_ASSERT(cmdResp.detail.find("cmake.exe") != std::string::npos);

    std::ofstream(root / "rogue_notes.md") << "hello";
    std::ofstream(root / "drop.zip") << "fake zip bytes";
    auto intakeResp = bridge.Handle({token, "corr-4", "archive_intake", "archive_intake", "/Archive", true, false, std::nullopt, true, root, root / "Archive"});
    TEST_ASSERT(intakeResp.status.ok);
    TEST_ASSERT(fs::exists(root / "Archive/Audit/archive_intake_manifest.json"));
    TEST_ASSERT(fs::exists(root / "Archive/Audit/archive_audit_report.md"));

    if (g_failures == 0) {
        std::cout << "All PlatformHardeningTests passed\n";
        return 0;
    }

    std::cerr << g_failures << " test assertions failed\n";
    return 1;
}
