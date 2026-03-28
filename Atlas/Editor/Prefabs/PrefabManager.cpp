// PrefabManager.cpp
// Atlas Editor — prefab manager: save from selection, load/place into scene.

#include "Prefabs/PrefabManager.h"

namespace atlas::editor::prefab {

PrefabManager::PrefabManager(PrefabLibrary& library)
    : m_library(library)
{}

bool PrefabManager::Initialize() { return true; }
void PrefabManager::Shutdown()   {}

std::optional<PrefabDefinition>
PrefabManager::CaptureFromSelection(
    const std::string&                   prefabId,
    const std::string&                   displayName,
    EPrefabCategory                      category,
    const std::vector<SelectionSnapshot>& selection)
{
    if (selection.empty()) return std::nullopt;

    PrefabDefinition def;
    def.prefabId     = prefabId;
    def.displayName  = displayName;
    def.category     = category;
    def.schemaVersion = 1;

    // Use the first node as origin; capture relative positions.
    float originX = selection[0].posX;
    float originY = selection[0].posY;
    float originZ = selection[0].posZ;

    for (const auto& snap : selection)
    {
        // Gather voxel cells.
        for (const auto& cell : snap.voxelCells)
            def.voxelCells.push_back(cell);

        // Capture as child node.
        PrefabChildNode child;
        child.localId  = snap.nodeId;
        child.type     = snap.type;
        child.relPosX  = snap.posX - originX;
        child.relPosY  = snap.posY - originY;
        child.relPosZ  = snap.posZ - originZ;
        child.relRotY  = snap.rotY;
        child.assetRef = snap.assetRef;
        def.children.push_back(child);
    }

    return def;
}

bool PrefabManager::SaveToLibrary(const PrefabDefinition& def)
{
    return m_library.RegisterPrefab(def);
}

PrefabPlacementResult PrefabManager::Place(const std::string& prefabId,
                                             float worldX, float worldY, float worldZ,
                                             float rotY)
{
    auto opt = m_library.FindById(prefabId);
    if (!opt)
    {
        return { false, "", 0, "Prefab not found: " + prefabId };
    }

    m_library.IncrementUseCount(prefabId);

    if (m_placeCb)
    {
        auto result = m_placeCb(*opt, worldX, worldY, worldZ, rotY);
        return result;
    }

    // Stub result when no callback is registered.
    return { true, prefabId + "_instance_" + std::to_string(m_counter++),
             static_cast<int32_t>(opt->children.size()), "" };
}

std::string PrefabManager::GenerateId(const std::string& baseName)
{
    return baseName + "_" + std::to_string(m_counter++);
}

} // namespace atlas::editor::prefab
