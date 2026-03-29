#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P10 Tool — Virtual camera rig authoring for cinematics and gameplay cameras.
class VirtualCameraRigTool : public ITool {
public:
    enum class RigType { Handheld, Steadicam, Crane, Dolly, Orbital, Locked };
    enum class FocusMode { Manual, AutoFocus, DepthOfField, TrackSubject };
    enum class LensPreset { Wide16mm, Normal35mm, Telephoto85mm, Telephoto200mm, Custom };

    struct LensSettings {
        LensPreset preset{LensPreset::Normal35mm};
        float focalLength{35.0f};
        float aperture{2.8f};
        float shutterSpeed{0.016f};
        float iso{400.0f};
        float focusDistance{5.0f};
        float nearClip{0.1f};
        float farClip{10000.0f};
    };

    struct RigNode {
        std::string nodeId;
        std::string name;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotX{0.0f};
        float rotY{0.0f};
        float rotZ{0.0f};
        float springStiffness{1.0f};
        float springDamping{0.2f};
        bool enableSpring{false};
    };

    struct CameraRig {
        std::string rigId;
        std::string name;
        RigType type{RigType::Handheld};
        FocusMode focusMode{FocusMode::Manual};
        LensSettings lens;
        std::vector<RigNode> nodes;
        std::string targetEntityId;
        bool active{true};
        float shakeIntensity{0.0f};
        float shakeFrequency{1.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "VirtualCameraRigTool"; }
    bool IsActive() const override { return m_active; }

    // Rig management
    std::string CreateRig(const std::string& name, RigType type = RigType::Handheld);
    bool RemoveRig(const std::string& rigId);
    bool SetRigType(const std::string& rigId, RigType type);
    bool SetFocusMode(const std::string& rigId, FocusMode mode);
    bool SetTargetEntity(const std::string& rigId, const std::string& entityId);
    bool SetRigActive(const std::string& rigId, bool active);
    bool SetShakeIntensity(const std::string& rigId, float intensity);
    bool SetShakeFrequency(const std::string& rigId, float frequency);
    int GetRigCount() const { return static_cast<int>(m_rigs.size()); }
    const CameraRig* GetRig(const std::string& rigId) const;
    std::vector<std::string> GetRigIds() const;
    std::vector<std::string> GetActiveRigIds() const;

    // Node management
    std::string AddNode(const std::string& rigId, const std::string& name,
                         float px = 0.0f, float py = 0.0f, float pz = 0.0f);
    bool RemoveNode(const std::string& rigId, const std::string& nodeId);
    bool SetNodePosition(const std::string& rigId, const std::string& nodeId,
                          float px, float py, float pz);
    bool SetNodeRotation(const std::string& rigId, const std::string& nodeId,
                          float rx, float ry, float rz);
    bool SetNodeSpring(const std::string& rigId, const std::string& nodeId,
                        float stiffness, float damping);
    int GetNodeCount(const std::string& rigId) const;

    // Lens
    bool SetLensPreset(const std::string& rigId, LensPreset preset);
    bool SetFocalLength(const std::string& rigId, float mm);
    bool SetAperture(const std::string& rigId, float aperture);
    bool SetFocusDistance(const std::string& rigId, float distance);

    // Persistence
    bool SaveRigs(const std::string& filePath) const;
    bool LoadRigs(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, CameraRig> m_rigs;
    int m_nextRigIndex{0};
    int m_nextNodeIndex{0};
};

} // namespace Atlas::Editor
