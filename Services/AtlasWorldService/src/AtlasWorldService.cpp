// AtlasWorldService.cpp
#include "AtlasWorldService.h"

namespace Atlas::Services
{

void AtlasWorldService::initialise() {}
void AtlasWorldService::shutdown()   { closeWorld(); }

bool AtlasWorldService::openWorld(const std::string& worldId)
{
    snapshot_.worldId = worldId;
    snapshot_.state   = WorldState::Loaded;
    snapshot_.isDirty = false;
    return true;
}

bool AtlasWorldService::saveWorld(bool)
{
    if (snapshot_.state == WorldState::Unloaded) return false;
    snapshot_.isDirty     = false;
    snapshot_.lastSavedAt = "stub-timestamp";
    return true;
}

bool AtlasWorldService::closeWorld()
{
    snapshot_ = {};
    sectors_.clear();
    return true;
}

WorldStateSnapshot AtlasWorldService::queryState() const { return snapshot_; }

std::vector<SectorInfo> AtlasWorldService::listSectors() const { return sectors_; }

std::optional<SectorInfo> AtlasWorldService::querySector(uint64_t sectorId) const
{
    for (const auto& s : sectors_)
        if (s.sectorId == sectorId) return s;
    return std::nullopt;
}

bool AtlasWorldService::loadSector(uint64_t sectorId)
{
    for (auto& s : sectors_)
        if (s.sectorId == sectorId) { s.isLoaded = true; ++snapshot_.loadedSectors; return true; }
    SectorInfo s; s.sectorId = sectorId; s.isLoaded = true;
    sectors_.push_back(s); ++snapshot_.loadedSectors;
    return true;
}

bool AtlasWorldService::unloadSector(uint64_t sectorId)
{
    for (auto& s : sectors_)
    {
        if (s.sectorId != sectorId || !s.isLoaded) continue;
        s.isLoaded = false;
        if (snapshot_.loadedSectors > 0) --snapshot_.loadedSectors;
        return true;
    }
    return false;
}

} // namespace Atlas::Services
