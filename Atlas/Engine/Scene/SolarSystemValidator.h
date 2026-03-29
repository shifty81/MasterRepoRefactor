#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 30C — Validator for solar system data integrity, consistency, and configuration compliance.
class SolarSystemValidator {
public:
    enum class ValidationSeverity { Info, Warning, Error, Critical };
    enum class ValidationCategory { Structure, Orbit, Physics, Data, Config, Security };
    enum class ValidationState { NotValidated, Validating, Valid, Invalid, Partial };

    struct ValidationIssue {
        std::string issueId;
        ValidationSeverity severity{ValidationSeverity::Info};
        ValidationCategory category{ValidationCategory::Data};
        std::string message;
        std::string objectRef;
        std::string ruleId;
    };

    struct ValidationReport {
        std::string reportId;
        std::string systemId;
        ValidationState state{ValidationState::NotValidated};
        std::vector<ValidationIssue> issues;
        std::string validatedAt;
        float duration{0.0f};
    };

    struct ValidationRule {
        std::string ruleId;
        std::string name;
        ValidationCategory category{ValidationCategory::Data};
        bool enabled{true};
        bool mandatory{false};
    };

    // Rule management
    bool RegisterRule(const ValidationRule& rule);
    bool UnregisterRule(const std::string& ruleId);
    bool EnableRule(const std::string& ruleId);
    bool DisableRule(const std::string& ruleId);

    // Validation
    ValidationReport ValidateSystem(const std::string& systemId,
                                    const std::string& dataPath) const;
    std::vector<ValidationReport> ValidateSystemBatch(
        const std::vector<std::string>& systemIds,
        const std::string& dataDir) const;

    // Report queries
    const ValidationReport* GetReport(const std::string& reportId) const;
    std::vector<ValidationReport> GetAllReports() const;
    std::vector<ValidationIssue> GetIssuesByCategory(const std::string& reportId,
                                                      ValidationCategory category) const;
    std::vector<ValidationIssue> GetIssuesBySeverity(const std::string& reportId,
                                                      ValidationSeverity severity) const;

    // Rule queries
    int GetRuleCount() const { return static_cast<int>(m_rules.size()); }
    std::vector<ValidationRule> GetRules() const;

    // Utilities
    void ClearReports();
    bool ExportReport(const std::string& reportId, const std::string& filePath) const;
    bool LoadRules(const std::string& filePath);
    bool IsSystemValid(const std::string& reportId) const;
    ValidationState GetValidationState(const std::string& reportId) const;
    void AddCustomValidator(const std::string& ruleId,
                            std::function<bool(const std::string&)> validator);

private:
    std::unordered_map<std::string, ValidationRule> m_rules;
    std::unordered_map<std::string, ValidationReport> m_reports;
    std::unordered_map<std::string,
        std::function<bool(const std::string&)>> m_customValidators;
    int m_nextReportIndex{0};
};

} // namespace Atlas::Engine
