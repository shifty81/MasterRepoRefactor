#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P8 Tool — Weather system authoring tool for dynamic weather and environmental effects.
class WeatherSystemTool : public ITool {
public:
    enum class WeatherType { Clear, Cloudy, Rain, Storm, Snow, Fog, Sandstorm, Hail };
    enum class TransitionCurve { Linear, EaseIn, EaseOut, EaseInOut, Step };
    enum class WindDirection { North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest };

    struct WeatherState {
        std::string stateId;
        std::string name;
        WeatherType type{WeatherType::Clear};
        float precipitationIntensity{0.0f};
        float cloudCoverage{0.0f};
        float fogDensity{0.0f};
        float windSpeed{0.0f};
        WindDirection windDirection{WindDirection::North};
        float temperature{20.0f};
        float visibility{1000.0f};
        float thunderProbability{0.0f};
    };

    struct WeatherTransition {
        std::string transitionId;
        std::string fromStateId;
        std::string toStateId;
        float duration{30.0f};
        TransitionCurve curve{TransitionCurve::EaseInOut};
        float probability{1.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "WeatherSystemTool"; }
    bool IsActive() const override { return m_active; }

    // State management
    std::string CreateWeatherState(const std::string& name, WeatherType type);
    bool RemoveWeatherState(const std::string& stateId);
    bool SetWeatherStateType(const std::string& stateId, WeatherType type);
    bool SetPrecipitation(const std::string& stateId, float intensity);
    bool SetCloudCoverage(const std::string& stateId, float coverage);
    bool SetFogDensity(const std::string& stateId, float density);
    bool SetWindSpeed(const std::string& stateId, float speed);
    bool SetWindDirection(const std::string& stateId, WindDirection direction);
    bool SetTemperature(const std::string& stateId, float celsius);
    int GetStateCount() const { return static_cast<int>(m_states.size()); }
    const WeatherState* GetWeatherState(const std::string& stateId) const;

    // Transition management
    std::string AddTransition(const std::string& fromId, const std::string& toId,
                               float duration = 30.0f,
                               TransitionCurve curve = TransitionCurve::EaseInOut);
    bool RemoveTransition(const std::string& transitionId);
    bool SetTransitionDuration(const std::string& transitionId, float duration);
    bool SetTransitionCurve(const std::string& transitionId, TransitionCurve curve);
    bool SetTransitionProbability(const std::string& transitionId, float probability);
    int GetTransitionCount() const { return static_cast<int>(m_transitions.size()); }
    const WeatherTransition* GetTransition(const std::string& transitionId) const;

    // Playback / preview
    bool SetActiveState(const std::string& stateId);
    bool TriggerTransition(const std::string& transitionId);
    std::string GetActiveStateId() const { return m_activeStateId; }
    bool IsTransitioning() const { return m_isTransitioning; }

    // Zones
    bool AddWeatherZone(const std::string& stateId, float cx, float cz, float radius);
    int GetWeatherZoneCount() const { return static_cast<int>(m_zones.size()); }

    // Persistence
    bool SaveProfile(const std::string& filePath) const;
    bool LoadProfile(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    bool m_isTransitioning{false};
    std::string m_activeStateId;
    std::vector<WeatherState> m_states;
    std::vector<WeatherTransition> m_transitions;
    std::vector<std::tuple<std::string, float, float, float>> m_zones; // stateId, cx, cz, radius
    int m_nextStateIndex{0};
    int m_nextTransIndex{0};
};

} // namespace Atlas::Editor
