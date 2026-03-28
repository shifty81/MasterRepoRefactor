#pragma once

struct EditorVector3
{
    float X = 0.0f;
    float Y = 0.0f;
    float Z = 0.0f;
};

enum class EEditorCameraMode
{
    Free,
    Orbit
};

struct EditorCameraState
{
    EEditorCameraMode Mode = EEditorCameraMode::Free;
    EditorVector3 Position;
    EditorVector3 OrbitTarget;
    float Yaw = 0.0f;
    float Pitch = 0.0f;
    float Distance = 400.0f;
};
