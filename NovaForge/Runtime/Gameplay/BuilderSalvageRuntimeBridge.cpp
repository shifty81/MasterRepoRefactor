#include "BuilderSalvageRuntimeBridge.h"

namespace Runtime::Gameplay
{
    bool BuilderSalvageRuntimeBridge::RegisterAssembly(const std::string& /*assemblyId*/)
    {
        // TODO:
        // - bind assembly to mission, hazard, and save systems
        return true;
    }

    bool BuilderSalvageRuntimeBridge::NotifyNodeDetached(const std::string& /*assemblyId*/, const std::string& /*nodeId*/)
    {
        // TODO:
        // - update mission progression, integrity, and save delta
        return true;
    }

    bool BuilderSalvageRuntimeBridge::NotifyNodeRepaired(const std::string& /*assemblyId*/, const std::string& /*nodeId*/)
    {
        // TODO:
        // - propagate restored subsystem effects
        return true;
    }
}
