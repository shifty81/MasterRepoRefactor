// CommandTypes.h
// Atlas Editor — shared types for the editor command system (undo/redo).

#pragma once
#include <functional>
#include <string>

namespace atlas::editor {

/// Base interface for any reversible editor action.
struct ICommand
{
    virtual ~ICommand() = default;

    /// Execute or re-execute the command.
    virtual void Execute() = 0;

    /// Revert the effect of Execute().
    virtual void Undo() = 0;

    /// Human-readable description shown in the Undo/Redo menu.
    virtual std::string GetDescription() const = 0;
};

} // namespace atlas::editor
