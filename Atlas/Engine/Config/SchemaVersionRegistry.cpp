// SchemaVersionRegistry.cpp
// Atlas Engine Config — schema version registry.

#include "Config/SchemaVersionRegistry.h"

#include <algorithm>
#include <sstream>

namespace atlas::config {

bool SchemaVersionRegistry::Initialize() { return true; }
void SchemaVersionRegistry::Shutdown()
{
    m_schemas.clear();
    m_missingRefs.clear();
    m_conflicts.clear();
    m_configValues.clear();
}

void SchemaVersionRegistry::RegisterSchema(const SchemaVersion& sv)
{
    for (auto& s : m_schemas)
        if (s.schemaId == sv.schemaId) { s = sv; return; }
    m_schemas.push_back(sv);
}

bool SchemaVersionRegistry::HasSchema(const std::string& schemaId) const
{
    return FindSchema(schemaId).has_value();
}

std::optional<SchemaVersion> SchemaVersionRegistry::FindSchema(
    const std::string& schemaId) const
{
    for (const auto& s : m_schemas)
        if (s.schemaId == schemaId) return s;
    return std::nullopt;
}

bool SchemaVersionRegistry::CheckVersion(const std::string& schemaId,
                                           uint32_t major, uint32_t minor,
                                           uint32_t patch) const
{
    auto s = FindSchema(schemaId);
    if (!s) return false;
    return s->majorVersion == major &&
           s->minorVersion >= minor &&
           (s->minorVersion > minor || s->patchVersion >= patch);
}

bool SchemaVersionRegistry::IsCompatible(const std::string& schemaId,
                                           const std::string& versionString) const
{
    // Parse "major.minor.patch" from string.
    uint32_t major = 0, minor = 0, patch = 0;
    char sep;
    std::istringstream ss(versionString);
    ss >> major >> sep >> minor >> sep >> patch;
    return CheckVersion(schemaId, major, minor, patch);
}

bool SchemaVersionRegistry::IsDeprecated(const std::string& schemaId) const
{
    auto s = FindSchema(schemaId);
    return s && s->isDeprecated;
}

std::string SchemaVersionRegistry::GetVersionString(
    const std::string& schemaId) const
{
    auto s = FindSchema(schemaId);
    if (!s) return "0.0.0";
    return FormatVersion(*s);
}

void SchemaVersionRegistry::AddMissingRef(const MissingReference& ref)
{
    m_missingRefs.push_back(ref);
}

void SchemaVersionRegistry::ClearMissingRefs(const std::string& sourceId)
{
    if (sourceId.empty()) { m_missingRefs.clear(); return; }
    m_missingRefs.erase(
        std::remove_if(m_missingRefs.begin(), m_missingRefs.end(),
                       [&](const MissingReference& r){ return r.sourceId == sourceId; }),
        m_missingRefs.end());
}

std::vector<MissingReference>
SchemaVersionRegistry::GetBlockingMissingRefs() const
{
    std::vector<MissingReference> result;
    for (const auto& r : m_missingRefs)
        if (r.isBlocking) result.push_back(r);
    return result;
}

void SchemaVersionRegistry::RegisterConfigValue(const std::string& key,
                                                  const std::string& value,
                                                  const std::string& source)
{
    m_configValues.push_back({ key, value, source });
}

void SchemaVersionRegistry::DetectConfigConflicts()
{
    m_conflicts.clear();
    for (size_t i = 0; i < m_configValues.size(); ++i)
    {
        for (size_t j = i + 1; j < m_configValues.size(); ++j)
        {
            if (m_configValues[i].key  == m_configValues[j].key &&
                m_configValues[i].value != m_configValues[j].value)
            {
                ConfigConflict c;
                c.settingKey  = m_configValues[i].key;
                c.valueA      = m_configValues[i].value;
                c.valueB      = m_configValues[j].value;
                c.sourceA     = m_configValues[i].source;
                c.sourceB     = m_configValues[j].source;
                c.resolution  = "Use value from " + c.sourceA + " (first defined)";
                m_conflicts.push_back(c);
            }
        }
    }
}

ValidationReport SchemaVersionRegistry::RunValidation(
    const std::string& schemaId,
    const std::string& dataVersion) const
{
    ValidationReport report;
    report.schemaId        = schemaId;
    report.checkedVersion  = dataVersion;
    report.schemaMatch     = IsCompatible(schemaId, dataVersion);

    if (!report.schemaMatch)
    {
        std::string current = GetVersionString(schemaId);
        report.errors.push_back(
            "Schema version mismatch for '" + schemaId + "': "
            "data=" + dataVersion + " registry=" + current);
    }

    if (IsDeprecated(schemaId))
        report.warnings.push_back("Schema '" + schemaId + "' is deprecated");

    // Include missing refs.
    report.missingRefs = m_missingRefs;
    if (!m_missingRefs.empty())
        report.warnings.push_back(
            std::to_string(m_missingRefs.size()) + " missing reference(s)");

    // Include conflicts.
    report.configConflicts = m_conflicts;
    for (const auto& c : m_conflicts)
        report.warnings.push_back("Config conflict: " + c.settingKey);

    report.passed = report.errors.empty() && !report.HasBlockingIssues();

    if (m_validationCb) m_validationCb(report);
    return report;
}

std::vector<std::string> SchemaVersionRegistry::GetValidationSummary(
    const ValidationReport& report) const
{
    std::vector<std::string> lines;
    lines.push_back("[Schema] " + report.schemaId + " v" + report.checkedVersion
                    + (report.schemaMatch ? " OK" : " MISMATCH"));
    for (const auto& e : report.errors)
        lines.push_back("[ERROR] " + e);
    for (const auto& w : report.warnings)
        lines.push_back("[WARN]  " + w);
    for (const auto& r : report.missingRefs)
        lines.push_back("[MISREF] " + r.sourceId + " → " + r.refId
                        + (r.isBlocking ? " [BLOCKING]" : ""));
    for (const auto& c : report.configConflicts)
        lines.push_back("[CONFLICT] " + c.settingKey + ": " + c.valueA
                        + " vs " + c.valueB);
    lines.push_back("[RESULT] " + std::string(report.passed ? "PASSED" : "FAILED"));
    return lines;
}

void SchemaVersionRegistry::RegisterDefaultGameSchemas()
{
    auto reg = [this](const char* id, uint32_t maj, uint32_t min,
                       uint32_t pat = 0, const char* notes = "")
    {
        SchemaVersion sv;
        sv.schemaId      = id;
        sv.majorVersion  = maj;
        sv.minorVersion  = min;
        sv.patchVersion  = pat;
        sv.notes         = notes;
        RegisterSchema(sv);
    };

    reg("save_data",         1, 0, 0, "World save envelope");
    reg("player_state",      1, 0, 0, "Player controller snapshot");
    reg("fleet_data",        1, 0, 0, "Fleet + ship definitions");
    reg("season_data",       1, 0, 0, "Titan race + season state");
    reg("economy_data",      1, 0, 0, "Credits, contracts, standings");
    reg("item_definition",   1, 0, 0, "Item/recipe data records");
    reg("voxel_chunk",       1, 0, 0, "Voxel chunk serialisation");
    reg("structure_def",     1, 0, 0, "Module/structure definitions");
    reg("faction_def",       1, 0, 0, "Faction and standing records");
    reg("mission_def",       1, 0, 0, "Mission/contract definitions");
    reg("pcg_seed_table",    1, 0, 0, "PCG seed registry snapshot");
    reg("keybind_config",    1, 0, 0, "Player keybind overrides");
    reg("asset_import_rules",1, 0, 0, "Asset naming/import rules");
}

} // namespace atlas::config
