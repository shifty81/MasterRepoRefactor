#pragma once

#include "Outliner/OutlinerTypes.h"
#include "Selection/SelectionSystem.h"

class SceneOutliner
{
public:
    bool Initialize();
    void RebuildFromSelectionSystem(const SelectionSystem& Selection);
    const SceneOutlinerState& GetState() const;

private:
    SceneOutlinerState State;
};
