// VoxelEditCommand.cpp
// Atlas Editor — undoable voxel edit command.

#include "Commands/VoxelEditCommand.h"

namespace atlas::editor {

VoxelEditCommand::VoxelEditCommand(std::string                  chunkId,
                                   EVoxelEditOp                 op,
                                   std::vector<VoxelEditRecord> records)
    : m_chunkId(std::move(chunkId))
    , m_op(op)
    , m_records(std::move(records))
{}

void VoxelEditCommand::Execute()
{
    // Stub: apply newMaterial for each record to the voxel chunk m_chunkId.
    for (const auto& r : m_records) { (void)r; }
}

void VoxelEditCommand::Undo()
{
    // Stub: restore oldMaterial for each record.
    for (const auto& r : m_records) { (void)r; }
}

std::string VoxelEditCommand::GetDescription() const
{
    switch (m_op)
    {
        case EVoxelEditOp::Add:    return "Voxel Add ("   + m_chunkId + ")";
        case EVoxelEditOp::Remove: return "Voxel Remove (" + m_chunkId + ")";
        case EVoxelEditOp::Paint:  return "Voxel Paint ("  + m_chunkId + ")";
        default:                   return "Voxel Edit ("   + m_chunkId + ")";
    }
}

} // namespace atlas::editor
