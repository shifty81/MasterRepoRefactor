// novaforge_epic10_test.cpp
// Epic 10 — Second-wave improvements test suite.
//
// Covers all five Epic 10 tasks:
//   Task 10.1 — Search roots (GET /project/search-roots)
//   Task 10.2 — Builder/PCG tool hooks (POST /editor/tools/builder)
//   Task 10.3 — Richer editor state (GET /editor/state)
//   Task 10.4 — Codegen proposal workflow (propose → diff → approve → apply)
//   Task 10.5 — Workspace dashboard (GET /workspace/dashboard)
//
// All tests run in-process; no HTTP server is required.

#include "ArbiterBridgeService.h"
#include "BridgeAuditLogger.h"

#include <cassert>
#include <cstdlib>
#include <string>

using namespace NovaForge::Integration::Arbiter;
using namespace Arbiter::Bridge;

// ============================================================
// Helpers
// ============================================================

static std::string connectSession(ArbiterBridgeService& svc,
                                  const std::string& projectId = "novaforge")
{
    SessionConnectRequest req;
    req.projectId     = projectId;
    req.clientVersion = "0.1.0";
    auto resp = svc.connectSession(req);
    assert(resp.result.succeeded());
    return resp.sessionToken;
}

// ============================================================
// Task 10.1 — Search roots
// ============================================================

static void testTask101_SearchRoots()
{
    BridgeAuditLogger    logger;
    ArbiterBridgeService svc;
    svc.setAuditLogger(&logger);
    svc.start({});

    const std::string token = connectSession(svc);

    auto roots = svc.getSearchRoots(token);
    assert(roots.result.succeeded());
    assert(roots.roots.size() >= 4u); // at least docs, data, content, source

    // Verify each root has non-empty label, path, and kind
    for (const auto& r : roots.roots)
    {
        assert(!r.label.empty());
        assert(!r.path.empty());
        assert(!r.kind.empty());
    }

    // Verify known roots are present
    bool foundDocs    = false;
    bool foundData    = false;
    bool foundContent = false;
    bool foundSource  = false;
    for (const auto& r : roots.roots)
    {
        if (r.kind == "docs")    foundDocs    = true;
        if (r.kind == "data")    foundData    = true;
        if (r.kind == "content") foundContent = true;
        if (r.kind == "source")  foundSource  = true;
    }
    assert(foundDocs);
    assert(foundData);
    assert(foundContent);
    assert(foundSource);

    // Audit log must have an entry for the search roots call
    assert(!logger.getEntries().empty());

    // Unauthorised access must fail
    auto badRoots = svc.getSearchRoots("");
    assert(!badRoots.result.succeeded());
    assert(badRoots.result.errorCode == BridgeErrorCode::Unauthorized);
    assert(badRoots.roots.empty());

    // Service-stopped access must fail
    svc.stop();
    auto stoppedRoots = svc.getSearchRoots(token);
    assert(!stoppedRoots.result.succeeded());
    assert(stoppedRoots.result.errorCode == BridgeErrorCode::BackendUnavailable);
}

// ============================================================
// Task 10.2 — Builder / PCG tool hooks
// ============================================================

static void testTask102_BuilderTools()
{
    BridgeAuditLogger    logger;
    ArbiterBridgeService svc;
    svc.setAuditLogger(&logger);
    svc.start({});

    const std::string token = connectSession(svc);

    // All whitelisted builder actions should succeed in dry-run mode
    const BuilderToolActionId whitelisted[] = {
        BuilderToolActionId::ValidateData,
        BuilderToolActionId::RunPCGPreview,
        BuilderToolActionId::OpenScene,
        BuilderToolActionId::FocusEntity,
        BuilderToolActionId::RegenerateSchemas,
        BuilderToolActionId::RunBuilderInspect,
        BuilderToolActionId::RunPCGDiagnostics,
        BuilderToolActionId::GeneratePCGPreview,
        BuilderToolActionId::ValidateBuilderData,
    };

    for (auto id : whitelisted)
    {
        BuilderToolRequest req;
        req.actionId = id;
        req.dryRun   = true;
        auto res = svc.runBuilderTool(token, req);
        assert(res.result.succeeded());
        assert(res.wasDryRun);
    }

    // Non-whitelisted action must be denied
    {
        BuilderToolRequest badReq;
        badReq.actionId = static_cast<BuilderToolActionId>(99);
        badReq.dryRun   = true;
        auto res = svc.runBuilderTool(token, badReq);
        assert(!res.result.succeeded());
        assert(res.result.errorCode == BridgeErrorCode::UnsupportedOp);
    }

    // Diagnostic actions should populate diagnosticsLog in non-dry-run
    // (requires write-enabled session; use a fresh session for this assertion
    //  via the stub which defaults to read-only — just verify dry-run path)
    {
        BuilderToolRequest diagReq;
        diagReq.actionId = BuilderToolActionId::RunPCGDiagnostics;
        diagReq.dryRun   = true;
        auto res = svc.runBuilderTool(token, diagReq);
        assert(res.result.succeeded());
        assert(res.wasDryRun);
    }

    // Unauthorized call must fail
    {
        BuilderToolRequest req;
        req.actionId = BuilderToolActionId::ValidateData;
        req.dryRun   = true;
        auto res = svc.runBuilderTool("", req);
        assert(!res.result.succeeded());
        assert(res.result.errorCode == BridgeErrorCode::Unauthorized);
    }

    // Backend-stopped call must fail
    svc.stop();
    {
        BuilderToolRequest req;
        req.actionId = BuilderToolActionId::ValidateData;
        req.dryRun   = true;
        auto res = svc.runBuilderTool(token, req);
        assert(!res.result.succeeded());
        assert(res.result.errorCode == BridgeErrorCode::BackendUnavailable);
    }
}

