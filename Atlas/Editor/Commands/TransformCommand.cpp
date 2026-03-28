// TransformCommand.cpp
// Atlas Editor — undoable transform command.

#include "Commands/TransformCommand.h"

namespace atlas::editor {

TransformCommand::TransformCommand(SelectionHandle target,
                                   TransformSnapshot before,
                                   TransformSnapshot after)
    : m_target(std::move(target))
    , m_before(before)
    , m_after(after)
{}

void TransformCommand::Execute()
{
    // In a full engine integration this would call into a scene/ECS layer.
    // Stub: apply m_after transform to m_target.
    (void)m_after;
}

void TransformCommand::Undo()
{
    // Stub: restore m_before transform to m_target.
    (void)m_before;
}

std::string TransformCommand::GetDescription() const
{
    return "Transform: " + m_target.Id;
}

} // namespace atlas::editor
