#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P15 Tool — Cinematic scene direction, shot management, and director timeline authoring.
class CinematicDirectorTool : public ITool {
public:
    enum class ShotType { Establishing, CutIn, CutAway, OverShoulder, POV, TwoShot, CloseUp, Extreme };
    enum class DirectorMode { Idle, Previewing, Recording, Exporting };
    enum class PlaybackState { Stopped, Playing, Paused, Scrubbing };

    struct ShotDescriptor {
        std::string shotId;
        std::string name;
        ShotType shotType{ShotType::Establishing};
        float cameraCutTime{0.0f};
        float duration{5.0f};
        std::string notes;
        std::string linkedCameraId;
        std::vector<std::string> linkedActorIds;
    };

    struct DirectorTimeline {
        std::string timelineId;
        std::string name;
        std::vector<std::string> shots;
    };

    struct DirectorExportSettings {
        std::string outputPath;
        float frameRate{30.0f};
        std::string resolution{"1920x1080"};
        std::string codec{"H264"};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CinematicDirectorTool"; }
    bool IsActive() const override { return m_active; }

    // Shot management
    std::string CreateShot(const std::string& name, ShotType type = ShotType::Establishing);
    bool RemoveShot(const std::string& shotId);
    bool AddShotToTimeline(const std::string& timelineId, const std::string& shotId);
    bool RemoveShotFromTimeline(const std::string& timelineId, const std::string& shotId);
    bool SetShotDuration(const std::string& shotId, float duration);
    bool LinkCamera(const std::string& shotId, const std::string& cameraId);
    bool LinkActor(const std::string& shotId, const std::string& actorId);

    // Timeline management
    std::string CreateTimeline(const std::string& name);
    bool RemoveTimeline(const std::string& timelineId);

    // Playback
    bool PreviewShot(const std::string& shotId);
    bool PreviewTimeline(const std::string& timelineId);
    bool StartRecording(const std::string& timelineId);
    bool StopRecording();
    bool ExportTimeline(const std::string& timelineId, const DirectorExportSettings& settings);

    // Queries
    const ShotDescriptor* GetShotById(const std::string& shotId) const;
    std::vector<std::string> GetAllShots() const;
    std::vector<std::string> GetTimelineShots(const std::string& timelineId) const;
    int GetShotCount() const { return static_cast<int>(m_shots.size()); }
    DirectorMode GetDirectorMode() const { return m_mode; }
    PlaybackState GetPlaybackState() const { return m_playbackState; }

    // Persistence
    bool SaveDirectorProject(const std::string& filePath) const;
    bool LoadDirectorProject(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    DirectorMode m_mode{DirectorMode::Idle};
    PlaybackState m_playbackState{PlaybackState::Stopped};
    std::unordered_map<std::string, ShotDescriptor> m_shots;
    std::unordered_map<std::string, DirectorTimeline> m_timelines;
    int m_nextShotIndex{0};
    int m_nextTimelineIndex{0};
};

} // namespace Atlas::Editor
