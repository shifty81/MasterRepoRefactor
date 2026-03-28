#pragma once

#include <string>

namespace Runtime::Salvage
{
    enum class EDetachMode
    {
        CutFree,
        Unbolt,
        Unsocket,
        ExtractCore,
        HarvestMaterial,
        MissionRetrieve
    };

    class SalvageTargetComponent
    {
    public:
        bool Initialize(const std::string& targetId, const std::string& nodeId);
        bool CanDetach(std::string& outReason) const;
        bool StartDetach();
        bool CompleteDetach();

        const std::string& GetTargetId() const;
        const std::string& GetNodeId() const;

    private:
        std::string m_targetId;
        std::string m_nodeId;
        bool m_bDetachInProgress = false;
    };
}
