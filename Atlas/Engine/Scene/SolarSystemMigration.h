#pragma once
#include <string>
#include <vector>
#include <functional>

namespace Atlas::Engine {

/// Phase 24C — Versioned migration system for solar system data schemas.
/// Handles upgrading persisted solar system JSON from older format versions
/// to the current canonical format, with rollback support and audit logging.
class SolarSystemMigration {
public:
    enum class MigrationResult { Success, NoMigrationNeeded, Failed, RolledBack };
    enum class MigrationDirection { Upgrade, Downgrade };

    struct FieldRename {
        std::string oldName;
        std::string newName;
    };

    struct MigrationStep {
        std::string stepId;
        int fromVersion{0};
        int toVersion{1};
        MigrationDirection direction{MigrationDirection::Upgrade};
        std::string description;
        std::vector<FieldRename> fieldRenames;
        std::vector<std::string> removedFields;
        std::vector<std::string> addedFields;
        bool breakingChange{false};
    };

    struct MigrationReport {
        std::string systemId;
        int originalVersion{0};
        int targetVersion{0};
        MigrationResult result{MigrationResult::Success};
        std::vector<std::string> stepsApplied;
        std::vector<std::string> warnings;
        std::string errorMessage;
        bool dataLoss{false};
    };

    // Schema version registration
    void RegisterVersion(int version, const std::string& description);
    bool IsVersionRegistered(int version) const;
    int GetCurrentSchemaVersion() const { return m_currentVersion; }
    int GetMinSupportedVersion() const { return m_minVersion; }
    void SetCurrentSchemaVersion(int version);
    void SetMinSupportedVersion(int version);
    int GetRegisteredVersionCount() const { return static_cast<int>(m_versions.size()); }

    // Migration step registration
    std::string RegisterMigrationStep(int fromVersion, int toVersion,
                                       const std::string& description,
                                       bool breakingChange = false);
    bool AddFieldRename(const std::string& stepId,
                         const std::string& oldName, const std::string& newName);
    bool AddRemovedField(const std::string& stepId, const std::string& fieldName);
    bool AddAddedField(const std::string& stepId, const std::string& fieldName);
    int GetMigrationStepCount() const { return static_cast<int>(m_steps.size()); }
    const MigrationStep* GetStep(const std::string& stepId) const;

    // Migration execution
    MigrationReport Migrate(const std::string& systemId,
                             int fromVersion, int toVersion,
                             const std::string& dataJson = "");
    MigrationReport MigrateToLatest(const std::string& systemId,
                                     int fromVersion,
                                     const std::string& dataJson = "");
    bool CanMigrate(int fromVersion, int toVersion) const;
    std::vector<std::string> GetMigrationPath(int fromVersion, int toVersion) const;
    bool HasBreakingChanges(int fromVersion, int toVersion) const;

    // Validation
    bool ValidateSchema(const std::string& dataJson, int version) const;
    std::vector<std::string> GetSchemaErrors(const std::string& dataJson,
                                              int version) const;

    // Audit log
    void LogMigration(const MigrationReport& report);
    int GetMigrationLogCount() const { return static_cast<int>(m_log.size()); }
    const MigrationReport* GetLogEntry(int index) const;
    void ClearLog();

    // Callbacks
    using MigrationCallback = std::function<void(const MigrationReport&)>;
    void SetOnMigrationCompleteCallback(MigrationCallback cb);

    // Persistence
    bool SaveMigrationLog(const std::string& filePath) const;
    void Clear();

private:
    int m_currentVersion{1};
    int m_minVersion{1};
    std::vector<std::pair<int, std::string>> m_versions;   // version, description
    std::vector<MigrationStep> m_steps;
    std::vector<MigrationReport> m_log;
    MigrationCallback m_onComplete;
    int m_nextStepIndex{0};
};

} // namespace Atlas::Engine
