#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P15 Tool — Input action mapping, binding, and context management.
class InputActionMapTool : public ITool {
public:
    enum class InputDevice { Keyboard, Mouse, Gamepad, Touch, VR, Custom };
    enum class TriggerType { Pressed, Released, Held, Tapped, DoubleTapped, Chorded };
    enum class ActionCategory { Movement, Combat, UI, Debug, System, Custom };

    struct InputBinding {
        std::string bindingId;
        InputDevice device{InputDevice::Keyboard};
        int keyCode{0};
        TriggerType triggerType{TriggerType::Pressed};
        float deadzone{0.1f};
    };

    struct InputAction {
        std::string actionId;
        std::string name;
        ActionCategory category{ActionCategory::System};
        std::vector<std::string> bindings;
        bool consumeInput{true};
    };

    struct InputContext {
        std::string contextId;
        std::string name;
        std::vector<std::string> actions;
        int priority{0};
        bool exclusive{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "InputActionMapTool"; }
    bool IsActive() const override { return m_active; }

    // Action management
    std::string CreateAction(const std::string& name, ActionCategory category = ActionCategory::System);
    bool RemoveAction(const std::string& actionId);

    // Context management
    std::string CreateContext(const std::string& name, int priority = 0);
    bool RemoveContext(const std::string& contextId);
    bool AddActionToContext(const std::string& contextId, const std::string& actionId);

    // Binding management
    std::string AddBinding(const std::string& actionId, const InputBinding& binding);
    bool RemoveBinding(const std::string& actionId, const std::string& bindingId);

    // Context activation
    bool ActivateContext(const std::string& contextId);
    bool DeactivateContext(const std::string& contextId);

    // Queries
    const InputAction* GetAction(const std::string& actionId) const;
    const InputContext* GetContext(const std::string& contextId) const;
    std::vector<std::string> GetActiveContexts() const;
    std::vector<std::string> GetBindingsForAction(const std::string& actionId) const;

    // Import/Export and persistence
    bool ImportBindings(const std::string& filePath);
    bool ExportBindings(const std::string& filePath) const;
    bool SaveInputMap(const std::string& filePath) const;
    bool LoadInputMap(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, InputAction> m_actions;
    std::unordered_map<std::string, InputContext> m_contexts;
    std::unordered_map<std::string, InputBinding> m_bindings;
    std::vector<std::string> m_activeContextIds;
    int m_nextActionIndex{0};
    int m_nextContextIndex{0};
    int m_nextBindingIndex{0};
};

} // namespace Atlas::Editor
