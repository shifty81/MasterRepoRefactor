#pragma once

#include <string>
#include <vector>

namespace Runtime::BuilderRuntime
{
    struct SnapGraphEdge
    {
        std::string FromNodeId;
        std::string ToNodeId;
        std::string SocketType;
    };

    class SnapGraphRuntime
    {
    public:
        bool BuildFromAssembly(const std::string& assemblyId);
        std::vector<std::string> GetConnectedNodes(const std::string& nodeId) const;
        bool CanDetachNode(const std::string& nodeId, std::string& outReason) const;

    private:
        std::vector<SnapGraphEdge> m_edges;
    };
}
