#include "Inspector/PropertyInspector.h"
#include <iostream>

bool PropertyInspector::Initialize()
{
    std::cout << "[Inspector] Initialize\n";
    return true;
}

void PropertyInspector::InspectSelection(const SelectionSystem& Selection)
{
    State = {};
    const auto& Handle = Selection.GetCurrentSelection();
    if (!Handle.IsValid())
    {
        return;
    }

    State.SelectedId = Handle.Id;
    switch (Handle.Type)
    {
        case ESelectionTargetType::Entity: State.SelectedType = "Entity"; break;
        case ESelectionTargetType::Structure: State.SelectedType = "Structure"; break;
        case ESelectionTargetType::Module: State.SelectedType = "Module"; break;
        case ESelectionTargetType::VoxelChunk: State.SelectedType = "VoxelChunk"; break;
        default: State.SelectedType = "Unknown"; break;
    }

    State.Fields.push_back({"Id", State.SelectedId});
    State.Fields.push_back({"Type", State.SelectedType});
    State.Fields.push_back({"Transform", "Pending transform bridge"});
    State.Fields.push_back({"Components", "Pending component summary"});

    std::cout << "[Inspector] Inspecting " << State.SelectedId << "\n";
}

const InspectorState& PropertyInspector::GetState() const
{
    return State;
}
