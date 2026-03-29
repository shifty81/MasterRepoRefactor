#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P2 Tool — Edit ship module slots: add, remove, swap modules.
class ShipModuleEditorTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ShipModuleEditorTool"; }
    bool IsActive() const override { return m_active; }

    void SelectShip(const std::string& shipEntityId);
    void FitModule(const std::string& slotId, const std::string& moduleTypeId);
    void UnfitModule(const std::string& slotId);
    void SwapModules(const std::string& slotA, const std::string& slotB);
    void ValidateFit();

    const std::string& GetSelectedShip() const { return m_selectedShip; }
    bool IsFitValid() const { return m_fitValid; }

private:
    bool m_active{false};
    std::string m_selectedShip;
    bool m_fitValid{true};
    std::vector<std::string> m_fittedSlots;
};

} // namespace Atlas::Editor
