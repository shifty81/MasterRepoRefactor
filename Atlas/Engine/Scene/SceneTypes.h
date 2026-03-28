// SceneTypes.h
// Atlas Engine — scene primitive types: node IDs, node type enum,
// transform, and node flags bitfield.

#pragma once
#include <cstdint>
#include <string>

namespace atlas::engine::scene {

// ---------------------------------------------------------------------------
// Scene node ID
// ---------------------------------------------------------------------------

using SceneNodeId = uint32_t;
inline constexpr SceneNodeId kInvalidNodeId = 0;

// ---------------------------------------------------------------------------
// Node type
// ---------------------------------------------------------------------------

enum class ESceneNodeType : uint8_t
{
    Static,       ///< immovable world geometry
    Dynamic,      ///< movable object driven by physics or animation
    Light,        ///< point / spot / directional light source
    Camera,       ///< view frustum / render camera
    VoxelChunk,   ///< procedural voxel terrain chunk
    Character,    ///< player or NPC with capsule presence
    EditorOnly,   ///< gizmos / helper objects stripped in shipping builds
};

// ---------------------------------------------------------------------------
// Transform
// ---------------------------------------------------------------------------

struct SceneTransform
{
    float posX = 0.f, posY = 0.f, posZ = 0.f;
    float rotX = 0.f, rotY = 0.f, rotZ = 0.f, rotW = 1.f; ///< unit quaternion
    float scaleX = 1.f, scaleY = 1.f, scaleZ = 1.f;
};

// ---------------------------------------------------------------------------
// Node flags (bit-mask)
// ---------------------------------------------------------------------------

using SceneNodeFlags = uint32_t;

namespace NodeFlags {
    inline constexpr SceneNodeFlags None        = 0x00000000;
    inline constexpr SceneNodeFlags Visible     = 0x00000001; ///< included in render pass
    inline constexpr SceneNodeFlags CastShadow  = 0x00000002;
    inline constexpr SceneNodeFlags ReceiveShadow = 0x00000004;
    inline constexpr SceneNodeFlags Selected    = 0x00000008; ///< editor selection highlight
    inline constexpr SceneNodeFlags Locked      = 0x00000010; ///< editor lock (no transform edit)
    inline constexpr SceneNodeFlags Static      = 0x00000020; ///< signals transform won't change at runtime
    inline constexpr SceneNodeFlags Hidden      = 0x00000040; ///< excluded from all passes
    inline constexpr SceneNodeFlags Defaults    = Visible | CastShadow | ReceiveShadow;
}

} // namespace atlas::engine::scene
