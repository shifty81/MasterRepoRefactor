// bridge_types_compile_test.cpp
// Build verification: confirms AtlasBridgeTypes.h compiles cleanly and that
// all expected types, constants, and enum values are accessible.
//
// This test exits 0 on success. It uses only standard C++ and the shared header.

#include <AtlasBridgeTypes.h>
#include <cassert>
#include <cstdlib>
#include <string>

using namespace Atlas::Bridge;

static void testProtocolConstants()
{
    // kProtocolVersion must be the string "1.0"
    assert(std::string(kProtocolVersion) == "1.0");
    assert(kDefaultRestPort == 57100u);
    assert(kDefaultWsPort   == 57101u);
}

static void testBridgeResult()
{
    BridgeResult ok;
    assert(ok.errorCode == BridgeErrorCode::Success);
    assert(ok.succeeded());

    BridgeResult fail;
    fail.errorCode = BridgeErrorCode::Unauthorized;
    assert(!fail.succeeded());
}

static void testProjectInfo()
{
    ProjectInfo info;
    info.projectId   = "novaforge";
    info.displayName = "NovaForge";
    info.version     = "0.1.0";

    assert(info.capabilities.supportsProjectIndexing == true);
    assert(info.capabilities.supportsViewportAttach  == false);
}

static void testBuildTypes()
{
    BuildTarget target;
    target.name          = "AtlasEditor";
    target.configuration = BuildConfiguration::Debug;
    target.platform      = BuildPlatform::Win64;
    assert(!target.rebuild);

    BuildResult result;
    result.exitCode = 0;
    assert(result.result.succeeded());
}

static void testEditorSelection()
{
    EditorSelectionSnapshot snap;
    assert(snap.selectedObjectId == 0u);
    assert(snap.activeScene.empty());
}

static void testToolAction()
{
    // dryRun defaults to true in ToolActionRequest — verify the default is set
    ToolActionRequest req;
    req.actionId  = ToolActionId::ValidateData;
    // do NOT explicitly set dryRun so we test the struct default
    assert(req.dryRun); // struct default must be true (safe-by-default)

    ToolActionResult result;
    result.wasDryRun = req.dryRun;
    assert(result.wasDryRun);
}

static void testRequestEnvelopes()
{
    BridgeRequestEnvelope req;
    req.protocolVersion = kProtocolVersion;
    req.requestId       = "test-request-id";
    req.sessionId       = "test-session-id";
    req.service         = "ProjectService";
    req.operation       = "GetProjectInfo";
    assert(req.service == "ProjectService");

    BridgeResponseEnvelope resp;
    resp.success   = true;
    resp.requestId = req.requestId;
    assert(resp.success);
}

static void testSessionTypes()
{
    SessionConnectRequest req;
    req.protocolVersion = kProtocolVersion;
    req.clientVersion   = "0.1.0";
    req.projectId       = "novaforge";
    assert(!req.projectId.empty());

    SessionConnectResponse resp;
    resp.result.errorCode = BridgeErrorCode::Success;
    resp.sessionToken     = "abc123";
    resp.writeEnabled     = false;
    assert(resp.result.succeeded());
    assert(!resp.writeEnabled);
}

static void testAuditLogEntry()
{
    AuditLogEntry entry;
    entry.service    = "ToolService";
    entry.operation  = "RunToolAction";
    entry.success    = true;
    entry.wasDryRun  = true;
    entry.summary    = "dry-run completed";
    assert(entry.success);
    assert(entry.wasDryRun);
}

int main()
{
    testProtocolConstants();
    testBridgeResult();
    testProjectInfo();
    testBuildTypes();
    testEditorSelection();
    testToolAction();
    testRequestEnvelopes();
    testSessionTypes();
    testAuditLogEntry();

    return EXIT_SUCCESS;
}
