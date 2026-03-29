#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P26 Tool — Nav modifier volume placement, area flags, and agent cost override.
class NavModifierVolumeTool : public ITool {
public:
    enum class VolumeShape { Box, Sphere, Capsule, Convex, Custom };
    enum class NavAreaType { Walkable, Obstacle, Jump, Crouch, Swim, Fly, Null, Custom };
    enum class AgentType { Humanoid, Vehicle, Flying, Crawling, Custom };
    enum class ModifierBlend { Override, Add, Multiply, Min, Max, Custom };

    struct NavModifierVolumeDef {
        std::string volumeId;
        std::string volumeName;
        VolumeShape shape{VolumeShape::Box};
        NavAreaType areaType{NavAreaType::Walkable};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float extentX{100.0f};
        float extentY{100.0f};
        float extentZ{100.0f};
        bool enabled{true};
    };

    struct AgentCostOverrideDef {
        std::string overrideId;
        std::string volumeId;
        AgentType agentType{AgentType::Humanoid};
        float costMultiplier{1.0f};
        ModifierBlend blend{ModifierBlend::Override};
        bool blocksAgent{false};
    };

    struct NavAreaFlagDef {
        std::string flagId;
        std::string volumeId;
        std::string flagName;
        int flagValue{0};
        bool inherited{false};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "NavModifierVolumeTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateVolume(const NavModifierVolumeDef& def);
    bool DeleteVolume(const std::string& volumeId);
    bool EnableVolume(const std::string& volumeId, bool enabled);
    bool SetAreaType(const std::string& volumeId, NavAreaType areaType);
    const NavModifierVolumeDef* GetVolume(const std::string& volumeId) const;
    std::vector<std::string> GetAllVolumeIds() const;
    std::vector<std::string> GetVolumesByAreaType(NavAreaType type) const;
    std::vector<std::string> GetEnabledVolumes() const;
    bool AddAgentCostOverride(const std::string& volumeId, const AgentCostOverrideDef& ovr);
    bool RemoveAgentCostOverride(const std::string& volumeId, const std::string& overrideId);
    const AgentCostOverrideDef* GetAgentCostOverride(const std::string& overrideId) const;
    std::vector<std::string> GetCostOverridesByVolume(const std::string& volumeId) const;
    std::vector<std::string> GetCostOverridesByAgent(AgentType agentType) const;
    bool AddNavAreaFlag(const std::string& volumeId, const NavAreaFlagDef& flag);
    bool RemoveNavAreaFlag(const std::string& volumeId, const std::string& flagId);
    const NavAreaFlagDef* GetNavAreaFlag(const std::string& flagId) const;
    std::vector<std::string> GetFlagsByVolume(const std::string& volumeId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, NavModifierVolumeDef> m_volumes;
    std::unordered_map<std::string, std::vector<AgentCostOverrideDef>> m_costOverrides;
    std::unordered_map<std::string, std::vector<NavAreaFlagDef>> m_areaFlags;
};

} // namespace Atlas::Editor
