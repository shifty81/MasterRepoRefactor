# Project Manifest Specification

## Purpose

The project manifest is the single source of truth for how Arbiter connects to
and interacts with a game project in MasterRepo.

## Location

```
Shared/ProjectManifests/<project-id>.project.json
```

## Schema version

Current schema version: `1.0`

## Top-level sections

### `project`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique project identifier |
| `displayName` | string | Human-readable project name |
| `version` | string | Project version (semver) |
| `description` | string | Short project description |
| `repoRoot` | string | Relative path from manifest to repo root |

### `capabilities`

| Flag | Type | Description |
|------|------|-------------|
| `supportsViewportAttach` | bool | Native viewport can be embedded in WPF |
| `supportsLivePatch` | bool | Hot-patch code changes supported |
| `supportsAISession` | bool | AI sessions can be created |
| `supportsProjectIndexing` | bool | Repo can be indexed for AI |
| `supportsMultiWorkspace` | bool | Multiple workspaces supported |

### `buildTargets`

Array of build target objects:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | CMake target name |
| `displayName` | string | UI display name |
| `configuration` | string | `Debug`, `Release`, `Shipping` |
| `platform` | string | `Win64`, `Linux`, `macOS` |

### `bridge`

| Field | Type | Description |
|-------|------|-------------|
| `transport` | string | Transport type (`rest+websocket`, `namedpipe`) |
| `host` | string | Bind host (must be `localhost` for security) |
| `restPort` | int | REST API port |
| `wsPort` | int | WebSocket event stream port |
| `timeoutSeconds` | int | Default operation timeout |
| `bindLoopbackOnly` | bool | Restrict to loopback (must be true) |

### `repoPaths`

Paths relative to repo root for each major area.

### `safetySettings`

| Field | Type | Description |
|-------|------|-------------|
| `requireDryRunByDefault` | bool | Tool actions default to dry-run |
| `requireSessionTokenForWrites` | bool | Write ops require session token |
| `allowedToolActions` | string[] | Whitelist of permitted tool actions |
| `writeableRoots` | string[] | Paths Arbiter may write to |
