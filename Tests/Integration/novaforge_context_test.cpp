// novaforge_context_test.cpp
// Tests for NovaForgeProjectContext, NovaForgeSession, and NovaForgeBootstrap.
//
// These tests are shipping-safe: they have NO dependency on ArbiterBridgeService.
// They verify Epic 5 Task 5.2 (project context) and Task 5.1 (session/bootstrap).

#include "NovaForgeBootstrap.h"
#include "NovaForgeProjectContext.h"
#include "NovaForgeSession.h"

#include <cassert>
#include <cstdlib>
#include <string>

using namespace NovaForge::App;

static std::string testRepoRoot() { return "/repo/MasterRepoRefactor"; }

// ============================================================
// NovaForgeProjectContext
// ============================================================

static void testContextCreation()
{
    auto ctx = NovaForgeProjectContext::createDefault(testRepoRoot());
    assert(ctx.isValid());
    assert(ctx.projectId()   == "novaforge");
    assert(ctx.displayName() == "NovaForge");
    assert(ctx.version()     == "0.1.0");
    assert(ctx.repoRoot()    == testRepoRoot());
    assert(ctx.dataRoot()    == testRepoRoot() + "/NovaForge/Data");
    assert(ctx.contentRoot() == testRepoRoot() + "/NovaForge/Content");
    assert(ctx.docsRoot()    == testRepoRoot() + "/Docs");
    assert(ctx.scriptsRoot() == testRepoRoot() + "/Scripts");
    assert(ctx.testsRoot()   == testRepoRoot() + "/Tests");
    assert(ctx.engineRoot()  == testRepoRoot() + "/Atlas");
    assert(ctx.gameRoot()    == testRepoRoot() + "/NovaForge");
}

static void testContextCustomConfig()
{
    ProjectContextConfig cfg;
    cfg.repoRoot    = "/custom/root";
    cfg.projectId   = "myproject";
    cfg.displayName = "My Project";
    cfg.version     = "1.2.3";
    cfg.dataRoot    = "Data";
    cfg.contentRoot = "Content";

    NovaForgeProjectContext ctx(cfg);
    assert(ctx.isValid());
    assert(ctx.projectId()   == "myproject");
    assert(ctx.dataRoot()    == "/custom/root/Data");
    assert(ctx.contentRoot() == "/custom/root/Content");
}

static void testContextTrailingSlash()
{
    auto ctx = NovaForgeProjectContext::createDefault("/my/repo/");
    assert(ctx.dataRoot() == "/my/repo/NovaForge/Data");
}

static void testContextEmptyRootInvalid()
{
    ProjectContextConfig cfg;
    cfg.repoRoot = "";
    NovaForgeProjectContext ctx(cfg);
    assert(!ctx.isValid());
}

static void testContextEditorFlag()
{
    ProjectContextConfig cfg;
    cfg.repoRoot   = testRepoRoot();
    cfg.editorMode = true;
    cfg.debugMode  = false;

    NovaForgeProjectContext ctx(cfg);
    assert(ctx.isEditorMode());
    assert(!ctx.isDebugMode());
}

// ============================================================
// NovaForgeSession
// ============================================================

static void testSessionInitialState()
{
    NovaForgeSession session;
    assert(session.state()        == SessionState::Disconnected);
    assert(!session.isConnected());
    assert(session.sessionToken().empty());
}

static void testSessionLifecycle()
{
    NovaForgeSession session;

    session.onConnecting();
    assert(session.state() == SessionState::Connecting);
    assert(!session.isConnected());

    session.onConnected("tok-abc123");
    assert(session.state()        == SessionState::Connected);
    assert(session.isConnected());
    assert(session.sessionToken() == "tok-abc123");

    session.onDisconnecting();
    assert(session.state() == SessionState::Disconnecting);

    session.onDisconnected();
    assert(session.state()        == SessionState::Disconnected);
    assert(!session.isConnected());
    assert(session.sessionToken().empty());
}

static void testSessionReset()
{
    NovaForgeSession session;
    session.onConnected("some-token");
    assert(session.isConnected());
    session.reset();
    assert(!session.isConnected());
    assert(session.sessionToken().empty());
    assert(session.state() == SessionState::Disconnected);
}

// ============================================================
// NovaForgeBootstrap (without bridge — shipping safe)
// ============================================================

static void testBootstrapWithoutBridge()
{
    BootstrapConfig cfg;
    cfg.repoRoot          = testRepoRoot();
    cfg.startBridgeService = false;

    NovaForgeBootstrap bootstrap;
    auto result = bootstrap.run(cfg);
    assert(result.success);
    assert(bootstrap.isRunning());

    const auto* ctx = bootstrap.projectContext();
    assert(ctx != nullptr);
    assert(ctx->isValid());
    assert(ctx->projectId() == "novaforge");

    const auto* session = bootstrap.session();
    assert(session != nullptr);
    assert(!session->isConnected()); // no bridge, so still disconnected

    bootstrap.shutdown();
    assert(!bootstrap.isRunning());
    assert(bootstrap.projectContext() == nullptr);
    assert(bootstrap.session()        == nullptr);
}

static void testBootstrapEmptyRootFails()
{
    BootstrapConfig cfg;
    cfg.repoRoot = "";

    NovaForgeBootstrap bootstrap;
    auto result = bootstrap.run(cfg);
    assert(!result.success);
    assert(!bootstrap.isRunning());
}

static void testBootstrapDoubleRunFails()
{
    BootstrapConfig cfg;
    cfg.repoRoot          = testRepoRoot();
    cfg.startBridgeService = false;

    NovaForgeBootstrap bootstrap;
    assert(bootstrap.run(cfg).success);
    assert(!bootstrap.run(cfg).success);
    bootstrap.shutdown();
}

static void testBootstrapReusable()
{
    BootstrapConfig cfg;
    cfg.repoRoot          = testRepoRoot();
    cfg.startBridgeService = false;

    NovaForgeBootstrap bootstrap;
    assert(bootstrap.run(cfg).success);
    bootstrap.shutdown();
    assert(!bootstrap.isRunning());

    // Should be usable again after shutdown
    assert(bootstrap.run(cfg).success);
    bootstrap.shutdown();
}

// ============================================================
// Main
// ============================================================

int main()
{
    testContextCreation();
    testContextCustomConfig();
    testContextTrailingSlash();
    testContextEmptyRootInvalid();
    testContextEditorFlag();

    testSessionInitialState();
    testSessionLifecycle();
    testSessionReset();

    testBootstrapWithoutBridge();
    testBootstrapEmptyRootFails();
    testBootstrapDoubleRunFails();
    testBootstrapReusable();

    return EXIT_SUCCESS;
}
