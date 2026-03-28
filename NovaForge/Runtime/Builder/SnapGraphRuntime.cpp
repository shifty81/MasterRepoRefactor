#include "SnapGraphRuntime.h"

namespace Runtime::BuilderRuntime
{
    bool SnapGraphRuntime::BuildFromAssembly(const std::string& /*assemblyId*/)
    {
        // TODO:
        // - build adjacency from authored builder data
        return true;
    }

    std::vector<std::string> SnapGraphRuntime::GetConnectedNodes(const std::string& nodeId) const
    {
        std::vector<std::string> connected;
        for (const auto& edge : m_edges)
        {
            if (edge.FromNodeId == nodeId)
            {
                connected.push_back(edge.ToNodeId);
            }
            else if (edge.ToNodeId == nodeId)
            {
                connected.push_back(edge.FromNodeId);
            }
        }
        return connected;
    }

    bool SnapGraphRuntime::CanDetachNode(const std::string& /*nodeId*/, std::string& outReason) const
    {
        // TODO:
        // - validate critical structure and mission locks
        outReason.clear();
        return true;
    }
}
