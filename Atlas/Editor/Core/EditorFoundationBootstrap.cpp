#include "Core/EditorModeController.h"
#include "Input/EditorInputRouter.h"
#include "Camera/EditorCameraController.h"
#include "Selection/SelectionSystem.h"
#include "Outliner/SceneOutliner.h"
#include "Inspector/PropertyInspector.h"
#include "Gizmos/GizmoSystem.h"
#include <iostream>
#include <vector>
#include <string>

int main()
{
    EditorModeController Mode;
    EditorInputRouter Input;
    EditorCameraController Camera;
    SelectionSystem Selection;
    SceneOutliner Outliner;
    PropertyInspector Inspector;
    GizmoSystem Gizmo;

    Mode.Initialize();
    Input.Initialize();
    Camera.Initialize();
    Selection.Initialize();
    Outliner.Initialize();
    Inspector.Initialize();
    Gizmo.Initialize();

    Selection.RegisterSelectable({ESelectionTargetType::Structure, "ship_dev_001", "Dev Ship", {0,0,0}});
    Selection.RegisterSelectable({ESelectionTargetType::Module, "mod_0001", "Reactor MK1", {10,0,0}});

    Mode.ToggleMode();

    auto Frame = Input.BuildFrame({"W", "D", "LMB"}, 5.0f, -2.0f);
    Camera.Tick(Frame, 1.0f / 60.0f);

    Selection.SelectFirst();
    Outliner.RebuildFromSelectionSystem(Selection);
    Inspector.InspectSelection(Selection);

    Gizmo.SetToolMode(EEditorToolMode::Move);
    Gizmo.SetLocalMode(false);
    Gizmo.SetSnapEnabled(true);
    Gizmo.UpdateFromSelection(Selection);

    std::cout << "[EditorBootstrap] Complete\n";
    return 0;
}
