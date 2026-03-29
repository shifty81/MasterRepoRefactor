#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P2 Tool — Scripted event sequence editor with timeline scrubbing.
class EventTimelineTool : public ITool {
public:
    struct TimelineEvent {
        float timeSeconds{0.0f};
        std::string eventName;
        std::string targetEntityId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "EventTimelineTool"; }
    bool IsActive() const override { return m_active; }

    void AddEvent(float timeSeconds, const std::string& eventName,
                  const std::string& targetEntityId);
    void RemoveEvent(int index);
    void ScrubTo(float timeSeconds);
    void Play();
    void Stop();

    float GetCurrentTime() const { return m_currentTime; }
    bool IsPlaying() const { return m_playing; }
    const std::vector<TimelineEvent>& GetEvents() const { return m_events; }

private:
    bool m_active{false};
    bool m_playing{false};
    float m_currentTime{0.0f};
    std::vector<TimelineEvent> m_events;
};

} // namespace Atlas::Editor
