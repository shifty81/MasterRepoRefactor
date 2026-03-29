#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P26 Tool — Skeletal mesh editing, bone weight painting, and LOD generation.
class SkeletalMeshEditorTool : public ITool {
public:
    enum class EditMode { Bones, Weights, Sockets, LOD, Morph, Physics, Custom };
    enum class WeightMode { Additive, Subtractive, Smooth, Normalize, Mirror, Custom };
    enum class BoneSelectionMode { Single, Chain, Hierarchy, All, Custom };
    enum class MeshLODStrategy { Auto, Manual, Distance, ScreenSize, Custom };

    struct BoneDef {
        std::string boneId;
        std::string boneName;
        std::string parentBoneId;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotX{0.0f};
        float rotY{0.0f};
        float rotZ{0.0f};
        float length{1.0f};
        bool isRoot{false};
    };

    struct WeightPaintEntry {
        std::string entryId;
        std::string boneId;
        std::string meshId;
        float brushRadius{5.0f};
        float brushStrength{0.5f};
        WeightMode mode{WeightMode::Additive};
        bool symmetry{false};
    };

    struct MeshLODEntry {
        std::string lodId;
        std::string meshId;
        int lodLevel{0};
        float screenSizeThreshold{1.0f};
        float reductionPercent{0.0f};
        MeshLODStrategy strategy{MeshLODStrategy::Auto};
        bool generated{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SkeletalMeshEditorTool"; }
    bool IsActive() const override { return m_active; }

    bool AddBone(const BoneDef& bone);
    bool RemoveBone(const std::string& boneId);
    bool RenameBone(const std::string& boneId, const std::string& newName);
    const BoneDef* GetBone(const std::string& boneId) const;
    std::vector<std::string> GetAllBoneIds() const;
    std::vector<std::string> GetChildBones(const std::string& parentBoneId) const;
    std::vector<std::string> GetRootBones() const;
    bool AddWeightPaintEntry(const WeightPaintEntry& entry);
    bool RemoveWeightPaintEntry(const std::string& entryId);
    bool ApplyWeightPaint(const std::string& entryId);
    bool NormalizeWeights(const std::string& meshId);
    const WeightPaintEntry* GetWeightPaintEntry(const std::string& entryId) const;
    std::vector<std::string> GetWeightEntriesByBone(const std::string& boneId) const;
    bool CreateLOD(const MeshLODEntry& lod);
    bool RemoveLOD(const std::string& lodId);
    bool GenerateLOD(const std::string& lodId);
    const MeshLODEntry* GetLOD(const std::string& lodId) const;
    std::vector<std::string> GetLODsByMesh(const std::string& meshId) const;
    bool SetEditMode(EditMode mode);
    EditMode GetEditMode() const;
    void Reset();

private:
    bool m_active{false};
    EditMode m_editMode{EditMode::Bones};
    std::unordered_map<std::string, BoneDef> m_bones;
    std::unordered_map<std::string, WeightPaintEntry> m_weightEntries;
    std::unordered_map<std::string, MeshLODEntry> m_lods;
};

} // namespace Atlas::Editor
