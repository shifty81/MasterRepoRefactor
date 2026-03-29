#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 32C — Auditor for solar system data integrity, constraint checks, and anomaly detection.
class SolarSystemAuditor {
public:
    enum class AuditState { Idle, Running, Paused, Complete, Failed };
    enum class AuditSeverity { Info, Warning, Error, Critical };
    enum class CheckCategory { Structure, Physics, Gameplay, AI, Streaming, Content, Custom };

    struct AuditFinding {
        std::string findingId;
        CheckCategory category{CheckCategory::Structure};
        AuditSeverity severity{AuditSeverity::Info};
        std::string ruleId;
        std::string targetId;
        std::string message;
        bool autoFixable{false};
    };

    struct AuditRule {
        std::string ruleId;
        std::string name;
        CheckCategory category{CheckCategory::Structure};
        std::string description;
        bool enabled{true};
        AuditSeverity failSeverity{AuditSeverity::Warning};
    };

    struct AuditReport {
        std::string reportId;
        std::string systemId;
        std::string systemName;
        std::vector<std::string> findings;
        std::vector<std::string> rules;
        int passedCount{0};
        int failedCount{0};
        AuditState auditState{AuditState::Idle};
        double timestamp{0.0};
    };

    // Rule management
    bool RegisterRule(const AuditRule& rule);
    bool UnregisterRule(const std::string& ruleId);
    bool EnableRule(const std::string& ruleId);
    bool DisableRule(const std::string& ruleId);
    const AuditRule* GetRule(const std::string& ruleId) const;
    std::vector<std::string> GetAllRuleIds() const;
    std::vector<std::string> GetRulesByCategory(CheckCategory category) const;

    // Audit lifecycle
    bool RunAudit(const std::string& systemId);
    bool PauseAudit();
    bool ResumeAudit();
    bool CancelAudit();

    // Report access
    const AuditReport* GetReport(const std::string& reportId) const;
    const AuditFinding* GetFinding(const std::string& findingId) const;
    std::vector<std::string> GetFindingsBySeverity(AuditSeverity severity) const;
    std::vector<std::string> GetFindingsByCategory(CheckCategory category) const;
    AuditState GetAuditState() const { return m_state; }

    // Auto-fix
    bool AutoFix(const std::string& findingId);
    int AutoFixAll();

    // Metrics
    float GetPassRate() const;

    // Persistence
    bool ExportReport(const std::string& reportId, const std::string& filePath) const;
    bool LoadReport(const std::string& filePath);

    // Maintenance
    void ClearFindings();
    void Reset();

private:
    AuditState m_state{AuditState::Idle};
    std::unordered_map<std::string, AuditRule> m_rules;
    std::unordered_map<std::string, AuditFinding> m_findings;
    std::unordered_map<std::string, AuditReport> m_reports;
    int m_nextReportIndex{0};
    int m_nextFindingIndex{0};
};

} // namespace Atlas::Engine
