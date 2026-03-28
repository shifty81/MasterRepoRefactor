# Transport and Auth Binding Specification

## Purpose
Bind bridge requests to real local transport identity instead of trusting detached request payloads.

## Windows-First Transport Targets
- named pipes for local IPC
- loopback HTTP only for optional web gateway
- no public bridge binding

## Required Controls
- connection identity bound to session issuance
- per-request nonce
- correlation id
- replay protection
- loopback enforcement for web gateway
- origin validation for browser-based access

## Required Components
```text
/Atlas/Services/Bridge/BridgeTransport/
    NamedPipeTransport.h
    NamedPipeTransport_Win.cpp
    BridgeRequestAuth.h
    BridgeRequestAuth.cpp
```

## Required Tests
- bad nonce denied
- mismatched session and connection denied
- non-loopback gateway request denied