// ============================================================
// Task 10.3 — Richer editor state
// ============================================================

static void testTask103_EditorState()
{
    ArbiterBridgeService svc;
    svc.start({});
    const std::string token = connectSession(svc);

    auto state = svc.getEditorState(token);
    assert(state.result.succeeded());

    // Default stub values
    assert(state.simulationState == SimulationState::Stopped);
    assert(state.selectedObjectId == 0u);
    assert(state.selectedComponents.empty());
    // activeMode has a default populated value
    assert(!state.activeMode.empty());

    // Unauthorised
    auto unauth = svc.getEditorState("");
    assert(!unauth.result.succeeded());
    assert(unauth.result.errorCode == BridgeErrorCode::Unauthorized);

    // Stopped service
    svc.stop();
    auto stopped = svc.getEditorState(token);
    assert(!stopped.result.succeeded());
    assert(stopped.result.errorCode == BridgeErrorCode::BackendUnavailable);
}

// ============================================================
// Task 10.4 — Codegen proposal workflow
// ============================================================

static void testTask104_CodegenWorkflow()
{
    BridgeAuditLogger    logger;
    ArbiterBridgeService svc;
    svc.setAuditLogger(&logger);
    svc.start({});

    const std::string token = connectSession(svc);

    // Step 1: propose
    CodegenProposalRequest proposalReq;
    proposalReq.description = "Add health component to player entity";
    proposalReq.targetFile  = "NovaForge/Gameplay/PlayerSystems/HealthComponent.cpp";
    proposalReq.dryRun      = true;

    auto proposal = svc.proposeCodegen(token, proposalReq);
    assert(proposal.result.succeeded());
    assert(!proposal.proposalId.empty());
    assert(proposal.targetFile == proposalReq.targetFile);
    assert(!proposal.summary.empty());

    // Step 2: get diff
    auto diff = svc.getCodegenDiff(token, proposal.proposalId);
    assert(diff.result.succeeded());
    assert(diff.proposalId == proposal.proposalId);
    assert(!diff.diffText.empty());
    assert(diff.linesAdded > 0);
    assert(diff.linesRemoved == 0); // stub always adds, never removes

    // Diff must contain the target file path
    assert(diff.diffText.find(proposalReq.targetFile) != std::string::npos);

    // Step 3: reject — no changes applied, proposal removed
    {
        CodegenApprovalRequest reject;
        reject.proposalId = proposal.proposalId;
        reject.approved   = false;
        reject.comment    = "not ready yet";

        auto rejectResult = svc.approveAndApplyCodegen(token, reject);
        assert(rejectResult.result.succeeded());
        assert(!rejectResult.wasApplied);
        assert(rejectResult.appliedFile.empty());

        // Proposal is gone — a second call must return NotFound
        auto missingDiff = svc.getCodegenDiff(token, proposal.proposalId);
        assert(!missingDiff.result.succeeded());
        assert(missingDiff.result.errorCode == BridgeErrorCode::NotFound);
    }

    // Approve path: sessions are read-only by default, so approve must require
    // write auth and return Unauthorized.
    {
        auto proposal3 = svc.proposeCodegen(token, proposalReq);
        assert(proposal3.result.succeeded());

        CodegenApprovalRequest approveAttempt;
        approveAttempt.proposalId = proposal3.proposalId;
        approveAttempt.approved   = true;

        auto writeBlockResult = svc.approveAndApplyCodegen(token, approveAttempt);
        // Read-only session → Unauthorized
        assert(!writeBlockResult.result.succeeded());
        assert(writeBlockResult.result.errorCode == BridgeErrorCode::Unauthorized);

        // Clean up the pending proposal by rejecting it
        approveAttempt.approved = false;
        svc.approveAndApplyCodegen(token, approveAttempt);
    }

    // Error cases
    {
        // Empty targetFile
        CodegenProposalRequest badReq;
        badReq.description = "something";
        auto bad = svc.proposeCodegen(token, badReq);
        assert(!bad.result.succeeded());
        assert(bad.result.errorCode == BridgeErrorCode::InvalidRequest);

        // Unauthorised propose
        auto unauth = svc.proposeCodegen("", proposalReq);
        assert(!unauth.result.succeeded());
        assert(unauth.result.errorCode == BridgeErrorCode::Unauthorized);
    }

    svc.stop();
}

