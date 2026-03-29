#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P28 Tool — Vector field volume authoring, flow visualization, and particle coupling.
class VectorFieldEditorTool : public ITool {
public:
    enum class FieldType { Uniform, Vortex, Turbulent, Radial, Drag, Wind, Custom };
    enum class FieldDimension { TwoD, ThreeD, Custom };
    enum class VoxelDataType { Float16, Float32, Byte, Custom };
    enum class ParticleCoupling { OneWay, TwoWay, None, Custom };

    struct VectorFieldDef {
        std::string fieldId;
        std::string fieldName;
        FieldType fieldType{FieldType::Uniform};
        FieldDimension dimension{FieldDimension::ThreeD};
        VoxelDataType dataType{VoxelDataType::Float16};
        int resolutionX{32};
        int resolutionY{32};
        int resolutionZ{32};
        float boundsX{100.0f};
        float boundsY{100.0f};
        float boundsZ{100.0f};
        float intensity{1.0f};
        bool enabled{true};
    };

    struct FlowVisualizationDef {
        std::string visId;
        std::string fieldId;
        int streamlineCount{64};
        float stepSize{0.5f};
        float maxLength{50.0f};
        float lineWidth{1.0f};
        bool showArrows{true};
        bool useHeatMap{false};
        bool enabled{true};
    };

    struct ParticleCouplingDef {
        std::string couplingId;
        std::string fieldId;
        std::string particleSystemId;
        ParticleCoupling couplingType{ParticleCoupling::OneWay};
        float influenceRadius{10.0f};
        float strengthScale{1.0f};
        float dragCoefficient{0.1f};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "VectorFieldEditorTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateField(const VectorFieldDef& def);
    bool DeleteField(const std::string& fieldId);
    bool EnableField(const std::string& fieldId, bool enabled);
    bool SetFieldType(const std::string& fieldId, FieldType type);
    const VectorFieldDef* GetField(const std::string& fieldId) const;
    std::vector<std::string> GetAllFieldIds() const;
    std::vector<std::string> GetFieldsByType(FieldType type) const;
    std::vector<std::string> GetFieldsByDimension(FieldDimension dim) const;
    std::vector<std::string> GetEnabledFields() const;
    bool AddVisualization(const std::string& fieldId, const FlowVisualizationDef& def);
    bool RemoveVisualization(const std::string& fieldId, const std::string& visId);
    bool EnableVisualization(const std::string& visId, bool enabled);
    const FlowVisualizationDef* GetVisualization(const std::string& visId) const;
    std::vector<std::string> GetVisualizationsByField(const std::string& fieldId) const;
    bool AddCoupling(const std::string& fieldId, const ParticleCouplingDef& def);
    bool RemoveCoupling(const std::string& fieldId, const std::string& couplingId);
    bool SetCouplingType(const std::string& couplingId, ParticleCoupling type);
    const ParticleCouplingDef* GetCoupling(const std::string& couplingId) const;
    std::vector<std::string> GetCouplingsByField(const std::string& fieldId) const;
    std::vector<std::string> GetCouplingsByType(ParticleCoupling type) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, VectorFieldDef> m_fields;
    std::unordered_map<std::string, FlowVisualizationDef> m_visualizations;
    std::unordered_map<std::string, ParticleCouplingDef> m_couplings;
};

} // namespace Atlas::Editor
