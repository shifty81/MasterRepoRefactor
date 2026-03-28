// HierarchyNode.h
// Atlas Editor — typed scene-hierarchy nodes with parent/child relationships.

#pragma once
#include <cstdint>
#include <string>
#include <vector>

namespace atlas::editor::outliner {

enum class ENodeType : uint8_t
{
    World,       ///< root world container
    Sector,      ///< space sector / area
    Entity,      ///< generic world entity
    Module,      ///< ship or structure module
    Structure,   ///< multi-module build
    Character,   ///< player or NPC character
    FleetGroup,  ///< fleet formation grouping
    VoxelChunk,  ///< voxel terrain chunk
    Light,       ///< light source
    Trigger,     ///< gameplay trigger volume
    Folder,      ///< editor-only organisational folder
};

/// Summary of one ECS component attached to a node — display only.
struct ComponentSummaryEntry
{
    std::string componentType;
    bool        isActive      = true;
    std::string shortValue;   ///< human-readable value snippet
};

/// One node in the scene hierarchy.
struct HierarchyNode
{
    std::string  nodeId;
    std::string  displayLabel;
    ENodeType    type         = ENodeType::Entity;
    std::string  parentNodeId;              ///< empty = root child
    std::vector<std::string> childNodeIds;

    // --- transform ----------------------------------------------------
    float posX = 0.f, posY = 0.f, posZ = 0.f;
    float rotX = 0.f, rotY = 0.f, rotZ = 0.f; ///< Euler degrees
    float scaleX = 1.f, scaleY = 1.f, scaleZ = 1.f;

    // --- ownership & links -------------------------------------------
    uint64_t    ownerId     = 0;   ///< player / faction / NPC owning entity
    uint32_t    factionId   = 0;
    std::string linkedAssetId;     ///< source asset / prefab ID

    // --- component summary -------------------------------------------
    std::vector<ComponentSummaryEntry> components;

    bool        isLocked    = false; ///< prevents accidental edits
    bool        isVisible   = true;
};

} // namespace atlas::editor::outliner
