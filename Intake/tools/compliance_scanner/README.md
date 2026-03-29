# Compliance Scanner

This utility compares a repo against the project standard and emits `PASS`, `WARN`, and `FAIL` results.

## Checks included
- required top-level directories
- required config JSON files
- duplicate domain paths
- banned token scan
- per-area README coverage warnings
- docs pack completeness

## Typical use

```bash
python scan_compliance.py --repo /path/to/MasterRepo --docs /path/to/SplitDocsPack
```
