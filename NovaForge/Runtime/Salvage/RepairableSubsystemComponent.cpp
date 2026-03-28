#include "RepairableSubsystemComponent.h"

namespace Runtime::Salvage
{
    bool RepairableSubsystemComponent::Initialize(const std::string& subsystemId)
    {
        m_subsystemId = subsystemId;
        return true;
    }

    bool RepairableSubsystemComponent::IsFaulted() const
    {
        return m_bFaulted;
    }

    bool RepairableSubsystemComponent::BeginRepair()
    {
        if (!m_bFaulted)
        {
            return false;
        }

        m_bRepairInProgress = true;
        return true;
    }

    bool RepairableSubsystemComponent::CompleteRepair()
    {
        if (!m_bRepairInProgress)
        {
            return false;
        }

        m_bRepairInProgress = false;
        m_bFaulted = false;
        // TODO:
        // - propagate subsystem restoration to dependent nodes/systems
        return true;
    }
}
