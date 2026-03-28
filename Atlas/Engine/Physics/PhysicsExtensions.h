// PhysicsExtensions.h
// Atlas Engine — extends PhysicsWorld with collision layer filtering,
// ray-cast, sphere overlap, and contact/trigger callbacks.

#pragma once
#include "PhysicsWorld.h"

#include <functional>
#include <optional>
#include <string>

namespace atlas::physics {

// ---------------------------------------------------------------------------
// Collision layer bitmask
// ---------------------------------------------------------------------------

using CollisionLayer = uint32_t;

namespace Layers {
    inline constexpr CollisionLayer None          = 0x00000000;
    inline constexpr CollisionLayer World         = 0x00000001;
    inline constexpr CollisionLayer DynamicEntity = 0x00000002;
    inline constexpr CollisionLayer Trigger       = 0x00000004;
    inline constexpr CollisionLayer Projectile    = 0x00000008;
    inline constexpr CollisionLayer Character     = 0x00000010;
    inline constexpr CollisionLayer VoxelChunk    = 0x00000020;
    inline constexpr CollisionLayer Module        = 0x00000040;
    inline constexpr CollisionLayer EditorOnly    = 0x80000000;
    inline constexpr CollisionLayer All           = 0xFFFFFFFF;
}

// ---------------------------------------------------------------------------
// Body layer assignments (body ID → layer mask)
// ---------------------------------------------------------------------------

struct BodyLayerEntry
{
    BodyID          id            = 0;
    CollisionLayer  layer         = Layers::DynamicEntity;
    CollisionLayer  collidesWith  = Layers::All;
    bool            isTrigger     = false;
};

// ---------------------------------------------------------------------------
// Ray-cast
// ---------------------------------------------------------------------------

struct RayCast
{
    float originX, originY, originZ;
    float dirX, dirY, dirZ;     ///< normalised
    float maxDistance          = 1000.f;
    CollisionLayer queryLayers = Layers::All;
};

struct RayCastHit
{
    bool           hasHit    = false;
    BodyID         bodyId    = 0;
    float          distance  = 0.f;
    float          hitX = 0.f, hitY = 0.f, hitZ = 0.f;
    float          normalX = 0.f, normalY = 0.f, normalZ = 0.f;
    CollisionLayer hitLayer  = Layers::None;
};

// ---------------------------------------------------------------------------
// Contact event
// ---------------------------------------------------------------------------

struct ContactEvent
{
    BodyID bodyA = 0;
    BodyID bodyB = 0;
    float  impulse = 0.f;
    bool   isTrigger = false;
};

using ContactCallback = std::function<void(const ContactEvent&)>;
using TriggerCallback = std::function<void(BodyID trigger, BodyID other, bool entered)>;

// ---------------------------------------------------------------------------
// PhysicsLayerManager
// Keeps per-body layer assignments and provides query helpers.
// Works alongside the base PhysicsWorld.
// ---------------------------------------------------------------------------

class PhysicsLayerManager
{
public:
    bool Initialize() { return true; }
    void Shutdown()   { m_entries.clear(); }

    // ---- register body layer ------------------------------------------
    void RegisterBody(BodyID id,
                       CollisionLayer layer,
                       CollisionLayer collidesWith = Layers::All,
                       bool isTrigger = false);
    void UnregisterBody(BodyID id);

    CollisionLayer GetLayer        (BodyID id) const;
    CollisionLayer GetCollidesWith (BodyID id) const;
    bool           IsTrigger       (BodyID id) const;

    // ---- layer filter -------------------------------------------------
    bool ShouldCollide(BodyID a, BodyID b) const;

    // ---- ray-cast (world-space, using PhysicsWorld body positions) ----
    RayCastHit Raycast(const PhysicsWorld& world, const RayCast& ray) const;

    // ---- sphere overlap -----------------------------------------------
    std::vector<BodyID> OverlapSphere(
        const PhysicsWorld& world,
        float cx, float cy, float cz,
        float radius,
        CollisionLayer layers = Layers::All) const;

    // ---- contact callbacks -------------------------------------------
    void SetContactCallback(ContactCallback cb) { m_contactCb = std::move(cb); }
    void SetTriggerCallback(TriggerCallback  cb) { m_triggerCb = std::move(cb); }

    /// Call each simulation step after PhysicsWorld::Step().
    void ProcessContacts(const PhysicsWorld& world);

private:
    std::vector<BodyLayerEntry> m_entries;
    ContactCallback             m_contactCb;
    TriggerCallback             m_triggerCb;

    const BodyLayerEntry* Find(BodyID id) const;
    BodyLayerEntry*       FindMutable(BodyID id);
};

} // namespace atlas::physics
