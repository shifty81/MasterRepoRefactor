#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P27 Tool — Spline deformer cage authoring, lattice binding, and deformation baking.
class SplineDeformerTool : public ITool {
public:
    enum class DeformerType { SplineWarp, Lattice, Cage, Bend, Twist, Taper, Custom };
    enum class BindingMethod { ClosestPoint, Geodesic, Volume, Automatic, Custom };
    enum class DeformationAxis { X, Y, Z, XY, XZ, YZ, All, Custom };
    enum class InterpolationMode { Linear, Cubic, Bezier, BSpline, Custom };

    struct SplineDeformerDef {
        std::string deformerId;
        std::string deformerName;
        DeformerType deformerType{DeformerType::SplineWarp};
        std::string meshId;
        BindingMethod bindingMethod{BindingMethod::Automatic};
        DeformationAxis axis{DeformationAxis::Y};
        float stretchFactor{1.0f};
        float rollFactor{0.0f};
        float twistFactor{0.0f};
        bool preserveVolume{true};
        bool enabled{true};
    };

    struct SplineControlPointDef {
        std::string pointId;
        std::string deformerId;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float tangentX{0.0f};
        float tangentY{1.0f};
        float tangentZ{0.0f};
        InterpolationMode interpolation{InterpolationMode::Bezier};
        float weight{1.0f};
        int index{0};
    };

    struct DeformationBakeDef {
        std::string bakeId;
        std::string deformerId;
        std::string outputMeshId;
        float frameStart{0.0f};
        float frameEnd{1.0f};
        int frameSamples{1};
        bool bakeNormals{true};
        bool bakeTangents{false};
        bool completed{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SplineDeformerTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateDeformer(const SplineDeformerDef& def);
    bool DeleteDeformer(const std::string& deformerId);
    bool EnableDeformer(const std::string& deformerId, bool enabled);
    bool SetDeformerType(const std::string& deformerId, DeformerType type);
    const SplineDeformerDef* GetDeformer(const std::string& deformerId) const;
    std::vector<std::string> GetAllDeformerIds() const;
    std::vector<std::string> GetDeformersByType(DeformerType type) const;
    std::vector<std::string> GetDeformersByMesh(const std::string& meshId) const;
    bool AddControlPoint(const std::string& deformerId, const SplineControlPointDef& point);
    bool RemoveControlPoint(const std::string& deformerId, const std::string& pointId);
    bool MoveControlPoint(const std::string& pointId, float x, float y, float z);
    const SplineControlPointDef* GetControlPoint(const std::string& pointId) const;
    std::vector<std::string> GetControlPointsByDeformer(const std::string& deformerId) const;
    bool CreateBake(const DeformationBakeDef& def);
    bool ExecuteBake(const std::string& bakeId);
    bool DeleteBake(const std::string& bakeId);
    const DeformationBakeDef* GetBake(const std::string& bakeId) const;
    std::vector<std::string> GetBakesByDeformer(const std::string& deformerId) const;
    std::vector<std::string> GetCompletedBakes() const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, SplineDeformerDef> m_deformers;
    std::unordered_map<std::string, SplineControlPointDef> m_controlPoints;
    std::unordered_map<std::string, DeformationBakeDef> m_bakes;
};

} // namespace Atlas::Editor
