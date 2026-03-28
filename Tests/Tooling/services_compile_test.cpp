// services_compile_test.cpp
// Build verification: confirms all five service headers compile cleanly and that
// their public APIs are accessible and behave correctly at a basic level.

#include <AtlasBuildService.h>
#include <AtlasAssetService.h>
#include <AtlasWorldService.h>
#include <AtlasSessionService.h>
#include <AtlasTelemetryService.h>
#include <cassert>
#include <cstdlib>
#include <string>

using namespace Atlas::Services;

static void testBuildService()
{
    AtlasBuildService svc;
    svc.initialise();

    BuildRequest req;
    req.target = BuildTarget::Editor;
    req.dryRun = true;

    uint64_t id = svc.queueBuild(req);
    assert(id == 1u);

    BuildJob job = svc.queryJob(id);
    assert(job.jobId == id);
    assert(job.status == BuildStatus::Succeeded);

    assert(svc.overallStatus() == BuildStatus::Idle);
    assert(svc.listJobs().size() == 1u);

    svc.shutdown();
}

static void testAssetService()
{
    AtlasAssetService svc;
    svc.initialise();

    ImportRequest req;
    req.sourcePath = "Content/Meshes/Cube.fbx";
    req.hint       = AssetType::Mesh;
    req.dryRun     = true;

    ImportResult r = svc.importAsset(req);
    assert(r.success);
    assert(r.assetId == 1u);

    auto found = svc.findById(r.assetId);
    assert(found.has_value());
    assert(found->type == AssetType::Mesh);

    assert(svc.listAll().size() == 1u);
    assert(svc.listByType(AssetType::Texture).empty());

    assert(svc.deleteAsset(r.assetId));
    assert(svc.listAll().empty());

    svc.shutdown();
}

static void testWorldService()
{
    AtlasWorldService svc;
    svc.initialise();

    assert(svc.openWorld("world-001"));
    WorldStateSnapshot snap = svc.queryState();
    assert(snap.worldId == "world-001");
    assert(snap.state == WorldState::Loaded);
    assert(!snap.isDirty);

    assert(svc.loadSector(42u));
    assert(svc.queryState().loadedSectors == 1u);

    assert(svc.querySector(42u).has_value());
    assert(!svc.querySector(99u).has_value());

    assert(svc.unloadSector(42u));
    assert(svc.queryState().loadedSectors == 0u);

    assert(svc.saveWorld());
    assert(!svc.queryState().isDirty);

    assert(svc.closeWorld());
    assert(svc.queryState().state == WorldState::Unloaded);

    svc.shutdown();
}

static void testSessionService()
{
    AtlasSessionService svc;
    svc.initialise();

    std::string id = svc.createSession("AtlasAI.WpfHost", "proj-novaforge");
    assert(!id.empty());

    auto profile = svc.findSession(id);
    assert(profile.has_value());
    assert(profile->state == SessionState::Active);
    assert(profile->clientId == "AtlasAI.WpfHost");

    assert(svc.listActiveSessions().size() == 1u);

    assert(svc.suspendSession(id));
    assert(svc.listActiveSessions().empty());

    assert(svc.activateSession(id));
    assert(svc.listActiveSessions().size() == 1u);

    assert(svc.terminateSession(id));

    SessionCapabilities caps = svc.getCapabilities();
    assert(caps.supportsAISession);
    assert(!caps.supportsViewportAttach);

    svc.shutdown();
}

static void testTelemetryService()
{
    AtlasTelemetryService svc;
    svc.initialise();

    svc.log(LogLevel::Info,    "TestSource", "Info message");
    svc.log(LogLevel::Warning, "TestSource", "Warning message");
    svc.log(LogLevel::Error,   "TestSource", "Error message");

    auto logs = svc.getRecentLogs(10);
    assert(logs.size() == 3u);

    HealthSummary h = svc.getHealthSummary();
    assert(!h.servicesHealthy);
    assert(h.errorCount   == 1u);
    assert(h.warningCount == 1u);
    assert(h.lastError == "Error message");

    bool listenerCalled = false;
    svc.addLogListener([&](const LogEntry& e) { listenerCalled = true; (void)e; });
    svc.log(LogLevel::Debug, "TestSource", "Debug message");
    assert(listenerCalled);

    TelemetryEvent ev;
    ev.eventType = "BuildStarted";
    ev.source    = "AtlasBuildService";
    svc.emit(ev);
    assert(svc.getRecentEvents(10).size() == 1u);

    svc.clearListeners();
    svc.shutdown();
}

int main()
{
    testBuildService();
    testAssetService();
    testWorldService();
    testSessionService();
    testTelemetryService();

    return EXIT_SUCCESS;
}
