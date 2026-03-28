// ArbiterBridgeService.cpp
// NovaForge-side Arbiter bridge service implementation.

#include "ArbiterBridgeService.h"
#include "BridgeSessionManager.h"

#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <atomic>
#include <mutex>

namespace NovaForge::Integration::Arbiter
{

// ============================================================
// Internal implementation state
// ============================================================

struct ArbiterBridgeService::Impl
{
    BridgeSessionManager sessionManager;

    // Allowed tool action IDs (original whitelist)
    std::unordered_set<uint32_t> allowedActionIds =
    {
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::ValidateData),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::RunPCGPreview),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::OpenScene),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::FocusEntity),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::RegenerateSchemas),
    };

    // Allowed builder tool action IDs (Epic 10 / Task 10.2)
    std::unordered_set<uint32_t> allowedBuilderActionIds =
    {
        static_cast<uint32_t>(::Arbiter::Bridge::BuilderToolActionId::ValidateData),
        static_cast<uint32_t>(::Arbiter::Bridge::BuilderToolActionId::RunPCGPreview),
        static_cast<uint32_t>(::Arbiter::Bridge::BuilderToolActionId::OpenScene),
        static_cast<uint32_t>(::Arbiter::Bridge::BuilderToolActionId::FocusEntity),
        static_cast<uint32_t>(::Arbiter::Bridge::BuilderToolActionId::RegenerateSchemas),
        static_cast<uint32_t>(::Arbiter::Bridge::BuilderToolActionId::RunBuilderInspect),
        static_cast<uint32_t>(::Arbiter::Bridge::BuilderToolActionId::RunPCGDiagnostics),
        static_cast<uint32_t>(::Arbiter::Bridge::BuilderToolActionId::GeneratePCGPreview),
        static_cast<uint32_t>(::Arbiter::Bridge::BuilderToolActionId::ValidateBuilderData),
    };

    std::atomic<uint32_t> buildIdCounter{0};
    std::atomic<uint32_t> proposalIdCounter{0};

    // Dashboard tracking — updated on each build/tool call
    mutable std::mutex dashboardMutex;
    std::string  lastBuildTarget;
    std::string  lastBuildId;
    bool         lastBuildSucceeded     = false;
    std::string  lastBuildTimestampUtc;
    std::string  lastToolAction;
    std::string  lastToolTimestampUtc;

    // Pending codegen proposals (proposalId → request snapshot)
    std::unordered_map<std::string, ::Arbiter::Bridge::CodegenProposalRequest> pendingProposals;
};

// ============================================================
// Lifecycle
// ============================================================

ArbiterBridgeService::ArbiterBridgeService()
    : m_impl(std::make_unique<Impl>())
{
}

ArbiterBridgeService::~ArbiterBridgeService()
{
    stop();
}

bool ArbiterBridgeService::start(const BridgeServiceConfig& config)
{
    if (m_running)
    {
        log("ArbiterBridgeService: already running");
        return false;
    }

    m_config  = config;
    m_running = true;

    log("ArbiterBridgeService: started — REST port "
        + std::to_string(config.restPort)
        + ", WS port "
        + std::to_string(config.wsPort)
        + (config.bindLoopbackOnly ? " [loopback-only]" : " [WARNING: open binding]"));

    return true;
}

void ArbiterBridgeService::stop()
{
    if (!m_running)
        return;

    m_impl->sessionManager.revokeAll();
    m_running = false;
    log("ArbiterBridgeService: stopped — all sessions revoked");
}

bool ArbiterBridgeService::isRunning() const
{
    return m_running;
}

// ============================================================
// Logging and audit
// ============================================================

void ArbiterBridgeService::setLogCallback(BridgeLogCallback callback)
{
    m_logCallback = std::move(callback);
}

void ArbiterBridgeService::setAuditLogger(BridgeAuditLogger* logger)
{
    m_auditLogger = logger;
}

void ArbiterBridgeService::log(const std::string& message)
{
    if (m_logCallback)
        m_logCallback(message);
}

