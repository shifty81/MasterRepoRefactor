// PhysicsExtensions.cpp
// Atlas Engine — collision layer manager, ray-cast, sphere overlap, contacts.

#include "Physics/PhysicsExtensions.h"

#include <algorithm>
#include <cmath>

namespace atlas::physics {

void PhysicsLayerManager::RegisterBody(BodyID id,
                                         CollisionLayer layer,
                                         CollisionLayer collidesWith,
                                         bool isTrigger)
{
    for (auto& e : m_entries)
    {
        if (e.id == id) { e.layer = layer; e.collidesWith = collidesWith;
                          e.isTrigger = isTrigger; return; }
    }
    m_entries.push_back({ id, layer, collidesWith, isTrigger });
}

void PhysicsLayerManager::UnregisterBody(BodyID id)
{
    m_entries.erase(
        std::remove_if(m_entries.begin(), m_entries.end(),
                       [id](const BodyLayerEntry& e){ return e.id == id; }),
        m_entries.end());
}

CollisionLayer PhysicsLayerManager::GetLayer(BodyID id) const
{
    const BodyLayerEntry* e = Find(id);
    return e ? e->layer : Layers::DynamicEntity;
}

CollisionLayer PhysicsLayerManager::GetCollidesWith(BodyID id) const
{
    const BodyLayerEntry* e = Find(id);
    return e ? e->collidesWith : Layers::All;
}

bool PhysicsLayerManager::IsTrigger(BodyID id) const
{
    const BodyLayerEntry* e = Find(id);
    return e ? e->isTrigger : false;
}

bool PhysicsLayerManager::ShouldCollide(BodyID a, BodyID b) const
{
    CollisionLayer layA = GetLayer(a);
    CollisionLayer cwA  = GetCollidesWith(a);
    CollisionLayer layB = GetLayer(b);
    CollisionLayer cwB  = GetCollidesWith(b);
    return (layA & cwB) && (layB & cwA);
}

RayCastHit PhysicsLayerManager::Raycast(const PhysicsWorld& world,
                                           const RayCast& ray) const
{
    RayCastHit best;
    best.distance = ray.maxDistance;

    size_t count = world.BodyCount();
    // We iterate body IDs via the collision-layer entries since we don't have
    // direct iteration on the base world — use registered entries.
    for (const auto& entry : m_entries)
    {
        if (!(entry.layer & ray.queryLayers)) continue;

        const RigidBody* rb = world.GetBody(entry.id);
        if (!rb || !rb->active) continue;

        // Sphere approximation radius 0.5.
        constexpr float r = 0.5f;
        float dx = rb->position.x - ray.originX;
        float dy = rb->position.y - ray.originY;
        float dz = rb->position.z - ray.originZ;

        float dot = dx * ray.dirX + dy * ray.dirY + dz * ray.dirZ;
        if (dot < 0.f) continue;

        float d2 = dx*dx + dy*dy + dz*dz - dot*dot;
        if (d2 > r * r) continue;

        float disc = r * r - d2;
        float dist = dot - std::sqrt(disc > 0.f ? disc : 0.f);
        if (dist < 0.f || dist > best.distance) continue;

        best.hasHit   = true;
        best.bodyId   = entry.id;
        best.distance = dist;
        best.hitX     = ray.originX + ray.dirX * dist;
        best.hitY     = ray.originY + ray.dirY * dist;
        best.hitZ     = ray.originZ + ray.dirZ * dist;
        best.hitLayer = entry.layer;

        float nx = best.hitX - rb->position.x;
        float ny = best.hitY - rb->position.y;
        float nz = best.hitZ - rb->position.z;
        float len = std::sqrt(nx*nx + ny*ny + nz*nz);
        if (len > 0.f) { nx /= len; ny /= len; nz /= len; }
        best.normalX = nx; best.normalY = ny; best.normalZ = nz;
    }

    return best;
}

std::vector<BodyID> PhysicsLayerManager::OverlapSphere(
    const PhysicsWorld& world,
    float cx, float cy, float cz,
    float radius,
    CollisionLayer layers) const
{
    std::vector<BodyID> result;
    for (const auto& entry : m_entries)
    {
        if (!(entry.layer & layers)) continue;
        const RigidBody* rb = world.GetBody(entry.id);
        if (!rb || !rb->active) continue;

        float dx = rb->position.x - cx;
        float dy = rb->position.y - cy;
        float dz = rb->position.z - cz;
        float d2 = dx*dx + dy*dy + dz*dz;
        float rSum = radius + 0.5f; // approximate body radius
        if (d2 <= rSum * rSum)
            result.push_back(entry.id);
    }
    return result;
}

void PhysicsLayerManager::ProcessContacts(const PhysicsWorld& world)
{
    const auto& pairs = world.GetCollisions();
    for (const auto& pair : pairs)
    {
        if (!ShouldCollide(pair.a, pair.b)) continue;

        bool trigger = IsTrigger(pair.a) || IsTrigger(pair.b);
        ContactEvent evt{ pair.a, pair.b, 0.f, trigger };

        if (trigger && m_triggerCb)
            m_triggerCb(trigger ? pair.a : 0, trigger ? pair.b : 0, true);
        else if (m_contactCb)
            m_contactCb(evt);
    }
}

const BodyLayerEntry* PhysicsLayerManager::Find(BodyID id) const
{
    for (const auto& e : m_entries)
        if (e.id == id) return &e;
    return nullptr;
}

BodyLayerEntry* PhysicsLayerManager::FindMutable(BodyID id)
{
    for (auto& e : m_entries)
        if (e.id == id) return &e;
    return nullptr;
}

} // namespace atlas::physics
