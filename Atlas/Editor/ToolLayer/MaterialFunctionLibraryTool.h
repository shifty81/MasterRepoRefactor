#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P26 Tool — Material function library authoring, parameter exposure, and reuse graph.
class MaterialFunctionLibraryTool : public ITool {
public:
    enum class FunctionCategory { Math, Texture, Color, Utility, Lighting, Noise, Custom };
    enum class ParameterType { Float, Float2, Float3, Float4, Texture2D, Bool, Int, Custom };
    enum class FunctionScope { Local, Global, Shared, Deprecated, Custom };
    enum class OutputPinType { Color, Scalar, Vector, Boolean, Custom };

    struct MaterialFunctionDef {
        std::string functionId;
        std::string functionName;
        FunctionCategory category{FunctionCategory::Utility};
        FunctionScope scope{FunctionScope::Local};
        std::string description;
        std::string authorId;
        int version{1};
        bool published{false};
    };

    struct FunctionParameterDef {
        std::string paramId;
        std::string functionId;
        std::string paramName;
        ParameterType type{ParameterType::Float};
        std::string defaultValue;
        bool exposed{true};
        int sortOrder{0};
    };

    struct FunctionOutputDef {
        std::string outputId;
        std::string functionId;
        std::string outputName;
        OutputPinType pinType{OutputPinType::Scalar};
        std::string description;
        int sortOrder{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MaterialFunctionLibraryTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateFunction(const MaterialFunctionDef& def);
    bool DeleteFunction(const std::string& functionId);
    bool PublishFunction(const std::string& functionId);
    bool DeprecateFunction(const std::string& functionId);
    const MaterialFunctionDef* GetFunction(const std::string& functionId) const;
    std::vector<std::string> GetAllFunctionIds() const;
    std::vector<std::string> GetFunctionsByCategory(FunctionCategory category) const;
    std::vector<std::string> GetPublishedFunctions() const;
    bool AddParameter(const std::string& functionId, const FunctionParameterDef& param);
    bool RemoveParameter(const std::string& functionId, const std::string& paramId);
    bool ExposeParameter(const std::string& paramId, bool exposed);
    const FunctionParameterDef* GetParameter(const std::string& paramId) const;
    std::vector<std::string> GetParametersByFunction(const std::string& functionId) const;
    std::vector<std::string> GetExposedParameters(const std::string& functionId) const;
    bool AddOutput(const std::string& functionId, const FunctionOutputDef& output);
    bool RemoveOutput(const std::string& functionId, const std::string& outputId);
    const FunctionOutputDef* GetOutput(const std::string& outputId) const;
    std::vector<std::string> GetOutputsByFunction(const std::string& functionId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, MaterialFunctionDef> m_functions;
    std::unordered_map<std::string, std::vector<FunctionParameterDef>> m_params;
    std::unordered_map<std::string, std::vector<FunctionOutputDef>> m_outputs;
};

} // namespace Atlas::Editor
