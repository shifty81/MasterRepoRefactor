#include "Core/EditorModeController.h"
#include <iostream>

bool EditorModeController::Initialize()
{
    std::cout << "[EditorMode] Initialize Mode=Game Tool=Select\n";
    return true;
}

void EditorModeController::ToggleMode()
{
    State.Mode = (State.Mode == EEditorMode::Game) ? EEditorMode::Editor : EEditorMode::Game;
    std::cout << "[EditorMode] Toggled -> "
              << (State.Mode == EEditorMode::Editor ? "Editor" : "Game") << "\n";
}

void EditorModeController::SetToolMode(EEditorToolMode InToolMode)
{
    State.ToolMode = InToolMode;
    std::cout << "[EditorMode] Tool changed\n";
}

void EditorModeController::SetGridSnapEnabled(bool bEnabled)
{
    State.bGridSnapEnabled = bEnabled;
}

void EditorModeController::SetLocalTransformMode(bool bEnabled)
{
    State.bLocalTransformMode = bEnabled;
}

const EditorSessionState& EditorModeController::GetState() const
{
    return State;
}
