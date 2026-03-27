# Tool Protocol

See `Shared/ToolProtocol/README.md` for the full protocol specification.

## Quick reference

### MVP service endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
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

### Version negotiation

On first connection, Arbiter sends a handshake request to `/session/connect`:

```json
{
  "protocolVersion": "1.0",
  "clientVersion": "0.1.0",
  "projectId": "novaforge"
}
```

The backend responds with capabilities and supported protocol version.
