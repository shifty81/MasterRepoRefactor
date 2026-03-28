#pragma once

#include "Camera/EditorCameraTypes.h"
#include "Input/EditorInputTypes.h"

class EditorCameraController
{
public:
    bool Initialize();
    void SetMode(EEditorCameraMode InMode);
    void FocusTarget(const EditorVector3& InTarget);
    void Tick(const EditorInputFrame& Frame, float DeltaTime);

    const EditorCameraState& GetState() const;

private:
    EditorCameraState State;
    float MoveSpeed = 500.0f;
};
