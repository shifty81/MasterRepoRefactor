// PrefabLibrary.h
// Atlas Editor — prefab catalog with category filtering, search, and preview.

#pragma once
#include "Prefabs/PrefabTypes.h"

#include <optional>
#include <string>
#include <vector>

namespace atlas::editor::prefab {

class PrefabLibrary
{
public:
    bool Initialize();
    void Shutdown();

    // ---- registration -----------------------------------------------
    bool RegisterPrefab(const PrefabDefinition& def);
    bool UnregisterPrefab(const std::string& prefabId);

    // ---- lookup / filter --------------------------------------------
    std::optional<PrefabDefinition> FindById(const std::string& prefabId) const;

    /// List all prefabs of a given category.
    std::vector<PrefabDefinition> ListByCategory(EPrefabCategory cat) const;

    /// Free-text search across name, tags, and author.
    std::vector<PrefabDefinition> Search(const std::string& query) const;

    std::vector<PrefabDefinition> ListAll() const;

    // ---- metadata update --------------------------------------------
    bool UpdateMetadata(const std::string& prefabId,
                        const PrefabMetadata& meta);
    bool IncrementUseCount(const std::string& prefabId);

    // ---- stats -------------------------------------------------------
    size_t Count()                          const { return m_prefabs.size(); }
    size_t CountByCategory(EPrefabCategory) const;

private:
    std::vector<PrefabDefinition> m_prefabs;
    PrefabDefinition* GetMutable(const std::string& prefabId);
};

} // namespace atlas::editor::prefab
