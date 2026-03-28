// PlacementSystem.h
// Atlas Editor — placement system: grid/socket snap, preview ghost, validity feedback,
// and transform application to selected targets.

#pragma once
#include "Gizmos/GizmoTypes.h"

#include <functional>
#include <string>
#include <vector>

namespace atlas::editor::placement {

/// Result of snapping a position to the active grid.
struct GridSnapResult
{
    float snappedX = 0.f;
    float snappedY = 0.f;
    float snappedZ = 0.f;
    bool  didSnap  = false;
};

/// A named socket point on a module/structure.
struct SocketPoint
{
    std::string socketId;
    std::string ownerNodeId;
    float worldX = 0.f, worldY = 0.f, worldZ = 0.f;
    float normalX = 0.f, normalY = 1.f, normalZ = 0.f;
    std::string compatibleType;  ///< type tag — only matching types can snap
};

/// Live placement preview ghost state.
struct PlacementGhost
{
    std::string  sourceAssetId;
    float        previewX = 0.f, previewY = 0.f, previewZ = 0.f;
    float        previewRotY = 0.f;
    bool         isVisible   = false;
    bool         isValid     = true;       ///< false = red highlight
    std::string  invalidReason;
};

/// Validity check result for a proposed placement.
struct PlacementValidityResult
{
    bool        valid           = true;
    std::string reason;
    bool        overlapsExisting = false;
    bool        outOfBounds      = false;
    bool        incompatibleSocket = false;
};

/// Callback fired when a placement is confirmed (user commits the ghost).
using PlacementConfirmedCallback =
    std::function<void(const std::string& assetId,
                       float x, float y, float z, float rotY)>;

class PlacementSystem
{
public:
    bool Initialize();
    void Shutdown();

    // ---- grid snap ---------------------------------------------------
    void          SetGridSize(float size)  { m_gridSize = size; }
    float         GetGridSize()      const { return m_gridSize; }
    void          SetGridSnapEnabled(bool enabled) { m_gridSnapEnabled = enabled; }
    bool          IsGridSnapEnabled() const { return m_gridSnapEnabled; }
    GridSnapResult SnapToGrid(float x, float y, float z) const;

    // ---- socket snap -------------------------------------------------
    void         RegisterSocket(const SocketPoint& socket);
    void         UnregisterSocket(const std::string& socketId);
    void         ClearSockets();

    /// Find the nearest compatible socket within snapRadius.
    /// Returns true and fills outSocket if a snap target is found.
    bool FindNearestSocket(float x, float y, float z,
                            const std::string& compatibleType,
                            float snapRadius,
                            SocketPoint& outSocket) const;

    // ---- placement preview -------------------------------------------
    bool  BeginPlacement(const std::string& assetId);
    void  UpdatePlacementPosition(float x, float y, float z, float rotY = 0.f);
    void  EndPlacement();         ///< cancel without confirming
    bool  ConfirmPlacement();     ///< commit ghost position

    const PlacementGhost& GetGhost() const { return m_ghost; }

    // ---- validity feedback -------------------------------------------
    PlacementValidityResult CheckValidity(float x, float y, float z,
                                          const std::string& assetId) const;

    // ---- transform application ---------------------------------------
    /// Apply a delta move to the selected node.
    bool ApplyDeltaMove(const std::string& nodeId,
                         float dx, float dy, float dz);

    /// Apply absolute transform to a node.
    bool ApplyTransform(const std::string& nodeId,
                         float px, float py, float pz,
                         float rx, float ry, float rz,
                         float sx, float sy, float sz);

    // ---- toggle local/world space -----------------------------------
    void SetLocalSpace(bool local) { m_localSpace = local; }
    bool IsLocalSpace()      const { return m_localSpace; }

    void SetConfirmedCallback(PlacementConfirmedCallback cb)
    { m_confirmedCb = std::move(cb); }

private:
    float  m_gridSize        = 1.0f;
    bool   m_gridSnapEnabled = true;
    bool   m_localSpace      = false;

    std::vector<SocketPoint>  m_sockets;
    PlacementGhost            m_ghost;
    PlacementConfirmedCallback m_confirmedCb;
};

} // namespace atlas::editor::placement
