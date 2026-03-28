# Project Manifests

This folder contains project manifest files that define project identity, capabilities,
build targets, and bridge configuration for AtlasAI integration.

## Files

- `novaforge.project.json` — manifest for the NovaForge game project

## Format

Each manifest is a JSON file with the following top-level sections:

- `project` — identity and version information
- `capabilities` — supported operations and feature flags
- `buildTargets` — available build configurations
- `bridge` — transport settings for AtlasAI bridge connection
- `repoPaths` — root paths for code, data, content, and docs
- `safetySettings` — action whitelist and trust configuration