void ArbiterBridgeService::auditLog(
    const std::string& requestId,
    const std::string& sessionId,
    const std::string& service,
    const std::string& operation,
    bool               success,
    const std::string& summary,
    bool               wasDryRun,
    const std::string& failReason) const
{
    if (m_auditLogger)
    {
        m_auditLogger->log(
            requestId, sessionId, service, operation,
            success, summary, wasDryRun, failReason);
    }
}

// ============================================================
// Session management  (Task 4.1 prerequisite)
// ============================================================

::Arbiter::Bridge::SessionConnectResponse ArbiterBridgeService::connectSession(
    const ::Arbiter::Bridge::SessionConnectRequest& request)
{
    if (!m_running)
    {
        ::Arbiter::Bridge::SessionConnectResponse response;
        response.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        response.result.message   = "Bridge service is not running";
        return response;
    }

    auto response = m_impl->sessionManager.createSession(
        request, ::Arbiter::Bridge::kProtocolVersion);

    if (response.result.succeeded())
    {
        log("ArbiterBridgeService: session connected — project=" + request.projectId
            + " token=" + response.sessionToken.substr(0, 8) + "...");
        auditLog({}, {}, "SessionService", "Connect",
                 true, "Session created for project=" + request.projectId);
    }
    else
    {
        log("ArbiterBridgeService: session connect failed — " + response.result.message);
        auditLog({}, {}, "SessionService", "Connect",
                 false, "Session create failed",
                 false, response.result.message);
    }

    return response;
}

::Arbiter::Bridge::BridgeResult ArbiterBridgeService::disconnectSession(
    const std::string& sessionToken)
{
    ::Arbiter::Bridge::BridgeResult result;

    if (!m_impl->sessionManager.validateToken(sessionToken))
    {
        result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        result.message   = "Invalid or expired session token";
        return result;
    }

    m_impl->sessionManager.revokeSession(sessionToken);
    log("ArbiterBridgeService: session disconnected");
    auditLog({}, sessionToken, "SessionService", "Disconnect",
             true, "Session revoked");

    result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    result.message   = "Session disconnected";
    return result;
}

// ============================================================
// Session validation helpers
// ============================================================

bool ArbiterBridgeService::validateSession(const std::string& token) const
{
    return m_impl->sessionManager.validateToken(token);
}

bool ArbiterBridgeService::validateWriteSession(const std::string& token) const
{
    return m_impl->sessionManager.isWriteAuthorized(token);
}

// ============================================================
// Project info  GET /project/info  (Task 4.1)
// ============================================================

::Arbiter::Bridge::ProjectInfo ArbiterBridgeService::getProjectInfo(
    const std::string& sessionToken) const
{
    ::Arbiter::Bridge::ProjectInfo info;

    if (!validateSession(sessionToken))
    {
        // Return a minimal error indicator via the projectId field;
        // callers should check validateSession before calling this.
        info.projectId = "__unauthorized__";
        return info;
    }

    info.projectId   = "novaforge";
    info.displayName = "NovaForge";
    info.version     = "0.1.0";
    info.repoRoot    = ""; // populated at runtime from manifest path

    info.capabilities.supportsViewportAttach   = false;
    info.capabilities.supportsLivePatch        = false;
    info.capabilities.supportsAISession        = true;
    info.capabilities.supportsProjectIndexing  = true;
    info.capabilities.supportsMultiWorkspace   = false;

    return info;
}

// ============================================================
// Build  POST /build/run  (Task 4.3)
// ============================================================

