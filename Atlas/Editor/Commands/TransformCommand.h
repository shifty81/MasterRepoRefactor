// TransformCommand.h
// Atlas Editor — undoable transform (move / rotate / scale) command.

#pragma once
#include "Commands/CommandTypes.h"
#include "Selection/SelectionTypes.h"

#include <array>
#include <string>

namespace atlas::editor {

/// Simple 3-component vector used for editor-side transforms.
struct EditorVec3 { float x = 0.f, y = 0.f, z = 0.f; };

/// Snapshot of one axis-aligned transform.
struct TransformSnapshot
{
    EditorVec3 position;
    EditorVec3 rotationEulerDeg;
    EditorVec3 scale { 1.f, 1.f, 1.f };
};

/// Applies a transform delta to a selected entity and records before/after
/// snapshots so the operation can be cleanly undone.
class TransformCommand : public ICommand
{
public:
    TransformCommand(SelectionHandle target,
                     TransformSnapshot before,
                     TransformSnapshot after);

    void        Execute()          override;
    void        Undo()             override;
    std::string GetDescription()   const override;

private:
    SelectionHandle   m_target;
    TransformSnapshot m_before;
    TransformSnapshot m_after;
};

} // namespace atlas::editor
