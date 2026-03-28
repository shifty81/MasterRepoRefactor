# AtlasBridgeContract

This module defines the shared C++ contract types for the AtlasAI ↔ NovaForge bridge.

## Purpose

Provides a stable, versioned interface between:

- `AtlasAI` — AI tooling shell (C# / WPF)
- `NovaForge` — native C++ game and engine backend

## Contents

### `include/AtlasBridgeTypes.h`

Defines all cross-boundary data types:

- `ProtocolVersion` — version negotiation
- `BridgeResult` / `BridgeErrorCode` — common result model
- `ProjectInfo` / `ProjectCapabilities` — project identity and feature flags
- `BuildTarget` / `BuildResult` — build request and result types
- `EditorSelectionSnapshot` — editor state snapshot
- `OpenFileRequest` — file open request
- `ToolActionRequest` / `ToolActionResult` — whitelisted tool action types

## Rules

- No WPF types
- No gameplay types
- No engine internals
- No service-specific logic
- Plain C++ data structures only
- Standard library types only (`std::string`, `std::vector`, etc.)