::Arbiter::Bridge::BuildResult ArbiterBridgeService::runBuild(
    const std::string&                    sessionToken,
    const ::Arbiter::Bridge::BuildTarget& target)
{
    ::Arbiter::Bridge::BuildResult result;

    if (!m_running)
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        result.result.message   = "Bridge service is not running";
        auditLog({}, sessionToken, "BuildService", "RunBuild",
                 false, "Service not running", false, result.result.message);
        return result;
    }

    if (!validateSession(sessionToken))
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        result.result.message   = "Invalid or expired session token";
        auditLog({}, sessionToken, "BuildService", "RunBuild",
                 false, "Unauthorized", false, result.result.message);
        return result;
    }

    const uint32_t buildId = ++m_impl->buildIdCounter;
    result.buildId = "build-" + std::to_string(buildId);

    log("ArbiterBridgeService: build requested — target=" + target.name
        + " buildId=" + result.buildId);

    // TODO: integrate with actual build system (CMake/MSBuild dispatch)
    result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    result.result.message   = "Build queued";
    result.exitCode         = 0;
    result.outputLog        = "Build stub: target '" + target.name + "' queued with id "
                              + result.buildId;

    // Update dashboard tracking
    {
        std::lock_guard<std::mutex> lk(m_impl->dashboardMutex);
        m_impl->lastBuildTarget       = target.name;
        m_impl->lastBuildId           = result.buildId;
        m_impl->lastBuildSucceeded    = true;
        m_impl->lastBuildTimestampUtc = m_impl->sessionManager.utcNowIso8601();
    }

    auditLog({}, sessionToken, "BuildService", "RunBuild",
             true, "Queued target=" + target.name + " id=" + result.buildId);

    return result;
}

// ============================================================
// Editor selection  GET /editor/selection  (Task 4.2)
// ============================================================

::Arbiter::Bridge::EditorSelectionSnapshot ArbiterBridgeService::getEditorSelection(
    const std::string& sessionToken) const
{
    ::Arbiter::Bridge::EditorSelectionSnapshot snapshot;

    if (!validateSession(sessionToken))
        return snapshot; // empty snapshot — caller checks session separately

    // TODO: integrate with Atlas editor backend to retrieve live selection
    snapshot.activeScene        = "";
    snapshot.selectedObjectName = "";
    snapshot.selectedObjectType = "";
    snapshot.selectedObjectId   = 0;

    return snapshot;
}

// ============================================================
// File operations
// ============================================================

::Arbiter::Bridge::BridgeResult ArbiterBridgeService::openFile(
    const std::string&                        sessionToken,
    const ::Arbiter::Bridge::OpenFileRequest& request)
{
    ::Arbiter::Bridge::BridgeResult result;

    if (!m_running)
    {
        result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        result.message   = "Bridge service is not running";
        return result;
    }

    if (!validateSession(sessionToken))
    {
        result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        result.message   = "Invalid or expired session token";
        auditLog({}, sessionToken, "EditorService", "OpenFile",
                 false, "Unauthorized", false, result.message);
        return result;
    }

    log("ArbiterBridgeService: open file — " + request.filePath);

    // TODO: integrate with editor open-file command
    result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    result.message   = "Open file stub: not yet implemented";

    auditLog({}, sessionToken, "EditorService", "OpenFile",
             true, "Requested file=" + request.filePath);

    return result;
}

// ============================================================
// Tool actions  POST /editor/tools/run  (Task 4.4)
// ============================================================

bool ArbiterBridgeService::isToolActionAllowed(
    ::Arbiter::Bridge::ToolActionId actionId) const
{
    return m_impl->allowedActionIds.count(
        static_cast<uint32_t>(actionId)) > 0;
}

