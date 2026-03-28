# Tool Protocol

See `Shared/ToolProtocol/README.md` for the full protocol specification.

## Quick reference

### MVP service endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/session/connect` | POST | Establish a bridge session (returns session token) |
| `/session/disconnect` | POST | Revoke the current session |
| `/project/info` | GET | Get project identity and capabilities |
| `/editor/selection` | GET | Get current editor selection snapshot |
| `/build/run` | POST | Queue a build target |
| `/editor/tools/run` | POST | Run a whitelisted tool action |

### MVP event types

| Event | Service | Description |
|-------|---------|-------------|
| `BackendConnected` | SessionService | Bridge connected |
| `BackendDisconnected` | SessionService | Bridge disconnected |
| `BuildProgress` | BuildService | Build progress update |
| `BuildCompleted` | BuildService | Build finished |
| `BuildFailed` | BuildService | Build failed |
| `LogOutput` | TelemetryService | Log line from backend |

---

## Endpoint details

### POST `/session/connect`

Establishes a new bridge session. Must be called before any other endpoint.

**Request payload:**
```json
{
  "protocolVersion": "1.0",
  "clientVersion": "0.1.0",
  "projectId": "novaforge"
}
```

**Response payload (inside envelope):**
```json
{
  "sessionToken": "<opaque-uuid>",
  "serverVersion": "1.0",
  "projectId": "novaforge",
  "writeEnabled": false
}
```

The returned `sessionToken` must be included in the `sessionId` field of all
subsequent request envelopes.

**Error cases:**
- `VERSION_MISMATCH` — protocol version not supported by backend

---

### POST `/session/disconnect`

Revokes the current session token. All subsequent calls with that token will
return `UNAUTHORIZED`.

---

### GET `/project/info`

Returns static project identity and capability flags.

**Response payload:**
```json
{
  "projectId": "novaforge",
  "displayName": "NovaForge",
  "version": "0.1.0",
  "repoRoot": "/path/to/repo",
  "capabilities": {
    "supportsViewportAttach": false,
    "supportsLivePatch": false,
    "supportsAISession": true,
    "supportsProjectIndexing": true,
    "supportsMultiWorkspace": false
  }
}
```

**Requires:** valid session token  
**Write authorization:** no

---

### GET `/editor/selection`

Returns the current editor selection state.

**Response payload:**
```json
{
  "activeScene": "SectorAlpha",
  "selectedObjectName": "Station_01",
  "selectedObjectType": "StationEntity",
  "selectedObjectId": 42
}
```

**Requires:** valid session token  
**Write authorization:** no  
**Editor-only:** yes — returns `INVALID_STATE` when editor is not running

---

### POST `/build/run`

Queues a build target. Returns a `buildId` for progress tracking.

**Request payload:**
```json
{
  "target": "AtlasEditor",
  "configuration": "Debug",
  "platform": "Win64",
  "rebuild": false
}
```

**Response payload:**
```json
{
  "buildId": "build-1",
  "outputLog": "Build queued for target 'AtlasEditor'"
}
```

**Requires:** valid session token  
**Write authorization:** yes (mutating operation)

---

### POST `/editor/tools/run`

Runs one of the whitelisted tool actions.

**Request payload:**
```json
{
  "action": "ValidateData",
  "parameter": "",
  "dryRun": true
}
```

**Response payload:**
```json
{
  "wasDryRun": true,
  "summary": "dry-run completed"
}
```

**Allowed `action` values:**
- `ValidateData`
- `RunPCGPreview`
- `OpenScene`
- `FocusEntity`
- `RegenerateSchemas`

**Requires:** valid session token  
**Write authorization:** required when `dryRun: false`

---

## Safety and audit

Every bridge operation is written to the audit log with:
- UTC timestamp
- request ID
- session ID
- service and operation names
- success/failure
- dry-run flag
- summary / fail reason

See `BridgeAuditLogger.h` for the in-process audit log API.

---

## Version negotiation

On first connection, AtlasAI sends a handshake request to `/session/connect`:

```json
{
  "protocolVersion": "1.0",
  "clientVersion": "0.1.0",
  "projectId": "novaforge"
}
```

The backend responds with capabilities and supported protocol version.
If `protocolVersion` does not match the server's supported version, the
response returns `VERSION_MISMATCH` and no session token is issued.

---

## Failure and rollback

| Scenario | Behavior |
|----------|----------|
| Invalid session token | `UNAUTHORIZED` — no operation is attempted |
| Non-dry-run without write auth | `UNAUTHORIZED` — no mutation occurs |
| Action not in whitelist | `UNSUPPORTED_OPERATION` — rejected before dispatch |
| Service not running | `BACKEND_UNAVAILABLE` — no state changed |
| Build fails | `exitCode != 0` in `BuildResult.outputLog`; session remains active |
| Partial tool failure | Returns `UNKNOWN_ERROR` with details in `summary`; no rollback |

All mutating operations must be re-requested if they fail. The bridge does not
perform automatic retries or rollback.
