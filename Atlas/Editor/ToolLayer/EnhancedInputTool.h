#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P18 Tool — Enhanced Input action mapping, input context configuration, and modifier/trigger management.
class EnhancedInputTool : public ITool {
public:
    enum class InputTriggerType { Pressed, Released, Hold, HoldAndRelease, Tap, ChordAction, Pulse };
    enum class InputModifierType { DeadZone, FOVScaling, Negate, Scale, Smooth, SwizzleAxis, Normalize };
    enum class InputActionValueType { Boolean, Axis1D, Axis2D, Axis3D };

    struct InputModifierDef {
        std::string modifierId;
        std::string name;
        InputModifierType modifierType{InputModifierType::DeadZone};
        std::vector<std::string> parameters;
    };

    struct InputTriggerDef {
        std::string triggerId;
        std::string name;
        InputTriggerType triggerType{InputTriggerType::Pressed};
        float threshold{0.5f};
        float holdTime{0.5f};
        float pauseTime{0.0f};
    };

    struct InputActionDef {
        std::string actionId;
        std::string name;
        InputActionValueType valueType{InputActionValueType::Boolean};
        std::vector<std::string> modifiers;
        std::vector<std::string> triggers;
        bool consume{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "EnhancedInputTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateAction(const std::string& name, InputActionValueType valueType);
    bool RemoveAction(const std::string& actionId);
    std::string AddModifier(const std::string& actionId, InputModifierType type);
    bool RemoveModifier(const std::string& modifierId);
    std::string AddTrigger(const std::string& actionId, InputTriggerType type);
    bool RemoveTrigger(const std::string& triggerId);
    std::string CreateInputContext(const std::string& name);
    bool RemoveInputContext(const std::string& contextId);
    bool MapAction(const std::string& contextId, const std::string& actionId, int key);
    bool UnmapAction(const std::string& contextId, const std::string& actionId);
    bool SetActionValueType(const std::string& actionId, InputActionValueType valueType);
    bool SetTriggerThreshold(const std::string& triggerId, float threshold);
    bool SetModifierScale(const std::string& modifierId, float scale);
    bool ActivateContext(const std::string& contextId);
    bool DeactivateContext(const std::string& contextId);
    bool PreviewAction(const std::string& actionId);
    const InputActionDef* GetAction(const std::string& actionId) const;
    const InputModifierDef* GetModifier(const std::string& modifierId) const;
    const InputTriggerDef* GetTrigger(const std::string& triggerId) const;
    const std::string* GetContext(const std::string& contextId) const;
    std::vector<std::string> GetAllActionIds() const;
    std::vector<std::string> GetAllContextIds() const;
    std::vector<std::string> GetMappingsByContext(const std::string& contextId) const;
    bool ValidateAction(const std::string& actionId) const;
    bool ExportInputConfig(const std::string& filePath) const;
    bool SaveInputConfig(const std::string& filePath) const;
    bool LoadInputConfig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, InputActionDef> m_actions;
    std::unordered_map<std::string, InputModifierDef> m_modifiers;
    std::unordered_map<std::string, InputTriggerDef> m_triggers;
    std::unordered_map<std::string, std::string> m_contexts;
    int m_nextActionIndex{0};
    int m_nextContextIndex{0};
};

} // namespace Atlas::Editor