::Arbiter::Bridge::ToolActionResult ArbiterBridgeService::runToolAction(
    const std::string&                              sessionToken,
    const ::Arbiter::Bridge::ToolActionRequest&     request)
{
    ::Arbiter::Bridge::ToolActionResult result;
    result.wasDryRun = request.dryRun;

    if (!m_running)
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        result.result.message   = "Bridge service is not running";
        auditLog({}, sessionToken, "ToolService", "RunToolAction",
                 false, "Service not running", request.dryRun, result.result.message);
        return result;
    }

    if (!validateSession(sessionToken))
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        result.result.message   = "Invalid or expired session token";
        auditLog({}, sessionToken, "ToolService", "RunToolAction",
                 false, "Unauthorized", request.dryRun, result.result.message);
        return result;
    }

    // Require write authorization for non-dry-run actions
    if (!request.dryRun && !validateWriteSession(sessionToken))
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        result.result.message   = "Write authorization required for non-dry-run actions";
        auditLog({}, sessionToken, "ToolService", "RunToolAction",
                 false, "Write auth required", false, result.result.message);
        return result;
    }

    if (!isToolActionAllowed(request.actionId))
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::UnsupportedOp;
        result.result.message   = "Tool action is not in the whitelist";
        auditLog({}, sessionToken, "ToolService", "RunToolAction",
                 false,
                 "Denied action id=" + std::to_string(
                     static_cast<uint32_t>(request.actionId)),
                 request.dryRun,
                 result.result.message);
        return result;
    }

    const std::string actionIdStr =
        std::to_string(static_cast<uint32_t>(request.actionId));

    // Derive a human-readable name for dashboard tracking
    static const char* kActionNames[] = {
        "ValidateData", "RunPCGPreview", "OpenScene", "FocusEntity", "RegenerateSchemas"
    };
    const std::string actionName =
        (static_cast<uint32_t>(request.actionId) < 5u)
            ? kActionNames[static_cast<uint32_t>(request.actionId)]
            : actionIdStr;

    log("ArbiterBridgeService: tool action id=" + actionIdStr
        + (request.dryRun ? " [DRY RUN]" : " [EXECUTE]"));

    // Update dashboard tracking
    {
        std::lock_guard<std::mutex> lk(m_impl->dashboardMutex);
        m_impl->lastToolAction       = actionName;
        m_impl->lastToolTimestampUtc = m_impl->sessionManager.utcNowIso8601();
    }

    if (request.dryRun)
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
        result.result.message   = "Dry-run: action would be permitted";
        result.summary          = "dry-run completed";
        auditLog({}, sessionToken, "ToolService", "RunToolAction",
                 true, "Dry-run id=" + actionIdStr, true);
        return result;
    }

    // TODO: route to actual editor tool implementations
    result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    result.result.message   = "Tool action stub: not yet implemented";
    result.summary          = "stub executed";

    auditLog({}, sessionToken, "ToolService", "RunToolAction",
             true, "Executed id=" + actionIdStr, false);

    return result;
}

// ============================================================
// Epic 10 / Task 10.2 — Builder / PCG tool validation helper
// ============================================================

bool ArbiterBridgeService::isBuilderToolActionAllowed(
    ::Arbiter::Bridge::BuilderToolActionId actionId) const
{
    return m_impl->allowedBuilderActionIds.count(
        static_cast<uint32_t>(actionId)) > 0;
}

// ============================================================
// Epic 10 / Task 10.1 — Search roots  GET /project/search-roots
// ============================================================

::Arbiter::Bridge::ProjectSearchRoots ArbiterBridgeService::getSearchRoots(
    const std::string& sessionToken) const
{
    ::Arbiter::Bridge::ProjectSearchRoots roots;

    if (!m_running)
    {
        roots.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        roots.result.message   = "Bridge service is not running";
        return roots;
    }

    if (!validateSession(sessionToken))
    {
        roots.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        roots.result.message   = "Invalid or expired session token";
        return roots;
    }

    // Populate the standard NovaForge search roots (from project manifest layout)
    roots.roots =
    {
        { "Docs",              "Docs",             "docs"    },
        { "DataTables",        "NovaForge/Data",   "data"    },
        { "Content",           "NovaForge/Content","content" },
        { "Config",            "NovaForge/Data/Config", "config" },
        { "SourceAtlas",       "Atlas",            "source"  },
        { "SourceNovaForge",   "NovaForge",        "source"  },
        { "SourceArbiter",     "Arbiter",          "source"  },
        { "SharedContracts",   "Shared",           "source"  },
    };

    roots.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    roots.result.message   = "OK";

    auditLog({}, sessionToken, "ProjectService", "GetSearchRoots",
             true, "Returned " + std::to_string(roots.roots.size()) + " search roots");

    return roots;
}

