// VoxelChunkEditor.cpp
// Atlas Editor — stateful voxel chunk editing with dirty tracking.

#include "Voxel/VoxelChunkEditor.h"

#include <algorithm>
#include <cstring>

namespace atlas::editor::voxel {

// ----------------------------------------------------------------------------
static const VoxelCell kAirCell {};

VoxelChunkEditor::VoxelChunkEditor(std::string chunkId)
    : m_chunkId(std::move(chunkId))
{
    m_cells.fill(kAirCell);
}

bool VoxelChunkEditor::InBounds(VoxelPos p) const
{
    return p.x >= 0 && p.x < kChunkSize &&
           p.y >= 0 && p.y < kChunkSize &&
           p.z >= 0 && p.z < kChunkSize;
}

const VoxelCell& VoxelChunkEditor::GetCell(VoxelPos p) const
{
    if (!InBounds(p)) return kAirCell;
    return m_cells[static_cast<size_t>(Index(p))];
}

bool VoxelChunkEditor::SetCell(VoxelPos p, VoxelCell cell)
{
    if (!InBounds(p)) return false;
    auto& existing = m_cells[static_cast<size_t>(Index(p))];
    if (existing.material == cell.material && existing.shape == cell.shape)
        return false;
    existing = cell;
    ExpandDirty(p);
    return true;
}

bool VoxelChunkEditor::ClearCell(VoxelPos p)
{
    return SetCell(p, kAirCell);
}

// ---- brush -----------------------------------------------------------------

ChunkEditResult VoxelChunkEditor::ApplyBrush(VoxelPos centre,
                                              const BrushSettings& brush)
{
    ChunkEditResult result;
    int32_t r = brush.radius;

    for (int32_t dz = -r; dz <= r; ++dz)
    for (int32_t dy = -r; dy <= r; ++dy)
    for (int32_t dx = -r; dx <= r; ++dx)
    {
        // Shape filter
        if (brush.shape == EBrushShape::Sphere)
        {
            if (dx*dx + dy*dy + dz*dz > r*r) continue;
        }
        // Cylinder: circle in XZ, full height Y
        if (brush.shape == EBrushShape::Cylinder)
        {
            if (dx*dx + dz*dz > r*r) continue;
        }

        VoxelPos p { centre.x + dx, centre.y + dy, centre.z + dz };
        if (!InBounds(p)) continue;

        bool changed = false;
        switch (brush.op)
        {
            case EBrushOp::Add:
                changed = SetCell(p, { brush.material, 0 });
                break;
            case EBrushOp::Remove:
                changed = ClearCell(p);
                break;
            case EBrushOp::Paint:
            {
                VoxelCell c = GetCell(p);
                if (c.material != 0)   // only paint existing solid cells
                {
                    c.material = brush.material;
                    changed = SetCell(p, c);
                }
                break;
            }
        }
        if (changed) { ++result.cellsModified; result.anyModified = true; }
    }

    if (result.anyModified)
    {
        result.needsMeshRebuild = true;
        result.dirtyRegion = m_dirtyRegion;
    }
    return result;
}

// ---- dirty tracking --------------------------------------------------------

void VoxelChunkEditor::ExpandDirty(VoxelPos p)
{
    m_dirty = true;
    m_dirtyRegion.minCorner.x = std::min(m_dirtyRegion.minCorner.x, p.x);
    m_dirtyRegion.minCorner.y = std::min(m_dirtyRegion.minCorner.y, p.y);
    m_dirtyRegion.minCorner.z = std::min(m_dirtyRegion.minCorner.z, p.z);
    m_dirtyRegion.maxCorner.x = std::max(m_dirtyRegion.maxCorner.x, p.x);
    m_dirtyRegion.maxCorner.y = std::max(m_dirtyRegion.maxCorner.y, p.y);
    m_dirtyRegion.maxCorner.z = std::max(m_dirtyRegion.maxCorner.z, p.z);
}

void VoxelChunkEditor::ClearDirty()
{
    m_dirty = false;
    m_dirtyRegion = { {kChunkSize, kChunkSize, kChunkSize}, {-1, -1, -1} };
}

void VoxelChunkEditor::TriggerMeshRebuild()
{
    if (m_rebuildCb) m_rebuildCb(m_chunkId);
    ClearDirty();
}

// ---- serialisation ---------------------------------------------------------

std::vector<uint8_t> VoxelChunkEditor::Serialise() const
{
    // Format: [kTotal * kBytesPerCell bytes]  each cell: {material, shape}
    std::vector<uint8_t> buf;
    buf.reserve(static_cast<size_t>(kTotal) * kBytesPerCell);
    for (const auto& c : m_cells)
    {
        buf.push_back(c.material);
        buf.push_back(c.shape);
    }
    return buf;
}

bool VoxelChunkEditor::Deserialise(const std::vector<uint8_t>& data)
{
    if (data.size() != static_cast<size_t>(kTotal) * kBytesPerCell) return false;
    for (int32_t i = 0; i < kTotal; ++i)
    {
        m_cells[static_cast<size_t>(i)].material = data[static_cast<size_t>(i) * 2];
        m_cells[static_cast<size_t>(i)].shape    = data[static_cast<size_t>(i) * 2 + 1];
    }
    m_dirty = false;
    return true;
}

} // namespace atlas::editor::voxel
