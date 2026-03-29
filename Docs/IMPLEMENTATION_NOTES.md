# Implementation Notes

## Immediate next steps
1. Wire real DI container registration.
2. Replace the placeholder docking host with your preferred docking framework or custom panel host.
3. Connect `EngineBridgeService` to the native Atlas runtime via named pipes or WebSocket.
4. Persist workspace layouts under a user profile path.
5. Add command palette UI and searchable command registry.
6. Add schema registry and AtlasAI task graph execution.

## Why this shape
The current repo already contains an early WPF Atlas Suite shell. This scaffold is a cleaner, more formalized build-pack that introduces:
- service contracts
- module boundaries
- plugin registration
- command bus
- job queue
- panel descriptors
- workspace layout persistence points

## Project boundaries
- `AtlasSuite.App`: UI shell, view models, WPF composition.
- `AtlasSuite.Core`: contracts, models, command/job infrastructure.
- `AtlasSuite.Modules.*`: implementation stubs for major domains.
- `AtlasSuite.Plugins.*`: extension model.
