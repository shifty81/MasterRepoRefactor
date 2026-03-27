# Arbiter Bridge

## Overview

The Arbiter bridge connects the Arbiter AI tooling shell (C# / WPF) to the
NovaForge/Atlas native backend (C++).

The bridge is intentionally kept narrow. It defines a stable, versioned protocol
so that the WPF layer and the native backend can evolve independently.

## Transport model

- **REST (HTTP)** on `localhost` for request/response operations
- **WebSocket** on `localhost` for event streams and long-running task updates
- **Named pipes** as optional alternative for Windows-only low-latency use cases
- All transports bind to loopback only by default

Default ports (from `novaforge.project.json`):

| Transport | Port |
|-----------|------|
| REST | 57100 |
| WebSocket | 57101 |

## Request / response model

See `Shared/ToolProtocol/README.md` for the full envelope specification.

All requests include:
- `protocolVersion`
- `requestId` (UUID)
- `sessionId` (UUID)
- `service` name
- `operation` name
- `timestampUtc`
- `payload`

## Whitelisted tool actions

Only these actions may be triggered via the bridge:

| Action | Description |
|--------|-------------|
| `ValidateData` | Validate game data against schemas |
| `RunPCGPreview` | Run a procedural generation preview |
| `OpenScene` | Open a named scene in the editor |
| `FocusEntity` | Focus the editor camera on an entity |
| `RegenerateSchemas` | Regenerate data validation schemas |

Any action not in this list returns `UNSUPPORTED_OPERATION`.

## Read-only vs write actions

| Category | Examples | Requires write session |
|----------|----------|----------------------|
| Read | `GetProjectInfo`, `GetEditorSelection` | No |
| Write | `RunBuild`, `RunToolAction` (non-dry-run) | Yes |

## Dry-run behavior

All tool actions default to `dryRun: true`. The caller must explicitly set
`dryRun: false` and present a valid write-capable session token to execute
any mutating operation.

## Editor-only vs runtime-safe behavior

| Operation | Editor-only | Runtime-safe |
|-----------|-------------|--------------|
| `GetProjectInfo` | No | Yes |
| `GetEditorSelection` | Yes | No |
| `RunBuild` | Yes | No |
| `OpenScene` | Yes | No |
| `ValidateData` | No | Yes |

Editor-only operations must not be invoked when the editor is not running.
The bridge service should return `INVALID_STATE` in that case.

## Local trust / approval rules

1. The bridge binds to loopback only.
2. A session token is generated during handshake.
3. Write operations require a valid session token.
4. Mutating tool actions require explicit `dryRun: false` from the caller.
5. Future: editor-side approval gate for high-risk operations.
