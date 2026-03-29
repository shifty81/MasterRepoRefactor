#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P19 Tool — Interchange framework asset translation, pipeline configuration, and importer/exporter management.
class InterchangeTool : public ITool {
public:
    enum class InterchangePipelineType { Import, Export, Reimport, Scripted, Custom };
    enum class TranslatorType { FBX, GLTF, OBJ, USD, Alembic, DataTable, Custom };
    enum class PipelineExecutionFlags { None_, Async, Silent, Batch, Preview, Validate };

    struct TranslatorConfig {
        std::string translatorId;
        std::string name;
        TranslatorType translatorType{TranslatorType::FBX};
        std::vector<std::string> supportedExtensions;
        bool enabled{true};
        int priority{0};
    };

    struct PipelineDef {
        std::string pipelineId;
        std::string name;
        InterchangePipelineType pipelineType{InterchangePipelineType::Import};
        std::string translatorId;
        PipelineExecutionFlags flags{PipelineExecutionFlags::None_};
        std::vector<std::string> preprocessors;
        std::vector<std::string> postProcessors;
    };

    struct InterchangeResult {
        std::string resultId;
        std::string pipelineId;
        std::string inputPath;
        std::string outputPath;
        bool success{false};
        std::vector<std::string> warnings;
        std::vector<std::string> errors;
        double elapsedMs{0.0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "InterchangeTool"; }
    bool IsActive() const override { return m_active; }

    bool RegisterTranslator(const TranslatorConfig& config);
    bool UnregisterTranslator(const std::string& translatorId);
    std::string CreatePipeline(const std::string& name, InterchangePipelineType type, const std::string& translatorId);
    bool RemovePipeline(const std::string& pipelineId);
    const PipelineDef* GetPipeline(const std::string& pipelineId) const;
    std::vector<std::string> GetAllPipelineIds() const;
    bool SetPipelineType(const std::string& pipelineId, InterchangePipelineType type);
    bool SetExecutionFlags(const std::string& pipelineId, PipelineExecutionFlags flags);
    bool AddPreProcessor(const std::string& pipelineId, const std::string& processorId);
    bool RemovePreProcessor(const std::string& pipelineId, const std::string& processorId);
    bool AddPostProcessor(const std::string& pipelineId, const std::string& processorId);
    bool RemovePostProcessor(const std::string& pipelineId, const std::string& processorId);
    InterchangeResult RunPipeline(const std::string& pipelineId, const std::string& inputPath);
    bool RunPipelineAsync(const std::string& pipelineId, const std::string& inputPath, const std::string& callbackId);
    bool CancelPipeline(const std::string& pipelineId);
    const InterchangeResult* GetResult(const std::string& resultId) const;
    std::vector<std::string> GetAllResults() const;
    bool PreviewPipeline(const std::string& pipelineId);
    bool ValidatePipeline(const std::string& pipelineId) const;
    std::vector<std::string> ListTranslators() const;
    std::vector<std::string> ListPipelines() const;
    void ClearResults();
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, PipelineDef> m_pipelines;
    std::unordered_map<std::string, TranslatorConfig> m_translators;
    std::unordered_map<std::string, InterchangeResult> m_results;
    int m_nextPipelineIndex{0};
    int m_nextResultIndex{0};
};

} // namespace Atlas::Editor
