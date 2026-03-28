# Audit Chain Specification

## Purpose
Make audit logs tamper-evident.

## Required Model
Each audit record must include:
- timestampUtc
- eventType
- payload
- prevHash
- recordHash
- correlationId

## Hashing Rule
- canonicalize record payload
- compute `recordHash = SHA-256(prevHash + canonicalPayload)`
- persist `prevHash` and `recordHash` with each record

## Required File Structure
```text
%LOCALAPPDATA%/AtlasSuite/Audit/
    2026-03-28.audit.jsonl
    2026-03-29.audit.jsonl
```

## Verification Requirements
A verification tool must:
- read the full file in order
- recompute each record hash
- fail on edit, insertion, deletion, or reordering

## Required Tooling
```text
/Tools/Audit/VerifyAuditChain.ps1
```

## Required Tests
- valid chain verifies
- edited record fails verification
- deleted middle record fails verification
