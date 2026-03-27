// ArbiterBridgeService.cpp
// NovaForge-side Arbiter bridge service implementation.

#include "ArbiterBridgeService.h"
#include "BridgeSessionManager.h"

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

    // Allowed tool action IDs
    std::unordered_set<uint32_t> allowedActionIds =
    {
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::ValidateData),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::RunPCGPreview),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::OpenScene),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::FocusEntity),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::RegenerateSchemas),
    };

    std::atomic<uint32_t> buildIdCounter{0};
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
    const std::string& failReason)
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

    log("ArbiterBridgeService: tool action id=" + actionIdStr
        + (request.dryRun ? " [DRY RUN]" : " [EXECUTE]"));

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

} // namespace NovaForge::Integration::Arbiter
