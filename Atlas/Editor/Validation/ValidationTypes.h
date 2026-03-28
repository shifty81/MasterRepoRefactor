// ValidationTypes.h
// Atlas Editor — shared types for the data validation toolkit.

#pragma once
#include <string>
#include <vector>

namespace atlas::editor {

enum class EValidationSeverity : uint8_t
{
    Info,
    Warning,
    Error
};

struct ValidationIssue
{
    EValidationSeverity severity    = EValidationSeverity::Error;
    std::string         category;   ///< e.g. "Item", "Recipe", "Module"
    std::string         assetId;    ///< ID of the offending asset or file
    std::string         message;    ///< Human-readable description
    std::string         suggestion; ///< Optional fix hint
};

struct ValidationReport
{
    std::vector<ValidationIssue> issues;

    bool HasErrors() const
    {
        for (const auto& i : issues)
            if (i.severity == EValidationSeverity::Error) return true;
        return false;
    }

    bool HasWarnings() const
    {
        for (const auto& i : issues)
            if (i.severity == EValidationSeverity::Warning) return true;
        return false;
    }

    size_t ErrorCount() const
    {
        size_t n = 0;
        for (const auto& i : issues)
            if (i.severity == EValidationSeverity::Error) ++n;
        return n;
    }

    size_t WarningCount() const
    {
        size_t n = 0;
        for (const auto& i : issues)
            if (i.severity == EValidationSeverity::Warning) ++n;
        return n;
    }
};

} // namespace atlas::editor
