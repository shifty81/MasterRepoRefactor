#pragma once

#include "Gizmos/GizmoTypes.h"
#include "Selection/SelectionSystem.h"

class GizmoSystem
{
public:
    bool Initialize();
    void UpdateFromSelection(const SelectionSystem& Selection);
    void SetToolMode(EEditorToolMode Mode);
    void SetLocalMode(bool bEnabled);
    void SetSnapEnabled(bool bEnabled);

    const GizmoState& GetState() const;

private:
    GizmoState State;
};
