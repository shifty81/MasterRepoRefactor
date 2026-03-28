// SaveLoadExtensions.h
// Atlas Engine SaveLoad — extended save/load subsystems: player state,
// fleet/titan/season, structures/modules, contracts/economy.

#pragma once
#include <cstdint>
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::saveload {

// ---------------------------------------------------------------------------
// Generic save slot descriptor
// ---------------------------------------------------------------------------

struct SaveSlot
{
    uint32_t    slotId       = 0;
    std::string saveName;
    std::string timestamp;          ///< ISO-8601
    std::string version;            ///< schema version string
    uint64_t    playerId     = 0;
    uint32_t    playtimeSeconds = 0;
    bool        isValid      = true;
    bool        isAutoSave   = false;
};

// ---------------------------------------------------------------------------
// Player state save/load
// ---------------------------------------------------------------------------

struct PlayerSaveData
{
    uint64_t    playerId      = 0;
    float       health        = 100.f;
    float       shieldHP      = 100.f;
    float       credits       = 0.f;
    uint64_t    locationId    = 0;      ///< sector/station/system
    std::string activeCraftId;
    std::string playerState;            ///< "Idle", "Flying", etc.
    // Skills: serialised as "skill_id:level" pairs.
    std::vector<std::string> skillEntries;
};

// ---------------------------------------------------------------------------
// Fleet save/load
// ---------------------------------------------------------------------------

struct ShipSaveData
{
    uint64_t    shipId        = 0;
    std::string shipClass;
    float       hullHP        = 100.f;
    uint64_t    locationId    = 0;
    bool        isDocked      = false;
};

struct FleetSaveData
{
    uint64_t                  fleetId   = 0;
    uint64_t                  ownerId   = 0;
    std::vector<ShipSaveData> ships;
};

// ---------------------------------------------------------------------------
// Season / Titan save/load
// ---------------------------------------------------------------------------

struct TitanSaveEntry
{
    std::string titanId;
    float       progress   = 0.f;
    float       pressure   = 0.f;
    bool        isDefeated = false;
};

struct SeasonSaveData
{
    uint32_t                    seasonNumber    = 1;
    float                       globalPressure  = 0.f;
    std::string                 currentPhase;
    std::vector<TitanSaveEntry> titans;
};

// ---------------------------------------------------------------------------
// Structure / Module save/load
// ---------------------------------------------------------------------------

struct ModuleSaveEntry
{
    uint64_t    moduleId   = 0;
    std::string moduleType;
    float       posX = 0.f, posY = 0.f, posZ = 0.f;
    bool        isActive   = true;
};

struct StructureSaveData
{
    uint64_t                    structureId = 0;
    std::string                 structureType;
    uint64_t                    sectorId    = 0;
    std::vector<ModuleSaveEntry> modules;
};

// ---------------------------------------------------------------------------
// Contract / Economy save/load
// ---------------------------------------------------------------------------

struct ContractSaveEntry
{
    std::string contractId;
    std::string status;     ///< "active", "completed", "failed"
    float       progressPct = 0.f;
    uint64_t    assignedTo  = 0;
};

struct EconomySaveData
{
    uint64_t                      playerId = 0;
    float                         credits  = 0.f;
    std::vector<ContractSaveEntry> contracts;
    // Faction standings: "faction_id:standing" pairs.
    std::vector<std::string>       standingEntries;
};

// ---------------------------------------------------------------------------
// World-level save envelope
// ---------------------------------------------------------------------------

struct WorldSaveData
{
    uint32_t          slotId    = 0;
    PlayerSaveData    player;
    FleetSaveData     fleet;
    SeasonSaveData    season;
    EconomySaveData   economy;
    std::vector<StructureSaveData> structures;
    std::string       saveVersion = "1.0";
};

// ---------------------------------------------------------------------------
// Validation result for loaded data
// ---------------------------------------------------------------------------

struct SaveLoadValidation
{
    bool        success     = true;
    std::string errorMessage;
    std::vector<std::string> warnings;
};

// ---------------------------------------------------------------------------
// SaveLoadManager
// ---------------------------------------------------------------------------

using SaveCompleteCallback = std::function<void(uint32_t slotId, bool success)>;
using LoadCompleteCallback = std::function<void(uint32_t slotId, bool success, const std::string& error)>;

class SaveLoadManager
{
public:
    bool Initialize();
    void Shutdown();

    // ---- slot management -----------------------------------------------
    void  RegisterSlot(const SaveSlot& slot);
    bool  DeleteSlot  (uint32_t slotId);
    bool  HasSlot     (uint32_t slotId) const;
    std::optional<SaveSlot> FindSlot(uint32_t slotId) const;
    std::vector<SaveSlot>   ListSlots() const { return m_slots; }
    size_t SlotCount() const { return m_slots.size(); }

    // ---- save operations -----------------------------------------------
    bool SaveWorld    (const WorldSaveData& data);
    bool SavePlayer   (const PlayerSaveData& data);
    bool SaveFleet    (const FleetSaveData&  data);
    bool SaveSeason   (const SeasonSaveData& data);
    bool SaveEconomy  (const EconomySaveData& data);

    // ---- load operations -----------------------------------------------
    std::optional<WorldSaveData>   LoadWorld  (uint32_t slotId) const;
    std::optional<PlayerSaveData>  LoadPlayer (uint32_t slotId) const;
    std::optional<FleetSaveData>   LoadFleet  (uint32_t slotId) const;
    std::optional<SeasonSaveData>  LoadSeason (uint32_t slotId) const;
    std::optional<EconomySaveData> LoadEconomy(uint32_t slotId) const;

    // ---- validation ----------------------------------------------------
    SaveLoadValidation ValidateWorld(const WorldSaveData& data) const;
    bool               SchemaVersionMatches(const std::string& version) const;

    // ---- callbacks -----------------------------------------------------
    void SetSaveCompleteCallback(SaveCompleteCallback cb) { m_saveCb = std::move(cb); }
    void SetLoadCompleteCallback(LoadCompleteCallback cb) { m_loadCb = std::move(cb); }

    // ---- stats ---------------------------------------------------------
    size_t SaveCount() const { return m_saveCount; }
    size_t LoadCount() const { return m_loadCount; }

    static constexpr const char* CURRENT_VERSION = "1.0";

private:
    std::vector<SaveSlot>       m_slots;
    std::vector<WorldSaveData>  m_saves;
    size_t                      m_saveCount = 0;
    size_t                      m_loadCount = 0;
    SaveCompleteCallback        m_saveCb;
    LoadCompleteCallback        m_loadCb;

    SaveSlot* GetMutableSlot(uint32_t slotId);
};

} // namespace atlas::saveload
