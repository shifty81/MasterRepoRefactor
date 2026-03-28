// PropertyEditCommand.cpp
// Atlas Editor — undoable property-edit command.

#include "Commands/PropertyEditCommand.h"

namespace atlas::editor {

PropertyEditCommand::PropertyEditCommand(SelectionHandle  target,
                                         std::string      propertyPath,
                                         std::string      oldValue,
                                         std::string      newValue)
    : m_target(std::move(target))
    , m_propertyPath(std::move(propertyPath))
    , m_oldValue(std::move(oldValue))
    , m_newValue(std::move(newValue))
{}

void PropertyEditCommand::Execute()
{
    ApplyValue(m_newValue);
}

void PropertyEditCommand::Undo()
{
    ApplyValue(m_oldValue);
}

void PropertyEditCommand::ApplyValue(const std::string& value)
{
    // Stub: in a full integration, dispatch the new value to the property
    // binding layer using m_target and m_propertyPath.
    (void)value;
}

std::string PropertyEditCommand::GetDescription() const
{
    return "Edit property '" + m_propertyPath + "' on " + m_target.Id;
}

} // namespace atlas::editor
