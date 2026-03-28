#include "AssemblyRuntimeComponent.h"

namespace Runtime::BuilderRuntime
{
    bool AssemblyRuntimeComponent::Initialize(const std::string& assemblyId)
    {
        m_assemblyId = assemblyId;
        // TODO:
        // - materialize node states from authored assembly data
        // - register with save/load and debug services
        return true;
    }

    void AssemblyRuntimeComponent::Shutdown()
    {
        // TODO:
        // - unregister runtime state
    }

    const std::string& AssemblyRuntimeComponent::GetAssemblyId() const
    {
        return m_assemblyId;
    }

    const std::vector<AssemblyNodeState>& AssemblyRuntimeComponent::GetNodeStates() const
    {
        return m_nodeStates;
    }

    bool AssemblyRuntimeComponent::MarkNodeDetached(const std::string& nodeId)
    {
        for (auto& node : m_nodeStates)
        {
            if (node.NodeId == nodeId)
            {
                node.bDetached = true;
                return true;
            }
        }
        return false;
    }

    bool AssemblyRuntimeComponent::MarkNodeRepaired(const std::string& nodeId)
    {
        for (auto& node : m_nodeStates)
        {
            if (node.NodeId == nodeId)
            {
                node.bRepaired = true;
                return true;
            }
        }
        return false;
    }

    bool AssemblyRuntimeComponent::RecalculateIntegrity()
    {
        // TODO:
        // - trace support graph
        // - update critical/unsupported states
        return true;
    }
}
