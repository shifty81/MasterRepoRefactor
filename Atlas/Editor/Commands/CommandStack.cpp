// CommandStack.cpp
// Atlas Editor — typed command stack built on top of UndoStack.

#include "Commands/CommandStack.h"

namespace atlas::editor {

void CommandStack::Submit(std::unique_ptr<ICommand> cmd)
{
    // Capture a shared_ptr so the lambda keeps the command alive.
    auto shared = std::shared_ptr<ICommand>(std::move(cmd));

    // Execute immediately.
    shared->Execute();

    // Record undo / redo callbacks.
    UndoAction action;
    action.description = shared->GetDescription();
    action.undo = [shared]() { shared->Undo(); };
    action.redo = [shared]() { shared->Execute(); };

    m_stack.PushAction(std::move(action));
}

bool CommandStack::Undo()  { return m_stack.Undo(); }
bool CommandStack::Redo()  { return m_stack.Redo(); }
void CommandStack::Clear() { m_stack.Clear(); }

} // namespace atlas::editor
