#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P15 Tool — Runtime debug overlay panels, visualizers, and diagnostic HUD management.
class RuntimeDebugOverlayTool : public ITool {
public:
    enum class OverlayPanel { FPS, Memory, CPU, GPU, DrawCalls, Physics, AI, Network, Audio, Custom };
    enum class VisualiserType { BoundingBox, Skeleton, NavMesh, Collision, LightRadius, CameraFrustum, Waypoints };
    enum class OverlayPosition { TopLeft, TopRight, BottomLeft, BottomRight, Center, Custom };

    struct OverlayConfig {
        std::string panelId;
        OverlayPanel panel{OverlayPanel::FPS};
        OverlayPosition position{OverlayPosition::TopLeft};
        bool visible{true};
        float opacity{1.0f};
        int fontSize{14};
    };

    struct VisualiserConfig {
        std::string visId;
        VisualiserType type{VisualiserType::BoundingBox};
        std::string targetEntityId;
        float colorR{1.0f};
        float colorG{0.0f};
        float colorB{0.0f};
        float lineWidth{1.0f};
    };

    struct OverlayTheme {
        std::string themeName;
        float backgroundColorR{0.0f};
        float backgroundColorG{0.0f};
        float backgroundColorB{0.0f};
        float textColorR{1.0f};
        float textColorG{1.0f};
        float textColorB{1.0f};
        float accentColorR{0.0f};
        float accentColorG{0.8f};
        float accentColorB{1.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "RuntimeDebugOverlayTool"; }
    bool IsActive() const override { return m_active; }

    // Panel management
    std::string AddPanel(OverlayPanel panel, OverlayPosition position = OverlayPosition::TopLeft);
    bool RemovePanel(const std::string& panelId);
    bool SetPanelVisible(const std::string& panelId, bool visible);
    bool SetPanelOpacity(const std::string& panelId, float opacity);
    bool SetPanelPosition(const std::string& panelId, OverlayPosition position);

    // Visualiser management
    std::string AddVisualiser(VisualiserType type, const std::string& targetEntityId);
    bool RemoveVisualiser(const std::string& visId);
    bool SetVisualiserColor(const std::string& visId, float r, float g, float b);

    // Theme
    bool SetTheme(const OverlayTheme& theme);
    bool ToggleAllPanels(bool visible);

    // Queries
    const OverlayConfig* GetPanelConfig(const std::string& panelId) const;
    std::vector<std::string> GetPanelIds() const;
    std::vector<std::string> GetVisualiserIds() const;

    // Persistence
    bool SaveOverlayConfig(const std::string& filePath) const;
    bool LoadOverlayConfig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, OverlayConfig> m_panels;
    std::unordered_map<std::string, VisualiserConfig> m_visualisers;
    OverlayTheme m_theme;
    int m_nextPanelIndex{0};
    int m_nextVisIndex{0};
};

} // namespace Atlas::Editor
