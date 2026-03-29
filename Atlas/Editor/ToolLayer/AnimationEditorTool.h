#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P1 Tool — Multi-layer animation editing.
class AnimationEditorTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AnimationEditorTool"; }
    bool IsActive() const override { return m_active; }

    void LoadClip(const std::string& clipName);
    void AddLayer(const std::string& layerName);
    void SetPlaybackRate(float rate);
    float GetPlaybackRate() const { return m_playbackRate; }
    const std::vector<std::string>& GetLayers() const { return m_layers; }

private:
    bool m_active{false};
    float m_playbackRate{1.0f};
    std::vector<std::string> m_layers;
};

} // namespace Atlas::Editor
