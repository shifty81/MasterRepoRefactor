// PrefabLibrary.cpp
// Atlas Editor — prefab catalog.

#include "Prefabs/PrefabLibrary.h"

#include <algorithm>

namespace atlas::editor::prefab {

bool PrefabLibrary::Initialize() { return true; }
void PrefabLibrary::Shutdown()   { m_prefabs.clear(); }

bool PrefabLibrary::RegisterPrefab(const PrefabDefinition& def)
{
    for (const auto& p : m_prefabs)
        if (p.prefabId == def.prefabId) return false; // duplicate
    m_prefabs.push_back(def);
    return true;
}

bool PrefabLibrary::UnregisterPrefab(const std::string& prefabId)
{
    auto it = std::find_if(m_prefabs.begin(), m_prefabs.end(),
                           [&](const PrefabDefinition& p){ return p.prefabId == prefabId; });
    if (it == m_prefabs.end()) return false;
    m_prefabs.erase(it);
    return true;
}

std::optional<PrefabDefinition>
PrefabLibrary::FindById(const std::string& prefabId) const
{
    for (const auto& p : m_prefabs)
        if (p.prefabId == prefabId) return p;
    return std::nullopt;
}

std::vector<PrefabDefinition>
PrefabLibrary::ListByCategory(EPrefabCategory cat) const
{
    std::vector<PrefabDefinition> result;
    for (const auto& p : m_prefabs)
        if (p.category == cat) result.push_back(p);
    return result;
}

std::vector<PrefabDefinition>
PrefabLibrary::Search(const std::string& query) const
{
    std::vector<PrefabDefinition> result;
    for (const auto& p : m_prefabs)
    {
        bool match = false;
        auto contains = [&](const std::string& s) {
            return s.find(query) != std::string::npos;
        };
        if (contains(p.displayName) || contains(p.meta.author) ||
            contains(p.meta.description))
        {
            match = true;
        }
        if (!match)
        {
            for (const auto& tag : p.tags)
                if (contains(tag)) { match = true; break; }
        }
        if (match) result.push_back(p);
    }
    return result;
}

std::vector<PrefabDefinition> PrefabLibrary::ListAll() const
{
    return m_prefabs;
}

bool PrefabLibrary::UpdateMetadata(const std::string& prefabId,
                                    const PrefabMetadata& meta)
{
    PrefabDefinition* p = GetMutable(prefabId);
    if (!p) return false;
    p->meta = meta;
    return true;
}

bool PrefabLibrary::IncrementUseCount(const std::string& prefabId)
{
    PrefabDefinition* p = GetMutable(prefabId);
    if (!p) return false;
    ++p->meta.useCount;
    return true;
}

size_t PrefabLibrary::CountByCategory(EPrefabCategory cat) const
{
    return static_cast<size_t>(
        std::count_if(m_prefabs.begin(), m_prefabs.end(),
                      [cat](const PrefabDefinition& p){ return p.category == cat; }));
}

PrefabDefinition* PrefabLibrary::GetMutable(const std::string& prefabId)
{
    for (auto& p : m_prefabs)
        if (p.prefabId == prefabId) return &p;
    return nullptr;
}

} // namespace atlas::editor::prefab
