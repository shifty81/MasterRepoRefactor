// CommandStack.h
// Atlas Editor — typed command stack built on top of UndoStack.

#pragma once
#include "Commands/CommandTypes.h"
#include "Framework/UndoStack.h"

#include <memory>
#include <string>

namespace atlas::editor {

/// Bridges ICommand-derived objects into the existing UndoStack.
class CommandStack
{
public:
    explicit CommandStack(size_t maxDepth = 64) : m_stack(maxDepth) {}

    /// Execute a command and push it onto the undo history.
    void Submit(std::unique_ptr<ICommand> cmd);

    bool Undo();
    bool Redo();
    void Clear();

    bool        CanUndo()          const { return m_stack.CanUndo(); }
    bool        CanRedo()          const { return m_stack.CanRedo(); }
    std::string UndoDescription()  const { return m_stack.UndoDescription(); }
    std::string RedoDescription()  const { return m_stack.RedoDescription(); }
    size_t      UndoCount()        const { return m_stack.UndoCount(); }
    size_t      RedoCount()        const { return m_stack.RedoCount(); }

private:
    UndoStack m_stack;
};

} // namespace atlas::editor
