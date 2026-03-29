#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 29D — Registry for animation bodies with clip, blend, layer, and LOD management
class AnimationBodyRegistry {
public:
    enum class AnimationBodyState { Inactive, Active, Playing, Paused, Stopped, Transitioning };
    enum class AnimationClipType { Skeletal, Morph, Procedural, Physics, Hybrid };
    enum class BlendSpace { TwoD, OneD, Direct };
    enum class AnimationLayer { Base, Override, Additive, Gesture, Cinematic };

    struct ClipBounds {
        float startTime{0.0f};
        float endTime{1.0f};
        float blendIn{0.1f};
        float blendOut{0.1f};
        bool loop{false};
    };

    struct BlendWeights {
        std::string layer;
        float weight{1.0f};
        std::vector<std::string> maskBones;
    };

    struct AnimationRuntimeSettings {
        float speed{1.0f};
        float currentTime{0.0f};
        bool rootMotion{false};
        bool mirrorX{false};
        float transitionDuration{0.2f};
    };

    struct AnimationLODSettings {
        float lodDistance0{10.0f};
        float lodDistance1{30.0f};
        float lodDistance2{60.0f};
        int maxBonesLOD0{64};
        int maxBonesLOD1{32};
        int maxBonesLOD2{16};
        bool disableAtMaxDistance{false};
    };

    struct AnimationBodyRecord {
        std::string recordId;
        std::string name;
        std::string sceneId;
        AnimationBodyState state{AnimationBodyState::Inactive};
        AnimationClipType clipType{AnimationClipType::Skeletal};
        BlendSpace blendSpace{BlendSpace::TwoD};
        AnimationLayer layer{AnimationLayer::Base};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        BlendWeights blendWeights;
        AnimationRuntimeSettings runtimeSettings;
        AnimationLODSettings lodSettings;
        std::vector<std::string> clipIds;
        bool active{false};
    };

    std::string RegisterBody(const std::string& name, const std::string& sceneId);
    bool UnregisterBody(const std::string& id);
    bool SetBodyState(const std::string& id, AnimationBodyState state);
    bool SetBodyPosition(const std::string& id, float x, float y, float z);
    bool ActivateBody(const std::string& id);
    bool DeactivateBody(const std::string& id);
    bool PlayBody(const std::string& id);
    bool PauseBody(const std::string& id);
    bool StopBody(const std::string& id);
    bool SetClipType(const std::string& id, AnimationClipType clipType);
    bool SetBlendSpace(const std::string& id, BlendSpace blendSpace);
    bool SetLayer(const std::string& id, AnimationLayer layer);
    bool SetBlendWeights(const std::string& id, const BlendWeights& weights);
    bool SetRuntimeSettings(const std::string& id, const AnimationRuntimeSettings& settings);
    bool SetLODSettings(const std::string& id, const AnimationLODSettings& lodSettings);
    bool SetAnimationSpeed(const std::string& id, float speed);
    bool SetAnimationTime(const std::string& id, float time);

    int GetBodyCount() const;
    const AnimationBodyRecord* GetBody(const std::string& id) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByScene(const std::string& sceneId) const;
    std::vector<std::string> GetBodiesByLayer(AnimationLayer layer) const;
    std::vector<std::string> GetBodiesByState(AnimationBodyState state) const;

    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, AnimationBodyRecord> m_records;
    int m_nextIndex{0};
};

} // namespace Atlas::Engine
