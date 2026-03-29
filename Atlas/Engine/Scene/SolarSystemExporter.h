#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 33C — Exporter for solar system data to various output formats and external pipeline targets.
class SolarSystemExporter {
public:
    enum class ExportState { Idle, Preparing, Exporting, Finalizing, Complete, Failed, Cancelled };
    enum class ExportFormat { JSON, Binary, CSV, XML, FlatBuffers, USD, Custom };
    enum class ExportTarget { File, Database, Network, Cloud, Memory, Custom };

    struct ExportFilter {
        std::string filterId;
        std::string name;
        std::vector<std::string> includeTypes;
        std::vector<std::string> excludeTypes;
        float minOrbitRadius{0.0f};
        float maxOrbitRadius{1000.0f};
        std::vector<std::string> factionFilter;
    };

    struct ExportManifest {
        std::string manifestId;
        std::string systemId;
        std::string systemName;
        ExportFormat format{ExportFormat::JSON};
        ExportTarget target{ExportTarget::File};
        std::string outputPath;
        std::vector<std::string> filters;
        bool includeMetadata{true};
        bool compress{false};
        int version{1};
    };

    struct ExportResult {
        std::string resultId;
        std::string manifestId;
        std::string outputPath;
        int recordsExported{0};
        long long sizeBytes{0};
        double elapsedMs{0.0};
        ExportState exportState{ExportState::Idle};
        std::vector<std::string> errors;
    };

    // Exporter registration
    bool RegisterExporter(const std::string& exporterId, const std::string& format);
    bool UnregisterExporter(const std::string& exporterId);

    // Manifest management
    std::string CreateManifest(const std::string& systemId, const std::string& systemName);
    bool RemoveManifest(const std::string& manifestId);
    const ExportManifest* GetManifest(const std::string& manifestId) const;
    std::vector<std::string> GetAllManifestIds() const;

    // Manifest configuration
    bool SetExportFormat(const std::string& manifestId, ExportFormat format);
    bool SetExportTarget(const std::string& manifestId, ExportTarget target);
    bool SetOutputPath(const std::string& manifestId, const std::string& outputPath);
    bool AddFilter(const std::string& manifestId, const ExportFilter& filter);
    bool RemoveFilter(const std::string& manifestId, const std::string& filterId);
    bool SetCompression(const std::string& manifestId, bool compress);
    bool SetMetadata(const std::string& manifestId, bool includeMetadata);

    // Export operations
    ExportResult Export(const std::string& manifestId);
    bool ExportAsync(const std::string& manifestId, const std::string& callbackId);
    bool CancelExport(const std::string& manifestId);

    // Result access
    const ExportResult* GetResult(const std::string& resultId) const;
    std::vector<std::string> GetAllResults() const;
    ExportState GetExportState(const std::string& manifestId) const;

    // Validation and introspection
    bool ValidateManifest(const std::string& manifestId) const;
    std::vector<std::string> ListFormats() const;
    std::vector<std::string> ListTargets() const;

    // Maintenance
    void ClearResults();
    void Reset();

private:
    ExportState m_state{ExportState::Idle};
    std::unordered_map<std::string, ExportManifest> m_manifests;
    std::unordered_map<std::string, ExportResult> m_results;
    std::unordered_map<std::string, ExportFilter> m_filters;
    int m_nextManifestIndex{0};
    int m_nextResultIndex{0};
};

} // namespace Atlas::Engine
