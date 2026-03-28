#pragma once

#include <string>
#include <vector>

namespace Runtime::BuilderRuntime
{
    struct AssemblyNodeState
    {
        std::string NodeId;
        bool bDetached = false;
        bool bRepaired = false;
        bool bDestroyed = false;
    };

    class AssemblyRuntimeComponent
    {
    public:
        bool Initialize(const std::string& assemblyId);
        void Shutdown();

        const std::string& GetAssemblyId() const;
        const std::vector<AssemblyNodeState>& GetNodeStates() const;

        bool MarkNodeDetached(const std::string& nodeId);
        bool MarkNodeRepaired(const std::string& nodeId);
        bool RecalculateIntegrity();

    private:
        std::string m_assemblyId;
        std::vector<AssemblyNodeState> m_nodeStates;
    };
}
