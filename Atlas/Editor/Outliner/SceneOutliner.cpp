#include "Outliner/SceneOutliner.h"
#include <iostream>

bool SceneOutliner::Initialize()
{
    std::cout << "[Outliner] Initialize\n";
    return true;
}

void SceneOutliner::RebuildFromSelectionSystem(const SelectionSystem& Selection)
{
    State.Nodes.clear();

    for (const auto& Obj : Selection.GetRegisteredObjects())
    {
        std::string Type;
        switch (Obj.Type)
        {
            case ESelectionTargetType::Entity: Type = "Entity"; break;
            case ESelectionTargetType::Structure: Type = "Structure"; break;
            case ESelectionTargetType::Module: Type = "Module"; break;
            case ESelectionTargetType::VoxelChunk: Type = "VoxelChunk"; break;
            default: Type = "Unknown"; break;
        }

        State.Nodes.push_back({Obj.Id, Obj.Label, "", Type});
    }

    std::cout << "[Outliner] Nodes=" << State.Nodes.size() << "\n";
}

const SceneOutlinerState& SceneOutliner::GetState() const
{
    return State;
}
