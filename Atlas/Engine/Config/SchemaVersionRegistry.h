// SchemaVersionRegistry.h
// Atlas Engine Config — schema version checks, missing-reference detection,
// config conflict detection, and expose validation results for WPF + editor.

#pragma once
#include <cstdint>
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::config {

// ---------------------------------------------------------------------------
// Schema version entry
// ---------------------------------------------------------------------------

struct SchemaVersion
{
    std::string   schemaId;          ///< e.g. "save_data", "item_definition"
    uint32_t      majorVersion = 1;
    uint32_t      minorVersion = 0;
    uint32_t      patchVersion = 0;
    std::string   notes;
    bool          isDeprecated = false;
    std::string   migrationHint;     ///< how to upgrade from previous version
};

inline std::string FormatVersion(const SchemaVersion& v)
{
    return std::to_string(v.majorVersion) + "."
         + std::to_string(v.minorVersion) + "."
         + std::to_string(v.patchVersion);
}

// ---------------------------------------------------------------------------
// Missing reference
// ---------------------------------------------------------------------------

enum class ERefType : uint8_t
{
    Item,
    Recipe,
    Loot,
    Module,
    Structure,
    Faction,
    Mission,
    Season,
    Asset,
    Config,
};

struct MissingReference
{
    std::string   sourceId;      ///< where the reference originates
    std::string   refId;         ///< the ID that could not be resolved
    ERefType      refType       = ERefType::Item;
    std::string   detail;
    bool          isBlocking    = false;  ///< blocks runtime if unresolved
};

// ---------------------------------------------------------------------------
// Config conflict
// ---------------------------------------------------------------------------

struct ConfigConflict
{
    std::string settingKey;
    std::string valueA;
    std::string valueB;
    std::string sourceA;
    std::string sourceB;
    std::string resolution;   ///< what was chosen / how to fix
};

// ---------------------------------------------------------------------------
// Full validation report
// ---------------------------------------------------------------------------

struct ValidationReport
{
    std::string              schemaId;
    std::string              checkedVersion;
    bool                     schemaMatch      = false;
    std::vector<MissingReference> missingRefs;
    std::vector<ConfigConflict>   configConflicts;
    std::vector<std::string>      warnings;
    std::vector<std::string>      errors;
    bool                     passed  = false;

    bool HasBlockingIssues() const
    {
        for (const auto& r : missingRefs)
            if (r.isBlocking) return true;
        return !errors.empty();
    }
};

// ---------------------------------------------------------------------------
// SchemaVersionRegistry
// ---------------------------------------------------------------------------

class SchemaVersionRegistry
{
public:
    bool Initialize();
    void Shutdown();

    // ---- schema registration ------------------------------------------
    void RegisterSchema  (const SchemaVersion& sv);
    bool HasSchema       (const std::string& schemaId) const;
    std::optional<SchemaVersion> FindSchema(const std::string& schemaId) const;
    std::vector<SchemaVersion>   ListSchemas() const { return m_schemas; }
    size_t SchemaCount() const { return m_schemas.size(); }

    // ---- version checks -----------------------------------------------
    bool CheckVersion    (const std::string& schemaId,
                           uint32_t major, uint32_t minor = 0,
                           uint32_t patch = 0) const;
    bool IsCompatible    (const std::string& schemaId,
                           const std::string& versionString) const;
    bool IsDeprecated    (const std::string& schemaId) const;
    std::string GetVersionString(const std::string& schemaId) const;

    // ---- missing reference tracking -----------------------------------
    void          AddMissingRef   (const MissingReference& ref);
    void          ClearMissingRefs(const std::string& sourceId = "");
    bool          HasMissingRefs  () const { return !m_missingRefs.empty(); }
    const std::vector<MissingReference>& GetMissingRefs() const
    { return m_missingRefs; }
    std::vector<MissingReference> GetBlockingMissingRefs() const;

    // ---- config conflict detection ------------------------------------
    void   RegisterConfigValue(const std::string& key,
                                  const std::string& value,
                                  const std::string& source);
    void   DetectConfigConflicts();
    bool   HasConfigConflicts() const { return !m_conflicts.empty(); }
    const  std::vector<ConfigConflict>& GetConflicts() const
    { return m_conflicts; }

    // ---- full validation report ---------------------------------------
    ValidationReport RunValidation(const std::string& schemaId,
                                    const std::string& dataVersion) const;

    // ---- editor/WPF exposure ------------------------------------------
    /// Returns a flat string-list suitable for a list-view in WPF or editor.
    std::vector<std::string> GetValidationSummary(
        const ValidationReport& report) const;

    // ---- change callback ----------------------------------------------
    using ValidationCallback = std::function<void(const ValidationReport&)>;
    void SetValidationCallback(ValidationCallback cb)
    { m_validationCb = std::move(cb); }

    // ---- built-in game schemas ----------------------------------------
    void RegisterDefaultGameSchemas();

private:
    struct ConfigEntry { std::string key, value, source; };

    std::vector<SchemaVersion>   m_schemas;
    std::vector<MissingReference> m_missingRefs;
    std::vector<ConfigConflict>  m_conflicts;
    std::vector<ConfigEntry>     m_configValues;
    ValidationCallback           m_validationCb;
};

} // namespace atlas::config
