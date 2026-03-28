// SaveLoadExtensions.cpp
// Atlas Engine SaveLoad — extended save/load manager.

#include "SaveLoad/SaveLoadExtensions.h"

#include <algorithm>

namespace atlas::saveload {

bool SaveLoadManager::Initialize()
{
    m_saveCount = 0;
    m_loadCount = 0;
    return true;
}

void SaveLoadManager::Shutdown()
{
    m_slots.clear();
    m_saves.clear();
}

// ---- slot management -------------------------------------------------------

void SaveLoadManager::RegisterSlot(const SaveSlot& slot)
{
    for (auto& s : m_slots)
        if (s.slotId == slot.slotId) { s = slot; return; }
    m_slots.push_back(slot);
}

bool SaveLoadManager::DeleteSlot(uint32_t slotId)
{
    auto it = std::find_if(m_slots.begin(), m_slots.end(),
                           [slotId](const SaveSlot& s){ return s.slotId == slotId; });
    if (it == m_slots.end()) return false;
    m_slots.erase(it);

    m_saves.erase(
        std::remove_if(m_saves.begin(), m_saves.end(),
                       [slotId](const WorldSaveData& d){ return d.slotId == slotId; }),
        m_saves.end());
    return true;
}

bool SaveLoadManager::HasSlot(uint32_t slotId) const
{
    return FindSlot(slotId).has_value();
}

std::optional<SaveSlot> SaveLoadManager::FindSlot(uint32_t slotId) const
{
    for (const auto& s : m_slots)
        if (s.slotId == slotId) return s;
    return std::nullopt;
}

// ---- save operations -------------------------------------------------------

bool SaveLoadManager::SaveWorld(const WorldSaveData& data)
{
    // Upsert.
    for (auto& d : m_saves)
    {
        if (d.slotId == data.slotId) {
            d = data;
            ++m_saveCount;
            if (m_saveCb) m_saveCb(data.slotId, true);
            return true;
        }
    }
    m_saves.push_back(data);
    ++m_saveCount;
    if (m_saveCb) m_saveCb(data.slotId, true);
    return true;
}

bool SaveLoadManager::SavePlayer(const PlayerSaveData& data)
{
    // Find or create world save for the player's slot.
    for (auto& d : m_saves)
    {
        if (d.player.playerId == data.playerId || d.slotId == 0)
        {
            d.player = data;
            ++m_saveCount;
            return true;
        }
    }
    WorldSaveData wd;
    wd.player = data;
    m_saves.push_back(wd);
    ++m_saveCount;
    return true;
}

bool SaveLoadManager::SaveFleet(const FleetSaveData& data)
{
    for (auto& d : m_saves)
        if (d.fleet.ownerId == data.ownerId || m_saves.empty())
        { d.fleet = data; ++m_saveCount; return true; }
    WorldSaveData wd;
    wd.fleet = data;
    m_saves.push_back(wd);
    ++m_saveCount;
    return true;
}

bool SaveLoadManager::SaveSeason(const SeasonSaveData& data)
{
    if (!m_saves.empty())
    {
        m_saves.back().season = data;
        ++m_saveCount;
        return true;
    }
    WorldSaveData wd;
    wd.season = data;
    m_saves.push_back(wd);
    ++m_saveCount;
    return true;
}

bool SaveLoadManager::SaveEconomy(const EconomySaveData& data)
{
    if (!m_saves.empty())
    {
        m_saves.back().economy = data;
        ++m_saveCount;
        return true;
    }
    WorldSaveData wd;
    wd.economy = data;
    m_saves.push_back(wd);
    ++m_saveCount;
    return true;
}

// ---- load operations -------------------------------------------------------

std::optional<WorldSaveData> SaveLoadManager::LoadWorld(uint32_t slotId) const
{
    for (const auto& d : m_saves)
        if (d.slotId == slotId)
        {
            ++const_cast<SaveLoadManager*>(this)->m_loadCount;
            if (m_loadCb) m_loadCb(slotId, true, "");
            return d;
        }
    if (m_loadCb) m_loadCb(slotId, false, "Slot not found");
    return std::nullopt;
}

std::optional<PlayerSaveData> SaveLoadManager::LoadPlayer(
    uint32_t slotId) const
{
    auto world = LoadWorld(slotId);
    if (world) return world->player;
    return std::nullopt;
}

std::optional<FleetSaveData> SaveLoadManager::LoadFleet(
    uint32_t slotId) const
{
    auto world = LoadWorld(slotId);
    if (world) return world->fleet;
    return std::nullopt;
}

std::optional<SeasonSaveData> SaveLoadManager::LoadSeason(
    uint32_t slotId) const
{
    auto world = LoadWorld(slotId);
    if (world) return world->season;
    return std::nullopt;
}

std::optional<EconomySaveData> SaveLoadManager::LoadEconomy(
    uint32_t slotId) const
{
    auto world = LoadWorld(slotId);
    if (world) return world->economy;
    return std::nullopt;
}

// ---- validation ------------------------------------------------------------

SaveLoadValidation SaveLoadManager::ValidateWorld(
    const WorldSaveData& data) const
{
    SaveLoadValidation v;
    v.success = true;

    if (!SchemaVersionMatches(data.saveVersion))
    {
        v.warnings.push_back("Schema version mismatch: " + data.saveVersion);
    }
    if (data.player.playerId == 0)
    {
        v.warnings.push_back("Player ID is zero — may be a new game");
    }
    if (data.season.seasonNumber == 0)
    {
        v.warnings.push_back("Season number is zero");
    }
    if (data.fleet.ships.empty())
    {
        v.warnings.push_back("Fleet has no ships");
    }

    return v;
}

bool SaveLoadManager::SchemaVersionMatches(const std::string& version) const
{
    return version == CURRENT_VERSION;
}

SaveSlot* SaveLoadManager::GetMutableSlot(uint32_t slotId)
{
    for (auto& s : m_slots)
        if (s.slotId == slotId) return &s;
    return nullptr;
}

} // namespace atlas::saveload
