// AtlasWorldService.h
// World/scene service — open, save, query, and manage world/sector state.

#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include <optional>

namespace Atlas::Services
{

enum class WorldState : uint8_t
{
    Unloaded, Loading, Loaded, Saving, Error
};

struct SectorInfo
{
    uint64_t    sectorId    = 0;
    std::string name;
    bool        isLoaded    = false;
    uint32_t    entityCount = 0;
};

struct WorldStateSnapshot
{
    std::string worldId;
    WorldState  state          = WorldState::Unloaded;
    uint32_t    loadedSectors  = 0;
    uint32_t    totalEntities  = 0;
    bool        isDirty        = false;
    std::string lastSavedAt;
};

class AtlasWorldService
{
public:
    AtlasWorldService()  = default;
    ~AtlasWorldService() = default;

    void initialise();
    void shutdown();

    bool openWorld(const std::string& worldId);
    bool saveWorld(bool forceSave = false);
    bool closeWorld();

    WorldStateSnapshot      queryState()                              const;
    std::vector<SectorInfo> listSectors()                             const;
    std::optional<SectorInfo> querySector(uint64_t sectorId)          const;
    bool loadSector(uint64_t sectorId);
    bool unloadSector(uint64_t sectorId);

private:
    WorldStateSnapshot snapshot_;
    std::vector<SectorInfo> sectors_;
};

} // namespace Atlas::Services
