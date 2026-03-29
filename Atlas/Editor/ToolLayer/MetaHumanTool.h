#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P21 Tool — MetaHuman identity configuration, LOD management, and facial animation authoring.
class MetaHumanTool : public ITool {
public:
    enum class MetaHumanGender { Male, Female, NonBinary, Custom };
    enum class LODPolicy { Automatic, Manual, ScreenSize, Distance, Forced, Custom };
    enum class FacialAnimChannel { Brow, Eye, Nose, Mouth, Cheek, Jaw, Custom };

    struct MetaHumanIdentityDef {
        std::string identityId;
        std::string name;
        MetaHumanGender gender{MetaHumanGender::Custom};
        std::string skinPreset;
        std::string hairPreset;
        std::string eyeColorPreset;
        int age{30};
        std::string regionPreset;
    };

    struct LODConfigDef {
        std::string configId;
        std::string identityId;
        LODPolicy policy{LODPolicy::Automatic};
        int activeLODLevel{0};
        int maxLODLevel{4};
        float screenSizeThreshold{0.05f};
        float distanceThreshold{1000.0f};
        bool enableDynamicLOD{true};
    };

    struct FacialAnimBlendShape {
        std::string blendShapeId;
        std::string identityId;
        FacialAnimChannel channel{FacialAnimChannel::Mouth};
        std::string curveName;
        float weight{0.0f};
        float minWeight{0.0f};
        float maxWeight{1.0f};
        bool driven{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MetaHumanTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateIdentity(const MetaHumanIdentityDef& def);
    bool DeleteIdentity(const std::string& identityId);
    const MetaHumanIdentityDef* GetIdentity(const std::string& identityId) const;
    std::vector<std::string> GetAllIdentityIds() const;
    bool SetGender(const std::string& identityId, MetaHumanGender gender);
    bool SetSkinPreset(const std::string& identityId, const std::string& preset);
    bool SetHairPreset(const std::string& identityId, const std::string& preset);
    bool SetAge(const std::string& identityId, int age);

    std::string CreateLODConfig(const LODConfigDef& def);
    bool DeleteLODConfig(const std::string& configId);
    const LODConfigDef* GetLODConfig(const std::string& configId) const;
    bool SetLODPolicy(const std::string& configId, LODPolicy policy);
    bool SetActiveLODLevel(const std::string& configId, int level);
    bool SetScreenSizeThreshold(const std::string& configId, float threshold);
    bool SetDynamicLOD(const std::string& configId, bool enabled);

    std::string AddBlendShape(const FacialAnimBlendShape& shape);
    bool RemoveBlendShape(const std::string& blendShapeId);
    const FacialAnimBlendShape* GetBlendShape(const std::string& blendShapeId) const;
    std::vector<std::string> GetBlendShapesByChannel(FacialAnimChannel channel) const;
    bool SetBlendShapeWeight(const std::string& blendShapeId, float weight);

    bool ExportIdentity(const std::string& identityId, const std::string& filePath) const;
    bool ImportIdentity(const std::string& filePath);
    int GetIdentityCount() const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, MetaHumanIdentityDef> m_identities;
    std::unordered_map<std::string, LODConfigDef> m_lodConfigs;
    std::unordered_map<std::string, FacialAnimBlendShape> m_blendShapes;
    int m_nextIdentityIndex{0};
};

} // namespace Atlas::Editor
