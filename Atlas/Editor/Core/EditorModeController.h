#pragma once

#include "Core/EditorTypes.h"

class EditorModeController
{
public:
    bool Initialize();
    void ToggleMode();
    void SetToolMode(EEditorToolMode InToolMode);
    void SetGridSnapEnabled(bool bEnabled);
    void SetLocalTransformMode(bool bEnabled);

    const EditorSessionState& GetState() const;

private:
    EditorSessionState State;
};