// ============================================================
// Task 10.5 — Workspace dashboard
// ============================================================

static void testTask105_WorkspaceDashboard()
{
    BridgeAuditLogger    logger;
    ArbiterBridgeService svc;
    svc.setAuditLogger(&logger);
    svc.start({});

    const std::string token = connectSession(svc);

    // Fresh dashboard before any build or tool action
    {
        auto dash = svc.getWorkspaceDashboard(token);
        assert(dash.result.succeeded());
        assert(dash.projectId    == "novaforge");
        assert(dash.projectName  == "NovaForge");
        assert(!dash.projectVersion.empty());
        assert(dash.activeSessionCount >= 1u); // at least our own session
        assert(!dash.searchRoots.roots.empty());
        assert(!dash.currentProjectStatus.empty());
    }

    // Run a build — dashboard should reflect it
    {
        BuildTarget t;
        t.name = "NovaForgeClient";
        svc.runBuild(token, t);

        auto dash = svc.getWorkspaceDashboard(token);
        assert(dash.result.succeeded());
        assert(dash.buildHealth.lastBuildTarget == "NovaForgeClient");
        assert(!dash.buildHealth.lastBuildId.empty());
        assert(dash.buildHealth.lastBuildSucceeded);
        assert(!dash.buildHealth.lastBuildTimestampUtc.empty());
    }

    // Run a tool action — dashboard should reflect it
    {
        ToolActionRequest toolReq;
        toolReq.actionId = ToolActionId::ValidateData;
        toolReq.dryRun   = true;
        svc.runToolAction(token, toolReq);

        auto dash = svc.getWorkspaceDashboard(token);
        assert(dash.result.succeeded());
        assert(!dash.lastToolAction.empty());
        assert(!dash.lastToolTimestampUtc.empty());
    }

    // Multi-session: connect a second session and check count
    {
        auto token2 = connectSession(svc);
        auto dash = svc.getWorkspaceDashboard(token);
        assert(dash.activeSessionCount >= 2u);
    }

    // Unauthorised access
    {
        auto unauth = svc.getWorkspaceDashboard("");
        assert(!unauth.result.succeeded());
        assert(unauth.result.errorCode == BridgeErrorCode::Unauthorized);
    }

    // Stopped service
    svc.stop();
    {
        auto stopped = svc.getWorkspaceDashboard(token);
        assert(!stopped.result.succeeded());
        assert(stopped.result.errorCode == BridgeErrorCode::BackendUnavailable);
    }
}

// ============================================================
// Cross-task: audit log coverage
// ============================================================

static void testAuditLogCoverage()
{
    BridgeAuditLogger    logger;
    ArbiterBridgeService svc;
    svc.setAuditLogger(&logger);
    svc.start({});

    const std::string token = connectSession(svc);

    // Drive all Epic 10 endpoints
    svc.getSearchRoots(token);

    BuilderToolRequest bReq;
    bReq.actionId = BuilderToolActionId::RunBuilderInspect;
    bReq.dryRun   = true;
    svc.runBuilderTool(token, bReq);

    svc.getEditorState(token);

    CodegenProposalRequest cReq;
    cReq.description = "test";
    cReq.targetFile  = "some/file.cpp";
    auto prop = svc.proposeCodegen(token, cReq);
    svc.getCodegenDiff(token, prop.proposalId);
    CodegenApprovalRequest aReq;
    aReq.proposalId = prop.proposalId;
    aReq.approved   = false;
    svc.approveAndApplyCodegen(token, aReq);

    svc.getWorkspaceDashboard(token);

    auto entries = logger.getEntries();
    // connect + getSearchRoots + runBuilderTool + getEditorState
    // + propose + approveAndApply + getDashboard = ≥7 entries
    assert(entries.size() >= 7u);

    svc.stop();
}

// ============================================================
// Main
// ============================================================

int main()
{
    testTask101_SearchRoots();
    testTask102_BuilderTools();
    testTask103_EditorState();
    testTask104_CodegenWorkflow();
    testTask105_WorkspaceDashboard();
    testAuditLogCoverage();

    return EXIT_SUCCESS;
}
