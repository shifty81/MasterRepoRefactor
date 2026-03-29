# Arbiter Auto-Doc Generator

This utility scans JSON-backed config/data files and generates Markdown schema reference docs.

## What it does
- walks the repo
- finds `.json` files
- infers key paths and value types
- writes one Markdown file per JSON source
- builds an index page linking all generated docs

## Typical use

```bash
python generate_docs.py --repo /path/to/MasterRepo --out /path/to/output/generated
```

## Suggested integration
- run locally after config/schema edits
- optionally run in CI to keep schema docs fresh
- link the generated output from your main docs index