// ============================================================
// Epic 10 / Task 10.2 — Builder / PCG tool hooks
//   POST /editor/tools/builder
// ============================================================

::Arbiter::Bridge::BuilderToolResult ArbiterBridgeService::runBuilderTool(
    const std::string&                           sessionToken,
    const ::Arbiter::Bridge::BuilderToolRequest& request)
{
    ::Arbiter::Bridge::BuilderToolResult result;
    result.wasDryRun = request.dryRun;

    if (!m_running)
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        result.result.message   = "Bridge service is not running";
        return result;
    }

    if (!validateSession(sessionToken))
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        result.result.message   = "Invalid or expired session token";
        return result;
    }

    if (!request.dryRun && !validateWriteSession(sessionToken))
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        result.result.message   = "Write authorization required for non-dry-run builder actions";
        return result;
    }

    if (!isBuilderToolActionAllowed(request.actionId))
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::UnsupportedOp;
        result.result.message   = "Builder tool action is not in the whitelist";
        auditLog({}, sessionToken, "ToolService", "RunBuilderTool",
                 false,
                 "Denied builder action id="
                     + std::to_string(static_cast<uint32_t>(request.actionId)),
                 request.dryRun,
                 result.result.message);
        return result;
    }

    const std::string actionIdStr =
        std::to_string(static_cast<uint32_t>(request.actionId));

    log("ArbiterBridgeService: builder tool action id=" + actionIdStr
        + (request.dryRun ? " [DRY RUN]" : " [EXECUTE]"));

    // Update dashboard tracking
    {
        std::lock_guard<std::mutex> lk(m_impl->dashboardMutex);
        m_impl->lastToolAction       = "Builder:" + actionIdStr;
        m_impl->lastToolTimestampUtc = m_impl->sessionManager.utcNowIso8601();
    }

    if (request.dryRun)
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
        result.result.message   = "Dry-run: builder action would be permitted";
        result.summary          = "dry-run completed";
        result.diagnosticsLog   = "";
        auditLog({}, sessionToken, "ToolService", "RunBuilderTool",
                 true, "Dry-run builder id=" + actionIdStr, true);
        return result;
    }

    // Diagnostic actions populate the log field
    const bool isDiagnostic =
        (request.actionId == ::Arbiter::Bridge::BuilderToolActionId::RunPCGDiagnostics
      || request.actionId == ::Arbiter::Bridge::BuilderToolActionId::RunBuilderInspect);

    result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    result.result.message   = "Builder tool stub: not yet implemented";
    result.summary          = "stub executed";
    result.diagnosticsLog   = isDiagnostic
        ? "[stub] diagnostics output for action " + actionIdStr
        : "";

    auditLog({}, sessionToken, "ToolService", "RunBuilderTool",
             true, "Executed builder id=" + actionIdStr, false);

    return result;
}

// ============================================================
// Epic 10 / Task 10.3 — Richer editor state  GET /editor/state
// ============================================================

::Arbiter::Bridge::EditorStateSnapshot ArbiterBridgeService::getEditorState(
    const std::string& sessionToken) const
{
    ::Arbiter::Bridge::EditorStateSnapshot snap;

    if (!m_running)
    {
        snap.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        snap.result.message   = "Bridge service is not running";
        return snap;
    }

    if (!validateSession(sessionToken))
    {
        snap.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        snap.result.message   = "Invalid or expired session token";
        return snap;
    }

    // TODO: integrate with Atlas editor runtime to retrieve live state
    snap.result.errorCode       = ::Arbiter::Bridge::BridgeErrorCode::Success;
    snap.activeScene            = "";  // populated by Atlas editor integration
    snap.activeMap              = "";
    snap.loadedWorldId          = "";
    snap.activeMode             = "Inspect"; // default editor mode
    snap.simulationState        = ::Arbiter::Bridge::SimulationState::Stopped;
    snap.selectedObjectName     = "";
    snap.selectedObjectType     = "";
    snap.selectedObjectId       = 0;
    snap.selectedComponents     = {};

    auditLog({}, sessionToken, "EditorService", "GetEditorState",
             true, "Editor state snapshot returned");

    return snap;
}

