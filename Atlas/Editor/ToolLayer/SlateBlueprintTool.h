#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P23 Tool — Slate blueprint widget authoring, slot binding, and live preview management.
class SlateBlueprintTool : public ITool {
public:
    enum class WidgetSlotType { Canvas, Overlay, Horizontal, Vertical, Grid, Wrap, Custom };
    enum class BindingMode { OneWay, TwoWay, OneTime, EventDriven, Custom };
    enum class PreviewResolution { HD, FHD, QHD, UHD, Custom };
    enum class WidgetAnimMode { Play, Pause, Stop, Loop, PingPong, Custom };

    struct SlateWidgetDef {
        std::string widgetId;
        std::string widgetName;
        std::string widgetClass;
        WidgetSlotType slotType{WidgetSlotType::Canvas};
        bool isRoot{false};
    };

    struct SlotBindingDef {
        std::string bindingId;
        std::string widgetId;
        std::string propertyName;
        BindingMode mode{BindingMode::OneWay};
        std::string sourceExpression;
    };

    struct WidgetAnimationEntry {
        std::string animId;
        std::string widgetId;
        WidgetAnimMode animMode{WidgetAnimMode::Play};
        float duration{1.0f};
        bool looping{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SlateBlueprintTool"; }
    bool IsActive() const override { return m_active; }

    bool RegisterWidget(const SlateWidgetDef& def);
    bool UnregisterWidget(const std::string& widgetId);
    const SlateWidgetDef* GetWidget(const std::string& widgetId) const;
    std::vector<std::string> GetAllWidgetIds() const;
    std::vector<std::string> GetWidgetsBySlotType(WidgetSlotType slotType) const;
    bool AddBinding(const SlotBindingDef& binding);
    bool RemoveBinding(const std::string& bindingId);
    const SlotBindingDef* GetBinding(const std::string& bindingId) const;
    std::vector<std::string> GetBindingsForWidget(const std::string& widgetId) const;
    std::string CreateAnimation(const WidgetAnimationEntry& entry);
    bool DeleteAnimation(const std::string& animId);
    const WidgetAnimationEntry* GetAnimation(const std::string& animId) const;
    std::vector<std::string> GetAnimationsForWidget(const std::string& widgetId) const;
    bool SetAnimMode(const std::string& animId, WidgetAnimMode mode);
    bool StartPreview(PreviewResolution resolution);
    bool StopPreview();
    bool SetPreviewResolution(PreviewResolution resolution);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, SlateWidgetDef> m_widgets;
    std::unordered_map<std::string, SlotBindingDef> m_bindings;
    std::unordered_map<std::string, WidgetAnimationEntry> m_animations;
    int m_nextAnimIndex{0};
};

} // namespace Atlas::Editor
