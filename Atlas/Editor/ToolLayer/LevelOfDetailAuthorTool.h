#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P11 Tool — Manual Level-of-Detail authoring for mesh asset groups.
class LevelOfDetailAuthorTool : public ITool {
public:
    enum class LODTransitionMode { Distance, ScreenSize, BlendTree };
    enum class NormalMode { Preserve, Recalculate, Transfer };
    enum class SimplificationAlgorithm { QuadricError, Voxelization, Progressive };

    struct LODScreenSizeThreshold {
        int lodIndex{0};
        float screenSizePercent{100.0f};
        float transitionWidth{0.05f};
    };

    struct LODMeshVariant {
        std::string variantId;
        int lodLevel{0};
        std::string meshId;
        std::string meshPath;
        float screenSizeThreshold{100.0f};
        float distanceThreshold{0.0f};
        int triangleCount{0};
        int vertexCount{0};
        float reductionPercent{0.0f};
        bool hasBillboard{false};
    };

    struct LODGroup {
        std::string groupId;
        std::string name;
        LODTransitionMode transitionMode{LODTransitionMode::ScreenSize};
        NormalMode normalMode{NormalMode::Preserve};
        SimplificationAlgorithm algorithm{SimplificationAlgorithm::QuadricError};
        std::vector<LODMeshVariant> variants;
        std::string baseMeshId;
        std::string baseMeshPath;
        float fadeTransitionWidth{0.05f};
        bool animateCrossFade{true};
        bool receiveGI{true};
        bool autoGenerate{false};
        int autoGenerateLevels{3};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LevelOfDetailAuthorTool"; }
    bool IsActive() const override { return m_active; }

    // Group management
    std::string CreateGroup(const std::string& name,
                             const std::string& baseMeshId = "");
    bool RemoveGroup(const std::string& groupId);
    bool SetBaseMesh(const std::string& groupId, const std::string& meshId,
                      const std::string& meshPath = "");
    bool SetTransitionMode(const std::string& groupId, LODTransitionMode mode);
    bool SetNormalMode(const std::string& groupId, NormalMode mode);
    bool SetAlgorithm(const std::string& groupId, SimplificationAlgorithm algo);
    bool SetFadeTransitionWidth(const std::string& groupId, float width);
    bool SetAnimateCrossFade(const std::string& groupId, bool animate);
    bool SetReceiveGI(const std::string& groupId, bool receive);
    bool SetAutoGenerate(const std::string& groupId, bool autoGen, int levels = 3);
    int GetGroupCount() const { return static_cast<int>(m_groups.size()); }
    const LODGroup* GetGroup(const std::string& groupId) const;
    std::vector<std::string> GetGroupIds() const;

    // Variant management
    std::string AddVariant(const std::string& groupId, int lodLevel,
                            const std::string& meshId,
                            float screenSizeThreshold = 50.0f);
    bool RemoveVariant(const std::string& groupId, const std::string& variantId);
    bool SetVariantMesh(const std::string& groupId, const std::string& variantId,
                         const std::string& meshId, const std::string& meshPath = "");
    bool SetVariantScreenSize(const std::string& groupId,
                               const std::string& variantId, float screenSize);
    bool SetVariantDistance(const std::string& groupId,
                             const std::string& variantId, float distance);
    bool SetVariantTriangleCount(const std::string& groupId,
                                  const std::string& variantId, int count);
    bool SetVariantBillboard(const std::string& groupId,
                               const std::string& variantId, bool hasBillboard);
    int GetVariantCount(const std::string& groupId) const;
    const LODMeshVariant* GetVariant(const std::string& groupId,
                                       const std::string& variantId) const;

    // Auto-generation
    bool AutoGenerateLODs(const std::string& groupId);
    std::vector<LODScreenSizeThreshold> GetDefaultThresholds(int lodLevels) const;

    // Preview
    bool PreviewAtLODLevel(const std::string& groupId, int lodLevel);
    int GetCurrentPreviewLOD(const std::string& groupId) const;

    // Persistence
    bool SaveGroups(const std::string& filePath) const;
    bool LoadGroups(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, LODGroup> m_groups;
    std::unordered_map<std::string, int> m_previewLOD;
    int m_nextGroupIndex{0};
    int m_nextVariantIndex{0};
};

} // namespace Atlas::Editor
