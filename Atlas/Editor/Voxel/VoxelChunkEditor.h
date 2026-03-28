// VoxelChunkEditor.h
// Atlas Editor — stateful voxel chunk editing with dirty tracking and undo hooks.

#pragma once
#include "Voxel/VoxelTypes.h"

#include <array>
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::editor::voxel {

/// In-editor representation of one voxel chunk (kChunkSize^3 cells).
class VoxelChunkEditor
{
public:
    explicit VoxelChunkEditor(std::string chunkId);

    // ---- access -------------------------------------------------------
    const std::string& GetChunkId() const { return m_chunkId; }
    const VoxelCell&   GetCell(VoxelPos p) const;
    bool               InBounds(VoxelPos p) const;

    // ---- editing -------------------------------------------------------

    /// Place a single cell; returns true if the cell changed.
    bool SetCell(VoxelPos p, VoxelCell cell);

    /// Remove (air) a single cell; returns true if the cell changed.
    bool ClearCell(VoxelPos p);

    /// Apply a brush stroke centred on `centre`.
    ChunkEditResult ApplyBrush(VoxelPos centre, const BrushSettings& brush);

    // ---- dirty tracking ------------------------------------------------
    bool           IsDirty()         const { return m_dirty; }
    DirtyRegion    GetDirtyRegion()   const { return m_dirtyRegion; }
    void           ClearDirty();

    // ---- mesh rebuild hook ---------------------------------------------
    using MeshRebuildCallback = std::function<void(const std::string& chunkId)>;
    void SetMeshRebuildCallback(MeshRebuildCallback cb) { m_rebuildCb = std::move(cb); }
    void TriggerMeshRebuild();

    // ---- serialisation -------------------------------------------------
    /// Serialise all non-air cells to a simple binary blob (for save/undo).
    std::vector<uint8_t> Serialise()   const;
    /// Restore chunk state from a previously serialised blob.
    bool                 Deserialise(const std::vector<uint8_t>& data);

private:
    static constexpr int32_t kTotal = kChunkSize * kChunkSize * kChunkSize;

    int32_t Index(VoxelPos p) const
    {
        return p.x + p.y * kChunkSize + p.z * kChunkSize * kChunkSize;
    }

    void ExpandDirty(VoxelPos p);

    std::string               m_chunkId;
    std::array<VoxelCell, kTotal> m_cells {};  // value-init → all air
    bool                      m_dirty        = false;
    DirtyRegion               m_dirtyRegion  { {kChunkSize, kChunkSize, kChunkSize},
                                               {-1, -1, -1} };
    MeshRebuildCallback       m_rebuildCb;
};

} // namespace atlas::editor::voxel
