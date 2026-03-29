#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P25 Tool — Asset data validation, schema enforcement, and validation report generation.
class DataValidatorTool : public ITool {
public:
    enum class ValidationSeverity { Info, Warning, Error, Critical, Custom };
    enum class ValidatorScope { Asset, Package, Project, Custom };
    enum class ValidationRuleType { Schema, Range, Reference, Format, Custom, Dependency };
    enum class ValidationReportState { Pending, Running, Passed, Failed, Partial, Custom };

    struct ValidationRuleDef {
        std::string ruleId;
        std::string ruleName;
        ValidationRuleType ruleType{ValidationRuleType::Schema};
        ValidatorScope scope{ValidatorScope::Asset};
        ValidationSeverity severity{ValidationSeverity::Error};
        std::string expr;
        bool enabled{true};
    };

    struct ValidationResult {
        std::string resultId;
        std::string ruleId;
        std::string assetId;
        ValidationSeverity severity{ValidationSeverity::Error};
        std::string message;
        bool passed{false};
    };

    struct ValidationReport {
        std::string reportId;
        std::string assetId;
        ValidationReportState state{ValidationReportState::Pending};
        std::vector<std::string> resultIds;
        int errorCount{0};
        int warningCount{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "DataValidatorTool"; }
    bool IsActive() const override { return m_active; }

    bool RegisterRule(const ValidationRuleDef& rule);
    bool UnregisterRule(const std::string& ruleId);
    const ValidationRuleDef* GetRule(const std::string& ruleId) const;
    std::vector<std::string> GetAllRuleIds() const;
    std::vector<std::string> GetRulesByScope(ValidatorScope scope) const;
    bool ValidateAsset(const std::string& assetId, const std::string& ruleId);
    const ValidationResult* GetResult(const std::string& resultId) const;
    std::vector<std::string> GetResultsByRule(const std::string& ruleId) const;
    std::vector<std::string> GetResultsByAsset(const std::string& assetId) const;
    bool BuildReport(const std::string& assetId);
    const ValidationReport* GetReport(const std::string& reportId) const;
    std::vector<std::string> GetAllReportIds() const;
    std::vector<std::string> GetReportsByState(ValidationReportState state) const;
    std::vector<std::string> GetPassedReports() const;
    std::vector<std::string> GetFailedReports() const;
    void ClearResults();
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, ValidationRuleDef> m_rules;
    std::unordered_map<std::string, ValidationResult> m_results;
    std::unordered_map<std::string, ValidationReport> m_reports;
};

} // namespace Atlas::Editor
