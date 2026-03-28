#pragma once

#include <string>

namespace Runtime::SaveLoad
{
    class DeterministicRestoreService
    {
    public:
        bool RebuildScenarioFromSeed(const std::string& scenarioId, unsigned int seed);
        bool ApplyWorldDeltas(const std::string& slotId);
        bool ValidateRestoreDrift() const;
    };
}
