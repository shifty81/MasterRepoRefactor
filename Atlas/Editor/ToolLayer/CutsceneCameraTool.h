#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P7 Tool — Place, animate, and sequence cameras for in-engine cutscenes.
class CutsceneCameraTool : public ITool {
public:
    enum class EasingType { Linear, EaseIn, EaseOut, EaseInOut, Bezier };

    struct CameraKeyframe {
        std::string keyframeId;
        float time{0.0f};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotPitch{0.0f};
        float rotYaw{0.0f};
        float rotRoll{0.0f};
        float fov{60.0f};
        float dofFocalDistance{10.0f};
        float dofAperture{2.8f};
        EasingType easing{EasingType::EaseInOut};
    };

    struct CutsceneTrack {
        std::string trackId;
        std::string name;
        float duration{5.0f};
        std::vector<CameraKeyframe> keyframes;
        bool looping{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CutsceneCameraTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateTrack(const std::string& name, float duration = 5.0f);
    bool RemoveTrack(const std::string& trackId);
    std::string AddKeyframe(const std::string& trackId, float time,
                            float px, float py, float pz,
                            float pitch = 0.0f, float yaw = 0.0f);
    bool RemoveKeyframe(const std::string& trackId, const std::string& kfId);
    bool SetKeyframeFOV(const std::string& trackId,
                        const std::string& kfId, float fov);
    bool SetKeyframeEasing(const std::string& trackId,
                           const std::string& kfId, EasingType easing);
    bool SetTrackLooping(const std::string& trackId, bool looping);
    bool SetTrackDuration(const std::string& trackId, float duration);
    bool PlayTrack(const std::string& trackId);
    bool StopTrack(const std::string& trackId);
    const CutsceneTrack* GetTrack(const std::string& trackId) const;
    int GetTrackCount() const { return static_cast<int>(m_tracks.size()); }
    void ClearAll();

private:
    bool m_active{false};
    std::vector<CutsceneTrack> m_tracks;
    int m_nextTrackIndex{0};
    int m_nextKfIndex{0};
};

} // namespace Atlas::Editor
