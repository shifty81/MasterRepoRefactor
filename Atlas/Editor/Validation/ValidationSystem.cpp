// ValidationSystem.cpp
// Atlas Editor — orchestrates all data validation passes.

#include "Validation/ValidationSystem.h"

namespace atlas::editor {

bool ValidationSystem::Initialize()
{
    return true;
}

void ValidationSystem::Shutdown() {}

ValidationReport ValidationSystem::RunAll()
{
    ValidationReport report;

    auto append = [&](ValidationReport sub) {
        for (auto& issue : sub.issues)
            report.issues.push_back(std::move(issue));
    };

    append(ValidateItemReferences());
    append(ValidateModuleReferences());
    append(ValidateConfigConflicts());
    append(ValidateLootReferences());
    append(ValidateSeasonSettings());

    return report;
}

ValidationReport ValidationSystem::ValidateItemReferences()
{
    // Stub: walk item/recipe registry and report missing references.
    return {};
}

ValidationReport ValidationSystem::ValidateModuleReferences()
{
    // Stub: walk module/structure registry and report dangling socket/link refs.
    return {};
}

ValidationReport ValidationSystem::ValidateConfigConflicts()
{
    // Stub: detect duplicate IDs, schema version mismatches, etc.
    return {};
}

ValidationReport ValidationSystem::ValidateLootReferences()
{
    // Stub: verify every loot table entry refers to a known item.
    return {};
}

ValidationReport ValidationSystem::ValidateSeasonSettings()
{
    // Stub: check season / server config for range errors and missing fields.
    return {};
}

} // namespace atlas::editor
