# Compliance Tools

## Files

- `compliance_scanner.py` — lightweight repo scanner for Master Repo standards

## Suggested usage

```bash
python compliance_scanner.py --repo . --out Docs/compliance_report.md
```

## Notes

This script is intentionally conservative. It is best used as:
- a first-pass audit helper
- a pre-merge check
- a refactor triage aid

Pair it with the repo docs:
- `Docs/Compliance_Rules.md`
- `Docs/Core_Runtime_Framework.md`
