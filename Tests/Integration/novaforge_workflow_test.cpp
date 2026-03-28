// novaforge_workflow_test.cpp
// Epic 9 — First real workflow milestone (bridge-dependent tests).
//
// Proves the backbone works end-to-end in-process (no HTTP server required):
//   Task 9.1 — AtlasAI reads project info
//   Task 9.2 — AtlasAI queries active editor selection
//   Task 9.3 — AtlasAI launches a safe build target
//   Task 9.4 — AtlasAI runs one safe editor tool
//   Task 9.5 — Shipping isolation: endpoints reject unauthenticated calls
//
// Requires NOVAFORGE_ENABLE_ARBITER_INTEGRATION=ON.
// For context/session/bootstrap tests that run without the bridge,
// see novaforge_context_test.cpp.

#include "AtlasBridgeService.h"
#include "BridgeAuditLogger.h"

#include <cassert>
#include <cstdlib>
#include <string>

using namespace NovaForge::Integration::AtlasAI;
using namespace Atlas::Bridge;

// ============================================================
// Helpers
// ============================================================

static std::string connectSession(AtlasBridgeService& svc)
{
    SessionConnectRequest req;
    req.projectId     = "novaforge";
    req.clientVersion = "0.1.0";
    auto resp = svc.connectSession(req);
    assert(resp.result.succeeded());
    return resp.sessionToken;
}

// ============================================================
// Task 9.1 — AtlasAI reads project info
// ============================================================

static void testTask91_ProjectInfo()
{
    BridgeAuditLogger    logger;
    AtlasBridgeService svc;
    svc.setAuditLogger(&logger);
    svc.start({});

    const std::string token = connectSession(svc);

    auto info = svc.getProjectInfo(token);
    assert(info.projectId   == "novaforge");
    assert(info.displayName == "NovaForge");
    assert(info.version     == "0.1.0");
    assert(info.capabilities.supportsAISession);
    assert(info.capabilities.supportsProjectIndexing);
    assert(!info.capabilities.supportsViewportAttach);

    // Audit log must contain entries
    assert(logger.getEntries().size() >= 1u);

    svc.stop();
}

// ============================================================
// Task 9.2 — AtlasAI queries active editor selection
// ============================================================

static void testTask92_EditorSelection()
{
    AtlasBridgeService svc;
    svc.start({});
    const std::string token = connectSession(svc);

    auto snap = svc.getEditorSelection(token);
    // Stub: no editor running yet, returns empty snapshot
    assert(snap.activeScene.empty());
    assert(snap.selectedObjectId == 0u);
    assert(snap.selectedObjectName.empty());

    svc.stop();
}

// ============================================================
// Task 9.3 — AtlasAI launches a safe build target
// ============================================================

static void testTask93_RunBuild()
{
    AtlasBridgeService svc;
    svc.start({});
    const std::string token = connectSession(svc);

    // Each call gets a unique buildId
    BuildTarget t1;
    t1.name = "NovaForgeClient";
    auto r1 = svc.runBuild(token, t1);
    assert(r1.result.succeeded());
    assert(!r1.buildId.empty());

    BuildTarget t2;
    t2.name = "AtlasEditor";
    auto r2 = svc.runBuild(token, t2);
    assert(r2.result.succeeded());
    assert(r2.buildId != r1.buildId);

    BuildTarget t3;
    t3.name          = "NovaForgeTests";
    t3.configuration = BuildConfiguration::Release;
    auto r3 = svc.runBuild(token, t3);
    assert(r3.result.succeeded());

    svc.stop();
}

// ============================================================
// Task 9.4 — AtlasAI runs one safe editor tool
// ============================================================

static void testTask94_ToolAction()
{
    BridgeAuditLogger    logger;
    AtlasBridgeService svc;
    svc.setAuditLogger(&logger);
    svc.start({});
    const std::string token = connectSession(svc);

    // All whitelisted actions should succeed in dry-run mode
    const ToolActionId whitelisted[] = {
        ToolActionId::ValidateData,
        ToolActionId::RunPCGPreview,
        ToolActionId::OpenScene,
        ToolActionId::FocusEntity,
        ToolActionId::RegenerateSchemas,
    };

    for (auto id : whitelisted)
    {
        ToolActionRequest req;
        req.actionId = id;
        req.dryRun   = true;
        auto res = svc.runToolAction(token, req);
        assert(res.result.succeeded());
        assert(res.wasDryRun);
    }

    // Non-whitelisted action must be denied even in dry-run
    ToolActionRequest badReq;
    badReq.actionId = static_cast<ToolActionId>(99);
    badReq.dryRun   = true;
    assert(!svc.runToolAction(token, badReq).result.succeeded());

    // Audit log: connect + 5 tool actions = at least 6 entries
    assert(logger.getEntries().size() >= 6u);

    svc.stop();
}

// ============================================================
// Task 9.5 — Shipping isolation verification
// ============================================================

static void testTask95_ShippingIsolation()
{
    // Service must reject all requests from unauthenticated / stopped state

    // (a) Service not started → BackendUnavailable
    {
        AtlasBridgeService svc;
        BuildTarget t;
        t.name = "NovaForgeClient";
        assert(svc.runBuild("", t).result.errorCode ==
               BridgeErrorCode::BackendUnavailable);
    }

    // (b) Service running but empty / bad token → Unauthorized
    {
        AtlasBridgeService svc;
        svc.start({});

        BuildTarget t;
        t.name = "NovaForgeClient";
        assert(!svc.runBuild("", t).result.succeeded());
        assert(!svc.runBuild("bogus-token", t).result.succeeded());

        ToolActionRequest r;
        r.actionId = ToolActionId::ValidateData;
        r.dryRun   = true;
        assert(!svc.runToolAction("", r).result.succeeded());

        auto info = svc.getProjectInfo("bad");
        assert(info.projectId == "__unauthorized__");

        svc.stop();
    }

    // (c) After stop → BackendUnavailable
    {
        AtlasBridgeService svc;
        svc.start({});
        const std::string token = connectSession(svc);
        svc.stop();

        BuildTarget t;
        t.name = "NovaForgeClient";
        assert(svc.runBuild(token, t).result.errorCode ==
               BridgeErrorCode::BackendUnavailable);
    }
}

// ============================================================
// Main
// ============================================================

int main()
{
    testTask91_ProjectInfo();
    testTask92_EditorSelection();
    testTask93_RunBuild();
    testTask94_ToolAction();
    testTask95_ShippingIsolation();

    return EXIT_SUCCESS;
}
