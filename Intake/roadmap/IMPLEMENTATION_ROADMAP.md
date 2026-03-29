# Implementation Roadmap

## Goal

Add a clean, maintainable docs layer for the entire project without blocking code work.

## Phase 1 — Drop-in docs pack
- add this pack under `Docs/SplitPack/` or merge into your preferred docs structure
- keep links relative and repo-local
- review system ownership names

## Phase 2 — Arbiter doc generation
- point the generator at repo JSON/config/data files
- generate schema reference docs into a target folder
- optionally wire it into a build or pre-commit step

## Phase 3 — Compliance enforcement
- run the scanner in CI or local scripts
- start with warnings
- promote important checks to failures later

## Phase 4 — Expand rules
Recommended next checks:
- banned legacy naming
- duplicate domain directories
- missing README/doc coverage per module
- undocumented JSON data files
- TODO/FIXME density
- orphaned archive migrations

## Suggested landing paths
- docs: `Docs/SplitPack/`
- generator: `Scripts/arbiter_doc_generator.py` or `Tools/ArbiterDocGenerator/`
- scanner: `Scripts/compliance_scan.py` or `Tools/ComplianceScanner/`
