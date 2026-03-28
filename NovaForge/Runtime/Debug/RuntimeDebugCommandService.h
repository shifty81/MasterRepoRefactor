#pragma once

#include <string>

namespace Runtime::Debug
{
    class RuntimeDebugCommandService
    {
    public:
        bool InjectBreachAtNode(const std::string& assemblyId, const std::string& nodeId);
        bool FaultSubsystem(const std::string& subsystemId);
        bool ForceDetachNode(const std::string& assemblyId, const std::string& nodeId);
        bool CreateCheckpoint(const std::string& slotName);
    };
}
