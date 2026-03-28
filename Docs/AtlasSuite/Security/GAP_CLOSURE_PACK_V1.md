# Gap Closure Pack v1

## Purpose
This pack closes the highest-risk gaps in the current platform hardening scaffold for Atlas Suite, AtlasAI, and NovaForge.

It is focused on converting the current implementation from a strong bootstrap into a trustworthy platform core.

## Objectives
- make path enforcement canonical and repo-anchored
- replace boolean approval with a real reviewed patch pipeline
- upgrade the command broker into a real execution enforcement layer
- replace weak archive hashing with SHA-256
- make core services thread-safe
- make audit logs tamper-evident
- add config schema versioning and validation
- deepen archive intake inspection
- bind bridge auth to real local transport identity
- add secret scanning and redaction

## Priority Tiers

### Tier 1 — Critical
1. Canonical path enforcement
2. Reviewed patch pipeline
3. Real command execution broker
4. SHA-256 archive hashing
5. Thread safety

### Tier 2 — Important
6. Tamper-evident audit chain
7. Config schema validation and versioning
8. Archive deep inspection
9. Transport and auth binding
10. Secret redaction and secret scanning

### Tier 3 — Finishing Layer
11. Finer capability granularity
12. Windows-first hardening hooks
13. Shipping isolation wiring
14. Expanded negative-path tests
15. Final Atlas tree merge

## Required Repo Targets
```text
/Docs/AtlasSuite/Security/
    GAP_CLOSURE_PACK_V1.md
    PATH_CANONICALIZATION_SPEC.md
    PATCH_REVIEW_SPEC.md
    COMMAND_BROKER_EXECUTION_SPEC.md
    AUDIT_CHAIN_SPEC.md
    CONFIG_SCHEMA_SPEC.md
    ARCHIVE_DEEP_INSPECTION_SPEC.md
    TRANSPORT_AUTH_BINDING_SPEC.md
    SECRET_REDACTION_SPEC.md

/Config/Security/Schemas/
    path_policy.schema.json
    session_capabilities.schema.json
    tool_allowlist.schema.json
    archive_intake_policy.schema.json
    shipping_feature_policy.schema.json

/Atlas/Services/Security/
    PathPolicyService/
    PatchReviewService/
    CommandBroker/
    AuditEventWriter/
    ConfigValidation/
    Redaction/

/Atlas/Services/Archive/
    ArchiveIntakeService/

/Atlas/Services/Bridge/
    BridgeTransport/

/Tests/
    Security/
    Archive/
    Bridge/
    BuildVerification/
```

## Recommended Implementation Order

### Phase A
- repo cleanup
- canonical path enforcement
- thread safety
- SHA-256 hashing
- config validation

### Phase B
- reviewed patch pipeline
- real command broker
- audit chain
- secret redaction

### Phase C
- archive deep inspection
- transport binding
- Windows-first hardening
- shipping integration
- expanded tests

## Acceptance Standard
The pack is complete only when:
- protected root writes require a reviewed patch artifact
- all path decisions are made on canonical repo-anchored paths
- every approved tool launch is validated, bounded, and audited
- archive intake uses SHA-256 and quarantine inventory
- audit files are chain-verifiable
- malformed config is rejected before service startup
- secrets are redacted before logs or reports are written
