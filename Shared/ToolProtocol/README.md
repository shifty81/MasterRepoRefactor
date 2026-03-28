# Tool Protocol

This folder defines the request/response protocol used by the AtlasAI bridge.

## Transport assumptions

- Local loopback only by default (`localhost`)
- REST (HTTP) for request/response operations
- WebSocket for event streams and long-running task updates
- JSON payloads
- Named pipes as optional alternative transport (Windows)

## Request envelope

```json
{
  "protocolVersion": "1.0",
  "requestId": "<uuid>",
  "sessionId": "<uuid>",
  "service": "<ServiceName>",
  "operation": "<OperationName>",
  "timestampUtc": "<ISO8601>",
  "payload": {}
}
```

## Response envelope

```json
{
  "protocolVersion": "1.0",
  "requestId": "<uuid>",
  "success": true,
  "errorCode": null,
  "message": "<human-readable>",
  "payload": {}
}
```

## Error response

```json
{
  "protocolVersion": "1.0",
  "requestId": "<uuid>",
  "success": false,
  "errorCode": "<UPPER_SNAKE_CASE_CODE>",
  "message": "<user-safe message>",
  "payload": {
    "details": "<developer-safe details>"
  }
}
```

## Event envelope

```json
{
  "protocolVersion": "1.0",
  "eventId": "<uuid>",
  "sessionId": "<uuid>",
  "service": "<ServiceName>",
  "eventType": "<EventType>",
  "timestampUtc": "<ISO8601>",
  "payload": {}
}
```

## Dry-run behavior

Any tool action that can modify code, assets, or project state MUST default to
`dryRun: true`. The caller must explicitly set `dryRun: false` and have a valid
write-capable session token to execute mutating operations.

## Error codes

| Code | Meaning |
|------|---------|
| `UNKNOWN_ERROR` | Unexpected failure |
| `INVALID_REQUEST` | Malformed or missing required fields |
| `UNAUTHORIZED` | Missing or invalid session token |
| `UNSUPPORTED_OPERATION` | Operation not supported by backend version |
| `TIMEOUT` | Operation exceeded time limit |
| `RESOURCE_BUSY` | Requested resource is locked or in use |
| `INVALID_STATE` | Operation cannot proceed in current state |
| `NOT_FOUND` | Requested resource does not exist |
| `VALIDATION_FAILED` | Input failed validation |
| `BACKEND_UNAVAILABLE` | Bridge service is not reachable |
| `VERSION_MISMATCH` | Protocol version incompatibility |
| `OPERATION_CANCELLED` | Operation was explicitly cancelled |
