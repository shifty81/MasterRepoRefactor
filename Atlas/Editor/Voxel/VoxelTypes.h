// VoxelTypes.h
// Atlas Editor — shared voxel data types for chunk editing.

#pragma once
#include <cstdint>
#include <string>
#include <vector>

namespace atlas::editor::voxel {

/// 3-D integer coordinate within a chunk.
struct VoxelPos { int32_t x = 0, y = 0, z = 0; };

/// Default chunk side length in voxels (power of 2 for bit-mask ops).
constexpr int32_t kChunkSize = 16;

/// Bytes used per voxel cell in the serialised blob (material + shape).
constexpr size_t kBytesPerCell = 2;

/// One voxel cell — material index 0 means empty/air.
struct VoxelCell
{
    uint8_t material  = 0;  ///< 0 = air, 1–255 = solid material
    uint8_t shape     = 0;  ///< 0 = full cube, future: slope/wedge/etc.
};

/// A dirty-region marker so only modified cells are rebuilt.
struct DirtyRegion
{
    VoxelPos minCorner;
    VoxelPos maxCorner;
    bool isEmpty() const { return minCorner.x > maxCorner.x; }
};

enum class EBrushShape : uint8_t { Cube, Sphere, Cylinder };
enum class EBrushOp    : uint8_t { Add, Remove, Paint };

struct BrushSettings
{
    EBrushShape shape    = EBrushShape::Cube;
    EBrushOp    op       = EBrushOp::Add;
    int32_t     radius   = 1;   ///< half-extent or sphere radius in voxels
    uint8_t     material = 1;   ///< material index applied by Add/Paint
};

/// Per-chunk edit result returned after applying a brush stroke.
struct ChunkEditResult
{
    bool    anyModified = false;
    int32_t cellsModified = 0;
    bool    needsMeshRebuild = false;
    DirtyRegion dirtyRegion;
};

} // namespace atlas::editor::voxel
