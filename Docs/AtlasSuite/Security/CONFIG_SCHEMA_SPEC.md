# Config Schema Specification

## Purpose
Add versioning and validation to security-critical configuration.

## Required Fields
Every security config must include:
- schemaVersion
- generatedBy optional
- lastUpdatedUtc optional

## Validation Rules
At load time:
- required fields must exist
- schemaVersion must be supported
- enums must be validated
- duplicate entries must be rejected
- paths must be canonicalized
- malformed JSON must fail startup

## Files Covered
- path_policy.json
- session_capabilities.json
- tool_allowlist.json
- archive_intake_policy.json
- shipping_feature_policy.json

## Versioning Rule
Breaking schema changes must increment `schemaVersion`.

## Required Tests
- reject malformed config
- reject unsupported schemaVersion
- reject missing required field
- accept valid config
