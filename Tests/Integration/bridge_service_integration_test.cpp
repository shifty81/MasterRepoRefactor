// bridge_service_integration_test.cpp
// Integration test: exercises ArbiterBridgeService together with
// BridgeSessionManager and BridgeAuditLogger end-to-end.
//
// No real HTTP server is required — the service operates on in-process calls.

#include "ArbiterBridgeService.h"
#include "BridgeAuditLogger.h"
#include "BridgeSessionManager.h"

#include <cassert>
#include <cstdlib>
#include <string>

using namespace NovaForge::Integration::Arbiter;
using namespace Arbiter::Bridge;

// ============================================================
// Helpers
// ============================================================

static void startService(ArbiterBridgeService& svc,
                         BridgeAuditLogger*    logger = nullptr)
{
    if (logger)
        svc.setAuditLogger(logger);

    BridgeServiceConfig cfg;
    cfg.restPort = 57100;
    cfg.wsPort   = 57101;

    bool started = svc.start(cfg);
    assert(started);
    assert(svc.isRunning());
}

static std::string connectAndGetToken(ArbiterBridgeService& svc)
{
    SessionConnectRequest req;
    req.protocolVersion = kProtocolVersion;
    req.clientVersion   = "0.1.0";
    req.projectId       = "novaforge";

    auto resp = svc.connectSession(req);
    assert(resp.result.succeeded());
    assert(!resp.sessionToken.empty());
    return resp.sessionToken;
}

// ============================================================
// Tests
// ============================================================

static void testLifecycle()
{
    ArbiterBridgeService svc;
    assert(!svc.isRunning());

    BridgeServiceConfig cfg;
    bool started = svc.start(cfg);
    assert(started);
    assert(svc.isRunning());

    // Double start must return false
    assert(!svc.start(cfg));

    svc.stop();
    assert(!svc.isRunning());
}

static void testSessionConnect()
{
    ArbiterBridgeService svc;
    startService(svc);
    auto token = connectAndGetToken(svc);
    // UUID v4 tokens have the format xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (36 chars)
    assert(token.length() == 36u);
}

static void testSessionConnectVersionMismatch()
{
    ArbiterBridgeService svc;
    startService(svc);

    SessionConnectRequest req;
    req.protocolVersion = "9.9"; // bad version
    req.projectId       = "novaforge";

    auto resp = svc.connectSession(req);
    assert(!resp.result.succeeded());
    assert(resp.result.errorCode == BridgeErrorCode::VersionMismatch);
}

static void testGetProjectInfoRequiresSession()
{
    ArbiterBridgeService svc;
    startService(svc);

    // Without a valid token the result has the sentinel projectId
    auto info = svc.getProjectInfo("bad-token");
    assert(info.projectId == "__unauthorized__");

    // With a valid token it returns the real project info
    auto token = connectAndGetToken(svc);
    info = svc.getProjectInfo(token);
    assert(info.projectId == "novaforge");
    assert(info.displayName == "NovaForge");
    assert(info.capabilities.supportsAISession);
}

static void testRunBuildRequiresSession()
{
    ArbiterBridgeService svc;
    startService(svc);

    BuildTarget target;
    target.name = "AtlasEditor";

    auto result = svc.runBuild("bad-token", target);
    assert(!result.result.succeeded());
    assert(result.result.errorCode == BridgeErrorCode::Unauthorized);

    // With a valid session
    auto token  = connectAndGetToken(svc);
    result      = svc.runBuild(token, target);
    assert(result.result.succeeded());
    assert(!result.buildId.empty());
}

static void testGetEditorSelection()
{
    ArbiterBridgeService svc;
    startService(svc);
    auto token = connectAndGetToken(svc);

    auto snap = svc.getEditorSelection(token);
    // Stub returns empty snapshot — just verify it doesn't crash
    assert(snap.activeScene.empty());
}

static void testToolActionDryRunAllowed()
{
    ArbiterBridgeService svc;
    startService(svc);
    auto token = connectAndGetToken(svc);

    ToolActionRequest req;
    req.actionId = ToolActionId::ValidateData;
    req.dryRun   = true;

    auto result = svc.runToolAction(token, req);
    assert(result.result.succeeded());
    assert(result.wasDryRun);
}

static void testToolActionDeniedWithoutWriteAuth()
{
    ArbiterBridgeService svc;
    startService(svc);
    auto token = connectAndGetToken(svc);

    // Sessions start without write auth, so dryRun=false must be denied
    ToolActionRequest req;
    req.actionId = ToolActionId::OpenScene;
    req.dryRun   = false;

    auto result = svc.runToolAction(token, req);
    assert(!result.result.succeeded());
    assert(result.result.errorCode == BridgeErrorCode::Unauthorized);
}

static void testToolActionNotWhitelisted()
{
    ArbiterBridgeService svc;
    startService(svc);
    auto token = connectAndGetToken(svc);

    ToolActionRequest req;
    req.actionId = static_cast<ToolActionId>(99); // not in whitelist
    req.dryRun   = true;

    auto result = svc.runToolAction(token, req);
    assert(!result.result.succeeded());
    assert(result.result.errorCode == BridgeErrorCode::UnsupportedOp);
}

static void testDisconnectSession()
{
    ArbiterBridgeService svc;
    startService(svc);
    auto token = connectAndGetToken(svc);

    // Disconnecting should revoke the token
    auto result = svc.disconnectSession(token);
    assert(result.succeeded());

    // Subsequent calls with that token must fail
    auto info = svc.getProjectInfo(token);
    assert(info.projectId == "__unauthorized__");
}

static void testAuditLogging()
{
    BridgeAuditLogger    logger;
    ArbiterBridgeService svc;
    startService(svc, &logger);
    auto token = connectAndGetToken(svc);

    // Run a dry-run tool action which should be audited
    ToolActionRequest req;
    req.actionId = ToolActionId::ValidateData;
    req.dryRun   = true;
    svc.runToolAction(token, req);

    auto entries = logger.getEntries();
    // At minimum: session connect + tool action
    assert(entries.size() >= 2u);

    // Check the recent entries helper
    auto recent = logger.getRecentEntries(1);
    assert(recent.size() == 1u);
    assert(recent[0].success);
}

static void testServiceNotRunning()
{
    ArbiterBridgeService svc; // not started

    BuildTarget target;
    target.name = "NovaForgeClient";

    auto result = svc.runBuild("any-token", target);
    assert(result.result.errorCode == BridgeErrorCode::BackendUnavailable);
}

// ============================================================
// Main
// ============================================================

int main()
{
    testLifecycle();
    testSessionConnect();
    testSessionConnectVersionMismatch();
    testGetProjectInfoRequiresSession();
    testRunBuildRequiresSession();
    testGetEditorSelection();
    testToolActionDryRunAllowed();
    testToolActionDeniedWithoutWriteAuth();
    testToolActionNotWhitelisted();
    testDisconnectSession();
    testAuditLogging();
    testServiceNotRunning();

    return EXIT_SUCCESS;
}
