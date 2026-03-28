#include "DeterministicRestoreService.h"

namespace Runtime::SaveLoad
{
    bool DeterministicRestoreService::RebuildScenarioFromSeed(const std::string& /*scenarioId*/, unsigned int /*seed*/)
    {
        // TODO:
        // - rebuild baseline encounter/assemblies from deterministic sources
        return true;
    }

    bool DeterministicRestoreService::ApplyWorldDeltas(const std::string& /*slotId*/)
    {
        // TODO:
        // - apply detached/repaired/hazard states
        return true;
    }

    bool DeterministicRestoreService::ValidateRestoreDrift() const
    {
        // TODO:
        // - compare restored graph against expected references
        return true;
    }
}
