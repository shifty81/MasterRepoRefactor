// ArbiterBridgeService.cpp
// NovaForge-side Arbiter bridge service implementation.

#include "ArbiterBridgeService.h"

#include <unordered_set>

namespace NovaForge::Integration::Arbiter
{

// ============================================================
// Internal implementation state
// ============================================================

struct ArbiterBridgeService::Impl
{
    // Allowed tool action IDs
    std::unordered_set<uint32_t> allowedActionIds =
    {
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::ValidateData),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::RunPCGPreview),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::OpenScene),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::FocusEntity),
        static_cast<uint32_t>(::Arbiter::Bridge::ToolActionId::RegenerateSchemas),
    };
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

    log("ArbiterBridgeService: started on REST port "
        + std::to_string(config.restPort)
        + ", WS port "
        + std::to_string(config.wsPort));

    return true;
}

void ArbiterBridgeService::stop()
{
    if (!m_running)
        return;

    m_running = false;
    log("ArbiterBridgeService: stopped");
}

bool ArbiterBridgeService::isRunning() const
{
    return m_running;
}

// ============================================================
// Logging
// ============================================================

void ArbiterBridgeService::setLogCallback(BridgeLogCallback callback)
{
    m_logCallback = std::move(callback);
}

void ArbiterBridgeService::log(const std::string& message)
{
    if (m_logCallback)
        m_logCallback(message);
}

// ============================================================
// Project info
// ============================================================

::Arbiter::Bridge::ProjectInfo ArbiterBridgeService::getProjectInfo() const
{
    ::Arbiter::Bridge::ProjectInfo info;
    info.projectId   = "novaforge";
    info.displayName = "NovaForge";
    info.version     = "0.1.0";
    info.repoRoot    = ""; // populated by caller from manifest

    info.capabilities.supportsViewportAttach   = false;
    info.capabilities.supportsLivePatch        = false;
    info.capabilities.supportsAISession        = true;
    info.capabilities.supportsProjectIndexing  = true;
    info.capabilities.supportsMultiWorkspace   = false;

    return info;
}

// ============================================================
// Build
// ============================================================

::Arbiter::Bridge::BuildResult ArbiterBridgeService::runBuild(
    const ::Arbiter::Bridge::BuildTarget& target)
{
    ::Arbiter::Bridge::BuildResult result;

    if (!m_running)
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        result.result.message   = "Bridge service is not running";
        return result;
    }

    log("ArbiterBridgeService: build requested — target=" + target.name);

    // TODO: integrate with actual build system
    result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    result.result.message   = "Build stub: not yet implemented";
    result.buildId          = "build-stub-001";
    result.exitCode         = 0;

    return result;
}

// ============================================================
// Editor selection
// ============================================================

::Arbiter::Bridge::EditorSelectionSnapshot ArbiterBridgeService::getEditorSelection() const
{
    ::Arbiter::Bridge::EditorSelectionSnapshot snapshot;

    // TODO: integrate with Atlas editor backend
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
    const ::Arbiter::Bridge::OpenFileRequest& request)
{
    ::Arbiter::Bridge::BridgeResult result;

    if (!m_running)
    {
        result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        result.message   = "Bridge service is not running";
        return result;
    }

    log("ArbiterBridgeService: open file — " + request.filePath);

    // TODO: integrate with editor open-file command
    result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    result.message   = "Open file stub: not yet implemented";

    return result;
}

// ============================================================
// Tool actions
// ============================================================

bool ArbiterBridgeService::isToolActionAllowed(
    ::Arbiter::Bridge::ToolActionId actionId) const
{
    return m_impl->allowedActionIds.count(
        static_cast<uint32_t>(actionId)) > 0;
}

::Arbiter::Bridge::ToolActionResult ArbiterBridgeService::runToolAction(
    const ::Arbiter::Bridge::ToolActionRequest& request)
{
    ::Arbiter::Bridge::ToolActionResult result;
    result.wasDryRun = request.dryRun;

    if (!m_running)
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::BackendUnavailable;
        result.result.message   = "Bridge service is not running";
        return result;
    }

    if (!isToolActionAllowed(request.actionId))
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::UnsupportedOp;
        result.result.message   = "Tool action is not whitelisted";
        return result;
    }

    log("ArbiterBridgeService: tool action — id="
        + std::to_string(static_cast<uint32_t>(request.actionId))
        + (request.dryRun ? " [DRY RUN]" : " [EXECUTE]"));

    if (request.dryRun)
    {
        result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
        result.result.message   = "Dry-run: action would be permitted";
        result.summary          = "dry-run completed";
        return result;
    }

    // TODO: route to actual editor tool implementations
    result.result.errorCode = ::Arbiter::Bridge::BridgeErrorCode::Success;
    result.result.message   = "Tool action stub: not yet implemented";
    result.summary          = "stub executed";

    return result;
}

} // namespace NovaForge::Integration::Arbiter
