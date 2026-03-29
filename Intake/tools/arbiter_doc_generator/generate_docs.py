#!/usr/bin/env python3
import argparse
import json
import os
from collections import defaultdict

def infer_type(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__

def walk_schema(value, prefix="", rows=None):
    if rows is None:
        rows = []

    value_type = infer_type(value)
    sample = value
    if isinstance(sample, (dict, list)):
        sample_repr = f"{value_type} ({len(sample)})"
    else:
        sample_repr = repr(sample)

    rows.append((prefix or "$", value_type, sample_repr))

    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            walk_schema(child, child_prefix, rows)
    elif isinstance(value, list) and value:
        first = value[0]
        child_prefix = f"{prefix}[]" if prefix else "$[]"
        walk_schema(first, child_prefix, rows)

    return rows

def write_markdown(src_rel, data, out_dir):
    rows = walk_schema(data)
    title = src_rel.replace(os.sep, "/")
    lines = [
        f"# Schema Reference: `{title}`",
        "",
        "## Overview",
        "",
        f"- Source: `{title}`",
        f"- Root type: `{infer_type(data)}`",
        "",
        "## Key Map",
        "",
        "| Path | Type | Sample |",
        "|---|---|---|",
    ]
    for path, t, sample in rows:
        sample_txt = str(sample).replace("|", "\\|").replace("\n", " ")
        if len(sample_txt) > 120:
            sample_txt = sample_txt[:117] + "..."
        lines.append(f"| `{path}` | `{t}` | `{sample_txt}` |")

    dest = os.path.join(out_dir, title.replace("/", "__") + ".md")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return dest

def main():
    parser = argparse.ArgumentParser(description="Generate Markdown schema docs from repo JSON files.")
    parser.add_argument("--repo", required=True, help="Path to repo root")
    parser.add_argument("--out", required=True, help="Output directory for generated docs")
    args = parser.parse_args()

    generated = []
    for dp, _, fns in os.walk(args.repo):
        for fn in sorted(fns):
            if not fn.lower().endswith(".json"):
                continue
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, args.repo)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as exc:
                print(f"[WARN] skipped {rel}: {exc}")
                continue
            generated.append((rel, write_markdown(rel, data, args.out)))

    index_path = os.path.join(args.out, "INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# Generated Schema Docs\n\n")
        for rel, dest in generated:
            name = os.path.basename(dest)
            f.write(f"- [{rel}](./{name})\n")
    print(f"Generated {len(generated)} schema docs into {args.out}")

if __name__ == "__main__":
    main()
