#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P17 Tool — Geometry scripting mesh operation authoring, boolean CSG, and procedural mesh generation.
class GeometryScriptTool : public ITool {
public:
    enum class MeshOperation { Boolean, Extrude, Revolve, Sweep, Subdivide, Simplify, Remesh, Offset, Shell };
    enum class BooleanMode { Union, Difference, Intersection, Trim };
    enum class GeomOutputType { StaticMesh, DynamicMesh, ProceduralMesh, Volume };

    struct MeshOpDef {
        std::string opId;
        std::string name;
        MeshOperation operation{MeshOperation::Boolean};
        std::vector<std::string> inputMeshIds;
        BooleanMode booleanMode{BooleanMode::Union};
        std::vector<std::string> parameters;
    };

    struct GeomScriptDef {
        std::string scriptId;
        std::string name;
        std::vector<std::string> ops;
        GeomOutputType outputType{GeomOutputType::StaticMesh};
        std::string outputPath;
        bool autoRebuild{false};
    };

    struct GeomBuildResult {
        std::string jobId;
        std::string scriptId;
        std::string outputPath;
        int vertexCount{0};
        int triCount{0};
        float elapsedMs{0.0f};
        std::vector<std::string> errors;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "GeometryScriptTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateScript(const std::string& name);
    bool RemoveScript(const std::string& scriptId);
    std::string AddOperation(const std::string& scriptId, MeshOperation op, const std::string& name);
    bool RemoveOperation(const std::string& scriptId, const std::string& opId);
    bool SetBooleanMode(const std::string& opId, BooleanMode mode);
    bool SetOutputType(const std::string& scriptId, GeomOutputType type);
    GeomBuildResult BuildScript(const std::string& scriptId);
    std::vector<GeomBuildResult> BuildAll();
    bool PreviewBuild(const std::string& scriptId);
    const GeomScriptDef* GetScript(const std::string& scriptId) const;
    const MeshOpDef* GetOperation(const std::string& opId) const;
    std::vector<std::string> GetAllScriptIds() const;
    std::vector<std::string> GetAllOpIds() const;
    const GeomBuildResult* GetBuildResult(const std::string& jobId) const;
    bool ValidateScript(const std::string& scriptId) const;
    bool ExportGeomScript(const std::string& scriptId, const std::string& filePath) const;
    bool SaveGeomScripts(const std::string& filePath) const;
    bool LoadGeomScripts(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, GeomScriptDef> m_scripts;
    std::unordered_map<std::string, MeshOpDef> m_operations;
    std::unordered_map<std::string, GeomBuildResult> m_buildResults;
    int m_nextScriptIndex{0};
    int m_nextOpIndex{0};
};

} // namespace Atlas::Editor
