// PrefabManager.h
// Atlas Editor — prefab manager: save from selection, load/place into scene,
// and session-level prefab operations.

#pragma once
#include "Prefabs/PrefabTypes.h"
#include "Prefabs/PrefabLibrary.h"

#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::editor::prefab {

/// Context snapshot of one selected node needed for prefab capture.
struct SelectionSnapshot
{
    std::string nodeId;
    std::string type;
    float posX = 0.f, posY = 0.f, posZ = 0.f;
    float rotY = 0.f;
    std::string assetRef;
    std::vector<PrefabVoxelCell> voxelCells; ///< filled when type == VoxelChunk
};

/// Result of placing a prefab into the scene.
struct PrefabPlacementResult
{
    bool        success    = false;
    std::string rootNodeId;          ///< newly created root node ID
    int32_t     nodesCreated = 0;
    std::string failureReason;
};

/// Callback invoked when a prefab is placed — allows the scene system to
/// materialise the resulting nodes.
using PrefabPlaceCallback =
    std::function<PrefabPlacementResult(const PrefabDefinition&,
                                         float worldX, float worldY, float worldZ,
                                         float rotY)>;

class PrefabManager
{
public:
    explicit PrefabManager(PrefabLibrary& library);

    bool Initialize();
    void Shutdown();

    // ---- save from selection ----------------------------------------
    /// Capture a prefab definition from the current selection snapshot.
    std::optional<PrefabDefinition> CaptureFromSelection(
        const std::string& prefabId,
        const std::string& displayName,
        EPrefabCategory    category,
        const std::vector<SelectionSnapshot>& selection);

    /// Save the captured definition into the library.
    bool SaveToLibrary(const PrefabDefinition& def);

    // ---- load / place -----------------------------------------------
    PrefabPlacementResult Place(const std::string& prefabId,
                                 float worldX, float worldY, float worldZ,
                                 float rotY = 0.f);

    void SetPlaceCallback(PrefabPlaceCallback cb) { m_placeCb = std::move(cb); }

    // ---- helpers ----------------------------------------------------
    /// Generate a unique prefab ID (timestamp + counter).
    std::string GenerateId(const std::string& baseName);

private:
    PrefabLibrary&      m_library;
    PrefabPlaceCallback m_placeCb;
    uint32_t            m_counter = 0;
};

} // namespace atlas::editor::prefab
