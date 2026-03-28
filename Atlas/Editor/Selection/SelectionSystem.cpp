#include "Selection/SelectionSystem.h"
#include <iostream>

bool SelectionSystem::Initialize()
{
    std::cout << "[Selection] Initialize\n";
    return true;
}

void SelectionSystem::RegisterSelectable(const SelectableObject& Object)
{
    Objects.push_back(Object);
    std::cout << "[Selection] Registered " << Object.Label << "\n";
}

SelectionHandle SelectionSystem::SelectFirst()
{
    if (!Objects.empty())
    {
        CurrentSelection.Type = Objects[0].Type;
        CurrentSelection.Id = Objects[0].Id;
        std::cout << "[Selection] Selected " << CurrentSelection.Id << "\n";
    }
    return CurrentSelection;
}

void SelectionSystem::ClearSelection()
{
    CurrentSelection = {};
}

const SelectionHandle& SelectionSystem::GetCurrentSelection() const
{
    return CurrentSelection;
}

const std::vector<SelectableObject>& SelectionSystem::GetRegisteredObjects() const
{
    return Objects;
}
