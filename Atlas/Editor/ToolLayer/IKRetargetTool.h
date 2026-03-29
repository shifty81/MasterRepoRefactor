#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P17 Tool — IK retargeting chain authoring, pose correction, and skeleton mapping management.
class IKRetargetTool : public ITool {
public:
    enum class IKChainType { Spine, Limb, FullBody, Partial, Facial, Tail };
    enum class RetargetMode { CopyPose, IKSolve, AnimationDriven, HybridIK };
    enum class BoneMatchMethod { Name, Hierarchy, Manual, Semantic };

    struct IKChainDef {
        std::string chainId;
        std::string name;
        IKChainType chainType{IKChainType::Limb};
        std::string rootBone;
        std::string endBone;
        RetargetMode retargetMode{RetargetMode::IKSolve};
        int solverIterations{10};
        float tolerance{0.001f};
    };

    struct SkeletonMapping {
        std::string mappingId;
        std::string sourceSkeleton;
        std::string targetSkeleton;
        BoneMatchMethod boneMatchMethod{BoneMatchMethod::Name};
        std::vector<std::string> bonePairs;
    };

    struct RetargetProfile {
        std::string profileId;
        std::string name;
        std::string sourceSkeleton;
        std::string targetSkeleton;
        std::vector<std::string> chains;
        float poseCorrectionScale{1.0f};
        float stretchFactor{1.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "IKRetargetTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateChain(const std::string& name, IKChainType type);
    bool RemoveChain(const std::string& chainId);
    std::string CreateMapping(const std::string& srcSkeleton, const std::string& tgtSkeleton);
    bool RemoveMapping(const std::string& mappingId);
    std::string CreateProfile(const std::string& name, const std::string& srcSkeleton, const std::string& tgtSkeleton);
    bool RemoveProfile(const std::string& profileId);
    bool AddChainToProfile(const std::string& profileId, const std::string& chainId);
    bool MapBone(const std::string& mappingId, const std::string& srcBone, const std::string& tgtBone);
    bool AutoMapBones(const std::string& mappingId);
    bool SetRetargetMode(const std::string& chainId, RetargetMode mode);
    bool SetSolverIterations(const std::string& chainId, int iterations);
    bool PreviewRetarget(const std::string& profileId);
    const IKChainDef* GetChain(const std::string& chainId) const;
    const SkeletonMapping* GetMapping(const std::string& mappingId) const;
    const RetargetProfile* GetProfile(const std::string& profileId) const;
    std::vector<std::string> GetAllChainIds() const;
    std::vector<std::string> GetAllMappingIds() const;
    std::vector<std::string> GetAllProfileIds() const;
    bool ValidateProfile(const std::string& profileId) const;
    bool ExportProfile(const std::string& profileId, const std::string& filePath) const;
    bool SaveRetargetData(const std::string& filePath) const;
    bool LoadRetargetData(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, IKChainDef> m_chains;
    std::unordered_map<std::string, SkeletonMapping> m_mappings;
    std::unordered_map<std::string, RetargetProfile> m_profiles;
    int m_nextChainIndex{0};
    int m_nextMappingIndex{0};
};

} // namespace Atlas::Editor
