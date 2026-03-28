#pragma once

#include "Selection/SelectionTypes.h"
#include "Camera/EditorCameraTypes.h"
#include <vector>
#include <string>

struct SelectableObject
{
    ESelectionTargetType Type = ESelectionTargetType::None;
    std::string Id;
    std::string Label;
    EditorVector3 Position;
};

class SelectionSystem
{
public:
    bool Initialize();
    void RegisterSelectable(const SelectableObject& Object);
    SelectionHandle SelectFirst();
    void ClearSelection();

    const SelectionHandle& GetCurrentSelection() const;
    const std::vector<SelectableObject>& GetRegisteredObjects() const;

private:
    std::vector<SelectableObject> Objects;
    SelectionHandle CurrentSelection;
};
