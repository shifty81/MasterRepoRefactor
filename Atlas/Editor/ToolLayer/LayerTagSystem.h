#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P3 Tool — Categorize assets with tags and control layer visibility.
class LayerTagSystem : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LayerTagSystem"; }
    bool IsActive() const override { return m_active; }

    void AddTag(const std::string& entityId, const std::string& tag);
    void RemoveTag(const std::string& entityId, const std::string& tag);
    void SetLayerVisible(const std::string& tag, bool visible);
    bool IsLayerVisible(const std::string& tag) const;
    std::vector<std::string> GetEntitiesWithTag(const std::string& tag) const;

private:
    bool m_active{false};
    std::unordered_map<std::string, bool> m_layerVisibility;
    std::unordered_map<std::string, std::vector<std::string>> m_tagToEntities;
};

} // namespace Atlas::Editor
