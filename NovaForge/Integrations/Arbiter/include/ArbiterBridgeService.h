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
    uint16_t    restPort          = 57100;
    uint16_t    wsPort            = 57101;
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

    // Lifecycle
    bool start(const BridgeServiceConfig& config);
    void stop();
    bool isRunning() const;

    // Logging
    void setLogCallback(BridgeLogCallback callback);

    // Project info
    ::Arbiter::Bridge::ProjectInfo      getProjectInfo() const;

    // Build
    ::Arbiter::Bridge::BuildResult      runBuild(
        const ::Arbiter::Bridge::BuildTarget& target);

    // Editor state
    ::Arbiter::Bridge::EditorSelectionSnapshot getEditorSelection() const;

    // File operations
    ::Arbiter::Bridge::BridgeResult     openFile(
        const ::Arbiter::Bridge::OpenFileRequest& request);

    // Tool actions (whitelisted only)
    ::Arbiter::Bridge::ToolActionResult runToolAction(
        const ::Arbiter::Bridge::ToolActionRequest& request);

private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;

    bool isToolActionAllowed(::Arbiter::Bridge::ToolActionId actionId) const;
    void log(const std::string& message);

    BridgeLogCallback   m_logCallback;
    BridgeServiceConfig m_config;
    bool                m_running = false;
};

} // namespace NovaForge::Integration::Arbiter
