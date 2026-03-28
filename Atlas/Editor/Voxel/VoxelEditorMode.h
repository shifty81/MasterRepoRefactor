// VoxelEditorMode.h
// Atlas Editor — voxel-editing mode controller (tool UI → chunk editor bridge).

#pragma once
#include "Voxel/VoxelTypes.h"
#include "Voxel/VoxelChunkEditor.h"

#include <memory>
#include <string>
#include <unordered_map>

namespace atlas::editor::voxel {

/// Manages all active chunk editors and routes brush strokes to them.
class VoxelEditorMode
{
public:
    bool Initialize();
    void Shutdown();

    // ---- chunk management ----------------------------------------------
    VoxelChunkEditor& GetOrCreateChunk(const std::string& chunkId);
    bool              ChunkExists(const std::string& chunkId) const;
    void              UnloadChunk(const std::string& chunkId);

    // ---- tool state ----------------------------------------------------
    void           SetBrush(const BrushSettings& brush) { m_brush = brush; }
    BrushSettings& GetBrush()                           { return m_brush; }

    /// Apply the current brush to the chunk at the given world position.
    ChunkEditResult Stroke(const std::string& chunkId, VoxelPos pos);

    // ---- persistence ---------------------------------------------------
    /// Serialise all dirty chunks and return a flat save blob.
    std::vector<uint8_t> SerialiseAll() const;

    /// Restore all chunks from a save blob produced by SerialiseAll().
    bool DeserialiseAll(const std::vector<uint8_t>& data);

    // ---- dirty-list ----------------------------------------------------
    std::vector<std::string> GetDirtyChunkIds() const;
    void                     RebuildDirtyMeshes();

private:
    std::unordered_map<std::string, std::unique_ptr<VoxelChunkEditor>> m_chunks;
    BrushSettings m_brush;
};

} // namespace atlas::editor::voxel
