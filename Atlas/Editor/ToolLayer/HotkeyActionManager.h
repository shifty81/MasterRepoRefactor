#pragma once
#include "ITool.h"
#include <string>
#include <unordered_map>

namespace Atlas::Editor {

/// P3 Tool — Assign and manage custom hotkey bindings for editor actions.
class HotkeyActionManager : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "HotkeyActionManager"; }
    bool IsActive() const override { return m_active; }

    void BindKey(const std::string& actionName, int keyCode);
    void UnbindKey(const std::string& actionName);
    bool IsActionTriggered(const std::string& actionName) const;
    int GetBoundKey(const std::string& actionName) const;
    void ResetToDefaults();
    int GetBindingCount() const { return static_cast<int>(m_bindings.size()); }

private:
    bool m_active{false};
    std::unordered_map<std::string, int> m_bindings;
};

} // namespace Atlas::Editor
