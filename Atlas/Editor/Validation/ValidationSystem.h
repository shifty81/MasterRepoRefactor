// ValidationSystem.h
// Atlas Editor — orchestrates all data validation passes.

#pragma once
#include "Validation/ValidationTypes.h"

namespace atlas::editor {

/// Runs validation passes against the active project data and returns a report.
class ValidationSystem
{
public:
    bool Initialize();
    void Shutdown();

    /// Run every registered validation pass and return the combined report.
    ValidationReport RunAll();

    /// Run only item/recipe reference checks.
    ValidationReport ValidateItemReferences();

    /// Run only module/structure reference checks.
    ValidationReport ValidateModuleReferences();

    /// Run config conflict checks.
    ValidationReport ValidateConfigConflicts();

    /// Run loot table reference checks.
    ValidationReport ValidateLootReferences();

    /// Run season / server settings checks.
    ValidationReport ValidateSeasonSettings();
};

} // namespace atlas::editor
