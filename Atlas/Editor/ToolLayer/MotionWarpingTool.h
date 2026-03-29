#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P17 Tool — Motion warping target authoring, warp window configuration, and root motion adjustment.
class MotionWarpingTool : public ITool {
public:
    enum class WarpAlgorithm { Simple, Scale, Rotation, RotationAndScale, IK, PhysicsBlend };
    enum class WarpAxis { XY, XYZ, Z, Horizontal, Vertical, All };
    enum class WarpTrigger { Animation, Montage, Sequence, Manual, Overlap, Custom };

    struct WarpTarget {
        std::string targetId;
        std::string name;
        std::vector<float> location;
        std::vector<float> rotation;
        std::vector<float> scale;
        WarpAlgorithm algorithm{WarpAlgorithm::Simple};
        WarpAxis axis{WarpAxis::XYZ};
    };

    struct WarpWindow {
        std::string windowId;
        std::string animationAsset;
        float startTime{0.0f};
        float endTime{1.0f};
        std::string warpTargetId;
        WarpTrigger warpTrigger{WarpTrigger::Animation};
    };

    struct WarpingConfig {
        std::string configId;
        std::string agentId;
        std::string syncPoint;
        float blendIn{0.1f};
        float blendOut{0.1f};
        float toleranceRadius{50.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MotionWarpingTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateWarpTarget(const std::string& name);
    bool RemoveWarpTarget(const std::string& targetId);
    std::string CreateWarpWindow(const std::string& animAsset, const std::string& targetId);
    bool RemoveWarpWindow(const std::string& windowId);
    bool SetWarpAlgorithm(const std::string& targetId, WarpAlgorithm algorithm);
    bool SetWarpAxis(const std::string& targetId, WarpAxis axis);
    bool SetWarpLocation(const std::string& targetId, float x, float y, float z);
    bool SetWarpRotation(const std::string& targetId, float x, float y, float z);
    bool SetWarpTrigger(const std::string& windowId, WarpTrigger trigger);
    bool SetWarpingConfig(const WarpingConfig& config);
    bool AddWindowToConfig(const std::string& configId, const std::string& windowId);
    bool PreviewWarp(const std::string& targetId);
    const WarpTarget* GetWarpTarget(const std::string& targetId) const;
    const WarpWindow* GetWarpWindow(const std::string& windowId) const;
    std::vector<std::string> GetAllTargetIds() const;
    std::vector<std::string> GetAllWindowIds() const;
    std::vector<std::string> GetWindowsByAgent(const std::string& agentId) const;
    bool ValidateWarpConfig(const std::string& configId) const;
    bool ExportWarpConfig(const std::string& configId, const std::string& filePath) const;
    bool SaveWarpTargets(const std::string& filePath) const;
    bool LoadWarpTargets(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, WarpTarget> m_targets;
    std::unordered_map<std::string, WarpWindow> m_windows;
    std::unordered_map<std::string, WarpingConfig> m_configs;
    int m_nextTargetIndex{0};
    int m_nextWindowIndex{0};
};

} // namespace Atlas::Editor
