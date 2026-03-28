// PCGDeterminismEngine.h
// Atlas Engine PCG — seed-based deterministic procedural generation:
// seed management, determinism guarantees, seed panel integration,
// regenerate API, and generation state inspection.

#pragma once
#include <cstdint>
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::pcg {

// ---------------------------------------------------------------------------
// PCG category (what kind of content is being generated)
// ---------------------------------------------------------------------------

enum class EPCGCategory : uint8_t
{
    Terrain,
    AsteroidField,
    LootTable,
    Encounter,
    StationLayout,
    Mission,
    Galaxy,
    DungeonRoom,
    NPC,
    Economy,
};

// ---------------------------------------------------------------------------
// Seed entry
// ---------------------------------------------------------------------------

struct PCGSeed
{
    std::string   generatorId;    ///< which generator this seed belongs to
    EPCGCategory  category        = EPCGCategory::Terrain;
    uint64_t      seed            = 0;
    std::string   label;          ///< human-readable description
    bool          isLocked        = false;  ///< locked seeds won't regenerate
    bool          isDirty         = false;  ///< flagged for re-generation
    uint64_t      generationCount = 0;      ///< how many times this was generated
};

// ---------------------------------------------------------------------------
// LCG random number generator (deterministic, reproducible)
// ---------------------------------------------------------------------------

class DeterministicRNG
{
public:
    explicit DeterministicRNG(uint64_t seed = 0) : m_state(seed) {}

    void     Seed(uint64_t seed)   { m_state = seed; }
    uint64_t State() const         { return m_state; }

    uint64_t NextUInt64();
    uint32_t NextUInt32();
    float    NextFloat01();      ///< [0, 1)
    float    NextFloatRange(float lo, float hi);
    int32_t  NextIntRange(int32_t lo, int32_t hi);
    bool     NextBool(float probability = 0.5f);

    /// Derive a child seed deterministically (useful for sub-systems).
    uint64_t DeriveChildSeed(const std::string& namespace_key) const;

private:
    uint64_t m_state = 0;
};

// ---------------------------------------------------------------------------
// Generation request
// ---------------------------------------------------------------------------

struct PCGGenerateRequest
{
    std::string   generatorId;
    EPCGCategory  category     = EPCGCategory::Terrain;
    uint64_t      seed         = 0;      ///< 0 = auto-assign
    bool          forceRegen   = false;
    std::string   context;               ///< e.g. "sector_alpha_007"
};

// ---------------------------------------------------------------------------
// Generation result (content type-erased as strings for portability)
// ---------------------------------------------------------------------------

struct PCGGenerateResult
{
    bool          success       = false;
    std::string   generatorId;
    uint64_t      usedSeed      = 0;
    std::string   category;
    std::vector<std::string> outputTokens;   ///< type-erased output summary
    std::string   errorMessage;
};

// ---------------------------------------------------------------------------
// Generator registration
// ---------------------------------------------------------------------------

using PCGGeneratorFn = std::function<PCGGenerateResult(
    const PCGGenerateRequest&, DeterministicRNG&)>;

struct PCGGeneratorDef
{
    std::string     generatorId;
    EPCGCategory    category    = EPCGCategory::Terrain;
    std::string     description;
    PCGGeneratorFn  fn;
    bool            isEnabled   = true;
};

// ---------------------------------------------------------------------------
// PCGDeterminismEngine
// ---------------------------------------------------------------------------

class PCGDeterminismEngine
{
public:
    bool Initialize(uint64_t masterSeed = 0);
    void Shutdown();

    // ---- master seed ---------------------------------------------------
    void     SetMasterSeed(uint64_t seed);
    uint64_t GetMasterSeed() const { return m_masterSeed; }

    // ---- seed management -----------------------------------------------
    void  RegisterSeed   (const PCGSeed& seed);
    bool  SetSeed        (const std::string& generatorId, uint64_t seed);
    bool  LockSeed       (const std::string& generatorId);
    bool  UnlockSeed     (const std::string& generatorId);
    bool  MarkDirty      (const std::string& generatorId);
    bool  ClearDirty     (const std::string& generatorId);
    bool  HasSeed        (const std::string& generatorId) const;
    std::optional<PCGSeed> FindSeed(const std::string& generatorId) const;
    std::vector<PCGSeed>   ListSeeds(EPCGCategory cat) const;
    std::vector<PCGSeed>   GetDirtySeeds()  const;
    std::vector<PCGSeed>   GetLockedSeeds() const;
    size_t SeedCount() const { return m_seeds.size(); }

    // ---- generator registration ----------------------------------------
    void RegisterGenerator(const PCGGeneratorDef& def);
    bool HasGenerator(const std::string& generatorId) const;

    // ---- generation ----------------------------------------------------
    PCGGenerateResult Generate  (const PCGGenerateRequest& request);
    PCGGenerateResult Regenerate(const std::string& generatorId,
                                   const std::string& context = "");
    void              RegenerateAll(EPCGCategory category);
    void              RegenerateDirty();

    /// Auto-assign deterministic seed from master + generator ID hash.
    uint64_t          AutoAssignSeed(const std::string& generatorId);

    // ---- determinism helpers -------------------------------------------
    DeterministicRNG  CreateRNG(const std::string& generatorId) const;
    bool              VerifyDeterminism(const std::string& generatorId,
                                         uint32_t trialCount = 3) const;

    // ---- panel integration ---------------------------------------------
    /// Returns seed panel summary (for UI display).
    struct SeedPanelEntry { std::string id; std::string label; uint64_t seed;
                            bool locked; bool dirty; std::string category; };
    std::vector<SeedPanelEntry> GetSeedPanelEntries() const;

    // ---- callback -------------------------------------------------------
    using GenerationCompleteCallback = std::function<void(const PCGGenerateResult&)>;
    void SetGenerationCompleteCallback(GenerationCompleteCallback cb)
    { m_genCb = std::move(cb); }

    size_t GenerationCount() const { return m_totalGenerations; }

private:
    uint64_t                        m_masterSeed       = 12345;
    std::vector<PCGSeed>            m_seeds;
    std::vector<PCGGeneratorDef>    m_generators;
    std::vector<PCGGenerateResult>  m_history;
    size_t                          m_totalGenerations = 0;
    GenerationCompleteCallback      m_genCb;

    PCGSeed* GetMutable(const std::string& generatorId);
    const PCGGeneratorDef* FindGeneratorDef(const std::string& generatorId) const;
};

} // namespace atlas::pcg
