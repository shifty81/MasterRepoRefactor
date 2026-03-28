#pragma once

#include <string>

namespace Runtime::Gameplay
{
    class BuilderSalvageRuntimeBridge
    {
    public:
        bool RegisterAssembly(const std::string& assemblyId);
        bool NotifyNodeDetached(const std::string& assemblyId, const std::string& nodeId);
        bool NotifyNodeRepaired(const std::string& assemblyId, const std::string& nodeId);
    };
}
