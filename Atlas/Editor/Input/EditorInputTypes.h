#pragma once

struct EditorInputFrame
{
    bool ToggleEditorMode = false;
    bool SelectPressed = false;
    bool MoveToolPressed = false;
    bool RotateToolPressed = false;
    bool ScaleToolPressed = false;
    bool ToggleSnap = false;
    bool ToggleLocalWorld = false;
    bool CameraForward = false;
    bool CameraBackward = false;
    bool CameraLeft = false;
    bool CameraRight = false;
    bool CameraUp = false;
    bool CameraDown = false;
    float LookYawDelta = 0.0f;
    float LookPitchDelta = 0.0f;
};
