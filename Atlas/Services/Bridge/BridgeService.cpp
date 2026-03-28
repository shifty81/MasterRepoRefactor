#include "bridge/BridgeService.h"

#include "common/Clock.h"

namespace Atlas::Bridge {

BridgeService::BridgeService(Atlas::Security::SessionAuthority& sessionAuthority,
                             Atlas::Security::CapabilityResolver& capabilityResolver,
                             Atlas::Security::PathPolicyService& pathPolicyService,
                             Atlas::Security::AuditEventWriter& auditWriter,
                             Atlas::Archive::ArchiveIntakeService& archiveIntakeService,
                             Atlas::Bridge::CommandBroker& commandBroker)
    : sessionAuthority_(sessionAuthority)
    , capabilityResolver_(capabilityResolver)
    , pathPolicyService_(pathPolicyService)
    , auditWriter_(auditWriter)
    , archiveIntakeService_(archiveIntakeService)
    , commandBroker_(commandBroker) {
}

BridgeResponse BridgeService::Handle(const BridgeRequest& request) {
    Atlas::Security::AuditRecord audit;
    audit.timestampUtc = Atlas::Common::UtcNowIso8601();
    audit.action = request.action;
    audit.capability = request.capability;
    audit.correlationId = request.correlationId;
    audit.dryRun = request.dryRun;
    if (!request.targetPath.empty()) {
        audit.targetRoots.push_back(request.targetPath.string());
    }

    const auto session = sessionAuthority_.Validate(request.sessionToken);
    if (!session.has_value()) {
        audit.message = "invalid or expired session";
        audit.success = false;
        auditWriter_.Write(audit);
        return {Atlas::Common::Status::Error(audit.message), audit.message};
    }

    audit.sessionId = session->token;
    audit.userIdentity = session->userIdentity;
    audit.machineIdentity = session->machineIdentity;

    if (!capabilityResolver_.HasCapability(ToString(session->mode), session->capabilities, request.capability, session->writeElevation)) {
        audit.message = "capability denied";
        audit.success = false;
        auditWriter_.Write(audit);
        return {Atlas::Common::Status::Error(audit.message), audit.message};
    }

    if (!request.targetPath.empty() && !pathPolicyService_.CanRead(request.targetPath)) {
        audit.message = "path outside managed roots";
        audit.success = false;
        auditWriter_.Write(audit);
        return {Atlas::Common::Status::Error(audit.message), audit.message};
    }

    if (!request.targetPath.empty() && request.capability.rfind("write_", 0) == 0) {
        if (!pathPolicyService_.CanWrite(request.targetPath, request.reviewedDiffApproved)) {
            audit.message = "write denied by path policy";
            audit.success = false;
            auditWriter_.Write(audit);
            return {Atlas::Common::Status::Error(audit.message), audit.message};
        }
    }

    if (request.command.has_value()) {
        const auto commandResult = commandBroker_.Execute(*request.command);
        audit.message = commandResult.status.message;
        audit.success = commandResult.status.ok;
        auditWriter_.Write(audit);
        return {commandResult.status, commandResult.commandLine};
    }

    if (request.runArchiveIntake) {
        Atlas::Archive::IntakeRunResult intakeResult;
        const auto status = archiveIntakeService_.Run(request.repoRoot, request.archiveRoot, &intakeResult);
        audit.message = status.message;
        audit.success = status.ok;
        audit.targetRoots.push_back(intakeResult.manifestPath.string());
        audit.targetRoots.push_back(intakeResult.reportPath.string());
        auditWriter_.Write(audit);
        return {status, intakeResult.reportPath.string()};
    }

    audit.message = "request accepted";
    audit.success = true;
    auditWriter_.Write(audit);
    return {Atlas::Common::Status::Ok("request accepted"), "accepted"};
}

} // namespace Atlas::Bridge
