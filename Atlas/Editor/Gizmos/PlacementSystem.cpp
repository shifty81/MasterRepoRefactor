// PlacementSystem.cpp
// Atlas Editor — placement system: grid/socket snap, preview ghost, validity.

#include "Gizmos/PlacementSystem.h"

#include <cmath>
#include <algorithm>

namespace atlas::editor::placement {

bool PlacementSystem::Initialize()
{
    m_ghost = {};
    m_sockets.clear();
    return true;
}

void PlacementSystem::Shutdown() { m_sockets.clear(); }

// ---- grid snap ---------------------------------------------------------------

static float RoundToGrid(float v, float g)
{
    return g > 0.f ? std::round(v / g) * g : v;
}

GridSnapResult PlacementSystem::SnapToGrid(float x, float y, float z) const
{
    if (!m_gridSnapEnabled)
        return { x, y, z, false };

    float sx = RoundToGrid(x, m_gridSize);
    float sy = RoundToGrid(y, m_gridSize);
    float sz = RoundToGrid(z, m_gridSize);
    bool  snapped = (sx != x || sy != y || sz != z);
    return { sx, sy, sz, snapped };
}

// ---- socket snap -------------------------------------------------------------

void PlacementSystem::RegisterSocket(const SocketPoint& socket)
{
    m_sockets.push_back(socket);
}

void PlacementSystem::UnregisterSocket(const std::string& socketId)
{
    m_sockets.erase(
        std::remove_if(m_sockets.begin(), m_sockets.end(),
                       [&](const SocketPoint& s){ return s.socketId == socketId; }),
        m_sockets.end());
}

void PlacementSystem::ClearSockets() { m_sockets.clear(); }

bool PlacementSystem::FindNearestSocket(float x, float y, float z,
                                         const std::string& compatibleType,
                                         float snapRadius,
                                         SocketPoint& outSocket) const
{
    float bestDist2 = snapRadius * snapRadius + 1.f;
    const SocketPoint* best = nullptr;

    for (const auto& s : m_sockets)
    {
        if (!compatibleType.empty() && s.compatibleType != compatibleType)
            continue;
        float dx = s.worldX - x;
        float dy = s.worldY - y;
        float dz = s.worldZ - z;
        float d2 = dx*dx + dy*dy + dz*dz;
        if (d2 < bestDist2) { bestDist2 = d2; best = &s; }
    }
    if (!best) return false;
    outSocket = *best;
    return true;
}

// ---- placement preview -------------------------------------------------------

bool PlacementSystem::BeginPlacement(const std::string& assetId)
{
    m_ghost = {};
    m_ghost.sourceAssetId = assetId;
    m_ghost.isVisible     = true;
    m_ghost.isValid       = true;
    return true;
}

void PlacementSystem::UpdatePlacementPosition(float x, float y, float z, float rotY)
{
    // Apply grid snap.
    auto snap = SnapToGrid(x, y, z);
    m_ghost.previewX    = snap.snappedX;
    m_ghost.previewY    = snap.snappedY;
    m_ghost.previewZ    = snap.snappedZ;
    m_ghost.previewRotY = rotY;

    // Live validity update.
    auto validity = CheckValidity(m_ghost.previewX, m_ghost.previewY,
                                   m_ghost.previewZ, m_ghost.sourceAssetId);
    m_ghost.isValid       = validity.valid;
    m_ghost.invalidReason = validity.reason;
}

void PlacementSystem::EndPlacement()
{
    m_ghost = {};
}

bool PlacementSystem::ConfirmPlacement()
{
    if (!m_ghost.isVisible || !m_ghost.isValid) return false;

    if (m_confirmedCb)
        m_confirmedCb(m_ghost.sourceAssetId,
                       m_ghost.previewX, m_ghost.previewY, m_ghost.previewZ,
                       m_ghost.previewRotY);
    m_ghost = {};
    return true;
}

// ---- validity ----------------------------------------------------------------

PlacementValidityResult
PlacementSystem::CheckValidity(float /*x*/, float /*y*/, float /*z*/,
                                const std::string& /*assetId*/) const
{
    // Stub: always valid. Real implementation would test bounding box overlap,
    // map bounds, and socket compatibility.
    return { true, "", false, false, false };
}

// ---- transform application ---------------------------------------------------

bool PlacementSystem::ApplyDeltaMove(const std::string& /*nodeId*/,
                                      float /*dx*/, float /*dy*/, float /*dz*/)
{
    // Stub: real implementation fetches node from SceneHierarchySystem and
    // adjusts its position by the delta.
    return true;
}

bool PlacementSystem::ApplyTransform(const std::string& /*nodeId*/,
                                      float /*px*/, float /*py*/, float /*pz*/,
                                      float /*rx*/, float /*ry*/, float /*rz*/,
                                      float /*sx*/, float /*sy*/, float /*sz*/)
{
    // Stub: real implementation delegates to SceneHierarchySystem::SetTransform.
    return true;
}

} // namespace atlas::editor::placement
