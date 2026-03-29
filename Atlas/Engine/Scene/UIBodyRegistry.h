#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 33D — Registry for UI body definitions used by the widget and interface subsystem.
class UIBodyRegistry {
public:
    enum class UIBodyState { Hidden, Visible, Active, Focused, Disabled, Animating, Destroyed };
    enum class UIBodyType { Widget, Panel, Button, Label, Image, Slider, InputField, Dropdown, List, Canvas };
    enum class UIAnchor { TopLeft, TopCenter, TopRight, MiddleLeft, Center, MiddleRight, BottomLeft, BottomCenter, BottomRight, Custom };
    enum class UIScaleMode { Constant, ScreenRelative, ViewportRelative, DPIAware, Custom };
    enum class UIUpdateMode { Always, Visible, OnDemand, Throttled };

    struct UIStyleDef {
        std::string styleId;
        std::string fontFamily;
        int fontSize{14};
        float foregroundR{1.0f};
        float foregroundG{1.0f};
        float foregroundB{1.0f};
        float foregroundA{1.0f};
        float backgroundR{0.0f};
        float backgroundG{0.0f};
        float backgroundB{0.0f};
        float backgroundA{0.8f};
        float borderWidth{1.0f};
        float borderRadius{4.0f};
        float padding{8.0f};
    };

    struct UILayoutDef {
        std::string layoutId;
        UIAnchor anchorPreset{UIAnchor::Center};
        float posX{0.0f};
        float posY{0.0f};
        float width{100.0f};
        float height{50.0f};
        int zOrder{0};
        UIScaleMode scaleMode{UIScaleMode::Constant};
    };

    struct UIBodyRecord {
        std::string bodyId;
        std::string name;
        UIBodyType uiType{UIBodyType::Widget};
        UIStyleDef styleDef;
        UILayoutDef layoutDef;
        UIUpdateMode updateMode{UIUpdateMode::Always};
        std::string tooltipText;
        bool visible{true};
        bool enabled{true};
        bool interactive{true};
        bool looping{false};
        UIBodyState bodyState{UIBodyState::Hidden};
    };

    // Body registration
    bool RegisterBody(const UIBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);

    // State and visibility
    bool SetBodyState(const std::string& bodyId, UIBodyState state);
    bool SetBodyVisible(const std::string& bodyId, bool visible);
    bool SetBodyEnabled(const std::string& bodyId, bool enabled);
    bool SetBodyInteractive(const std::string& bodyId, bool interactive);

    // Layout
    bool SetBodyPosition(const std::string& bodyId, float x, float y);
    bool SetBodySize(const std::string& bodyId, float width, float height);
    bool SetBodyAnchor(const std::string& bodyId, UIAnchor anchor);
    bool SetZOrder(const std::string& bodyId, int zOrder);
    bool SetScaleMode(const std::string& bodyId, UIScaleMode scaleMode);

    // Style and update
    bool SetStyleDef(const std::string& bodyId, const UIStyleDef& style);
    bool SetLayoutDef(const std::string& bodyId, const UILayoutDef& layout);
    bool SetUpdateMode(const std::string& bodyId, UIUpdateMode mode);
    bool SetTooltip(const std::string& bodyId, const std::string& tooltip);

    // Queries
    const UIBodyRecord* GetBodyById(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByType(UIBodyType type) const;
    std::vector<std::string> GetBodiesByState(UIBodyState state) const;
    std::vector<std::string> GetVisibleBodies() const;
    std::vector<std::string> GetActiveBodies() const;
    std::string GetFocusedBody() const;
    std::vector<std::string> GetBodiesInZRange(int zMin, int zMax) const;

    // Persistence
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, UIBodyRecord> m_bodies;
};

} // namespace Atlas::Engine
