#!/usr/bin/env python3
"""
Master Repo Compliance Scanner

Scans a repo against lightweight Master Repo standards.

Usage:
    python compliance_scanner.py --repo /path/to/repo --out compliance_report.md
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from typing import List, Dict

RULES = {
    "direct_input_calls": {
        "patterns": [r"\bGetAsyncKeyState\b", r"\bglfwGetKey\b", r"\bIsKeyDown\b", r"\bOnKeyDown\b"],
        "severity": "warning",
        "message": "Direct input handling found; prefer centralized input context routing.",
    },
    "hardcoded_season": {
        "patterns": [r"season.*=.*\d+", r"SeasonLength.*=.*\d+"],
        "severity": "warning",
        "message": "Possible hardcoded season value; prefer config-driven settings.",
    },
    "generic_suit_term": {
        "patterns": [r"\bplayer suit\b", r"\bsuit system\b"],
        "severity": "info",
        "message": "Prefer in-game terminology: rig.",
    },
    "missing_debug_hook_hint": {
        "patterns": [],
        "severity": "info",
        "message": "Major runtime systems should expose debug info providers or overlays.",
    },
}

SOURCE_EXTS = {".h", ".hpp", ".cpp", ".cxx", ".cc", ".cs", ".py", ".json", ".md"}

def scan_file(path: Path) -> List[Dict[str, str]]:
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings
    for rule_name, rule in RULES.items():
        for pattern in rule["patterns"]:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                line_no = text.count("\n", 0, match.start()) + 1
                findings.append({
                    "rule": rule_name,
                    "severity": rule["severity"],
                    "file": str(path),
                    "line": str(line_no),
                    "message": rule["message"],
                })
    return findings

def collect_findings(repo: Path) -> List[Dict[str, str]]:
    findings = []
    for path in repo.rglob("*"):
        if path.is_file() and path.suffix.lower() in SOURCE_EXTS:
            findings.extend(scan_file(path))
    return findings

def build_report(repo: Path, findings: List[Dict[str, str]]) -> str:
    lines = [
        "# Master Repo Compliance Report",
        "",
        f"Repo scanned: `{repo}`",
        "",
        "## Summary",
        "",
        f"- Files scanned: {sum(1 for p in repo.rglob('*') if p.is_file() and p.suffix.lower() in SOURCE_EXTS)}",
        f"- Findings: {len(findings)}",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("No findings from the current lightweight ruleset.")
    else:
        for f in findings:
            lines.append(
                f"- **{f['severity'].upper()}** `{f['rule']}` — `{f['file']}:{f['line']}` — {f['message']}"
            )
    lines += [
        "",
        "## Manual review prompts",
        "",
        "- Do major runtime systems use centralized state/input/interaction flow?",
        "- Are gameplay values pulled from config rather than hardcoded?",
        "- Is rig terminology used consistently instead of generic suit wording?",
        "- Do stateful systems expose save/load hooks?",
        "- Do major systems expose enough debug visibility?",
        "",
    ]
    return "\n".join(lines) + "\n"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    repo = Path(args.repo)
    findings = collect_findings(repo)
    report = build_report(repo, findings)
    Path(args.out).write_text(report, encoding="utf-8")

if __name__ == "__main__":
    main()
