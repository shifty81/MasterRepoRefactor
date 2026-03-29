#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P9 Tool — Fluid and water simulation authoring and parameter editor.
class FluidSimulationTool : public ITool {
public:
    enum class FluidType { Water, Lava, Oil, Blood, Smoke, Gas };
    enum class BoundaryType { Open, Closed, Periodic };
    enum class SolverType { SPH, FLIP, PIC, LBM };
    enum class EmitterShape { Point, Box, Sphere, Mesh };

    struct FluidEmitter {
        std::string emitterId;
        std::string name;
        EmitterShape shape{EmitterShape::Box};
        float posX{0.0f};
        float posY{5.0f};
        float posZ{0.0f};
        float extentX{1.0f};
        float extentY{1.0f};
        float extentZ{1.0f};
        float emissionRate{100.0f};
        float velocity{1.0f};
        float velDirX{0.0f};
        float velDirY{-1.0f};
        float velDirZ{0.0f};
        bool enabled{true};
    };

    struct FluidDomain {
        std::string domainId;
        std::string name;
        FluidType fluidType{FluidType::Water};
        SolverType solverType{SolverType::FLIP};
        BoundaryType boundaryX{BoundaryType::Closed};
        BoundaryType boundaryY{BoundaryType::Closed};
        BoundaryType boundaryZ{BoundaryType::Closed};
        float domainSizeX{10.0f};
        float domainSizeY{5.0f};
        float domainSizeZ{10.0f};
        int resolutionX{32};
        int resolutionY{16};
        int resolutionZ{32};
        float viscosity{0.001f};
        float surfaceTension{0.07f};
        float density{1000.0f};
        float gravity{-9.81f};
        float timeScale{1.0f};
        int subSteps{2};
        std::string materialId;
        std::vector<std::string> emitterIds;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "FluidSimulationTool"; }
    bool IsActive() const override { return m_active; }

    // Domain management
    std::string CreateDomain(const std::string& name, FluidType type = FluidType::Water,
                              SolverType solver = SolverType::FLIP);
    bool RemoveDomain(const std::string& domainId);
    bool SetDomainSize(const std::string& domainId, float sx, float sy, float sz);
    bool SetDomainResolution(const std::string& domainId, int rx, int ry, int rz);
    bool SetFluidType(const std::string& domainId, FluidType type);
    bool SetSolverType(const std::string& domainId, SolverType solver);
    bool SetViscosity(const std::string& domainId, float viscosity);
    bool SetSurfaceTension(const std::string& domainId, float tension);
    bool SetDensity(const std::string& domainId, float density);
    bool SetGravity(const std::string& domainId, float gravity);
    bool SetTimeScale(const std::string& domainId, float scale);
    bool SetSubSteps(const std::string& domainId, int steps);
    bool SetDomainMaterial(const std::string& domainId, const std::string& materialId);
    int GetDomainCount() const { return static_cast<int>(m_domains.size()); }
    const FluidDomain* GetDomain(const std::string& domainId) const;
    std::vector<std::string> GetDomainIds() const;

    // Emitter management
    std::string CreateEmitter(const std::string& name, const std::string& domainId,
                               EmitterShape shape = EmitterShape::Box);
    bool RemoveEmitter(const std::string& emitterId);
    bool SetEmitterPosition(const std::string& emitterId, float px, float py, float pz);
    bool SetEmitterExtent(const std::string& emitterId, float ex, float ey, float ez);
    bool SetEmissionRate(const std::string& emitterId, float rate);
    bool SetEmitterVelocity(const std::string& emitterId, float speed,
                             float dx, float dy, float dz);
    bool SetEmitterEnabled(const std::string& emitterId, bool enabled);
    int GetEmitterCount() const { return static_cast<int>(m_emitters.size()); }
    const FluidEmitter* GetEmitter(const std::string& emitterId) const;
    std::vector<std::string> GetEmitterIdsForDomain(const std::string& domainId) const;

    // Simulation control
    bool BakeDomain(const std::string& domainId, float duration = 5.0f);
    bool ClearBake(const std::string& domainId);
    bool IsBaked(const std::string& domainId) const;
    bool StepSimulation(const std::string& domainId, float deltaTime);

    // Persistence
    bool SaveFluidScene(const std::string& filePath) const;
    bool LoadFluidScene(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::vector<FluidDomain> m_domains;
    std::vector<FluidEmitter> m_emitters;
    int m_nextDomainIndex{0};
    int m_nextEmitterIndex{0};
};

} // namespace Atlas::Editor
