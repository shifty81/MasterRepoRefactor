// PCGDebugSystem.cpp
// Atlas Editor — PCG seed control, regeneration triggers, and debug visualization.

#include "PCG/PCGDebugSystem.h"

#include <algorithm>

namespace atlas::editor::pcg {

bool PCGDebugSystem::Initialize()
{
    m_state = {};
    return true;
}

void PCGDebugSystem::Shutdown() {}

void PCGDebugSystem::SetSeed(uint32_t seed)
{
    m_state.activeSeed = seed;
}

void PCGDebugSystem::RegenerateWorld()
{
    if (m_regenCb) m_regenCb(m_state.activeSeed);
}

void PCGDebugSystem::RegenerateSelected(const std::string& regionId)
{
    // Stub: run the generation pass restricted to regionId.
    (void)regionId;
    if (m_regenCb) m_regenCb(m_state.activeSeed);
}

void PCGDebugSystem::AddSpawnPoint(const PCGSpawnPoint& point)
{
    m_state.spawnPoints.push_back(point);
}

void PCGDebugSystem::ClearSpawnPoints()
{
    m_state.spawnPoints.clear();
}

void PCGDebugSystem::AddRegionBounds(const PCGGenerationBounds& bounds)
{
    m_state.regionBounds.push_back(bounds);
}

void PCGDebugSystem::ClearRegionBounds()
{
    m_state.regionBounds.clear();
}

void PCGDebugSystem::RegisterRule(const PCGRuleInspectorEntry& rule)
{
    m_state.rules.push_back(rule);
}

bool PCGDebugSystem::OverrideRule(const std::string& ruleId,
                                   const std::string& reason)
{
    for (auto& r : m_state.rules)
    {
        if (r.ruleId == ruleId)
        {
            r.isOverridden   = true;
            r.overrideReason = reason;
            return true;
        }
    }
    return false;
}

bool PCGDebugSystem::ClearOverride(const std::string& ruleId)
{
    for (auto& r : m_state.rules)
    {
        if (r.ruleId == ruleId)
        {
            r.isOverridden   = false;
            r.overrideReason.clear();
            return true;
        }
    }
    return false;
}

bool PCGDebugSystem::LockContent(const std::string& regionId)
{
    // Stub: mark the region so its generated content is preserved on next regen.
    (void)regionId;
    return true;
}

} // namespace atlas::editor::pcg
