#include "Gizmos/GizmoSystem.h"
#include <iostream>

bool GizmoSystem::Initialize()
{
    std::cout << "[Gizmo] Initialize\n";
    return true;
}

void GizmoSystem::UpdateFromSelection(const SelectionSystem& Selection)
{
    State.bVisible = Selection.GetCurrentSelection().IsValid();
    std::cout << "[Gizmo] Visible=" << (State.bVisible ? "true" : "false") << "\n";
}

void GizmoSystem::SetToolMode(EEditorToolMode Mode)
{
    State.Mode = Mode;
}

void GizmoSystem::SetLocalMode(bool bEnabled)
{
    State.bLocalMode = bEnabled;
}

void GizmoSystem::SetSnapEnabled(bool bEnabled)
{
    State.bSnapEnabled = bEnabled;
}

const GizmoState& GizmoSystem::GetState() const
{
    return State;
}
