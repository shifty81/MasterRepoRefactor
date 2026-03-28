// PhysicsTypes.h
// Atlas Engine — physics primitive types: bodies, shapes, collision layers, ray-cast.

#pragma once
#include <cstdint>
#include <string>
#include <vector>

namespace atlas::physics {

// ---------------------------------------------------------------------------
// Collision layers (bit-mask)
// ---------------------------------------------------------------------------

using CollisionLayer = uint32_t;

namespace Layers {
    inline constexpr CollisionLayer None          = 0x00000000;
    inline constexpr CollisionLayer World         = 0x00000001; ///< static world geometry
    inline constexpr CollisionLayer DynamicEntity = 0x00000002; ///< ships, players, props
    inline constexpr CollisionLayer Trigger       = 0x00000004; ///< trigger volumes (no collision response)
    inline constexpr CollisionLayer Projectile    = 0x00000008;
    inline constexpr CollisionLayer Character     = 0x00000010;
    inline constexpr CollisionLayer VoxelChunk    = 0x00000020;
    inline constexpr CollisionLayer Module        = 0x00000040;
    inline constexpr CollisionLayer EditorOnly    = 0x80000000; ///< gizmos / editor preview
    inline constexpr CollisionLayer All           = 0xFFFFFFFF;
}

// ---------------------------------------------------------------------------
// Shape types
// ---------------------------------------------------------------------------

enum class EPhysicsShape : uint8_t
{
    Box,
    Sphere,
    Capsule,
    ConvexHull,
    TriangleMesh,   ///< static only
    Compound,
};

struct PhysicsShapeDesc
{
    EPhysicsShape type         = EPhysicsShape::Box;
    float         halfExtentX  = 0.5f;
    float         halfExtentY  = 0.5f;
    float         halfExtentZ  = 0.5f;  ///< radius for sphere/capsule
    float         capsuleRadius = 0.25f;
    float         capsuleHalfHeight = 0.5f;
};

// ---------------------------------------------------------------------------
// Physics body motion type
// ---------------------------------------------------------------------------

enum class EBodyMotion : uint8_t
{
    Static,         ///< never moves (world geometry)
    Kinematic,      ///< moves, but not driven by forces (animated platforms)
    Dynamic,        ///< fully simulated rigidbody
};

// ---------------------------------------------------------------------------
// Physics body descriptor
// ---------------------------------------------------------------------------

struct PhysicsBodyDesc
{
    uint64_t         entityId     = 0;
    EBodyMotion      motion       = EBodyMotion::Dynamic;
    PhysicsShapeDesc shape;
    float            mass         = 1.0f;         ///< kg (ignored for Static/Kinematic)
    float            linearDamping  = 0.05f;
    float            angularDamping = 0.05f;
    float            restitution    = 0.3f;
    float            friction       = 0.5f;
    CollisionLayer   layer          = Layers::DynamicEntity;
    CollisionLayer   collidesWith   = Layers::All;
    bool             isTrigger      = false;
    bool             disableGravity = false;
};

// ---------------------------------------------------------------------------
// Physics body state (position/velocity snapshot)
// ---------------------------------------------------------------------------

struct PhysicsBodyState
{
    uint64_t entityId = 0;
    float    posX = 0.f, posY = 0.f, posZ = 0.f;
    float    rotX = 0.f, rotY = 0.f, rotZ = 0.f, rotW = 1.f; ///< quaternion
    float    velX = 0.f, velY = 0.f, velZ = 0.f;
    float    angVelX = 0.f, angVelY = 0.f, angVelZ = 0.f;
    bool     isAwake = true;
};

// ---------------------------------------------------------------------------
// Ray-cast
// ---------------------------------------------------------------------------

struct RayCast
{
    float originX, originY, originZ;
    float dirX, dirY, dirZ;    ///< normalised direction
    float maxDistance = 1000.f;
    CollisionLayer queryLayers = Layers::All;
};

struct RayCastHit
{
    bool     hasHit      = false;
    uint64_t entityId    = 0;
    float    distance    = 0.f;
    float    hitX = 0.f, hitY = 0.f, hitZ = 0.f;   ///< world-space hit point
    float    normalX = 0.f, normalY = 0.f, normalZ = 0.f;
    CollisionLayer hitLayer = Layers::None;
};

// ---------------------------------------------------------------------------
// Collision contact
// ---------------------------------------------------------------------------

struct CollisionContact
{
    uint64_t entityA    = 0;
    uint64_t entityB    = 0;
    float    impulse    = 0.f;
    float    normalX, normalY, normalZ;
    bool     isTrigger  = false;
};

} // namespace atlas::physics