// ============================================================
// Epic 10 / Task 10.4 — Codegen workflow
// ============================================================

::Arbiter::Bridge::CodegenProposal ArbiterBridgeService::proposeCodegen(
    const std::string&                               sessionToken,
    const ::Arbiter::Bridge::CodegenProposalRequest& request)
{
    ::Arbiter::Bridge::CodegenProposal proposal;

    if (!m_running)
    {
        proposal.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        proposal.result.message   = "Bridge service is not running";
        return proposal;
    }

    if (!validateSession(sessionToken))
    {
        proposal.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        proposal.result.message   = "Invalid or expired session token";
        return proposal;
    }

    if (request.targetFile.empty())
    {
        proposal.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::InvalidRequest;
        proposal.result.message   = "targetFile must not be empty";
        return proposal;
    }

    const uint32_t pid = ++m_impl->proposalIdCounter;
    proposal.proposalId  = "proposal-" + std::to_string(pid);
    proposal.description = request.description;
    proposal.targetFile  = request.targetFile;
    proposal.summary     = "[stub] Proposal to change " + request.targetFile
                           + ": " + request.description;

    // Store for diff and approval look-up
    {
        std::lock_guard<std::mutex> lk(m_impl->dashboardMutex);
        m_impl->pendingProposals[proposal.proposalId] = request;
    }

    proposal.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    proposal.result.message   = "Proposal created";

    log("ArbiterBridgeService: codegen proposed — id=" + proposal.proposalId
        + " file=" + request.targetFile);

    auditLog({}, sessionToken, "CodegenService", "ProposeCodegen",
             true, "proposal=" + proposal.proposalId + " file=" + request.targetFile,
             request.dryRun);

    return proposal;
}

::Arbiter::Bridge::CodegenDiff ArbiterBridgeService::getCodegenDiff(
    const std::string& sessionToken,
    const std::string& proposalId) const
{
    ::Arbiter::Bridge::CodegenDiff diff;

    if (!m_running)
    {
        diff.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        diff.result.message   = "Bridge service is not running";
        return diff;
    }

    if (!validateSession(sessionToken))
    {
        diff.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        diff.result.message   = "Invalid or expired session token";
        return diff;
    }

    std::lock_guard<std::mutex> lk(m_impl->dashboardMutex);
    auto it = m_impl->pendingProposals.find(proposalId);
    if (it == m_impl->pendingProposals.end())
    {
        diff.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::NotFound;
        diff.result.message   = "Proposal not found: " + proposalId;
        return diff;
    }

    const auto& req = it->second;

    // Stub diff — in production this would be populated by the AI codegen engine
    diff.proposalId  = proposalId;
    diff.diffText    = "--- a/" + req.targetFile + "\n"
                       "+++ b/" + req.targetFile + "\n"
                       "@@ -0,0 +1,3 @@\n"
                       "+// Generated stub\n"
                       "+// " + req.description + "\n"
                       "+\n";
    diff.linesAdded   = 3;
    diff.linesRemoved = 0;

    diff.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    diff.result.message   = "Diff generated";

    return diff;
}

