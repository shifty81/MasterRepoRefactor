#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P18 Tool — Environment Query System query authoring, test configuration, and generator management.
class EnvironmentQueryTool : public ITool {
public:
    enum class EQSGeneratorType { ActorsOfClass, OnCircle, Grid, PathingGrid, Composite, Custom };
    enum class EQSTestType { Distance, Dot, Trace, Overlap, Pathfinding, Gameplay, Custom };
    enum class EQSScoringFactor { Constant, Linear, InverseLinear, Square, Step };

    struct EQSGeneratorDef {
        std::string generatorId;
        std::string name;
        EQSGeneratorType generatorType{EQSGeneratorType::OnCircle};
        float radius{500.0f};
        float density{100.0f};
        int maxItems{50};
        std::string filterClass;
    };

    struct EQSTestDef {
        std::string testId;
        std::string name;
        EQSTestType testType{EQSTestType::Distance};
        EQSScoringFactor scoringFactor{EQSScoringFactor::Linear};
        float weight{1.0f};
        int filterMode{0};
        float filterMin{0.0f};
        float filterMax{10000.0f};
    };

    struct EQSQueryDef {
        std::string queryId;
        std::string name;
        std::vector<std::string> generators;
        std::vector<std::string> tests;
        std::string itemType;
        int runMode{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "EnvironmentQueryTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateQuery(const std::string& name);
    bool RemoveQuery(const std::string& queryId);
    std::string AddGenerator(const std::string& queryId, const std::string& name, EQSGeneratorType type);
    bool RemoveGenerator(const std::string& queryId, const std::string& generatorId);
    std::string AddTest(const std::string& queryId, const std::string& name, EQSTestType type);
    bool RemoveTest(const std::string& queryId, const std::string& testId);
    bool SetGeneratorType(const std::string& generatorId, EQSGeneratorType type);
    bool SetTestType(const std::string& testId, EQSTestType type);
    bool SetScoringFactor(const std::string& testId, EQSScoringFactor factor);
    bool SetTestWeight(const std::string& testId, float weight);
    bool SetFilterMode(const std::string& testId, int filterMode);
    bool RunQuery(const std::string& queryId, std::vector<std::string>& outResults) const;
    bool RunQueryAsync(const std::string& queryId, const std::string& callbackId);
    bool CancelQuery(const std::string& queryId);
    bool PreviewQuery(const std::string& queryId);
    const EQSQueryDef* GetQuery(const std::string& queryId) const;
    const EQSGeneratorDef* GetGenerator(const std::string& generatorId) const;
    const EQSTestDef* GetTest(const std::string& testId) const;
    std::vector<std::string> GetAllQueryIds() const;
    std::vector<std::string> GetGeneratorsByQuery(const std::string& queryId) const;
    std::vector<std::string> GetTestsByQuery(const std::string& queryId) const;
    std::vector<std::string> GetQueryResults(const std::string& queryId) const;
    bool ValidateQuery(const std::string& queryId) const;
    bool ExportQuery(const std::string& queryId, const std::string& filePath) const;
    bool SaveQueries(const std::string& filePath) const;
    bool LoadQueries(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, EQSQueryDef> m_queries;
    std::unordered_map<std::string, EQSGeneratorDef> m_generators;
    std::unordered_map<std::string, EQSTestDef> m_tests;
    int m_nextQueryIndex{0};
    int m_nextGeneratorIndex{0};
    int m_nextTestIndex{0};
};

} // namespace Atlas::Editor
