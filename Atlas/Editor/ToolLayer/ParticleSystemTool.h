#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P6 Tool — Place and configure particle system emitters in the world.
class ParticleSystemTool : public ITool {
public:
    enum class EmitterShape { Sphere, Box, Cone, Ring };

    struct ParticleEmitter {
        std::string emitterId;
        std::string presetAsset;
        EmitterShape shape{EmitterShape::Sphere};
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        float emitRate{50.0f};
        float lifetime{2.0f};
        float radius{1.0f};
        bool looping{true};
        bool autoPlay{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ParticleSystemTool"; }
    bool IsActive() const override { return m_active; }

    std::string PlaceEmitter(float x, float y, float z,
                             const std::string& presetAsset = "");
    bool RemoveEmitter(const std::string& emitterId);
    bool SetEmitRate(const std::string& emitterId, float rate);
    bool SetEmitterShape(const std::string& emitterId, EmitterShape shape);
    bool SetLooping(const std::string& emitterId, bool looping);
    bool SetAutoPlay(const std::string& emitterId, bool autoPlay);
    bool PlayEmitter(const std::string& emitterId);
    bool StopEmitter(const std::string& emitterId);
    void RegisterPreset(const std::string& presetId, const std::string& assetPath);
    int GetPresetCount() const { return static_cast<int>(m_presets.size()); }
    const std::vector<ParticleEmitter>& GetEmitters() const { return m_emitters; }
    int GetEmitterCount() const { return static_cast<int>(m_emitters.size()); }

private:
    bool m_active{false};
    std::vector<ParticleEmitter> m_emitters;
    std::unordered_map<std::string, std::string> m_presets;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