::Arbiter::Bridge::CodegenApplyResult ArbiterBridgeService::approveAndApplyCodegen(
    const std::string&                               sessionToken,
    const ::Arbiter::Bridge::CodegenApprovalRequest& request)
{
    ::Arbiter::Bridge::CodegenApplyResult applyResult;

    if (!m_running)
    {
        applyResult.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        applyResult.result.message   = "Bridge service is not running";
        return applyResult;
    }

    if (!validateSession(sessionToken))
    {
        applyResult.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        applyResult.result.message   = "Invalid or expired session token";
        return applyResult;
    }

    // Write authorization is only required when actually applying (approved=true);
    // rejection is read-only — it just discards the pending proposal.
    if (request.approved && !validateWriteSession(sessionToken))
    {
        applyResult.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        applyResult.result.message   = "Write authorization required to apply codegen";
        return applyResult;
    }

    std::lock_guard<std::mutex> lk(m_impl->dashboardMutex);
    auto it = m_impl->pendingProposals.find(request.proposalId);
    if (it == m_impl->pendingProposals.end())
    {
        applyResult.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::NotFound;
        applyResult.result.message   = "Proposal not found: " + request.proposalId;
        return applyResult;
    }

    applyResult.proposalId = request.proposalId;
    applyResult.wasApplied = request.approved;

    if (request.approved)
    {
        applyResult.appliedFile      = it->second.targetFile;
        applyResult.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
        applyResult.result.message   = "Proposal applied";

        log("ArbiterBridgeService: codegen applied — proposal=" + request.proposalId
            + " file=" + applyResult.appliedFile);
        auditLog({}, sessionToken, "CodegenService", "ApplyCodegen",
                 true, "applied proposal=" + request.proposalId
                       + " file=" + applyResult.appliedFile);
    }
    else
    {
        applyResult.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
        applyResult.result.message   = "Proposal rejected — no changes made";
        auditLog({}, sessionToken, "CodegenService", "ApplyCodegen",
                 true, "rejected proposal=" + request.proposalId);
    }

    // Remove from pending regardless of outcome
    m_impl->pendingProposals.erase(it);

    return applyResult;
}

// ============================================================
// Epic 10 / Task 10.5 — Workspace dashboard  GET /workspace/dashboard
// ============================================================

::Arbiter::Bridge::WorkspaceDashboard ArbiterBridgeService::getWorkspaceDashboard(
    const std::string& sessionToken) const
{
    ::Arbiter::Bridge::WorkspaceDashboard dash;

    if (!m_running)
    {
        dash.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        dash.result.message   = "Bridge service is not running";
        return dash;
    }

    if (!validateSession(sessionToken))
    {
        dash.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Unauthorized;
        dash.result.message   = "Invalid or expired session token";
        return dash;
    }

    dash.result.errorCode  = ::Arbiter::Bridge::BridgeErrorCode::Success;
    dash.projectId         = "novaforge";
    dash.projectName       = "NovaForge";
    dash.projectVersion    = "0.1.0";
    dash.activeSessionCount =
        m_impl->sessionManager.activeSessionCount();

    // Build health snapshot
    {
        std::lock_guard<std::mutex> lk(m_impl->dashboardMutex);
        dash.buildHealth.lastBuildTarget       = m_impl->lastBuildTarget;
        dash.buildHealth.lastBuildId           = m_impl->lastBuildId;
        dash.buildHealth.lastBuildSucceeded    = m_impl->lastBuildSucceeded;
        dash.buildHealth.lastBuildTimestampUtc = m_impl->lastBuildTimestampUtc;
        dash.lastToolAction                    = m_impl->lastToolAction;
        dash.lastToolTimestampUtc              = m_impl->lastToolTimestampUtc;
    }

    // Search roots — reuse the getSearchRoots logic
    {
        // Temporarily unlock to avoid deadlock; validate token already done above
        dash.searchRoots.roots =
        {
            { "Docs",            "Docs",              "docs"    },
            { "DataTables",      "NovaForge/Data",    "data"    },
            { "Content",         "NovaForge/Content", "content" },
            { "Config",          "NovaForge/Data/Config", "config" },
            { "SourceAtlas",     "Atlas",             "source"  },
            { "SourceNovaForge", "NovaForge",         "source"  },
            { "SourceArbiter",   "Arbiter",           "source"  },
            { "SharedContracts", "Shared",            "source"  },
        };
        dash.searchRoots.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    }

    dash.currentProjectStatus = m_impl->lastBuildTarget.empty() ? "idle" : "idle";

    auditLog({}, sessionToken, "WorkspaceService", "GetDashboard",
             true, "Dashboard returned");

    return dash;
}

} // namespace NovaForge::Integration::Arbiter
