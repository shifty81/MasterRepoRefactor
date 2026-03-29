#pragma once
#include <string>
#include <vector>
#include <functional>
#include <unordered_map>

namespace Atlas::Engine {

/// Phase 26C — Solar system orbital and gravitational simulator.
/// Computes N-body gravitational interactions, orbital trajectories, and
/// Lagrange point positions for runtime and authoring time simulation.
class SolarSystemSimulator {
public:
    enum class IntegratorType { Euler, LeapFrog, RungeKutta4, Verlet };
    enum class SimulationMode { Realtime, FastForward, Offline };
    enum class BodyCategory { Star, Planet, Moon, Asteroid, Station, Comet };

    struct OrbitalElements {
        float semiMajorAxis{1.0f};       // AU
        float eccentricity{0.0f};
        float inclination{0.0f};          // degrees
        float longitudeAscNode{0.0f};     // degrees
        float argumentPeriapsis{0.0f};    // degrees
        float meanAnomaly{0.0f};          // degrees
        float period{365.25f};            // days
    };

    struct CelestialBody {
        std::string bodyId;
        std::string name;
        BodyCategory category{BodyCategory::Planet};
        float mass{1.0f};                // solar masses for stars, Earth masses for others
        float radius{1.0f};              // km
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float velX{0.0f};
        float velY{0.0f};
        float velZ{0.0f};
        float rotationPeriod{24.0f};     // hours
        float axialTilt{0.0f};           // degrees
        OrbitalElements orbitalElements;
        std::string parentBodyId;
        bool isFixed{false};
        bool enabled{true};
    };

    struct SimulationState {
        double simulatedTimeDays{0.0};
        int stepCount{0};
        int activeBodyCount{0};
        float kineticEnergy{0.0f};
        float potentialEnergy{0.0f};
        float angularMomentum{0.0f};
        bool isRunning{false};
        bool isPaused{false};
    };

    struct LagrangePoint {
        std::string pointId;
        std::string label;           // L1, L2, L3, L4, L5
        std::string primaryBodyId;
        std::string secondaryBodyId;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        bool isStable{false};
    };

    // Configuration
    void SetIntegrator(IntegratorType type);
    IntegratorType GetIntegrator() const { return m_integratorType; }
    void SetSimulationMode(SimulationMode mode);
    SimulationMode GetSimulationMode() const { return m_simMode; }
    void SetTimeStep(double stepDays);
    double GetTimeStep() const { return m_timeStepDays; }
    void SetFastForwardMultiplier(float multiplier);
    void SetGravitationalConstant(float G);

    // Body registration
    bool AddBody(const CelestialBody& body);
    bool RemoveBody(const std::string& bodyId);
    bool UpdateBody(const std::string& bodyId, const CelestialBody& body);
    bool SetBodyOrbitalElements(const std::string& bodyId,
                                  const OrbitalElements& elements);
    bool SetBodyPosition(const std::string& bodyId,
                          float px, float py, float pz);
    bool SetBodyVelocity(const std::string& bodyId,
                          float vx, float vy, float vz);
    bool SetBodyEnabled(const std::string& bodyId, bool enabled);
    int GetBodyCount() const { return static_cast<int>(m_bodies.size()); }
    const CelestialBody* GetBody(const std::string& bodyId) const;
    std::vector<std::string> GetBodyIds() const;
    std::vector<std::string> GetBodiesByCategory(BodyCategory cat) const;

    // Simulation control
    void Start();
    void Pause();
    void Resume();
    void Stop();
    void Reset();
    void Step(int steps = 1);
    const SimulationState& GetState() const { return m_state; }
    double GetSimulatedTimeDays() const { return m_state.simulatedTimeDays; }
    bool IsRunning() const { return m_state.isRunning; }
    bool IsPaused() const { return m_state.isPaused; }

    // Physics queries
    float GetDistanceBetween(const std::string& bodyAId,
                               const std::string& bodyBId) const;
    float GetRelativeVelocity(const std::string& bodyAId,
                                const std::string& bodyBId) const;
    float GetEscapeVelocity(const std::string& bodyId) const;
    float GetHillSphereRadius(const std::string& bodyId) const;
    float GetSphereOfInfluence(const std::string& bodyId) const;

    // Lagrange points
    bool ComputeLagrangePoints(const std::string& primaryId,
                                 const std::string& secondaryId);
    const LagrangePoint* GetLagrangePoint(const std::string& pointId) const;
    std::vector<LagrangePoint> GetAllLagrangePoints(
        const std::string& primaryId, const std::string& secondaryId) const;
    int GetLagrangePointCount() const { return static_cast<int>(m_lagrangePoints.size()); }

    // Trajectory prediction
    std::vector<std::pair<float, float>> PredictTrajectory(
        const std::string& bodyId, int steps, double stepDays = -1.0) const;

    // Callbacks
    using StepCallback = std::function<void(const SimulationState&)>;
    void SetOnStepCallback(StepCallback cb);
    using CollisionCallback = std::function<void(const std::string&, const std::string&)>;
    void SetOnCollisionCallback(CollisionCallback cb);

    // Persistence
    bool SaveState(const std::string& filePath) const;
    bool LoadState(const std::string& filePath);
    void Clear();

private:
    IntegratorType m_integratorType{IntegratorType::LeapFrog};
    SimulationMode m_simMode{SimulationMode::Realtime};
    double m_timeStepDays{1.0 / 86400.0};
    float m_fastForwardMultiplier{1.0f};
    float m_gravitationalConstant{6.674e-11f};
    SimulationState m_state;
    std::unordered_map<std::string, CelestialBody> m_bodies;
    std::unordered_map<std::string, LagrangePoint> m_lagrangePoints;
    StepCallback m_onStep;
    CollisionCallback m_onCollision;
};

} // namespace Atlas::Engine
