// ArbiterBridgeService.h
// NovaForge-side bridge service that exposes safe editor and build operations to Arbiter.
//
// Rules:
// - This file must not expose arbitrary engine internals.
// - All operations must be editor-safe and explicitly permissioned.
// - Write operations default to dry-run unless explicitly overridden.
// - This service is guarded by NOVAFORGE_ENABLE_ARBITER_INTEGRATION.

#pragma once

#include <ArbiterBridgeTypes.h>
#include "BridgeAuditLogger.h"
#include <functional>
#include <memory>
#include <string>

namespace NovaForge::Integration::Arbiter
{

// ============================================================
// Service configuration
// ============================================================

struct BridgeServiceConfig
{
    uint16_t    restPort          = ::Arbiter::Bridge::kDefaultRestPort;
    uint16_t    wsPort            = ::Arbiter::Bridge::kDefaultWsPort;
    bool        bindLoopbackOnly  = true;
    uint32_t    timeoutSeconds    = 30;
};

// ============================================================
// Log callback
// ============================================================

using BridgeLogCallback = std::function<void(const std::string& message)>;

// ============================================================
// ArbiterBridgeService
// ============================================================

class ArbiterBridgeService
{
public:
    ArbiterBridgeService();
    ~ArbiterBridgeService();

    // --------------------------------------------------------
    // Lifecycle
    // --------------------------------------------------------
    bool start(const BridgeServiceConfig& config);
    void stop();
    bool isRunning() const;

    // --------------------------------------------------------
    // Logging and audit
    // --------------------------------------------------------
    void setLogCallback(BridgeLogCallback callback);
    void setAuditLogger(BridgeAuditLogger* logger);

    // --------------------------------------------------------
    // Session management (Epic 4 / Task 4.1)
    // --------------------------------------------------------

    /// Establishes a new bridge session and returns a session token.
    ::Arbiter::Bridge::SessionConnectResponse connectSession(
        const ::Arbiter::Bridge::SessionConnectRequest& request);

    /// Disconnects and invalidates the session for the given token.
    ::Arbiter::Bridge::BridgeResult disconnectSession(
        const std::string& sessionToken);

    // --------------------------------------------------------
    // Project info endpoint  GET /project/info  (Task 4.1)
    // --------------------------------------------------------
    ::Arbiter::Bridge::ProjectInfo getProjectInfo(
        const std::string& sessionToken) const;

    // --------------------------------------------------------
    // Build endpoint  POST /build/run  (Task 4.3)
    // --------------------------------------------------------
    ::Arbiter::Bridge::BuildResult runBuild(
        const std::string&                    sessionToken,
        const ::Arbiter::Bridge::BuildTarget& target);

    // --------------------------------------------------------
    // Editor state endpoint  GET /editor/selection  (Task 4.2)
    // --------------------------------------------------------
    ::Arbiter::Bridge::EditorSelectionSnapshot getEditorSelection(
        const std::string& sessionToken) const;

    // --------------------------------------------------------
    // File operations
    // --------------------------------------------------------
    ::Arbiter::Bridge::BridgeResult openFile(
        const std::string&                          sessionToken,
        const ::Arbiter::Bridge::OpenFileRequest&   request);

    // --------------------------------------------------------
    // Tool actions endpoint  POST /editor/tools/run  (Task 4.4)
    // --------------------------------------------------------
    ::Arbiter::Bridge::ToolActionResult runToolAction(
        const std::string&                              sessionToken,
        const ::Arbiter::Bridge::ToolActionRequest&     request);

private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;

    bool validateSession(const std::string& token) const;
    bool validateWriteSession(const std::string& token) const;
    bool isToolActionAllowed(::Arbiter::Bridge::ToolActionId actionId) const;

    void log(const std::string& message);
    void auditLog(
        const std::string& requestId,
        const std::string& sessionId,
        const std::string& service,
        const std::string& operation,
        bool               success,
        const std::string& summary,
        bool               wasDryRun  = false,
        const std::string& failReason = {});

    BridgeLogCallback   m_logCallback;
    BridgeAuditLogger*  m_auditLogger = nullptr;
    BridgeServiceConfig m_config;
    bool                m_running = false;
};

} // namespace NovaForge::Integration::Arbiter
