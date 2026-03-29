#!/usr/bin/env python3
"""
Arbiter Auto-Doc Generator
Turns JSON schemas into repo-ready Markdown docs.

Usage:
    python autodoc_generator.py --schemas ./Data/Schemas --out ./Docs/Generated
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def md_escape(text: str) -> str:
    return text.replace("|", r"\|")

def describe_value(value: Any, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            lines.append(f"{pad}- **{k}**: {type(v).__name__}")
            lines.append(describe_value(v, indent + 1))
        return "\n".join(line for line in lines if line.strip())
    if isinstance(value, list):
        if not value:
            return f"{pad}- empty list"
        first = value[0]
        return f"{pad}- list of {type(first).__name__}"
    return f"{pad}- example: `{value}`"

def schema_to_markdown(path: Path, data: Any) -> str:
    title = data.get("schema") or data.get("id") or path.stem
    lines = [
        f"# {title}",
        "",
        f"Source file: `{path.name}`",
        "",
    ]
    if isinstance(data, dict):
        if "display_name" in data:
            lines += [f"**Display name:** {data['display_name']}", ""]
        if "version" in data:
            lines += [f"**Version:** {data['version']}", ""]
        lines += ["## Top-level fields", ""]
        for key, value in data.items():
            typename = type(value).__name__
            lines.append(f"- **{key}** ({typename})")
        lines += ["", "## Structure notes", "", describe_value(data), ""]
        lines += ["## Raw example", "", "```json", json.dumps(data, indent=2), "```", ""]
    else:
        lines += ["```json", json.dumps(data, indent=2), "```", ""]
    return "\n".join(lines)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schemas", required=True, help="Directory containing JSON schema/example files")
    parser.add_argument("--out", required=True, help="Directory to write Markdown docs into")
    args = parser.parse_args()

    schemas_dir = Path(args.schemas)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(list(schemas_dir.rglob("*.json")))
    index_lines = ["# Generated Schema Docs", ""]
    for file in files:
        try:
            data = load_json(file)
            md = schema_to_markdown(file, data)
            out_file = out_dir / f"{file.stem}.md"
            out_file.write_text(md, encoding="utf-8")
            index_lines.append(f"- [{file.stem}]({out_file.name})")
        except Exception as exc:
            err_file = out_dir / f"{file.stem}.error.md"
            err_file.write_text(f"# Error processing {file.name}\n\n`{exc}`\n", encoding="utf-8")
            index_lines.append(f"- {file.stem} (error)")
    (out_dir / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
