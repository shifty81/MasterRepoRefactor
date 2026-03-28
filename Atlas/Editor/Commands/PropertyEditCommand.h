// PropertyEditCommand.h
// Atlas Editor — undoable property-edit command (scalar, string, enum fields).

#pragma once
#include "Commands/CommandTypes.h"
#include "Selection/SelectionTypes.h"

#include <string>

namespace atlas::editor {

/// Stores the before/after value of one named property as a string.
/// Concrete deserialisation is handled by higher-level property binding code.
class PropertyEditCommand : public ICommand
{
public:
    PropertyEditCommand(SelectionHandle  target,
                        std::string      propertyPath,
                        std::string      oldValue,
                        std::string      newValue);

    void        Execute()        override;
    void        Undo()           override;
    std::string GetDescription() const override;

private:
    void ApplyValue(const std::string& value);

    SelectionHandle m_target;
    std::string     m_propertyPath;
    std::string     m_oldValue;
    std::string     m_newValue;
};

} // namespace atlas::editor
