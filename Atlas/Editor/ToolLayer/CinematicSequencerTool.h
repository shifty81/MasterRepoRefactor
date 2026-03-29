#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P4 Tool — Compose in-engine cinematic sequences with keyframes and camera tracks.
class CinematicSequencerTool : public ITool {
public:
    struct Keyframe {
        float time{0.0f};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotYaw{0.0f};
        float fov{60.0f};
    };

    struct Track {
        std::string id;
        std::string name;
        std::vector<Keyframe> keyframes;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CinematicSequencerTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateTrack(const std::string& name);
    bool AddKeyframe(const std::string& trackId, const Keyframe& kf);
    bool RemoveTrack(const std::string& trackId);
    void Play();
    void Stop();
    bool IsPlaying() const { return m_playing; }
    const std::vector<Track>& GetTracks() const { return m_tracks; }
    int GetTrackCount() const { return static_cast<int>(m_tracks.size()); }

private:
    bool m_active{false};
    bool m_playing{false};
    std::vector<Track> m_tracks;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
