#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P17 Tool — Niagara particle system authoring, emitter configuration, and GPU simulation management.
class NiagaraSystemTool : public ITool {
public:
    enum class EmitterType { CPU, GPU, GPUMesh, Ribbon, Sprite, Beam };
    enum class SimulationSpace { World, Local, Custom };
    enum class EmissionMode { Burst, Continuous, EventDriven, Scripted };

    struct EmitterDef {
        std::string emitterId;
        std::string name;
        EmitterType emitterType{EmitterType::CPU};
        SimulationSpace simulationSpace{SimulationSpace::World};
        float spawnRate{100.0f};
        int maxParticles{1000};
        float lifetime{2.0f};
        float startDelay{0.0f};
    };

    struct SystemModule {
        std::string moduleId;
        std::string name;
        bool enabled{true};
        int sortPriority{0};
        std::string scriptPath;
    };

    struct NiagaraSystemDef {
        std::string systemId;
        std::string name;
        std::vector<std::string> emitters;
        std::vector<std::string> modules;
        bool autoActivate{true};
        bool looping{false};
        float warmupTime{0.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "NiagaraSystemTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateSystem(const std::string& name);
    bool RemoveSystem(const std::string& systemId);
    std::string AddEmitter(const std::string& systemId, const std::string& name, EmitterType type);
    bool RemoveEmitter(const std::string& systemId, const std::string& emitterId);
    std::string AddModule(const std::string& systemId, const std::string& name, const std::string& scriptPath);
    bool RemoveModule(const std::string& systemId, const std::string& moduleId);
    bool SetSpawnRate(const std::string& emitterId, float rate);
    bool SetMaxParticles(const std::string& emitterId, int maxParticles);
    bool SetSimulationSpace(const std::string& emitterId, SimulationSpace space);
    bool SetEmissionMode(const std::string& emitterId, EmissionMode mode);
    bool ActivateSystem(const std::string& systemId);
    bool DeactivateSystem(const std::string& systemId);
    bool ResetSystem(const std::string& systemId);
    bool PreviewSystem(const std::string& systemId);
    const NiagaraSystemDef* GetSystem(const std::string& systemId) const;
    const EmitterDef* GetEmitter(const std::string& emitterId) const;
    std::vector<std::string> GetAllSystemIds() const;
    std::vector<std::string> GetAllEmitterIds() const;
    std::vector<std::string> GetModulesBySystem(const std::string& systemId) const;
    bool ValidateSystem(const std::string& systemId) const;
    bool ExportSystem(const std::string& systemId, const std::string& filePath) const;
    bool SaveSystem(const std::string& filePath) const;
    bool LoadSystem(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, NiagaraSystemDef> m_systems;
    std::unordered_map<std::string, EmitterDef> m_emitters;
    std::unordered_map<std::string, SystemModule> m_modules;
    int m_nextSystemIndex{0};
    int m_nextEmitterIndex{0};
};

} // namespace Atlas::Editor
