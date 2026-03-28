# Secret Redaction Specification

## Purpose
Prevent secrets from leaking into audit logs, archive reports, config diagnostics, or AI-visible summaries.

## Scan Targets
- archive intake
- bridge request bodies
- audit payloads
- AI-readable summaries
- config diagnostics

## Minimum Pattern Set
- bearer tokens
- API keys
- private key headers
- connection strings
- credential JSON blocks

## Redaction Rule
Never persist the full secret value to logs or reports.

Store only:
- pattern type
- severity
- source location
- redacted preview

## Required Service API
```cpp
struct RedactionHit
{
    std::string patternType;
    std::string severity;
    std::string location;
    std::string redactedPreview;
};
```

## Required Tests
- API key is redacted
- private key block is redacted
- redacted preview preserves enough context for debugging
