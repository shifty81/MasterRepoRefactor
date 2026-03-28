# Archive Deep Inspection Specification

## Purpose
Turn archive intake from extension-only classification into a real quarantine analysis pipeline.

## Required Inspection Layers
For every intake file:
- extension classification
- binary signature or MIME detection
- SHA-256 hashing
- duplicate archive history lookup
- secret scanning
- executable detection
- donor repo fingerprinting

For zip files:
- entry inventory
- nested archive detection
- executable/script detection
- extracted tree manifest
- quarantine-only extraction

## Classification Outcomes
- archived_only
- promote_candidate
- donor_repo_candidate
- reject_executable
- reject_secret_exposure
- needs_review

## Required Outputs
- archive_intake_manifest.json
- archive_audit_report.md
- quarantine inventory JSON
- extracted tree manifest JSON

## Required Tests
- nested zip flagged
- executable intake flagged
- secret-like token flagged
- duplicate file detected
