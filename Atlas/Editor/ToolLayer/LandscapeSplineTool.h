#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P21 Tool — Landscape spline authoring, mesh assignment, and deformation configuration.
class LandscapeSplineTool : public ITool {
public:
    enum class SplineEditMode { Select, AddPoint, DeletePoint, MovePoint, AdjustTangent, SplitSegment, Custom };
    enum class DeformationType { None_, Raise, Lower, Flatten, Smooth, Carve, Custom };
    enum class MeshAlignMode { AlignToSpline, AlignToSurface, WorldUp, Custom };

    struct SplinePointConfig {
        std::string pointId;
        std::string splineId;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float width{200.0f};
        float layerWidth{200.0f};
        float tangentWeight{1.0f};
        bool selected{false};
    };

    struct SplineSegmentConfig {
        std::string segmentId;
        std::string splineId;
        std::string startPointId;
        std::string endPointId;
        std::string meshAssetId;
        float meshOffset{0.0f};
        MeshAlignMode alignMode{MeshAlignMode::AlignToSpline};
        bool flipMesh{false};
    };

    struct SplineDeformConfig {
        std::string deformId;
        std::string splineId;
        DeformationType deformType{DeformationType::Flatten};
        float deformStrength{1.0f};
        float falloffRadius{500.0f};
        float falloffAngle{45.0f};
        bool affectHeightmap{true};
        bool affectLayers{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LandscapeSplineTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateSpline(const std::string& name, const std::string& landscapeActorId);
    bool DeleteSpline(const std::string& splineId);
    std::vector<std::string> GetAllSplineIds() const;
    bool SetSplineEnabled(const std::string& splineId, bool enabled);

    std::string AddPoint(const std::string& splineId, const SplinePointConfig& point);
    bool RemovePoint(const std::string& splineId, const std::string& pointId);
    bool MovePoint(const std::string& pointId, float x, float y, float z);
    bool SetPointWidth(const std::string& pointId, float width);
    bool SetPointTangentWeight(const std::string& pointId, float weight);
    const SplinePointConfig* GetPoint(const std::string& pointId) const;
    std::vector<std::string> GetPointsForSpline(const std::string& splineId) const;

    std::string AddSegment(const std::string& splineId, const SplineSegmentConfig& segment);
    bool RemoveSegment(const std::string& splineId, const std::string& segmentId);
    bool AssignMesh(const std::string& segmentId, const std::string& meshAssetId);
    bool SetMeshAlignMode(const std::string& segmentId, MeshAlignMode mode);
    const SplineSegmentConfig* GetSegment(const std::string& segmentId) const;

    std::string ApplyDeform(const SplineDeformConfig& config);
    bool RemoveDeform(const std::string& deformId);
    bool SetDeformStrength(const std::string& deformId, float strength);
    bool SetDeformType(const std::string& deformId, DeformationType type);
    void SetEditMode(SplineEditMode mode);
    SplineEditMode GetEditMode() const { return m_editMode; }
    bool RebuildSplineMesh(const std::string& splineId);
    int GetSplineCount() const;
    void Reset();

private:
    bool m_active{false};
    SplineEditMode m_editMode{SplineEditMode::Select};
    std::unordered_map<std::string, SplinePointConfig> m_points;
    std::unordered_map<std::string, SplineSegmentConfig> m_segments;
    std::unordered_map<std::string, SplineDeformConfig> m_deforms;
    int m_nextSplineIndex{0};
};

} // namespace Atlas::Editor
