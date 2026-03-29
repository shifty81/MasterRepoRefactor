#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P5 Tool — PCG-driven automatic entity placement using density rules and seeds.
class ProceduralPlacementTool : public ITool {
public:
    struct PlacementRule {
        std::string entityType;
        float density{1.0f};
        float minSpacing{2.0f};
        int pcgSeed{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ProceduralPlacementTool"; }
    bool IsActive() const override { return m_active; }

    void AddRule(const PlacementRule& rule);
    void RemoveRule(const std::string& entityType);
    int GetRuleCount() const { return static_cast<int>(m_rules.size()); }
    int RunPlacement(float areaX, float areaZ, float radius);
    void ClearPlacements();
    int GetPlacedCount() const { return m_placedCount; }
    void SetGlobalSeed(int seed);
    int GetGlobalSeed() const { return m_globalSeed; }

private:
    bool m_active{false};
    std::vector<PlacementRule> m_rules;
    int m_placedCount{0};
    int m_globalSeed{0};
};

} // namespace Atlas::Editor
