#pragma once

#include "archive/ArchiveIntakeService.h"
#include "bridge/CommandBroker.h"
#include "security/AuditEventWriter.h"
#include "security/CapabilityResolver.h"
#include "security/PathPolicyService.h"
#include "security/SessionAuthority.h"

#include <filesystem>
#include <optional>
#include <string>

namespace Atlas::Bridge {

struct BridgeRequest {
    std::string sessionToken;
    std::string correlationId;
    std::string capability;
    std::string action;
    std::filesystem::path targetPath;
    bool dryRun{true};
    bool reviewedDiffApproved{false};
    std::optional<CommandRequest> command;
    bool runArchiveIntake{false};
    std::filesystem::path repoRoot;
    std::filesystem::path archiveRoot;
};

struct BridgeResponse {
    Atlas::Common::Status status;
    std::string detail;
};

class BridgeService {
public:
    BridgeService(Atlas::Security::SessionAuthority& sessionAuthority,
                  Atlas::Security::CapabilityResolver& capabilityResolver,
                  Atlas::Security::PathPolicyService& pathPolicyService,
                  Atlas::Security::AuditEventWriter& auditWriter,
                  Atlas::Archive::ArchiveIntakeService& archiveIntakeService,
                  Atlas::Bridge::CommandBroker& commandBroker);

    BridgeResponse Handle(const BridgeRequest& request);

private:
    Atlas::Security::SessionAuthority& sessionAuthority_;
    Atlas::Security::CapabilityResolver& capabilityResolver_;
    Atlas::Security::PathPolicyService& pathPolicyService_;
    Atlas::Security::AuditEventWriter& auditWriter_;
    Atlas::Archive::ArchiveIntakeService& archiveIntakeService_;
    Atlas::Bridge::CommandBroker& commandBroker_;
};

} // namespace Atlas::Bridge
