# Integration Notes

## 1. Session wiring
Create sessions inside Atlas Suite startup or your local login flow:
- observer for read-only dashboards
- editor for tooling mutations
- admin_local for owner-only flows

## 2. Path policy
Load `Config/Security/path_policy.json` at startup, then refuse to start the bridge if the policy fails to load.

## 3. Bridge transport
`BridgeService` is transport-agnostic. Wrap `Handle()` behind:
- named pipes
- loopback HTTP
- local websocket

Do not expose it directly to LAN.

## 4. Command execution
`CommandBroker` currently blocks live execution on purpose. That keeps the scaffold safe. Replace the final branch in `CommandBroker::Execute()` with your platform launcher after the rest of the policy enforcement is stable.

## 5. Archive intake hook
Call the archive intake pipeline:
- on Atlas Suite startup
- on explicit “Audit Root Drops” button
- after sync/import tasks finish

## 6. Shipping isolation
Do not compile this module into shipping builds.
