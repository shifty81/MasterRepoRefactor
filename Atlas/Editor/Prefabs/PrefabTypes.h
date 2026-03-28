// PrefabTypes.h
// Atlas Editor — prefab (template) data types for saved/reusable building blocks.

#pragma once
#include <cstdint>
#include <string>
#include <vector>

namespace atlas::editor::prefab {

enum class EPrefabCategory : uint8_t
{
    Structure,    ///< rooms, corridors, docking bays
    Module,       ///< ship modules (weapons, engines, reactors)
    Decoration,   ///< non-functional props
    Terrain,      ///< voxel terrain features (cave, cliff, plateau)
    Character,    ///< character rig templates
    Trigger,      ///< gameplay trigger volumes
    Lighting,     ///< light and atmosphere rigs
    Misc
};

/// One voxel cell captured from the editor at save time.
struct PrefabVoxelCell
{
    int32_t  localX = 0, localY = 0, localZ = 0;
    uint8_t  material  = 0;
    uint8_t  shape     = 0;
};

/// One child entity captured inside a prefab.
struct PrefabChildNode
{
    std::string localId;
    std::string type;       ///< node type tag
    float       relPosX = 0.f, relPosY = 0.f, relPosZ = 0.f;
    float       relRotY = 0.f;
    std::string assetRef;
};

/// Preview / metadata for library browsing.
struct PrefabMetadata
{
    std::string    author;
    std::string    description;
    std::string    thumbnailPath;    ///< relative path to icon/screenshot
    uint32_t       useCount    = 0;  ///< how many times this has been placed
    bool           isBuiltIn   = false;
};

/// The full prefab definition.
struct PrefabDefinition
{
    std::string              prefabId;
    std::string              displayName;
    EPrefabCategory          category = EPrefabCategory::Misc;
    std::vector<PrefabVoxelCell>  voxelCells;
    std::vector<PrefabChildNode>  children;
    std::vector<std::string> tags;
    PrefabMetadata           meta;
    uint32_t                 schemaVersion = 1;
};

} // namespace atlas::editor::prefab
