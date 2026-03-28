#pragma once

#include "Inspector/InspectorTypes.h"
#include "Selection/SelectionSystem.h"

class PropertyInspector
{
public:
    bool Initialize();
    void InspectSelection(const SelectionSystem& Selection);
    const InspectorState& GetState() const;

private:
    InspectorState State;
};
