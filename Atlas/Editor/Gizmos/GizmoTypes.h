#pragma once

#include "Core/EditorTypes.h"

struct GizmoState
{
    bool bVisible = false;
    EEditorToolMode Mode = EEditorToolMode::None;
    bool bLocalMode = false;
    bool bSnapEnabled = true;
};
