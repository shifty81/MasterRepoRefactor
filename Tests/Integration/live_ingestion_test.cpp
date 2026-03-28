// live_ingestion_test.cpp
// Tests for NovaForge::Integration::AtlasAI::LiveIngestionService.
//
// Covers:
//   - Service lifecycle (start / stop / isRunning)
//   - captureNow returns valid snapshots with populated subsystems
//   - Sequence ID increments on each capture
//   - Pull-model getters return the latest captured data
//   - Callback is invoked on captureNow
//   - Config flags (includeEconomy, includeFactions, etc.) are respected

#include "LiveIngestionService.h"
#include <cassert>
#include <string>

using namespace NovaForge::Integration::AtlasAI;

// ============================================================
// Helpers
// ============================================================

static IngestionConfig makeConfig(bool eco = true, bool fac = true,
                                   bool wld = true, bool plr = true)
{
    IngestionConfig c;
    c.includeEconomy       = eco;
    c.includeFactions      = fac;
    c.includeWorldState    = wld;
    c.includePlayerSystems = plr;
    return c;
}

// ============================================================
// Lifecycle tests
// ============================================================

static void testStartStop()
{
    LiveIngestionService svc;
    assert(!svc.isRunning());

    bool started = svc.start(makeConfig());
    assert(started);
    assert(svc.isRunning());

    svc.stop();
    assert(!svc.isRunning());
}

static void testDoubleStartReturnsFalse()
{
    LiveIngestionService svc;
    assert(svc.start(makeConfig()));
    assert(!svc.start(makeConfig())); // already running
    svc.stop();
}

// ============================================================
// captureNow tests
// ============================================================

static void testCaptureNowReturnsSnapshot()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    IngestionSnapshot snap = svc.captureNow();
    assert(snap.sequenceId == 1u);
    assert(!snap.capturedAt.empty());

    svc.stop();
}

static void testCaptureNowSequenceIncrements()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    auto s1 = svc.captureNow();
    auto s2 = svc.captureNow();
    auto s3 = svc.captureNow();

    assert(s1.sequenceId == 1u);
    assert(s2.sequenceId == 2u);
    assert(s3.sequenceId == 3u);

    svc.stop();
}

static void testCaptureNowPopulatesEconomy()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    auto snap = svc.captureNow();
    assert(snap.economy.activeMarkets > 0u);
    assert(!snap.economy.topResourceId.empty());
    assert(snap.economy.topResourcePrice > 0.0f);

    svc.stop();
}

static void testCaptureNowPopulatesFactions()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    auto snap = svc.captureNow();
    assert(snap.factions.factionCount > 0u);
    assert(!snap.factions.dominantFactionId.empty());

    svc.stop();
}

static void testCaptureNowPopulatesWorld()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    auto snap = svc.captureNow();
    assert(snap.world.loadedSectorCount > 0u);
    assert(snap.world.simulationRunning);
    assert(!snap.world.activeSectorId.empty());

    svc.stop();
}

static void testCaptureNowPopulatesPlayers()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    auto snap = svc.captureNow();
    assert(snap.players.onlinePlayerCount > 0u);

    svc.stop();
}

// ============================================================
// Config flag tests
// ============================================================

static void testEconomyDisabled()
{
    LiveIngestionService svc;
    svc.start(makeConfig(/*eco=*/false));

    auto snap = svc.captureNow();
    // When includeEconomy is false the economy sub-snapshot should be empty
    assert(snap.economy.activeMarkets == 0u);

    svc.stop();
}

static void testFactionsDisabled()
{
    LiveIngestionService svc;
    svc.start(makeConfig(/*eco=*/true, /*fac=*/false));

    auto snap = svc.captureNow();
    assert(snap.factions.factionCount == 0u);

    svc.stop();
}

// ============================================================
// Pull-model getter tests
// ============================================================

static void testGetLastSnapshotBeforeCapture()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    // Before any capture, getters return default structs
    auto snap = svc.getLastSnapshot();
    assert(snap.sequenceId == 0u);

    svc.stop();
}

static void testGetLastSnapshotAfterCapture()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    svc.captureNow();
    svc.captureNow();

    assert(svc.snapshotSequence() == 2u);
    auto eco = svc.getLastEconomySnapshot();
    assert(eco.activeMarkets > 0u);

    svc.stop();
}

// ============================================================
// Callback test
// ============================================================

static void testCallbackIsInvoked()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    uint64_t receivedSeq = 0;
    svc.setSnapshotCallback([&](const IngestionSnapshot& s) {
        receivedSeq = s.sequenceId;
    });

    svc.captureNow();
    assert(receivedSeq == 1u);

    svc.stop();
}

static void testCallbackCalledMultipleTimes()
{
    LiveIngestionService svc;
    svc.start(makeConfig());

    int callCount = 0;
    svc.setSnapshotCallback([&](const IngestionSnapshot&) { ++callCount; });

    svc.captureNow();
    svc.captureNow();
    svc.captureNow();
    assert(callCount == 3);

    svc.stop();
}

// ============================================================
// main
// ============================================================

int main()
{
    testStartStop();
    testDoubleStartReturnsFalse();
    testCaptureNowReturnsSnapshot();
    testCaptureNowSequenceIncrements();
    testCaptureNowPopulatesEconomy();
    testCaptureNowPopulatesFactions();
    testCaptureNowPopulatesWorld();
    testCaptureNowPopulatesPlayers();
    testEconomyDisabled();
    testFactionsDisabled();
    testGetLastSnapshotBeforeCapture();
    testGetLastSnapshotAfterCapture();
    testCallbackIsInvoked();
    testCallbackCalledMultipleTimes();

    return 0;
}
