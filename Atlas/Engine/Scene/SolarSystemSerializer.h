#pragma once
#include <string>
#include <vector>
#include <functional>

namespace Atlas::Engine {

/// Phase 21C — Serializes and deserializes solar system data to/from JSON
/// for persistence, network sync, and AI analysis.
class SolarSystemSerializer {
public:
    struct SerializedSystem {
        std::string systemId;
        std::string json;
        int version{1};
        bool valid{false};
    };

    // Serialize a registered system to JSON string
    SerializedSystem Serialize(const std::string& systemId) const;

    // Deserialize JSON back to a system ID usable with SolarSystemRegistry
    std::string Deserialize(const std::string& json,
                            bool registerToRegistry = true) const;

    // File I/O
    bool SaveToFile(const std::string& systemId, const std::string& filePath) const;
    bool LoadFromFile(const std::string& filePath,
                      bool registerToRegistry = true) const;

    // Batch operations
    int SaveAll(const std::string& directoryPath) const;
    int LoadAll(const std::string& directoryPath,
                bool registerToRegistry = true) const;

    // Validation
    bool ValidateJson(const std::string& json) const;
    std::string GetLastError() const { return m_lastError; }

    // Format upgrade
    std::string UpgradeToLatest(const std::string& json,
                                int fromVersion, int toVersion) const;
    int GetCurrentVersion() const { return m_currentVersion; }

    // Callbacks
    void SetOnSerializedCallback(
        std::function<void(const std::string&)> cb);
    void SetOnDeserializedCallback(
        std::function<void(const std::string&)> cb);

private:
    mutable std::string m_lastError;
    int m_currentVersion{1};
    std::function<void(const std::string&)> m_onSerialized;
    std::function<void(const std::string&)> m_onDeserialized;
};

} // namespace Atlas::Engine
