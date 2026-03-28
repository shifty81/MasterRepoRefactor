// PCGDebugTypes.h
// Atlas Editor — PCG debug and seed-control data types.

#pragma once
#include <cstdint>
#include <string>
#include <vector>

namespace atlas::editor::pcg {

struct PCGSpawnPoint
{
    std::string label;     ///< human-readable tag ("asteroid_field", "station", ...)
    float       worldX = 0.f;
    float       worldY = 0.f;
    float       worldZ = 0.f;
    bool        visible = true;
};

struct PCGGenerationBounds
{
    std::string regionId;
    float       minX = 0.f, maxX = 0.f;
    float       minY = 0.f, maxY = 0.f;
    float       minZ = 0.f, maxZ = 0.f;
};

struct PCGRuleInspectorEntry
{
    std::string ruleId;
    std::string description;
    bool        isActive   = true;
    bool        isOverridden = false;
    std::string overrideReason;
};

struct PCGDebugState
{
    uint32_t                         activeSeed    = 0;
    bool                             showSpawnPoints = true;
    bool                             showBounds      = true;
    std::vector<PCGSpawnPoint>       spawnPoints;
    std::vector<PCGGenerationBounds> regionBounds;
    std::vector<PCGRuleInspectorEntry> rules;
};

} // namespace atlas::editor::pcg
