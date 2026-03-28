#include "Camera/EditorCameraController.h"
#include <iostream>

bool EditorCameraController::Initialize()
{
    std::cout << "[EditorCamera] Initialize\n";
    return true;
}

void EditorCameraController::SetMode(EEditorCameraMode InMode)
{
    State.Mode = InMode;
}

void EditorCameraController::FocusTarget(const EditorVector3& InTarget)
{
    State.OrbitTarget = InTarget;
    std::cout << "[EditorCamera] Focus target set\n";
}

void EditorCameraController::Tick(const EditorInputFrame& Frame, float DeltaTime)
{
    if (State.Mode == EEditorCameraMode::Free)
    {
        if (Frame.CameraForward) State.Position.X += MoveSpeed * DeltaTime;
        if (Frame.CameraBackward) State.Position.X -= MoveSpeed * DeltaTime;
        if (Frame.CameraRight) State.Position.Y += MoveSpeed * DeltaTime;
        if (Frame.CameraLeft) State.Position.Y -= MoveSpeed * DeltaTime;
        if (Frame.CameraUp) State.Position.Z += MoveSpeed * DeltaTime;
        if (Frame.CameraDown) State.Position.Z -= MoveSpeed * DeltaTime;
    }

    State.Yaw += Frame.LookYawDelta;
    State.Pitch += Frame.LookPitchDelta;

    std::cout << "[EditorCamera] Pos=("
              << State.Position.X << ", "
              << State.Position.Y << ", "
              << State.Position.Z << ") Yaw=" << State.Yaw
              << " Pitch=" << State.Pitch << "\n";
}

const EditorCameraState& EditorCameraController::GetState() const
{
    return State;
}
