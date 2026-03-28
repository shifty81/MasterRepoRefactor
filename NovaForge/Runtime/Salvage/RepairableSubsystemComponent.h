#pragma once

#include <string>

namespace Runtime::Salvage
{
    class RepairableSubsystemComponent
    {
    public:
        bool Initialize(const std::string& subsystemId);
        bool IsFaulted() const;
        bool BeginRepair();
        bool CompleteRepair();

    private:
        std::string m_subsystemId;
        bool m_bFaulted = true;
        bool m_bRepairInProgress = false;
    };
}
