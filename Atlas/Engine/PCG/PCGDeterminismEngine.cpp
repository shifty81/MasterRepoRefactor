// PCGDeterminismEngine.cpp
// Atlas Engine PCG — deterministic PCG engine.

#include "PCG/PCGDeterminismEngine.h"

#include <algorithm>
#include <functional>

namespace atlas::pcg {

// ---- DeterministicRNG ------------------------------------------------------

static uint64_t lcgNext(uint64_t s)
{
    // LCG parameters (same as Java's LCG, well-studied).
    return s * 6364136223846793005ULL + 1442695040888963407ULL;
}

uint64_t DeterministicRNG::NextUInt64()
{
    m_state = lcgNext(m_state);
    return m_state;
}

uint32_t DeterministicRNG::NextUInt32()
{
    return static_cast<uint32_t>(NextUInt64() >> 32);
}

float DeterministicRNG::NextFloat01()
{
    return static_cast<float>(NextUInt32()) / 4294967296.f;
}

float DeterministicRNG::NextFloatRange(float lo, float hi)
{
    return lo + NextFloat01() * (hi - lo);
}

int32_t DeterministicRNG::NextIntRange(int32_t lo, int32_t hi)
{
    if (hi <= lo) return lo;
    return lo + static_cast<int32_t>(NextUInt32() % static_cast<uint32_t>(hi - lo));
}

bool DeterministicRNG::NextBool(float probability)
{
    return NextFloat01() < probability;
}

uint64_t DeterministicRNG::DeriveChildSeed(const std::string& key) const
{
    // Simple but deterministic: hash the key, XOR with current state.
    uint64_t h = 14695981039346656037ULL;
    for (char c : key) {
        h ^= static_cast<uint8_t>(c);
        h *= 1099511628211ULL;
    }
    return m_state ^ h;
}

// ---- PCGDeterminismEngine --------------------------------------------------

bool PCGDeterminismEngine::Initialize(uint64_t masterSeed)
{
    m_masterSeed       = (masterSeed == 0) ? 12345ULL : masterSeed;
    m_totalGenerations = 0;
    return true;
}

void PCGDeterminismEngine::Shutdown()
{
    m_seeds.clear();
    m_generators.clear();
    m_history.clear();
}

void PCGDeterminismEngine::SetMasterSeed(uint64_t seed)
{
    m_masterSeed = seed;
}

void PCGDeterminismEngine::RegisterSeed(const PCGSeed& seed)
{
    for (auto& s : m_seeds)
        if (s.generatorId == seed.generatorId) { s = seed; return; }
    m_seeds.push_back(seed);
}

bool PCGDeterminismEngine::SetSeed(const std::string& generatorId,
                                     uint64_t seed)
{
    PCGSeed* s = GetMutable(generatorId);
    if (!s || s->isLocked) return false;
    s->seed    = seed;
    s->isDirty = true;
    return true;
}

bool PCGDeterminismEngine::LockSeed(const std::string& generatorId)
{
    PCGSeed* s = GetMutable(generatorId);
    if (!s) return false;
    s->isLocked = true;
    return true;
}

bool PCGDeterminismEngine::UnlockSeed(const std::string& generatorId)
{
    PCGSeed* s = GetMutable(generatorId);
    if (!s) return false;
    s->isLocked = false;
    return true;
}

bool PCGDeterminismEngine::MarkDirty(const std::string& generatorId)
{
    PCGSeed* s = GetMutable(generatorId);
    if (!s) return false;
    s->isDirty = true;
    return true;
}

bool PCGDeterminismEngine::ClearDirty(const std::string& generatorId)
{
    PCGSeed* s = GetMutable(generatorId);
    if (!s) return false;
    s->isDirty = false;
    return true;
}

bool PCGDeterminismEngine::HasSeed(const std::string& generatorId) const
{
    return FindSeed(generatorId).has_value();
}

std::optional<PCGSeed> PCGDeterminismEngine::FindSeed(
    const std::string& generatorId) const
{
    for (const auto& s : m_seeds)
        if (s.generatorId == generatorId) return s;
    return std::nullopt;
}

std::vector<PCGSeed> PCGDeterminismEngine::ListSeeds(
    EPCGCategory cat) const
{
    std::vector<PCGSeed> result;
    for (const auto& s : m_seeds)
        if (s.category == cat) result.push_back(s);
    return result;
}

std::vector<PCGSeed> PCGDeterminismEngine::GetDirtySeeds() const
{
    std::vector<PCGSeed> result;
    for (const auto& s : m_seeds)
        if (s.isDirty) result.push_back(s);
    return result;
}

std::vector<PCGSeed> PCGDeterminismEngine::GetLockedSeeds() const
{
    std::vector<PCGSeed> result;
    for (const auto& s : m_seeds)
        if (s.isLocked) result.push_back(s);
    return result;
}

void PCGDeterminismEngine::RegisterGenerator(const PCGGeneratorDef& def)
{
    for (auto& g : m_generators)
        if (g.generatorId == def.generatorId) { g = def; return; }
    m_generators.push_back(def);
}

bool PCGDeterminismEngine::HasGenerator(
    const std::string& generatorId) const
{
    return FindGeneratorDef(generatorId) != nullptr;
}

PCGGenerateResult PCGDeterminismEngine::Generate(
    const PCGGenerateRequest& request)
{
    PCGGenerateResult result;
    result.generatorId = request.generatorId;
    result.category    = std::to_string(static_cast<int>(request.category));

    PCGSeed* seed = GetMutable(request.generatorId);
    uint64_t usedSeed = request.seed;

    if (usedSeed == 0)
        usedSeed = AutoAssignSeed(request.generatorId);

    if (seed)
    {
        if (seed->isLocked && !request.forceRegen)
        {
            result.success      = false;
            result.errorMessage = "Seed is locked";
            return result;
        }
        seed->seed = usedSeed;
        ++seed->generationCount;
        seed->isDirty = false;
    }

    result.usedSeed = usedSeed;

    const PCGGeneratorDef* def = FindGeneratorDef(request.generatorId);
    if (def && def->fn)
    {
        DeterministicRNG rng(usedSeed);
        result = def->fn(request, rng);
        result.usedSeed = usedSeed;
    }
    else
    {
        // Default placeholder generation.
        DeterministicRNG rng(usedSeed);
        result.success = true;
        result.outputTokens.push_back("generated:" + request.generatorId);
        result.outputTokens.push_back("seed:" + std::to_string(usedSeed));
        result.outputTokens.push_back("context:" + request.context);
    }

    ++m_totalGenerations;
    m_history.push_back(result);
    if (m_genCb) m_genCb(result);
    return result;
}

PCGGenerateResult PCGDeterminismEngine::Regenerate(
    const std::string& generatorId, const std::string& context)
{
    PCGGenerateRequest req;
    req.generatorId = generatorId;
    req.forceRegen  = true;
    req.context     = context;
    auto seed = FindSeed(generatorId);
    if (seed) { req.seed = seed->seed; req.category = seed->category; }
    return Generate(req);
}

void PCGDeterminismEngine::RegenerateAll(EPCGCategory category)
{
    for (const auto& s : m_seeds)
        if (s.category == category && !s.isLocked)
            Regenerate(s.generatorId);
}

void PCGDeterminismEngine::RegenerateDirty()
{
    for (const auto& s : m_seeds)
        if (s.isDirty && !s.isLocked)
            Regenerate(s.generatorId);
}

uint64_t PCGDeterminismEngine::AutoAssignSeed(
    const std::string& generatorId) const
{
    // Deterministically derive from master seed + generator ID hash.
    uint64_t h = 14695981039346656037ULL;
    for (char c : generatorId) { h ^= static_cast<uint8_t>(c); h *= 1099511628211ULL; }
    return m_masterSeed ^ h;
}

DeterministicRNG PCGDeterminismEngine::CreateRNG(
    const std::string& generatorId) const
{
    auto seed = FindSeed(generatorId);
    uint64_t s = seed ? seed->seed : AutoAssignSeed(generatorId);
    return DeterministicRNG(s);
}

bool PCGDeterminismEngine::VerifyDeterminism(
    const std::string& generatorId, uint32_t trialCount) const
{
    // Run generation multiple times with same seed; outputs must match.
    PCGGenerateRequest req;
    req.generatorId = generatorId;
    req.forceRegen  = true;
    req.seed        = AutoAssignSeed(generatorId);

    const PCGGeneratorDef* def = FindGeneratorDef(generatorId);
    if (!def || !def->fn) return true;  // no generator = trivially deterministic

    DeterministicRNG rng0(req.seed);
    PCGGenerateResult first = def->fn(req, rng0);

    for (uint32_t i = 1; i < trialCount; ++i)
    {
        DeterministicRNG rng(req.seed);
        PCGGenerateResult trial = def->fn(req, rng);
        if (trial.outputTokens != first.outputTokens) return false;
    }
    return true;
}

std::vector<PCGDeterminismEngine::SeedPanelEntry>
PCGDeterminismEngine::GetSeedPanelEntries() const
{
    std::vector<SeedPanelEntry> result;
    for (const auto& s : m_seeds)
    {
        SeedPanelEntry e;
        e.id       = s.generatorId;
        e.label    = s.label.empty() ? s.generatorId : s.label;
        e.seed     = s.seed;
        e.locked   = s.isLocked;
        e.dirty    = s.isDirty;
        e.category = std::to_string(static_cast<int>(s.category));
        result.push_back(e);
    }
    return result;
}

PCGSeed* PCGDeterminismEngine::GetMutable(const std::string& generatorId)
{
    for (auto& s : m_seeds)
        if (s.generatorId == generatorId) return &s;
    return nullptr;
}

const PCGGeneratorDef* PCGDeterminismEngine::FindGeneratorDef(
    const std::string& generatorId) const
{
    for (const auto& g : m_generators)
        if (g.generatorId == generatorId) return &g;
    return nullptr;
}

} // namespace atlas::pcg
