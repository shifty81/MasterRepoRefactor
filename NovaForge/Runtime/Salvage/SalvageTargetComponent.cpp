#include "SalvageTargetComponent.h"

namespace Runtime::Salvage
{
    bool SalvageTargetComponent::Initialize(const std::string& targetId, const std::string& nodeId)
    {
        m_targetId = targetId;
        m_nodeId = nodeId;
        return true;
    }

    bool SalvageTargetComponent::CanDetach(std::string& outReason) const
    {
        // TODO:
        // - tool, tier, structural lock, and mission validation
        outReason.clear();
        return true;
    }

    bool SalvageTargetComponent::StartDetach()
    {
        m_bDetachInProgress = true;
        return true;
    }

    bool SalvageTargetComponent::CompleteDetach()
    {
        if (!m_bDetachInProgress)
        {
            return false;
        }

        m_bDetachInProgress = false;
        // TODO:
        // - spawn loose actor or grant inventory item
        // - emit mission/save delta events
        return true;
    }

    const std::string& SalvageTargetComponent::GetTargetId() const
    {
        return m_targetId;
    }

    const std::string& SalvageTargetComponent::GetNodeId() const
    {
        return m_nodeId;
    }
}
