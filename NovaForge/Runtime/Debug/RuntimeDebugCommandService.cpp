#include "RuntimeDebugCommandService.h"

namespace Runtime::Debug
{
    bool RuntimeDebugCommandService::InjectBreachAtNode(const std::string& /*assemblyId*/, const std::string& /*nodeId*/)
    {
        return true;
    }

    bool RuntimeDebugCommandService::FaultSubsystem(const std::string& /*subsystemId*/)
    {
        return true;
    }

    bool RuntimeDebugCommandService::ForceDetachNode(const std::string& /*assemblyId*/, const std::string& /*nodeId*/)
    {
        return true;
    }

    bool RuntimeDebugCommandService::CreateCheckpoint(const std::string& /*slotName*/)
    {
        return true;
    }
}
