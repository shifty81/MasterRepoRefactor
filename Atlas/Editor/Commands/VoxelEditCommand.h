// VoxelEditCommand.h
// Atlas Editor — undoable voxel add/remove/paint command.

#pragma once
#include "Commands/CommandTypes.h"

#include <cstdint>
#include <string>
#include <vector>

namespace atlas::editor {

enum class EVoxelEditOp : uint8_t
{
    Add,
    Remove,
    Paint
};

struct VoxelCoord
{
    int32_t x = 0, y = 0, z = 0;
};

struct VoxelEditRecord
{
    VoxelCoord  coord;
    uint8_t     oldMaterial = 0;
    uint8_t     newMaterial = 0;
};

/// Records a batch of voxel cell edits so they can be undone as a unit.
class VoxelEditCommand : public ICommand
{
public:
    VoxelEditCommand(std::string           chunkId,
                     EVoxelEditOp          op,
                     std::vector<VoxelEditRecord> records);

    void        Execute()        override;
    void        Undo()           override;
    std::string GetDescription() const override;

private:
    std::string                  m_chunkId;
    EVoxelEditOp                 m_op;
    std::vector<VoxelEditRecord> m_records;
};

} // namespace atlas::editor
